from datetime import datetime
import os
import re
import pandas as pd
import numpy as np
import collections as co
import warnings

def make_dataset(stn_no):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    day = 24 * 60 * 60
    year = (365.2425) * day

    files = os.listdir('data/{0}/'.format(stn_no))
    
    file_obs = None    
    ptn = 'obs_{0}.csv'.format(stn_no)
    for file in files:
        if ptn in file:
            file_obs = file            
            break
            
    if file_obs: 
        print('Observation file found: {0}.'.format(file_obs))
    else:
        print('Error: observation file not found.')
        sys.exit(1)
    
    df_obs = pd.read_csv('data/{0}/'.format(stn_no) + file_obs)

    file_prd = None
    ptn = r'{}_(\d{{8}})_00UTC.csv'.format(stn_no)
    one = co.deque([])
    for file in files:
        if re.search(ptn, file):
            file_prd = file            
            print('Processing ECMWF file: {0}.'.format(file_prd), end='\r')
            df_prd = pd.read_csv('data/{0}/'.format(stn_no) + file_prd)
            
            arr = np.zeros((48, 2 + 96 + 1 + 2 + 2)) # date + 2 * 24 * 2 + offset + 2 + target + month
            date = df_prd.iloc[0, 0]
            timestamp = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()
            
            date_first = date
            date_last = df_prd.iloc[71, 0]
            
            idx_first = df_obs[df_obs[df_obs.columns[0]] == date_first].index
            idx_last = df_obs[df_obs[df_obs.columns[0]] == date_last].index
            
            if len(idx_first) == 0 or len(idx_last) == 0:
                continue
            if (idx_last - idx_first != 71):
                continue
            
            for j in range(48):
                arr[j, 0] = np.sin(timestamp * (2 * np.pi / year))
                arr[j, 1] = np.cos(timestamp * (2 * np.pi / year))
                for k in range(24):
                    arr[j, 2 + k] = df_prd.iloc[k, 1]
                    arr[j, 2 + 24 + k] = df_prd.iloc[k, 2]
                    arr[j, 2 + 48 + k] = df_obs.iloc[idx_first + k, 1]
                    arr[j, 2 + 72 + k] = df_obs.iloc[idx_first + k, 2]
                arr[j, 98] = j + 24
                arr[j, 99] = df_prd.iloc[24 + j, 1]
                arr[j, 100] = df_prd.iloc[24 + j, 2]
                arr[j, 101] = df_obs.iloc[idx_first + 24 + j, 1]
                arr[j, 102] = df_obs.iloc[idx_first + 24 + j, 2]
            one.append(pd.DataFrame(arr))
            
    df = pd.concat(one, ignore_index=True)
    df = df.dropna()
    df.to_csv('data/{0}/train_{0}.csv'.format(stn_no), index=False)
    
    if file_prd: 
        print('\nGenerated data/train_{0}.csv'.format(stn_no))
    else:
        print('Error: ECMWF file not found.')
        sys.exit(1) 
