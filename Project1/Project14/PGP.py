from gmssl.sm2 import CryptSM2
from gmssl.sm4 import CryptSM4
from gmssl import sm4,func

import random

def getRandom(randomlength=16):
    upperLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowerLetter = "abcdefghigklmnopqrstuvwxyz"
    digits="0123456789"
    wpecialCharacters = "!@#$%&_-.+="
    str_list =[random.choice(upperLetter+lowerLetter+digits+wpecialCharacters) for _ in range(randomlength)]
    random_str =''.join(str_list)
    return random_str

class PGP:
    def __init__(self):
        self.sm2C = CryptSM2("0","0")
        self.d = random.randint(1,0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123)
        self.publickey = self.sm2C._kg(self.d,'32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7''bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0')
        self.privatekey = hex(self.d)[2:]
        self.sm2C = CryptSM2(self.privatekey,self.publickey)
        # print(self.privatekey,self.publickey)
    
    def enc(self,m,pk):
        key = getRandom().encode()
        print("key = ",key)
        sm4_t = CryptSM4(mode = sm4.SM4_ENCRYPT)
        sm4_t.set_key(key, sm4.SM4_ENCRYPT)
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        c1 = sm4_t.crypt_cbc(iv, m)
        sm2_t = CryptSM2(self.privatekey, pk)
        c2 = sm2_t.encrypt(key)
        return (c1,c2)
    
    def dec(self,c):
        c1, c2 = c
        key = self.sm2C.decrypt(c2)
        sm4_t = CryptSM4(mode = sm4.SM4_DECRYPT)
        sm4_t.set_key(key, sm4.SM4_DECRYPT)
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        m = sm4_t.crypt_cbc(iv,c1)
        return m


tmp = PGP()
m = b'This is a text.'
c = tmp.enc(m,tmp.publickey)
print("message is {}".format(tmp.dec(c)))