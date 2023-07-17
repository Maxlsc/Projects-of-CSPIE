
from Cryptodome.Util.number import *
from random import randint
from ECDSA import ECDSA




def noncheck_m():
    print("One can forge signature of satochi,\n")
    tmp = ECDSA()
    P = tmp.P   #because of the pseudonymous of the blockchain,we can't get satoshi's public key,so we assume that this is Satoshi's public key
    G = tmp.G
    a = randint(1, tmp.n - 1)
    b = randint(1, tmp.n - 1)
    R = tmp.add(tmp.mul(a, G), tmp.mul(b, P))
    r = R[0] % tmp.n
    s = (R[0] * (inverse(b, tmp.n))) % tmp.n
    m = (R[0] * (inverse(b, tmp.n)) * a) % tmp.n
    print(tmp.vrfy_m(m, (r, s), P))




noncheck_m()

