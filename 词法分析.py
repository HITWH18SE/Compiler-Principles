# 预处理函数，去掉多余的空格、tab、回车和注释
def preprocess(raw_filename, preprocess_filename):
    fp_read = open(raw_filename, 'r')
    fp_write = open(preprocess_filename, 'w')

    # 读取源代码
    raw_text = fp_read.readlines()
    length = len(raw_text)
    i = 0
    while i < length:
        # 获取其中一行
        line = raw_text[i]
        # 去除单行注释
        index = line.find('//')
        if index != -1:
            line = line[0: index]
        # 去除多行注释
        index = line.find('/*')
        if index != -1:
            index = line.find('*/')
            while index == -1:
                i += 1
                line = raw_text[i]
                index = line.find('*/')
            line = line[index + 2:]
        # 去除后仍有其他内容，则去除多余空格并写入预处理文件
        if line:
            words = line.split()
            for word in words:
                fp_write.write(word + ' ')
        i += 1


# 处理，关键词、运算符、界符、数字、字符串、标识符、非法标识符
def process(preprocess_filename):
    # 关键词
    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
                'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
                'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
    # 运算符
    operator = ['+', '-', '*', '/', '%', '++', '--', '+=', '-=', '+=', '/=',  # 算术运算符
                '==', '!=', '>', '<', '>=', '<=',  # 关系运算符
                '&', '|', '^', '~', '<<', '>>', '>>>',  # 位运算符
                '&&', '||', '!',  # 逻辑运算符
                '=', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '&=', '^=', '|=',  # 赋值运算符
                '?:']  # 条件运算符
    # 界符
    delimiters = ['{', '}', '[', ']', '(', ')', '.', ',', ':', ';']

    fp_read = open(preprocess_filename, 'r')
    fp_write = open('result.txt', 'w')
    lines = fp_read.readlines()  # 依旧是按行读取
    i = -1
    for line in lines:  # 逐行遍历
        length = len(line)  # 获得当前行字符长度为了遍历每个字符
        while i < length - 1:
            i += 1
            if line[i] == ' ':  # 当前字符为空格，直接跳过
                continue
            # 当前字符在界符集中
            if line[i] in delimiters:
                print('(%s, delimiters)' % line[i], file=fp_write)
                continue
            # 当前字符在运算符集中
            if line[i] in operator:
                # 双符号运算符
                while line[i + 1] in operator:
                    print('(%s%s, operator)' % (line[i], line[i + 1]), file=fp_write)
                    i += 1
                # 单符号运算符
                else:
                    print('(%s, operator)' % line[i], file=fp_write)
                continue
            # 当前字符为数字（包括整数和浮点数）
            if line[i].isdigit():
                print('(', end='', file=fp_write)
                while line[i].isdigit():
                    # 浮点数处理
                    if line[i + 1] == '.':
                        print(line[i], end='', file=fp_write)
                        i += 1
                    print(line[i], end='', file=fp_write)
                    i += 1
                print(', digit)', file=fp_write)
                continue

            # 当前字符为字符串
            if line[i] == '\"' or line[i] == '\'':
                mark = line[i]
                temp = ''
                i += 1
                while line[i] != mark:
                    temp += line[i]
                    i += 1
                print('(%s, string)' % temp, file=fp_write)
                continue

            # 当前字符为关键词或标识符
            # 先获取该关键词或标识符
            temp = ''
            while True:
                if i > length - 1 or line[i] == ' ' or line[i] in operator or line[i] in delimiters:
                    break
                else:
                    temp += line[i]
                i += 1
            # 再判断
            # 当前字符在关键词集中
            if temp in keywords:
                print('(%s, keywords)' % temp, file=fp_write)
            # 当前字符可能是标识符（额外判断是否非法）
            else:
                if not temp[0].isalpha():
                    print('(%s, error)' % temp, file=fp_write)
                else:
                    print('(%s, identifier)' % temp, file=fp_write)
            i -= 1


