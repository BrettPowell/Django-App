import os
import requests
from . import config, league_api
from requests import get

from django.http import HttpResponse

def try_this():
    summoner = 'SEALTEAMLEADER'
    game_data = []
    match_history = league_api.get_match_history(summoner)
    game_data.append(league_api.get_champion_played(match_history, summoner))
    game_data.append(league_api.win_lose(match_history, summoner))
    this_thing = '''
    <html>
    <head>
    <div> Me: {} </div> '''.format(summoner)
    print(game_data[0][0])
    #for game in game_data[0]:
        #this_thing += '''
        #<body>Champion played was {} and we {} the game </body><br />
        #'''.format(game[0], game[1])
        #this_thing += '''</style>
        #</head>'''

        #if players['participantId'] == participant_id:
            #this_thing += '''
            #<body>Creep score / minutes {}</body><br />
            #'''.format(players['timeline']['creepsPerMinDeltas'], players['timeline']['csDiffPerMinDeltas'])
            #this_thing += '''</style>
            #</head><br />'''
    return HttpResponse(this_thing)
