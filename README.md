# ecommerce-clustering-project
This is a quick python clustering project that uses the Online Retail Data Set available at [UCI ML Rep.](https://archive.ics.uci.edu/ml/datasets/online+retail#)
Source:  Dr Daqing Chen, Director: Public Analytics group. chend '@' lsbu.ac.uk, School of Engineering, London South Bank University, London SE1 0AA, UK.

We will be using the numpy, pandas, scikit-learn, matplotlib and pickle libraries. 

## Data Cleaning

The Data Set is an excel sheet where each row represents an item . The for this project relevant columns are the "Stock Code", "Quantity"and "InvoiceNo" columns. We aim to create a matrix, where each row represents an Invoice Number and all Stock Codes are assigned a column. The cell values will be the Quantity information. In the following we will refer to each row as a "basket". This is performed with the [dataPrep.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/dataPrep.py) script. A screenshot of the obtained file is shown below. 

![baskets](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/2021-01-07.png  "Obtained 'baskets' File")


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

### Basket Sizes

It might be helpful to get an idea as to how big customers baskets can be. Specifically, we'll quickly look at how many different items are typically purchased together and what kind of quantities they are purchased at. 

A quick analysis shows that while the mean amount of different items purchased is at around 25, the median is at 15. The bar plots below depicts the number of invoices with a given number of different items. While the first one takes all data points into account, the second zooms into the item counts with significant number of invoices. 


![Bar1](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/DifferentDistribution.png "All Data Bar Plot")


![Bar2](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/DifferentDistributionMiddle.png "Selected Data Bar Plot")


## Clustering 

Using the obtained "baskets" dataframe we now convert this into a numpy array. Since we only care about invoices where several items are purchased together, we only keep invoices where at least three different items were purchased. This leaves us with 17504 rows. The numpy array is now ready to be fitted. We will now use the [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans) Clustering Algorithm from the Scikit-learn module to ensure high efficieny. Take a look at my [Python-Clustering-Algorithm](https://github.com/gmoharram/Python-Clustering-Algorithm). For our purposes we will set k = 400. We shouldn't expect our data to consist of several (even hundreds) of perfect clusters. Instead we expect there to be a few well defined clusters with a meaningful amount of data points but otherwise unrelated purchases. To ensure that we find those few meaningful cluster centroids, the clustering algorithm will be run several times with several (highly likely) different randomly chosen initial centroids. The fit with the lowest clustering loss function value is automatically chosen. 


