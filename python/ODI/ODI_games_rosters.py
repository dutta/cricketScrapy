import requests
import json
import pandas as pd
from pathlib import Path
import re
import os
import pickle
import traceback
from game_rosters import game_rosters
from ODI_games_meta import ODI_games_meta
import time 
import multiprocessing

def get_rosters(row):
    matchNumber = row[0]
    seriesNumber = row[1]
    matchName = row[2]
    print(matchName)
    try: 
        bb = game_rosters(seriesNumber,matchNumber)
    except: 
        print("ERROR IN ROSTERS FOR NUMBER %s" % matchName)
        traceback.print_exc()

    Path("./data/rosters").mkdir(parents=True, exist_ok=True)
    json.dump(bb, open( "./data/rosters/%s-rosters.json" % matchName, 'w' ) )


def ODI_get_all_rosters_as_json(startYear, endYear):
    for year in range(startYear,endYear+1):
        curr_df = ODI_games_meta(year)
        for row in curr_df.itertuples():
            get_rosters(row)
            

def multiprocesses_ODI_get_all_rosters_as_json(startYear, endYear):
    for year in range(startYear,endYear+1):
        curr_df = ODI_games_meta(year)
        starttime = time.time()
        pool = multiprocessing.Pool()
        work = [(x.matchNumber, x.seriesNumber,x.ODI_NUM) for x in curr_df.itertuples()]
        pool.map(get_rosters, work)
        pool.close()
        print('That took {} seconds'.format(time.time() - starttime))

multiprocesses_ODI_get_all_rosters_as_json(2010,2020)
    