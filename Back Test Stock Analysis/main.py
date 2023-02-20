import numpy as np
import pandas as pd
import matplotlib as plt
from datetime import datetime, timedelta
import datetime
import pandas_profiling
from datetime import date
from nsepy import get_history

import warnings

warnings.filterwarnings('ignore')

df = pd.read_csv('BackTest.csv')

# max_profit = int(input("enter the maximum profit : "))
stoploss = int(input("enter the maximum stoploss : "))
max_days = int(input("enter the maximum days : "))

# profit = 10
# stoploss = 10
# max_days = 22

df['date'] = pd.to_datetime(df['date'])

# df['end_date'] = df['date'] + timedelta(days=max_days)

# return_per = profit / 100

return_loss = stoploss / 100

new_df = df[::]


# return_threshold = return_per

return_losshold = return_loss

count = 0

for i, row in new_df.iterrows():
    
    symbol = row['symbol']
    
    end_date = row['date'] + timedelta(days=max_days)
    
    start_date = row['date']
    
    count = count + 1

    stock_data = get_history(symbol=symbol, start=start_date, end=end_date)
    
    
    if(len(stock_data) > 0):
    
        new_df.loc[i,'close_price'] = stock_data['Close'][0]
        
        max_profit = stock_data['Close'].max() - stock_data['Close'][0]
        
        max_loss = stock_data['Close'].min() - stock_data['Close'][0]

        
        max_close = stock_data['Close'].max()
        
        min_close = stock_data['Close'].min()
        
        min_close_value =  stock_data['Close'][0] -  (stock_data['Close'][0] * return_losshold)
        
        profit_date = [stock_data.loc[stock_data['Close'] == max_close].index[0]]
        
        new_df.loc[i,'max_profit_pre'] =  ( max_profit * 100 / stock_data['Close'][0] )
        
        new_df.loc[i,'Max_Loss_Pre'] =  ( max_loss * 100 / stock_data['Close'][0] )  
        
        new_df.loc[i,'Profit_Date'] =  pd.to_datetime(profit_date[0])
        
        new_df.loc[i,'Holding_Period'] = new_df.loc[i,'Profit_Date'] - row['date']

        new_df.loc[i,'Loss_Date'] = 0      
        
        
        new_df.loc[i,'Status'] = 'Success'
        
    
        if(min_close < min_close_value):
            
            loss_date = [stock_data.loc[stock_data['Close'] == min_close].index[0]]
            
            new_df.loc[i,'Loss_Date'] = pd.to_datetime(loss_date[0])
            
            new_df.loc[i,'Status'] = 'Fail'
        
            new_df.loc[i,'Holding_Period'] = new_df.loc[i,'Loss_Date'] - row['date']
            
        print(count , end = " ")
            
            
            
new_df.dropna(subset=['close_price'], inplace=True)                      
                     

report = pandas_profiling.ProfileReport(new_df)

# save the report to an HTML file
report.to_file('report.html')

new_df.to_csv('data.csv')

print("Processing Successfully Done , You Can Get data.csv and report.html file in the source folder")