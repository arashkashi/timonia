import sys
sys.path.append('.')

def findMin(lst : list , start : int , end : int) : ## indexing is from the end of the list
    minvalue = lst[-start]
    for i in range(start , end + 1):
        #print(i , lst[-i])
        if lst[-i] < minvalue :
            minvalue = lst[-i]
    
    return minvalue

def findMax(lst : list , start : int , end : int) :
    maxvalue = lst[-start]
    for i in range( start , end + 1 ):
        if lst[-i] > maxvalue :
            maxvalue = lst[-i]
    
    return maxvalue

def findinbetween( lst : list , start : int , end : int , pivot : str) -> dict : # pivot denotes if we are searching for min or max
    rsp={ 'value' : [] , 'index' : [] }
    list = []
    indexes=[]
    # print(start,end+1)
    # if end + 1 < len(lst):
    for i in range( start , min(end + 1,len(lst)) , 1 ):
        # print(start,end+1)
        list.append(lst[i])
        indexes.append(i)
    
    if pivot == 'Min' :
        rsp['value'].append(min(list))
        rsp['index'].append(indexes[list.index(min(list))])
    elif pivot == 'Max' :
        rsp['value'].append(max(list))
        rsp['index'].append(indexes[list.index(max(list))])
    else : 
        rsp['value'].append(False)
        rsp['index'].append(False)
    
    return rsp 
    