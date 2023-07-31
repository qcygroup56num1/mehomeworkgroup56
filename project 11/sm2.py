import time
import random
from gmssl import sm3

p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1711D7C3A431D7C90
Gy = 0xD59796F4FE9EDD6B7D8B9C583CE2D3695A9E13641146433FBCC939DCE249296B
IDA=0x234C49481278122212567776555
IDB=0x66474383374646446474759
message="test202100210057"


def RFC6979(num):
    n=int(sm3.sm3_hash(list(num)),16)
    return n

def get_bitsize(num):
    length=0
    while num/256:
        length+=1
        num=int (num/256)
    return length

def bytes_to_int(bytes):
    n=int.from_bytes(bytes,byteorder='little')
    return n

def int_to_bytes(num):
    n=num.to_bytes(get_bitsize(num),byteorder='little', signed=False)
    return n

# 求最大公约数
def get_gcd(x, y):
    if y == 0:
        return x
    if x==0:
        return y
    while y!=0:
        x,y=y,x%y
    return x

def get_inverse(a,m):#求模逆

        if get_gcd(a,m)!=1:
            return None
        u1,u2,u3 = 1,0,a
        v1,v2,v3 = 0,1,m
        while v3!=0:
            q = u3//v3
            v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
        return u1%m



    # 计算P+Q函数



def calculate_p_q(x1, y1, x2, y2, a, b, p):
    flag = 1  # 符号位
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 分子
        denominator = y1 * 2  # 分母

    # 若P≠Q，则k=(y2-y1)/(x2-x1) mod p
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

    # 求分母逆元
    inverse_value = get_inverse(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]


# 计算2P
def calculate_2p(p_x, p_y, a, b, p):
    temx = p_x
    temy = p_y
    pvalue = calculate_p_q(temx, temy, p_x, p_y, a, b, p)
    temx = pvalue[0]
    temy = pvalue[1]
    return pvalue


# 计算nP
def calculate_np(p_x, p_y, n, a, b, p):
    p_value = ["0", "0"]
    p_temp = [0, 0]
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

def key():
    dA=random.randrange(0,n)
    PA=calculate_np(Gx, Gy, dA, a, b, p)
    return dA,PA




#调用
def signRFC6979(msg,ID):
    print("输入信息：",message)
    r=0
    s=0
    dA, PA= key()
    M=message.encode()
    ENTL=8*get_bitsize(ID)
    data = ENTL.to_bytes(2,byteorder='little', signed=False)+int_to_bytes(ID)+int_to_bytes(a)+int_to_bytes(b)+int_to_bytes(Gx)+int_to_bytes(Gy)+int_to_bytes(PA[0])+int_to_bytes(PA[1])
    ZA = int(sm3.sm3_hash(list(data)),16)
    M_=int_to_bytes(ZA)+M
    e=int(sm3.sm3_hash(list(M_)),16)
    num=int_to_bytes(random.randrange(10000,100000))+int_to_bytes(ID)+"mysm3RFC6979".encode()
    
    #k的处理过程
    print("key的输入为：")
    print(num)
    REALk=RFC6979(num)%n
    print("经过RFC6979的key为:")
    print(REALk)
    
    while True:
        x1,y1=calculate_np(Gx, Gy, REALk, a, b, p)
        r=(x1+e)%n
        sign=(get_inverse(1+dA,n)*(REALk-r*dA))%n
        if sign!=0 and r!=0 and r+REALk != n :
            REALk=(REALk+1)%n
            break
    print("签名为：")
    return r,s

begin=time.time()
print(signRFC6979(message,IDA))
end=time.time()
print("消耗时间：",(end-begin)*1000,"ms")
