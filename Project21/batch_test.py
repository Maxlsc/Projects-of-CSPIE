import hashlib
import binascii
import random
import time
#This is just a preliminary and simple implementation
#Further supplementation is needed

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def sign(msg,sk):
    r=random.randint(0,n-1)
    R=EC_mul(G,r)
    e = sha256(R[0].to_bytes(32, byteorder="big") + bytes_point(EC_mul(G, sk)) + msg)
    s=r+e*sk
    return R,s

def verify(msg,pk,R,sig):
    e = sha256(R[0].to_bytes(32, byteorder="big") + bytes_point(pk) + msg)
    s1=EC_add(R,EC_mul(pk,e))
    s2=EC_mul(G,sig)
    if s1==s2:
        return True
    else:
        return False

def EC_add(p1, p2):
    if (p1 is None):
        return p2
    if (p2 is None):
        return p1
    if (p1[0] == p2[0] and p1[1] != p2[1]):
        return None
    if (p1 == p2):
        lam = (3 * p1[0] * p1[0] * pow(2 * p1[1], p - 2, p)) % p
    else:
        lam = ((p2[1] - p1[1]) * pow(p2[0] - p1[0], p - 2, p)) % p
    x3 = (lam * lam - p1[0] - p2[0]) % p
    return (x3, (lam * (p1[0] - x3) - p1[1]) % p)

def EC_mul(p, n):
    r = None
    for i in range(256):
        if ((n >> i) & 1):
            r = EC_add(r, p)
        p = EC_add(p, p)
    return r

def bytes_point(p):
    return (b'\x03' if p[1] & 1 else b'\x02') + p[0].to_bytes(32, byteorder="big")

def sha256(b):
    return int.from_bytes(hashlib.sha256(b).digest(), byteorder="big")

def on_curve(point):
    return (pow(point[1], 2, p) - pow(point[0], 3, p)) % p == 7

def jacobi(x):
    return pow(x, (p - 1) // 2, p)

sk_list=[0x0000000000000000000000000000000000000000000000000000000000000001,
          0x0000000000000000000000000000000000000000000000000000000000000002,
          0x0000000000000000000000000000000000000000000000000000000000000003,
          0x0000000000000000000000000000000000000000000000000000000000000004,
          0x0000000000000000000000000000000000000000000000000000000000000005]

pk_list = [EC_mul(G, sk) for sk in sk_list]

msg_list = [bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000001'),
            bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000002'),
            bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000003'),
            bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000004'),
            bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000005')]

result = [sign(msg, sk) for msg, sk in zip(msg_list, sk_list)]
R_list = [res[0] for res in result]
sig_list = [res[1] for res in result]

t1 = time.time()
for i in range(len(msg_list)):
    print("NO.",i+1,": ",verify(msg_list[i], pk_list[i], R_list[i], sig_list[i]))
print("Normal Verify Time:", time.time() - t1,"s")
print("\n")




def schnorr_batch(msg_list,pk_list,R_list,sig_list):
    sig = sum(sig_list)
    e = [sha256(R[0].to_bytes(32, byteorder="big") + bytes_point(pk) + msg) for R, pk, msg in zip(R_list, pk_list, msg_list)]
    s1 = EC_mul(G, sig)
    tmp1 = None
    for i in range(len(msg_list)):
        tmp1 = EC_add(tmp1, EC_mul(pk_list[i], e[i]))
    tmp2 = None
    for i in range(len(msg_list)):
        tmp2 = EC_add(tmp2, R_list[i])
    s2 = EC_add(tmp1, tmp2)
    if s1 == s2:
        return True
    else:
        return False

t2 = time.time()
print(schnorr_batch(msg_list, pk_list, R_list, sig_list))
print("Batch Verify Time:", time.time() - t2,"s")
