'''
Created on Jun 24, 2017

@author: charles
'''

from init import *
import datetime
import tushare as ts
import os.path as pt
# from tushare.util.dateu import today

class Stock(object):
    '''
    classdocs
    '''


    def __init__(self, code, start_date, end_date=datetime.date.today(), index=False):
        '''
        Constructor
        '''
        self.code = code
        self.start_date=start_date
        self.end_date = end_date
        self.index=index
        self.raw = ''
        self.fname = DATA_DIR+STOCK_CSV_DIR+self.code+'.CSV'
        
        if pt.isfile(self.fname):
            self.raw= pd.read_csv(self.fname)
            self.raw=self.raw.set_index(['date'])
#             print self.raw
        else:
            df_qfq = ts.get_h_data(str(self.code), start=str(self.start_date), end=str(self.end_date),index=self.index)
            df_qfq['code'] = self.code
            df_qfq['delta']= df_qfq['close'].diff(-1)/df_qfq['close'].shift(-1)
    #         df_qfq['delta2']= df_qfq['close'].shift(-1)
            self.raw = df_qfq.sort_index()
#             print self.raw
            df_qfq.to_csv(self.fname)
#         print(self.code)
        
        print self.raw
        
        
    def print_code(self): 
        print self.code
        
    def download(self):
        
        
        df_qfq = ts.get_h_data(str(self.code), start=str(self.start_date), end=str(self.end_date),index=self.index)
        df_qfq['code'] = self.code
        df_qfq['delta']= df_qfq['close'].diff(-1)/df_qfq['close'].shift(-1)
    #         df_qfq['delta2']= df_qfq['close'].shift(-1)
        self.raw = df_qfq.sort_index()
        df_qfq.to_csv(self.fname)
#         print df_qfq
        
    def stock_finance(self):
        print 'NA'
        
    def get_delta(self):
        
        return self.raw[['delta']]#.set_index(['Date'])
    
    
    def get_close(self):
#         print self.raw#[['date','close']]
        
        return self.raw[['close']]
        
        