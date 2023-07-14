#include <stdio.h>
#include <stdlib.h>
#include<iostream>
#include <sstream>
#include <iomanip>
#include "mytimer.hpp"
using namespace std;
double time233;
#include "sm4_aesni_x4.h"

int main() {
    unsigned char key[16 * 8] = { 0x02, 0x21, 0x45, 0x47, 0x89, 0xab, 0xcd, 0xef,
                             0xbe, 0xde, 0xba, 0x08, 0x70, 0x58, 0x11, 0xae };
    unsigned char in[16 * 8] = { 0x02, 0x21, 0x45, 0x47, 0x89, 0xab, 0xcd, 0xef,
                             0xbe, 0xde, 0xba, 0x08, 0x70, 0x58, 0x11, 0xae };
    SM4_Key sm4_key;
    SM4_KeyInit(key, &sm4_key);
    mytimer _time;
    _time.UpDate();
    SM4_AESNI_Encrypt_x8(in, in, &sm4_key);
    double end1 = _time.GetSecond();
    time233 = double(end1);
    printf("C:\n");
    for (int j = 0; j < 4; j++) {
        printf("\t");
        for (int i = 0; i < 16; i++) {
            printf("%02x ", in[i + 16 * j]);
        }
        printf("\n");
    }

    printf("P:\n");
    SM4_AESNI_Decrypt_x8(in, in, &sm4_key);
    for (int j = 0; j < 4; j++) {
        printf("\t");
        for (int i = 0; i < 16; i++) {
            printf("%02x ", in[i + 16 * j]);
        }
        printf("\n");
    }
    cout << endl << endl << "Time for encryption of SM4 with AES:  " << fixed << setprecision(7) << time233 << " s" << endl << endl;
    system("pause");
    return 0;
}