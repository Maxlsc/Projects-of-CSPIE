from smt.tree import *
from smt.proof import *
from math import ceil,log
from random import randint
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from hashlib import sha256
class HashWire:
    def __init__(self,n = 63,b = 4) -> None:
        self.n = n
        self.b = b
        self.d = ceil(log(self.n,self.b))
        self.seed_m = b'seed'
        self.p = sha256(self.seed_m).digest()
    
    def MDP(self,x) -> list:
        d = ceil(log(x+1,self.b))
        res = [x]
        for i in range(1,d):
            bi = self.b**i
            if ((x+1) % (bi)) != 0:
                y = (x//bi)*bi - 1
                res.append(y)
        return list(set(res))[::-1]
    
    def divide(self,x):
        tmp = x
        res = []
        while(tmp != 0):
            res.append(tmp % self.b)
            tmp = tmp // self.b
        return res[::-1]
    
    def KDF(self,salt):
        return scrypt(self.seed_m, salt, 32, N=2**14, r=8, p=1)

    def Hash(self,x,k):
        for _ in range(k):
            x = sha256(x).digest()
        return x
    
    def shuffle(self,arr):
        n = len(arr)-1
        for i in range(n-1,0,-1):
            j = randint(0,i+1)
            arr[i],arr[j] = arr[j],arr[i]
        return arr
    
    def PLA(self,k,r):
        dk = ceil(log(k,self.b))
        K = self.divide(k)
        z = b''
        if dk < self.d:
            z = self.p
        for i in range(dk):
            z = z+self.Hash(r[i],K[i])
        return z
    
    def Comm(self,k):
        sigma = self.MDP(k)
        self.seed = [self.KDF(self.seed_m+bytes(i)) for i in range(self.d)]
        for i in range(self.d):
            tmp = [self.seed[i]]
            for j in range(1,self.b):
                tmp.append(sha256(tmp[j-1]).digest())
            self.seed[i] = tmp

        comm = []
        for x in sigma:
            K = self.divide(x)
            r = []
            for i in range(len(K)):
                r.append(self.seed[i][K[i]])
            salt = self.KDF(self.seed_m+bytes(x))
            comm.append(sha256(salt+self.PLA(x,r)).digest())
        
        while len(comm)<self.d:
            comm.append(None)
        comm = self.shuffle(comm)
        self.tree = SparseMerkleTree()
        for i in range(len(comm)):
            if comm[i] != None:
                self.tree.update(bytes(i),comm[i])
        return self.tree.root
    
    def Prove():
        pass

    def Verify():
        pass

tmp = HashWire()
tmp.Comm(54)