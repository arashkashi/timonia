import sys
sys.path.append(".")
import math
import statistics

def ExponentialMovingAverage(order : int , LastValue : float , CurrentValue :float) -> float:
    return CurrentValue * 2 / (order + 1) + LastValue * (order - 1) / (order + 1)

def Average(list : list) -> float:
    return sum(list) / len(list)

def Closer( list : list , value :  float ) -> float :
    diff = []
    for x in list :
        diff.append(abs( x - value ) )
    return list[diff.index(min(diff))]

def drop_Unnormal( lst : list ) -> list :
    if len(lst) > 2 :
        sigma = math.sqrt(statistics.variance(lst)) / Average(lst) 
        while  len(lst) > 2 and ( max(lst) > ( 1 + sigma ) * Average(lst) or min(lst) < ( 1- sigma ) * Average(lst) ) :
            # sigma = math.sqrt(statistics.variance(lst)) / Average(lst)

            lst_rev = []
            dist = []

            for x in lst :
                dist.append( abs( x - Average(lst) ) )

            MaxDist = max(dist) 

            for i in range( len(lst) ) :
                if dist[i] < MaxDist :
                    lst_rev.append( lst[i])

            lst = lst_rev
            sigma = math.sqrt(statistics.variance(lst)) / Average(lst)

        return lst

    else : 
        return lst