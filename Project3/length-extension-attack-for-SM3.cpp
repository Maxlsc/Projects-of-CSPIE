#include<iostream>
using namespace std;
#pragma warning(disable:4996)

int IV[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };
int IV2[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };
int T[2] = { 0x79cc4519 ,0x7a879d8a };
char* plaintext_after_stuffing;
int length;

int T_j(int j) {
    if (j >= 0 && j <= 15) {
        return T[0];
    }
    else {
        return T[1];
    }
}
int FF(int X, int Y, int Z, int j) {
    if (j >= 0 && j <= 15) {
        return (X ^ Y ^ Z);
    }
    else {
        return ((X & Y) | (X & Z) | (Y & Z));
    }
}
int GG(int X, int Y, int Z, int j) {
    if (j >= 0 && j <= 15) {
        return (X ^ Y ^ Z);
    }
    else {
        return ((X & Y) | ((~X) & Z));
    }
}
int RSL(int X, int Y) {

    return (X << Y) | ((unsigned int)X >> (32 - Y));
}

int P0(int X) {
    return X ^ RSL(X, 9) ^ RSL(X, 17);
}

int P1(int X) {
    return X ^ RSL(X, 15) ^ RSL(X, 23);
}


static void dump_buf(char* ciphertext_32, int lenth)
{
    for (int i = 0; i < lenth; i++) {
        printf("%02X ", (unsigned char)ciphertext_32[i]);
    }
    printf("\n");
}

bool compare(char* ciphertext_32_1, char* ciphertext_32_2, int lenth)
{
    for (int i = 0; i < lenth; i++) {
        if ((unsigned char)ciphertext_32_1[i] != (unsigned char)ciphertext_32_2[i])
            return false;
        return true;
    }
}


int bit_stuffing(char plaintext[], int lenth_for_plaintext) {
    long long bit_len = lenth_for_plaintext * 8;
    int the_num_of_fin_group = (bit_len / 512) * 4 * 16;
    int the_mod_of_fin_froup = bit_len % 512;
    if (the_mod_of_fin_froup < 448) {
        int lenth_for_p_after_stuffing = (lenth_for_plaintext / 64 + 1) * 64;
        plaintext_after_stuffing = new char[lenth_for_p_after_stuffing];
        memcpy(plaintext_after_stuffing, plaintext, lenth_for_plaintext);
        plaintext_after_stuffing[lenth_for_plaintext] = 0x80;
        for (int i = lenth_for_plaintext + 1; i < lenth_for_p_after_stuffing - 8; i++) {
            plaintext_after_stuffing[i] = 0;
        }

        for (int i = lenth_for_p_after_stuffing - 8, j = 0; i < lenth_for_p_after_stuffing; i++, j++) {
            plaintext_after_stuffing[i] = ((char*)&bit_len)[7 - j];
        }
        return lenth_for_p_after_stuffing;
    }
    else if (the_mod_of_fin_froup >= 448) {
        int lenth_for_p_after_stuffing = (lenth_for_plaintext / 64 + 2) * 64;
        plaintext_after_stuffing = new char[lenth_for_p_after_stuffing];
        strcpy(plaintext_after_stuffing, plaintext);
        plaintext_after_stuffing[lenth_for_plaintext] = 0x80;
        for (int i = lenth_for_plaintext + 1; i < lenth_for_p_after_stuffing - 8; i++) {
            plaintext_after_stuffing[i] = 0;
        }

        for (int i = lenth_for_p_after_stuffing - 8, j = 0; i < lenth_for_p_after_stuffing; i++, j++) {
            plaintext_after_stuffing[i] = ((char*)&bit_len)[7 - j];
        }
        return lenth_for_p_after_stuffing;
    }

}

int bit_stuff_for_length_attack(char plaintext[], int lenth_for_plaintext, int length_for_message) {
    long long bit_len = (lenth_for_plaintext + length_for_message) * 8;
    int the_num_of_fin_group = (bit_len / 512) * 4 * 16;
    int the_mod_of_fin_froup = bit_len % 512;
    if (the_mod_of_fin_froup < 448) {
        int lenth_for_p_after_stuffing = (lenth_for_plaintext / 64 + 1) * 64;
        plaintext_after_stuffing = new char[lenth_for_p_after_stuffing];
        memcpy(plaintext_after_stuffing, plaintext, lenth_for_plaintext);
        plaintext_after_stuffing[lenth_for_plaintext] = 0x80;
        for (int i = lenth_for_plaintext + 1; i < lenth_for_p_after_stuffing - 8; i++) {
            plaintext_after_stuffing[i] = 0;
        }

        for (int i = lenth_for_p_after_stuffing - 8, j = 0; i < lenth_for_p_after_stuffing; i++, j++) {
            plaintext_after_stuffing[i] = ((char*)&bit_len)[7 - j];
        }
        return lenth_for_p_after_stuffing;
    }
    else if (the_mod_of_fin_froup >= 448) {
        int lenth_for_p_after_stuffing = (lenth_for_plaintext / 64 + 2) * 64;
        plaintext_after_stuffing = new char[lenth_for_p_after_stuffing];
        strcpy(plaintext_after_stuffing, plaintext);
        plaintext_after_stuffing[lenth_for_plaintext] = 0x80;
        for (int i = lenth_for_plaintext + 1; i < lenth_for_p_after_stuffing - 8; i++) {
            plaintext_after_stuffing[i] = 0;
        }

        for (int i = lenth_for_p_after_stuffing - 8, j = 0; i < lenth_for_p_after_stuffing; i++, j++) {
            plaintext_after_stuffing[i] = ((char*)&bit_len)[7 - j];
        }
        return lenth_for_p_after_stuffing;
    }

}

