# ecommerce-clustering-project
This is a python clustering project that uses the Online Retail Data Set available at [UCI ML Rep.](https://archive.ics.uci.edu/ml/datasets/online+retail#)
Source:  Dr Daqing Chen, Director: Public Analytics group. chend '@' lsbu.ac.uk, School of Engineering, London South Bank University, London SE1 0AA, UK.

We will be using the numpy, pandas, scikit-learn, matplotlib and pickle libraries. 

## Data Cleaning

The Data Set is an excel sheet where each row represents an item . The for this project relevant columns are the "Stock Code", "Quantity"and "InvoiceNo" columns. We aim to create a matrix, where each row represents an Invoice Number and all Stock Codes are assigned a column. The cell values will be the Quantity information. In the following we will refer to each row as a "basket". This is performed with the [dataPrep.py](https://github.com/gmoharram/ecommerce-clustering-project/blob/main/dataPrep.py) script. A screenshot of the obtained file is shown below. 