# 处理，关键词、运算符、界符、数字、字符串、标识符、非法标识符
def process_2(preprocess_filename):
    # 关键词
    # keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
    #             'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
    #             'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
    keywords = ['if', 'else', 'while', 'return', 'int', 'float', 'double', 'true', 'false']
    # 运算符
    # operator = ['+', '-', '*', '/', '%', '++', '--', '+=', '-=', '+=', '/=',  # 算术运算符
    #             '==', '!=', '>', '<', '>=', '<=',  # 关系运算符
    #             '&', '|', '^', '~', '<<', '>>', '>>>',  # 位运算符
    #             '&&', '||', '!',  # 逻辑运算符
    #             '=', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '&=', '^=', '|=',  # 赋值运算符
    #             '?:']  # 条件运算符
    operator = ['+', '-', '*', '/',  # 算术运算符
                '==', '!=', '>', '<', '>=', '<=',  # 关系运算符
                '&&', '||', '!',  # 逻辑运算符
                '='  # 赋值运算符
                ]
    # 界符
    # delimiters = ['{', '}', '[', ']', '(', ')', '.', ',', ':', ';', '<', '>']
    delimiters = ['{', '}', '(', ')', ',', ';']

    token = []

    fp_read = open(preprocess_filename, 'r')
    # fp_write = open('1.5带错误报告的完整token序列.txt', 'w')

    lines = fp_read.readlines()  # 按行读取
    length = len(lines)
    i = 0
    while i < length:
        lines[i] = lines[i].replace('\t', ' ')
        lines[i] = lines[i].replace('\n', '')
        lines[i] = lines[i].strip()
        i += 1

    # print(str(lines))

    row = 0
    while row < len(lines):
        line = lines[row]
        i = 0

        while i < len(line):
            # print('line[i]=' + line[i])
            # 当前字符为空格，跳过
            if line[i] == ' ':
                i += 1
                continue
            # 当前字符为单行注释，跳过
            if line[i] == '/' and line[i + 1] == '/':
                # print("line[i] == '/' and line[i + 1] == '/'")
                # print('(%s, //, single-line annotation)' % (str(row)), file=fp_write)
                break
            # 当前字符为多行注释，跳过
            if line[i] == '/' and line[i + 1] == '*':
                # print('(%s, /*, multi-line annotation)' % (str(row)), file=fp_write)
                index = line.find('*/')
                while index == -1:
                    row += 1
                    line = lines[row]
                    index = line.find('*/')
                # print('(%s, */, multi-line annotation)' % (str(row)), file=fp_write)
                i = index + 2
                continue
            # 当前字符在界符集中
            if line[i] in delimiters:
                # print('(%s, %s, delimiters)' % (str(row), line[i]), file=fp_write)

                token.append([line[i], "界符"])

                i += 1
                continue
            # 多符号运算符
            if line[i] + line[i + 1] in operator:
                temp = line[i] + line[i + 1]
                i += 2
                token.append([temp, "运算符"])
                continue

            # 当前字符在运算符集中
            if line[i] in operator:
                # print('(%s, %s, operator)' % (str(row), temp), file=fp_write)

                token.append([line[i], "运算符"])
                i += 1
                continue
            # 当前字符为数字（包括整数和浮点数）
            if line[i].isdigit():
                temp = ""
                # 多个数字
                while line[i].isdigit() or line[i] == '.':
                    temp += line[i]
                    # print("temp = " + temp)
                    i += 1
                    if i > len(line) - 1:
                        break

                # 防止有以数字开头的标识符等非法
                if line[i].isdigit() or line[i] in operator or line[i] in delimiters or line[i] == ' ':

                    # 浮点数
                    if temp.find('.') != -1:
                        # 防止有多个点的非法浮点数
                        index = temp.find('.')
                        if temp[index:].find('.') > 0:
                            # print('(%s, %s, error)' % (str(row), temp), file=fp_write)
                            token.append([temp, "错误"])
                        else:
                            # print('(%s, %s, float)' % (str(row), temp), file=fp_write)

                            token.append([temp, "浮点数"])

                    else:
                        # print('(%s, %s, integer)' % (str(row), temp), file=fp_write)

                        token.append([temp, "整数"])

                else:
                    # print('(%s, %s, error)' % (str(row), temp), file=fp_write)
                    token.append([temp, "错误"])

                continue
            # 当前字符为字符串
            if line[i] == '\"' or line[i] == '\'':
                # print("line[i] == '\"' or line[i] == '\''")
                # print('(%s, %s, delimiters)' % (str(row), line[i]), file=fp_write)
                mark = line[i]
                # print('mark = ' + mark)
                temp = ""
                i += 1
                while line[i] != mark:
                    temp += line[i]
                    # print("temp = " + temp)
                    i += 1
                    if i == len(line):
                        i -= 1
                        print("break = " + temp)
                        break
                # print("temp = " + temp + " line[i] = "+line[i])

                # 找到了另一端
                if line[i] == mark:
                    # print('(%s, %s, string)' % (str(row), temp), file=fp_write)
                    # print('(%s, %s, delimiters)' % (str(row), line[i]), file=fp_write)

                    token.append([temp, "字符串"])
                    token.append([line[i], "界符"])

                # 没找到另一端
                else:
                    # print('(%s, %s, error)' % (str(row), temp), file=fp_write)
                    token.append([temp, "错误"])
                i += 1
                continue

            # 当前字符为关键词或标识符
            # 先获取该关键词或标识符
            temp = ""
            while True:
                if i > len(line) - 1 or line[i] == ' ' or line[i] in operator or line[i] in delimiters:
                    break
                else:
                    temp += line[i]
                i += 1
            i -= 1
            # print("temp = " + str(temp))
            # print("after line[i] = " + line[i])
            # 再判断
            # 当前字符在关键词集中
            if temp in keywords:
                # print('(%s, %s, keywords)' % (str(row), temp), file=fp_write)

                token.append([temp, "关键词"])

            # 当前字符可能是标识符（额外判断是否非法）
            else:
                if not temp[0].isalpha():
                    # print('(%s, %s, error)' % (str(row), temp), file=fp_write)
                    token.append([temp, "错误"])
                else:
                    # print('(%s, %s, identifier)' % (str(row), temp), file=fp_write)
                    token.append([temp, "标识符"])

            i += 1
        row += 1

    result_filename = '1.token序列.txt'
    write = open(result_filename, 'w', encoding='UTF-8')
    for t in token:
        print('(%s, %s)' % (str(t[0]), str(t[1])), file=write)
    print("已获取token序列，词法分析部分结束")

    return token


def main():
    raw_filename = '0.源代码.txt'
    # preprocess_filename = 'preprocess.txt'
    # preprocess(raw_filename, preprocess_filename)
    # process(preprocess_filename)
    token = process_2(raw_filename)
    print(token)


if __name__ == '__main__':
    main()
