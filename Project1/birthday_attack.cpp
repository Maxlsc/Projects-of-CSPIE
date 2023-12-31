#pragma comment(lib,"libssl.lib")
#pragma comment(lib,"libcrypto.lib")
#include <iostream>
#include <random>
#include <openssl/evp.h>
#include <unordered_map>


std::string getRandom(int randomlength = 16) {
    std::string upperLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    std::string lowerLetter = "abcdefghigklmnopqrstuvwxyz";
    std::string digits = "0123456789";
    std::string specialCharacters = "!@#$%&_-.+=";

    std::string str;
    std::string charSet = upperLetter + lowerLetter + digits + specialCharacters;
    for (int i = 0; i < randomlength; ++i) {
        str += charSet[rand() % charSet.length()];
    }
    return str;
}

std::string sm3_hash(const std::string& input) {
    EVP_MD_CTX* ctx = EVP_MD_CTX_new();
    const EVP_MD* md = EVP_sm3();

    if (ctx == nullptr || md == nullptr) {
        return "";
    }

    if (EVP_DigestInit_ex(ctx, md, nullptr) != 1) {
        return "";
    }

    if (EVP_DigestUpdate(ctx, input.c_str(), input.length()) != 1) {
        return "";
    }

    unsigned char hash_value[EVP_MAX_MD_SIZE];
    unsigned int hash_len = 0;
    if (EVP_DigestFinal_ex(ctx, hash_value, &hash_len) != 1) {
        return "";
    }

    std::string hex_hash_value;
    for (unsigned int i = 0; i < hash_len; ++i) {
        char hex_byte[3];
        sprintf_s(hex_byte, sizeof(hex_byte), "%02x", hash_value[i]);
        hex_hash_value += hex_byte;
    }

    EVP_MD_CTX_free(ctx);

    return hex_hash_value;
}
int birthday_attack(int n) {
    std::unordered_map<std::string, std::string> dictionary;
    for (int i = 0; i < (1 << (n / 2)); ++i) {
        std::string str = getRandom();
        std::string res = sm3_hash(str);

        if (dictionary.find(res.substr(0, n / 4)) == dictionary.end()) {
            dictionary[res.substr(0, n / 4)] = str;
        }
        else {
            std::string str0 = dictionary[res.substr(0, n / 4)];
            std::string str1 = str;
            std::cout << str0 << " " << sm3_hash(str0) << std::endl;
            std::cout << str1 << " " << sm3_hash(str1) << std::endl;
            return 1;
        }
    }
    return 0;
}

int main() {
    int n = 24;

    clock_t start_time = clock();
    birthday_attack(n);
    clock_t end_time = clock();
    double execution_time = static_cast<double>(end_time - start_time) / CLOCKS_PER_SEC * 1000;
    std::cout << "ִ��ʱ��Ϊ��" << execution_time << " ����" << std::endl;

    int check = 0;
    while (check == 0) {
        check = birthday_attack(n);
    }

    return 0;
}