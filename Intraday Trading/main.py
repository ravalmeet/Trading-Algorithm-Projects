import streamlit as st
from intraday import main
import datetime
import pandas as pd
from time import sleep



st.write("Intraday Stocks List : ")

start_time = datetime.time(9, 15)   # Starting time
end_time = datetime.time(15, 30)   # Ending time
current_time = datetime.datetime.now().strftime('%H:%M:%S')
  
time_list = []

t = datetime.datetime.combine(datetime.date.today(), start_time)
while t.time() <= end_time:
    time_list.append(t.time().strftime('%H:%M:%S'))
    t += datetime.timedelta(minutes=5)




data = main()

def update_data():
    while True:
        # if current_time in time_list:
        data = main()
        if(len(data) > 0):
            st.table(data)
  

import threading
thread = threading.Thread(target=update_data)
thread.start()
print(len(data))
st.table(data)
