import pandas as pd
import requests
import sys
sys.path.append('.')
from datetime import datetime
from binance import Client
import numpy as np
from Heiken_pivot import Supp_Res
import os.path
import json

''' main pair is usdt pairs. sometimes miss bakhshi compare it with btc pairs, but is not essential for data base. Hence, for Volume/Mcap just coin_id is needed. '''
PAIR =  'USDT' # 'BTC'#

coins_original = { 'coin_id' : ['curve-dao-token' , 'melon' , 'aragon' , 'aave' , 'convex-finance' , 'binancecoin' , 'litecoin' , 'fantom' , 'frax-share' , 'waves' , 'maker' , 'solana' , 'ripple' , 'avalanche-2' , 'matic-network' , 'sushi' , 'cardano' , 'the-sandbox' , 'decentraland' , 'chainlink' , 'celer-network'  , 'ethereum' ,'bitcoin' ] ,
         'symbol' : [           'CRV' ,             'MLN' ,  'ANT' ,  'AAVE' ,   'CVX' ,               'BNB' ,     'LTC' ,         'FTM' ,      'FXS' ,    'WAVES' ,   'MKR' , 'SOL' ,     'XRP' ,      'AVAX' ,        'MATIC' ,      'SUSHI' ,    'ADA' ,        'SAND' ,        'MANA' ,         'LINK' ,        'CELR' ,        'ETH' ,    'BTC' ] } #  

''' for BTC pairs '''
# coins1 = { 'coin_id' : ['bitcoin' , 'ethereum' , 'binancecoin', 'litecoin' , 'ripple', 'matic-network',  'chainlink' ,  'cardano'  ,   'waves' ,  'curve-dao-token' , 'melon' , 'aragon' , 'aave' , 'convex-finance'  , 'fantom' , 'frax-share'  , 'maker' , 'solana'  , 'avalanche-2'  , 'sushi'  , 'the-sandbox' , 'decentraland' , 'celer-network' ] ,
#          'symbol' : [      'BTC' ,     'ETH'      , 'BNB'    ,     'LTC'       , 'XRP ' ,      'MATIC'    ,  'LINK'   ,      'ada'      ,'WAVES'  ,    'CRV' ,            'MLN' ,   'ANT' ,   'AAVE' ,   'CVX'  ,          'FTM' ,      'FXS' ,       'MKR' ,  'SOL' ,       'AVAX' ,     'SUSHI' ,         'SAND' ,        'MANA' ,           'CELR'  ] } #  

coins = coins_original



sma_window = 14 # rolling sma
last_comparison = 1.1 # second condition : vol/Mcap > 110% last Vol/Mcap
# next_comparison = 1.1 # not needed
firstTimestamp = 1609459200 # correspondind 2021-01-01 ----1609459200 for 1st Jan 2018 = 1514808000000 
''' firstTimestamp must be far enough. if not we will get broken timestamps'''
lastTimestamp = int((datetime.now()).timestamp())
unnormlist = []


