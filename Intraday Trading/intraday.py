from time import sleep
import os
import warnings
import sys
import datetime
import time
warnings.filterwarnings("ignore")

try:
    import xlwings as xw
except (ModuleNotFoundError, ImportError):
    print("xlwings module not found")
    os.system(f"{sys.executable} -m pip install -U xlwings")
finally:
    import xlwings as xw
    
try:
    import requests
except (ModuleNotFoundError, ImportError):
    print("requests module not found")
    os.system(f"{sys.executable} -m pip install -U requests")
finally:
    import requests

try:
    import pandas as pd
except (ModuleNotFoundError, ImportError):
    print("pandas module not found")
    os.system(f"{sys.executable} -m pip install -U pandas")
finally:
    import pandas as pd
    
try:
    from bs4 import BeautifulSoup
except (ModuleNotFoundError, ImportError):
    print("BeautifulSoup module not found")
    os.system(f"{sys.executable} -m pip install -U beautifulsoup4")
finally:
    from bs4 import BeautifulSoup
    
    
Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'



# Condition = "( {cash} ( ( {33489} ( [0] 5 minute volume > [0] 5 minute sma( volume,20 ) and latest rsi( 14 ) >= 60 and weekly rsi( 14 ) >= 60 and monthly rsi( 14 ) >= 55 and [0] 5 minute rsi( 14 ) >= 60 and [0] 30 minute rsi( 14 ) >= 55 and [0] 5 minute close > [-1] 30 minute high and [0] 5 minute close > [0] 5 minute upper bollinger band( 20 , 1.7 ) and [ -1 ] 5 minute close <= [ -1 ] 5 minute upper bollinger band( 20 , 1.7 ) and latest close < 5000 and [0] 5 minute close > [-1] 5 minute close ) ) or( {33489} ( [0] 5 minute volume > [0] 5 minute sma( volume,20 ) and latest rsi( 14 ) <= 40 and weekly rsi( 14 ) <= 40 and monthly rsi( 14 ) <= 45 and [0] 5 minute rsi( 14 ) <= 40 and [0] 30 minute rsi( 14 ) <= 45 and [0] 5 minute close < [-1] 30 minute low and [0] 5 minute close < [0] 5 minute lower bollinger band( 20 , 1.7 ) and latest close < 5000 and [0] 5 minute close < [-1] 5 minute close ) ) ) )  " 

Condition = " ( {cash} ( ( {57960} ( ( {57960} ( latest rsi( 14 ) >= 60 and weekly rsi( 14 ) >= 60 and monthly rsi( 14 ) >= 60 and latest close >= latest ema( latest close , 40 ) and latest close > latest upper bollinger band( 20 , 1 ) and 1 day ago  close <= 1 day ago  upper bollinger band( 20 , 1 ) and weekly close > latest upper bollinger band( 20 , 1 ) and 1 week ago  close <= 1 day ago  upper bollinger band( 20 , 1 ) and monthly close > latest upper bollinger band( 20 , 1 ) and 1 month ago  close <= 1 day ago  upper bollinger band( 20 , 1 ) ) ) ) ) ) ) "

def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    
    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)

        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
    return df

    



def main():
    new_df = pd.read_csv('new_df.csv')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    print("Process Started")
    data = GetDataFromChartink(Condition)
    data['time'] = current_time
    for i in range(len(data)):
        symbol = data.at[i, 'nsecode']

        per_chg = data.at[i,'per_chg']
        close = data.at[i,'close']
        volume = data.at[i,'volume']
        if symbol in new_df['nsecode'].tolist():
            index = new_df.index[new_df['nsecode'] == symbol].tolist()[0]
            new_df.at[index, 'occurance_time'] += 1
            new_df.at[index,'per_chg'] = per_chg
            new_df.at[index,'close'] = close
            new_df.at[index,'volume'] = volume
            new_df.at[index,'now'] = current_time
        else:
            new_row = {'nsecode': symbol, 'occurance_time': 1, 'per_chg': per_chg , 'close':close,'volume':volume ,'first_time':current_time, 'now': current_time}
            new_df = new_df.append(new_row, ignore_index=True)
    new_df.to_csv('new_df.csv', index=False)
    
    return new_df
    
    
     

# print("DONE")


start_time = datetime.time(9, 15)   # Starting time
end_time = datetime.time(15, 30)   # Ending time

# Create a list of times every 5 minutes
time_list = []
t = datetime.datetime.combine(datetime.date.today(), start_time)
while t.time() <= end_time:
    time_list.append(t.time().strftime('%H:%M:%S'))
    t += datetime.timedelta(minutes=5)



    