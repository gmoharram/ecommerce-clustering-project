# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 03:03:23 2021

@author: gmoha
"""
import pandas as pd 
import numpy as np
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


## check if there are items with negative quantities
N = X < 0
loc = np.argwhere(N == True)
# creates array with rows where there are negative quantities and the corresponding counts 
negative_indices = np.column_stack(np.unique(loc[:,0], return_counts = True))
#Only keep rows with exclusively positive quantities
X= np.delete(X, negative_indices[:,0], axis = 0)


##Remove item that has only been purchased once at a quantity of 80995 and belonging invoice row 
X = np.delete(X, 20756, axis = 0)
X = np.delete(X, 4068, axis = 1)

#Save Feature Matrix to .pckl file for future use
with open('pckl_variables/FeatureMatrix.pckl', 'wb') as f:
    pickle.dump(X, f)
    f.close()
    