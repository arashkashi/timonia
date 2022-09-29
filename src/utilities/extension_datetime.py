from datetime import date, timedelta, datetime
import pandas as pd

def add_date_column(df, timestamp_key='timestamp'):
	df['Date'] = df[timestamp_key].apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%m/%d/%Y, %H:%M"))
	return df
