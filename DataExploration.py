# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 03:02:17 2021

@author: gmoha
"""


import numpy as np
from matplotlib import pyplot as plt
plt.style.use('ggplot') #choose plot style


import pickle #to store and access variables in .pckl files

with open('pckl_variables/FeatureMatrix.pckl', 'rb') as f:
    [X, columns] = pickle.load(f)
    f.close()




#Remove quantity information (Only purchased: 1, not purchased: 0)
Y = np.where(X > 0, 1, X)


## Different items purchased 
diff_items = np.sum(Y, axis = 1)
mean_diff_items = np.mean(diff_items)
median_diff_items = np.median(diff_items)
diff_items_counts = np.column_stack(np.unique(diff_items, return_counts = True))
maxim = np.max(diff_items_counts[:,1])

#PLOTS
fig,ax = plt.subplots()
ax.bar(diff_items_counts[:,0], diff_items_counts[:,1], width = 2)
ax.set_title('Different Items Distribution')
ax.set_ylabel('# of invoices')
ax.set_xlabel('# of different items')
ax.set_xlim(xmin = 0, xmax = np.max(diff_items))  
ax.set_ylim(ymin = 0, ymax = np.max(diff_items_counts[:,1]))
#mid section
fig2,ax2 = plt.subplots()
ax2.bar(diff_items_counts[2:220,0], diff_items_counts[2:220,1], width = 2)
ax2.set_title('Different Items Distribution')
ax2.set_ylabel('# of invoices')
ax2.set_xlabel('# of different items')
ax2.set_xlim(xmin = 0, xmax = np.max(diff_items_counts[2:220, 0]))  
ax2.set_ylim(ymin = 0, ymax = np.max(diff_items_counts[2:220,1]))



##Mean Quantity of item when purchased 
mean_quantity = np.zeros(X.shape[1]) 
std_dev_quantity = np.zeros(X.shape[1]) 
for i in range(X.shape[1]):
    select = np.array(np.where(X[:,i] != 0))   
    mean_quantity[i] = np.mean(X[select, i])
    std_dev_quantity[i] = np.std(X[select, i])
    
#PLOTS
fig3, ax3 = plt.subplots()
ax3.scatter(np.arange(X.shape[1]), mean_quantity)
ax3.set_title('Mean Quantities Purchased')
ax3.set_ylabel('Mean Quantity')
ax3.set_xlabel('Item Number')