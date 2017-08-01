'''
Created on Jun 24, 2017

@author: charles
'''
from Util import *
import DataProcess as dp
import numpy as np

if __name__ == '__main__':
#     dp.download_stock_basics_info()
    codes = ['600009', '600177', '600271', '600309', '600340','600585', '600827', '600900',
            '601699','000333', '000423','000625','000776','000876','000898','002202','002304','002466']
    volumn = [300,1000, 500,400,300,500,700,700,1500,300,200,700,600,1300,2000,700,100,200]
    
    print volumn
    print np.array(volumn)[:,None]
    SZ300= dp.Stock(code='000300',start_date='2017-01-01', index=True)
#     S.print_code()
    SZ300.download()
 
    daily_data = pd.DataFrame() 
     
    print daily_data

# 
#     
    for stockcode in codes:
        S= dp.Stock(code=stockcode,start_date='2017-01-01')
        
        print S.get_close()
        #     S.print_code()
#         S.download() 
#         sID = code
#         S1=S.get_delta()
#         S1.columns=[stockcode]
          
        if daily_data.empty:
            daily_data = S.get_close()
        else:
#             daily_data=daily_data.join(S.get_close().set_index(['date']),how='outer',on = ['date'] )
            daily_data=daily_data.merge(S.get_close(),how='outer',left_index=True, right_index=True)#,on = ['date'] )
             
#         print daily_data
        print stockcode
        #     caculate_Beta(S.get_delta(), SZ300.get_delta())
#         single_Beta(S.get_delta(), SZ300.get_delta(),12)
    print daily_data 
    daily_data.to_csv('test3.csv')
    daily_data=daily_data.fillna(method='pad')
    daily_data.to_csv('test4.csv')


    daily_data['portfolio']=daily_data.dot(volumn)
#     print daily_data
    
    daily_data['delta']= daily_data['portfolio'].diff(1)/daily_data['portfolio'].shift(1)
    daily_data.sort_index()
    print daily_data
#     print(portfolio)
    
    single_Beta(daily_data[['delta']], SZ300.get_delta(),20)
      
    pass