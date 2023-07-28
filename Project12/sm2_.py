import random
from gmssl import sm3


#SM3推荐参数：secp256r1
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498

b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

k = 0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F

IDA=0x414C494345313233405941484F4F2E434F4D
IDB=0x414C4943453132334414C4943453132334
bPA=[]
#print(hashlib.sha1("123".encode()).hexdigest())

def show_points(p, a, b):
    return [(x, y) for x in range(p) for y in range(p) if (y * y - (x * x * x + a * x + b)) % p == 0]


def GCD(a, b):
    if b == 0:
        return a
    else:
        return GCD(b, a % b)


def XGCD(a, b):
    if (b == 0):
        return 1, 0, a
    else:
        x, y, d = XGCD(b, a % b)
        return y, (x - (a // b) * y), d


# print(XGCD(6553215,5754840))

def get_inverse(a, b):
    return XGCD(a, b)[0] % b


def pow_mod(a, b, n):
    a = a % n
    ans = 1
    # 这里我们不需要考虑b<0，因为分数没有取模运算
    while b != 0:
        if b & 1:
            ans = (ans * a) % n
        b >>= 1
        a = (a * a) % n
    return ans


def get_miller(m):
    while (m % 2 == 0):
        m = m // 2
    return m


def rabin_miller(p):
    if p == 2:
        return True
    elif p % 2 == 0:
        return False
    else:
        m = p - 1
        m = get_miller(m)
        the_pow_mod = pow_mod(2, m, p)
        if the_pow_mod == 1:
            return True
        a = m

        while (a <= p - 1):
            the_pow_mod = the_pow_mod ** 2 % p
            if the_pow_mod == 1:
                return True
            a = a * 2
        return False


# 求最大公约数——用于约分化简
def get_gcd(x, y):
    if y == 0:
        return x
    else:
        return get_gcd(y, x % y)

    # 计算P+Q函数



def get_Qr(n,p):
    # 求勒让德符号
    def Legender(a, p):
        return pow_mod(a, (p - 1) >> 1, p)

    class T:
        p = 0
        d = 0

    w = 0

    def multi_er(a, b, m):
        ans = T()
        ans.p = (a.p * b.p % m + a.d * b.d % m * w % m) % m
        ans.d = (a.p * b.d % m + a.d * b.p % m) % m
        return ans

    def power(a, b, m):
        ans = T()
        ans.p = 1
        ans.d = 0
        while b:
            if b & 1:
                ans = multi_er(ans, a, m);
                b -= 1
            b >>= 1
            a = multi_er(a, a, m)
        return ans
    a=0
    t=0
    while True:
        a=random.randrange(1,p)
        t= a*a-n
        w = t%p
        if Legender(w,p)+1==p:
            break
    tmp=T()
    tmp.p = a
    tmp.d = 1
    ans = power(tmp, (p + 1) >> 1, p)
    return ans.p,p-ans.p

def calculate_p_q(x1, y1, x2, y2, a, b, p):#p+q
    flag = 1

    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a
        denominator = 2 * y1

    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    gcd_value = get_gcd(member, denominator)
    member = member // gcd_value
    denominator = denominator // gcd_value

    inverse_value = get_inverse(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p

    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]


def calculate_2p(p_x, p_y, a, b, p):#2p
    tem_x = p_x
    tem_y = p_y
    p_value = calculate_p_q(tem_x, tem_y, p_x, p_y, a, b, p)
    tem_x = p_value[0]
    tem_y = p_value[1]
    return p_value


def calculate_np(p_x, p_y, n, a, b, p):#np
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

def calculate_Tp(p_x, p_y,a, b, p):
    return p_x,p-p_y

def get_key():
    dA=random.randrange(0,n)
    PA=calculate_np(Gx, Gy, dA, a, b, p)
    return dA,PA

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


def sign(msg,ID,dA,PA):
    global ZA
    M=msg.encode()
    ENTL=get_bitsize(ID)*8
    data = ENTL.to_bytes(2,byteorder='big', signed=False)+int_to_bytes(ID)+int_to_bytes(a)+int_to_bytes(b)+int_to_bytes(Gx)+int_to_bytes(Gy)+int_to_bytes(PA[0])+int_to_bytes(PA[1])
    ZA = int(sm3.sm3_hash(list(data)),16)
    M_=int_to_bytes(ZA)+M
    e=int(sm3.sm3_hash(list(M_)),16)
    r=0
    s=0
    while 1:
        x1,y1=calculate_np(Gx, Gy, k, a, b, p)
        r=(e+x1)%n
        s=(get_inverse(1+dA,n)*(k-r*dA))%n
        if s!=0 and r!=0 and r+k != n :
            break
    return r,s

def getPA():
    return bPA

def verify(msg,r,s,ID,P):
    if not(1<=r and r<=n-1) :
        return False
    if not(1<=s and s<=n-1) :
        return False
    M = msg.encode()
    ENTL = get_bitsize(ID) * 8
    data = ENTL.to_bytes(2, byteorder='big', signed=False) + int_to_bytes(ID) + int_to_bytes(a) + int_to_bytes(b) + int_to_bytes(Gx) + int_to_bytes(Gy) + int_to_bytes(P[0]) + int_to_bytes(P[1])
    ZA = int(sm3.sm3_hash(list(data)), 16)
    M_ = int_to_bytes(ZA) + M
    e = int(sm3.sm3_hash(list(M_)), 16)
    t = (r + s) % n
    if t==0 :
        return False
    SG=calculate_np(Gx, Gy, s, a, b, p)
    tG=calculate_np(P[0], P[1], t, a, b, p)
    xx,yy=calculate_p_q(SG[0],SG[1],tG[0],tG[1],a,b,p)
    R=(e+xx)%n
    if R == r:
        return True

def n_sign(e,dA):
    r=0
    s=0
    while 1:
        x1,y1=calculate_np(Gx, Gy, k, a, b, p)
        r=(e+x1)%n
        s=(get_inverse(1+dA,n)*(k-r*dA))%n
        if s!=0 and r!=0 and r+k != n :
            break
    return r,s

def n_verify(e,r,s,P):
    t = (r + s) % n
    if t == 0:
        return False
    SG = calculate_np(Gx, Gy, s, a, b, p)
    tG = calculate_np(P[0], P[1], t, a, b, p)
    xx, yy = calculate_p_q(SG[0], SG[1], tG[0], tG[1], a, b, p)
    R = (e + xx) % n
    if R == r:
        return True