/*
SM4的软件实现，目前只有查找表优化，优化到 0.0000017 s
*/
#include <stdio.h>
#include <stdlib.h>
#include<iostream>
#include <sstream>
#include <iomanip>
#include"mytimer.hpp"
#include "SM4.h"
using namespace std;
double time233;
int main() {
    unsigned char key[16] = { 0x02, 0x21, 0x45, 0x47, 0x89, 0xab, 0xcd, 0xef,
                             0xbe, 0xde, 0xba, 0x08, 0x70, 0x58, 0x11, 0xae };
    unsigned char p[16] = { 0x02, 0x21, 0x45, 0x47, 0x89, 0xab, 0xcd, 0xef,
                            0xbe, 0xde, 0xba, 0x08, 0x70, 0x58, 0x11, 0xae };
    SM4_Key sm4_key;
    int notice = SM4_KeyInit(key, &sm4_key);
    if (notice) {
        mytimer _time;
        _time.UpDate();
        SM4_Encrypt(p, p, sm4_key);
        double end1 = _time.GetSecond();
        time233 = double(end1);
        for (int i = 0; i < 16; i++) {
            printf("%02x ", p[i]);
        }
        printf("\n");
        SM4_Decrypt(p, p, sm4_key);
        for (int i = 0; i < 16; i++) {
            printf("%02x ", p[i]);
        }
        printf("\n");
        SM4_KeyDelete(sm4_key);
    }
    cout << endl << endl << "Time for encryption of SM4:  " << fixed << setprecision(7) << time233 << " s" << endl<<endl;
    return 0;
}