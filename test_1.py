import string,random

"""构造密码表"""
def table_code(seed_num):
    # 准备26个大写的英文字母
    table_abc = string.ascii_uppercase
    print(table_abc)

    # 将上面准备好的26个字母字符串 转化为列表保存 以便后续用列表的乱序方法
    list_table_abc = list(table_abc)

    # 括号内的数字我们称之为随机种子，只要种子一样，随机的结果就会是一样的
    #     seed_num = 1024
    random.seed(seed_num)

    table_dict = {}
    for row in range(1,27): # 第一层对横着的26行进行循环
        for col in range(1,27): # 第二层对竖着的26列进行循环
            table_dict[(row,col)] = list_table_abc[col-1]
        # 每构造完一行字母表，就使用乱序方法将26个字母的顺序打乱一次
        random.shuffle(list_table_abc)
    # print(table_dict)
    # 将密码表写入文件 以便后续验证
    with open(f'mi_biao_{seed_num}.txt','w') as f:
        f.write(str(table_dict))
    print(f"密码表 mi_biao_{seed_num}.txt 已生成")
    print()

"""生成加密文本"""
def code_text(ming_wen,key_word,seed_num):

    # 对明文进行密钥转化 计算出加密用的密钥
    ming_wen = ming_wen.upper()
    key_word = key_word.upper()
    mi_yao = list(ming_wen)
    key_word_num = 0 # 密钥初始索引
    mi_wen = [] # 存储密文的列表
    # 读取密码表文件 以便后续使用
    with open(f'mi_biao_{seed_num}.txt','r') as f:
        table_dict = f.read()
        # 使用eval方法 将读取到的字符串类型但是是字典结构的数据，转化成完全的字典类型的数据，
        table_dict = eval(table_dict)
    #         print(type(table_dict),table_dict)


    for index,single_ming_wen in enumerate(ming_wen):
        #     print(index,single_ming_wen)
        if single_ming_wen.isalpha():
            mi_yao[index] = key_word[key_word_num]
            key_word_num += 1
            # 如果密钥索引等于 密钥长度，则重置密钥索引为0
            # 比如 LANG 的最大索引是3 但是长度是4 如果索引等于4 说明索引超出，该从0开始了
            if key_word_num == len(key_word):
                key_word_num = 0

            # 1、得到加密列号，该字母在密码表第一行顺序字母表的列号，就是将来密文的列号
            # ord() 函数可以将字母转化成对应的ASCII表中的数字，26个大写字母对应在计算机中存储顺序是连续的，从A(65)开始到 Z(90)结束
            ming_wen_first_col_position = ord(single_ming_wen)-64
            # 2、得到加密行号，根据明文字母对应的密钥字母，找出明文应该去密码表哪一行进行加密
            ming_wen_first_row_position = ord(mi_yao[index])-64
            # 3、根据（行，列）号，交叉定位，得到明文字母在密码表中的加密结果
            single_mi_wen = table_dict[(ming_wen_first_row_position,ming_wen_first_col_position)]
            mi_wen.append(single_mi_wen)

        else:
            mi_yao[index] = single_ming_wen
            # 如果明文字符不是字母，直接将该字符添加进入密文列表即可
            mi_wen.append(single_ming_wen)

    print("明文",ming_wen)
    print(mi_yao)
    mi_yao = "".join(mi_yao)
    print("密钥",mi_yao)

    print(mi_wen)
    mi_wen = "".join(mi_wen)
    print("密文",mi_wen)

    # 将密文写入文件
    with open(f'mi_wen_{seed_num}.txt','w') as f:
        f.write(str(mi_wen))
    print("加密完成")

"""解密文本"""
def decode_text(key_word,seed_num):
    # 读取密码表数据
    with open(f"mi_biao_{seed_num}.txt","r") as f:
        table_dict = f.read()
    # 使用eval方法 将读取到的字符串类型但是是字典结构的数据，转化成完全的字典类型的数据，
    table_dict = eval(table_dict)
    # print(type(table_dict),table_dict)

    # 读取密文数据
    with open(f"mi_wen_{seed_num}.txt","r") as f2:
        mi_wen = f2.read()

    mi_wen = mi_wen.upper()
    mi_yao = list(mi_wen)
    key_word = key_word.upper()
    key_word_num = 0
    ming_wen = []
    for index,single_mi_wen in enumerate(mi_wen):
        #     print(index,single_ming_wen)
        if single_mi_wen.isalpha():
            mi_yao[index] = key_word[key_word_num]
            key_word_num += 1
            # 如果密钥索引等于 密钥长度，则重置密钥索引为0
            # 比如 LANG 的最大索引是3 但是长度是4 如果索引等于4 说明索引超出，该从0开始了
            if key_word_num == len(key_word):
                key_word_num = 0

            # 知道了密钥字母，也就知道了密文字母所在的行号
            mi_wen_row = ord(mi_yao[index])-64
            # 在密文所在的行里，搜索并找到密文的具体坐标位置
            for mi_wen_row_col in range(1,27):
                # 只要在密钥字母的行里再找到密文字母,其中密文字母的列号，就是明文字母的列号
                if table_dict[(mi_wen_row,mi_wen_row_col)] == single_mi_wen:
                    #                 print(f"密文是：{table_dict[(mi_wen_row,mi_wen_row_col)]},所在行是：{mi_wen_row}，列是：{mi_wen_row_col}")
                    #                 print(f"该密文解密后明文是：{table_dict[(1,mi_wen_row_col)]}")
                    ming_wen.append(table_dict[(1,mi_wen_row_col)])
        else:
            mi_yao[index] = single_mi_wen
            # 如果字符不是字母，则直接添加
            ming_wen.append(single_mi_wen)
    print()
    print("新密文是：",mi_wen)
    print("新密钥是：",mi_yao)
    print("新解密后的明文是：","".join(ming_wen))
    print("解密完成")

