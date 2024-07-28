from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import LinearSVR
from sklearn.pipeline import make_pipeline
import os
import pickle
import pandas as pd

def train_model(stn_no):
    train = pd.read_csv('data/{0}/train_{0}.csv'.format(stn_no))
    train_u = train.drop(['101', '102'], axis=1)
    label_u = train['101'].copy()
    train_v = train.drop(['101', '102'], axis=1)
    label_v = train['102'].copy()
    
    model_u = make_pipeline(StandardScaler(), PCA(n_components=0.98), LinearSVR(random_state=42, max_iter=16000))
    model_v = make_pipeline(StandardScaler(), PCA(n_components=0.98), LinearSVR(random_state=42, max_iter=16000))
        
    model_u.fit(train_u.values, label_u)
    print('Training a model_u for {0} . . .'.format(stn_no))
    model_v.fit(train_v.values, label_v)
    print('Training a model_v for {0} . . .'.format(stn_no))
    
    current_directory = os.getcwd()
    model_directory = os.path.join(current_directory, 'model')
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)
    
    with open('model/{0}.p'.format(stn_no), 'wb') as file:
        pickle.dump(model_u, file)
        pickle.dump(model_v, file)
    print('Generated models for {0}: model/{0}.p'.format(stn_no))
