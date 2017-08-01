'''
Created on Jun 24, 2017

@author: charles
'''
import pandas as pd
import numpy as np
import tushare as ts
import urllib2
import os
from init import *
# from pandas.compat.numpy import np_array_datetime64_compat
# from numpy import empty
import time
# from lib2to3.pgen2.token import STAR

def roll(df, w):
    # stack df.values w-times shifted once at each stack
    roll_array = np.dstack([df.values[i:i+w, :] for i in range(len(df.index) - w + 1)]).T
    # roll_array is now a 3-D array and can be read into
    # a pandas panel object
    panel = pd.Panel(roll_array, 
                     items=df.index[w-1:],
                     major_axis=df.columns,
                     minor_axis=pd.Index(range(w), name='roll'))
    # convert to dataframe and pivot + groupby
    # is now ready for any action normally performed
    # on a groupby object
    return panel.to_frame().unstack().T.groupby(level=0)

def beta(df):
    # first column is the market
    X = df.values[:, [0]]
    # prepend a column of ones for the intercept
    X = np.concatenate([np.ones_like(X), X], axis=1)
    # matrix algebra
    b = np.linalg.pinv(X.T.dot(X)).dot(X.T).dot(df.values[:, 1:])
    return pd.Series(b[1], df.columns[1:], name='Beta')

def single_Beta(stock, index, n):
#     print stock
#     print index
#     stock=stock.insert(0,'mkt',index['delta'])
    stock=stock.merge(index,how='outer',left_index=True, right_index=True)#
    
    print stock
    np_array = stock.values
    
    stock.to_csv('test.csv')
    print(np_array[-n:, :])
    
    np_array=np_array[-n:, :]
    
    s = np_array[:, 0]
    m = np_array[:,1]
    
    covariance = np.cov(s, m)
    beta = covariance[0,1]/covariance[1,1]
    
    print beta
    
    return beta

def caculate_Beta(stock, index):
#     X = pd.concat([index,stock])
#     stock['mkt']=index['close']
    stock.insert(0,'mkt',index['delta'])
    
    stock.to_csv('test.csv')
#     stock.sort_index(ascending=True)
#     print('caculate Beta')
#     print(stock)
    
    rdf = roll(stock.pct_change().dropna(), 12)
    betas = rdf.apply(beta)
    

#     print(stock)

#     df = pd.concat(inex)
    
def get_fin_data(start, end, fin_type='report'):
    years = range(start, end)
    print years
    quarters = range(1,5)
    
    if fin_type == 'report':
        for year in years:
            fin_rpt =''
            for quarter in quarters:
                print(year,quarter)
    #             try:
                fin_rpt=ts.get_report_data(year, quarter)
    #             print len(fin_rpt)
    #             except TypeError:
    #                 fin_rpt=ts.get_report_data(year, quarter)
    #             else:
    #                 break
                while fin_rpt is None:
                    print "empty"
                    time.sleep(10)
                    fin_rpt=ts.get_report_data(year, quarter)
    #                 print len(fin_rpt)
                print fin_rpt
                fin_rpt['quarter'] = str(year)+str(quarter)
                fin_rpt.to_csv(DATA_DIR+FIN_DIR+str(year)+'_'+str(quarter)+'_report.CSV', encoding="utf-8")
                
                print fin_rpt
    elif fin_type == 'growth':
        for year in years:
            fin_rpt =''
            for quarter in quarters:
                print(year,quarter)
    #             try:
                fin_rpt=ts.get_growth_data(year, quarter)
    #             print len(fin_rpt)
    #             except TypeError:
    #                 fin_rpt=ts.get_report_data(year, quarter)
    #             else:
    #                 break
                while fin_rpt is None:
                    print "empty"
                    time.sleep(10)
                    fin_rpt=ts.get_growth_data(year, quarter)
    #                 print len(fin_rpt)
                print fin_rpt
                fin_rpt['quarter'] = str(year)+str(quarter)
                fin_rpt.to_csv(DATA_DIR+FIN_DIR+str(year)+'_'+str(quarter)+'_growth.CSV', encoding="utf-8")
                
                print fin_rpt
        
    elif fin_type == 'profit':
        for year in years:
            fin_rpt =''
            for quarter in quarters:
                print(year,quarter)

                fin_rpt=ts.get_profit_data(year, quarter)

                while fin_rpt is None:
                    print "empty"
                    time.sleep(10)
                    fin_rpt=ts.get_profit_data(year, quarter)

                print fin_rpt
                fin_rpt['quarter'] = str(year)+str(quarter)
                fin_rpt.to_csv(DATA_DIR+FIN_DIR+str(year)+'_'+str(quarter)+'_profit.CSV', encoding="utf-8")
                
                print fin_rpt
    elif fin_type == 'eastmoney':
        q_lastdays = ['03-31','06-30','09-30','12-31']
        for year in years:
            fin_rpt =''
            for quarter in q_lastdays:
                print(str(year)+'-'+quarter)
                get_eastmoney_fin(str(year)+'-'+quarter)

                
                
    