# 以图片形式保存密码表
def save_pic_table(seed_num):
    # 将密码表写入图片文件 以便后续更清楚地观察
    from PIL import Image,ImageDraw,ImageFont
    # import time
    import string
    # 准备26个大写的英文字母
    table_abc = string.ascii_uppercase

    img_bac = Image.new("RGB", (600, 600), (255, 255, 255))
    fnt = ImageFont.truetype("simhei", 16)
    color = [(0,0,220),(0,180,0)]

    # 画网格线
    for lin_high in range(20,600,20):
        # 画横线
        ImageDraw.Draw(img_bac).line([(0,lin_high),(600,lin_high)], fill=color[lin_high//20%2], width=1)
        # 画竖线
        ImageDraw.Draw(img_bac).line([(lin_high,0),(lin_high,600)], fill=(0,0,0), width=1)


    # 画行 和 列 的数字标号 以及明文字母
    for first_row_col_num in range(0,27):
        # 画第 一 行的数字标号
        ImageDraw.Draw(img_bac).text((first_row_col_num*20+20+3,0),str(first_row_col_num) ,font=fnt, fill=(0, 0, 0))

        # 画第 二 行的明文字母
        try:
            ImageDraw.Draw(img_bac).text((first_row_col_num*20+20+20+3,20),table_abc[first_row_col_num] ,font=fnt, fill=(0, 0, 0))
        except:
            pass

        # 画第 一 列的数字标号
        ImageDraw.Draw(img_bac).text((0+3,first_row_col_num*20+20),str(first_row_col_num) ,font=fnt, fill=(0, 0, 0))
        # 画第 二 列的明文字母
        try:
            ImageDraw.Draw(img_bac).text((20+3,first_row_col_num*20+20+20),table_abc[first_row_col_num],font=fnt, fill=(0, 0, 0))
        except:
            pass


    # 填充具体的密码表内的字母

    # 读取密码表数据
    #     seed_num = 1024
    with open(f"mi_biao_{seed_num}.txt","r") as f:
        table_dict = f.read()
    # 使用eval方法 将读取到的字符串类型但是是字典结构的数据，转化成完全的字典类型的数据，
    table_dict = eval(table_dict)

    # 将密码表中字母写入图片
    for single_acb_site, single_acb_name in table_dict.items():
        ImageDraw.Draw(img_bac).text((single_acb_site[1]*20+20+3,single_acb_site[0]*20+20),single_acb_name ,font=fnt, fill=(200, 100, 200))

    ImageDraw.Draw(img_bac).text((240,560),"维吉尼亚密码表" ,font=fnt, fill=(200, 0, 0))
    ImageDraw.Draw(img_bac).text((260,580),"浪淘三千" ,font=fnt, fill=(200, 0, 0))

    # 展示图片
    img_bac.show()
    # 等展示的图片关闭后，保存图片
    img_bac.save(f'维吉尼亚密码表-{seed_num}.jpg')

while True:
    do_text = """
    维吉尼亚密码
    1、加密
    2、解密
    3、生成文本密码表
    4、生成图片密码表
    5、没事了
    """
    print(do_text)
    do_what = input("你要做什么操作,请输入序号：")

    if do_what == "1":
        seed_num = int(input("请输入你的随机种子："))
        ming_wen = input("请输入你的明文：")
        key_word = input("请输入你的口令：")
        # 进行加密的时候 将明文字符 和 关键口令 随机种子 作为参数传递
        code_text(ming_wen,key_word,seed_num)
    elif do_what == "2":
        seed_num = int(input("请输入你的随机种子："))
        key_word = input("请输入你的口令：")
        # 进行解密的时候 将关键口令 随机种子 作为参数传递
        decode_text(key_word,seed_num)
    elif do_what == "3":
        seed_num = int(input("请输入你的随机种子："))
        # 构造密码表时候 将随机种子作为参数传递
        table_code(seed_num)
    elif do_what == "4":
        seed_num = int(input("请输入你的随机种子："))
        print("欢迎下次使用")
    elif do_what == "5":
        print("欢迎下次使用")
        break
    else:
        print()
        print("！！！！请按规则输入")
