import 词法分析
import 语法分析


# 新建一个中间变量t（序号与id表中已有的t不能相同），并存入id表
def get_t(id_table, type):
    i = 1
    while "t" + str(i) in id_table.keys():
        i += 1
    t = "t" + str(i)
    add_id(id_table, t, type)
    return t


# 新建一个行标记L（序号与L表中已有的L不能相同），并存入L表
def get_L(L_table):
    i = 1
    while "L" + str(i) in L_table:
        i += 1
    L = "L" + str(i)
    L_table.append(L)
    return L


# 新建一个id项
def add_id(id_table, id, type):
    # 判断是否重复声明，如果重复声明，就弹出错误，否则在id表中新建id项
    if id in id_table.keys():
        print("错误：%s 重复声明" % id)
        return False
    else:
        id_table[id] = {}
        id_table[id]["type"] = type
        return True


# 遍历语法分析树，执行语义子程序
def translate(node, id_table, L_table):
    # 从该结点的子结点中接受到的所有属性，是字典嵌套，外层key是子结点的字符，内层key是不同的属性，如code、t
    parameters = {}
    # 先进行深度优先的先序遍历
    for c in node.child:
        node_name = c.character
        # 若出现了重复的右部字符，就在后面添加数字后加入属性字典
        if c.character in parameters.keys():
            i = 2
            while c.character + str(i) in parameters.keys():
                i = i + 1
            node_name += str(i)
        parameters[node_name] = translate(c, id_table, L_table)

    # 等返回上层结点（归约）时执行该结点的语义动作
    # 先获取该结点对应表达式的左部和右部（该结点的字符为对应表达式的左部）
    right = []
    for c in node.child:
        right.append(c.character)
    left = node.character

    # print("node: ", end="")
    # print(node.character)
    # print("left = " + str(left))
    # print("right = " + str(right))
    # print("parameters:")
    # print(parameters)
    # print()

    # 如果这个结点是叶子结点，说明没有对应的产生式，则直接返回属性
    if not right:
        # 特殊情况，叶子结点是id，返回具体名称/值
        if left == "id" or left == "digit":
            return {"name": node.token[0]}
        else:
            return {"name": left}

    # 具体的语义动作（返回值为当前节点的某些属性，默认当前结点已经接收到了子结点传过来的属性
    # 若有重复名称的子结点，则子结点名字后面带序号2、3等

    if left == "程序" and right == ["函数定义"]:
        filename = '9.中间代码.txt'
        write = open(filename, 'w', encoding='UTF-8')
        print(str(parameters["函数定义"]["code"]), file=write)
        print("中间代码生成完毕，语义分析部分结束")
        # print(id_table)
        return
    # 函数定义以及传入参数
    elif left == "函数定义" and right == ["函数定义", "函数定义"]:
        code = "%s\n\n%s" % (str(parameters["函数定义"]["code"]), str(parameters["函数定义2"]["code"]))
        return {"code": code}
    elif left == "函数定义" and right == ["变量类型", "id", "(", ")", "{", "函数块", "}"]:

        add_id(id_table, parameters["id"]["name"], parameters["变量类型"]["name"])

        code = "%s %s()\n{\n%s\n}" % (
            str(parameters["变量类型"]["name"]), str(parameters["id"]["name"]), str(parameters["函数块"]["code"]))
        return {"code": code}
    elif left == "函数定义" and right == ["变量类型", "id", "(", "传入参数", ")", "{", "函数块", "}"]:

        add_id(id_table, parameters["id"]["name"], parameters["变量类型"]["name"])

        code = "%s %s(%s)\n{\n%s\n}" % (
            str(parameters["变量类型"]["name"]), str(parameters["id"]["name"]), str(parameters["传入参数"]["code"]),
            str(parameters["函数块"]["code"]))
        return {"code": code}
    elif left == "传入参数" and right == ["变量类型", "id"]:

        add_id(id_table, parameters["id"]["name"], parameters["变量类型"]["name"])

        code = "%s %s" % (str(parameters["变量类型"]["name"]), str(parameters["id"]["name"]))
        return {"code": code}
    elif left == "传入参数" and right == ["变量类型", "id", ",", "传入参数"]:

        add_id(id_table, parameters["id"]["name"], parameters["变量类型"]["name"])

        code = "%s %s, %s" % (
            str(parameters["变量类型"]["name"]), str(parameters["id"]["name"]), str(parameters["传入参数"]["code"]))
        return {"code": code}
    elif left == "函数块" and right == ["函数块", "函数块"]:
        code = "%s%s" % (str(parameters["函数块"]["code"]), str(parameters["函数块2"]["code"]))
        return {"code": code}
    # 声明
    elif left == "函数块" and right == ["变量类型", "id", ";"]:

        add_id(id_table, parameters["id"]["name"], parameters["变量类型"]["name"])

        code = "%s %s\n" % (str(parameters["变量类型"]["name"]), str(parameters["id"]["name"]))
        return {"code": code}
    # 赋值
    elif left == "函数块" and right == ["id", "=", "算术表达式", ";"]:
        code = "%s" % str(parameters["算术表达式"]["code"])
        code += "%s = %s\n" % (str(parameters["id"]["name"]), str(parameters["算术表达式"]["t"]))
        return {"code": code}
    # 循环
    elif left == "函数块" and right == ["while", "(", "布尔表达式", ")", "{", "函数块", "}"]:
        L_this = get_L(L_table)
        L_true = get_L(L_table)
        L_false = get_L(L_table)

        code = "%s" % (str(parameters["布尔表达式"]["code"]))
        code += "%s: (while)if %s goto %s\n" % (L_this, str(parameters["布尔表达式"]["t"]), L_true)
        code += "goto %s\n" % L_false
        code += "%s: %s" % (L_true, str(parameters["函数块"]["code"]))
        code += "goto %s\n" % L_this
        code += "%s: " % L_false
        return {"code": code}

    # 分支（无else）
    elif left == "函数块" and right == ["if", "(", "布尔表达式", ")", "{", "函数块", "}"]:
        L_true = get_L(L_table)
        L_false = get_L(L_table)

        code = "%s" % (str(parameters["布尔表达式"]["code"]))
        code += "(if)if %s goto %s\n" % (str(parameters["布尔表达式"]["t"]), L_true)
        code += "goto %s\n" % L_false
        code += "%s: %s" % (L_true, str(parameters["函数块"]["code"]))
        code += "%s: " % L_false
        return {"code": code}

    # 分支（有else）
    elif left == "函数块" and right == ["if", "(", "布尔表达式", ")", "{", "函数块", "}", "else", "{", "函数块", "}"]:
        L_true = get_L(L_table)
        L_false = get_L(L_table)
        L_next = get_L(L_table)

        code = "%s" % (str(parameters["布尔表达式"]["code"]))
        code += "(if else)if %s goto %s\n" % (str(parameters["布尔表达式"]["t"]), L_true)
        code += "goto %s\n" % L_false
        code += "%s: %s" % (L_true, str(parameters["函数块"]["code"]))
        code += "goto %s\n" % L_next
        code += "%s: %s" % (L_false, str(parameters["函数块2"]["code"]))
        code += "%s: " % L_next
        return {"code": code}

    elif left == "变量类型":
        return {"name": right[0]}
    # 算术表达式部分
    elif left == "算术表达式" and right == ["算术表达式", "算术运算符", "算术表达式"]:
        # 类型检测
        # 特殊情况：某个算术表达式的t是数字
        t1 = parameters["算术表达式"]["t"]
        t2 = parameters["算术表达式2"]["t"]
        if t1[0].isdigit():
            if t1.find('.') > 0:
                type1 = "float"
            else:
                type1 = "int"
        else:
            type1 = id_table[t1]["type"]
        if t2[0].isdigit():
            if t2.find('.') > 0:
                type2 = "float"
            else:
                type2 = "int"
        else:
            type2 = id_table[t2]["type"]

        if type1 != type2:
            print("错误：%s %s %s 类型不同" % (
                str(parameters["算术表达式"]["t"]), str(parameters["算术运算符"]["name"]), str(parameters["算术表达式2"]["t"])))
        t = get_t(id_table, type1)

        code = "%s%s" % (str(parameters["算术表达式"]["code"]), str(parameters["算术表达式2"]["code"]))
        code += "%s = %s %s %s\n" % (t,
                                     str(parameters["算术表达式"]["t"]), str(parameters["算术运算符"]["name"]),
                                     str(parameters["算术表达式2"]["t"]))
        return {"code": code, "t": t}

    elif left == "算术表达式" and right == ["-", "算术表达式"]:

        t = get_t(id_table, id_table[parameters["算术表达式"]["t"]]["type"])
        code = "%s" % str(parameters["算术表达式"]["code"])
        code += "%s = - %s\n" % (t, str(parameters["算术表达式"]["t"]))
        return {"code": code, "t": t}
    elif left == "算术表达式" and right == ["(", "算术表达式", ")"]:
        return {"code": parameters["算术表达式"]["code"], "t": parameters["算术表达式"]["t"]}
    elif left == "算术表达式" and right == ["id"]:
        t = parameters["id"]["name"]
        code = ""
        return {"code": code, "t": t}
    elif left == "算术表达式" and right == ["digit"]:
        t = parameters["digit"]["name"]
        code = ""
        return {"code": code, "t": t}
    # 布尔表达式部分
    elif left == "布尔表达式" and right == ["算术表达式", "比较运算符", "算术表达式"]:
        # 类型检测
        # 特殊情况：某个算术表达式的t是数字
        t1 = parameters["算术表达式"]["t"]
        t2 = parameters["算术表达式2"]["t"]
        if t1[0].isdigit():
            if t1.find('.') > 0:
                type1 = "float"
            else:
                type1 = "int"
        else:
            type1 = id_table[t1]["type"]
        if t2[0].isdigit():
            if t2.find('.') > 0:
                type2 = "float"
            else:
                type2 = "int"
        else:
            type2 = id_table[t2]["type"]

        if type1 != type2:
            print("错误：%s %s %s 类型不同" % (
                str(parameters["算术表达式"]["t"]), str(parameters["比较运算符"]["name"]), str(parameters["算术表达式2"]["t"])))
        t = get_t(id_table, type1)
        code = "%s%s" % (str(parameters["算术表达式"]["code"]), str(parameters["算术表达式2"]["code"]))
        code += "%s = %s %s %s\n" % (
            t, str(parameters["算术表达式"]["t"]), str(parameters["比较运算符"]["name"]), str(parameters["算术表达式2"]["t"]))
        return {"code": code, "t": t}
    elif left == "布尔表达式" and right == ["布尔表达式", "&&", "布尔表达式"]:
        t = get_t(id_table, "bool")
        code = "%s%s" % (str(parameters["布尔表达式"]["code"]), str(parameters["布尔表达式2"]["code"]))
        code += "%s = %s && %s\n" % (t, str(parameters["布尔表达式"]["t"]), str(parameters["布尔表达式2"]["t"]))
        return {"code": code, "t": t}
    elif left == "布尔表达式" and right == ["布尔表达式", "||", "布尔表达式"]:
        t = get_t(id_table, "bool")
        code = "%s%s" % (str(parameters["布尔表达式"]["code"]), str(parameters["布尔表达式2"]["code"]))
        code += "%s = %s || %s\n" % (t, str(parameters["布尔表达式"]["t"]), str(parameters["布尔表达式2"]["t"]))
        return {"code": code, "t": t}
    elif left == "布尔表达式" and right == ["!", "布尔表达式"]:
        t = get_t(id_table, "bool")
        code = "%s" % str(parameters["布尔表达式"]["code"])
        code += "%s = ! %s\n" % (t, str(parameters["布尔表达式"]["t"]))
        return {"code": code, "t": t}
    elif left == "布尔表达式" and right == ["(", "布尔表达式", ")"]:
        return {"code": parameters["布尔表达式"]["code"], "t": parameters["布尔表达式"]["t"]}
    elif left == "布尔表达式" and right == ["true"]:
        t = get_t(id_table, "bool")
        code = "%s = true\n" % t
        return {"code": code, "t": t}
    elif left == "布尔表达式" and right == ["false"]:
        t = get_t(id_table, "bool")
        code = "%s = false\n" % t
        return {"code": code, "t": t}
    elif left == "比较运算符":
        return {"name": right[0]}
    elif left == "算术运算符":
        return {"name": right[0]}


