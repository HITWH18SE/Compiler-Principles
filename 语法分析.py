import copy
import 词法分析


# 产生式
class Product:
    def __init__(self, left, right):
        self.left = left
        self.right = right


# LR(0)项目，即带圆点的产生式
# 三个变量分别表示产生式左部、右部和圆点坐标（在对应坐标字符的左侧）
class Item:
    def __init__(self, left, right, index):
        self.left = left
        self.right = right
        self.index = index


# 以标准格式打印LR(0)项目集
def print_item(I):
    for item in I:
        right = ""
        for i in range(0, len(item.right)):
            if i == item.index:
                right += "."
            right += item.right[i] + " "
        if item.index >= len(item.right):
            right += "."
        print(str(item.left) + " -> " + right)


# 求G的所有FIRST(X)，X∈(V U T)
def get_FIRST(G):
    # 初始化
    FIRST = {}
    # 去掉S'
    temp_V = set(G['V'])
    temp_V.discard(G['S'] + "'")

    for X in temp_V:
        FIRST[X] = []
    for X in G['T']:
        FIRST[X] = [X]
    # print("FIRST:" + str(FIRST))

    # 第一阶段处理
    for product in G['P']:
        X = product.left
        if "ε" in product.right:
            FIRST[X].append("ε")
        if product.right[0] in G['T']:
            FIRST[X].append(product.right[0])
    # print("After 1, FIRST:" + str(FIRST))

    # 第二阶段处理，对于V中所有非终结符X，循环增加其FIRST集
    flag_change = True
    while flag_change:
        flag_change = False
        for product in G['P']:
            # print()
            X = product.left
            Y = product.right
            # print("X = " + X + ", Y = " + str(Y))
            # if (X→Y…∈P and Y∈V) then FIRST(X):= FIRST(X)∪(FIRST(Y)-{ε})
            if Y[0] in G['V']:
                # print(Y[0] + " in V : {")
                if union_FIRST_or_FOLLOW(FIRST, X, Y[0], True):
                    flag_change = True
                # print("}")
                # print("after FIRST[X} = " + str(FIRST[X]))

            # if (X→Y1…Yn∈P and Y1...Yi-1→ε) then for k=2 to i do FIRST(X):= FIRST(X)∪(FIRST(Yk)-{ε})
            if len(Y) == 1:
                continue
            # 产生式右部全部都是非终结符
            else:
                # print(str(Y) + " all in V : {")
                flag_epsilon = False
                # 把右部的非终结符里能推导出ε的FIRST集去掉ε之后添加到FIRST(X)中
                for y in Y:
                    # print("y = " + y)
                    flag_epsilon = False

                    if "ε" in FIRST[y]:
                        # print(y + " → ε")
                        flag_epsilon = True
                        if union_FIRST_or_FOLLOW(FIRST, X, y, True):
                            flag_change = True
                        # print("after FIRST[X} = " + str(FIRST[X]))
                    # 如果当前这个非终结符推不出ε，若之后还有终结符，就再来最后一次，否则就停止循环
                    if not flag_epsilon:
                        # print(y + " can't → ε")
                        if union_FIRST_or_FOLLOW(FIRST, X, y, True):
                            flag_change = True
                        # print("after FIRST[X} = " + str(FIRST[X]))
                        break

                # 如果右部每一个非终结符都能推出ε，就给FIRST(X)加上ε
                if flag_epsilon:
                    # print(str(Y) + " all → ε")
                    if union_FIRST_or_FOLLOW(FIRST, X, "ε", False):
                        flag_change = True

                # print("}")

    return FIRST


# 求两个FIRST或FOLLOW的并集，并返回该并集是否比原本的左侧集合更大，参数except_epsilon指示是否需要减去{ε}，求FIRST集需要用到
def union_FIRST_or_FOLLOW(F, X, Y, except_epsilon):
    set_X = set(F[X])
    if Y == "ε":
        set_Y = set("ε")
    else:
        set_Y = set(F[Y])
    # print("%s" % (str(set_X)) + " + ", end='')
    # print("%s" % (str(set_Y)), end="")
    if except_epsilon:
        set_Y.discard("ε")
        # print(" -  {ε} ", end="")
    before = len(F[X])
    F[X] = list(set_X.union(set_Y))
    # print("= %s" % (str(F[X])))
    after = len(F[X])
    if before < after:
        return True
    else:
        return False


