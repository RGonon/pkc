import hashlib 
import random

def gcd(a,b):
    a = -a if a<0 else a 
    b = -b if b<0 else b
    x = b if a < b else a
    y = b if a > b else a 
    r = 1
    while r !=0:
        r = x%y
        x = y 
        y = r
    return x

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

def miller_rabin(n):
    t = 2 
    k = 0
    while (n-1)%t==0:
        t *=2
        k +=1
    m = (n-1)//(2**k)
    a = random.randint(2,(n-2))
    b = mod_exp(a,m,n)
    if b == 1 or b == -1:
        return True
    b_k = 1
    while b_k < k:
        b = mod_exp(b,2,n)
        if b == 1:
            return False
        elif b == n-1: 
        #n-1 instead of -1 bc python does not return negative mod
            return True 
        b_k += 1
    return False if b != n-1 else True  


def rsa_pks_genkey(key_length):
    a = False
    b = False
    k = key_length //2
    while not a:
        p = random.randint(2**(k-1),2**k-1)
        if p %2 ==0:
            p = p+1 if p<2**k-1 else p-1
        a = miller_rabin(p)
    while not b:
        q = random.randint(2**(k-1),2**k-1)
        if q %2==0:
            q = q+1 if q<2**k-1 else q-1
        b = miller_rabin(q)
    n = p*q
    e = 65537
    phi = (p-1)*(q-1)
    if gcd(e,phi) !=1:
        return rsa_genkey(key_length)
    d = extended_gcd(phi,e)[2]
    d = d%phi if d<0 else d
    m = hashlib.sha1() 
    return (p,q,d),(n,e,m)


def rsa_pks_sign(m,sk,pk):
    hash_fun = pk[2].copy()
    hash_fun.update((str(m)).encode())
    h = hash_fun.digest()
    h= int.from_bytes(h,"big")%pk[0]
    return mod_exp(h,sk[2],pk[0])

def rsa_pks_verify(sig,m,pk):
    s =  mod_exp(sig,pk[1],pk[0])
    hash_fun = pk[2].copy()
    hash_fun.update((str(m)).encode())
    h = hash_fun.digest()
    h = int.from_bytes(h,"big")%pk[0]
    return 1 if s ==h else 0


key_length = 256
sk,pk = rsa_pks_genkey(key_length)
m = 1234
sig = rsa_pks_sign(m,sk,pk)
print(rsa_pks_verify(sig,m,pk))


key_length = 512
sk,pk = rsa_pks_genkey(key_length)
m = 1234
sig = rsa_pks_sign(m,sk,pk)
print(rsa_pks_verify(sig,m,pk))

key_length = 1024
sk,pk = rsa_pks_genkey(key_length)
m = 1234
sig = rsa_pks_sign(m,sk,pk)
print(rsa_pks_verify(sig,m,pk))
