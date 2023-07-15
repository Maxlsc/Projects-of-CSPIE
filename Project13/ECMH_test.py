from Crypto.Util.number import *
from random import randint
from sympy.ntheory.residue_ntheory import nthroot_mod
from hashlib import sha256
class ECMH:
    def __init__(self) -> None:
        self.p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        self.n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
        self.a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
        self.b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
        self.G = (0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0)

        self.d = randint(1, self.n-1)
        self.P = self.mul(self.d, self.G)

        self.Sum = None

    def is_on_curve(self,P):
        if not P:
            return True
        return ((P[1] ** 2) % self.p == (P[0] ** 3 + self.a * P[0] + self.b) % self.p)


    def add(self,P,Q):
        assert self.is_on_curve(P) and self.is_on_curve(Q)
        if not P:
            return Q
        if not Q:
            return P
        if P[0] == Q[0]:
            if P[1] != Q[1]:
                return None
            else:
                return self.double(P)
        else:
            lamb = (Q[1] - P[1]) * inverse((Q[0] - P[0]) % self.p, self.p) % self.p

            x3 = (lamb ** 2 - P[0] - Q[0]) % self.p
            y3 = (lamb * (P[0] - x3) - P[1]) %self.p

        return (x3,y3)

    def double(self,P):
        assert self.is_on_curve(P)
        if not P:
            return P
        lmbd = (3 * (P[0] ** 2) + self.a) * inverse((2 * P[1]) % self.p, self.p) % self.p
        x3 = (lmbd ** 2 - 2 * P[0]) % self.p
        y3 = (lmbd * (P[0] - x3) - P[1]) % self.p
        return (x3,y3)
    
    def mul(self,k,P):
        assert self.is_on_curve(P)
        flag = 1<<255
        acc = None
        for _ in range(255):
            if 0 != k & flag:
                acc = self.add(acc, P)
            acc = self.double(acc)
            flag >>= 1
        if 0 != k & flag:
            acc = self.add(acc, P)
        return acc
    
    def EChash(self,m):
        u = sha256(m.encode()).hexdigest()
        for i in range(10):
            x = int(sha256(('0'+hex(i)[2]+u).encode()).hexdigest(),16)
            res = nthroot_mod(x**3+self.a*x+self.b,2,self.p)
            if res != None:
                assert self.is_on_curve((x,res))
                return (x,res)
            
    def ECMH_add(self,m):
        self.Sum = self.add(self.Sum, self.EChash(m))

    def ECMH_dev(self,m):
        tmp = self.EChash(m)
        P = (tmp[0], -tmp[1])
        self.Sum = self.add(self.Sum, P)


tmp = ECMH()
tmp.ECMH_add("123")
print(tmp.Sum)
tmp.ECMH_add("123")
print(tmp.Sum)
tmp.ECMH_dev("123")
print(tmp.Sum)
tmp.ECMH_dev("123")
print(tmp.Sum)