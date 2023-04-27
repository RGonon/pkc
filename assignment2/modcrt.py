def to_bin(n):
    s=""
    while n!=0:
        r = n%2
        s = str(r) + s
        n//=2
    return s

def mod_exp(a,e,n):
    b = to_bin(e)
    s = 1
    l = len(b)
    r=0
    for i in range(l):
        if b[i] == "1":
            r = (s*a) % n
        else:
            r = s
        s= (r**2) % n
    return r

print("Modular exp of 3^12345 mod 97: ",mod_exp(3, 12345, 97))
print("Modular exp of 3^123456789012345 mod 976: ",mod_exp(3, 123456789012345, 976))
print()
def extended_gcd(a,b):
    x0,y0= (1,0) 
    x1,y1 = (0,1)
    u = a
    v = b 
    while (v != 0):
        q = u // v
        x2,y2 = (x0 -q*x1),(y0 - q*y1)
        u = v
        v = a*x2 + b*y2
        x0,y0 = x1,y1
        x1,y1 = x2,y2
    return (u,x0,y0)

def crt(p,q,a,b):
    res = extended_gcd(p,q)
    x = (b*p*res[1]) + (a*q*res[2])
    return x % (p*q)

print("CRT with x ≅ 1 mod 10 and x ≅ 2 mod 21: ",crt(10, 21, 1, 2))
print("CRT with x ≅ 11 mod 257 and x ≅ 13 mod 293: ",crt(257, 293, 11, 13))
print()
def crt_list(primes,values):
    res = 0
    N = 1
    i= 0
    lenght = len(primes)
    while i < lenght:N*=primes[i]; i+=1
    for i in range(lenght):
        N_i = (N//primes[i])
        inv = extended_gcd(N_i,primes[i])[1]
        res = (res+ values[i]*inv* N_i)% N
    return res
    

print("CRT List [10,21,29] and [1,2,3]: ",crt_list([10, 21, 29], [1, 2, 3]))
print("CRT List [257,293,337] and [11,13,31]: ",crt_list([257, 293, 337], [11, 13, 31]))
