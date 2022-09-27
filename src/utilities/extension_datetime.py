from datetime import date, timedelta, datetime

def add_date_column(df):
	df['Date'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x/1000).strftime("%m/%d/%Y, %H:%M"))
	return df
