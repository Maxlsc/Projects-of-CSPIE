from hashlib import sha256
from Cryptodome.Util.number import *
from random import randint


class ECDSA:
    def __init__(self) -> None:
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.a = 0
        self.b = 7
        self.G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
                  0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

        self.d = randint(1, self.n - 1)
        self.P = self.mul(self.d, self.G)

    def is_on_curve(self, P):
        if not P:
            return True
        return ((P[1] ** 2) % self.p == (P[0] ** 3 + self.a * P[0] + self.b) % self.p)

    def add(self, P, Q):
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
            y3 = (lamb * (P[0] - x3) - P[1]) % self.p

        return (x3, y3)

    def double(self, P):
        assert self.is_on_curve(P)
        if not P:
            return P
        lmbd = (3 * (P[0] ** 2) + self.a) * inverse((2 * P[1]) % self.p, self.p) % self.p
        x3 = (lmbd ** 2 - 2 * P[0]) % self.p
        y3 = (lmbd * (P[0] - x3) - P[1]) % self.p
        return (x3, y3)

    def mul(self, k, P):
        assert self.is_on_curve(P)
        flag = 1 << 255
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
        e = int(sha256(m.encode()).hexdigest(), 16)
        k = randint(1, self.n - 1)
        G = self.G
        R = self.mul(k, G)
        r = R[0] % self.n
        s = inverse(k, self.n) * (e + self.d * r)
        return (r, s)

    def sign_k0(self, m):
        e = int(sha256(m.encode()).hexdigest(), 16)
        k = randint(1, self.n - 1)
        G = self.G
        R = self.mul(k, G)
        r = R[0] % self.n
        s = inverse(k, self.n) * (e + self.d * r)
        return (r, s, k)

    def sign_k1(self, m, k):
        e = int(sha256(m.encode()).hexdigest(), 16)
        G = self.G
        R = self.mul(k, G)
        r = R[0] % self.n
        s = inverse(k, self.n) * (e + self.d * r)
        return (r, s)

    def vrfy(self, m, sign, P):
        r, s = sign
        e = int(sha256(m.encode()).hexdigest(), 16)
        w = inverse(s, self.n)
        G = self.G
        r1, s1 = self.add(self.mul((e * w) % self.n, G), self.mul((r * w) % self.n, P))
        return r == r1

    def vrfy_m(self, e, sign, P):
        r, s = sign
        w = inverse(s, self.n)
        G = self.G
        r1, s1 = self.add(self.mul((e * w) % self.n, G), self.mul((r * w) % self.n, P))
        return r == r1