# 给生成的中间代码加上行标号
def add_line():
    filename = '9.中间代码.txt'
    fp_read = open(filename, 'r', encoding='UTF-8')
    lines = fp_read.readlines()
    length = len(lines)
    L_dict = {}
    # 第一遍扫描，找到所有L对应的行数，建立字典
    for i in range(length):
        if lines[i][0] == 'L':
            j = 1
            while lines[i][j].isdigit():
                j += 1
            if lines[i][j] == ':':
                words = lines[i].split(' ')
                lines[i] = ""
                for word in words:
                    if ':' in word:
                        L = word.strip(':')
                        L_dict[L] = i + 1
                    else:
                        lines[i] += word + ' '
                # print(lines[i])

    # 第二遍扫描，替换所有L，并添加行号
    for i in range(length):
        if "goto" in lines[i]:
            start = lines[i].find("goto") + 5
            end = start + 1
            while lines[i][end].isdigit():
                end += 1
            L = lines[i][start: end]
            number = L_dict[L]
            lines[i] = lines[i][0: start] + str(number) + "\n"
        lines[i] = (str(i + 1) + ": " + lines[i]).strip(' ')

    fp_read.close()

    fp_write = open(filename, 'w', encoding='UTF-8')
    fp_write.writelines(lines)


def main():
    filename = "2.表达式_测试.txt"
    G = 语法分析.get_G(filename)

    action, goto = 语法分析.get_SLR1_table(G)

    token = 词法分析.process_2('0.源代码.txt')

    root = 语法分析.LR_analysis(G, action, goto, token)
    id_table = {}
    L_table = []
    translate(root, id_table, L_table)
    add_line()


if __name__ == '__main__':
    main()