for k in range(len(coins['coin_id'])) : #### len(coins['coin_id'])
    coin_id = coins['coin_id'][k]
    print(coin_id)
    try :
        '''coingecko api for total volume $ market cap'''
        rsp =requests.get('https://api.coingecko.com/api/v3/coins/'+coin_id+'/market_chart/range?vs_currency=usd&from='+str(firstTimestamp) + '&to=' + str(lastTimestamp))
        ### 'https://api.coingecko.com/api/v3/coins/avalanche/market_chart/range?vs_currency=usd&from=1609459200&to=1655103009
        rsp = rsp.json()
        
        
    except :
        print('coin_id :: ' + coin_id + ' is not valid.')
        pass
    
    if 'prices' in rsp :
        prices = pd.DataFrame(rsp['prices'])
    else:
        pass
    prices = pd.DataFrame(rsp['prices'])
    prices.rename(columns = { 0 :'timestamp' ,  1 : 'prices' }, inplace = True)

    '''this not volume on Binance. i name it total volume.'''
    '''totla_volumes and market_caps should be added to out data base'''
    total_volume = pd.DataFrame(rsp["total_volumes"])
    total_volume.rename(columns = { 0 :'timestamp' ,  1 : 'total_volume' }, inplace = True)
    

    market_Cap = pd.DataFrame(rsp["market_caps"])
    market_Cap.rename(columns = { 0 :'timestamp' ,  1 : 'market_caps' }, inplace = True)


    df = pd.merge(prices, total_volume , on=['timestamp'])
    df = pd.merge(df, market_Cap , on=['timestamp'])

    '''calculating Vol/Mcap'''
    df['Vol_Mcap_ratio'] = df.total_volume/df.market_caps 


    ###################################################### below not needed for data base #################################################################
    client  = Client()

    klines = pd.DataFrame( client.get_historical_klines(coins['symbol'][k] +PAIR, Client.KLINE_INTERVAL_1DAY, "2018-01-01" ) )
    klines = klines.iloc[:,:7]
    klines.columns = ['timestamp' , 'Open' , 'High' , 'Low' , 'Close' , 'Volume' , "Close Time"]

    
    df = pd.merge(df, klines , on=['timestamp'])
    df = df.astype(float)
    df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    
    # input()
    df['moving_avg_Vol_MCap'] = df['Vol_Mcap_ratio'].rolling(window=sma_window).mean()

    # df['UnNorm_Vol_MCap'] = ""
    for i in range(25 , len(df.timestamp)) :
        if df.Vol_Mcap_ratio[i] >= np.mean(df.Vol_Mcap_ratio.iloc[:i-1]) + 2*np.std(df.Vol_Mcap_ratio.iloc[:i-1]) :
            df.at[i, 'Un_Norm_Vol_MCap' ] = True
        else :
            df.at[i, 'Un_Norm_Vol_MCap' ] = np.nan

    # df['Gr_than_Pr'] = np.where(df.Vol_Mcap_ratio > last_comparison * df.Vol_Mcap_ratio.shift(1) , True , np.nan)
    # df['Gr_than_NEXT'] = np.where(df.Vol_Mcap_ratio > next_comparison * df.Vol_Mcap_ratio.shift(-1) , True , np.nan)
    # df['Greater'] = np.where(df.Vol_Mcap_ratio > next_comparison * df.Vol_Mcap_ratio.shift(-1)  & df.Vol_Mcap_ratio > last_comparison * df.Vol_Mcap_ratio.shift(1) ,
    #                              True , np.nan)

    # df.set_index('timestamp' , inplace=True)

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
    else :
        df.at[ 0 , 'Heiken_color' ] = 'red'

    for i in range( 1 , len(df.Open) ) :
        df.at[ i , 'Heiken_C'] = 0.25 * (df.Open[i] + df.High[i] + df.Low[i] + df.Close[i])
        df.at[ i , 'Heiken_O'] = 0.5 * (df.Heiken_C[i-1] + df.Heiken_O[i-1])
        df.at[ i , 'Heiken_H'] = max(df.Heiken_C[i] , df.Heiken_O[i] , df.High[i])
        df.at[ i , 'Heiken_L'] = min(df.Heiken_C[i] , df.Heiken_O[i] , df.Low[i] )


        if df.Heiken_C[i] > df.Heiken_O[i] :
            df.at[ i , 'Heiken_color' ] = 'green'
        else :
            df.at[ i , 'Heiken_color' ] = 'red'

    
    df['Greater'] = np.where( (df.Vol_Mcap_ratio > last_comparison * df.Vol_Mcap_ratio.shift(1) ) , True , np.nan)

    df['Slope']= round((df.Close -df.Close.shift(1))/df.Close.shift(1) *100 , 2)
    df['Pivot'] = ''

    # for i in range( 1 , len(df.Open) - 1 ) :
    #     if df.Heiken_color[i] != df.Heiken_color[i-1] and df.Heiken_color[i] != df.Heiken_color[i+1]:
    #         df.at[ i , 'Heiken_color' ] = df.Heiken_color[i-1]
    pivots=Supp_Res( df.High , df.Open , df.Close , df.Low , df.timestamp )
    # pivots.to_csv(coins['symbol'][k]+'_pivot.csv')
    for i in range(len(pivots.indexes)) :
        df.at[ pivots.indexes[i] , 'Pivot'] = pivots.type[i]

    df = df.drop(['Heiken_H','Heiken_O','Heiken_C','Heiken_L'], axis = 1)


    # print(df['success_short'].value_counts())
    # print(a)

    df.to_csv(coin_id+'_'+PAIR+'.csv')

    if df['Un_Norm_Vol_MCap'][len(df.index)-1]  == True :
        unnormlist.append(coin_id)




with open('report.txt', 'w') as f:
    for c in unnormlist:
        f.write(f'{c}  is UnNormal')
        f.write('\n')



# print(df)
