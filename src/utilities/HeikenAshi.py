import sys
sys.path.append('.')
import pandas as pd

class HeikenAshi():
    
    def calculate(highs : pd.core.frame.DataFrame , opens : pd.core.frame.DataFrame ,
                  closes : pd.core.frame.DataFrame, lows : pd.core.frame.DataFrame) -> pd.core.frame.DataFrame :
        HeikenCandles = { 'c':[] , 'o':[] , 'h':[] , 'l':[] , 'wave' : [] }
        candlesdata = { 'c':closes.values.tolist() , 'o': opens.values.tolist() , 'h':highs.values.tolist() , 'l': lows.values.tolist() }
        for i in range(len(candlesdata['o'])):
            if i==0 :
                HeikenCandles['o'].append(candlesdata['o'][i])
                HeikenCandles['c'].append( 0.25 * ( candlesdata['c'][i] + candlesdata['o'][i] + candlesdata['l'][i] + candlesdata['h'][i] ) )
                HeikenCandles['h'].append( max( HeikenCandles['o'][-1] , HeikenCandles['c'][-1] , candlesdata['h'][i] ) )
                HeikenCandles['l'].append( min( HeikenCandles['o'][-1] , HeikenCandles['c'][-1] , candlesdata['l'][i] ) )
            else :
                HeikenCandles['o'].append( ( HeikenCandles['o'][-1] + HeikenCandles['c'][-1] ) / 2 )
                HeikenCandles['c'].append( 0.25 * ( candlesdata['c'][i] + candlesdata['o'][i] + candlesdata['l'][i] + candlesdata['h'][i] ) )
                HeikenCandles['h'].append( max( HeikenCandles['o'][-1] , HeikenCandles['c'][-1] , candlesdata['h'][i] ) )
                HeikenCandles['l'].append( min( HeikenCandles['o'][-1] , HeikenCandles['c'][-1] , candlesdata['l'][i] ) )
            
            if HeikenCandles['c'][i] > HeikenCandles['o'][i] :
                HeikenCandles['wave'].append('green')
            else:
                HeikenCandles['wave'].append('red') 

        
        
        return pd.DataFrame(list(HeikenCandles['wave']), columns =["Heiken-Ashi unfiltred Wave"])

    def smooth( wave : list) -> list :
        for i in range( 1 , len(wave) - 1 , 1 ) : # smoothing
            if wave[i] != wave[ i - 1 ] and wave[i] != wave[ i + 1 ] :
                wave[i] = wave[ i - 1 ]
        
        return wave

    def smooth2( wave : list , Heikencandlesdata : dict ) -> list :
        for i in range( 2 , len(wave) - 2 , 1 ) : # smoothing
            if wave[i] != wave[ i - 1 ] and wave[i] == wave[ i + 1 ] and  wave[i+2] !=wave[i] :
                # if wave[i] == 'green' and Heikencandlesdata['l'][i+1] != Heikencandlesdata['o'][i+1] :
                    wave[i] = wave[ i - 1 ]
                    wave[ i + 1 ] = wave[ i - 1 ]
                # elif wave[i] == 'red' and Heikencandlesdata['h'][i+1] != Heikencandlesdata['o'][i+1] :
                    wave[i] = wave[ i - 1 ]
                    wave[ i + 1 ] = wave[ i - 1 ]
        return wave
        
    def block( smoothed_wave : list ) -> dict :
        rsp = { 'block end' : [] , 'block color' : [] }
        for i in range( 1 , len(smoothed_wave) , 1 ) :
            if smoothed_wave[i] != smoothed_wave[i-1]:    
                rsp['block end'].append( i - 1 )
                rsp['block color'].append(smoothed_wave[i-1])

        return rsp
        

