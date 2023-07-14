#pragma once
#ifndef SM4_H
#define SM4_H
#include <stdint.h>
typedef uint32_t* SM4_Key;
int SM4_KeyInit(uint8_t* key, SM4_Key* sm4_key);
void SM4_Encrypt(uint8_t* plaintext, uint8_t* ciphertext, SM4_Key sm4_key);
void SM4_Decrypt(uint8_t* ciphertext, uint8_t* plaintext, SM4_Key sm4_key);
void SM4_KeyDelete(SM4_Key sm4_key);

#endif