import pandas as pd
import requests
import sys
sys.path.append('.')
from datetime import datetime
from binance import Client
import numpy as np
from Heiken_pivot import Supp_Res
import os.path
from os import path
import time

if os.path.exists('results') :
    pass
else :
    os.mkdir('results')

stoploss = 0.05
coins = pd.read_csv('futures-list.csv')
coins.columns = ['Row','Coin' , 'coinmarketcap' , 'coingecko']
coins.set_index('Coin', inplace=True)
coins.drop('Row', axis=1, inplace=True) 
coins.drop('coinmarketcap', axis=1, inplace=True) 
coins.dropna(inplace=True)
print(coins)

# import json'''
PAIR =  'USDT' # 'BTC'#
# coins_original = { 'coin_id' : ['curve-dao-token' ,  "lido-dao"   ,   'melon' , 'aragon' , 'aave' , 'convex-finance' , 'binancecoin' , 'litecoin' , 'fantom' , 'frax-share' , 'waves' , 'maker' , 'solana' , 'ripple' , 'avalanche-2' , 'matic-network' , 'sushi' , 'cardano' , 'the-sandbox' , 'decentraland' , 'chainlink' , 'celer-network'  , 'ethereum' ,'bitcoin' ] ,
#          'symbol' : ['CRV' ,   'LDO'  ,   'MLN' ,            'ANT' , 'AAVE' ,   'CVX' ,               'BNB' ,     'LTC' , 'FTM' ,'FXS' , 'WAVES' ,'MKR' ,'SOL' ,'XRP' , 'AVAX' ,    'MATIC' ,  'SUSHI' ,'ADA' , 'SAND' ,  'MANA' ,      'LINK' ,    'CELR' ,  'ETH' ,'BTC' ] } #  

# coins1 = { 'coin_id' : ['bitcoin' , 'ethereum' , 'binancecoin', 'litecoin' , 'matic-network',  'chainlink'   ,   'waves' ,  'curve-dao-token' , 'melon' , 'aragon' , 'aave' , 'convex-finance'  , 'fantom' , 'frax-share'  , 'maker' , 'solana'  , 'avalanche-2'  , 'sushi'  , 'the-sandbox' , 'decentraland' , 'celer-network' , 'optimism' ,    'stepn'  ,    'flow' ,       'apecoin' , 'dogecoin'  , 'near' , 'badger-dao' , 'mirror-protocol' , 'barnbridge' , 'orion-protocol' , 'api3' , 'dydx' , 'origin-protocol' , 'injective-protocol' , 'numeraire' , 'yearn-finance' , 'compound-coin' , 'havven' , 'uniswap' , 'wrapped-nxm'] ,
#          'symbol' : [      'BTC' ,     'ETH'      , 'BNB'    ,     'LTC'        ,      'MATIC'    ,  'LINK'   ,  'WAVES'  ,    'CRV' ,            'MLN' ,   'ANT' ,   'AAVE' ,   'CVX'  ,          'FTM' ,      'FXS' ,       'MKR' ,  'SOL' ,       'AVAX' ,     'SUSHI' ,         'SAND' ,        'MANA' ,           'CELR'    , 'OP'       ,  'GMT'       , 'FLOW'  , 'APE'      , 'DOGE'      , 'NEAR'      ,  'BADGER'     , 'MIR'            , 'BOND'        ,  'ORN'          , 'API3' , 'DYDX' , 'OGN'             , 'INJ'                , 'NMR'       , 'YFI'           , 'COMP'          ,  'SNX'   , 'UNI' ,'WNXM'] } #  , 'near-protocol' , 'NEAR' , 'toncoin'  , 'TON'# , 'ripple',  'cardano'
# # , 'XRP '   ,    'ada'
repeat = []
# coins = coins1
print('Coins in backtest : ',len(coins.index))
df_results = pd.DataFrame(columns=coins.index)
print(df_results)
sma_window = 14 # rolling sma
last_comparison = 1 # condition
next_comparison = 1.1 #
firstTimestamp = 1609459200 # correspondind 2021-01-01 ----1609459200 for 1st Jan 2018 = 1514808000000
lastTimestamp = int((datetime.now()).timestamp())
unnormlist = []
wrong = []

