import sys
sys.path.append('.')
import statistics
from src.utilities.Generals import *
import math
import pandas as pd 

class Volatality():
    def calculate(highs : pd.core.frame.DataFrame ,
                   opens : pd.core.frame.DataFrame , closes : pd.core.frame.DataFrame ,
                   lows : pd.core.frame.DataFrame ) -> dict :
        Volatality = { "OC_AVG_volatility" : [] , "HL_AVG_volatility" : [] , "OCvariance" : [] , "HLvariance" : [] , "OC" : [] , "HL" : [] }
        candlesData = { 'o' : opens.values.tolist() , 'c' : closes.values.tolist() , 'l' : lows.values.tolist() , 'h' : highs.values.tolist() }
               
        for i in range(len(candlesData['o'])):
            Volatality['OC'].append( ( candlesData['c'][i] - candlesData['o'][i] ) / candlesData['o'][i] )
            Volatality['HL'].append( ( candlesData['h'][i] - candlesData['l'][i] ) / candlesData['l'][i] )
        
        
        
        Volatality['OC_AVG_volatility'].append( Average( Volatality['OC'] ) )
        Volatality['HL_AVG_volatility'].append( Average( Volatality['HL'] ) )

        Volatality['OCvariance'].append( round( math.sqrt( statistics.variance( Volatality['OC'] ) ) , 3 ) ) 
        Volatality['HLvariance'].append( round( math.sqrt( statistics.variance( Volatality['HL'] ) ) , 3 ) )

        return Volatality