# 求G的所有FIRST(a)，a∈(V U T)*，a = X1X2X3...Xn
# 如果之前没有记录过对应的FIRST(a)，就将其添加到FIRST集中
def get_FIRST_alpha(FIRST, a):
    # 如果a是单个非终结符或者终结符，则FIRST集中已经存在，直接返回即可
    if len(a) == 1:
        # α=ε的特殊情况，特殊处理
        if "ε" in a:
            FIRST["ε"] = ["ε"]
        return FIRST[a[0]]
    # 如果a是多个非终结符或终结符的集合，就开始运行算法求解FIRST(a)
    string_a = ""
    for X in a:
        string_a = string_a + X + " "
    string_a = string_a.strip()
    FIRST[string_a] = []

    flag_epsilon = False
    for X in a:
        flag_epsilon = False
        if "ε" in FIRST[X]:
            flag_epsilon = True
            union_FIRST_or_FOLLOW(FIRST, string_a, X, True)
        if not flag_epsilon:
            union_FIRST_or_FOLLOW(FIRST, string_a, X, True)
            break
    # 如果X1-Xn都能推出ε，就把ε也添加到FIRST中
    if flag_epsilon:
        union_FIRST_or_FOLLOW(FIRST, string_a, "ε", False)
    return FIRST[string_a]


# 求G的所有FOLLOW(X)
def get_FOLLOW(G):
    filename = '5.FIRST集与FOLLOW集.txt'
    write = open(filename, 'w', encoding='UTF-8')
    # 获取FIRST集，并输出到文件
    FIRST = get_FIRST(G)

    print("FIRST:", file=write)
    keys = FIRST.keys()
    for k in keys:
        print(str(k) + ": " + str(FIRST[k]), file=write)



    # 初始化
    FOLLOW = {}
    # 去掉S'
    temp_V = set(G['V'])
    temp_V.discard(G['S'] + "'")
    for X in temp_V:
        FOLLOW[X] = []
    FOLLOW[G['S']].append("#")

    # 第二阶段处理，A→αBβ
    flag_change = True
    while flag_change:
        flag_change = False
        for product in G['P']:
            # print()
            A = product.left
            Y = product.right
            for i in range(0, len(Y)):
                B = Y[i]
                # 如果B不是非终结符，则继续循环直到找到非终结符
                if B not in G['V']:
                    continue
                # 判断B后面是否还有β
                if i == len(Y) - 1:
                    flag_change = union_FIRST_or_FOLLOW(FOLLOW, B, A, False)
                else:
                    beta = Y[i+1:]
                    FIRST_beta = get_FIRST_alpha(FIRST, beta)
                    # 如果ε∈FIRST(β)
                    if "ε" in FIRST_beta:
                        flag_change = union_FIRST_or_FOLLOW(FOLLOW, B, A, False)

                    set_B = set(FOLLOW[B])
                    set_beta = set(FIRST_beta)
                    # print("%s" % (str(set_B)) + " + ", end='')
                    # print("%s" % (str(set_beta)), end="")
                    set_beta.discard("ε")
                    # print(" -  {ε} ", end="")
                    before = len(FOLLOW[B])
                    FOLLOW[B] = list(set_B.union(set_beta))
                    # print("= %s" % (str(FOLLOW[B])))
                    after = len(FOLLOW[B])
                    if before < after:
                        flag_change = True
    # 输出FOLLOW至文件
    print("\nFOLLOW:", file=write)
    keys = FOLLOW.keys()
    for k in keys:
        print(str(k) + ": " + str(FOLLOW[k]), file=write)

    return FOLLOW


# 求I的闭包
def CLOSURE(G, I):
    J = copy.copy(I)
    for item in J:
        if item.index >= len(item.right):
            continue
        B = item.right[item.index]
        # print("B = " + str(B))
        if B in G['V']:
            for product in G['P']:
                if product.left == B:
                    temp = Item(product.left, product.right, 0)
                    if not item_in_set(temp, J):
                        J.append(temp)
    return J


# 判断某个LR(0)项目是否在某个项目集中，求闭包时需要用到
def item_in_set(item, set):
    for i in set:
        if item.left == i.left and item.right == i.right and item.index == i.index:
            return True
    return False


