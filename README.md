# ecommerce-clustering-project
This is a quick python clustering project that uses the Online Retail Data Set available at [UCI ML Rep.](https://archive.ics.uci.edu/ml/datasets/online+retail#)
Source:  Dr Daqing Chen, Director: Public Analytics group. chend '@' lsbu.ac.uk, School of Engineering, London South Bank University, London SE1 0AA, UK.

We will be using the numpy, pandas, scikit-learn, matplotlib and pickle libraries. 

## Data Cleaning

The Data Set is an excel sheet where each row represents an item . The for this project relevant columns are the "Stock Code", "Quantity"and "InvoiceNo" columns. We aim to create a matrix, where each row represents an Invoice Number and all Stock Codes are assigned a column. The cell values will be the Quantity information. In the following we will refer to each row as a "basket". This is performed with the [dataPrep.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/dataPrep.py) script. A screenshot of the obtained file is shown below. 

![baskets](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/2021-01-07.png  "Obtained 'baskets' File")

In total we find 25900 different invoices and 4070 different items. However, one of the items has the Stock Code 'D' which signifies that a discount code was used. After dropping the discount column we generate a 25900 by 4069 pandas dataframe. Throughout this project we will save some generated variables in .pckl files using the [pickle module](https://docs.python.org/3/library/pickle.html) which serializes python objects. While this generates relatively large files, it saves massive amounts of processing time.  

## Clustering 

Using the obtained "baskets" dataframe we now convert this into a numpy array. Since we only care about invoices where several items are purchased together, we only keep invoices where at least three different items were purchased. This leaves us with 17504 rows. The numpy array is now ready to be fitted. We will now use the [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans) Clustering Algorithm from the Scikit-learn module to ensure high efficieny. Take a look at my [Python-Clustering-Algorithm](https://github.com/gmoharram/Python-Clustering-Algorithm). For our purposes we will set k = 400. We shouldn't expect our data to consist of several (even hundreds) of perfect clusters. Instead we expect there to be a few well defined clusters with a meaningful amount of data points but otherwise unrelated purchases. To ensure that we find those few meaningful cluster centroids, the clustering algorithm will be run several times with several (highly likely) different randomly chosen initial centroids. The fit with the lowest clustering loss function value is automatically chosen. 


