#include <cstdio>
#include <cstring>
#include <stdlib.h>
#include "sha2.h"

struct node{
    uint8_t hash[32];
    uint32_t left, right;
    node *lson,*rson,*fa;
}*root;

uint8_t data[800000];

void MT_init(node* now, uint32_t left, uint32_t right){
    // printf("%u, %u\n",left,right);
    now->left = left, now->right = right;
    if(left==right){
        uint8_t tmp[9];
        tmp[0] = 0;
        for(int i = 1; i < 9; i++) tmp[i] = data[8*left+i-1];
        sha256(now->hash, tmp, 9);
        return ;
    }
    now->lson = (node*)malloc(sizeof(node));
    now->rson = (node*)malloc(sizeof(node));
    MT_init(now->lson, left, (left + right) / 2);
    MT_init(now->rson, ((left + right)/2) + 1, right);
    uint8_t tmp[65];
    tmp[0] = 1;
    memcpy((tmp+1), (now->lson->hash), 32);
    // for(int i = 0; i < 32; i++) tmp[i+1] = now->lson->hash[i];
    memcpy((tmp+33), (now->rson->hash), 32);
    sha256(now->hash, tmp, 65);
    return ;
}

bool check_byte(uint8_t* p, uint8_t* q, uint32_t len){
    for(int i = 0; i < len; i++){
        if(p[i]!=q[i]) return 0;
    }
    return 1;
}

void print(uint8_t* p){
    for(int i = 0; i < 32; i++){
        printf("%02x ",p[i]);
    }
    printf("\n");
}

void MT_cal(node* now, uint32_t tar, uint8_t* data_p, uint8_t* hash){
    if(now->left == now->right){
        uint8_t tmp[9];
        tmp[0] = 0;
        for(int i = 1; i < 9; i++) tmp[i] = data_p[i-1];
        sha256(hash, tmp, 9);
        // printf("%d\n",now->left);
        // print(hash);
        // print(now->hash);
        return ;
    }
    uint8_t tmp[65];
    if(tar <= (now->left + now->right)/2){
        MT_cal(now->lson, tar, data_p, hash);
        tmp[0] = 1;
        memcpy(tmp+1, hash, 32);
        memcpy(tmp+33, now->rson->hash, 32);
        sha256(hash, tmp, 65);
    }else{ 
        MT_cal(now->rson, tar, data_p, hash);
        tmp[0] = 1;
        memcpy(tmp+1, now->lson->hash, 32);
        memcpy(tmp+33, hash, 32);
        sha256(hash, tmp, 65);
    }
    return ;
}

bool MT_proof(uint8_t* data_p){
    uint8_t hash[32];
    for(int i = 0; i < 100000; i++){
        if(check_byte(data_p,data+i*8,8)){
            // printf("%d\n",i);
            MT_cal(root, i, data_p, hash);
            print(hash);
            print(root->hash);
            return check_byte(root->hash, hash, 32);
        }
    }
    return 0;
}

void MT_del(node* now){
    if(now->left == now->right){
        free(now);
        return ;
    }
    uint8_t tmp[65];
    MT_del(now->lson);
    MT_del(now->rson);
    return ;
}

int main(){
    root = (node*)malloc(sizeof(node));
    uint64_t* p;
    for(int i = 0; i < 100000; i++){
        p = (uint64_t*) (data+i*8);
        *p = (i + 1);
    }
    MT_init(root, 0, 100000 - 1);
    p = (uint64_t*) (data+4*8);
    if(MT_proof(data+4*8)) printf("%02x is in the MT.\n",*p);
    else printf("%02x isn't in the MT.\n",*p);
    // for(int i = 0; i < 100000; i++){
    //     p = (uint64_t*) (data+i*8);
    //     if(!MT_proof(data+i*8)) printf("%02x isn't in the MT.\n",*p);
    // }
    uint64_t q = 0;
    if(MT_proof((uint8_t*)&q)) printf("%02x is in the MT.\n",q);
    else printf("%02x isn't in the MT.\n",q);
    MT_del(root);
}