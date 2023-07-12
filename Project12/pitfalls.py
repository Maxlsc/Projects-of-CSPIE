from hashlib import sha256
from gmssl import sm3, func
from Crypto.Util.number import *
from random import randint
from ECDSA import ECDSA
from sm2 import sm2

def leaking_k():
    print("Leaking k leads to leaking of d\n")
    tmp = ECDSA()
    r,s,k = tmp.sign_k0("123")
    e = int(sha256("123".encode()).hexdigest(),16)
    print("r = {}, s = {}, k = {}".format(r,s,k))
    d = (inverse(r,tmp.n)*(s*k-e))%tmp.n
    print("d' = {}".format(d))
    print("d  = {}".format(tmp.d))
    print()

def reusing_k():
    print("Reusing k leads to leaking of d\n")
    tmp = ECDSA()
    k = randint(1,tmp.n-1)
    r0,s0 = tmp.sign_k1("1",k)
    e0 = int(sha256("1".encode()).hexdigest(),16)
    r1,s1 = tmp.sign_k1("2",k)
    e1 = int(sha256("2".encode()).hexdigest(),16)
    k0 = ((e0-e1)*inverse(s0-s1,tmp.n)) % tmp.n
    d = (inverse(r0,tmp.n)*(s0*k0-e0))%tmp.n
    print("r0 = {}, s0 = {}, e0 = {}".format(r0,s0,e0))
    print("r1 = {}, s1 = {}, e1 = {}".format(r1,s1,e1))
    print("d' = {}".format(d))
    print("d  = {}".format(tmp.d))
    print()

def reusing_k_dif():
    print("Two users, reusing k leads to leaking of d, that is they can deduce each other’s d\n")
    A = ECDSA()
    B = ECDSA()
    k = randint(1,A.n-1)
    r0,s0 = A.sign_k1("1",k)
    e0 = int(sha256("1".encode()).hexdigest(),16)
    r1,s1 = B.sign_k1("2",k)
    e1 = int(sha256("2".encode()).hexdigest(),16)
    dA = ((((e1 + B.d * r1) * s0) * inverse(s1,A.n) - e0)*inverse(r0,A.n)) % A.n
    dB = ((((e0 + A.d * r0) * s1) * inverse(s0,B.n) - e1)*inverse(r1,B.n)) % B.n
    print("r0 = {}, s0 = {}, e0 = {}".format(r0,s0,e0))
    print("r1 = {}, s1 = {}, e1 = {}".format(r1,s1,e1))
    print("dA' = {}".format(dA))
    print("dA  = {}".format(A.d))
    print("dB' = {}".format(dB))
    print("dB  = {}".format(B.d))
    print()

def symmetry_s():
    print("Malleability, e.g. (r, s) and (r, -s) are both valid signatures, lead to blockchain network split\n")
    tmp = ECDSA()
    r,s = tmp.sign("123")
    print(tmp.vrfy("123",(r,-s),tmp.P))

def noncheck_m():
    print("One can forge signature if the verification does not check m\n")
    tmp = ECDSA()
    P = tmp.P
    G = tmp.G
    a = randint(1,tmp.n-1)
    b = randint(1,tmp.n-1)
    R = tmp.add(tmp.mul(a,G),tmp.mul(b,P))
    r = R[0] % tmp.n
    s = (R[0]*(inverse(b,tmp.n))) % tmp.n
    m = (R[0]*(inverse(b,tmp.n))*a) % tmp.n
    print(tmp.vrfy_m(m,(r,s),P))

def two_kind():
    print("Same d and k with ECDSA, leads to leaking of d\n")
    tmp0 = ECDSA()
    tmp1 = sm2()
    tmp1.d = tmp0.d
    tmp1.P = tmp0.P
    r1,s1,k = tmp1.sign("1")
    e1 = int(sm3.sm3_hash(func.bytes_to_list("1".encode())),16)
    r0,s0 = tmp0.sign_k1("0",k)
    e0 = int(sha256("0".encode()).hexdigest(),16)
    d = ((s0*s1-e0)*inverse(r0-s0*s1-s0*r1,tmp1.n)) % tmp1.n
    print("d' = {}".format(d))
    print("d  = {}".format(tmp0.d))
    

def test():
    leaking_k()
    reusing_k()
    reusing_k_dif()
    symmetry_s()
    noncheck_m()
    two_kind()

test()
