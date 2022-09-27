import pandas as pd
import time

def add_pivot_with_heiken(df):
	print("8" * 50)
	print(df)
	print("8" * 50)
	df['Heiken_H']=''
	df['Heiken_L']=''
	df['Heiken_O']=''
	df['Heiken_C']=''
	df['Heiken_color'] = ''
	df['Greater']=''

	df.at[ 0 , 'Heiken_H'] = df.High[0]
	df.at[ 0 , 'Heiken_L'] = df.Low[0]
	df.at[ 0 , 'Heiken_O'] = df.Open[0]
	df.at[ 0 , 'Heiken_C'] = df.Close[0]
	if df.Heiken_C[0] > df.Heiken_O[0] :
		df.at[ 0 , 'Heiken_color' ] = 'green'
	else:
		df.at[ 0 , 'Heiken_color' ] = 'red'

	for i in range( 1 , len(df.Open) ) :
		df.at[ i , 'Heiken_C'] = 0.25 * (df.Open[i] + df.High[i] + df.Low[i] + df.Close[i])
		df.at[ i , 'Heiken_O'] = 0.5 * (df.Heiken_C[i-1] + df.Heiken_O[i-1])
		df.at[ i , 'Heiken_H'] = max(df.Heiken_C[i] , df.Heiken_O[i] , df.High[i])
		df.at[ i , 'Heiken_L'] = min(df.Heiken_C[i] , df.Heiken_O[i] , df.Low[i] )


	if df.Heiken_C[i] > df.Heiken_O[i] :
		df.at[ i , 'Heiken_color' ] = 'green'
	else:
		df.at[ i , 'Heiken_color' ] = 'red'

	df['Greater'] = np.where( (df.Vol_Mcap_ratio > last_comparison * df.Vol_Mcap_ratio.shift(1) ) , True , np.nan)

	df['Slope']= round((df.Close -df.Close.shift(1))/df.Close.shift(1) *100 , 2)
	df['Pivot'] = ''

	pivots=Supp_Res( df.High , df.Open , df.Close , df.Low , df.timestamp )

	for i in range(len(pivots.indexes)) :
		df.at[ pivots.indexes[i] , 'Pivot'] = pivots.type[i]

	df = df.drop(['Heiken_H','Heiken_O','Heiken_C','Heiken_L'], axis = 1)
	return df