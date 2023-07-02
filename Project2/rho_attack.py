import random
import time
from gmssl import sm3, func

def getRandom(randomlength=16):
    upperLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowerLetter = "abcdefghigklmnopqrstuvwxyz"
    digits="0123456789"
    wpecialCharacters = "!@#$%&_-.+="
    str_list =[random.choice(upperLetter+lowerLetter+digits+wpecialCharacters) for _ in range(randomlength)]
    random_str =''.join(str_list)
    return random_str

def rho_attack(n):
    str = sm3.sm3_hash(func.bytes_to_list(getRandom().encode()))
    f0 = sm3.sm3_hash(func.bytes_to_list(str.encode()))
    f1 = f0
    while(1):
        # print(f0,f1)
        f0_t = sm3.sm3_hash(func.bytes_to_list(f0.encode()))
        f1 = sm3.sm3_hash(func.bytes_to_list(f1.encode()))
        f1_t = sm3.sm3_hash(func.bytes_to_list(f1.encode()))
        if f0_t[:n//4]==f1_t[:n//4]:
            print(f0,f0_t)
            print(f1,f1_t)
            return 1
        f0 = f0_t
        f1 = f1_t

n = 12

start_time = time.perf_counter()
rho_attack(n)
end_time = time.perf_counter()
execution_time = (end_time - start_time) * 1000
print("执行时间为：", execution_time, "毫秒")