# 项目集的转移函数（求出项目集I关于非终结符X的后继项目集）
def GO(G, I, X):
    J = []
    for item in I:
        if item.index >= len(item.right):
            continue
        B = item.right[item.index]
        if B == X:
            if B in G['V'] or B in G['T']:
                J.append(Item(item.left, item.right, item.index + 1))
    # print("J : ")
    # print_item(J)
    return CLOSURE(G, J)


# 输入文法G'，计算LR(0)项目集规范族C
def get_LR0_collection(G):
    C = []
    I = []
    I.append(Item(G['P'][0].left, G['P'][0].right, 0))
    C.append(CLOSURE(G, I))
    V_or_T = G['V'] + G['T']
    # print("V or T:"+str(V_or_T))
    for I in C:
        for X in V_or_T:
            J = GO(G, I, X)
            # 如果J不为空集
            if len(J) > 0:
                # 判断J是否在C中
                flag = True
                for K in C:
                    if set_equal(J, K):
                        flag = False
                # 如果J不在C中，则将其添加到C中
                if flag:
                    C.append(J)

    # 输出LR0项目集规范族到文件
    filename = '4.LR(0)项目集规范族.txt'
    write = open(filename, 'w', encoding='UTF-8')
    for i in range(len(C)):
        print("I(" + str(i) + "):", file=write)
        for item in C[i]:
            right = ""
            for i in range(0, len(item.right)):
                if i == item.index:
                    right += ". "
                right += item.right[i] + " "
            if item.index >= len(item.right):
                right += "."
            print(item.left + " -> " + right, file=write)
        print("", file=write)

    return C


# 判断两个项目集是否相等，求项目集规范族需要用到
def set_equal(A, B):
    n1 = len(A)
    n2 = len(B)
    if n1 != n2:
        return False
    for i in range(n1):
        if not item_equal(A[i], B[i]):
            return False
    return True


# 判断两个LR(0)项目集是否相等，求两个项目集相等需要用到
def item_equal(a, b):
    if a.left == b.left and a.right == b.right and a.index == b.index:
        return True
    return False


# 输入文法G的拓广文法G'，获取LRO分析表
def get_LRO_table(G):
    # 先获取LR0项目集规范族
    C = get_LR0_collection(G)

    n = len(C)
    action = [["" for i in range(len(G['T']) + 1)] for i in range(n)]
    goto = [["" for i in range(len(G['V']))] for i in range(n)]
    for k in range(n):
        I = C[k]
        for item in I:
            # 圆点不在右部表达式的最右侧，即还不需要归约
            if item.index < len(item.right):
                character = item.right[item.index]
                # 找出满足GO(I, character)=C[j]的j
                for j in range(n):
                    if set_equal(GO(G, I, character), C[j]):
                        # 如果character是终结符
                        if character in G['T']:
                            # 在action表里添加状态转移以及当前符号压入栈的提示
                            action[k][G['T'].index(character)] = "S" + str(j)
                        # 如果是非终结符
                        else:
                            # 在goto表里添加状态转移提示
                            goto[k][G['V'].index(character)] = str(j)
                        break
            # 圆点在右部表达式的最右侧，即需要归约
            else:
                # 如果该表达式是S'->S，则在action表里添加acc
                if item.left == G['S'] + "'":
                    action[k][len(action[k]) - 1] = "acc"
                    continue
                # 否则，找到P中对应的产生式序号
                m = len(G['P'])
                for j in range(1, m):
                    if G['P'][j].left == item.left and G['P'][j].right == item.right:
                        for a in range(len(G['T']) + 1):
                            action[k][a] = "r" + str(j)
    return action, goto


