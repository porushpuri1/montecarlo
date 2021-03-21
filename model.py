#!/usr/bin/python

import yfinance as yf
import streamlit as st
import datetime 
import pandas as pd
import requests
import numpy as np
yf.pdr_override()


st.write("""
# Monte Carlo Simulation
""")


st.sidebar.header('User Input Parameters')

today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'AAPL')
    start_date = st.sidebar.text_input("Start Date", '2019-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
company_name = get_symbol(symbol.upper())

start = pd.to_datetime(start)
end = pd.to_datetime(end)


# Read data 
data = yf.download(symbol,start,end)


# Adjusted Close Price
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data['Adj Close'])

close_price = data['Adj Close']
returns = close_price.pct_change()

last_price = close_price[-1]


num_simulations = 1000
num_days = 252

simulation_df = pd.DataFrame()

for x in range(num_simulations):
    count = 0
    daily_vol = returns.std()
    
    price_series = []
    
    price = last_price * (1 + np.random.normal(0, daily_vol))
    price_series.append(price)
    
    for y in range(num_days):
        if count == 251:
            break
        price = price_series[count] * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)
        count += 1
    
    simulation_df[x] = price_series

summary = simulation_df.describe()

st.header(f"Monte Carlo Simulations....\n {company_name}")
st.line_chart(simulation_df)

#st.dataframe(simulation_df)
#st.write(simulation_df.describe())

mean_monte = summary.agg('mean')
st.header(f"Line of Means....\n {company_name}")
st.line_chart(mean_monte)

model_inter = mean_monte.describe()
st.header(f"Monte Carlo Interpretation..\n {company_name}")
st.dataframe(model_inter)





