import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# load the historical price data
df = pd.read_csv('crypto_data/btc-usd-max.csv')

# convert the snapped_at to datetime
df['snapped_at'] = pd.to_datetime(df['snapped_at'])


# set the snapped_at as the index
df.set_index('snapped_at', inplace=True)

# Function to calculate investment value
def calculate_investment_value(start_date, end_date, initial_investment):
    try:
        # Retrieve the start and end prices as scalar values
        start_price = df.loc[start_date, 'price']
        end_price = df.loc[end_date, 'price']

        # Ensure these are scalar values
        if isinstance(start_price, pd.Series):
            start_price = start_price.iloc[0]
        if isinstance(end_price, pd.Series):
            end_price = end_price.iloc[0]

        investment_value = (end_price / start_price) * initial_investment
        return investment_value
    except KeyError:
        return None  # Return None if dates are not found in DataFrame


# function to plot historical prices
def plot_historical_prices():
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['price'], label = 'Bitcoin Price')
    plt.title('Historical Bitcoin Prices')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Streamlit app
def main():
    st.title('Historical Bitcoin Investment Calculator')
    
    st.sidebar.header('Investment Details')
    initial_investment = st.sidebar.number_input('Initial Investment ($)', min_value=1.0, value=50.0, step=1.0)
    start_date = st.sidebar.date_input('Start Date', min_value=df.index.min().date(), max_value=df.index.max().date())
    end_date = st.sidebar.date_input('End Date', min_value=df.index.min().date(), max_value=df.index.max().date())
    
    if start_date >= end_date:
        st.error('End date must be after start date.')
    else:
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        investment_value = calculate_investment_value(start_date_str, end_date_str, initial_investment)
        
        if investment_value is not None:
            st.write(f'The value of the investment on {end_date_str} would be ${investment_value:.2f}')
            plot_historical_prices()
        else:
            st.error('Error calculating investment value. Please check your input dates.')
        

if __name__ == '__main__':
    main()