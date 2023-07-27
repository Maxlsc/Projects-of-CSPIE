from Crypto.Util.number import *
from random import randint
from sympy.ntheory.residue_ntheory import nthroot_mod
from hashlib import sha256
class ECMH:
    def __init__(self,mode) -> None:
        self.p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        self.n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
        self.a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
        self.b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

        self.Sum = None

        self.mode = mode

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
        if self.mode == 1:
            return self.fab(m)
        else:
            return self.TaI(m)

    def TaI(self,m):
        u = sha256(m.encode()).hexdigest()
        for i in range(10):
            x = int(sha256(('0'+hex(i)[2]+u).encode()).hexdigest(),16)
            res = nthroot_mod(x**3+self.a*x+self.b,2,self.p)
            if res != None:
                assert self.is_on_curve((x,res))
                return (x,res)

    def fab(self,m):
        u = int(sha256(m.encode()).hexdigest(),16)
        p = self.p
        a = self.a
        b = self.b
        v = ((3*a - pow(u,4,p))*(inverse(6*u,p)))%p
        x = (nthroot_mod((pow(v,2,p)-b-(pow(u,6,p)*inverse(27,p))+p)%p,3,p)+pow(u,2,p)*inverse(3,p))%p
        y = (u*x+v)%p
        if u == 0:
            return None
        assert(self.is_on_curve((x,y)))
        return (x,y)
            
    def ECMH_add(self,m):
        self.Sum = self.add(self.Sum, self.EChash(m))

    def ECMH_dev(self,m):
        tmp = self.EChash(m)
        P = (tmp[0], -tmp[1])
        self.Sum = self.add(self.Sum, P)


tmp = ECMH(1)
tmp.ECMH_add("123")
print(tmp.Sum)
tmp.ECMH_add("123")
print(tmp.Sum)
tmp.ECMH_dev("123")
print(tmp.Sum)
tmp.ECMH_dev("123")
print(tmp.Sum)