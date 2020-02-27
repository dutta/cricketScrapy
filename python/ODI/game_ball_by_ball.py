import requests
import pandas as pd
import json 
import re
import pathlib

"""
Gets all ball_by_ball context from a given match (also requires the seriesID, it is possible there are two matches with the same number)
"""
def game_ball_by_ball(series_id, match_id):
    a = requests.get('http://site.api.espn.com/apis/site/v2/sports/cricket/%s/playbyplay?contentorigin=espn&event=%s' % (series_id,match_id))
    data = json.loads(a.text)
    pages = int(data['commentary']['pageCount'])
    res = []
    for i in range(1,pages+1): 
        page = requests.get('http://site.api.espn.com/apis/site/v2/sports/cricket/%s/playbyplay?contentorigin=espn&event=%s&page=%s' % (series_id,match_id,i))
        page_data = json.loads(page.text)
        try: items = page_data['commentary']['items']
        except Exception: print(page_data)
        for evs in items:
            ball_res = {'ball': evs['innings']['balls']}
            try: ball_res['playType'] = evs['playType']['description']
            except Exception: pass
            try: ball_res['innings'] = evs['periodText']
            except Exception: pass
            try: score = evs['homeScore'] if '/' in evs['homeScore'] else evs['awayScore']
            except Exception: pass
            try: ball_res['score'] = score
            except Exception: pass
            try: ball_res['runs'] = score.split('/')[0]
            except Exception: pass
            try: ball_res['wickets'] = score.split('/')[1]
            except Exception: pass
            try: ball_res['runs_scored'] = evs['scoreValue']
            except Exception: pass
            try: ball_res['bowler'] = evs['bowler']['athlete']['name']
            except Exception: pass
            try: ball_res['bowler_id'] = evs['bowler']['athlete']['id']
            except Exception: pass
            try: ball_res['batsman'] = evs['batsman']['athlete']['name']
            except Exception: pass
            try: ball_res['batsman_id'] = evs['batsman']['athlete']['id']
            except Exception: pass
            try: ball_res['overs'] = evs['over']['overs']
            except Exception: pass
            try: ball_res['shortText'] = evs['shortText']
            except Exception: pass
            try: text1 = evs['shortText']
            except Exception: pass
            try: text2 = evs['text']
            except Exception: text2 = ""
            try: ball_res['text'] = text2
            except Exception: pass

            try: ball_res['commentary'] = text1 + ' ' + text2
            except Exception: pass
            try: speeds1 = re.findall('[0-9]{3}kph',ball_res['commentary'])
            except Exception: pass
            try: speeds2 = re.findall('[0-9]{2}kph',ball_res['commentary'])
            except Exception: pass
            
            try: 
                ball_res['speed'] = speeds1[0] if len(speeds1) > 0 else (speeds2[0] if len(speeds2) > 0 else None)
                res.append(ball_res)
            except Exception: pass

    res_df = pd.DataFrame(res)
    return res_df
    #Path("./gameFiles/ODI/").mkdir(parents=True, exist_ok=True)
    #res_df.to_csv('./gamefiles/ODI/%s-ballbyball.csv'% matchName)


