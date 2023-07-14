#pragma once
// sm4_simd_sbox.h

#ifndef SM4_SIMD_SBOX_H
#define SM4_SIMD_SBOX_H

#include <stdint.h>

/**
 * @brief SM4 ����Կ
 */
typedef uint32_t* SM4_Key;

/**
 * @brief ��ʼ�� SM4 ����Կ
 * @param key 128bit������Կ
 * @param sm4_key SM4 ��Կָ��
 * @return ����ִ�гɹ�����1��ʧ�ܷ���0
 */
int SM4_KeyInit(uint8_t* key, SM4_Key* sm4_key);

/**
 * @brief SM4 ���ܣ�����in��out��Ӧ�ڴ��ص���
 * @param plaintext ����128x8bit��������
 * @param ciphertext ���128x8bit��������
 * @param sm4_key ���ڼ��ܵ� SM4 ��Կ
 */
void SM4_Encrypt_x8(uint8_t* plaintext, uint8_t* ciphertext, SM4_Key sm4_key);

/**
 * @brief SM4 ���ܣ�����in��out��Ӧ�ڴ��ص���
 * @param ciphertext ����128bit��������
 * @param plaintextt ���128bit��������
 * @param sm4_key ���ڼ��ܵ� SM4 ��Կ
 */
void SM4_Decrypt_x8(uint8_t* ciphertext, uint8_t* plaintext, SM4_Key sm4_key);

/**
 * @brief ɾ�� SM4 ����Կ
 * @param sm4_key SM4 ����Կ
 */
void SM4_KeyDelete(SM4_Key sm4_key);

#endif