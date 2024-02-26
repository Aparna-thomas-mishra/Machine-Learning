import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date
from datapackage import Package

st.set_page_config(
    page_title="Stock Price Analysis",
    page_icon="📈",  
    layout="wide",  
    initial_sidebar_state="expanded"
)

package = Package('datapackage.json')

# Extract the relevant CSV resource
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        sp500_df = pd.DataFrame(resource.read(), columns=['Stock Ticker', 'Company Name', 'Sector'])

def find_ticker_symbol(company_name):
    # Convert user input to lowercase for case-insensitivity
    user_input_lower = company_name.lower()

    # Check if the lowercase 'Company Name' contains the lowercase user input
    ticker = sp500_df[sp500_df['Company Name'].str.lower().str.contains(user_input_lower)]['Stock Ticker'].values

    return ticker[0] if len(ticker) > 0 else None

# Custom CSS to create a gradient background
custom_css = """
    body {
        background: linear-gradient(to right, #00c6fb, #005bea);
    }
"""

# Apply the custom CSS
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
    
st.write("""
         Stock Price App
         
         Shown are the stock **closing price** and **volume** 
         
         """)

#Define ticker symbol

company_name = st.text_input("Enter Company Name: ")

if company_name:     
    tickerSymbol = find_ticker_symbol(company_name)

    if tickerSymbol:
        st.write(f"Selected Ticker Symbol : {tickerSymbol}")
        #Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        #Get historical prices of this ticker
        tickerDF = tickerData.history(period = '1mo', start = '2005-5-31', end = date.today())

        # Create two columns for side-by-side display
        col1, col2 = st.columns(2)

        # Display closing price chart in the first column
        with col1:
            st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
            st.write("""
                     **Closing Price**
                     """)
            st.line_chart(tickerDF.Close)
            st.markdown("</div>", unsafe_allow_html=True)

        # Display volume chart in the second column
        with col2:
            st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
            st.write("""
                     **Volume**
                     """)
            st.line_chart(tickerDF.Volume)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.write(f"Stock ticker {company_name} not found. PLease enter a valid stock ticker")
