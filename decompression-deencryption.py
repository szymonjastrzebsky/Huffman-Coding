import math

with open('skompresowany.txt', 'rb') as file:
    text = [i for i in file.read()]

tab_of_ascii_lists = [[col + row - 256 if col + row > 255 else col + row
                       for col in range(256)] for row in range(256)]

key = input('Podaj klucz: ')

if len(key) == 0:
    print('Brak klucza!')
    exit()

j = 0

dencrypted_text = []

for char in text:

    key_sign = ord(key[j])

    dencrypted_text.append(tab_of_ascii_lists[key_sign].index(char))

    j = (j + 1) % len(key)

compressed_text = dencrypted_text

uniq_signs_count = compressed_text[0]

try:
    dictionary = [chr(compressed_text[i]) for i in range(1, uniq_signs_count + 1)]

    list_to_decompress = [bin(compressed_text[i])[2:].zfill(8)
                          for i in range(uniq_signs_count + 1, len(compressed_text))]

    bin_text = ''.join(list_to_decompress)

    redundant_bits = int(bin_text[:3], 2)

    to_decompress = bin_text[3:(len(bin_text) - redundant_bits)]

    N = math.ceil(math.log2(uniq_signs_count))

    decompressed = [dictionary[int(to_decompress[i:(i + N)], 2)] for i in range(0, len(to_decompress), N)]

    with open('zdekompresowany.txt', 'w') as file:
        file.write(''.join(decompressed))

except (ValueError, IndexError):
    print('Nieprawidlowy klucz!')