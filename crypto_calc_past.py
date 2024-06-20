import pandas as pd

# load the historical price data
df = pd.read_csv("crypto_data/btc-usd-max.csv")

# convery the snapped_at to datetime
df['snapped_at'] = pd