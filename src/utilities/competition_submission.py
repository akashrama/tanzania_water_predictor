import pickle 
import pandas as pd
import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV, cross_val_score
# from sklearn.ensemble import BaggingClassifier
# from sklearn.metrics import recall_score, hamming_loss, f1_score, precision_score 
from src.utilities import data_cleaning

def submit_test_data(model):
    
    # Testing data
    test_df = pd.read_csv('../../../data/raw/test_set.csv') 
    id_df = pd.DataFrame(test_df[['id', 'region']])
    clean_test = data_cleaning.clean_all_data(test_df)
    encoded_test = data_cleaning.encode_data(clean_test)
    print("data is cleaned and encoded")

    # Prediction for test data
    prediction = model.predict(encoded_test)
    print("Prediction for test data finished")


    ### Making submission file###
    # Dataframe as per submission format
    id_df['status_group']=prediction
    submission_df = id_df.drop('region', axis=1)
    

    # Store submission dataframe into file
    submission_df.to_csv("../../../data/processed/submission_set.csv", index = False)
    print("Store submission dataframe into file: successfully")