#pragma once
#ifndef SM4_H
#define SM4_H
#include <stdint.h>
typedef struct _SM4_Key {
    uint32_t rk[32];//32ÂÖÃÜÔ¿
} SM4_Key;

void SM4_KeyInit(uint8_t* key, SM4_Key* sm4_key);

#endif // !SM4_H