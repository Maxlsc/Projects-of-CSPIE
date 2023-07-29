import binascii
from gmssl import sm3
import time

def sm3_hash(message: bytes):
    start_time = time.time()
    hash_hex = sm3.sm3_hash(message)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    print("time：{:.2f} ms".format(elapsed_time))
    print(hash_hex)

def bytes2hex(bytesData):
    hex = binascii.hexlify(bytesData)
    print(hex)
    print(hex.decode())
    return hex

# main
if __name__ == '__main__':
    message = bytearray([ord('a')] * (2 << 10))
    sm3_hash(message)

