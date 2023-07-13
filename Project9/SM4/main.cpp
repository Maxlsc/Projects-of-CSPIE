/*
SM4的软件实现，目前只有查找表优化，优化到 0.0000017 s
*/
#include <stdio.h>
#include <stdlib.h>
#include<iostream>
#include <sstream>
#include <iomanip>
#include"mytimer.hpp"
#include "sm4.h"
using namespace std;
double time233;
int main() {
    // 01 23 45 67 89 ab cd ef fe dc ba 98 76 54 32 10
    unsigned char key[16] = { 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
                             0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10 };
    // 01 23 45 67 89 ab cd ef fe dc ba 98 76 54 32 10
    unsigned char in[16] = { 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
                            0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10 };
    SM4_Key sm4_key;
    int success = SM4_KeyInit(key, &sm4_key);
    if (success) {
        mytimer _time;
        _time.UpDate();
        SM4_Encrypt(in, in, sm4_key);
        double end1 = _time.GetSecond();
        time233 = float(end1);
        // 68 1e df 34 d2 06 96 5e 86 b3 e9 4f 53 6e 42 46
        for (int i = 0; i < 16; i++) {
            printf("%02x ", in[i]);
        }
        printf("\n");
        SM4_Decrypt(in, in, sm4_key);
        // 01 23 45 67 89 ab cd ef fe dc ba 98 76 54 32 10
        for (int i = 0; i < 16; i++) {
            printf("%02x ", in[i]);
        }
        printf("\n");
        SM4_KeyDelete(sm4_key);
    }
    cout << endl << endl << "Time for encryption of SM4:  " << fixed << setprecision(7) << time233 << " s" << endl<<endl;
    system("pause");
    return 0;
}