int MC(int value) {
    return (value & 0x000000FFU) << 24 | (value & 0x0000FF00U) << 8 |
        (value & 0x00FF0000U) >> 8 | (value & 0xFF000000U) >> 24;
}

void CF(int* IV, int* p_a_f) {
    int W[68];
    int W_t[64];
    for (int i = 0; i < 16; i++)
    {
        W[i] = MC(p_a_f[i]);
    }
    for (int i = 16; i < 68; i++)
    {
        W[i] = P1(W[i - 16] ^ W[i - 9] ^ (RSL(W[i - 3], 15))) ^ RSL(W[i - 13], 7) ^ W[i - 6];
    }
    for (int i = 0; i < 64; i++) {
        W_t[i] = W[i] ^ W[i + 4];
    }
    int A = IV[0], B = IV[1], C = IV[2], D = IV[3], E = IV[4], F = IV[5], G = IV[6], H = IV[7];
    for (int i = 0; i < 64; i++) {
        int temp = RSL(A, 12) + E + RSL(T_j(i), i % 32);
        int SS1 = RSL(temp, 7);
        int SS2 = SS1 ^ RSL(A, 12);
        int TT1 = FF(A, B, C, i) + D + SS2 + W_t[i];
        int TT2 = GG(E, F, G, i) + H + SS1 + W[i];
        D = C;
        C = RSL(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = RSL(F, 19);
        F = E;
        E = P0(TT2);


    }
    IV[0] = A ^ IV[0]; IV[1] = B ^ IV[1]; IV[2] = C ^ IV[2]; IV[3] = D ^ IV[3]; IV[4] = E ^ IV[4]; IV[5] = F ^ IV[5]; IV[6] = G ^ IV[6]; IV[7] = H ^ IV[7];
}
void sm3(char plaintext[], int* hash_val, int lenth_for_plaintext) {
    int n = bit_stuffing(plaintext, lenth_for_plaintext) / 64;
    for (int i = 0; i < n; i++) {
        CF(IV, (int*)&plaintext_after_stuffing[i * 64]);
    }
    for (int i = 0; i < 8; i++) {
        hash_val[i] = MC(IV[i]);
    }
    memcpy(IV, IV2, 64);
}


void sm3_for_length_attack(char plaintext[], int* hash_val, int lenth_for_plaintext, int length_for_message) {
    int n = bit_stuff_for_length_attack(plaintext, lenth_for_plaintext, length_for_message) / 64;
    for (int i = 0; i < n; i++) {

        CF(IV, (int*)&plaintext_after_stuffing[i * 64]);
    }
    for (int i = 0; i < 8; i++) {
        hash_val[i] = MC(IV[i]);
    }
    memcpy(IV, IV2, 64);
}

int sm3_length_attack(char* memappend,int* temp, int* hash_val, int length_formemappend, int length_for_message) {
    memcpy(IV, hash_val, 32);
    int new_hash_val[8];
    sm3_for_length_attack(memappend, new_hash_val, length_formemappend, length_for_message);
 
    cout << "The hash obtained by the length extension attack, this part will calculate the hash value before the length extension attack" << endl;
    dump_buf((char*)new_hash_val, 32);
    if (compare((char*)temp, (char*)new_hash_val, 32))
        cout << "The length attack succeeded";
    else
        cout << "lose";
    return 0;
}


int main() {
    char m[] = "best wish for you";
    int hash_val[8];
    int hash_val2[8];
    sm3(m, hash_val, 3);
    dump_buf((char*)hash_val, 32);
    for (int i = 0; i < 8; i++) {
        hash_val2[i] = MC(hash_val[i]);
    }
    bit_stuffing(m, 3);
    char plaintext_for_length_attack[67];
    memcpy(plaintext_for_length_attack, plaintext_after_stuffing, 64);
    char memappend[] = "Thank you";
    memcpy(&plaintext_for_length_attack[64], memappend, 3);
    sm3(plaintext_for_length_attack, hash_val, 67);
    cout << "Manually fill the message and ask for hash, this part directly adds the padding information to the plaintext" << endl;
    dump_buf((char*)hash_val, 32);
    sm3_length_attack(memappend, hash_val,hash_val2, 3, 64);
    return 0;
}