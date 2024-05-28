# 加密函数
def encrypt(ming, key):
    key_length = len(key)  # 获取密钥的长度
    key_asc = [ord(i) for i in key]  # 将密钥中的每个字符转换为对应的ASCII值
    ming_asc = [ord(i) for i in ming]  # 将明文中的每个字符转换为对应的ASCII值
    mi = ''  # 密文
    for i in range(len(ming_asc)):
        num = (ming_asc[i] + key_asc[i % key_length]) % 26  # 使用维吉尼亚加密算法进行加密
        mi += chr(num + 65)  # 将加密后的ASCII值转换回字符，并添加到密文字符串中
    return mi

# 解密函数
def decrypt(mi, key):
    key_length = len(key)  # 获取密钥的长度
    key_asc = [ord(i) for i in key]  # 将密钥中的每个字符转换为对应的ASCII值
    mi_asc = [ord(i) for i in mi]  # 将密文中的每个字符转换为对应的ASCII值
    ming = ''  # 初始化明文字符串
    for i in range(len(mi_asc)):
        num = (mi_asc[i] - key_asc[i % key_length] + 26) % 26  # 使用维吉尼亚解密算法进行解密
        ming += chr(num + 65)  # 将解密后的ASCII值转换回字符，并添加到明文字符串中
    return ming

# 主函数
def main():
    while True:
        choice = input("\n1.加密\n2.解密\n请选择操作，输入其他任意键退出： \n")
        if choice == '1':
            ming = input("请输入明文: ").upper()
            key = input("请输入密钥: ").upper()
            mi = encrypt(ming, key)  # 加密
            print("加密后的文本是：", mi)
            with open('密文1.txt', 'w') as f:
                f.write(mi)
            print("密文已保存至 '密文1.txt'")
        elif choice == '2':
            try:
                with open('密文1.txt', 'r') as f:  # 读取密文
                    mi = f.read()
                key = input("请输入密钥: ").upper()
                mi2 = decrypt(mi, key)  # 解密
                print("解密后的文本是： ", mi2)
            except FileNotFoundError:  # 文件不存在
                print("未找到密文。")
        else:
            break

if __name__ == "__main__":
    main()
