from gmssl import sm3, func
from Crypto.Util.number import *
from random import randint
from pysmx import SM3
from math import ceil
import hmac
import binascii
class sm2:
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
        
    def k_gen(self,m):
        h1 = sm3.sm3_hash(func.bytes_to_list(m)).encode()
        V = b'\x01' * 32
        K = b'\x00' * 32
        K = hmac.new(K, V + b'\x00' + self.d.to_bytes(32,"big") + h1,SM3.SM3).digest()
        V = hmac.new(K, V, SM3.SM3).digest()
        K = hmac.new(K, V + b'\x01' + self.d.to_bytes(32,"big") + h1,SM3.SM3).digest()
        V = hmac.new(K, V, SM3.SM3).digest()
        while(1):
            T = b''
            while len(T) < 32:
                V = hmac.new(K, V, SM3.SM3).digest()
                T = T + V
            k = int.from_bytes(T,"big")
            if 0 < k < self.n:
                return k
            K = hmac.new(K, V + b'\x00',SM3.SM3).digest()
            V = hmac.new(K, V, SM3.SM3).digest()


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
    
    def kdf(self, z, klen):
        klen = int(klen)
        ct = 1
        rcnt = ceil(klen/32)
        zin = [i for i in z]
        ha = ""
        for i in range(rcnt):
            msg = zin + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
            ha = ha + sm3.sm3_hash(msg)
            ct += 1
        return ha[0: klen * 2].encode()

    def enc(self,m,P):
        M = m.encode()
        k = randint(1, self.n-1)
        G = self.G      
        S = None
        while S == None:
            k = randint(1, self.n-1)        
            S = self.mul(k, P)
        
        x1,y1 = self.mul(k, G)
        x1 = x1.to_bytes(32, "big")
        y1 = y1.to_bytes(32, "big")
        x2,y2 = S
        x2 = x2.to_bytes(32, "big")
        y2 = y2.to_bytes(32, "big")
        t = self.kdf(x2+y2, len(M))
        C1 = x1 + y1
        C2 = bytes(i^j for i,j in zip(M,t))
        C3 = sm3.sm3_hash(func.bytes_to_list(x2 + M + y2))
        return (C1,C2,C3)

    def dec(self,c):
        C1, C2, C3 = c
        kG = (int.from_bytes(C1[:32],"big"),int.from_bytes(C1[32:],"big"))
        assert self.is_on_curve(kG)
        x2,y2 = self.mul(self.d, kG)
        x2 = x2.to_bytes(32, "big")
        y2 = y2.to_bytes(32, "big")
        t = self.kdf(x2+y2, len(C2))
        M = bytes(i^j for i,j in zip(C2,t))
        u = sm3.sm3_hash(func.bytes_to_list(x2 + M + y2))
        assert u == C3
        return M.decode()
    
    def sign(self, m):
        ZA = sm3.sm3_hash(func.bytes_to_list(b'\x00'+self.a.to_bytes(32,"big")+self.b.to_bytes(32,"big")+self.G[0].to_bytes(32,"big")+self.G[1].to_bytes(32,"big")+self.P[0].to_bytes(32,"big")+self.P[1].to_bytes(32,"big")))
        M = ZA+m
        e = int(sm3.sm3_hash(func.bytes_to_list(M.encode())),16)
        G = self.G
        r = 0
        while r == 0 or r+k == self.n or s == 0:
            k = self.k_gen(M.encode())
            x1,y1 = self.mul(k, G)
            r = (e + x1) % self.n
            s = (inverse(1+self.d, self.n) * (k - r * self.d)) % self.n
        return (r.to_bytes(32,"big"),s.to_bytes(32,"big"))
    
    def vrfy(self, m, sign, P):
        r,s = sign
        r = int.from_bytes(r,"big")
        s = int.from_bytes(s,"big")
        ZA = sm3.sm3_hash(func.bytes_to_list(b'\x00'+self.a.to_bytes(32,"big")+self.b.to_bytes(32,"big")+self.G[0].to_bytes(32,"big")+self.G[1].to_bytes(32,"big")+P[0].to_bytes(32,"big")+P[1].to_bytes(32,"big")))
        M = ZA+m
        e = int(sm3.sm3_hash(func.bytes_to_list(M.encode())),16)
        t = (r + s) % self.n
        assert t != 0
        x1, y1 = self.add(self.mul(s,self.G),self.mul(t,P))
        R = (e + x1) % self.n
        return R == r


tmp = sm2()
c = tmp.enc('123',tmp.P)
print(tmp.dec(c))
sign = tmp.sign("123")
print(tmp.vrfy("123", sign, tmp.P))