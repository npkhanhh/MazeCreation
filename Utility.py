import math as m

def findNearSquaredNumber(n):
    if m.sqrt(n).is_integer():
        return int(m.sqrt(n))
    bigger = n+1
    smaller = n-1
    while True:
        if m.sqrt(bigger).is_integer():
            return int(m.sqrt(bigger))
        if m.sqrt(smaller).is_integer():
            return int(m.sqrt(smaller))
        bigger = bigger+1
        smaller = smaller-1