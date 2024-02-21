pip install yfinance pandas streamlit

import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date

def find_ticker_symbol(company_name):
    try:
        ticker = yf.Ticker(company_name)

        company_info = ticker.info

        tickerSymbol = company_info['symbol']

        return tickerSymbol
    
    except ValueError as e:
        
        print(f"Error: {e}")
        return None
    
st.write("""
         Stock Price App
         
         Shown are the stock **closing price** and **volume** 
         
         """)

#Define ticker symbol

company_name = st.text_input("Enter the stock ticker: ")

if company_name:     
    tickerSymbol = find_ticker_symbol(company_name)

    if tickerSymbol:
        st.write(f"Selected Ticker Symbol : {tickerSymbol}")
        #Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        today = date.today()
        #print("Today's date:", today)

        #Get historical prices of this ticker
        tickerDF = tickerData.history(period = '1mo', start = '2005-5-31', end = today)

        #Open High Low Close Volume Dividends Stock Splits
        st.write("""
                 **Closing Price**
                 """)
        st.line_chart(tickerDF.Close)

        st.write("""
                 **Volume**
                 """)
        st.line_chart(tickerDF.Volume)

    else:
        st.write(f"Stock ticker {company_name} not found. PLease enter a valid stock ticker")
