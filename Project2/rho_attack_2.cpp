#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <ratio>
#include <chrono>
#include <time.h>
#include <iostream>
#include <unordered_map>
#include <string>
#include <algorithm>
using namespace std;

#define FF0(x,y,z) x^y^z
#define FF1(x,y,z) (x&y)|(x&z)|(y&z)

#define GG0(x,y,z) x^y^z
#define GG1(x,y,z) (x&y)|((~x)&z)

static uint32_t rot(uint32_t a, uint8_t n)
{
    return (a << n) | (a >> (32 - n));
}

#define P0(x) x^rot(x,9)^rot(x,17)
#define P1(x) x^rot(x,15)^rot(x,23)

static const uint32_t IV[8] =
{
    0x7380166F,    0x4914B2B9,
    0x172442D7,    0xDA8A0600,
    0xA96F30BC,    0x163138AA,
    0xE38DEE4D,    0xB0FB0E4E,
};

static uint32_t T[64];

static void T_init(){
    for(int i = 0; i < 64; i++){
        if(i < 16) T[i] = 0x79cc4519;
        else       T[i] = 0x7a879d8a;
    }
}

static void CF(uint8_t* B,uint32_t* V){
    uint32_t w0[68],w[64];
    for(int i = 0; i < 16; i++){
        w0[i] =  ((uint32_t)B[i * 4 + 0] << 24) & 0xFF000000
                |((uint32_t)B[i * 4 + 1] << 16) & 0x00FF0000
                |((uint32_t)B[i * 4 + 2] << 8 ) & 0x0000FF00
                |((uint32_t)B[i * 4 + 3] << 0 ) & 0x000000FF;
    }
    for(int i = 16; i < 68; i++) w0[i] = P1(w0[i-16]^w0[i-9]^rot(w0[i-3],15))^rot(w0[i-13],7)^w0[i-6];
    for(int i = 0; i < 64; i++) w[i] = w0[i] ^ w0[i+4];

    uint32_t V0[8];
    for(int i = 0; i < 8; i++) V0[i] = V[i];
    uint32_t ss1 = 0,ss2 = 0,tt1 = 0,tt2 = 0;
    for(int i = 0; i < 64; i++){
        ss1 = rot(rot(V0[0],12)+V0[4]+rot(T[i],(i%32)),7);
        ss2 = ss1^rot(V0[0],12);
        tt1 = V0[3]+ss2+w[i] + (i<16 ? FF0(V0[0],V0[1],V0[2]) : FF1(V0[0],V0[1],V0[2]));
        tt2 = V0[7]+ss1+w0[i]+ (i<16 ? GG0(V0[4],V0[5],V0[6]) : GG1(V0[4],V0[5],V0[6]));
        V0[3] = V0[2];
        V0[2] = rot(V0[1],9);
        V0[1] = V0[0];
        V0[0] = tt1;
        V0[7] = V0[6];
        V0[6] = rot(V0[5],19);
        V0[5] = V0[4];
        V0[4] = P0(tt2);
    }
    for(int i = 0; i < 8; i++) V[i] = V0[i] ^ V[i];
}

static void print(uint8_t *p,int len){
    for(int i = 0; i < len; i++){
        printf("%02x",p[i]);
    }
    printf("\n");
}

void sm3_hash(uint8_t* data, uint32_t data_len, uint8_t* res){

    T_init();

    uint32_t round = (data_len+ 1 + 8 + 64)/64;
    uint8_t* msg = (uint8_t*)malloc(round * 64);
    memset(msg, 0, round*64);
    memcpy(msg, data, data_len);
    msg[data_len] = 0x80;

    for(int i = 0; i < 8; i++){
        msg[round * 64 - i - 1] = ((uint64_t)(data_len<<3)>>(i<<3)) &0xff;
    }
    uint32_t V[8];
    for(int i = 0; i < 8; i++){
        V[i] = IV[i];
    }
    for(int i = 0; i < round; i++){
        CF(&msg[i*64], V);
    }
    free(msg);
    for (int i = 0; i < 8; i++){
        res[i * 4 + 0] = (uint32_t)((V[i] >> 24) & 0xFF);
        res[i * 4 + 1] = (uint32_t)((V[i] >> 16) & 0xFF);
        res[i * 4 + 2] = (uint32_t)((V[i] >>  8) & 0xFF);
        res[i * 4 + 3] = (uint32_t)((V[i] >>  0) & 0xFF);
    }
}

void get_random(uint8_t* s, int n){
    for(int i = 0; i < n; i++){
        s[i] = rand() % 256;
    }
    return ;
}
const char tab[16] = {'1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
unordered_map<string,string> dict;
void rho_attack(int n){

    auto begin = std::chrono::high_resolution_clock::now();
    srand(time(NULL));
    uint8_t s[32],tmp[32];
    uint8_t hash[32];
    // int len = n/2;
    int len = 32;
    get_random(s,len);
    while(1){
        string h,s0;
        sm3_hash(s,len,hash);
        for(int i = 0; i < len; i++) s0 += s[i];
        // s0[32] = 0;
        int m = (n/2);
        for(int i = 0; i < m ; i++){
            h += tab[(hash[i]>>4)&(0xf)];
            h += tab[(hash[i]>>0)&(0xf)];
        }
        if(n%2) h += tab[(hash[m]>>4)&(0xf)];
        // h[n] = 0;

        if(dict.count(h) == 0) dict[h] = s0;
        else{
            if(dict[h] == s0){
                srand(time(NULL));
                continue;
            }
            print(s, len);
            for(int i = 0; i < len; i++) tmp[i] = (uint8_t)dict[h][i];
            print(tmp,len);
            printf("\n");
            print(hash,32);
            sm3_hash(tmp,len,hash);
            print(hash,32);
            break;
        }
        for(int i = 0; i < len; i++) s[i] = hash[i];
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::ratio<1, 1000>> diff = end - begin;
    std::cout << diff.count() << "ms";
    return;
}

int main(){    
    int n = 12;
    rho_attack(n);
    return 0;
}