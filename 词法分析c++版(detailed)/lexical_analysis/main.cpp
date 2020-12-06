#include<iostream>
#include<fstream>
#include<cstdio>
#include<cstring>
#include<string>
#include<cstdlib>

using namespace std;

/*
1：标识符
2：数字
3：算数运算符 + - *
4：关系运算符 <=、  >=、  !=、  == =、 <、>
5：保留字(32)
auto       break    case     char        const      continue
default    do       double   else        enum       extern
float      for      goto     if          int        long
register   return   short    signed      sizeof     static
struct     switch   typedef  union       unsigned   void
volatile    while
6：界符
*/

int seekresult;        //fseek的时候用来接着的
string word = "";        //字符串,当前词
char ch;            //每次读进来的一个字符
int num = 0;            //每个单词中当前字符的位置
int line = 1;            //行数
int col = 1;            //列数
bool flag;            //文件是否结束扫描
int type;            //单词的类型

//保留字表
static char ReserveWord[32][20] = {
        "auto", "break", "case", "char", "const", "continue",
        "default", "do", "double", "else", "enum", "extern",
        "float", "for", "goto", "if", "int", "long",
        "register", "return", "short", "signed", "sizeof", "static",
        "struct", "switch", "typedef", "union", "unsigned", "void",
        "volatile", "while"
};

//算术运算符表
static char ArithmeticOperator[4][4] = {
        "+", "-", "*", "/"
};
//逻辑运算符表
static char RelationalOperator[7][4] = {
        "<", "<=", ">", ">=", "=", "==", "!="
};
//界符表(12)
static char Boundary[36][4] = {
        ";", "(", ")", "^", ",", "#", "%", "[", "]", "{", "}", "."
};

//标识符表
char IdentifierTable[1000][40] = {};

//常数表
char DigitBTable[1000][40] = {};

int Inum = 0;

int Dnum = 0;


//判断是否是：字母
bool Isletter(char x) {
    return (x >= 'a' && x <= 'z') || (x >= 'A' && x <= 'Z');
}

//判断是否是：数字
bool IsDigit(char x) {
    return x >= '0' && x <= '9';
}

//判断是否是：界符
bool IsBoundary(char x) {
    int i = 0;
    int temp = 0;
    for (i = 0; i < 14; i++) {
        if (x == Boundary[i][0]) {
            temp = 1;
            break;
        }
    }
    return temp == 1;
}

//判断是否是 算数运算符：加减乘
bool IsArithmetic(char x) {
    return x == '+' || x == '-' || x == '*';
}

//判断是否是 关系运算符：等于（赋值），大于小于（大于等于，小于等于，大于小于）
bool IsRelational(char x) {
    return x == '=' || x == '<' || x == '>';
}

