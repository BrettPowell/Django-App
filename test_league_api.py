import unittest
from . import league_api

class LeagueApi(unittest.TestCase):

    def test_get_participant_id(self):
        pass

    def test_win_lose_champ(self):
        pass

    #def test_get_match_history(self):
        #summoner = 'SEALTEAMLEADER'
        #self.cache = league_api.WriteFile()
        #expected = league_api.get_match_history(self.cache, summoner, True)
        #actual = league_api.get_match_history(self.cache, summoner, False)
        #self.assertEqual(expected, actual, msg="The stored data doesn't equal the api data. \n {} \n {}".format(expected, actual))
