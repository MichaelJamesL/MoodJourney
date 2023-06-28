import pandas as pd
from datetime import datetime
import streamlit as st

def writeUser(name, emotion):
    try :
        data = pd.read_csv('user.csv')
    except :
        print("No historical data recorded, will create fresh new data")
        data = pd.DataFrame(columns=['Name', 'Emotions', 'Date'])
        data.to_csv('user.csv') # Create data if not exist yet. We use csv file for simplicity, but in real application we need to use a database

    date = datetime.now()

    #date = pd.to_datetime(date).dt.normalize() # dt.normalize to remove time component since we only need the date 

    df_user = pd.DataFrame({'Name':[name], 'Emotions':[emotion], "Date":[date]})

    df_user.to_csv('user.csv', mode='a', index=True, header=False)


def readUser(name):
    df = pd.read_csv('user.csv')
    return df.loc[df['Name'] == name]

def countUser(name):
    df = readUser(name)
    return df.shape[0]

"""    
name = st.text_input("What is your name?")
st.line_chart(readUser(name), x="Date", y="Emotions")
writeUser(name, "sad")
"""

