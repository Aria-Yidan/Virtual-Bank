# -*- coding:UTF-8 -*-

"""
http://wenku.baidu.com/link?url=N0x5Y00a2JpAP1VNXA571HZ6vVCagk3VevommDyNDMS8iqO1C-HqX6LQhOpHNpb1N5cz7VjDic2iob6F1T4QhK73rQBQQvwv86Hx29GAqpO
"""

#--RSA--#
import random

def _aks_(a,n):
    a1 = pow(17-a,n,n)
    a2 = pow(17,n,n) - (a % n)
    if a1 == a2:
        return 1
    else:
        return 0
        
def get_hugeprime():
    flag = 0
    while not flag:
        n = random.randrange(2**4,2**6)
        if (n%2==0 or n%3==0 or n%5==0 or n%7==0 or n%13==0):
            continue
        flag = _aks_(2,n)
    return n

def gcd(a,b):
    temp = a
    if (a < b):
        a = b
        b = temp
    while (b != 0):
        temp = a % b
        a = b
        b = temp
    return (a,b)

def product_e(euler_n):     
	tepflag=1
     	while tepflag:          	
		e=random.randrange(euler_n)
		if (gcd(e,euler_n)==(1,0)):
			tepflag=0
	return e 

def extended_euclid(a,b):
    X1=1
    X2=0
    X3=b
    Y1=0
    Y2=1
    Y3=a
    while (Y3!=1):
        if Y3==0:
            return 0
        Q=X3/Y3
        T1=X1-Q*Y1
        T2=X2-Q*Y2
        T3=X3-Q*Y3
        X1=Y1
        X2=Y2
        X3=Y3
        Y1=T1
        Y2=T2
        Y3=T3
    return Y2%b


def getRSA():
    #-- random prime p and q--#
    p = get_hugeprime()
    q = get_hugeprime()
    while (p == q):
        q = get_hugeprime()
    
    n = p * q
    euler_n = (p-1) * (q - 1) 
    d = 0
    while(d == 0):
        e = product_e(n)
        d = extended_euclid(e,euler_n)
    
    return [n,euler_n,e,d]

def RSA_encrypt(m, e, n):
    C = []    
    M = m.lower()
    print "M=",M
    for i in M:
        C.append(pow(ord(i),e,n))
    return C

def RSA_Decrypt(c, d, n):
    M = []
    for i in c:
        M.append(chr(pow(i,d,n)))
    m = ''.join(M)
    return m
#"""
rsa = getRSA()
print rsa
m = "ABCDEFG"
c = RSA_encrypt(m,rsa[2],rsa[0])
print c
print RSA_Decrypt(c,rsa[3],rsa[0])
message = "一二三"

#"""