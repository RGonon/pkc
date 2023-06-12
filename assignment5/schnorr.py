import hashlib 
import math
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

def generate_prime_subgroup(plen, qlen = 160):
    a1 = False
    b = False
    while not a1:
        q = random.randint(2**(qlen-1),2**qlen-1)
        if q %2==0:
            q = q+1 if q<2**qlen-1 else q-1
        a1 = miller_rabin(q) and ((math.log2(q)//1) >= qlen-1)
    while not b:
        k = random.randint(2**(plen-qlen-1),(2**(plen-qlen)-1))
        p = k*q+1
        if p % 2 == 0:
            p = p + 1 if p < 2 ** (plen-qlen)- 1 else p-1
        b = miller_rabin(p)
    a = random.randint(2,p-1)
    g = mod_exp(a,k,p)
    return (p,q,g)

def schnorr_setup(plen):
    pp = generate_prime_subgroup(plen)
    return pp

def schnorr_genkey(pp):
    a = random.randint(1,pp[1]-1) 
    A = mod_exp(pp[2],a,pp[0])
    H = hashlib.sha1() 
    sk = a
    pk = (pp[0],pp[1],pp[2],A,H)
    return sk,pk

def schnorr_hash(R, msg, q):
    s = 0 
    for c in msg:
        s+=ord(c)
    hash_fun = hashlib.sha1()
    res = (R | s)
    hash_fun.update(str(res).encode())
    h = hash_fun.digest()
    h = int.from_bytes(h,"big") %q
    return h

def schnorr_sign(msg, sk, pp):
    r = random.randint(0,pk[1]-1)
    R = mod_exp(pk[2],r,pk[0])
    h = schnorr_hash(R,msg,pp[1])
    s = (r + sk * h) % pp[1]
    return (R,s)

def schnorr_verify(sig, msg, pk, pp):
    h = schnorr_hash(sig[0],msg,pp[1])
    left = mod_exp(pk[2],sig[1],pk[0])
    right = (sig[0]*mod_exp(pk[3],h,pk[0]))%pk[0]
    return 1 if left == right else 0 


plen = 256
for i in range(4):
    print("Schnorr signing with key lenght = ",plen)
    pp = schnorr_setup(plen)
    sk,pk = schnorr_genkey(pp)
    msg = "This is a text message"
    print(msg)
    sig = schnorr_sign(msg, sk, pp)
    print(schnorr_verify(sig, msg, pk, pp))
    plen=plen*2
    print()
