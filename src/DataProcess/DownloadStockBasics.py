'''
Created on Jun 23, 2017

@author: charles
'''
# import sys
# sys.path.append('../')

from init import *



def download_stock_basics_info():
    downloadDir = DATA_DIR
    stockList = STOCK_List
    
    try:
        print("Starting to download stock basics information")
        df = ts.get_stock_basics()
        df=df[df['timeToMarket']>0]
        df['timeToMarket']=pd.to_datetime(pd.Series(df['timeToMarket']), format='%Y%m%d')
        df.to_csv(downloadDir+ stockList)
         
        print(df)
    
    except Exception as e:
        print str(e)
        
    print(DATA_DIR)

if __name__ == '__main__':
#     DATA_DIR = os.path.abspath(os.path.pardir+'/stockdata_new/')
    
    download_stock_basics_info()
    pass