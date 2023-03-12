import copy


def key_to_order(key_word):
    byte_key_list = [ord(element) for element in list(key_word)]
    key_list = [-1] * len(byte_key_list)
    temp_byte_key_list = copy.deepcopy(byte_key_list)
    temp_byte = max(byte_key_list)
    for j in range(len(byte_key_list)):
        temp_position = byte_key_list.index(max(temp_byte_key_list))
        temp_byte = max([value for value in byte_key_list if value is not None])
        for i in range(len(byte_key_list) - 1, -1, -1):
            if byte_key_list[i] is not None:
                if byte_key_list[i] <= temp_byte:
                    temp_byte = byte_key_list[i]
                    temp_position = i
        key_list[temp_position] = max(key_list) + 1
        byte_key_list[temp_position] = None
        temp_byte_key_list[temp_position] = -1
    return key_list


# TODO: Transpositional_decrypt_leer: DisrColTransKey2Changed
def insert_space(plain_list, key_list):
    cipher_list = []
    i = 0
    temp_index = 0
    last_space_index = 0
    while i < len(plain_list):
        if (i - last_space_index) == key_list[temp_index % len(key_list)]:
            cipher_list.append(" ")
            temp_index += 1
            last_space_index = i
        else:
            cipher_list.append(plain_list[i])
            i += 1
    return cipher_list


def into_rows(plain_list, key_list):
    cipher_list = []
    row = []
    for i in range(len(plain_list)):
        if i % len(key_list) == 0 and 0 != len(row):
            cipher_list.append(row)
            row = []
        row.append(plain_list[i])
    cipher_list.append(row)
    return cipher_list


def read_ordered_rows(plain_list_with_rows, key_list):
    cipher_list = []
    x = 0
    for x in range(len(plain_list_with_rows[0])):
        for y in range(len(plain_list_with_rows)):
            if key_list.index(x) < len(plain_list_with_rows[y]):
                cipher_list.append(plain_list_with_rows[y][key_list.index(x)])
    return cipher_list


# TODO: Transpositional_encrypt_leer-DisrColTransKey2Changed

def sum_up(key, l, pos):
    sum = 0
    for i in range(key[pos]):
        sum += l[key.index(i)]
    return sum


def read_ordered_rows_reverse(cipher, key):
    cipher_list = list(cipher)
    full_y_length = int(len(cipher_list) / len(key))
    last_row_length = len(cipher_list) % len(key)
    amount_list = [full_y_length + (1 if i < last_row_length else 0) for i in range(len(key))]
    plain = [["" for j in range(len(key))] for i in range(full_y_length + (1 if last_row_length > 0 else 0))]
    for i in range(len(cipher_list)):
        for j in range(len(amount_list)):
            pos = sum_up(key, amount_list, j)
            for y in range(amount_list[j]):
                plain[y][j] = cipher_list[pos + y]

    return plain


def into_rows_reverse(cipher_list, key_list):
    plain = []
    for y_content in cipher_list:
        for x_content in y_content:
            plain.append(x_content)
    return plain


def insert_space_reverse(cipher_list, key_list):
    plain = cipher_list
    position = 0
    i = 0
    j = 0
    while i < len(plain):
        value = key_list[j%len(key_list)]
        if key_list[j % len(key_list)] == i-position:
            plain.pop(i)
            position = i
            j += 1
        else:
            i += 1
    return plain


if __name__ == "__main__":
    plain = "Hallo Michael. Hier ist Tobias!"
    key = key_to_order("hallo")
    disruption_key = key_to_order("key")
    print(plain)
    a = insert_space(plain, key)
    ah = into_rows(a, disruption_key)
    haha = read_ordered_rows(ah, disruption_key)
    cipher = ""
    for c in haha:
        cipher += c
    plain_0 = read_ordered_rows_reverse(list(cipher), disruption_key)
    plain_1 = into_rows_reverse(plain_0, disruption_key)
    plain_2 = insert_space_reverse(plain_1, key)
    plain_3 = ""
    for c in plain_2:
        plain_3 += c
    print(plain_3)
