'''
Created on Jun 23, 2017

@author: charles
'''

import platform, os
import pandas as pd
import tushare as ts
from Util import *

DATA_DIR = '/home/charles/stock/StockQuant/stockdata_new/'#os.path.abspath(os.path.curdir+'/stockdata_new/')
# print(DATA_DIR)
STOCK_List = '/stocklist.csv'
STOCK_CSV_DIR = '/stock_csv/'
FIN_DIR = '/basic_csv/'
