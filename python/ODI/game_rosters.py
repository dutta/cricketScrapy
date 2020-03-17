import requests
import pandas as pd
import json 
import re
import pathlib


def game_rosters(series_id,match_id):
    a = requests.get("http://www.espncricinfo.com/matches/engine/match/%s.json" % match_id)
    data = json.loads(a.text)

    team1_data = {}
    team2_data = {}
    #### TEAM 1 ####
    team1 = data['team'][0]
    team1_data['team_name'] = team1['team_name']
    team1_data['athlete_info_list'] = []
    team1_data['roster_list'] = []
    for player in team1['player']:
        team1_data['athlete_info_list'].append(player)
        team1_data['roster_list'].append(player['card_long'])

    #### TEAM 2 ####
    team2 = data['team'][1]
    team2_data['team_name'] = team2['team_name']
    team2_data['athlete_info_list'] = []
    team2_data['roster_list'] = []
    for player in team2['player']:
        team2_data['athlete_info_list'].append(player)
        team2_data['roster_list'].append(player['card_long'])

    res = {'team_1' : team1_data, 'team_2' : team2_data}
    return res
    # print(res['team_1']['roster_list'])
    # print(res['team_2']['roster_list'])

#game_rosters('19754','1214668')