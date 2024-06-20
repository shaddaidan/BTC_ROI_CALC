import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# load the historical price data
df = pd.read_csv('crypto_data/btc-usd-max.csv')

# convert the snapped_at to datetime
df['snapped_at'] = pd.to_datetime(df['snapped_at'])

# set the snapped_at as the index
