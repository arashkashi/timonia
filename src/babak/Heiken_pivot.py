from audioop import avg
import sys
sys.path.append(".")
from datetime import datetime
import time
# import websocket
from Unsolved import findMax, findMin
from HeikenAshi import HeikenAshi
from Volatility import Volatality
from Unsolved import findinbetween
import pandas as pd

import numpy
import binance
from Generals import Average
import statistics
import math
from operator import itemgetter





def Supp_Res( highs : pd.core.frame.DataFrame ,
                   opens : pd.core.frame.DataFrame , closes : pd.core.frame.DataFrame ,
                   lows : pd.core.frame.DataFrame , times : pd.core.frame.DataFrame ) :
    # print(HeikenAshi.calculate(highs, opens, closes , lows))
    wave = HeikenAshi.smooth(HeikenAshi.calculate(highs, opens, closes , lows)['Heiken-Ashi unfiltred Wave'])
    # wave = HeikenAshi.smooth2(wave , HeikenAshi.calculate(candlesdata) )
    blocks = HeikenAshi.block(wave)

    PV = 3 # pivot vicinity
    candlesdata = { 'o' : opens.values.tolist() , 'c' : closes.values.tolist() , 'l' : lows.values.tolist() , 'h' : highs.values.tolist() , 't' : times.values.tolist() }
    starting_index = 0
    candids = { "pivot pairs" : [] , "shadow" : [] , "indexes" : [] , "type" : [] , "shadow in range" : [] , "close time" : [] }#pivot pairs : close , shadow : high|low , type: supp|res
    shadow_ratio = 40 # shadow size in percent which is valuble for Supp. and Res. volatility
    
    for j in range(len(blocks['block color'])):
        if wave[ blocks['block end'][j] ] == 'red' :
            pivot_pair = []
            pivot_pair.append( findinbetween( candlesdata['c'] , starting_index , blocks['block end'][j] , 'Min')["value"][0] )
            
            candids['indexes'].append( findinbetween( candlesdata['c'] , starting_index , blocks['block end'][j] , 'Min')["index"][0] )
            candids['close time'].append(pd.to_datetime(candlesdata['t'][candids['indexes'][-1]],unit='ms'))
            pivot_pair.append( findinbetween( candlesdata['l'] , candids['indexes'][-1] - PV , candids['indexes'][-1] + PV , 'Min' )["value"][0] )
            if findinbetween( candlesdata['l'] , starting_index , blocks['block end'][j] , 'Min')["value"][0] != findinbetween( candlesdata['l'] , candids['indexes'][-1] - PV , candids['indexes'][-1] + PV , 'Min' )["value"][0] :
                index = findinbetween( candlesdata['l'] , starting_index , blocks['block end'][j] , 'Min')["index"][0]
                if min(candlesdata['c'][index] , candlesdata['o'][index]) - candlesdata['l'][index] > shadow_ratio / 100 * (candlesdata['h'][index] - candlesdata['l'][index]) :
                    candids["shadow"].append( findinbetween( candlesdata['l'] , starting_index , blocks['block end'][j] , 'Min')["value"][0] )
                    candids['shadow in range'].append('Valid')
                else :
                    candids["shadow"].append( findinbetween( candlesdata['l'] , starting_index , blocks['block end'][j] , 'Min')["value"][0] )
                    candids['shadow in range'].append('Short Shadow')
            else:
                candids['shadow in range'].append('Invalid')
                candids["shadow"].append( findinbetween( candlesdata['l'] , starting_index , blocks['block end'][j] , 'Min')["value"][0] )
            candids["pivot pairs"].append(pivot_pair)
            candids['type'].append('bottom')

            
        else :
            pivot_pair = []
            pivot_pair.append( findinbetween( candlesdata['c'] , starting_index , blocks['block end'][j] , 'Max')["value"][0] )
            candids['indexes'].append( findinbetween( candlesdata['c'] , starting_index , blocks['block end'][j] , 'Max')["index"][0] )
            candids['close time'].append(pd.to_datetime(candlesdata['t'][candids['indexes'][-1]], unit='ms'))
            pivot_pair.append( findinbetween( candlesdata['h'] , candids['indexes'][-1] - PV , candids['indexes'][-1] + PV , 'Max' )["value"][0] )
            if findinbetween( candlesdata['h'] , starting_index , blocks['block end'][j] , 'Max')["value"][0] != findinbetween( candlesdata['h'] , candids['indexes'][-1] - PV , candids['indexes'][-1] + PV , 'Max' )["value"][0] :
                index = findinbetween( candlesdata['h'] , starting_index , blocks['block end'][j] , 'Max')["index"][0]
                if candlesdata['h'][index] - max(candlesdata['o'][index] , candlesdata['c'][index]) > shadow_ratio /100 * (candlesdata['h'][index] - candlesdata['l'][index]) :
                    candids["shadow"].append( findinbetween( candlesdata['h'] , starting_index , blocks['block end'][j] , 'Max')["value"][0] )
                    candids['shadow in range'].append('Valid')
                else :
                    candids["shadow"].append( findinbetween( candlesdata['h'] , starting_index , blocks['block end'][j] , 'Max')["value"][0] )
                    candids['shadow in range'].append('Short Shadow')
            else:
                candids['shadow in range'].append('Invalid')
                candids["shadow"].append( findinbetween( candlesdata['h'] , starting_index , blocks['block end'][j] , 'Max')["value"][0] )
            candids["pivot pairs"].append(pivot_pair)
            candids['type'].append('top')
            
            
        starting_index = blocks['block end'][j]

    a = pd.DataFrame.from_dict(candids , orient='columns')
    return a