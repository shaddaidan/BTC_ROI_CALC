import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load the historical price data
df = pd.read_csv('crypto_data/btc-usd-max.csv')

# Convert the snapped_at to datetime
df['snapped_at'] = pd.to_datetime(df['snapped_at'])

# Set the snapped_at as the index
df.set_index('snapped_at', inplace=True)

# Function to calculate investment value and ROI
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
        roi_percent = ((investment_value - initial_investment) / initial_investment) * 100
        return investment_value, roi_percent
    except KeyError:
        return None, None  # Return None if dates are not found in DataFrame

# Function to plot historical prices
def plot_historical_prices():
    plt.figure(figsize=(12, 6))
    
    # Customize the plot
    plt.plot(df.index, df['price'], label='Bitcoin Price', color='blue', linewidth=2)
    
    # Add title and labels with improved styling
    plt.title('Historical Bitcoin Prices', fontsize=18, fontweight='bold')
    plt.xlabel('Date', fontsize=14, fontweight='bold')
    plt.ylabel('Price (USD)', fontsize=14, fontweight='bold')
    
    # Customize the ticks on the axes
    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    
    # Add a legend with improved styling
    plt.legend(fontsize=12, loc='upper left')
    
    # Add grid with customized style
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Optionally, add some markers to highlight specific points
    plt.scatter(df.index[-10:], df['price'][-10:], color='red', zorder=5)  # Highlight the last 10 points

    # Optionally, add annotations
    max_price = df['price'].max()
    max_price_date = df['price'].idxmax()
    plt.annotate(f'Highest Price: ${max_price:.2f}', xy=(max_price_date, max_price),
                 xytext=(max_price_date, max_price + 1000),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=12, fontweight='bold', color='darkred')

    st.pyplot(plt)



# Streamlit app
def main():
    st.title('📈 Historical Bitcoin Investment Calculator')
    
    st.sidebar.header('Investment Details 💼')
    initial_investment = st.sidebar.number_input('Initial Investment ($)', min_value=1.0, value=50.0, step=1.0)
    start_date = st.sidebar.date_input('Start Date 📅', min_value=df.index.min().date(), max_value=df.index.max().date())
    end_date = st.sidebar.date_input('End Date 📅', min_value=df.index.min().date(), max_value=df.index.max().date())
    
    if start_date >= end_date:
        st.error('❌ End date must be after start date.')
    else:
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        investment_value, roi_percent = calculate_investment_value(start_date_str, end_date_str, initial_investment)
        
        if investment_value is not None:
            st.markdown(f"<h2>The value of the investment on {end_date_str} would be <span style='color:green;'>${investment_value:.2f}</span> 💵</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3>The ROI is <span style='color:blue;'>{roi_percent:.2f}%</span> 📈</h3>", unsafe_allow_html=True)
            plot_historical_prices()
        else:
            st.error('❌ Error calculating investment value. Please check your input dates.')
    
    # Adding a footer with the author's name
    st.markdown("---")
    st.markdown("<h4>Made by Shaddai 😊</h4>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
