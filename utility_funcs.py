
#utility functions

def isAnyoneNext(totalTime,finished,arriv,n):
    i = 0
    while(i<n):
        if(totalTime>arriv[i] and finished[i] == 0):
            break
        i += 1
    if i == n:
        return False
    else:
        return True

def check_if_all_finished(finished,n):
    for i in range(n):
        if (finished[i] == 0):
            return False
    
    return True