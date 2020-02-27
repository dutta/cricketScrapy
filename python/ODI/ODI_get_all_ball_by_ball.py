import requests
import json
import pandas as pd
from pathlib import Path
import re
import os
import traceback
import multiprocessing
import time

from game_ball_by_ball import game_ball_by_ball
from match_scorecard import match_scorecard
from ODI_games_meta import ODI_games_meta

def get_ball_by_ball(row):
    matchNumber = row[0]
    seriesNumber = row[1]
    matchName = row[2]
    print(matchName)
    try: 
        bb = game_ball_by_ball(seriesNumber,matchNumber)
    except: 
        print("ERROR IN BALLBYBALL FOR NUMBER %s" % matchName)
        traceback.print_exc()

    Path("./data/ball-by-ball").mkdir(parents=True, exist_ok=True)
    bb.to_csv('./data/ball-by-ball/%s-ball-by-ball.csv'% matchName)


def ODI_get_all_ball_by_ball_as_csv(startYear, endYear):
    for year in range(startYear,endYear+1):
        curr_df = ODI_games_meta(year)
        for row in curr_df.itertuples():
            
            get_ball_by_ball(row)
            

def multiprocesses_ODI_get_all_ball_by_ball_as_csv(startYear, endYear):
    for year in range(startYear,endYear+1):
        curr_df = ODI_games_meta(year)
        starttime = time.time()
        pool = multiprocessing.Pool()
        work = [(x.matchNumber, x.seriesNumber,x.ODI_NUM) for x in curr_df.itertuples()]
        pool.map(get_ball_by_ball, work)
        pool.close()
        print('That took {} seconds'.format(time.time() - starttime))

multiprocesses_ODI_get_all_ball_by_ball_as_csv(2016,2020)