import hashlib
import gmssl
import random
import time

#参数：secp256r1
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

def int_to_bytes(num):
    return num.to_bytes(get_bitsize(num),byteorder='little', signed=False)
def bytes_to_int(bytes):
    return int.from_bytes(bytes,byteorder='little')

def get_inverse(a,m):#模逆

        if get_gcd(a,m)!=1:
            return None
        u1,u2,u3 = 1,0,a
        v1,v2,v3 = 0,1,m
        while v3!=0:
            q = u3//v3
            v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
        return u1%m

# 求最大公约数——用于约分化简
def get_gcd(x, y):
    if y == 0:
        return x
    if x==0:
        return y
    while y!=0:
        x,y=y,x%y
    return x

def calculate_p_q(x1, y1, x2, y2, a, b, p):
    sign = 1  # 符号位
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 分子
        denominator = 2 * y1  # 分母
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            sign = 0
            member = abs(member)
            denominator = abs(denominator)
    # 分子和分母化简
    gcd_value = get_gcd(member, denominator)
    member = member // gcd_value
    denominator = denominator // gcd_value
    # 分母逆元
    inverse_value = get_inverse(denominator, p)
    k = (member * inverse_value)
    if sign == 0:
        k = -k
    k = k % p
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]


# 计算2P
def calculate_2p(p_x, p_y, a, b, p):
    tem_x = p_x
    tem_y = p_y
    p_value = calculate_p_q(tem_x, tem_y, p_x, p_y, a, b, p)
    tem_x = p_value[0]
    tem_y = p_value[1]
    return p_value


# 计算nP
def calculate_np(p_x, p_y, n, a, b, p):
    p_value = ["0", "0"]
    p_temp = [0, 0]
    # 因为分数没有取模运算，不考虑b小于0
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

def get_key():
    private=random.randrange(0,n)
    public=calculate_np(Gx, Gy, dA, a, b, p)
    return private,public

def get_bitsize(number):
    length=0
    while number/256:
        length+=1
        num=int (number/256)
    return length

message="test_hello_world"
print("消息：",message)
P=[12347259512020005462763638353364532312367891845761963173968514567546337027094, 12346944205781153898153509065115980357578581414964392335433501542694784316391]
r,s=65713732757593917641705955129814776632782548295209210156195240041086117167123, 54432546964026281203981084782644312411948733933855404654835874846733002636486
def forge_ECDSA():
    def forge_sign():
        u = random.randrange(1, n)
        v = random.randrange(1, n)
        temp = calculate_np(Gx, Gy, u, a, b, p)
        temp2 = calculate_np(P[0], P[1], v, a, b, p)
        R = x, y = calculate_p_q(temp[0], temp[1], temp2[0], temp2[1], a, b, p)
        fr = x % n
        fs = (fr * get_inverse(v, n)) % n
        fe = (fr * u * get_inverse(v, n)) % n
        return fr, fs, fe
    r,s,e=forge_sign()
    print("伪造签名：")
    print(r,s)
    def verify(r,s,e):
        k = get_inverse(s, n)
        temp = calculate_np(Gx, Gy, e * k, a, b, p)
        temp2 = calculate_np(P[0], P[1], r * k, a, b, p)
        R, S = calculate_p_q(temp[0], temp[1], temp2[0], temp2[1], a, b, p)
        if (R== r):
            return True
        else:
            return False
    return verify(r,s,e)

begin=time.time()
print(forge_ECDSA())
end=time.time()
print("消耗的时间为",end-begin,"s")

