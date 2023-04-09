from math import * 

def gcd(a,b):
    #we know that gcd(a,b) = gcd(|a|,|b|)
    a = -a if a<0 else a 
    b = -b if b<0 else b
    #we need to verify the condition x > y 
    x = b if a < b else a
    y = b if a > b else a 
    #initialisation how the remainder
    r = 1
    #loop to compute the gcd
    while r !=0:
        r = x%y
        x = y 
        y = r
    return x

def extended_gcd(a,b):
    #initialisation of variables needed for computation
    x0,y0= (1,0) 
    x1,y1 = (0,1)
    #We set u & v in order to preserver the value of a & b
    u = a
    v = b 
    #loop to compute extend gcd
    while (v != 0):
        q = u // v
        x2,y2 = (x0 -q*x1),(y0 - q*y1)
        u = v
        v = a*x2 + b*y2
        x0,y0 = x1,y1
        x1,y1 = x2,y2
    #we return the value of rk-1 when rk ==0, with x and y
    return (u,x0,y0)


print("Extend GCD with a = 45 and b = 78 : ",extended_gcd(45,78))
print("Extend GCD with a = 666 and b = 1428 : ",extended_gcd(666,1428))
print("Extend GCD with a = 1020 and b = 10290 : ",extended_gcd(1020,10290))
print("Extend GCD with a = 2**20+4  and b = 3**10+5 : ",extended_gcd(2**20+4,3**10+5))
print("Extend GCD with a = 2**30+1 and b = 3**30+6 : ",extended_gcd(2**30+1,3**30+6))
