from Crypto.Util.number import *
from gmssl.sm2 import CryptSM2

g = '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7''bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0'
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
d1 = 0x94b8a9d27b8821945c0ff89bef829a357dec0b70de8377cec7c70bd294887cb4 
d2 = 0x383c53f785cd1e45da3c07f8473527581a2ee50a5974943691868e73694a4f61

print(hex(d1))
print(hex(d2))

sm2C = CryptSM2("0","0")
d = (inverse((d1*d2)%n, n)-1) %n
publickey = sm2C._kg(d,g)
privatekey = hex(d)[2:]
sm2C = CryptSM2(privatekey,publickey)

m = b'This is a text.'
c = sm2C.encrypt(m)
m1 = sm2C.decrypt(c)
print(c)
