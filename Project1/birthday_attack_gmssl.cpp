#include <iostream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <openssl/sm3.h>
using namespace std;
const int N = 24;    
const int M = N >> 3;
void hash(const unsigned char* msg, size_t m, unsigned char p[SM3_DIGEST_LENGTH]) 
{
	sm3_ctx_t ctx;
	sm3_init(&ctx);
	sm3_update(&ctx, msg, m);
	sm3_final(&ctx, p);
	memset(&ctx, 0, sizeof(sm3_ctx_t));
}

void print_p(const uint8_t str[SM3_DIGEST_LENGTH]) 
{
	for (int i = 0; i < SM3_DIGEST_LENGTH; i++) 
		printf("%02x", str[i]);
	printf("\n");
}

int main(int argc, char** argv) 
{
	unsigned char txr[] = "2021004600XX";
	uint8_t p[SM3_DIGEST_LENGTH];
	hash(txr, sizeof(txr), p);
	printf("hash: ");
	print_p(p);
	uint8_t attack_array[32] = { 0 };
	uint8_t col_p[SM3_DIGEST_LENGTH];
	uint64_t cnt = 0;
	for (int i = 0;pow(2, N/2) ; i++) 
	{
		hash(attack_array, 32, col_p);
		int temp = memcmp(p, col_p, M);
		if (temp == 0) 
		{
			printf("attack: ");
			print_p(col_p);
			break;
		}
		*((uint64_t*)attack_array) += 1;
	}
	return 0;
}
