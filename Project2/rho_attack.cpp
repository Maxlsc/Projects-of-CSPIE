#pragma comment(lib,"libssl.lib")
#pragma comment(lib,"libcrypto.lib")
#include <iostream>
#include <string>
#include <random>
#include <ctime>
#include "openssl/evp.h"
#include <openssl/objects.h>

std::string getRandom(int randomLength = 16) {
    std::string upperLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    std::string lowerLetter = "abcdefghigklmnopqrstuvwxyz";
    std::string digits = "0123456789";
    std::string specialCharacters = "!@#$%&_-.+=";
    std::string str;
    std::string characters = upperLetter + lowerLetter + digits + specialCharacters;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, characters.size() - 1);

    for (int i = 0; i < randomLength; i++) {
        str += characters[dis(gen)];
    }

    return str;
}

std::string sm3_hash(const std::string& input) {
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();
    const EVP_MD* md = EVP_sm3();

    if (!ctx || !md) {
        return "";
    }

    if (EVP_DigestInit_ex(ctx, md, nullptr) != 1) {
        EVP_MD_CTX_free(ctx);
        return "";
    }

    if (EVP_DigestUpdate(ctx, input.c_str(), input.length()) != 1) {
        EVP_MD_CTX_free(ctx);
        return "";
    }

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int hashLength;

    if (EVP_DigestFinal_ex(ctx, hash, &hashLength) != 1) {
        EVP_MD_CTX_free(ctx);
        return "";
    }

    EVP_MD_CTX_free(ctx);

    std::vector<char> hexHash(hashLength * 2 + 1);
    const char hexDigits[] = "0123456789ABCDEF";

    for (unsigned int i = 0; i < hashLength; i++) {
        hexHash[i * 2] = hexDigits[(hash[i] & 0xF0) >> 4];
        hexHash[i * 2 + 1] = hexDigits[hash[i] & 0x0F];
    }

    hexHash[hashLength * 2] = '\0';

    return hexHash.data();
}

bool rho_attack(int n) {
    std::string str = getRandom();
    std::string f0 = sm3_hash(str);
    std::string f1 = f0;

    while (true) {
        std::string f0_t = sm3_hash(f0);
        f1 = sm3_hash(f1);
        std::string f1_t = sm3_hash(f1);

        if (f0_t.substr(0, n / 4) == f1_t.substr(0, n / 4)) {
            std::cout << f0 << " " << f0_t << std::endl;
            std::cout << f1 << " " << f1_t << std::endl;
            return true;
        }

        f0 = f0_t;
        f1 = f1_t;
    }
}

int main() {
    int n = 12;

    clock_t startTime = clock();
    rho_attack(n);
    clock_t endTime = clock();
    double executionTime = (endTime - startTime) * 1000.0 / CLOCKS_PER_SEC;
    std::cout << "执行时间为：" << executionTime << "毫秒" << std::endl;

    return 0;
}