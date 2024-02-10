import math

# funkcja konwertujaca wartosc decymalna na binarna dodajac przy tym ew. zera wiodace

def to_binary(dec_value, bits_count):
    return format(dec_value, 'b').zfill(bits_count)

# odczytujemy wygenerowany plik z tekstem do kompresji

with open("do_kompresji.txt", "r") as file:
    content = file.read()

# posortowana lista zawierajaca wypisany kazdy rodzaj znaku wystepujacego w tekscie

char_types_summary_list = sorted(list(set(content)))
print(f'Slownik: {''.join(char_types_summary_list)}')

# ilosc typow znakow w tekscie

diff_char_types = len(char_types_summary_list)
print(f'X: {str(diff_char_types)}')

# obliczenie minimalnej ilosci bitow potrzebnej na zakodowanie jednego znaku w tekscie

N = math.ceil(math.log2(diff_char_types))
print(f'N: {str(N)}')

# obliczenie ilosci nadmiarowych bitow, a konkretniej 1

R = (8 - (3 + len(content) * N) % 8) % 8
print(f'R: {str(R)}')

# dlugosc tekstu przed kompresja

print(f'Dlugosc tekstu: {str(len(content))}')

# tworzymy plik binarny ze skompresowanym tekstem

with open("skompresowany.txt", "wb") as compressed:
    # inicjalizacja pustej tablicy bajtów
    bytes_tab = bytearray()

    # dodanie do tablicy ilosci typow znakow w tekscie przed jego kompresja

    bytes_tab.append(diff_char_types)

    # dodanie do tablicy elementow z listy zawierajacej wypisany kazdy rodzaj znaku wystepujacego w tekscie

    for char_type in char_types_summary_list:
        bytes_tab.append(ord(char_type))

    # inicjalizacja zmiennej przechowujacej nasz tekst w postaci ciagu 0 i 1

    binary_text = ""

    # dodajemy 3 bity, ktorych wartosc informuje nas o tym ile mamy dodac jedynek na koncu zakodowanego tekstu

    binary_text += to_binary(R, 3)

    # zamieniamy tekst do kompresji na ciag zer i jedynek

    for char in content:
        binary_text += to_binary(char_types_summary_list.index(char), N)

    # dodajemy nadmiarowe jedynki na koniec zakodowanego tekstu

    binary_text += '1' * R

    list_of_chr = []

    # konwertujemy każde 8 bitow na znak ASCII

    for i in range(0, len(binary_text), 8):
        sign = chr(int(binary_text[i:(i + 8)], 2))

        list_of_chr.append(sign)

        bytes_tab.append(ord(sign))

    print(f'Dlugosc tekstu po kompresji: {str(len(list_of_chr))}')

    # ------------------------------------------------------

    tab_of_ascii_lists = [[col + row - 256 if col + row > 255 else col + row
                           for col in range(256)] for row in range(256)]

    key = input('Podaj klucz: ')

    if len(key) == 0:
        print('Brak klucza!')
        exit()

    index = 0

    tab_encrypt = []

    for char in bytes_tab:
        key_char = ord(key[index])

        tab_encrypt.append(tab_of_ascii_lists[key_char][char])

        index = (index + 1) % len(key)

    compressed.write(bytes(tab_encrypt))
