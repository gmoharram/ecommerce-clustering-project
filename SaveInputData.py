# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 03:03:23 2021

@author: gmoha
"""
import pandas as pd 
import pickle

#Import data and remove invoice number info and Discount Column
df = pd.read_excel('order_baskets.csv')
df.drop(columns =['Unnamed: 0', 'D'], axis=1, inplace = True) 

#Save to pickle file
with open('pckl_variables/loaded_baskets_df.pckl', 'wb') as f:
   pickle.dump(df, f)
   f.close()
   
'''
GET df WITH:

with open('pckl_variables/loaded_baskets_df.pckl', 'rb') as f:
    df = pickle.load(f)
    f.close()
    
'''
   
   
#Create numpy feature matrix out of df
X = df.to_numpy()

#Save Feature Matrix to .pckl file for future use
with open('pckl_variables/FeatureMatrix.pckl', 'wb') as f:
    pickle.dump(X, f)
    f.close()
    