//从文件里读一个单词
int Scanner(FILE *fp) {
    //先读一个字符，赋值给ch
    ch = fgetc(fp);

    //处理空白字符
    if (feof(fp)) {
        flag = 0;
        return 0;
    } else if (ch == ' ') {
        col++;
        return 0;
    } else if (ch == '\n') {
        line++;
        col = 1;
        return 0;
    }
        //如果是字母开头或 '_' 看关键字还是标识符
    else if (Isletter(ch) || ch == '_') {
        word += ch;
        col++;
        while ((ch = fgetc(fp)) && (Isletter(ch) || IsDigit(ch) || ch == '_')) {
            word += ch;
            col++;
        }
        //文件读完，返回true
        if (feof(fp)) {
            flag = 0;
            return 1;
        }
        //检验是否是保留字
        for (int i = 1; i <= 32; i++) {
            if (word == ReserveWord[i]) {
                //SEEK_CUR当前位置，fseek函数作用：文件位置指针从当前位置位移一个位置
                seekresult = fseek(fp, -1, SEEK_CUR);
                //4+i：保留字
                return 4 + i;
            }
        }
        //检查是否是标识符
        for (int Ii = 0; Ii < Inum; Ii++) {
            if (Inum != 0 && strcmp(IdentifierTable[Ii], word.c_str()) == 0) {
                seekresult = fseek(fp, -1, SEEK_CUR);
                //1：标识符
                //return 1;
                return 1000 + Ii + 1;
            }
        }
        strcpy(IdentifierTable[Inum], word.c_str());
        Inum = Inum + 1;

        //写追加
        ofstream Arithmetic_operator;
        Arithmetic_operator.open("IdentifierTable.txt", ios::app);
        Arithmetic_operator << word << " " << endl;
        Arithmetic_operator.close();

        seekresult = fseek(fp, -1, SEEK_CUR);
        //1：标识符
        return 1000 + Inum;
    }

        //开始是加减乘，一定是算数运算符3
    else if (IsArithmetic(ch)) {
        word += ch;
        col++;
        //3：算数运算符
        return 3;
    }

        //开始是数字就一定是数字2
    else if (IsDigit(ch)) {
        word += ch;
        col++;
        while ((ch = fgetc(fp)) && IsDigit(ch)) {
            word += ch;
            col++;
        }
        int Di = 0;
        for (Di = 0; Di < Inum; Di++) {
            if (Dnum != 0 && strcmp(DigitBTable[Di], word.c_str()) == 0) {
                seekresult = fseek(fp, -1, SEEK_CUR);
                //2：数字
                return 2000 + Di + 1;
            }
        }
        strcpy(DigitBTable[Dnum], word.c_str());
        Dnum = Dnum + 1;
        //写追加
        ofstream Arithmetic_operator;
        Arithmetic_operator.open("DigitBTabl.txt", ios::app);
        Arithmetic_operator << word << " " << endl;
        Arithmetic_operator.close();


        seekresult = fseek(fp, -1, SEEK_CUR);
        //2：数字
        return 2000 + Dnum;
    }

        //检验界符6
    else if (IsBoundary(ch)) {
        int Ji;
        for (Ji = 0; Ji < 12; Ji++) {
            if (ch == Boundary[Ji][0]) {
                break;
            }
        }
        word += ch;
        col++;
        //32+5+i：界符
        return (32 + 5 + Ji);
    }

        //检验关系运算符4 ：<=、>=、!=、==、 < 、>
    else if (IsRelational(ch)) {
        col++;
        word += ch;
        //检验  != <=
        if (ch == '<') {
            ch = fgetc(fp);
            if (ch == '>' || ch == '=') {
                word += ch;
                col++;
                return 4;
            }
        }
            //检验  >= ==
        else {
            ch = fgetc(fp);
            // 赋值运算符
            if (ch == '=') {
                word += ch;
                col++;
                return 4;
            }
        }
        if (feof(fp)) {
            flag = 0;
        }
        seekresult = fseek(fp, -1, SEEK_CUR);
        //3:算数运算符
        return 3;
    }

        //首字符是 / 有可能是除号 也有可能是注释
    else if (ch == '/') {
        col++;
        word += ch;
        ch = fgetc(fp);
        //这种情况是除号
        if (ch != '*' && ch != '/') {
            seekresult = fseek(fp, -1, SEEK_CUR);
            //3:算数运算符
            return 3;
        }
        //注释符//：这一行剩下的全被注释了
        if (ch == '/') {
            word.clear();
            while ((ch = fgetc(fp)) && ch != '\n' && !feof(fp)) {}
            if (feof(fp)) {
                flag = 0;
                return 0;
            } else {
                seekresult = fseek(fp, -1, SEEK_CUR);
            }
            line++;
            col = 1;
            return 0;
        }
        if (ch == '*') {
            bool flag5 = 1;
            while (flag5) {
                word.clear();
                ch = fgetc(fp);
                col++;
                if (ch == '\n') {
                    line++;
                    col = 1;
                }
                if (ch != '*')
                    continue;
                else {
                    ch = fgetc(fp);
                    col++;
                    if (ch == '\n') {
                        line++;
                        col = 1;
                    }
                    if (ch == '/') {
                        flag5 = 0;
                    } else continue;
                }
                if (feof(fp)) {
                    flag = 0;
                    return 0;
                }
            }
        }
    } else {
        word += ch;
        col++;
        return -1;
    }
}

int main() {
    FILE *fp;

    flag = 1;
    //打开源代码文件
    //未打开
    if ((fp = fopen("E:\\programming\\C++\\lab1111\\code.txt", "r")) == NULL) {
        cout << "Sorry,can't open this file." << endl;
        flag = 0;
    }
    //已打开
    while (flag == 1) {
        //反复调用扫描函数提取单词
        type = Scanner(fp);

        //1：标识符
        if (type > 1000 && type < 2000) {
            cout << "(" << word << "," << type - 1000 << " Identifier" << ")" << endl;
            if (word.length() > 20)
                cout << "ERROR Identifier length cannot exceed 20 characters" << endl;
            word.clear();
        }
        //2：数字
        else if (type > 2000) {
            cout << "(" << word << "," << (type - 2000) << " Digit" << ")" << endl;
            if (word[0] == '0')
                cout << "ERROR: The first digit cannot be 0!" << endl;
            word.clear();
        }
        //3：算数运算符 + - * /
        else if (type == 3) {
            cout << "(" << word << "," << "3 ArithmeticOperator" << ")" << endl;
            word.clear();
        }

            //4：关系运算符 <、<=、>、>=、= 、!=
        else if (type == 4) {
            cout << "(" << word << "," << "4 RelationalOperator" << ")" << endl;
            word.clear();
        }
            //5：5+32到5+32+11：界符
        else if (type >= 37) {
            cout << "(" << word << "," << "5 Boundary" << ")" << endl;
            word.clear();
        }
            //6：5 - 36：保留字
        else if (type >= 5 && type <= 36) {
            cout << "(" << word << "," << "6 ReservedWord" << ")" << endl;
            word.clear();
        }
            //7：非法字符
        else if (type == -1) {
            cout << "Illegal character   " << "line " << line << " col " << col - 1 << "  " << word << endl;
            word.clear();
        }
    }
    fclose(fp);

    return 0;
}