# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:38:20 2021

@author: gmoha
"""

import pickle

from matplotlib import pyplot as plt
plt.style.use('ggplot') #choose plot style

#Open results from kMeans clustering for k= 400,780,20 to compare in dictionary

d_amounts = {} 
d_wss = {}

with open('pckl_variables/kMeans_amounts_wss_start_stop_step.pckl' ,'rb') as f:
    d_amounts, d_wss = pickle.load(f)
    f.close()


#Looked at values for k
k = list(d_amounts.keys())

#Obtained amount of meaningful clusters N for each k
clusters_N = []
for i in k:
    clusters_N.append(d_amounts[i].size)

#Mean meaningful cluster size for each k
mean_size = []
iteration = 0
for i in k:
    mean = (d_amounts[i].sum() - d_amounts[i].max())/(clusters_N[iteration] - 1)  #Not counting cluster with majority of datapoints
    mean_size.append(mean) 
    iteration += 1
    
#Mulitply mean size with cluster amount for each k
mean_N_multiplied = []
for i in range(len(mean_size)):
    mean_N_multiplied.append(mean_size[i]*(clusters_N[i] - 1))
    
#Calculate what fraction of the k centroids are surrounded by meaningful clusters for each k
fraction_meaningful = []
for i in k:
    fraction_meaningful.append(d_amounts[i].size / i)
    
#Calculate marginal increase in cluster amounts 
marginal_amounts = []
for i in k:
    if i == 400:
        prev = i
        marginal_amounts.append(0)
    else:
        marginal_amounts.append((d_amounts[i].size - d_amounts[prev].size)/(i - prev))
        prev = i
        
#Calculate marignal increase in datapoints meaningfully clustered (NS)        
marginal_NS = []
for i in range(len(mean_size)):
    if i == 0:
        marginal_NS.append(0)
    else:
        marginal_NS.append((mean_N_multiplied[i] - mean_N_multiplied[i-1])/(k[i]-k[i-1]))
    

with open('pckl_variables/k_N_S_NS.pckl', 'wb') as f:
    pickle.dump([k, clusters_N, mean_size, mean_N_multiplied], f)
    f.close()
    
#Calculate change in wss value
wss_change = {}
kstart = list(d_wss.keys())[0]
kstep  = 50
kstop = list(d_wss.keys())[-1]
for i in range(kstart,kstop,kstep):
    x = i + kstep/2
    change = (d_wss[i + kstep] - d_wss[i])/kstep
    wss_change[x] = change
    
    
    
    
    

figA, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_title('Amount of Clusters N and their Mean Sizes S')
ax1.set_xlabel('K-value')
ax1.set_ylabel('Cluster Amount N', color=color)
ax1.plot(k, clusters_N, color = color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('Mean Cluster Size S', color=color)  # we already handled the x-label with ax1
ax2.plot(k, mean_size, color=color)
ax2.tick_params(axis='y', labelcolor=color)

figA.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()


figB,ax3 = plt.subplots()
ax3.bar(k, mean_N_multiplied, width = 10)
ax3.set_title('Amount of Data Points Clustered (NS-value)')
ax3.set_ylabel('Ns-value')
ax3.set_xlabel('K-value')

figC,ax4 = plt.subplots()
ax4.bar(k, fraction_meaningful, width = 10)
ax4.set_title('Fraction of Meaningful Clusters')
ax4.set_ylabel('Fraction F')
ax4.set_xlabel('K-value')

figD,ax5 = plt.subplots()
ax5.plot(k, abs(marginal_NS))
ax5.set_title('Marginal Change of Meaningfully Clustered Data Points')
ax5.set_ylabel('Change C')
ax5.set_xlabel('K-value')


#Plot obtained wss-values
figE,ax6 = plt.subplots()
ax6.plot(list(d_wss.keys()), list(d_wss.values()))
ax6.set_title('Within-Cluster-Sum of Squared Errors (WSS) at different k-values')
ax6.set_ylabel('WSS')
ax6.set_xlabel('k')

#Plot change in wss-values
fig,ax = plt.subplots()
ax.scatter(list(wss_change.keys()), list(wss_change.values()))
ax.set_title('Change in WSS at different k-values')
ax.set_ylabel('Change in WSS')
ax.set_ylim([-1.3 ,0.1])
ax.set_xlabel('k')