# 输入文法G的拓广文法G'，获取SLR(1)分析表
# 目前还有一个问题，要在函数内部生成G'，或者调整一下goto表的生成规则，否则会把E'也弄进去（已解决）
def get_SLR1_table(G):
    # 这里的G还是非拓广文法
    FOLLOW = get_FOLLOW(G)

    # 求G的拓广文法G'的LR0项目集
    G['P'].insert(0, Product(G['S'] + "'", [G['S']]))
    G['V'].insert(0, G['S'] + "'")
    C = get_LR0_collection(G)

    # action和goto表的初始化
    n = len(C)
    row = {}
    for t in G['T']:
        row[t] = ""
    row["#"] = ""
    action = []
    for i in range(n):
        action.append(copy.copy(row))

    temp_V = set(G['V'])
    temp_V.discard(G['S'] + "'")
    # print("temp_V = " + str(temp_V))
    row = {}
    for v in temp_V:
        row[v] = ""
    goto = []
    for i in range(n):
        goto.append(copy.copy(row))

    for k in range(n):
        I = C[k]
        for item in I:
            # 圆点不在右部表达式的最右侧，即还不需要归约
            if item.index < len(item.right):
                character = item.right[item.index]
                # 找出满足GO(I, character)=C[j]的j
                for j in range(n):
                    if set_equal(GO(G, I, character), C[j]):
                        # 如果character是终结符
                        if character in G['T']:
                            # 在action表里添加状态转移以及当前符号压入栈的提示
                            action[k][character] = "S" + str(j)
                        # 如果是非终结符
                        else:
                            # 在goto表里添加状态转移提示
                            # 这里index-1是因为S'被去掉了
                            goto[k][character] = str(j)
                        break
            # 圆点在右部表达式的最右侧，即需要归约
            else:
                # 如果该表达式是S'->S，则在action表里添加acc
                if item.left == G['S'] + "'":
                    action[k]["#"] = "acc"
                    continue
                # 否则，找到P中对应的产生式序号
                m = len(G['P'])
                for j in range(1, m):
                    if G['P'][j].left == item.left and G['P'][j].right == item.right:
                        FOLLOW_A = FOLLOW[item.left]
                        # print("FOLLOW(A) = " + str(FOLLOW_A))
                        for t in G['T']:
                            if t in FOLLOW_A:
                                action[k][t] = "r" + str(j)
                        if "#" in FOLLOW_A:
                            action[k]["#"] = "r" + str(j)
                        break

    # 输出action和goto表到文件
    filename = '6.SLR(1)分析表.txt'
    write = open(filename, 'w', encoding='UTF-8')
    print("action:", file=write)
    print("[", end='', file=write)
    i = 0
    T = G['T']
    for t in T:
        print(str(i) + ": " + str(t), end=", ", file=write)
        i += 1
    print("#]", file=write)
    i = 0
    for row in action:
        print(str(i) + str(row), file=write)
        i += 1

    print("", file=write)
    print("goto:", file=write)
    V = G['V']
    for i in range(1, len(V)):
        print(str(V[i]), end="  ", file=write)
    i = 0
    for row in goto:
        print(str(i) + str(row), file=write)
        i += 1

    return action, goto


# 语法分析树的结点
class Node:
    def __init__(self, character, token=None):
        self.child = []
        self.character = character
        self.token = token

    def add_child(self, node):
        self.child.append(node)


# 打印树的所有结点到文件
def print_Node(node, write, h):
    for i in range(h):
        print("|\t", end="", file=write)
    print(node.character, file=write)
    for c in node.child:
        print_Node(c, write, h+1)


