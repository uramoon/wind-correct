from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVR
from sklearn.pipeline import make_pipeline
from datetime import datetime, timedelta
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys
import pickle
import pandas as pd
import numpy as np
import warnings

def correct_wind(mdl_no, stn_no, ymd):
    warnings.simplefilter(action='ignore', category=FutureWarning)

    with open('model/{0}.p'.format(mdl_no), 'rb') as file:
        model_u = pickle.load(file)
        model_v = pickle.load(file)
        
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, 'output')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    day = 24 * 60 * 60
    year = (365.2425) * day
    files = os.listdir('input/{0}/'.format(mdl_no))
   
    file_obs = None    
    ptn = 'obs_{0}.csv'.format(mdl_no)
    for file in files:
        if ptn in file:
            file_obs = file            
            break
            
    if file_obs: 
        print('Observation file found: {0}.'.format(file_obs))
    else:
        print('Error: observation file not found.')
        sys.exit(1)
    
    df_obs = pd.read_csv('input/{0}/'.format(mdl_no) + file_obs)
    
    files = os.listdir('input/{0}/'.format(stn_no))
    file_prd = None
    ptn = '{0}_{1}_00UTC.csv'.format(stn_no, ymd)
    for file in files:
        if ptn in file:
            file_prd = file            
            break
            
    if file_prd: 
        print('ECMWF file for target location found: {0}.'.format(file_prd))
    else:
        print('Error: ECMWF file for target location not found.')
        sys.exit(1)
    
    df_prd = pd.read_csv('input/{0}/'.format(stn_no) + file_prd)

    files = os.listdir('input/{0}/'.format(mdl_no))
    file_mdl = None
    ptn = '{0}_{1}_00UTC.csv'.format(mdl_no, ymd)
    for file in files:
        if ptn in file:
            file_mdl = file            
            break
            
    if file_mdl: 
        print('ECMWF file for model location found: {0}.'.format(file_mdl))
    else:
        print('Error: ECMWF file for model location not found.')
        sys.exit(1)

    df_mdl = pd.read_csv('input/{0}/'.format(mdl_no) + file_mdl)

    arr = np.zeros((48, 2 + 96 + 1 + 2)) # date + 2 * 24 * 2 + offset + 2 
    date = df_prd.iloc[0, 0]
    timestamp = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()
    
    date_first = date
    date_last = df_prd.iloc[23, 0]
            
    idx_first = df_obs[df_obs[df_obs.columns[0]] == date_first].index
    idx_last = df_obs[df_obs[df_obs.columns[0]] == date_last].index
    
    if len(idx_first) == 0 or len(idx_last) == 0:
        print('Error: {0} does not contain observations {1}:0h-23h'.format(file_obs, ymd))
        exit(1)
    if (idx_last - idx_first != 23):
        print('Error: {0} does not contain observations {1}:0h-23h'.format(file_obs, ymd))
        exit(1)
            
    for j in range(48):
        arr[j, 0] = np.sin(timestamp * (2 * np.pi / year))
        arr[j, 1] = np.cos(timestamp * (2 * np.pi / year))
        
        for k in range(24):
            arr[j, 2 + k] = df_mdl.iloc[k, 1]
            arr[j, 2 + 24 + k] = df_mdl.iloc[k, 2]
            arr[j, 2 + 48 + k] = df_obs.iloc[idx_first + k, 1]
            arr[j, 2 + 72 + k] = df_obs.iloc[idx_first + k, 2]
        arr[j, 98] = j + 24
        arr[j, 99] = df_prd.iloc[24 + j, 1]
        arr[j, 100] = df_prd.iloc[24 + j, 2]
    df = pd.DataFrame(arr)
    df = df.interpolate(axis=1)
    
    pred_u = model_u.predict(df)
    pred_v = model_v.predict(df)

    vector_a = df_prd.iloc[0:24, 1].values.reshape(1, -1)
    vector_b = df_mdl.iloc[0:24, 1].values.reshape(1, -1)
    cos_sim_u = cosine_similarity(vector_a, vector_b)[0][0]

    vector_a = df_prd.iloc[0:24, 2].values.reshape(1, -1)
    vector_b = df_mdl.iloc[0:24, 2].values.reshape(1, -1)
    cos_sim_v = cosine_similarity(vector_a, vector_b)[0][0]

    ori_u = df_prd.iloc[24:72, 1].values.reshape(-1)
    ori_v = df_prd.iloc[24:72, 2].values.reshape(-1)

    if cos_sim_u < 0:
        pred_u = ori_u
    else:
        w = 1 - cos_sim_u
        pred_u = ori_u * w + pred_u * (1 - w)

    if cos_sim_v < 0:
        pred_v = ori_v
    else:
        w = 1 - cos_sim_v
        pred_v = ori_v * w + pred_v * (1 - w)

    date = datetime.strptime(str(ymd), '%Y%m%d')
    date = date + timedelta(days=1)

    lst_date = []
    for j in range(48):
        dt = date + timedelta(hours=j)
        lst_date.append(dt.strftime('%Y-%m-%d %H:%M:%S'))        
    
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, 'output')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    filename_output = os.path.join(output_directory, '{0}p_{1}_{2}.csv'.format(mdl_no, stn_no, ymd))
    data = {'corr_fct': lst_date, 'corr_u': pred_u, 'corr_v': pred_v}
    df = pd.DataFrame(data)
    df.to_csv(filename_output, float_format='%.06f', index=False)
    print('Generated output/{0}p_{1}_{2}.csv'.format(mdl_no, stn_no, ymd))
