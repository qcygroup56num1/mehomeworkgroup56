from gmssl import sm3
from hashlib import sha1
import random
import time
import math

#SM3参数：
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

def get_inverse(a,m):#求模逆

        if get_gcd(a,m)!=1:
            return None
        u1,u2,u3 = 1,0,a
        v1,v2,v3 = 0,1,m
        while v3!=0:
            q = u3//v3
            v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
        return u1%m


def pow_mod(a, b, n):
    a = a % n
    answer = 1
    # 因为分数没有取模运算，所以不需要考虑b小于0的情况
    while b != 0:
        if b & 1:
            ans = (ans * a) % n
        b=b-1
        a = (a * a) % n
    return answer

def is_prime(n):
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

# 求最大公约数
def get_gcd(x, y):
    if y == 0:
        return x
    if x==0:
        return y
    while y!=0:
        x,y=y,x%y
    return x


def get_Qr(n,p):
    # 求勒让德符号
    def Legender(a, p):
        return pow_mod(a, (p - 1) >> 1, p)

    class T:
        p = 0
        d = 0

    w = 0
    a=0
    t=0
    while True:
        a=random.randrange(1,p)
        t= a*a-n
        w = t%p
        if Legender(w,p)+1==p:
            break
    temp=T()
    temp.p = a
    temp.d = 1
    ans = power_mod(temp, (p + 1) >> 1, p)
    return ans.p,p-ans.p

def calculate_p_q(x1, y1, x2, y2, a, b, p):
    flag = 1  # 符号位
    # P = Q，则k=[(3x1^2+a)/2*y1]mod p
    if x1 == x2 and y1 == y2:
        member = 3 * (x1** 2) + a 
        denominator =  y1*2
    # P≠Q，则k=(y2-y1)/(x2-x1) mod p
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)
    # 化简分子和分母
    gcd_value = get_gcd(member, denominator)
    member = member // gcd_value
    denominator = denominator // gcd_value
    # 求逆
    inverse = get_inverse(denominator, p)
    k = (member * inverse)
    if flag == 0:
        k = -k
    k = k % p
    # 计算x3,y3
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]


# 计算2P
def calculate_2p(px, py, a, b, p):
    tem_x = px
    tem_y = py
    value =calculate_p_q(tem_x, tem_y, px, py, a, b, p)
    tem_x = value[0]
    tem_y = value[1]
    return p_value


# 计算nP
def calculate_np(p_x, p_y, n, a, b, p):
    p_value = ["0", "0"]
    p_temp = [0, 0]
    #因为分数没有取模运算，所以不考虑b小于0
    while n != 0:
        if n & 1:
            if (p_value[0] == "0" and p_value[1] == "0"):
                p_value[0], p_value[1] = p_x, p_y
            else:
                p_value = calculate_p_q(p_value[0], p_value[1], p_x, p_y, a, b, p)
        n >>= 1
        p_temp = calculate_2p(p_x, p_y, a, b, p)
        p_x, p_y = p_temp[0], p_temp[1]
    return p_value

def calculate_Tp(px, py,a, b, p):
    return px,p-py

def get_key():
    private=random.randrange(0,n)
    public=calculate_np(Gx, Gy, private, a, b, p)
    return private,public

def get_bitsize(num):
    len=0
    while num/256:
        len+=1
        num=int (num/256)
    return len

def int_to_bytes(num):
    return num.to_bytes(get_bitsize(num),byteorder='big', signed=False)
def bytes_to_int(bytes):
    return int.from_bytes(bytes,byteorder='big')




message="text202100210057"
def ECDSA():
    public=[0,0]
    def ECDSA_sign(msg):
        start_time=time.time()
        nonlocal  public
        M = message.encode()
        private, public = get_key()
        k = random.randrange(1, n)
        R = calculate_np(Gx, Gy, k, a, b, p)
        r = R[0] % n
        e = int(sha1(M).hexdigest(), 16)
        s = (get_inverse(k, n) * (e + private * r)) % n
        end_time=time.time()
        print("待签消息：",message)
        print("生成的签名为：")
        print(r,s)
        print(public)
        print(e)
        print("签名用的时间：",(end_time-start_time)*1000,"ms")
        return r, s

    def ECDSA_verif_sign(msg, sign):
        start_time = time.time()
        r, s = sign
        M = message.encode()
        e = int(sha1(M).hexdigest(), 16)
        w = get_inverse(s, n)
        temp1 = calculate_np(Gx, Gy, e * w, a, b, p)
        temp2 = calculate_np(public[0], public[1], r * w, a, b, p)
        R, S = calculate_p_q(temp1[0], temp1[1], temp2[0], temp2[1], a, b, p)
        end_time= time.time()
        if (r == R):
            print("验证通过")
            print("验证用的时间：", (end_time - start_time)*1000, "ms")
            return True

        else:
            return False
    return ECDSA_verif_sign(message,ECDSA_sign(message))

r,s=41159732757593917641705955129814776632782548295209210156195240041086117167123, 57859546964026281203981084782644312411948733933855404654835874846733002636486
P=[26877259512020005462763638353364532382639391845761963173968516804546337027093, 48566944205781153898153509065115980357578581414964392335433501542694784316391]

def write_ECDSA():
    def forge_sign():
        u = random.randrange(1, n)
        v = random.randrange(1, n)
        temp1 = calculate_np(Gx, Gy, u, a, b, p)
        temp2 = calculate_np(P[0], P[1], v, a, b, p)
        R = x, y = calculate_p_q(temp1[0], temp1[1], temp2[0], temp2[1], a, b, p)
        f_r = x % n
        f_e = (f_r * u * get_inverse(v, n)) % n
        f_s = (f_r * get_inverse(v, n)) % n
        return f_r, f_s, f_e

    r,s,e=forge_sign()

    def verify(r,s,e):
        w = get_inverse(s, n)
        temp = calculate_np(Gx, Gy, e * w, a, b, p)
        temp2 = calculate_np(P[0], P[1], r * w, a, b, p)
        R, S = calculate_p_q(temp[0], temp[1], temp2[0], temp2[1], a, b, p)
        if (R == r):
            return True
        else:
            return False
    return verify(r,s,e)

print(write_ECDSA())

print(ECDSA())


