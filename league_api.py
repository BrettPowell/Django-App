from requests import get
from sys import argv

import abc
import argparse
import json
import os

class CacheSystem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_cached_version(self):
         """Retrieve data from the input source
        and return an object.
        """

    @abc.abstractmethod
    def set_cached_version(self, info):
        """Save the data object to the output."""


@CacheSystem.register
class WriteFile():
    def __init__(self):
        self.filename = 'match_history'

    def get_cached_version(self):
        with open(self.filename, 'r') as f:
            jsonified_game_info = f.read()
            f.closed
        return json.loads(jsonified_game_info)

    def set_cached_version(self, game_info):
        jsonified_game_info = json.dumps(game_info)
        f = open(self.filename, 'w')
        f.write(jsonified_game_info)

def api_call(endpoint):

    header = {"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8", "X-Riot-Token": os.environ.get('Riot_API_Key')}
    return get('https://na1.api.riotgames.com/lol/{}'.format(endpoint), headers=header).json()

def new_api_data(cache, summoner):
    user_info = api_call('summoner/v3/summoners/by-name/{}'.format(summoner))
    history = api_call('match/v3/matchlists/by-account/{}'.format(user_info['accountId']))
    game_info = {}
    last_ten = history['matches'][:5]
    index = 0
    for game in last_ten:
        game_info[index] = api_call('match/v3/matches/{}'.format(game['gameId']))
        index += 1

    #Now we got new data set update the cache
    cache.set_cached_version(game_info)
    return game_info

def get_match_history(cache, summoner, get_new_data):
    if get_new_data:
        return new_api_data(cache, summoner)
    try:
        game_info = cache.get_cached_version()
        return game_info
    except FileNotFoundError:
        print("Couldn't find cache file making api call")
        return new_api_data(cache, summoner)

def get_champion_played(match_history, summoner):
    champion_list = []
    for game in match_history:
        participant_id = _get_participant_id(match_history[game], summoner)
        for player in match_history[game]['participants']:
            if player['participantId'] == participant_id:
                champ = api_call('static-data/v3/champions/{}'.format(player['championId']))
                champ.get('name', 'Rate limit')
                champion_list.append(champ['name'])
    return champion_list


def _get_participant_id(game_info, summoner):
    for participant in game_info['participantIdentities']:
        if participant['player']['summonerName'] == summoner:
            return participant['participantId']

def win_lose(summoner, match_history):
    summoner_information = []
    index = 0
    for game in match_history:
        participant_id = _get_participant_id(match_history[game], summoner)
        for players in match_history[game]['participants']:
            if players['participantId'] == participant_id:
                if players['stats']['win']:
                    summoner_information.append('won')
                else:
                    summoner_information.append('lost')
        index += 1
    return summoner_information

def merge_information(game_data):
    for game in game_data:
        ### Messing with output
        print(game)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Getting info from League API')
    parser.add_argument('summoner', type=str,
                    help='Input a summoner you would like to lookup')

    # Store_true means the arguement is true when the flag is present in the request
    parser.add_argument('--purge', help='Get new API data', action='store_true')
    args = parser.parse_args()
    game_data = []
    summoner = args.summoner
    cache = WriteFile()
    match_history = get_match_history(cache, summoner, args.purge)
    game_data.append(get_champion_played(match_history, summoner))
    game_data.append(win_lose(summoner, match_history))
    game_results = zip(game_data[0], game_data[1])
    print(list(game_results))