# 输入文法G、SLR(1)的action与goto分析表、词法分析得到的token串，输出LR分析结果以及对应的语法分析树至文件
def LR_analysis(G, action, goto, token):
    filename = '7.LR分析过程.txt'
    write = open(filename, 'w', encoding='UTF-8')

    # id表
    # id_table = {}

    # 结点栈
    stack_node = []

    # 状态栈
    stack_state = [0]
    # 符号栈
    stack_character = ["#"]
    # 输入缓冲区
    buffer = []
    for t in token:
        if t[1] == "标识符":
            buffer.append("id")
            # if t[0] not in id_table.keys():
            #     id_table[t[0]] = {}

        elif t[1] == "浮点数" or t[1] == "整数":
            buffer.append("digit")
        else:
            buffer.append(str(t[0]))
    buffer.append("#")
    # print("buffer = " + str(buffer))
    # 用于记录输入缓冲区当前下标的变量
    ip = 0
    while True:
        print("", file=write)
        print("状态栈: " + str(stack_state), file=write)
        print("符号栈: " + str(stack_character), file=write)
        if ip >= len(buffer):
            break

        # 获得栈顶状态S以及ip指向的符号a
        S = stack_state[len(stack_state)-1]
        a = buffer[ip]

        print("输入缓冲区: ", end="", file=write)
        input = buffer[ip:]
        for c in input:
            print(c, end=" ", file=write)
        print("", file=write)

        # 获取SLR1分析表中对应的字符串
        string = action[S][a]
        print("分析表内容: " + string, file=write)
        print("当前动作: ", end="", file=write)
        # 出错
        if string == '':
            print("分析出错")
            print("分析出错", file=write)
            return
        # 需要转移至状态i，并且把a压入栈中
        elif string[0] == 'S':
            i = int(string[1:])
            print("移进状态%s，输入符号%s" % (str(i), a), file=write)
            stack_character.append(a)
            stack_state.append(i)

            stack_node.append(Node(a, token[ip]))  # 结点入栈
            ip = ip + 1

        # 需要根据G中第k条产生式归约，两个栈各弹出n个符号，最后再查询goto表将新的状态压入状态栈
        elif string[0] == 'r':
            k = int(string[1:])
            n = len(G['P'][k].right)
            print("按第%s个产生式归约: " % str(k) + str(G['P'][k].right) + " -> " + G['P'][k].left, end="", file=write)
            A = G['P'][k].left

            # 归约以后弹出n个符号
            stack_state = stack_state[0: len(stack_state)-n]
            stack_character = stack_character[0: len(stack_character)-n]

            # 查询goto表，将新的状态压入状态栈
            S = stack_state[len(stack_state) - 1]
            stack_state.append(int(goto[S][A]))
            print("，将状态%s压入栈中" % str(goto[S][A]), file=write)
            stack_character.append(A)

            # 结点栈弹出n个结点，并生成它们的父结点，再将父结点压入栈
            child_nodes = stack_node[len(stack_node) - n:]
            stack_node = stack_node[0: len(stack_node) - n]
            father = Node(A)
            # print("father = " + father.character)
            for c in child_nodes:
                father.add_child(c)
            stack_node.append(father)

        # 分析成功
        elif string == "acc":
            print("SLR(1)分析成功，语法分析部分结束")
            print("分析成功", file=write)

            filename = '8.语法分析树.txt'
            write = open(filename, 'w', encoding='UTF-8')
            root = stack_node[0]
            print_Node(stack_node[0], write, 0)
            return root
            # return root, id_table


# 读取表达式，自动生成集合P，并且自动生成文法G
# 表达式需要满足规则，出现在左侧的都是非终结符V，剩下的都是终结符T以及ε，开始符号S是第一条表达式的左部（全部用空格隔开）
def get_G(filename):
    fp_read = open(filename, 'r', encoding='UTF-8')
    lines = fp_read.readlines()

    result_filename = '3.文法G.txt'
    write = open(result_filename, 'w', encoding='UTF-8')

    P = []
    V = []
    T = []
    # 记录出现过的所有字符
    characters = []

    print("P : ", file=write)
    length = len(lines)
    for i in range(length):
        lines[i] = lines[i].replace('\n', '')
        if not lines[i]:
            continue
        if "#" in lines[i]:
            continue
        print(lines[i], file=write)
        k = lines[i].index("->")
        left = lines[i][0:k-1]
        right = lines[i][k+3:]
        right = right.split(" ")
        # print("left:" + left)
        # print("right:" + str(right))
        P.append(Product(left, right))
        if left not in V:
            V.append(left)

    for i in range(len(P)):
        right = P[i].right
        for c in right:
            if c not in V and c not in T and c != 'ε':
                T.append(c)

    S = P[0].left

    print("", file=write)
    print("V : ", end="", file=write)
    for v in V:
        print(str(v), end="  ", file=write)
    print("", file=write)
    print("T : ", end="", file=write)
    for t in T:
        print(str(t), end="  ", file=write)
    print("", file=write)
    print("S : " + str(S), file=write)

    G = {'V': V, 'T': T, 'P': P, 'S': S}
    return G


def main():
    filename = "2.表达式_简单加法与乘法.txt"
    G = get_G(filename)

    action, goto = get_SLR1_table(G)

    token = 词法分析.process_2('0.源代码.txt')

    root = LR_analysis(G, action, goto, token)


# main()