def combine_fin_data(start, end):
    years = range(start, end)
    print years
    quarters = range(1,5)
    
    list_=[]
    for year in years:
        for quarter in quarters:
            print(year, quarter)
            rpt_data = pd.read_csv(DATA_DIR + FIN_DIR + str(year) + '_' + str(quarter) + '_report.CSV', encoding="utf-8",index_col=0).set_index('code')
            profit_data = pd.read_csv(DATA_DIR + FIN_DIR + str(year) + '_' + str(quarter) + '.CSV', encoding="utf-8",index_col=0).set_index('code')
            growth_data = pd.read_csv(DATA_DIR + FIN_DIR + str(year) + '_' + str(quarter) + '_growth.CSV', encoding="utf-8",index_col=0).set_index('code')
#             fin_data = pd.concat([rpt_data,profit_data,growth_data],ignore_index= True)
# fin_data = pd.merge(rpt_data, profit_data, on=['code', 'quarter'],left_index=False, right_index=False)
#             fin_data = pd.merge(fin_data, growth_data, on = ['code', 'quarter'],left_index=False, right_index=False)
            fin_data = pd.merge(rpt_data, profit_data, on=[ 'quarter'],left_index=True, right_index=True)
            fin_data = pd.merge(fin_data, growth_data, on = ['quarter'],left_index=True, right_index=True).drop_duplicates(keep='first')
            print fin_data
            list_.append(fin_data)
#             fin_data.to_csv(DATA_DIR+FIN_DIR+str(year)+'_'+str(quarter)+'_all.CSV', encoding="utf-8")
            
    all_data = pd.concat(list_)
    all_data.to_csv(DATA_DIR+FIN_DIR+'_all_combine.CSV', encoding="utf-8")
    


def get_eastmoney_fin(quarter='2017-03-31', pagesize=10000):
    
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YJBB&fd="+quarter+"&p=1&ps=10000"
    data = ''
    
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req)
    
    fin_list = resp.read()
    fin_list = fin_list.replace('(["', '')
    fin_list = fin_list.replace('"])', '')
    
    fin_list = fin_list.strip().split('","')
    
#     print fin_list
    

    headerlist = ['code', 'name', 'eps', 'eps2','revenue', 'roe_yoy','roe_mom','net_profit','profit_yoy','profit_mom', 'bvps','roe', 'cfps','gross_profit_rate', 'tmp', 'tmp2', 'report_date','quarter','tmp3']
    for i in range(0,len(fin_list)):
        fin_attr = fin_list[i].strip().split(',')
        print i

        if i == 0:
            listFin = [fin_attr]
            
        else:
            listFin.append(fin_attr)
#         print fin_attr
    
    df = pd.DataFrame(listFin, columns=headerlist)
    print df
    
    df.to_csv(DATA_DIR+FIN_DIR+quarter+'_eastmoney.CSV', encoding="utf-8")
 
            
if __name__ == '__main__':
    pass
