import random
import time
from gmssl import sm3, func

def padding(msg):
    msg.append(0x80)
    len0 = len(msg)
    msg = msg+[0]*(56-len0)

    bit_length = (len0 - 1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])
    return msg

def get_iv(str):
    print(str)
    res = []
    for i in range(8):
        res.append(int(str[i*8:i*8+8],16))
        # print(str[i*8:i*8+8])
    return res

def sm3_hash_0(len0,msg):
    # print(msg)
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1 + len0) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])

    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i*64:(i+1)*64])

    V = []
    V.append(IV)
    for i in range(0, group_count):
        V.append(sm3.sm3_cf(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result

str1 = 'secret'
str2 = 'padding'
msg1 = func.bytes_to_list(str1.encode())
msg2 = func.bytes_to_list(str2.encode())

IV = get_iv(sm3.sm3_hash(msg1))

msg3 = msg1+msg2

print(sm3_hash_0(len(msg1),msg2))
print(sm3.sm3_hash(msg3))