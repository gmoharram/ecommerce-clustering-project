# ecommerce-clustering-project
This is a python clustering project that uses the Online Retail Data Set available at [UCI ML Rep.](https://archive.ics.uci.edu/ml/datasets/online+retail#)
Source:  Dr Daqing Chen, Director: Public Analytics group. chend '@' lsbu.ac.uk, School of Engineering, London South Bank University, London SE1 0AA, UK.

We will be using the numpy, pandas, scikit-learn, matplotlib and pickle libraries. 

1. [Data Cleaning](https://github.com/gmoharram/ecommerce-clustering-project#data-cleaning)

2. [Data Exploration](https://github.com/gmoharram/ecommerce-clustering-project#data-exploration)

3. [Clustering](https://github.com/gmoharram/ecommerce-clustering-project#data-exploration)

## Data Cleaning

The Data Set is an excel sheet where each row represents an item . The for this project relevant columns are the "Stock Code", "Quantity"and "InvoiceNo" columns. We aim to create a matrix, where each row represents an Invoice Number and all Stock Codes are assigned a column. The cell values will be the Quantity information. In the following we will refer to each row as a "basket". This is performed with the [dataPrep.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/dataPrep.py) script. A screenshot of the obtained file is shown below. 

![Baskets](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/2021-01-07.png "Baskets")


#### Discount Code

In total we find 25900 different invoices and 4071 different items. However, one of the items has the Stock Code 'D' which signifies that a discount code was used. After dropping the discount column and invoice Number column we generate a 25900 by 4069 pandas dataframe. Throughout this project we will save some generated variables in .pckl files using the [pickle module](https://docs.python.org/3/library/pickle.html) which serializes python objects. While this generates relatively large files, it saves massive amounts of processing time. This process is performed by [SaveInputData.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/SaveInputData.py).

#### Negative Quantities

While trying to compute the average number of different items purchased I suspected that there might be negative quantity values in our data set. That was indeed the case. There were 5108 unique invoice numbers that contained negative quantities. While most of these only had one stock item for which that was true, there were others with up to 101 such cases. It is not stated at the data source, how these values are to be interpreted. One interpretation could be that those items were returned at purchase. While we could change those values to zero, I chose to ignore those invoice numbers, leaving us with 20792 data points. 

#### Never Purchased Items

Furthermore, we delete all empty columns. These items have never been purchased and need not be considered in our centroid search. After performing that step we are left with 3941 columns. 

#### Miscellaneous

Additionally, there was one item (Stock Code '23843') that was purchased a single time at an exorbitant quantity of 80995 and then immediately thereafter returned. I noticed this while computing the mean quantities purchased of each item. That item column along with the belonging invoice number row was dicarded to avoid shifting a centroid in its direction. 

## Data Exploration

After doing the initital cleaning we now aim to understand our data better. This gives us a chance to spot any problems with our data set. Some of the data cleaning above was based on what I came across while exploring the data. It also gives us an idea of what we expect to see once our data is fitted, which is an important way to understand what outcomes are sensible. The exploration was performed with the [DataExploration.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/DataExploration.py) script.

#### Basket Sizes

It might be helpful to get an idea as to how big customers baskets can be. Specifically, we'll quickly look at how many different items are typically purchased together and what kind of quantities they are purchased at. 

A quick analysis shows that while the mean amount of different items purchased is at around 25, the median is at 15. The bar plots below depicts the number of invoices with a given number of different items. While the first one takes all data points into account, the second zooms into the item counts with significant number of invoices. 

<p align="center">
  <img width="400" height="300" src="https://github.com/gmoharram/ecommerce-clustering-project/blob/main/DifferentDistribution.png">
  <img width="400" height="300" src="https://github.com/gmoharram/ecommerce-clustering-project/blob/main/DifferentDistributionMiddle.png">
</p>


#### Mean Quantities

The mean quantities usually purchased of each item gives us an idea of where to realistically expect our centroids to be. For it to be a useful number we only include non-zero numbers when taking the mean. However, the feature matrix will be normalized before running the clustering algorithm and so those numbers (and more importantly how they compare to eachother) should have no effect on the centroid location and therefore only serves as a metric for comparison. 


<p align="center">
  <img width="450" height="350" src="https://github.com/gmoharram/ecommerce-clustering-project/blob/main/MeanQuantities.png">
</p>

## Clustering 

The previous steps have left us with a 17504 by 3940 numpy array which is ready to be fitted. We will now use the [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans) Clustering Algorithm from the Scikit-learn module to ensure high efficieny. For a basic implementation in python take a look at my [Python-Clustering-Algorithm](https://github.com/gmoharram/Python-Clustering-Algorithm). We shouldn't expect our data to consist of several (even hundreds) of perfect clusters. Instead we expect there to be a few well defined clusters with a meaningful amount of data points but otherwise unrelated purchases. To ensure that we find those few meaningful cluster centroids for any given k, the clustering algorithm is run several times with different initial centroids. The fit with the lowest clustering loss function value is automatically chosen. 

#### Choosing K

However, there is still the issue of choosing an appropriate value for k. I've chosen to run the algorithm with incrementally higher values for k [initialClustering.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/initialClustering.py) and then look at how many "meaningful" 
clusters are found. I've conservatively defined "meaningful" to mean consisting of more than three data points. Below is a graph of the amount N of meaningful clusters generated at a given k-value along with the mean size S of those clusters. Finally, the rest of the analysis is performed with the k-value with the greatest NS value  (or the greatest amount of datapoins assigned to meaningful clusters). For all k-values there was one centroid where most datapoints (thousands) were clustered. This is just the average of all data points that weren't succesfully assigned to a cluster and could mean a lot of one-element clusters that are presumably close to zero (a small-volume/ one-item purchase for example). I've left this one out of my meaningful clusters calculations. While there might be information hidden in that cluster, this can be minimized by choosing an adequate k-value and performing the clustering with many initial centroids. The comparison is performed by [inititalClusteringKComparison.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/initialClusteringKComparison.py). 

<p align="center">
  <img width="400" height="300" src="https://github.com/gmoharram/ecommerce-clustering-project/blob/main/AmountClustersNmeanSizeS.png">
  <img width="400" height="300" src="https://github.com/gmoharram/ecommerce-clustering-project/blob/main/NSvalues.png">
</p>

As we can see on the left graph increasing the centroid number k continuously (fluctuations are due to imperfect clustering) increases the amount of clusters with more than 3 data points. However, we can also see that the mean size of those clusters is continuously decreasing. This is a clear indication that the information gained by increasing k is diminishing. One the right graph, where the total data points "meaningfully" clustered at a given k is shown, this is confirmed. Additionally, there could be the case where initially bigger clusters are broken down further. While this is the intention to some extent, there is a point at which that becomes excessive, since some variation withing a cluster is essential. In hindsight, I would recommend setting the meaningful cluster threshold considerably higher than 4 given the size of our data set. This would cause the N-graph to plateau considerably faster and we might possibly see it decrease at the picked out k-values. I also recommend performing the initial clusterings in phases since it does take some time. 

Finally, we'll look at the difference in the total data points meaningfully clustered (derivative of the NS-function). 

<p align="center">
  <img width="450" height="350" src="https://github.com/gmoharram/ecommerce-clustering-project/blob/main/MarginalDataPoints.png">
</p>

Again, the flucuations (negative changes) are due to imperfect clustering. Ultimately, we pick k = 1350. 
