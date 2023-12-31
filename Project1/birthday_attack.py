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

def birthday_attack(n):
    dict = {}
    for _ in range(2**(n//2)):
        str = getRandom()
        res = sm3.sm3_hash(func.bytes_to_list(str.encode()))
        # print(res[:n//4])
        # print(dict.values())
        if res[:n//4] not in dict.keys():
            dict[res[:n//4]] = str
        else:
            str0 = dict[res[:n//4]]
            str1 = str
            print(str0 , sm3.sm3_hash(func.bytes_to_list(str0.encode())))
            print(str1 , sm3.sm3_hash(func.bytes_to_list(str1.encode())))
            return 1
    return 0

n = 24

start_time = time.perf_counter()
birthday_attack(n)
end_time = time.perf_counter()
execution_time = (end_time - start_time) * 1000
print("执行时间为：", execution_time, "毫秒")

check = 0
while check == 0:
    check = birthday_attack(n)