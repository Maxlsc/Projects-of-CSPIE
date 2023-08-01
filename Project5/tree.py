import hashlib

class Node:
    def __init__(self):
        self.hash = None
        self.left = 0
        self.right = 0
        self.lson = None
        self.rson = None
        self.fa = None

data = bytearray(800000)

def MT_init(now, left, right):
    now.left = left
    now.right = right
    if left == right:
        tmp = bytearray(9)
        tmp[0] = 0
        for i in range(1, 9):
            tmp[i] = data[8*left+i-1]
        now.hash = hashlib.sha256(tmp).digest()
        return
    now.lson = Node()
    now.rson = Node()
    MT_init(now.lson, left, (left + right) // 2)
    MT_init(now.rson, ((left + right) // 2) + 1, right)
    tmp = bytearray(65)
    tmp[0] = 1
    tmp[1:33] = now.lson.hash
    tmp[33:65] = now.rson.hash
    now.hash = hashlib.sha256(tmp).digest()

def check_byte(p, q, length):
    for i in range(length):
        if p[i] != q[i]:
            return False
    return True

def print_hash(p):
    for b in p:
        print(f'{b:02x}', end=' ')
    print()

def MT_cal(now, tar, data_p, hash_val):
    if now.left == now.right:
        tmp = bytearray(9)
        tmp[0] = 0
        for i in range(1, 9):
            tmp[i] = data_p[i-1]
        hash_val[:] = hashlib.sha256(tmp).digest()
        return
    tmp = bytearray(65)
    if tar <= (now.left + now.right) // 2:
        MT_cal(now.lson, tar, data_p, hash_val)
        tmp[0] = 1
        tmp[1:33] = hash_val
        tmp[33:65] = now.rson.hash
        hash_val[:] = hashlib.sha256(tmp).digest()
    else:
        MT_cal(now.rson, tar, data_p, hash_val)
        tmp[0] = 1
        tmp[1:33] = now.lson.hash
        tmp[33:65] = hash_val
        hash_val[:] = hashlib.sha256(tmp).digest()

def MT_proof(data_p):
    hash_val = bytearray(32)
    for i in range(100000):
        if check_byte(data_p, data[i*8:(i+1)*8], 8):
            MT_cal(root, i, data_p, hash_val)
            print_hash(hash_val)
            print_hash(root.hash)
            return check_byte(root.hash, hash_val, 32)
    return False

def MT_proof_p(data_p, pls):
    hash_val = bytearray(32)
    MT_cal(root, pls, data_p, hash_val)
    print_hash(hash_val)
    print_hash(root.hash)
    return check_byte(root.hash, hash_val, 32)

def MT_del(now):
    if now.left == now.right:
        del now
        return
    MT_del(now.lson)
    MT_del(now.rson)

if __name__ == '__main__':
    root = Node()
    p = memoryview(data)
    for i in range(100000):
        p[i*8:i*8+8] = (i + 1).to_bytes(8, byteorder='little')
    MT_init(root, 0, 100000 - 1)
    p = int.from_bytes(p[4*8:4*8+8], byteorder='little')
    if MT_proof(p.to_bytes(8, byteorder='little')):
        print(f'{p:02x} is in the MT.')
    else:
        print(f'{p:02x} isn\'t in the MT.')

    q = 0
    if MT_proof(q.to_bytes(8, byteorder='little')):
        print(f'{q:02x} is in the MT.')
    else:
        print(f'{q:02x} isn\'t in the MT.')

    if MT_proof_p(p.to_bytes(8, byteorder='little'), 5):
        print(f'{p:02x} is in the MT.')
    else:
        print(f'{p:02x} isn\'t in the MT.')

    if MT_proof_p(p.to_bytes(8, byteorder='little'), 4):
        print(f'{p:02x} is in the MT.')
    else:
        print(f'{p:02x} isn\'t in the MT.')

    MT_del(root)
