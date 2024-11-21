import random
import string

ip = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

pc1 = [
    57, 49, 41, 33, 25, 17, 9, 1,
    58, 50, 42, 34, 26, 18, 10, 2,
    59, 51, 43, 35, 27, 19, 11, 3,
    60, 52, 44, 36, 63, 55, 47, 39,
    31, 23, 15, 7, 62, 54, 46, 38,
    30, 22, 14, 6, 61, 53, 45, 37,
    29, 21, 13, 5, 28, 20, 12, 4
]

round_shift = [1, 1, 2, 2,
                  2, 2, 2, 2,
                  1, 2, 2, 2,
                  2, 2, 2, 1]

pc2 = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

expansion = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

s_box = [
    #1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    #2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    #3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    #4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    #5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    #6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    #7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    #8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

p_box = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

ip_invers = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

def string_to_binary(usr_input):
    binary_blocks = []
    
    for i in range(0, len(usr_input), 8): #1 blok, 8 karakter
        block = usr_input[i:i+8]
        
        binary = ''
        for char in block:
            bin_char = format(ord(char), '08b')
            binary += bin_char
        
        binary = binary.ljust(64, '0') # Jika kurang dari 64 bit, padding dengan 0
        
        binary_blocks.append(binary)
    
    full_binary = ''.join(binary_blocks)

    return full_binary

def initial_permutation(binary):
    ip_result = [None] * 64
    
    for i in range(64):
        ip_result[i] = binary[ip[i] - 1]

    ip_result_str = ''.join(ip_result)
    
    return ip_result_str
    
def internal_key(key):
    
    binary_key = ''

    # Convert characters ke binary
    for char in key:
        bin_key = format(ord(char), '08b') 
        binary_key += bin_key
    
    pc1_key_string = ''.join(binary_key[bit - 1] for bit in pc1) #pc1

    c0 = pc1_key_string[:28]
    d0 = pc1_key_string[28:]
    round_keys = []
    for round_num in range(16):
        c0 = c0[round_shift[round_num]:] + c0[:round_shift[round_num]]
        d0 = d0[round_shift[round_num]:] + d0[:round_shift[round_num]]
        cd_concatenated = c0 + d0

        round_key = ''.join(cd_concatenated[bit - 1] for bit in pc2) #pc2

        round_keys.append(round_key)
    
    return round_keys

def binary_to_hex(binary_str):
    decimal_value = int(binary_str, 2)
    hex_value = hex(decimal_value)[2:].upper()
    return hex_value

def hex_to_binary(hex_str):
    decimal_value = int(hex_str, 16)
    binary_str = bin(decimal_value)[2:]
    padded_binary_str = binary_str.zfill(64)
    return padded_binary_str

def des_encryption(usr_input, key):
    binary_usr_input = string_to_binary(usr_input)

    blocks = [binary_usr_input[i:i+64] for i in range(0, len(binary_usr_input), 64)]
    
    round_keys = internal_key(key)

    encrypted_blocks = []

    for block in blocks:
        ip_result_str = initial_permutation(block)

        l_i = ip_result_str[:32]
        r_i = ip_result_str[32:]

        for round_num in range(16):
            # expansion 32 bits ke 48 bits
            expand_result = [r_i[i - 1] for i in expansion]
            expand_result_str = ''.join(expand_result)

            round_key_i = round_keys[round_num]

            xor_result_str = ''
            for i in range(48):
                xor_result_str += str(int(expand_result_str[i]) ^ int(round_key_i[i]))

            six_bit = [xor_result_str[i:i+6] for i in range(0, 48, 6)]

            s_box_sub = ''

            for i in range(8):
                row = int(six_bit[i][0] + six_bit[i][-1], 2)
                col = int(six_bit[i][1:-1], 2)

                s_box_value = s_box[i][row][col]

                s_box_sub += format(s_box_value, '04b')

            p_box_result = [s_box_sub[i - 1] for i in p_box] #p_box

            l_i_list = list(l_i)

            # left xor pbox
            new_r_i = [str(int(l_i_list[i]) ^ int(p_box_result[i])) for i in range(32)]
            new_r_i_str = ''.join(new_r_i)

            l_i = r_i
            r_i = new_r_i_str

        round_result = r_i + l_i

        result = [round_result[ip_invers[i] - 1] for i in range(64)] #ip_invers

        result_str = ''.join(result)

        encrypted_blocks.append(result_str)

    full_result = ''.join(encrypted_blocks)

    result_hex = binary_to_hex(full_result)
    
    # print("Final Cipher text (HEX):", result_hex)
    return result_hex

def des_decryption(usr_input, key):
    round_keys = internal_key(key)

    blocks = [usr_input[i : i + 16] for i in range(0, len(usr_input), 16)]

    decrypted_blocks = []  # Untuk menyimpan hasil dekripsi setiap blok

    for block in blocks:
        bin_usr_input = hex_to_binary(block)

        bin_usr_input_ip = initial_permutation(bin_usr_input)

        l_i = bin_usr_input_ip[:32]
        r_i = bin_usr_input_ip[32:]

        for round_num in range(16):
            expand_result = [r_i[i - 1] for i in expansion]

            # XOR ekspansi dan round key (dalam urutan terbalik)
            round_key_i = round_keys[15 - round_num]
            xor_result_str = ''.join([str(int(expand_result[i]) ^ int(round_key_i[i])) for i in range(48)])

            six_bit = [xor_result_str[i:i + 6] for i in range(0, 48, 6)]

            s_box_sub = ''
            for i in range(8):
                row = int(six_bit[i][0] + six_bit[i][-1], 2)
                col = int(six_bit[i][1:-1], 2)
                s_box_value = s_box[i][row][col]
                s_box_sub += format(s_box_value, '04b')

            p_box_result = [s_box_sub[i - 1] for i in p_box]

            # XOR l_i dan P-box
            new_r_i = ''.join([str(int(l_i[i]) ^ int(p_box_result[i])) for i in range(32)])

            l_i, r_i = r_i, new_r_i

        round_result = r_i + l_i

        result = [round_result[ip_invers[i] - 1] for i in range(64)] #ip invers

        decrypted_blocks.append(''.join(result))

    full_decrypt_result = ''.join(decrypted_blocks)

    plain_text_result = "".join([chr(int(full_decrypt_result[i : i + 8], 2)) for i in range(0, len(full_decrypt_result), 8)])
    
    return plain_text_result