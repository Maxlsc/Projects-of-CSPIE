from hashlib import sha256
from Crypto.Util.number import *
from random import randint
class ECDSA:
    def __init__(self) -> None:
        self.p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        self.n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
        self.a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
        self.b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
        self.G = (0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0)

        self.d = randint(1, self.n-1)
        self.P = self.mul(self.d, self.G)

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
    
    def sign(self, m):
        e = int(sha256(m.encode()).hexdigest(),16)
        k = randint(1,self.n-1)
        G = self.G
        R = self.mul(k,G)
        r = R[0] % self.n
        s = inverse(k,self.n)*(e + self.d*r)
        return (r,s)

    def sign_k0(self, m):
        e = int(sha256(m.encode()).hexdigest(),16)
        k = randint(1,self.n-1)
        G = self.G
        R = self.mul(k,G)
        r = R[0] % self.n
        s = inverse(k,self.n)*(e + self.d*r)
        return (r,s,k)
    
    def sign_k1(self, m, k):
        e = int(sha256(m.encode()).hexdigest(),16)
        G = self.G
        R = self.mul(k,G)
        r = R[0] % self.n
        s = inverse(k,self.n)*(e + self.d*r)
        return (r,s)

    def vrfy(self, m, sign, P):
        r,s = sign
        e = int(sha256(m.encode()).hexdigest(),16)
        w = inverse(s,self.n)
        G = self.G
        r1,s1 = self.add(self.mul((e*w) % self.n,G),self.mul((r*w) % self.n,P))
        return r == r1
    
    def vrfy_m(self, e, sign, P):
        r,s = sign
        w = inverse(s,self.n)
        G = self.G
        r1,s1 = self.add(self.mul((e*w) % self.n,G),self.mul((r*w) % self.n,P))
        return r == r1


