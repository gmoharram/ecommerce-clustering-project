# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 13:34:51 2020

@author: gmoha
"""

import numpy as np
import pandas as pd

raw_data = pd.read_excel('OnlineRetail.xlsx')


invoices = raw_data['InvoiceNo'].unique()
stock_codes = raw_data['StockCode'].unique()
order_baskets = pd.DataFrame(index = invoices, columns = stock_codes, data = np.zeros((invoices.size, stock_codes.size)))

for inv in invoices:
    
    applicable = raw_data['InvoiceNo'] == inv
    invoice_data = raw_data[applicable]
    
    print(inv)
    for idx in invoice_data.index:
        order_baskets[invoice_data['StockCode'][idx]][invoice_data['InvoiceNo'][idx]] = invoice_data['Quantity'][idx]
        print("Item {0} done".format(idx))
    
    print("{0} done!".format(inv))
    

order_baskets.to_csv('order_baskets.csv', encoding = 'utf-8', columns = order_baskets.columns)