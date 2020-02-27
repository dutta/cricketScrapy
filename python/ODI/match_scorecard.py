import requests
import pandas as pd
import json 
import re
import pathlib

def match_scorecard(series_id, match_id):
    a = requests.get('http://site.api.espn.com/apis/site/v2/sports/cricket/%s/summary?contentorigin=espn&event=%s' % (series_id,match_id))
    data = json.loads(a.text)
    rosters = data['rosters']
    res = []
    #print(rosters)
    for team in rosters:
        #print(team.keys())
        team_name = team['team']['displayName']
        for player in team['roster']:
            player_row = {}
            player_row['team'] = team_name
            if(player['captain'] == True):
                player_row['role'] = 'Captain'
            player_row['player'] = player['athlete']['name']
            player_row['player_id'] = player['athlete']['id']
            player_row['batting_style'] = player['athlete']['style'][0]['shortDescription']
            if(player['position']['id'] == "WK"):
                player_row['role'] = "WK"
            try: battingInnings = 'First Innings' if player['linescores'][0]['statistics']['categories'][0]['name'] == 'batting' else 'Second Innings'
            except: print(player)
            batting_line_score_index = 0 if player['linescores'][0]['statistics']['categories'][0]['name'] == 'batting' else 1
            bowling_line_score_index = 1 if player['linescores'][0]['statistics']['categories'][0]['name'] == 'batting' else 0
            player_row['batting_innings'] = battingInnings
            player_row['batting_position'] = player['linescores'][batting_line_score_index]['statistics']['categories'][0]['stats'][3]['value']
            if('batting' in player['linescores'][batting_line_score_index]['statistics']):
                player_row['runs_scored'] = int(player['linescores'][batting_line_score_index]['statistics']['categories'][0]['stats'][29]['value'])
                player_row['balls_faced'] = int(player['linescores'][batting_line_score_index]['statistics']['categories'][0]['stats'][0]['value'])
                player_row['minutes'] = int(player['linescores'][batting_line_score_index]['statistics']['categories'][0]['stats'][23]['value'])
                player_row['fours'] = int(player['linescores'][batting_line_score_index]['statistics']['categories'][0]['stats'][13]['value'])
                player_row['sixes'] = int(player['linescores'][batting_line_score_index]['statistics']['categories'][0]['stats'][30]['value'])
                player_row['strike_rate'] = player['linescores'][batting_line_score_index]['statistics']['categories'][0]['stats'][31]['value']

            if('bowling' in player['linescores'][bowling_line_score_index]['statistics']):
                #player_row['bowled?'] = True
                player_row['overs_bowled'] = player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][32]['value']
                player_row['maidens'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][28]['value'])
                player_row['runs_conceded'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][12]['value'])
                player_row['wickets'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][38]['value'])
                player_row['econ'] = player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][15]['value']
                player_row['0s_conceded'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][14]['value'])
                player_row['4s_conceded'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][19]['value'])
                player_row['6s_conceded'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][34]['value'])
                player_row['wides'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][39]['value'])
                player_row['no_balls'] = int(player['linescores'][bowling_line_score_index]['statistics']['categories'][0]['stats'][30]['value'])

            res.append(player_row)
    res_df = pd.DataFrame(res)
    return res_df
    # Path("./gameFiles/ODI/").mkdir(parents=True, exist_ok=True)
    # res_df.to_csv('./gamefiles/ODI/%s-scorecard.csv'% matchName)