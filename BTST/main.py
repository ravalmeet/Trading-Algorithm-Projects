import numpy as np
import pandas as pd
from nsepy import get_history
import ydata_profiling
from datetime import date, timedelta
from colorama import Back, Fore, Style
import warnings
import webbrowser

warnings.filterwarnings("ignore")

# file_path = "Backtest6.csv"

file_path = input("Enter the path of the file: ") + '.csv'

try:
    df = pd.read_csv(file_path)
    print(Back.GREEN + Fore.WHITE + "File Read Successfully !!" + Style.RESET_ALL)
except:
    print(Back.RED + Fore.WHITE + "Please Check file path Again !!" + Style.RESET_ALL)



num = int(input("How many rows you want to scan outoff " + str(len(df)) + " : "))    
print(Back.GREEN + Fore.WHITE + "Processing Start ... " + Style.RESET_ALL)    
if(num < len(df)):
    new_df = df[:num:]
else:
    new_df = df[::]




new_df['date'] = pd.to_datetime(new_df['date'], format="%d-%m-%Y")
new_df['next_date'] = new_df['date'] + timedelta(days=1)



def bearish_BTST(new_df):
    
    count = 0
    
    for i, row in new_df.iterrows():
    
        symbol = row['symbol']
    
        end_date = row['date'] + timedelta(days=1)
    
        start_date = row['date']
    
        count = count + 1

        stock_data = get_history(symbol=symbol, start=start_date, end=end_date)
    

        if(len(stock_data) > 1):

            if(stock_data.iloc[0]['Close'] > stock_data.iloc[1]['Low']):
                new_df.loc[i,'status_low'] = 'Success'
            else:
                new_df.loc[i,'status_low'] = 'Fail'
            

            if(stock_data.iloc[0]['Close'] > stock_data.iloc[1]['Open']):
                new_df.loc[i,'status_open'] = 'Success'
            else:
                new_df.loc[i,'status_open'] = 'Fail'
                

            if(stock_data.iloc[0]['Close'] > stock_data.iloc[1]['Close']):
                new_df.loc[i,'status_close'] = 'Success'
            else:
                new_df.loc[i,'status_close'] = 'Fail'
            
            if(stock_data.iloc[0]['Close'] > stock_data.iloc[1]['High']):
                new_df.loc[i,'status_high'] = 'Success'
            else:
                new_df.loc[i,'status_high'] = 'Fail'
       
            print(str(count) + "-" + str(len(new_df)) , end = " ")
        
    new_df.dropna(subset=['status_high'], inplace=True)
    
    report = ydata_profiling.ProfileReport(new_df)

             # save the report to an HTML file
    report.to_file('new_df_report.html')

    filename = "new_df_report.html"

    webbrowser.open_new_tab(filename)
            

def bullish_BTST(new_df):
    
    count = 0
    
    for i, row in new_df.iterrows():
    
        symbol = row['symbol']
    
        end_date = row['date'] + timedelta(days=1)
    
        start_date = row['date']
    
        count = count + 1

        stock_data = get_history(symbol=symbol, start=start_date, end=end_date)
    

        if(len(stock_data) > 1):

            if(stock_data.iloc[0]['Close'] < stock_data.iloc[1]['Low']):
                new_df.loc[i,'status_low'] = 'Success'
            else:
                new_df.loc[i,'status_low'] = 'Fail'
            

            if(stock_data.iloc[0]['Close'] < stock_data.iloc[1]['Open']):
                new_df.loc[i,'status_open'] = 'Success'
            else:
                new_df.loc[i,'status_open'] = 'Fail'
                

            if(stock_data.iloc[0]['Close'] < stock_data.iloc[1]['Close']):
                new_df.loc[i,'status_close'] = 'Success'
            else:
                new_df.loc[i,'status_close'] = 'Fail'
                
            if(stock_data.iloc[0]['Close'] < stock_data.iloc[1]['High']):
                new_df.loc[i,'status_high'] = 'Success'
            else:
                new_df.loc[i,'status_high'] = 'Fail'
       
            print(str(count) + "-" + str(len(new_df)) , end = " ")
        
    new_df.dropna(subset=['status_high'], inplace=True)
    
    report = ydata_profiling.ProfileReport(new_df)

             # save the report to an HTML file
    report.to_file('new_df_report.html')

    filename = "new_df_report.html"

    webbrowser.open_new_tab(filename)
            
            
            
        

def Bullish_swing(new_df):
    
    count = 0
    
    stoploss = int(input("Enter the Maximum stoploss : "))
    
    max_days = int(input("Enter the Maximum days : "))
    
