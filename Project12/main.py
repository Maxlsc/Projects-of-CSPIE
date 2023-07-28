import sm2_
from random import randint



IDA=0x414C494345313233405941484F4F2E434F4D
IDB=0x414C4943453132334414C4943453132334
msg="Alice have a love gril"




def leak_k():
    da,PA=sm2_.get_key()
    r,s=sm2_.sign(msg,IDA,da,PA)
    da_=(sm2_.k-s)*sm2_.get_inverse(r+s,sm2_.n)%sm2_.n
   # print('da:',da_)
    r1,s1=sm2_.sign(msg,IDA,da_,PA)
    if sm2_.verify(msg, r1, s1, IDA, PA):
        print('Leaking k leads to leaking of d is ok')
    else:
        print('fault')

def reusing_k():
    m1='I am alice'
    m2='I want to have a grilfriend'
    dA,PA=sm2_.get_key()
    r1, s1 = sm2_.sign(m1, IDA, dA, PA)
    r2, s2 = sm2_.sign(m2, IDA, dA, PA)
    da=(s2-s1)*sm2_.get_inverse(s1-s2+r1-r2,sm2_.n)%sm2_.n
    r,s=sm2_.sign(msg,IDA,da,PA)
    if sm2_.verify(msg,r,s,IDA,PA):
        print('Reusing k leads to leaking of d is ok')
    else:
        print('fault')




def two_user():
    da_a, pA_a = sm2_.get_key()
    A_r, A_s =sm2_.sign(msg, IDA,da_a,pA_a)
    da_b, pA_b = sm2_.get_key()
    B_r, B_s = sm2_.sign(msg, IDB, da_b, pA_b)
    DA=((sm2_.k-A_s)*sm2_.get_inverse(A_r+A_s,sm2_.n))%sm2_.n
    DB=((sm2_.k-B_s)*sm2_.get_inverse(B_r+B_s,sm2_.n))%sm2_.n
    if DA==da_a and DB==da_b:
        print('Two users, using k leads to leaking of k that is they can deduce each other’s d is ok')
    else:
        print('fault')

def noncheck_m():
    da, PA = sm2_.get_key()
    a = randint(1, sm2_.n - 1)
    b = randint(1, sm2_.n - 1)
    r=(b-a)%sm2_.n
    s=a%sm2_.n
    aG=sm2_.calculate_np(sm2_.Gx, sm2_.Gy, a, sm2_.a, sm2_.b, sm2_.p)#aG
    bP=sm2_.calculate_np(PA[0], PA[1], b, sm2_.a, sm2_.b, sm2_.p)  # bP
    xx, yy = sm2_.calculate_p_q(aG[0], aG[1], bP[0], bP[1], sm2_.a, sm2_.b, sm2_.p)
    e=(-xx+b-a)%sm2_.n
    if sm2_.n_verify(e,r,s,PA):
        print('One can forge signature if the verification does not check m is ok')
    else:
        print('fault')

leak_k()
reusing_k()
two_user()
noncheck_m()




