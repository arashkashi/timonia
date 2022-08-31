import pandas as pd
import numpy as np

df = pd.read_csv('binancecoin_USDT.csv')
# print(df)

df = df.iloc[:-1, :]
print(type(df))
print(df)

# for index, row in df.iterrows():
# 	if index == 0:
# 		print(row['prices'])

