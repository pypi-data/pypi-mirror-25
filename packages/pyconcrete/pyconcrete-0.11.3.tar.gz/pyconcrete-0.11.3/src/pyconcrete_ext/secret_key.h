
        #define SECRET_NUM 0x39
        #define SECRET_KEY_LEN 16
        static const unsigned char* GetSecretKey()
        {
            unsigned int i = 0;
            static unsigned char key[] = {(0xEB ^ (0x39 - 0)), (0xA6 ^ (0x39 - 1)), (0x4D ^ (0x39 - 2)), (0x51 ^ (0x39 - 3)), (0xA5 ^ (0x39 - 4)), (0x49 ^ (0x39 - 5)), (0x82 ^ (0x39 - 6)), (0x90 ^ (0x39 - 7)), (0xB9 ^ (0x39 - 8)), (0xDA ^ (0x39 - 9)), (0x86 ^ (0x39 - 10)), (0x15 ^ (0x39 - 11)), (0x1A ^ (0x39 - 12)), (0x12 ^ (0x39 - 13)), (0x1B ^ (0x39 - 14)), (0xB6 ^ (0x39 - 15)), 0/* terminal char */};
            static int is_encrypt = 1/*true*/;
            if( is_encrypt )
            {
                for(i = 0 ; i < SECRET_KEY_LEN ; ++i)
                {
                    key[i] = key[i] ^ (SECRET_NUM - i);
                }
                is_encrypt = 0/*false*/;
            }
            return key;
        }
    