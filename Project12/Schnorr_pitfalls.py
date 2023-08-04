from Schnorr import *
from gmssl import sm3, func
import secrets


def Schnorr_sign_and_assign_k(k, M, sk):
    R = EC_multi(k, G)
    tmp = str(R[0]) + str(R[1]) + M
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    s = k + e * sk % N
    return (R, s)


def ECDSA_sign_and_assign_k(k, m, sk):
    R = EC_multi(k, G)
    r = R[0] % N  # Rx mod n
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8'))) 
    e = int(e, 16)
    tmp1 = inv(k, N)
    tmp2 = (e + sk * r) % N
    s = tmp1 * tmp2 % N
    return (r, s)

def Schnorr_leaking_k():
    sk, pk = key_gen()
    msg_a = "testmessage"
    k = secrets.randbelow(N) 
    signature = Schnorr_sign_and_assign_k(k, msg_a, sk)
    R, s = signature
    tmp = str(R[0]) + str(R[1]) + msg_a
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    d = (s - k % N) * inv(e, N) % N
    msg_f = "message of B"
    Sign_f = Schnorr_sign(msg_f, d)
    if Schnorr_verify(Sign_f, msg_f, pk) == 1:
        print("forge successfully")
    else:
        print("forge unsuccessfully")

def Schnorr_reusing_k():
    sk, pk = key_gen()
    msg1 = "sdu"
    msg2 = "testmessage"
    k = secrets.randbelow(N) 
    signature1 = Schnorr_sign_and_assign_k(k, msg1, sk)
    signature2 = Schnorr_sign_and_assign_k(k, msg2, sk)
    R1, s1 = signature1
    R2, s2 = signature2
    if R1 != R2: return 'error'
    R = R1
    tmp = str(R[0]) + str(R[1]) + msg1
    e1 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    tmp = str(R[0]) + str(R[1]) + msg2
    e2 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    d = ((s1 - s2) % N) * inv((e1 - e2), N) % N
    msg_f = "2635410120"
    Sign_f = Schnorr_sign(msg_f, d)
    if Schnorr_verify(Sign_f, msg_f, pk) == 1:
        print("forge successfully")
    else:
        print("forge unsuccessfully")
def same_k_of_different_users():
    k = secrets.randbelow(N) 
    sk_a1, pk_a1 = key_gen()
    msg_a1 = "I'm A1"
    Sign1 = Schnorr_sign_and_assign_k(k, msg_a1, sk_a1)
    r1, s1 = Sign1
    tmp = str(r1[0]) + str(r1[1]) + msg_a1
    e1 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    d1 = (s1 - k % N) * inv(e1, N) % N
    
    sk_a2, pk_a2 = key_gen()
    msg_a2 = "I'm A2"
    Sign2 = Schnorr_sign_and_assign_k(k, msg_a2, sk_a2)
    
    r2, s2 = Sign2
    tmp = str(r2[0]) + str(r2[1]) + msg_a2
    e2 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    d2 = (s2 - k % N) * inv(e2, N) % N
    if d2 == sk_a2:
        print(" get sk")
    else:
        print("not get sk")

def verify_Malleability():
    sk, pk = key_gen()
    message = "message"
    signature = Schnorr_sign(message, sk)
    r, s = signature
    signature_test = (r, -s)
    if Schnorr_verify(signature_test, message, pk) == 1:
        print("success")
    else:
        print("false")


def same_k_ECDSA():
    sk, pk = key_gen()
    k = secrets.randbelow(N)
    message1 = "ECSDA"
    signature1 = ECDSA_sign_and_assign_k(k, message1, sk)
    message2 = "Schnorr"
    signature2 = Schnorr_sign_and_assign_k(k, message2, sk)
    r, s1 = signature1
    R, s2 = signature2
    e1 = int(sm3.sm3_hash(func.bytes_to_list(bytes(message1, encoding='utf-8'))), 16)
    tmp = str(R[0]) + str(R[1]) + message2
    e2 = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    tmp1 = (s2 - inv(s1, N) * e1) % N
    tmp2 = (inv(s1, N) * r + e2) % N
    d = tmp1 * inv(tmp2, N) % N
    if d == sk:
        print("get sk")
    else:
        print("not get sk")


if __name__ == '__main__':
    print("leaking k：")
    Schnorr_leaking_k()
    
    print("reusing k：")
    Schnorr_reusing_k()
    
    print("两个用户重用k：")
    same_k_of_different_users()
    
    print("验证(r,s) and (r,-s)均为合法签名：")
    verify_Malleability()
    
    print("ECDSA与Schnorr使用相同的d和k导致d泄露：")
    same_k_ECDSA()
