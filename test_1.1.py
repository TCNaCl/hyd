import string, random

def create_password_table(seed):
    """生成并保存密码表"""
    letters = string.ascii_uppercase
    letters_list = list(letters)
    random.seed(seed)
    table = {}
    for row in range(1, 27):
        for col in range(1, 27):
            table[(row, col)] = letters_list[col - 1]
        random.shuffle(letters_list)

    with open(f'table_{seed}.txt', 'w') as f:
        f.write(str(table))
    print(f"密码表 table_{seed}.txt 已生成")

def encrypt_text(plain_text, password, seed):
    """生成加密文本，同时生成密码表"""
    create_password_table(seed)  # 在加密前生成密码表
    plain_text = plain_text.upper()
    password = password.upper()
    temp_key = list(plain_text)
    password_index = 0
    cipher_text = []

    with open(f'table_{seed}.txt', 'r') as f:
        table = eval(f.read())

    for index, char in enumerate(plain_text):
        if char.isalpha():
            temp_key[index] = password[password_index]
            password_index += 1
            if password_index == len(password):
                password_index = 0
            row = ord(char) - 64
            col = ord(temp_key[index]) - 64
            cipher_char = table[(row, col)]
            cipher_text.append(cipher_char)
        else:
            temp_key[index] = char
            cipher_text.append(char)

    cipher_text = "".join(cipher_text)
    with open(f'cipher_{seed}.txt', 'w') as f:
        f.write(cipher_text)
    print("密文", cipher_text, "已保存")

def decrypt_text(password, seed):
    """解密文本"""
    with open(f"table_{seed}.txt", "r") as f:
        table = eval(f.read())

    with open(f"cipher_{seed}.txt", "r") as f2:
        cipher = f2.read().upper()

    password = password.upper()
    temp_key = list(cipher)
    password_index = 0
    decrypted_text = []

    for index, char in enumerate(cipher):
        if char.isalpha():
            temp_key[index] = password[password_index]
            password_index += 1
            if password_index == len(password):
                password_index = 0

            row = ord(temp_key[index]) - 64
            col = next(col for col, letter in table.items() if letter == char and col[0] == row)
            decrypted_text.append(chr(col[1] + 64))
        else:
            temp_key[index] = char
            decrypted_text.append(char)

    decrypted_text = "".join(decrypted_text)
    print("解密后的明文是：", decrypted_text)

def main():
    while True:
        print("\n维吉尼亚密码\n1、加密\n2、解密\n请选择操作，输入其他任意键退出：")
        action = input("请输入操作序号：")

        if action == "1":
            seed = int(input("请输入随机种子："))
            plain_text = input("请输入明文：")
            password = input("请输入密钥：")
            encrypt_text(plain_text, password, seed)
        elif action == "2":
            seed = int(input("请输入随机种子："))
            password = input("请输入密钥：")
            decrypt_text(password, seed)
        else:
            break

if __name__ == "__main__":
    main()