for coin in coins.index : #### len(coins['coin_id'])
    time.sleep(0.5)
    coin_id = coins.coingecko[coin]
    print(coin_id)
    try :
        rsp =requests.get('https://api.coingecko.com/api/v3/coins/'+coin_id+'/market_chart/range?vs_currency=usd&from='+str(firstTimestamp) + '&to=' + str(lastTimestamp))
        if rsp.status_code == 200 :
            print('coin_id for ' + coin + ' is ' + coin_id + ' and OK.')

        else :
            wrong.append(coin)
            print('coin_id for ' + coin + ' is wrong.' )
            continue
        ### 'https://api.coingecko.com/api/v3/coins/avalanche/market_chart/range?vs_currency=usd&from=1609459200&to=1655103009
        rsp = rsp.json()
        
        
    except :
        pass
    
    if 'prices' in rsp :
        prices = pd.DataFrame(rsp['prices'])
    else:
        wrong.append(coin + 'no price')
        print(coin+ ' gives no price.')

        continue
    
    prices.rename(columns = { 0 :'timestamp' ,  1 : 'prices' }, inplace = True)


    total_volume = pd.DataFrame(rsp["total_volumes"])
    total_volume.rename(columns = { 0 :'timestamp' ,  1 : 'total_volume' }, inplace = True)
    

    market_Cap = pd.DataFrame(rsp["market_caps"])
    market_Cap.rename(columns = { 0 :'timestamp' ,  1 : 'market_caps' }, inplace = True)


    df = pd.merge(prices, total_volume , on=['timestamp'])
    df = pd.merge(df, market_Cap , on=['timestamp'])

    df['Vol_Mcap_ratio'] = df.total_volume/df.market_caps 

    client  = Client()

    klines = pd.DataFrame( client.get_historical_klines(coin +PAIR, Client.KLINE_INTERVAL_1DAY, "2018-01-01" ) )
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

    # df.set_index('Date' , inplace=True)

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

    df['Greater'] = np.where(df.Vol_Mcap_ratio > df.Vol_Mcap_ratio.shift(1) * 1.1 , True , np.nan)

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

    df['short_condition'] = np.where((df.Heiken_color.shift(1) == 'green') & (df.Heiken_color.shift(2) == 'green') & (df.Heiken_color.shift(3) == 'green') & (df.Un_Norm_Vol_MCap) & (df.Greater) & (df.Close.shift(1) >df.Open.shift(1)) & (df.Close.shift(2) >df.Open.shift(2)) & (df.Close.shift(3) >df.Open.shift(3)) , True , False) # & (df.Close.shift(3) >df.Open.shift(3)) (df.Un_Norm_Vol_MCap.shift(1) != True) &
    df['short_next_candle_success'] = np.where((df.short_condition) & (df.Close < df.Open), True , False)
    df['short_two_candle_success'] =  np.where((df.short_next_candle_success) & (df.Close.shift(-1) < df.Open.shift(-1)), True , np.nan)

    for i in range(len(df.index)) :
        if df.short_condition[df.index[i]] :
            # if df.Close[df.index[i]] < df.Open[df.index[i]] :
            df.at[i,'percent'] = df.Open[df.index[i]] / df.Close[df.index[i]] 
            # else :
            #     df.at[i,'percent'] = df.Close[df.index[i]]  / df.Open[df.index[i]]
            repeat.append(df.Date[df.index[i]])
        else :
            df.at[i,'percent'] = 1 
    
    df.to_csv('results\\'+coin_id+'_'+PAIR+'.csv')
    

    df_results.at['short_condition',coin] =df['short_condition'].sum()
    df_results.at['short_next_candle_success',coin] =df['short_next_candle_success'].sum()
    df_results.at['short_two_candle_success',coin] =df['short_two_candle_success'].sum()

    df_results.at['Capital' , coin] = round((df['percent'].product()-1)*100,2)

    

    if df['Un_Norm_Vol_MCap'][len(df.index)-1]  == True :  #### -1
        unnormlist.append(coin)




with open('report.txt', 'w') as f:
    for c in unnormlist:
        print(f'{c}  is UnNormal')
        f.write(f'{c}  is UnNormal')
        f.write('\n')

with open('wrong.txt', 'w') as f:
    for c in wrong:
        f.write(f'{c}  id is wrong.')
        f.write('\n')


print(df_results)

df_results.to_csv('results\\result_3Heiken_3last green_short_percent_unprevious.csv')

print(repeat)
print(len(repeat))
repetition = []
for i in repeat :
    
    if repeat.count(i) > 1 :
        print('Date : ' , i , 'repetion : ' , repeat.count(i))
        repetition.append(repeat.count(i))

commonday = 0
for i in range(2, max(repetition) +1) :
    commonday = repetition.count(i) / i * (i-1) + commonday

print('non_common_day : ' , df_results.sum()['short_condition']-commonday)
print('common days : ' , commonday)
