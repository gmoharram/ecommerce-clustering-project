import numpy as np
import pickle

from NormalizeMatrixColumns import normalizeColumns 
from wss import calculate_wss

#Using Scikit-learn
from sklearn.cluster import KMeans



#Import data 
with open('pckl_variables/FeatureMatrix.pckl', 'rb') as f:
    [X, columns] = pickle.load(f)
    f.close()
        

#Only include data points with at least 3 items
Y = np.where(X > 0, 1, X) #Remove Quantity Information, only yes (1) or no (0)
X = X[Y.sum(1) >= 3] #only consider purchases with at least 3 different items


#Normalizing the Feature Matrix columns
(X, X_norm) = normalizeColumns(X) 


#Dictionary to store amount of meaningful clusters and their sizes for each k
d_amounts = {}
#Dictiionary to store Within-Cluster-Sum of Squared Errors (WSS) for each k
d_wss = {}

#what k-values to look at
k_start = 700
k_step = 20
steps = 5

# perform clustering with different number of centroids k
for i in range(steps):

   #scikit KMeans
   k = k_start + i*k_step
   kmeans = KMeans(n_clusters = k, init = 'k-means++', n_init = 5, max_iter = 300).fit(X)

   centroids = kmeans.cluster_centers_
   centroids[np.abs(centroids) < 0.0001] = 0 # Remove near zero values
   labels = kmeans.labels_

   #Find Cluster Sizes
   amounts = np.zeros(kmeans.n_clusters)
   for i in labels:
       amounts[i] += 1
    
   #Only look at Clusters with at least 3 data points
   cluster_amounts = amounts[amounts > 3] 
   
   #append to dictionary
   d_amounts[k] = cluster_amounts
   
   #Save wss at k
   d_wss[k] = calculate_wss(X, centroids, labels)
   
   #Keep track of progress
   print("{0} clustering done!".format(k))
    
#Save cluster amount results for this k-value for comparison 
with open('pckl_variables/kMeans_amounts_wss_{0}_{1}_{2}.pckl'.format(k_start, k, k_step), 'wb') as f:
    pickle.dump(d_amounts, d_wss, f)
    f.close()
        
    
    
    
