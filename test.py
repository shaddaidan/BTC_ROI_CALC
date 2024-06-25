import streamlit as st
from btc_investment_calculator import calculate_investment_value, plot_historical_prices, df

# Streamlit app
def main():
    # Set page configuration
    st.set_page_config(page_title="Bitcoin Investment Calculator", layout="wide")
    
    # Custom CSS for header and other elements
    st.markdown("""
        <style>
        .header {
            background-color: #4CAF50;
            padding: 20px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            width: 100%;
        }
        .investment-value {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            color: green;
            font-size: 16px;
            font-weight: bold;
            margin: 10px 0;
        }
        .roi {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            color: blue;
            font-size: 16px;
            font-weight: bold;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="header">📈 Historical Bitcoin Investment Calculator</div>', unsafe_allow_html=True)
    
    # Sidebar
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
            st.markdown(f"<div class='investment-value'>The value of the investment on {end_date_str} would be ${investment_value:.2f} 💵</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='roi'>The ROI is {roi_percent:.2f}% 📈</div>", unsafe_allow_html=True)
            plt = plot_historical_prices()
            st.pyplot(plt)  # Ensure the plot is displayed
        else:
            st.error('❌ Error calculating investment value. Please check your input dates.')
    
    # Adding a footer with the author's name
    st.markdown("---")
    st.markdown("<h4>Made by ShaddaiConcepts 😊</h4>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
