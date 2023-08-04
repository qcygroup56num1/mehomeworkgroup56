import math
import random
import time

from sympy.ntheory import discrete_log

def primitive_root(n):		# 求最小原根
    k=(n-1)//2
    for i in range(2,n-1):
        if multimod(i,k,n)!=1:
            return i
        
def multimod(a,k,n):    #快速幂取模
    ans=1
    while(k!=0):
        if k%2:         #奇数
            ans=(ans%n)*(a%n)%n
        a=(a%n)*(a%n)%n
        k=k//2          #整除2
    return ans

def isprime(n):
  #检查是否为素数。
  if n <= 1:
    return False
  if n == 2:
    return True
  if n % 2 == 0:
    return False
  for i in range(3, int(n ** 0.5) + 1, 2):
    if n % i == 0:
      return False
  return True


def prime(a, b):
    t = 0
    while t==0:
        i = random.randrange(a, b)
        if isprime(i):
            t=1
    return i

def divisor_number(p):
    for temp in range(pow(2, 10), (p - 1) // 2):
        if (p - 1) % temp == 0 & isprime(temp):
            return temp

def findPrimefactors(s, n):
    d=n%2
    while d == 0:
        s.add(2)
        n = n // 2
        d=n%2
    for m in range(3, int(sqrt(n)), 2):
        while n % m == 0:
            s.add(m)
            n = n // m
    if n > 2:
        s.add(n)


def number(p, q):
    while True:
        k = (p - 1) // q
        x = primitive_root(p)
        y = pow(x, k, p)
        return y


def TA():
    p = prime(pow(2, 30), pow(2, 35))
    q = divisor_number(p)
    params = {
        "p": p,
        "q": q,
        "al": number(p, q),
        "t": random.randrange(1, 20)
    }
    return params

def findPrimitive(n):
    s = set()
    if not isprime(n):
        return -1
    phi = n - 1
    findPrimefactors(s, phi)

    for r in range(2, phi + 1):
        flag = False
        for it in s:
            if pow(r, phi // it, n) == 1:
                flag = True
                break
        if not flag:
            return r
    return -1

def key(params: dict):
    public_key = {
        "al": params["al"],
    }
    private_key = {
        "a": random.randrange(0, params["q"] - 1),
    }
    output = {
        "sk": private_key,
        "pk": public_key
    }
    return output


def identification(params: dict, keys: dict):
    al: int = keys["pk"]["al"]
    p: int = params["p"]
    q: int = params["q"]
    a: int = keys["sk"]["a"]
    t: int = params["t"]
    v = pow(al, -a, p) % p
    k = random.randrange(1, params["q"])
    gamma = pow(al, k, p)
    r = random.randrange(0, 2 ** t - 1)
    y = k + r * a % q
    gammaget = pow(al, y, p) * pow(v, r, p) % p
    if gammaget== gamma:
        print(f"p: {p} \nq: {q} \nal: {al}  \na: {a} \n"
              f" \nt: {t} \nv: {v} \nk: {k} \n"
              f"gamma: {gamma} \nr: {r} \ny: {y}  \ngammaget: {gammaget}")
        
        print("验证成功")
    else:
        print("验证失败")
begin = time.time()
parame = TA()
mykey = key(parame)
identification(parame, mykey)
end = time.time()
print("所用时间为:", end - begin, "s")
