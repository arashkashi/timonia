from src.sampler.sampler import Sampler
import pandas as pd
import requests
import time
from binance import Client
from src.utilities.pre_processor import *
from src.utilities.extension_datetime import *
from datetime import date, timedelta, datetime
import numpy as np

# Each sample is in the following format
# {"prices":[[1663333350686,22.26499972222752]],
# "market_caps":[[1663333350686,32433634.79536896]],
# "total_volumes":[[1663333350686,1604323.5003636908]]}
class Sampler20220830(Sampler):
	def __init__(self, id, vs_currency):
		self.id = id
		self.vs_currency = vs_currency

	def next_sample(self):
		sma_window = 14 # rolling sma
		rsp =requests.get(f'https://api.coingecko.com/api/v3/coins/{self.id}/market_chart?vs_currency={self.vs_currency}&days=1')
		json = rsp.json()

		prices = pd.DataFrame(json['prices'])
		prices.rename(columns = { 0 :'timestamp' ,  1 : 'prices' }, inplace = True)

		total_volume = pd.DataFrame(json["total_volumes"])
		total_volume.rename(columns = { 0 :'timestamp' ,  1 : 'total_volume' }, inplace = True)

		market_Cap = pd.DataFrame(json["market_caps"])
		market_Cap.rename(columns = { 0 :'timestamp' ,  1 : 'market_caps' }, inplace = True)

		df = pd.merge(prices, total_volume , on=['timestamp'])
		df = pd.merge(df, market_Cap , on=['timestamp'])

		df['Vol_Mcap_ratio'] = df.total_volume/df.market_caps
		df = df.astype(float)

		client  = Client()
		yesterday_date_in_string = (date.today()- timedelta(days=1)).strftime("%Y-%m-%d")
		klines = pd.DataFrame( client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, yesterday_date_in_string ) )
		klines = klines.iloc[:,:7]
		klines.columns = ['timestamp' , 'Open' , 'High' , 'Low' , 'Close' , 'Volume' , "Close Time"]
		klines = klines.astype(float)
		klines = add_date_column(klines)
		
		df = add_date_column(df)
		df = pd.merge(df, klines , on=['Date'])

		

		df['moving_avg_Vol_MCap'] = df['Vol_Mcap_ratio'].rolling(window=sma_window).mean()

		for i in range(25 , len(df.index)):
			if df.Vol_Mcap_ratio[i] >= np.mean(df.Vol_Mcap_ratio.iloc[:i-1]) + 2*np.std(df.Vol_Mcap_ratio.iloc[:i-1]) :
				df.at[i, 'Un_Norm_Vol_MCap' ] = True
			else :
				df.at[i, 'Un_Norm_Vol_MCap' ] = np.nan

		df = add_pivot_with_heiken(df)

		last_element = df.iloc[-1]

		return last_element



