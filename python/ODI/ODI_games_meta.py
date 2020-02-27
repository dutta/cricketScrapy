import requests
import json
import pandas as pd
from pathlib import Path
import re
import os

def ODI_games_meta(startingYear,endingYear=None):
    if(endingYear == None):
        endingYear = startingYear
    gameslist = []
    for year in range(startingYear,endingYear+1):
        a = requests.get('http://stats.espncricinfo.com/ci/engine/records/team/match_results.json?class=2;id=%s;type=year' % (year))
        data = a.text
        games = re.findall('<a href="/ci/engine/match/\d{1,10}.html" class="data-link">ODI # \d{4}</a>',data)
        gameslist.append(games)
    
    year_names = [x for x in range(startingYear,endingYear+1)]

    for listofGames in gameslist:
        res = []
        for game in listofGames:
            game_info = {}
            gameNumber = game.split("ODI # ")[1].split('<')[0]
            matchNumber = game.split('.html')[0].split('/')[-1]
            metadataUrl = "http://www.espncricinfo.com/matches/engine/match/%s.json" % (matchNumber)
            a = requests.get(metadataUrl)
            try: data = json.loads(a.text)
            except: continue
            seriesNumber = data['series'][0]['core_recreation_id']

            game_info['ODI_NUM'] = gameNumber
            game_info['matchNumber'] = matchNumber
            game_info['seriesNumber'] = seriesNumber
            game_info['description'] = data['description']
            game_info['ground_name'] = data['match']['ground_name']
            game_info['country_name'] = data['match']['country_name']
            game_info['date'] = data['match']['date']
            game_info['result_text'] = data['live']['status']
            game_info['win_type'] = data['match']['amount_name']
            game_info['win_amount'] = data['match']['amount']
            game_info['first_innings_runs'] = data['innings'][0]['runs']
            game_info['first_innings_wickets'] = data['innings'][0]['wickets']
            game_info['second_innings_runs'] = data['innings'][1]['runs']
            game_info['second_innings_wickets'] = data['innings'][1]['wickets']
            batting_team_id = data['innings'][0]['batting_team_id']
            bowling_team_id = data['innings'][0]['bowling_team_id']
            winning_team_id = data['match']['winner_team_id']
            toss_winner_team_id = data['match']['toss_winner_team_id']
            batting_team = bowling_team = winning_Team = toss_team = None
            for team in data['team']:
                if(batting_team_id == team['team_id']):
                    batting_team = team['team_name']
                if(bowling_team_id == team['team_id']):
                    bowling_team = team['team_name']
                if(winning_team_id == team['team_id']):
                    winning_Team = team['team_name']
                if(toss_winner_team_id == team['team_id']):
                    toss_team = team['team_name']
            game_info['batting_team'] = batting_team
            game_info['bowling_team'] = bowling_team
            game_info['winner'] = winning_Team
            game_info['toss_winner'] = toss_team

            if(data['match']['rain_rule'] == '1'):
                game_info['D/L method'] = True

            res.append(game_info)
            print("META COLLECTING ODI # %s: %s" % (game_info['ODI_NUM'],game_info['result_text']))
        res_df = pd.DataFrame(res)
        # Path("./gameFiles/").mkdir(parents=True, exist_ok=True)
        # res_df.to_csv('./gamefiles/all_games_metadata-%d.csv' % year_names[count])
        #count += 1
        return res_df

