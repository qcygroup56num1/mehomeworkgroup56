#include<iostream>
#include<bitset>
#include<sstream>
#include<fstream>

using namespace std;
#pragma warning(disable:4996)

int T[2] = { 0x79cc4519 ,0x7a879d8a };
#define NUM  4294967296;
//准备工作
int tt(int j) {
    if (j >= 0 && j <= 15) {
        return T[0];
    }
    else {
        return T[1];
    }
}
int ff(int X, int Y, int Z, int j) {
    if (j >= 0 && j <= 15) {
        return (X ^ Y ^ Z);
    }
    else {
        return ((X & Y) | (X & Z) | (Y & Z));
    }
}
int gg(int X, int Y, int Z, int j) {
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


//输出结果
static void dump_buffer(char* ciphertext_32, int lenth)
{
    for (int i = 0; i < lenth; i++) {
        printf("%02X ", (unsigned char)ciphertext_32[i]);
    }
    printf("\n");
}

char* plaintext_after_stuffing;
int length;
int IV[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };
int IV2[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };

int bit_stuffing(char plaintext[], int lenth_for_plaintext) {
    //int lenth_for_plaintext = strlen(plaintext);
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
        // dump_buf(plaintext_after_stuffing, lenth_for_p_after_stuffing);
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
    //int lenth_for_plaintext = strlen(plaintext);
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
        //dump_buf(plaintext_after_stuffing, lenth_for_p_after_stuffing);
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

int reversebytes_uint32t(int value) {
    return (value & 0x000000FFU) << 24 | (value & 0x0000FF00U) << 8 |
        (value & 0x00FF0000U) >> 8 | (value & 0xFF000000U) >> 24;
}

void CF(int* V, int* BB) {
    int W[68];
    int W_t[64];
    for (int i = 0; i < 16; i++)
    {
        W[i] = reversebytes_uint32t(BB[i]);
    }
    for (int i = 16; i < 68; i++)
    {
        W[i] = P1(W[i - 16] ^ W[i - 9] ^ (RSL(W[i - 3], 15))) ^ RSL(W[i - 13], 7) ^ W[i - 6];
    }
    for (int i = 0; i < 64; i++) {
        W_t[i] = W[i] ^ W[i + 4];
        // cout << hex << W_t[i] << endl;
    }
    int A = V[0], B = V[1], C = V[2], D = V[3], E = V[4], F = V[5], G = V[6], H = V[7];
    //cout << "        A         B         C         D         E         F        G         H " << endl;
   // cout <<dec<<0<< " " << hex << A << "  " << B << "  " << C << "  " << D << "  " << E << "  " << F << "  " << G << "  " << H << endl;
    for (int i = 0; i < 64; i++) {
        int temp = RSL(A, 12) + E + RSL(tt(i), i % 32);
        int SS1 = RSL(temp, 7);
        int SS2 = SS1 ^ RSL(A, 12);
        int TT1 = ff(A, B, C, i) + D + SS2 + W_t[i];
        int TT2 = gg(E, F, G, i) + H + SS1 + W[i];
        D = C;
        C = RSL(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = RSL(F, 19);
        F = E;
        E = P0(TT2);
        // cout <<dec << i <<" " << hex << A << "  " << B << "  " << C << "  " << D << "  " << E << "  " << F << "  " << G << "  " << H << endl;

    }
    V[0] = A ^ V[0]; V[1] = B ^ V[1]; V[2] = C ^ V[2]; V[3] = D ^ V[3]; V[4] = E ^ V[4]; V[5] = F ^ V[5]; V[6] = G ^ V[6]; V[7] = H ^ V[7];

}
void sm3(char plaintext[], int* hash_val, int lenth_for_plaintext) {
    int n = bit_stuffing(plaintext, lenth_for_plaintext) / 64;
    for (int i = 0; i < n; i++) {
        CF(IV, (int*)&plaintext_after_stuffing[i * 64]);
    }
    for (int i = 0; i < 8; i++) {
        hash_val[i] = reversebytes_uint32t(IV[i]);
    }
    memcpy(IV, IV2, 64);
}


void sm3forattack(char plaintext[], int* hash_val, int lenth_for_plaintext, int length_for_message) {
    int n = bit_stuff_for_length_attack(plaintext, lenth_for_plaintext, length_for_message) / 64;
    for (int i = 0; i < n; i++) {
        CF(IV, (int*)&plaintext_after_stuffing[i * 64]);
    }

    for (int i = 0; i < 8; i++) {
        hash_val[i] = reversebytes_uint32t(IV[i]);
    }
    memcpy(IV, IV2, 64);
}

int sm3_length_attack(char* memappend, int* hash_val, int length_formemappend, int length_for_message) {
    int new_hash_val[8];
    memcpy(IV, hash_val, 32);
    sm3forattack(memappend, new_hash_val, length_formemappend, length_for_message);
    cout << "长度扩展攻击得到的哈希值" << endl;
    dump_buffer((char*)new_hash_val, 32);
    return 0;
}

int sm3_lea(int hash_val[], int lenth) {
    memcpy(IV, hash_val, 32);
    return 0;
}

int main() {
    int hash_val1[8];
    int hash_val2[8];
    char mingwen[67];
    char plaintext[] = "202100210057";
    char testappend[] = "get";

    cout << "初始信息为" << plaintext << "添加信息为" << testappend << endl;
    sm3(plaintext, hash_val1, 3);
    dump_buffer((char*)hash_val1, 32);
    for (int i = 0; i < 8; i++) {
        hash_val2[i] = reversebytes_uint32t(hash_val1[i]);
    }

    clock_t startTime = clock();
    bit_stuffing(plaintext, 3);
    memcpy(mingwen, plaintext_after_stuffing, 64);
    memcpy(&mingwen[64], testappend, 3);
    sm3(mingwen, hash_val1, 67);
    cout << "消息填充并求哈希值" << endl;
    dump_buffer((char*)hash_val1, 32);
    sm3_length_attack(testappend, hash_val2, 3, 64);
    clock_t endTime = clock();
    cout << "长度扩展攻击用时：" << (double(endTime - startTime) / CLOCKS_PER_SEC)*1000 << "ms" << endl;
    system("pause");
    return 0;
}