#     stoploss = 10
#     max_days = 27
    
    
    new_df['date'] = pd.to_datetime(new_df['date'])
        
    return_loss = stoploss / 100
    
    return_losshold = return_loss

    for i, row in new_df.iterrows():
    
        symbol = row['symbol']
    
        end_date = row['date'] + timedelta(days=max_days)
    
        start_date = row['date']
    
        count = count + 1

        stock_data = get_history(symbol=symbol, start=start_date, end=end_date)
    
#         print(stock_data)

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
    
    report = ydata_profiling.ProfileReport(new_df)

    # save the report to an HTML file
    report.to_file('new_df_report.html')

    filename = "new_df_report.html"

    webbrowser.open_new_tab(filename)
            
            
            

             
        

def Bearish_swing(new_df):
    
    print("This Model is Working Under Process...")
    
#     count = 0
    
#     stoploss = int(input("Enter the Maximum stoploss : "))
    
#     max_days = int(input("Enter the Maximum days : "))
    
# #     stoploss = 10
# #     max_days = 27
    
    
#     new_df['date'] = pd.to_datetime(new_df['date'])
        
#     return_loss = stoploss / 100
    
#     return_losshold = return_loss

#     for i, row in new_df.iterrows():
    
#         symbol = row['symbol']
    
#         end_date = row['date'] + timedelta(days=max_days)
    
#         start_date = row['date']
    
#         count = count + 1

#         stock_data = get_history(symbol=symbol, start=start_date, end=end_date)
    
# #         print(stock_data)

#         if(len(stock_data) > 0):
            
         
    
#             new_df.loc[i,'close_price'] = stock_data['Close'][0]
        
            
        
#             max_loss = stock_data['Close'].max() - stock_data['Close'][0]
        
#             max_profit = stock_data['Close'][0] - stock_data['Close'].min()

        
#             max_close = stock_data['Close'].min()
        
#             min_close = stock_data['Close'].max()
        
#             min_close_value =  stock_data['Close'][0] +  (stock_data['Close'][0] * return_losshold)
        
#             profit_date = [stock_data.loc[stock_data['Close'] == max_close].index[0]]
        
#             new_df.loc[i,'max_profit_pre'] =  ( max_profit * 100 / stock_data['Close'][0] )
        
#             new_df.loc[i,'Max_Loss_Pre'] =  ( max_loss * 100 / stock_data['Close'][0] )  
        
#             new_df.loc[i,'Profit_Date'] =  pd.to_datetime(profit_date[0])
        
#             new_df.loc[i,'Holding_Period'] = new_df.loc[i,'Profit_Date'] - row['date']

#             new_df.loc[i,'Loss_Date'] = 0      
        
        
#             new_df.loc[i,'Status'] = 'Success'
        
    
#             if(min_close > min_close_value):
            
#                 loss_date = [stock_data.loc[stock_data['Close'] == min_close].index[0]]
            
#                 new_df.loc[i,'Loss_Date'] = pd.to_datetime(loss_date[0])
            
#                 new_df.loc[i,'Status'] = 'Fail'
        
#                 new_df.loc[i,'Holding_Period'] = new_df.loc[i,'Loss_Date'] - row['date']
            
#             print(count , end = " ")
            
    
#     new_df.dropna(subset=['close_price'], inplace=True)
    
#     report = ydata_profiling.ProfileReport(new_df)

#     # save the report to an HTML file
#     report.to_file('new_df_report.html')

#     filename = "new_df_report.html"

#     webbrowser.open_new_tab(filename)
            
            
            

              
                         
            
        
        
        
        
        
        
        
        
        
        
        
        
      
        
        
while True:
    
    input_data = int(input("1. Bullish_BTST , 2. Bearish_BTST , 3. Bullish_Swing , 4. Bearish_Swing  :  "))

# input_data = 3

    if(input_data == 1):
        print(Back.GREEN + Fore.WHITE + "Bullish BTST Backtest Started !!" + Style.RESET_ALL)
        bullish_BTST(new_df)
        new_df.dropna(subset=['status_low'], inplace=True) 
    elif(input_data == 2):
        print(Back.GREEN + Fore.WHITE + "Bearish BTST Backtest Started !!" + Style.RESET_ALL)
        bearish_BTST(new_df)
        new_df.dropna(subset=['status_low'], inplace=True) 
    elif(input_data == 3):
        print(Back.GREEN + Fore.WHITE + "Bullish Swing Backtest Started !!" + Style.RESET_ALL)
        Bullish_swing(new_df)
    elif(input_data == 4):
        print(Back.GREEN + Fore.WHITE + "Bearish Swing Backtest Started !!" + Style.RESET_ALL)
        Bearish_swing(new_df) 
    else:
        print(Back.RED + Fore.WHITE + "Please Enter 1 or 2 !!" + Style.RESET_ALL)


            
            




