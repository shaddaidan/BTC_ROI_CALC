# app.py

import streamlit as st
from btc_investment_calculator import calculate_investment_value, plot_historical_prices, df

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
    st.markdown("<h4>Made by ShaddaiConcepts 😊</h4>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
