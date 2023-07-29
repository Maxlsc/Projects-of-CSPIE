from smt.tree import *
from smt.proof import *
from math import ceil,log
from random import randint
import random
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
        self.seed = [self.KDF(self.seed_m+bytes(i)) for i in range(self.d)]
        for i in range(self.d):
            tmp = [self.seed[i]]
            for j in range(1,self.b):
                tmp.append(sha256(tmp[j-1]).digest())
            self.seed[i] = tmp
    
    def MDP(self,x) -> list:
        d = ceil(log(x+1,self.b))
        res = [x]
        for i in range(1,d):
            bi = self.b**i
            if ((x+1) % (bi)) != 0:
                y = (x//bi)*bi - 1
                res.append(y)
        # print(sorted(list(set(res))))
        return sorted(list(set(res)))
    
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
        random.seed(int(self.seed_m.hex(),16))
        for i in range(n-1,0,-1):
            j = randint(0,i+1)
            arr[i],arr[j] = arr[j],arr[i]
        return arr
    
    def PLA(self,p,r,k):
        z = b''
        if ceil(log(k,self.b)) < self.d:
            z = p
        for i in range(len(r)):
            z = z+r[i]
        return z
    
    def Comm(self,k):
        sigma = self.MDP(k)

        comm = []
        for x in sigma:
            K = self.divide(x)
            if(len(K)<ceil(log(k,self.b))):
                K = [0]*(ceil(log(k,self.b))-len(K))+K
            r = []
            for i in range(len(K)):
                r.append(self.seed[i-len(K)+self.d][K[i]])
            salt = self.KDF(self.seed_m+bytes(x))
            comm.append(sha256(salt+self.PLA(self.p,r,x)).digest())
            # print(sha256(salt+self.PLA(self.p,r,x)).digest(),x)
        
        while len(comm)<self.d:
            comm.append(None)
        comm = self.shuffle(comm)
        tree = SparseMerkleTree()
        dict = {}
        for i in range(len(comm)):
            if comm[i] != None:
                tree.update(bytes(i),comm[i])
                dict[comm[i]] = bytes(i)
        return (tree,dict)
    
    def Prove(self,k,t):
        if k < t:
            return None
        T = self.divide(t)
        sigma = self.MDP(k)
        for x in sigma:
            if x >= t:
                MDP = x
                break
        K = self.divide(MDP)
        if(len(K)<ceil(log(k,self.b))):
            K = [0]*(ceil(log(k,self.b))-len(K))+K
        # print(T,K)
        r = []
        for i in range(len(K)-len(T)):
            r.append(self.seed[i-len(K)+self.d][K[i]])
            # print(i-len(K)+self.d,K[i])
        p = self.PLA(self.p,r,MDP)
        res = []
        for i in range(len(K)-len(T),len(K)):
            res.append(self.seed[i-len(K)+self.d][K[i]-T[i-len(K)+len(T)]])
            # print(i-len(K)+self.d,K[i]-T[i-len(K)+len(T)])
        salt = self.KDF(self.seed_m+bytes(MDP))

        return (p,res,salt)

    def Verify(self,t,proof,dict,root):
        if proof == None:
            return False
        p,r,salt = proof
        T = self.divide(t)
        for i in range(len(T)):
            r[i] = self.Hash(r[i],T[i])
        tmp = sha256(salt+self.PLA(p,r,0.1)).digest()
        # print(tmp)
        pls = dict[tmp]
        proof_t = tree.prove(pls)
        return verify_proof(proof_t, root, pls, tmp)


tmp = HashWire()
tree,dict = tmp.Comm(54)
res = True
for i in range(54):
    proof = tmp.Prove(54,i)
    res = res & tmp.Verify(i,proof,dict,tree.root)

print(res)