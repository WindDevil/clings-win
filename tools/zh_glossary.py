"""Chinese text for the Windows twin.

Upstream clings writes its exercise text in English.  The twin keeps the same
content but shows Chinese titles, objectives, hints and comments, because the
audience is Windows-first beginners who may not read English comfortably.

The mapping lives here instead of in the generated tree so that ``make sync``
can rebuild everything and ``make check`` can prove the translation is complete:
an upstream text change shows up as a missing entry rather than silently
reverting a comment to English.

Rules for the strings below:

* Identifiers, API names, format specifiers and file names stay in English
  (``printf``, ``sizeof``, ``malloc``, ``argv``, ``.c``), matching the code.
* ``TODO:`` stays as-is; it is a marker learners search for.
* Translate the meaning, not the English word order.
"""

from __future__ import annotations

# title: -> exercise titles, used in file headers, `clings list` and topic READMEs.
TITLES: dict[str, str] = {
    "#error, #line, and #pragma pack": "#error、#line 与 #pragma pack",
    "#include with a standard header": "用 #include 引入标准头文件",
    "#include with a user header": "用 #include 引入自己的头文件",
    "#undef and defined": "#undef 与 defined",
    "A singly linked list": "单向链表",
    "A small state machine": "一个小状态机",
    "Advanced printf formatting": "printf 格式化进阶",
    "Advanced scanf input": "scanf 输入进阶",
    "Alignment requirements": "对齐要求",
    "Allocate, initialize, and free": "分配、初始化与释放",
    "Allocation statistics": "分配统计",
    "Anonymous structs and unions": "匿名结构体与联合体",
    "Arena allocator": "区域分配器",
    "Array traversal": "遍历数组",
    "Array-to-pointer decay": "数组退化为指针",
    "Arrays of structs": "结构体数组",
    "Assertions and defensive programming": "断言与防御式编程",
    "Assignment versus equality": "赋值与相等",
    "Asymmetric bounds": "不对称边界",
    "Avoid signed integer overflow": "避免有符号整数溢出",
    "Binary random access": "二进制随机访问",
    "Binary search tree": "二叉查找树",
    "Binary, octal, and hexadecimal input": "二进制、八进制与十六进制输入",
    "Bitfields": "位域",
    "Bitfields and explicit masks": "位域与显式掩码",
    "Bitwise set, clear, toggle, and test": "位操作：置位、清位、取反与测试",
    "Bounded copying with strncpy": "用 strncpy 做有界拷贝",
    "Bounds checking": "边界检查",
    "Buffered output and memory allocation": "缓冲输出与内存分配",
    "C standard changes": "C 标准的变化",
    "C11 atomics": "C11 原子操作",
    "Character arrays": "字符数组",
    "Characters and ASCII": "字符与 ASCII",
    "Comments and escape sequences": "注释与转义序列",
    "Compile-time assertions": "编译期断言",
    "Complex declarations and function-pointer tables":
        "复杂声明与函数指针表",
    "Complex numbers": "复数",
    "Compound assignment and comma": "复合赋值与逗号运算符",
    "Compound literals": "复合字面量",
    "Conditional compilation": "条件编译",
    "Converting strings to double": "把字符串转成 double",
    "Dangling else": "悬挂 else",
    "Dangling pointers and safe free": "野指针与安全释放",
    "Declaration grammar and function-pointer tables":
        "声明文法与函数指针表",
    "Declarations and definitions": "声明与定义",
    "Default argument promotions": "默认实参提升",
    "Defining and using structs": "定义并使用结构体",
    "Dereference and address-of": "解引用与取地址",
    "Detecting a memory leak": "发现内存泄漏",
    "Dynamic array/vector": "动态数组（vector）",
    "Dynamic linking with LoadLibrary": "用 LoadLibrary 动态加载",
    "EOF, feof, and ferror": "EOF、feof 与 ferror",
    "Endianness": "字节序",
    "Enums": "枚举",
    "Environment variables": "环境变量",
    "Escaped strings and line continuation": "转义字符串与续行",
    "External linkage across files": "跨文件的外部链接",
    "External type checking": "外部类型检查",
    "Fixed-width integers and format macros": "定宽整数与格式宏",
    "Flexible array members": "柔性数组成员",
    "Floating-point bit patterns": "浮点数的位模式",
    "Floating-point comparison": "浮点数比较",
    "Free then realloc": "先 free 再 realloc",
    "Function pointers and dispatch": "函数指针与分派",
    "Function-like macros": "函数式宏",
    "Generic byte-level swap": "通用字节交换",
    "Growing an allocation": "扩大一块分配",
    "Header and source split": "头文件与源文件分离",
    "Identifier length": "标识符长度",
    "Implementation-defined behavior": "实现定义行为",
    "Implementing string operations": "自己实现字符串函数",
    "Include ctype.h": "引入 ctype.h",
    "Include guards": "头文件保护",
    "Include the I/O header": "引入 I/O 头文件",
    "Initialize before use": "先初始化再使用",
    "Input validation": "输入校验",
    "Integer arithmetic": "整数运算",
    "Integer bit patterns": "整数的位模式",
    "Integer promotions": "整型提升",
    "Integer types and ranges": "整数类型与取值范围",
    "Internal linkage and file-scope state": "内部链接与文件作用域状态",
    "Internal linkage and inline helpers": "内部链接与内联辅助函数",
    "Lexical maximal munch": "词法最长匹配",
    "Macro side effects": "宏的副作用",
    "Macros are not statements": "宏不是语句",
    "Macros are not type definitions": "宏不是类型定义",
    "Memory location zero": "地址 0",
    "Multiline macros": "多行宏",
    "NULL and const correctness": "NULL 与 const 正确性",
    "NULL, empty string, and NUL": "NULL、空串与 NUL",
    "Nested structs": "嵌套结构体",
    "Null pointer checks": "空指针检查",
    "Object-like macros": "对象式宏",
    "Octal integer constants": "八进制整型常量",
    "One-past pointer arithmetic": "越尾一个位置的指针运算",
    "POSIX threads and a mutex": "POSIX 线程与互斥量",
    "Padding and alignment": "填充与对齐",
    "Parameters and return values": "参数与返回值",
    "Pass by value and pass by pointer": "值传递与指针传递",
    "Passing structs by value and by pointer": "结构体：值传递与指针传递",
    "Pointer arithmetic": "指针运算",
    "Pointer compatibility and const": "指针兼容性与 const",
    "Pointers to arrays and &array": "数组指针与 &array",
    "Pointers to pointers": "指向指针的指针",
    "Precedence and parentheses": "优先级与括号",
    "Print a value": "打印一个值",
    "Print with printf": "用 printf 打印",
    "Pseudo-random numbers": "伪随机数",
    "Queue ADT": "队列抽象数据类型",
    "RAND_MAX portability": "RAND_MAX 的可移植性",
    "Random access with fseek and ftell": "用 fseek 和 ftell 随机访问",
    "Read compiler diagnostics": "读懂编译器诊断",
    "Read with scanf": "用 scanf 读输入",
    "Recursion and base cases": "递归与基准情形",
    "Registering atexit handlers": "注册 atexit 处理函数",
    "Respecting buffer bounds": "遵守缓冲区边界",
    "Robust integer parsing": "稳健地解析整数",
    "Safe formatting with snprintf": "用 snprintf 安全格式化",
    "Safe parsing with sscanf": "用 sscanf 安全解析",
    "Searching strings": "在字符串里查找",
    "Semicolon and empty-statement traps": "分号与空语句陷阱",
    "Sequence points": "序列点",
    "Shift operators and masks": "移位运算与掩码",
    "Short-circuit evaluation": "短路求值",
    "Signals and sig_atomic_t": "信号与 sig_atomic_t",
    "Signed and unsigned conversions": "有符号与无符号转换",
    "Stack frames": "栈帧",
    "Storage classes and scope": "存储类与作用域",
    "Stream buffering": "流缓冲",
    "String literals and mutable strings": "字符串字面量与可变字符串",
    "Stringizing and token pasting": "字符串化与记号拼接",
    "Tail recursion": "尾递归",
    "Text file I/O": "文本文件 I/O",
    "The math library": "数学库",
    "Thread-local storage": "线程局部存储",
    "Time arithmetic": "时间运算",
    "Tokenizing with strtok_r": "用 strtok_r 分词",
    "Two-dimensional arrays": "二维数组",
    "Type punning without strict-aliasing violations":
        "不做违反严格别名规则的类型双关",
    "Type qualifiers and storage-class specifiers": "类型限定符与存储类说明符",
    "Type-generic math with tgmath.h": "用 tgmath.h 做类型通用数学运算",
    "Unions share storage": "联合体共用存储",
    "Unsigned wrap and checked signed addition": "无符号回绕与带检查的有符号加法",
    "Use-after-free": "释放后使用",
    "Variable-length arrays": "变长数组",
    "Variadic functions": "变参函数",
    "Variadic macros": "变参宏",
    "Whitespace in macro definitions": "宏定义里的空白",
    "Writing and reading structs": "写入与读出结构体",
    "X-macros": "X-macro",
    "Zero-initialized allocation": "零初始化的分配",
    "_Generic selection": "_Generic 选择",
    "_Noreturn functions": "_Noreturn 函数",
    "alignof and alignas": "alignof 与 alignas",
    "argc, argv, and the program environment":
        "argc、argv 与程序运行环境",
    "atomic_flag spin lock": "atomic_flag 自旋锁",
    "break and continue": "break 与 continue",
    "char signedness": "char 的符号性",
    "ctype.h classification and conversion": "ctype.h 的字符分类与转换",
    "fgets and fputs": "fgets 与 fputs",
    "fgets, fputs, and sorting strings": "fgets、fputs 与字符串排序",
    "for and while loops": "for 与 while 循环",
    "fprintf and fscanf": "fprintf 与 fscanf",
    "getc and putc": "getc 与 putc",
    "getc, putc, and ungetc": "getc、putc 与 ungetc",
    "getchar and putchar": "getchar 与 putchar",
    "goto for single-exit cleanup": "用 goto 做单出口清理",
    "if and else": "if 与 else",
    "iso646.h alternative spellings": "iso646.h 的替代写法",
    "long double": "long double",
    "main return values": "main 的返回值",
    "memcpy, memmove, memset, and memcmp": "memcpy、memmove、memset 与 memcmp",
    "offsetof and container_of": "offsetof 与 container_of",
    "printf format specifiers": "printf 格式说明符",
    "qsort and bsearch": "qsort 与 bsearch",
    "restrict and aliasing contracts": "restrict 与别名约定",
    "setjmp and longjmp": "setjmp 与 longjmp",
    "sizeof and increment operators": "sizeof 与自增运算符",
    "sprintf and snprintf": "sprintf 与 snprintf",
    "stdbool.h and stddef.h": "stdbool.h 与 stddef.h",
    "strcat and strncat": "strcat 与 strncat",
    "switch and fallthrough": "switch 与贯穿",
    "typedef and designated initializers": "typedef 与指定初始化器",
    "void functions and return statements": "void 函数与 return 语句",
    "while and do-while": "while 与 do-while",
}

# objective: -> one-line learning goal.
OBJECTIVES: dict[str, str] = {
    "Access a nested member through an outer struct pointer.":
        "通过外层结构体指针访问嵌套成员。",
    "Access anonymous union members directly through the outer struct.":
        "通过外层结构体直接访问匿名联合体的成员。",
    "Allocate a struct plus trailing data in one block.":
        "用一次分配同时容纳结构体和尾部数据。",
    "Append a string while respecting the destination size.":
        "在目标缓冲区大小的限制下追加字符串。",
    "Avoid accidentally ending an if or loop with a semicolon.":
        "避免误用分号提前结束 if 或循环。",
    "Avoid the usual arithmetic conversion trap when comparing.":
        "比较时避开寻常算术转换的陷阱。",
    "Avoid unsequenced reads and writes of the same object.":
        "避免对同一对象做无序列点保护的读写。",
    "Build masks and avoid shifting by the width of the type.":
        "构造掩码，并避免按类型宽度移位。",
    "Build, traverse, and free a linked list.":
        "构建、遍历并释放一个链表。",
    "Call toupper after including the header that declares it.":
        "先引入声明 toupper 的头文件，再调用它。",
    "Check for NULL and respect pointer-to-const.":
        "检查 NULL，并尊重指向 const 的指针。",
    "Choose an expression based on the type of a value.":
        "根据值的类型选择对应的表达式。",
    "Clear a pointer after freeing its target.":
        "释放目标之后把指针清空。",
    "Combine malloc, setvbuf, output, fclose, and free.":
        "把 malloc、setvbuf、输出、fclose 和 free 串起来用。",
    "Compare floating-point values with an epsilon.":
        "用 epsilon 比较浮点数。",
    "Compare struct value parameters with struct pointer parameters.":
        "对比结构体值参数与结构体指针参数。",
    "Compare union size with the size of its largest member.":
        "比较联合体大小与它最大成员的大小。",
    "Compile a program from a main file, a header, and an implementation file.":
        "用 main 文件、头文件和实现文件编译一个程序。",
    "Configure full buffering and flush a stream.":
        "配置全缓冲并刷新流。",
    "Continue a macro definition onto the next line.":
        "把宏定义续写到下一行。",
    "Copy a stream one character at a time with getc and putc.":
        "用 getc 和 putc 逐字符复制流。",
    "Copy a string safely and always terminate the destination.":
        "安全复制字符串，并保证目标以 NUL 结尾。",
    "Copy a text file line by line.": "逐行复制文本文件。",
    "Copy at most dest_size - 1 bytes and always terminate.":
        "最多复制 dest_size - 1 个字节，并保证结尾有 NUL。",
    "Count set bits and convert sign-magnitude to two's complement.":
        "统计置位个数，并把原码转换成补码。",
    "Create a struct value and access its members through a pointer.":
        "创建结构体值，并通过指针访问它的成员。",
    "Create a temporary struct value with a compound literal.":
        "用复合字面量创建临时结构体值。",
    "Create an array whose length is a runtime value.":
        "创建长度由运行时决定的数据。",
    "Create threads and protect shared state with a mutex.":
        "创建线程，并用互斥量保护共享状态。",
    "Declare a function that never returns and observe its exit status.":
        "声明一个不会返回的函数，并观察它的退出状态。",
    "Declare a global variable in a header and define it in another file.":
        "在头文件里声明全局变量，在另一个文件里定义它。",
    "Detect byte order and inspect an integer's first byte.":
        "判断字节序，并查看整数的第一个字节。",
    "Detect overflow before performing signed addition.":
        "在做有符号加法之前检测溢出。",
    "Detect the C standard version at compile time.":
        "在编译期判断 C 标准版本。",
    "Distinguish a null pointer, an empty string, and the NUL character.":
        "区分空指针、空串和 NUL 字符。",
    "Distinguish a pointer to an array from a pointer to its first element.":
        "区分数组指针和指向首元素的指针。",
    "Distinguish entry-condition and exit-condition loops.":
        "区分入口条件循环和出口条件循环。",
    "Distinguish sizeof expressions from increment side effects.":
        "分清 sizeof 表达式与自增副作用。",
    "Do not assume rand() returns a value below a fixed small bound.":
        "不要假定 rand() 的返回值小于某个固定的小上界。",
    "Do not treat a pointer to a single object as an array.":
        "不要把单个对象的指针当成数组用。",
    "Fix a format-string warning that the compiler reports.":
        "修掉编译器报出的格式串警告。",
    "Format text with snprintf and understand truncation.":
        "用 snprintf 格式化文本，并理解截断行为。",
    "Forward a variable argument list to a variadic function.":
        "把可变实参列表转发给另一个变参函数。",
    "Generate an enum and a string table from one list.":
        "用同一份列表生成枚举和字符串表。",
    "Get loop bounds and accumulators right.":
        "把循环边界和累加器写对。",
    "Give every local variable a defined initial value.":
        "让每个局部变量都有确定的初值。",
    "Grow a dynamic array and preserve existing elements.":
        "扩容动态数组，并保留已有元素。",
    "Implement a fixed-capacity circular queue.":
        "实现一个定容量的环形队列。",
    "Implement a simple bump allocator with aligned allocations.":
        "实现一个简单的、按对齐分配的区域分配器。",
    "Implement strlen, strcmp, and strcpy with pointers.":
        "用指针实现 strlen、strcmp 和 strcpy。",
    "Include a local header so its macro is visible.":
        "引入本地头文件，让其中的宏可见。",
    "Include the standard header that declares fixed-width integer types.":
        "引入声明定宽整数类型的标准头文件。",
    "Include the standard header that declares printf.":
        "引入声明 printf 的标准头文件。",
    "Insert into and search a binary search tree.":
        "向二叉查找树插入节点并查找。",
    "Inspect and reconstruct an IEEE-754 float with memcpy.":
        "用 memcpy 查看并还原 IEEE-754 浮点数。",
    "Install a signal handler and use a sig_atomic_t flag.":
        "安装信号处理函数，并使用 sig_atomic_t 标志。",
    "Iterate over an array and compute a sum and maximum.":
        "遍历数组，求出总和与最大值。",
    "Keep a counter private to one translation unit with static.":
        "用 static 把计数器限制在单个编译单元内。",
    "Keep declarations and definitions consistent across translation units.":
        "让各个编译单元的声明与定义保持一致。",
    "Let a function allocate and update a caller-owned pointer.":
        "让函数分配内存并更新调用方持有的指针。",
    "Load a symbol from a shared library at runtime.":
        "在运行时从动态库中取出一个符号。",
    "Match each conversion specifier to its argument type.":
        "让每个转换说明符与实参类型匹配。",
    "Modify caller-owned data through pointers.":
        "通过指针修改调用方的数据。",
    "Never dereference a null pointer.": "绝不解引用空指针。",
    "Observe implementation-defined char signedness and packing pragmas.":
        "观察实现定义的 char 符号性和打包编译指示。",
    "Observe padding and member offsets with offsetof.":
        "用 offsetof 观察填充和成员偏移。",
    "Observe that && and || may not evaluate their right operand.":
        "观察 && 和 || 可能不计算右操作数。",
    "Observe that nested function calls use distinct activation records.":
        "观察嵌套函数调用使用各自独立的活动记录。",
    "Observe the lifetime of a static variable and block scope.":
        "观察静态变量的生存期与块作用域。",
    "Pack fields with bitfields and compare them with an explicit mask.":
        "用位域打包字段，并与显式掩码做对比。",
    "Pair every allocation with a matching free.":
        "让每次分配都有对应的 free。",
    "Parse a double with strtod and reject trailing input.":
        "用 strtod 解析 double，并拒绝多余的尾部输入。",
    "Parse a hexadecimal string with strtoul.":
        "用 strtoul 解析十六进制字符串。",
    "Parse values from a string with sscanf.":
        "用 sscanf 从字符串里解析出各个值。",
    "Pass a non-const array through a pointer-to-const.":
        "通过指向 const 的指针传递非 const 数组。",
    "Peek at a character and put it back into the stream.":
        "先看一眼字符，再把它放回流里。",
    "Practice integer division, modulo, and truncation.":
        "练习整数除法、取模和截断。",
    "Prevent multiple inclusion with a preprocessor guard.":
        "用预处理保护防止重复引入。",
    "Protect macro arguments and the whole expansion with parentheses.":
        "用括号保护宏参数和整个展开结果。",
    "Query alignment with alignof and keep members aligned.":
        "用 alignof 查询对齐，并让成员保持对齐。",
    "Query and request alignment.": "查询对齐，并指定对齐。",
    "Read a line with fgets and sort an array of strings.":
        "用 fgets 读一行，并对字符串数组排序。",
    "Read a specific struct record from a binary file.":
        "从二进制文件里读出指定的结构体记录。",
    "Read a typedef for an array of function pointers.":
        "读懂函数指针数组的 typedef。",
    "Read a variable number of int arguments with va_list.":
        "用 va_list 读取数量不定的 int 实参。",
    "Read an integer from stdin with scanf.":
        "用 scanf 从标准输入读一个整数。",
    "Read and use a typedef for a function pointer and an array of function pointers.":
        "读懂并使用函数指针及其数组的 typedef。",
    "Read and write environment variables with getenv and _putenv_s.":
        "用 getenv 和 _putenv_s 读写环境变量。",
    "Read and write through pointers.": "通过指针读写数据。",
    "Read until EOF and distinguish end-of-file from an error.":
        "读到 EOF，并区分文件结束与读取出错。",
    "Recognize that a leading zero means base 8.":
        "认识到前导 0 表示八进制。",
    "Recover an outer struct from a pointer to one of its members.":
        "由成员指针反推出外层结构体。",
    "Register a cleanup function with atexit.":
        "用 atexit 注册清理函数。",
    "Reinterpret object representation with memcpy.":
        "用 memcpy 重新解释对象的表示。",
    "Reject indices outside the logical array length.":
        "拒绝超出逻辑长度的下标。",
    "Reject input with trailing characters or out-of-range values.":
        "拒绝带有多余字符或超出范围的输入。",
    "Remember that a space can turn a function-like macro into an object-like macro.":
        "记住一个空格就能把函数式宏变成对象式宏。",
    "Return a defined success or failure status from a program.":
        "让程序返回明确表示成功或失败的状态码。",
    "Return early from a void function and return values from int functions.":
        "在 void 函数里提前 return，在 int 函数里返回值。",
    "Return values through parameters and clamp a range.":
        "通过参数返回结果，并把范围夹紧。",
    "Rewrite a recursive sum using an accumulator.":
        "用累加器改写递归求和。",
    "Scan a const string and modify a mutable char array.":
        "扫描 const 字符串，修改可变的 char 数组。",
    "See how an array parameter becomes a pointer.":
        "看清数组参数如何变成指针。",
    "See that a function-like macro can evaluate its argument more than once.":
        "看清函数式宏可能多次计算它的实参。",
    "See that char operands are promoted to int in arithmetic expressions.":
        "看清 char 操作数在算术表达式里会提升为 int。",
    "Seed the generator and bound its output.":
        "给随机数发生器设种子，并限制输出范围。",
    "Seek to a byte offset and report the resulting position.":
        "定位到某个字节偏移，并报告结果位置。",
    "Select code at preprocessing time based on the language version.":
        "在预处理阶段按语言版本选择代码。",
    "Set a freed pointer to NULL to prevent accidental reuse.":
        "释放后把指针置为 NULL，防止误用。",
    "Split a string without modifying the caller's buffer.":
        "切分字符串，同时不改动调用方的缓冲区。",
    "Store a struct with fwrite and read it back with fread.":
        "用 fwrite 写出结构体，再用 fread 读回来。",
    "Store functions in variables and choose one at runtime.":
        "把函数存进变量，在运行时选一个调用。",
    "Store several small flags in one struct.":
        "把几个小标志位存进一个结构体。",
    "Store text in a char array and access its characters.":
        "把文本存进 char 数组，并访问其中字符。",
    "Track outstanding allocations with wrapped malloc and free.":
        "包装 malloc 和 free，跟踪尚未释放的分配。",
    "Track state while scanning a string.":
        "在扫描字符串的过程中跟踪状态。",
    "Transpose a 3x3 matrix with nested loops.":
        "用嵌套循环转置一个 3x3 矩阵。",
    "Traverse an array of structs and find the best element.":
        "遍历结构体数组，找出最优元素。",
    "Treat address zero as a null pointer, not as a valid object address.":
        "把地址 0 当作空指针，而不是有效对象地址。",
    "Undefine a macro and test it with defined().":
        "取消宏定义，并用 defined() 测试它。",
    "Understand how the lexer greedily forms the longest token.":
        "理解词法分析如何贪心地构成最长的记号。",
    "Understand modulo wrap and avoid signed integer overflow.":
        "理解取模回绕，并避开有符号整数溢出。",
    "Use # to stringize and ## to paste tokens.":
        "用 # 做字符串化，用 ## 拼接记号。",
    "Use +=, -=, *=, /=, %= and the comma operator.":
        "使用 +=、-=、*=、/=、%= 和逗号运算符。",
    "Use == for comparison and recognize the = versus == trap.":
        "比较用 ==，并认出 = 与 == 的陷阱。",
    "Use _Static_assert to enforce assumptions at compile time.":
        "用 _Static_assert 在编译期强制检查假设。",
    "Use _Thread_local to give each thread its own object.":
        "用 _Thread_local 让每个线程拥有自己的对象。",
    "Use a forward declaration and an internal helper.":
        "使用前置声明和内部辅助函数。",
    "Use a named compile-time constant.": "使用一个有名字的编译期常量。",
    "Use a typedef and initialize members by name.":
        "使用 typedef，并按名字初始化成员。",
    "Use an enum for a small closed set of values.":
        "用枚举表示一小组封闭取值。",
    "Use and/or/not from iso646.h.": "使用 iso646.h 里的 and/or/not。",
    "Use assert for programmer errors and return values for user errors.":
        "程序员错误用 assert，用户错误用返回值。",
    "Use atomic_flag as a simple test-and-set lock.":
        "用 atomic_flag 实现一个简单的测试并设置锁。",
    "Use atomic_int for lock-free counter updates.":
        "用 atomic_int 做无锁的计数更新。",
    "Use bool and size_t from the standard headers.":
        "使用标准头文件里的 bool 和 size_t。",
    "Use braces to make else bind to the intended if.":
        "用花括号让 else 绑定到预期的 if。",
    "Use break to stop early and continue to skip one iteration.":
        "用 break 提前结束，用 continue 跳过一轮。",
    "Use calloc when every byte must start as zero.":
        "需要每个字节初值都是零时用 calloc。",
    "Use comments and escape sequences correctly.":
        "正确使用注释和转义序列。",
    "Use comparison callbacks for sorting and searching.":
        "用比较回调配合排序和查找。",
    "Use const, volatile, extern, auto, and register.":
        "使用 const、volatile、extern、auto 和 register。",
    "Use diagnostics, line control, and packing pragmas.":
        "使用诊断、行控制和打包编译指示。",
    "Use do { ... } while (0) for a statement-like macro.":
        "用 do { ... } while (0) 写像语句一样的宏。",
    "Use double complex, I, conj, creal, and cimag.":
        "使用 double complex、I、conj、creal 和 cimag。",
    "Use escape sequences inside a string literal and continue lines explicitly.":
        "在字符串字面量里使用转义序列，并显式续行。",
    "Use field width and a scanset in sscanf.":
        "在 sscanf 里使用字段宽度和扫描集。",
    "Use goto for a clear cleanup path in C.":
        "用 goto 写出清晰的清理路径。",
    "Use hypot and other functions from math.h.":
        "使用 math.h 里的 hypot 等函数。",
    "Use intentional fallthrough and a default case.":
        "使用有意为之的贯穿和 default 分支。",
    "Use isalnum and toupper with unsigned char casts.":
        "把参数转成 unsigned char 后再传给 isalnum 和 toupper。",
    "Use long double and compare its precision with double.":
        "使用 long double，并与 double 比较精度。",
    "Use long internal identifiers and rely on the standard minimum.":
        "使用较长的内部标识符，并依赖标准给出的最小保证。",
    "Use malloc and free for a dynamically sized array.":
        "用 malloc 和 free 管理动态长度的数组。",
    "Use masks and bitwise operators safely.":
        "安全地使用掩码和位运算符。",
    "Use non-local jumps for a simple error path.":
        "用非局部跳转实现一条简单的错误路径。",
    "Use parentheses to express intent clearly.":
        "用括号把意图写清楚。",
    "Use printf to print a line of text.":
        "用 printf 打印一行文本。",
    "Use printf with %d to print an integer value.":
        "用 printf 的 %d 打印一个整数。",
    "Use realloc directly instead of freeing before growing an allocation.":
        "扩容时直接调 realloc，不要先 free。",
    "Use realloc safely and initialize only the new elements.":
        "安全使用 realloc，并只初始化新增的元素。",
    "Use restrict to promise that two pointer parameters do not alias.":
        "用 restrict 承诺两个指针参数不互相别名。",
    "Use signed char and unsigned char explicitly when the sign matters.":
        "符号性重要时，明确使用 signed char 和 unsigned char。",
    "Use sizeof, CHAR_BIT, INT_MIN, and INT_MAX correctly.":
        "正确使用 sizeof、CHAR_BIT、INT_MIN 和 INT_MAX。",
    "Use sqrt with both double and float arguments through tgmath.h.":
        "通过 tgmath.h 用 sqrt 处理 double 和 float 实参。",
    "Use static functions and file-scope state.":
        "使用 static 函数和文件作用域状态。",
    "Use strchr, strrchr, and strstr.": "使用 strchr、strrchr 和 strstr。",
    "Use strtol, errno, and the end pointer to validate input.":
        "用 strtol、errno 和结束指针校验输入。",
    "Use the byte-oriented memory functions correctly.":
        "正确使用按字节操作的内存函数。",
    "Use the half-open interval [low, high).":
        "使用半开区间 [low, high)。",
    "Use the promoted types expected by variadic functions.":
        "使用变参函数期望的提升后类型。",
    "Use the standard input/output character macros directly.":
        "直接使用标准的输入输出字符宏。",
    "Use time_t and difftime.": "使用 time_t 和 difftime。",
    "Use typedef instead of an object-like macro for pointer types.":
        "指针类型用 typedef，不要用对象式宏。",
    "Use uint64_t and PRIu64 from stdint.h and inttypes.h.":
        "使用 stdint.h 和 inttypes.h 里的 uint64_t 与 PRIu64。",
    "Use void pointers and unsigned char for type-agnostic code.":
        "用 void 指针和 unsigned char 写与类型无关的代码。",
    "Use width, zero padding, precision, and the * width argument.":
        "使用宽度、补零、精度和 * 宽度参数。",
    "Walk an array with pointers and return a pointer into it.":
        "用指针遍历数组，并返回指向数组内部的指针。",
    "Work with char values and the ctype classification functions.":
        "处理 char 值，并使用 ctype 的字符分类函数。",
    "Work with the arguments passed to main.":
        "处理传给 main 的参数。",
    "Write and read a text file with fopen, fputs, and fread.":
        "用 fopen、fputs 和 fread 写读文本文件。",
    "Write clear conditional branches.": "写出清晰的条件分支。",
    "Write formatted data to a file and read it back.":
        "把格式化数据写入文件，再读回来。",
    "Write formatted text into a fixed-size buffer.":
        "把格式化文本写进固定大小的缓冲区。",
    "Write recursive functions with correct base cases.":
        "写出基准情形正确的递归函数。",
    # The topic READMEs still carry the upstream wording even where the twin
    # overrides the exercise itself, so keep both spellings mapped.
    "Read and write environment variables with getenv and setenv.":
        "用 getenv 和 _putenv_s 读写环境变量。",
}

# hint: -> a nudge that points at the concept without giving the answer away.
HINTS: dict[str, str] = {
    "#pragma pack(push, 1) removes padding between the two members.":
        "#pragma pack(push, 1) 会去掉两个成员之间的填充。",
    "#undef removes the macro before the second #if.":
        "#undef 会在第二个 #if 之前撤销这个宏。",
    "%08d zero-pads to width 8; %.3f uses three fractional digits.":
        "%08d 补零到宽度 8；%.3f 保留三位小数。",
    "%3d reads at most three digits; %[abc] reads only a, b, and c.":
        "%3d 最多读三位数字；%[abc] 只读 a、b、c。",
    "&a + 1 advances by the whole array, not by one element.":
        "&a + 1 跨越整个数组，而不是一个元素。",
    "++counter increments first; counter++ returns the old value.":
        "++counter 先自增；counter++ 返回旧值。",
    "010 is 8, not 10; 0195 is not a valid C integer constant.":
        "010 是 8，不是 10；0195 不是合法的 C 整数常量。",
    "A VLA is declared with a runtime expression: int values[n].":
        "变长数组用运行时表达式声明：int values[n]。",
    "A bare block macro breaks if/else syntax.":
        "光秃秃的块状宏会破坏 if/else 的语法。",
    "A do-while body always executes at least once.":
        "do-while 的循环体至少执行一次。",
    "A failed static assertion must make the build fail.":
        "静态断言失败必须让编译失败。",
    "A mask of width w has w low bits set: (1u << w) - 1u.":
        "宽度 w 的掩码是低 w 位全为 1：(1u << w) - 1u。",
    "A negative int converted to unsigned becomes a very large value.":
        "负的 int 转成无符号后会变成很大的值。",
    "A pointer to const may point at non-const data.":
        "指向 const 的指针可以指向非 const 数据。",
    "A pointer-to-const can read but not write the pointed-to object.":
        "指向 const 的指针能读，但不能写它指向的对象。",
    "A second helper macro is needed to expand a macro before stringizing it.":
        "要先把宏展开再字符串化，就得再套一层辅助宏。",
    "A semicolon after if creates an empty body.":
        "if 后面直接写分号会产生一个空语句体。",
    "A single = assigns; a double == compares.":
        "单个 = 是赋值；两个 == 才是比较。",
    "A string literal must not be modified; a char array may be modified.":
        "字符串字面量不能改；char 数组可以改。",
    "A struct pointer can modify the caller's struct.":
        "结构体指针可以修改调用方的结构体。",
    "A trailing backslash continues the macro definition.":
        "行尾的反斜杠用来续写宏定义。",
    "A uint16_t value of 1 stores 0x01 first on little-endian systems.":
        "在小端系统上，值为 1 的 uint16_t 先存 0x01。",
    "A void function uses a bare return; an int function must return a value.":
        "void 函数写 return; 就行；int 函数必须返回一个值。",
    "A word starts when the previous character was whitespace.":
        "前一个字符是空白时，一个新词开始。",
    "A zero denominator is a normal error, so return -1 instead of dividing.":
        "分母为零属于正常的错误，返回 -1，不要真的去除。",
    "Add the include for config.h in main.c.":
        "在 main.c 里加上对 config.h 的 include。",
    "Add the standard header that declares int32_t and INT32_MAX.":
        "加上声明 int32_t 和 INT32_MAX 的标准头文件。",
    "Advance one element at a time; p < values + count is the end condition.":
        "每次前进一个元素；结束条件是 p < values + count。",
    "After free(*pointer), assign NULL through the pointer-to-pointer.":
        "free(*pointer) 之后，通过二级指针把它置为 NULL。",
    "Align each request to 8 bytes before bumping the used offset.":
        "每次分配前先把大小按 8 字节对齐，再移动已用偏移。",
    "An anonymous union member is promoted into the enclosing struct scope.":
        "匿名联合体的成员会提升到外层结构体的作用域里。",
    "An index is invalid when it is less than zero or greater than or equal to count.":
        "下标小于 0，或大于等于 count，就是无效的。",
    "Array indexes start at 0; sizeof(\"hello\") includes the terminating NUL.":
        "数组下标从 0 开始；sizeof(\"hello\") 包含结尾的 NUL。",
    "Assign through *slot, not to the local slot parameter.":
        "要通过 *slot 赋值，而不是给本地的 slot 参数赋值。",
    "Assigning the parameter itself does not modify the caller's variable.":
        "只给参数本身赋值，不会改变调用方的变量。",
    "Base 16 accepts an optional 0x prefix.":
        "十六进制可以带 0x 前缀，也可以不带。",
    "Bitfield layout is implementation-defined; masks make the encoding explicit.":
        "位域的布局由实现定义；用掩码能把编码写明确。",
    "C11 introduced __STDC_VERSION__ value 201112L.":
        "C11 对应的 __STDC_VERSION__ 是 201112L。",
    "CHAR_MIN tells you whether plain char is signed; #pragma pack changes padding.":
        "CHAR_MIN 能看出 char 是否带符号；#pragma pack 改变填充。",
    "Check INT_MAX - b before adding b to a.":
        "在 a 上加 b 之前，先检查 INT_MAX - b。",
    "Check errno, endptr, and the character after the number.":
        "要检查 errno、endptr，以及数字后面的那个字符。",
    "Check for positive, then negative, then the remaining zero case.":
        "先判断正数，再判断负数，最后处理剩下的零。",
    "Clearing a bit uses value & ~(1u << bit).":
        "清位用 value & ~(1u << bit)。",
    "Copy the byte from a before overwriting it.":
        "先把 a 里的字节存下来，再覆盖它。",
    "Declare add in the header and define it in math_utils.c.":
        "在头文件里声明 add，在 math_utils.c 里定义它。",
    "Define the guard macro before the guarded declarations.":
        "保护宏要定义在被保护的声明之前。",
    "Designated initializers make the field mapping explicit.":
        "指定初始化器能把字段对应关系写明确。",
    "Double the capacity when the array is full.":
        "数组满时把容量翻倍。",
    "Double usually requires more alignment than int.":
        "double 通常比 int 要求更严格的对齐。",
    "Each case should return the matching color name.":
        "每个分支返回对应的颜色名。",
    "Each worker increments the shared counter 1000 times.":
        "每个工作线程把共享计数器加 1000 次。",
    "Escape sequences keep their meaning inside string literals.":
        "转义序列在字符串字面量里依然生效。",
    "Escape sequences start with a backslash; comments need both delimiters.":
        "转义序列以反斜杠开头；注释需要成对的定界符。",
    "Every union member starts at the same address.":
        "联合体的每个成员都从同一个地址开始。",
    "Exact equality is usually the wrong comparison for computed doubles.":
        "对算出来的 double 做精确相等比较，通常都是错的。",
    "February has 29 days when leap is true.":
        "leap 为真时，二月有 29 天。",
    "For a single object, only the one-past pointer is valid; do not dereference it.":
        "对单个对象来说，只有越尾一个位置的那个指针是合法的，而且不能解引用。",
    "INT_POINTER a, b declares b as int, not int *.":
        "INT_POINTER a, b 会把 b 声明成 int，而不是 int *。",
    "Increment the free counter when a non-NULL pointer is freed.":
        "释放非 NULL 指针时，把释放计数加一。",
    "Inside a function, an array parameter has pointer type.":
        "在函数内部，数组参数的类型是指针。",
    "Integer division truncates toward zero.":
        "整数除法向零截断。",
    "Leave room for the terminating NUL.":
        "给结尾的 NUL 留出位置。",
    "Lowercase letters live in a contiguous range only for the execution character set.":
        "小写字母连续，这个性质只对执行字符集成立。",
    "Modern C guarantees at least 31 significant external and 63 internal identifier characters.":
        "现代 C 至少保证外部标识符前 31 个、内部标识符前 63 个字符有意义。",
    "Multiplication binds more tightly than addition.":
        "乘法的结合比加法更紧。",
    "NEXT_VALUE() expands to the expression every time it appears.":
        "NEXT_VALUE() 每出现一次，就把那个表达式展开一次。",
    "NULL is a null pointer; \"\" is a valid empty string; '\\0' is NUL.":
        "NULL 是空指针；\"\" 是合法的空串；'\\0' 是 NUL 字符。",
    "NULL is the portable null pointer constant.":
        "NULL 是可移植的空指针常量。",
    "Object-like macros are simple text substitutions.":
        "对象式宏就是简单的文本替换。",
    "PRIu64 is the portable printf specifier for uint64_t.":
        "PRIu64 是 uint64_t 的可移植 printf 说明符。",
    "Parenthesize both the parameters and the entire replacement expression.":
        "参数和整个替换表达式都要加括号。",
    "Pass (unsigned char) to ctype functions to avoid negative arguments.":
        "传给 ctype 函数的参数要转成 (unsigned char)，避免出现负值。",
    "Pass both space and comma as delimiters.":
        "空格和逗号都要作为分隔符传进去。",
    "Plain char may be signed or unsigned; signed char and unsigned char are explicit.":
        "char 是否带符号由实现决定；signed char 和 unsigned char 则是明确的。",
    "Post-increment returns the old value; pre-increment returns the new value.":
        "后置自增返回旧值；前置自增返回新值。",
    "Qualifiers affect how an object may be accessed and optimized.":
        "限定符影响对象可以被怎样访问和优化。",
    "Read the old value, update the object, then return the old value.":
        "先读出旧值，再更新对象，最后返回旧值。",
    "Reject empty input, trailing characters, ERANGE, and out-of-range values.":
        "空输入、多余字符、ERANGE、超出范围的值，都要拒绝。",
    "Return 0 for success and 1 for failure.":
        "成功返回 0，失败返回 1。",
    "Return the function that matches the operator character.":
        "返回与运算符字符对应的那个函数。",
    "SUM(...) should pass every argument, including the count.":
        "SUM(...) 要把每个实参都传下去，包括那个计数。",
    "Save *a before overwriting it.":
        "在覆盖 *a 之前先把它存下来。",
    "Seek by index * sizeof(record).":
        "用 index * sizeof(record) 计算定位偏移。",
    "Set *out only after the copy has been allocated and filled.":
        "副本分配好、填好之后，再给 *out 赋值。",
    "Smaller values go left; larger values go right.":
        "较小的值放左边，较大的值放右边。",
    "Start filling at old_count so the existing elements survive.":
        "从 old_count 开始填，已有的元素才不会丢。",
    "Start result at -1 so the fallback path is well-defined.":
        "把 result 初值设为 -1，兜底路径才有确定行为。",
    "Subtract the byte offset of the inner member.":
        "减去内层成员的字节偏移。",
    "The ( must immediately follow the macro name.":
        "左括号必须紧跟宏名。",
    "The C standard only guarantees RAND_MAX >= 32767.":
        "C 标准只保证 RAND_MAX >= 32767。",
    "The address lives inside the person struct.":
        "这个地址位于 person 结构体内部。",
    "The allocation size is sizeof *packet + length bytes.":
        "分配大小是 sizeof *packet 加上 length 个字节。",
    "The buffer passed to setvbuf must remain valid until the stream is closed.":
        "传给 setvbuf 的缓冲区必须一直有效，直到流被关闭。",
    "The child re-runs this program with the \"child\" argument, then exits with status 7.":
        "子进程带着 \"child\" 参数重新运行本程序，然后以状态 7 退出。",
    "The cleanup path must release the tracked allocation.":
        "清理路径必须释放被跟踪的那块分配。",
    "The comma operator evaluates left to right and yields the right operand.":
        "逗号运算符从左到右求值，结果是右操作数。",
    "The comparator returns negative, zero, or positive.":
        "比较函数返回负数、零或正数。",
    "The compiler needs a declaration of printf; add the standard I/O header.":
        "编译器需要 printf 的声明；加上标准 I/O 头文件。",
    "The compiler needs the declaration from ctype.h; add the include.":
        "编译器需要 ctype.h 里的声明；把这个 include 加上。",
    "The controlling expression is not evaluated; only its type is used.":
        "控制表达式不会被求值，只用到它的类型。",
    "The declaration promises the signature; the definition supplies the body.":
        "声明承诺了函数签名，定义提供函数体。",
    "The destination pointer must advance after each copied character.":
        "每复制一个字符，目标指针都要前进。",
    "The extern declaration promises a definition in config.c.":
        "extern 声明承诺了在 config.c 里有对应的定义。",
    "The format strings used for writing and reading must agree.":
        "写入和读取用的格式串必须一致。",
    "The linker does not compare the types of extern declarations.":
        "链接器不会比对各个 extern 声明的类型。",
    "The literal comma in the format must match the input string.":
        "格式串里的那个逗号必须和输入串里的对齐。",
    "The loop must consume exactly count arguments.":
        "循环必须正好取出 count 个实参。",
    "The new node must point at the previous head.":
        "新节点要指向原来的表头。",
    "The number of bits in an int is sizeof(int) * CHAR_BIT.":
        "int 的位数是 sizeof(int) * CHAR_BIT。",
    "The recursive call should be the last operation.":
        "递归调用应当是这个函数里最后一步操作。",
    "The right side of && is only evaluated when the left side is true.":
        "只有左侧为真时，才会计算 && 的右侧。",
    "The string table uses #name, not a fixed string.":
        "字符串表用 #name 生成，不是写死的字符串。",
    "The syntax is (struct point){.x = 3, .y = 4}.":
        "写法是 (struct point){.x = 3, .y = 4}。",
    "The tail index wraps with modulo capacity.":
        "尾部下标用模 capacity 回绕。",
    "The transposed element at [row][column] comes from input[column][row].":
        "转置后 [row][column] 上的元素来自 input[column][row]。",
    "The upper bound is exclusive: value < high.":
        "上界不包含在内：value < high。",
    "The worker thread modifies its own copy of thread_value.":
        "工作线程修改的是它自己那份 thread_value。",
    "The write flag must reflect the enabled argument.":
        "写标志要反映 enabled 参数的值。",
    "Unsigned arithmetic wraps; signed overflow is undefined behavior.":
        "无符号运算会回绕；有符号溢出是未定义行为。",
    "Update call_count before returning the incremented value.":
        "返回自增后的值之前，先更新 call_count。",
    "Use %c after %d to detect trailing non-whitespace input.":
        "在 %d 后面加 %c，用来发现后面还有非空白字符。",
    "Use %d for an int argument and include the newline in the format string.":
        "int 实参用 %d，并且把换行写进格式串。",
    "Use %d to print an int; %s expects a string.":
        "打印 int 用 %d；%s 要的是字符串。",
    "Use LoadLibraryA, GetProcAddress and FreeLibrary; convert FARPROC through a union.":
        "用 LoadLibraryA、GetProcAddress 和 FreeLibrary；FARPROC 通过联合体转换。",
    "Use a conditional expression to provide a fallback.":
        "用条件表达式给出兜底值。",
    "Use binary mode and compare the number of complete items written.":
        "用二进制模式，并比较完整写出的元素个数。",
    "Use memcpy instead of pointer casts to avoid strict-aliasing violations.":
        "用 memcpy 代替指针强制转换，避开严格别名违规。",
    "Use mode \"w\" for writing and mode \"r\" for reading.":
        "写入用 \"w\" 模式，读取用 \"r\" 模式。",
    "Use students[i].score for each element.":
        "每个元素都用 students[i].score 访问。",
    "Use the L suffix for long double constants.":
        "long double 常量要加 L 后缀。",
    "Use the arrow operator when you have a pointer.":
        "手里是指针时，就用箭头运算符。",
    "Use values[i] inside the loop, not values[0].":
        "循环里要用 values[i]，不是 values[0]。",
    "When count is zero, leave the outputs unchanged.":
        "count 为零时，不要改动输出。",
    "Without braces, else binds to the nearest unmatched if.":
        "不写花括号时，else 会绑定到最近的那个还没配对的 if。",
    "Write NULL through the pointer-to-pointer after free.":
        "free 之后通过二级指针写入 NULL。",
    "Write fill into every element, not just the first.":
        "每个元素都要写入 fill，不能只写第一个。",
    "__STDC_VERSION__ is 201112L for C11 and 201710L for C17.":
        "C11 的 __STDC_VERSION__ 是 201112L，C17 是 201710L。",
    "__builtin_frame_address is a GCC/Clang extension.":
        "__builtin_frame_address 是 GCC/Clang 的扩展。",
    "_putenv_s must succeed before getenv can find the new value.":
        "_putenv_s 成功之后，getenv 才能找到新值。",
    "a+++b is tokenized as (a++) + b.":
        "a+++b 会被切分成 (a++) + b。",
    "alignof reports the strictest alignment the type requires.":
        "alignof 给出该类型要求的最严格对齐。",
    "argv[0] is the program name; user arguments start at argv[1].":
        "argv[0] 是程序名；用户参数从 argv[1] 开始。",
    "atexit returns 0 on success and nonzero on failure.":
        "atexit 成功返回 0，失败返回非零值。",
    "atomic_fetch_add adds to the current value and returns the old value.":
        "atomic_fetch_add 把当前值加上去，并返回旧值。",
    "atomic_flag_test_and_set returns the previous state.":
        "atomic_flag_test_and_set 返回之前的状态。",
    "binary_operation is a typedef for int (*)(int, int).":
        "binary_operation 是 int (*)(int, int) 的 typedef。",
    "bool is defined in <stdbool.h>; size_t is defined in <stddef.h>.":
        "bool 定义在 <stdbool.h>；size_t 定义在 <stddef.h>。",
    "calloc(count, size) returns zeroed memory.":
        "calloc(count, size) 返回已经清零的内存。",
    "char and short promote to int; float promotes to double.":
        "char 和 short 提升为 int；float 提升为 double。",
    "conj changes the sign of the imaginary part.":
        "conj 把虚部的符号取反。",
    "continue skips the rest of the current iteration; break exits the loop.":
        "continue 跳过本轮剩下的语句；break 直接退出循环。",
    "difftime(end, start) returns end - start seconds.":
        "difftime(end, start) 返回 end - start 秒。",
    "factorial(n) = n * factorial(n - 1).":
        "factorial(n) = n * factorial(n - 1)。",
    "feof is true only after a read attempts to pass the end of the file.":
        "只有读取试图越过文件末尾之后，feof 才为真。",
    "fgets includes the newline when the buffer is large enough.":
        "缓冲区足够大时，fgets 会把换行也读进来。",
    "free(values) followed by realloc(values, ...) uses a dangling pointer.":
        "先 free(values) 再 realloc(values, ...)，用的是已经失效的指针。",
    "fseek with SEEK_SET positions the stream at an absolute offset.":
        "fseek 配 SEEK_SET 会把流定位到绝对偏移。",
    "getc returns EOF when there are no more characters.":
        "没有字符可读时，getc 返回 EOF。",
    "hypot(x, y) computes sqrt(x*x + y*y) without avoidable overflow.":
        "hypot(x, y) 计算 sqrt(x*x + y*y)，并避免本可避免的溢出。",
    "iso646.h defines and as && and or as ||.":
        "iso646.h 把 and 定义为 &&，把 or 定义为 ||。",
    "long values use %ld; doubles use %f or %.2f.":
        "long 用 %ld；double 用 %f 或 %.2f。",
    "longjmp returns control to the matching setjmp call.":
        "longjmp 会把控制权交回与它配对的 setjmp 调用处。",
    "memcpy preserves the bit pattern; a cast to float converts the numeric value.":
        "memcpy 保留位模式；强制转换成 float 则是转换数值。",
    "memcpy requires non-overlapping regions; memmove handles overlap.":
        "memcpy 要求两块内存不重叠；memmove 能处理重叠。",
    "offsetof takes the struct type and the member name.":
        "offsetof 接收结构体类型和成员名。",
    "operation_table is typedef int (*[3])(int, int).":
        "operation_table 是 typedef int (*[3])(int, int)。",
    "printf returns the number of characters printed, including the newline.":
        "printf 返回打印出的字符数，包含换行符。",
    "qsort receives an array of pointers, so cast to const char *const *.":
        "qsort 收到的是指针数组，所以要转成 const char *const *。",
    "raise(SIGINT) invokes the installed handler synchronously.":
        "raise(SIGINT) 会同步调用已经安装的处理函数。",
    "rand() % upper produces values from 0 to upper - 1.":
        "rand() % upper 得到 0 到 upper - 1 之间的值。",
    "restrict tells the compiler that destination and source do not overlap.":
        "restrict 告诉编译器，目标和源不会重叠。",
    "scanf needs the address of the variable: &value.":
        "scanf 需要变量的地址：&value。",
    "setvbuf must be called before other I/O on the stream.":
        "必须在流上做其它 I/O 之前调用 setvbuf。",
    "sizeof(left + right) is sizeof(int) for char operands.":
        "操作数是 char 时，sizeof(left + right) 等于 sizeof(int)。",
    "snprintf returns the number of characters that would have been written.":
        "snprintf 返回的是「如果空间够，本会写出的字符数」。",
    "snprintf takes the buffer size and returns the number of characters it would write.":
        "snprintf 接收缓冲区大小，返回它本会写出的字符数。",
    "static file-scope objects are visible only in their own .c file.":
        "static 的文件作用域对象只在自己的 .c 文件里可见。",
    "strncat appends at most n characters and always terminates.":
        "strncat 最多追加 n 个字符，并且总会补上 NUL。",
    "strncpy does not guarantee a terminating NUL when the source is too long.":
        "源串过长时，strncpy 不保证结尾有 NUL。",
    "strstr finds a substring, not just a single character.":
        "strstr 找的是子串，不只是单个字符。",
    "sum_to(n) includes n; factorial multiplies 2 through n.":
        "sum_to(n) 把 n 也算进去；factorial 相乘的范围是 2 到 n。",
    "tgmath.h selects the correct real function from the argument type.":
        "tgmath.h 会根据实参类型挑出正确的实数函数。",
    "ungetc can push a character back onto stdin for a test.":
        "测试时可以用 ungetc 把一个字符退回 stdin。",
    "ungetc pushes one character back onto the input stream.":
        "ungetc 把一个字符退回输入流。",
    "value &= value - 1 clears the lowest set bit.":
        "value &= value - 1 会清掉最低的那个置位。",
}

# Comment lines inside exercise and solution bodies.  "TODO:" stays English so
# learners can keep searching for it the same way they would in any C project.
COMMENTS: dict[str, str] = {
    "TODO: a union is only as large as its largest member.":
        "TODO: 联合体的大小等于它最大成员的大小。",
    "TODO: a word starts when we were not in one.":
        "TODO: 上一刻不在词里，这一刻就是新词的开始。",
    "TODO: account for leap years.": "TODO: 把闰年考虑进来。",
    "TODO: add amount to the existing value.":
        "TODO: 把 amount 加到已有的值上。",
    "TODO: add parentheses so the sum is multiplied by c.":
        "TODO: 加括号，让和乘以 c。",
    "TODO: add the current element.": "TODO: 把当前元素加进去。",
    "TODO: add the current student's score.":
        "TODO: 加上当前学生的分数。",
    "TODO: add the two values.": "TODO: 把两个值相加。",
    "TODO: advance by the whole array, not one element.":
        "TODO: 一次跨越整个数组，不是一个元素。",
    "TODO: align the allocation size.": "TODO: 把分配大小对齐。",
    "TODO: append the value and increase size.":
        "TODO: 追加这个值，并把 size 加一。",
    "TODO: call the selected operation.": "TODO: 调用选中的操作。",
    "TODO: call the selected table entry.":
        "TODO: 调用表中选中的那一项。",
    "TODO: choose multiply for any non-plus operator.":
        "TODO: 只要运算符不是加号，就选乘法。",
    "TODO: clamp to the lower bound.": "TODO: 夹到下限。",
    "TODO: classify letters and digits.":
        "TODO: 判断字母和数字。",
    "TODO: clear the caller's pointer.": "TODO: 清空调用方的指针。",
    "TODO: clear the lowest set bit.": "TODO: 清掉最低的置位。",
    "TODO: clear the selected bit.": "TODO: 清掉选中的那一位置位。",
    "TODO: close the comment.": "TODO: 把注释闭合。",
    "TODO: compare against the null pointer.":
        "TODO: 与空指针比较。",
    "TODO: compare instead of assign.": "TODO: 这里是比较，不是赋值。",
    "TODO: compare the low byte of value 1.":
        "TODO: 比较 value1 的低字节。",
    "TODO: complete the byte swap.": "TODO: 完成字节交换。",
    "TODO: compute the Euclidean distance.":
        "TODO: 计算欧几里得距离。",
    "TODO: compute the average as a long double.":
        "TODO: 用 long double 算平均值。",
    "TODO: consume every variadic argument.":
        "TODO: 取出每一个可变实参。",
    "TODO: continue the macro definition onto the next line.":
        "TODO: 把宏定义续写到下一行。",
    "TODO: convert lowercase letters to uppercase.":
        "TODO: 把小写字母转成大写。",
    "TODO: copy the line that was read.":
        "TODO: 把读到的这一行复制出去。",
    "TODO: copy the object representation.":
        "TODO: 复制对象的表示。",
    "TODO: copy the whole array, not count bytes.":
        "TODO: 复制整个数组，不是 count 个字节。",
    "TODO: copy until the terminating NUL.":
        "TODO: 一直复制到结尾的 NUL。",
    "TODO: count every call.": "TODO: 每次调用都计数。",
    "TODO: count the free.": "TODO: 把这次 free 也计入。",
    "TODO: define a 16-byte buffer size.":
        "TODO: 定义一个 16 字节的缓冲区长度。",
    "TODO: define config_value.": "TODO: 定义 config_value。",
    "TODO: define the include guard macro.":
        "TODO: 定义头文件保护宏。",
    "TODO: detect overflow before adding.":
        "TODO: 相加之前先检测溢出。",
    "TODO: detect overflow before doing the addition.":
        "TODO: 做加法之前先检测溢出。",
    "TODO: do not read and modify the same object without a sequence point.":
        "TODO: 不要在没有序列点的情况下同时读写同一个对象。",
    "TODO: double the non-negative value.":
        "TODO: 把非负的值翻倍。",
    "TODO: expand the argument twice.":
        "TODO: 把实参展开两次。",
    "TODO: expand x before stringizing it.":
        "TODO: 先把 x 展开，再字符串化。",
    "TODO: flush the stream.": "TODO: 刷新流。",
    "TODO: format name followed by age.":
        "TODO: 按「名字 年龄」的顺序格式化。",
    "TODO: format the greeting with the name C.":
        "TODO: 用名字 C 拼出问候语。",
    "TODO: forward all arguments, including the count.":
        "TODO: 把所有实参都转发出去，包括那个计数。",
    "TODO: grow without freeing the original block first.":
        "TODO: 不要先释放原来的块，直接扩容。",
    "TODO: honor the enabled argument.":
        "TODO: 按 enabled 参数决定是否启用。",
    "TODO: include n in the sum.": "TODO: 求和时把 n 也算进去。",
    "TODO: include the header for fixed-width integers.":
        "TODO: 引入定宽整数对应的头文件。",
    "TODO: include the header that declares printf.":
        "TODO: 引入声明 printf 的头文件。",
    "TODO: include the header that declares toupper.":
        "TODO: 引入声明 toupper 的头文件。",
    "TODO: include the local header that defines CONFIG_VALUE.":
        "TODO: 引入定义 CONFIG_VALUE 的本地头文件。",
    "TODO: increment the shared counter.":
        "TODO: 递增共享计数器。",
    "TODO: initialize both members by name.":
        "TODO: 按名字初始化两个成员。",
    "TODO: initialize the VLA element.":
        "TODO: 初始化变长数组的元素。",
    "TODO: initialize the current element.":
        "TODO: 初始化当前元素。",
    "TODO: initialize the fallback value.":
        "TODO: 初始化兜底值。",
    "TODO: initialize the volatile value.":
        "TODO: 初始化这个 volatile 值。",
    "TODO: jump back to the setjmp call.":
        "TODO: 跳回 setjmp 的调用处。",
    "TODO: keep the ( immediately after SQUARE.":
        "TODO: 左括号要紧跟在 SQUARE 后面。",
    "TODO: keep the result below upper.":
        "TODO: 让结果落在 upper 以下。",
    "TODO: larger values go to the right subtree.":
        "TODO: 较大的值放到右子树。",
    "TODO: leave room for the terminator.":
        "TODO: 给结尾符留出位置。",
    "TODO: link the new node to the old head.":
        "TODO: 把新节点接到原来的表头上。",
    "TODO: look up the strlen symbol.":
        "TODO: 查找 strlen 这个符号。",
    "TODO: make the caller's pointer null after freeing it.":
        "TODO: 释放之后把调用方的指针置空。",
    "TODO: make the macro behave like a single statement.":
        "TODO: 让这个宏表现得像一条语句。",
    "TODO: make the upper bound exclusive.":
        "TODO: 让上界不包含在内。",
    "TODO: make thread_value thread-local.":
        "TODO: 把 thread_value 变成线程局部的。",
    "TODO: mask the four-bit value field.":
        "TODO: 把 4 位的 value 字段掩出来。",
    "TODO: measure the offset of the value member.":
        "TODO: 测出 value 成员的偏移。",
    "TODO: measure the width of int, not char.":
        "TODO: 量的是 int 的宽度，不是 char 的。",
    "TODO: multiply by the recursive result.":
        "TODO: 乘以递归返回的结果。",
    "TODO: multiply value by 2.": "TODO: 把 value 乘以 2。",
    "TODO: negative numbers have sign -1.":
        "TODO: 负数的符号位是 -1。",
    "TODO: negative values are smaller than any unsigned.":
        "TODO: 负值比任何无符号值都小。",
    "TODO: only one-past is valid for a single object.":
        "TODO: 对单个对象来说，只有越尾一个位置是合法的。",
    "TODO: open the file for writing.":
        "TODO: 以写入方式打开文件。",
    "TODO: pack the struct without padding.":
        "TODO: 让结构体不带填充地打包。",
    "TODO: parenthesize the whole macro expansion.":
        "TODO: 给整个宏展开加括号。",
    "TODO: parse base 16.": "TODO: 按十六进制解析。",
    "TODO: pass the full length through the const pointer.":
        "TODO: 把完整长度通过指向 const 的指针传出去。",
    "TODO: pre-increment the private counter.":
        "TODO: 前置自增这个私有计数器。",
    "TODO: pre-increment the static counter.":
        "TODO: 前置自增这个 static 计数器。",
    "TODO: preserve the existing elements.":
        "TODO: 保留已有的元素。",
    "TODO: preserve the maximal-munch tokenization.":
        "TODO: 保持最长匹配的切分结果。",
    "TODO: preserve the signed value.": "TODO: 保留有符号的值。",
    "TODO: print Hello, C! followed by a newline.":
        "TODO: 打印 Hello, C! 并换行。",
    "TODO: print the integer value.": "TODO: 打印这个整数值。",
    "TODO: put the character back into the stream.":
        "TODO: 把这个字符退回流里。",
    "TODO: read at most three digits.":
        "TODO: 最多读三位数字。",
    "TODO: read one character from stdin.":
        "TODO: 从标准输入读一个字符。",
    "TODO: read the anonymous union member.":
        "TODO: 读取匿名联合体的成员。",
    "TODO: read the environment variable back.":
        "TODO: 把环境变量读回来。",
    "TODO: read the promoted int argument.":
        "TODO: 取出提升为 int 的那个实参。",
    "TODO: record that the signal was caught.":
        "TODO: 记下信号已经被捕获。",
    "TODO: record the payload length.": "TODO: 记录负载长度。",
    "TODO: register the cleanup function.":
        "TODO: 注册清理函数。",
    "TODO: reinterpret the bit pattern instead of converting the number.":
        "TODO: 重新解释位模式，而不是转换数值。",
    "TODO: reject indices that are out of range.":
        "TODO: 拒绝越界的下标。",
    "TODO: reject trailing characters.":
        "TODO: 拒绝多余的尾部字符。",
    "TODO: release the lock.": "TODO: 释放锁。",
    "TODO: release the tracked allocation.":
        "TODO: 释放被跟踪的这块分配。",
    "TODO: remove CLINGS_FEATURE before the second test.":
        "TODO: 在第二次测试之前撤销 CLINGS_FEATURE。",
    "TODO: replace the character.": "TODO: 替换这个字符。",
    "TODO: report success after a bounded append.":
        "TODO: 有界追加成功之后返回成功。",
    "TODO: report the actual alignment of int.":
        "TODO: 报出 int 实际的对齐。",
    "TODO: report the alignment of double.":
        "TODO: 报出 double 的对齐。",
    "TODO: report the error.": "TODO: 报告这个错误。",
    "TODO: restore the correct compile-time assumption.":
        "TODO: 恢复正确的编译期假设。",
    "TODO: restore the escape sequences.":
        "TODO: 恢复这些转义序列。",
    "TODO: return 0 for success and 1 for failure.":
        "TODO: 成功返回 0，失败返回 1。",
    "TODO: return a bool result, not an integer remainder.":
        "TODO: 返回 bool 结果，而不是整数余数。",
    "TODO: return a distinct inner frame.":
        "TODO: 返回一个不同的内层栈帧。",
    "TODO: return ascending order.": "TODO: 返回升序。",
    "TODO: return the backslash character.":
        "TODO: 返回反斜杠字符。",
    "TODO: return the blue color name.":
        "TODO: 返回蓝色的颜色名。",
    "TODO: return the complex conjugate.":
        "TODO: 返回这个复数的共轭。",
    "TODO: return the computed sum to the caller.":
        "TODO: 把算出的和返回给调用方。",
    "TODO: return the last visible character, not the NUL terminator.":
        "TODO: 返回最后一个可见字符，不是结尾的 NUL。",
    "TODO: return the long-identifier value.":
        "TODO: 返回那个长标识符对应的值。",
    "TODO: return the newline character.":
        "TODO: 返回换行符。",
    "TODO: return the number of characters read.":
        "TODO: 返回读到的字符个数。",
    "TODO: return the octal constant 010.":
        "TODO: 返回八进制常量 010。",
    "TODO: return the pointed-to value only when the pointer is not null.":
        "TODO: 只在指针不为空时返回它指向的值。",
    "TODO: return the remainder, not the quotient.":
        "TODO: 返回余数，不是商。",
    "TODO: return the square of value.":
        "TODO: 返回 value 的平方。",
    "TODO: return the sum of both coordinates.":
        "TODO: 返回两个坐标之和。",
    "TODO: return the tab character.": "TODO: 返回制表符。",
    "TODO: return true only for a null pointer.":
        "TODO: 只在指针为空时返回真。",
    "TODO: return zero-initialized storage.":
        "TODO: 返回已经清零的存储。",
    "TODO: scanf needs the address of value.":
        "TODO: scanf 需要的是 value 的地址。",
    "TODO: search all user arguments.":
        "TODO: 在所有用户参数里查找。",
    "TODO: search for the whole substring.":
        "TODO: 查找整个子串。",
    "TODO: seek relative to the beginning of the file.":
        "TODO: 相对文件开头定位。",
    "TODO: seek to the selected record.":
        "TODO: 定位到选中的那条记录。",
    "TODO: shift the x coordinate by dx.":
        "TODO: 把 x 坐标平移 dx。",
    "TODO: skip this value, do not stop the loop.":
        "TODO: 跳过这个值，不要退出循环。",
    "TODO: sort in ascending order.": "TODO: 按升序排序。",
    "TODO: store the new value.": "TODO: 存下这个新值。",
    "TODO: stringize each name.": "TODO: 把每个名字字符串化。",
    "TODO: subtract one to build the mask.":
        "TODO: 减一，构造出掩码。",
    "TODO: subtract start from end.": "TODO: 用 end 减 start。",
    "TODO: subtract the offset of the inner member.":
        "TODO: 减去内层成员的偏移。",
    "TODO: swap the row and column indices.":
        "TODO: 把行下标和列下标交换。",
    "TODO: swap the two integers without losing either value.":
        "TODO: 交换两个整数，并且不丢掉任何一个值。",
    "TODO: terminate the copied string.":
        "TODO: 给复制出来的字符串补上结尾。",
    "TODO: terminate with status 7.":
        "TODO: 以状态 7 结束进程。",
    "TODO: the sum is promoted to int.":
        "TODO: 求和的结果会提升为 int。",
    "TODO: treat NULL as an empty input.":
        "TODO: 把 NULL 当作空输入处理。",
    "TODO: update the pointer that slot points to.":
        "TODO: 更新 slot 指向的那个指针。",
    "TODO: use an epsilon comparison.":
        "TODO: 用 epsilon 比较。",
    "TODO: use an exit-condition loop.":
        "TODO: 用出口条件循环。",
    "TODO: use post-increment here.": "TODO: 这里用后置自增。",
    "TODO: use the conversion specifier for an int.":
        "TODO: 用 int 对应的转换说明符。",
    "TODO: use the correct specifier for a long value.":
        "TODO: 用 long 对应的说明符。",
    "TODO: use the format macro for uint64_t.":
        "TODO: 用 uint64_t 对应的格式宏。",
    "TODO: use the local array, not a pointer, to compute the length.":
        "TODO: 用本地数组求长度，不要用指针。",
    "TODO: use the logical AND operator, not bitwise AND.":
        "TODO: 用逻辑与，不是按位与。",
    "TODO: use the matching source element.":
        "TODO: 用对应的源元素。",
    "TODO: use the standard minimum guarantee.":
        "TODO: 用标准给出的最小保证。",
    "TODO: use the typedef for both declarations.":
        "TODO: 两个声明都用这个 typedef。",
    "TODO: use type-generic sqrt.": "TODO: 用类型通用的 sqrt。",
    "TODO: validate every part of the conversion.":
        "TODO: 校验转换的每一个环节。",
    "TODO: visit every element.": "TODO: 访问到每一个元素。",
    "TODO: write into the nested city field.":
        "TODO: 写进嵌套的 city 字段。",
    "TODO: write name followed by age.":
        "TODO: 先写名字，再写年龄。",
    "TODO: write one complete record.":
        "TODO: 写出完整的一条记录。",
    "TODO: write the current character.":
        "TODO: 写出当前字符。",
    "TODO: write the supplied text.": "TODO: 写入传进来的文本。",
    "TODO: write through the pointer, not to the local parameter.":
        "TODO: 通过指针写，不要只给本地参数赋值。",
    "TODO: zero-pad the value to width 8.":
        "TODO: 把值补零到宽度 8。",
    "TODO: match the type in value.c.":
        "TODO: 让这里的类型与 value.c 里的定义一致。",
    "Thin assertion interface for clings exercises.":
        "clings 练习用的轻量断言接口。",
    "The implementation lives in test.c, so including this header does not":
        "实现放在 test.c 里，所以包含这个头文件并不会",
    "transitively provide stdio.h, stdlib.h, or string.h to exercise code.":
        "顺带把 stdio.h、stdlib.h、string.h 带进练习代码。",
}

# Whole-line replacements for lines that are not plain comment payloads.
LINES: dict[str, str] = {
    "#if defined(__STDC_VERSION__) && /* TODO: test for C11 or newer. */":
        "#if defined(__STDC_VERSION__) && /* TODO: 判断是否为 C11 或更新版本。 */",
    "Run an exercise with:": "运行练习：",
    "| Exercise | Objective |": "| 练习 | 目标 |",
    "# Basics": "# 基础",
    "# Preprocessor Directives": "# 预处理指令",
    "# Macros and Macro Hygiene": "# 宏与宏卫生",
    "# Types, Variables, and Storage": "# 类型、变量与存储",
    "# Operators and Expressions": "# 运算符与表达式",
    "# Control Flow": "# 控制流",
    "# Functions and Scope": "# 函数与作用域",
    "# Pointers": "# 指针",
    "# Arrays and Strings": "# 数组与字符串",
    "# Dynamic Memory": "# 动态内存",
    "# Structs, Unions, Enums, and Bitfields": "# 结构体、联合体、枚举与位域",
    "# Data Representation": "# 数据表示",
    "# Standard Library": "# 标准库",
    "# Character I/O": "# 字符 I/O",
    "# File I/O": "# 文件 I/O",
    "# Undefined Behavior, Safety, and Portability":
        "# 未定义行为、安全与可移植性",
    "# Data Structures": "# 数据结构",
    "# Translation Units and Linkage": "# 编译单元与链接",
    "# Advanced C": "# 高级 C",
    "# Modern C Library": "# 现代 C 库",
}

# User-facing strings inside the runner.  Each entry is (English source text,
# Chinese replacement); every one must match the upstream runner exactly once
# (or more, for text that repeats), otherwise sync fails loudly.
RUNNER: list[tuple[str, str]] = [
    ('description="Run and verify the clings C exercises.",',
     'description="编译并运行 clings 的 C 语言练习。",'),
    ('help="list all exercises"', 'help="列出全部练习"'),
    ('help="show the next exercise"', 'help="显示下一个练习"'),
    ('help="compile and run an exercise"', 'help="编译并运行一个练习"'),
    ('help="run every exercise"', 'help="运行全部练习"'),
    ('help="keep going after a failure"', 'help="失败后继续往下跑"'),
    ('help="show a hint"', 'help="查看提示"'),
    ('help="show or apply a solution"', 'help="查看或应用参考答案"'),
    ('help="copy the solution over the exercise"',
     'help="把参考答案写到练习文件上"'),
    ('help="restore the original exercise"', 'help="恢复初始练习"'),
    ('help="verify every solution"', 'help="校验全部参考答案"'),
    ('help="check exercises start broken and solutions pass"',
     'help="检查练习初始失败、参考答案通过"'),
    ('help="show toolchain information"', 'help="显示工具链信息"'),
    ('help="re-run an exercise on change"', 'help="文件变化后自动重跑"'),
    ('help="remove compiled artifacts"', 'help="删除编译产物"'),
    ('print(red("no exercises found"))', 'print(red("没有找到任何练习"))'),
    ('print(red(f"ambiguous exercise: {needle}"))',
     'print(red(f"练习名有歧义: {needle}"))'),
    ('print(red(f"unknown exercise: {needle}"))',
     'print(red(f"找不到这个练习: {needle}"))'),
    ('return False, "compilation failed\\n" + build.stdout',
     'return False, "编译失败\\n" + build.stdout'),
    ('return False, "exercise timed out after 10 seconds"',
     'return False, "练习运行超过 10 秒，已中止"'),
    ('return False, "solution compilation failed\\n" + build.stdout',
     'return False, "参考答案编译失败\\n" + build.stdout'),
    ('return False, "solution timed out after 10 seconds"',
     'return False, "参考答案运行超过 10 秒，已中止"'),
    ('return False, f"missing solution: {exercise.solution_root}"',
     'return False, f"找不到参考答案: {exercise.solution_root}"'),
    ('meta.get("hint", "No hint available.")', 'meta.get("hint", "暂无提示。")'),
    ('green("done") if exercise.ident in completed else yellow("todo")',
     'green("已完成") if exercise.ident in completed else yellow("待完成")'),
    ('print(f"\\n{completed_count}/{len(exercises)} completed")',
     'print(f"\\n已完成 {completed_count}/{len(exercises)}")'),
    ('print(green("All exercises are complete. Try `./clings verify`."))',
     'print(green("所有练习都完成了。可以运行 `./clings verify` 做一次全量校验。"))'),
    ('print(f"\\n{cyan(\'running\')} {exercise.ident} - {exercise.title}")',
     'print(f"\\n{cyan(\'运行\')} {exercise.ident} - {exercise.title}")'),
    ('print(green("  passed"))', 'print(green("  通过"))'),
    ('print(red("  failed"))', 'print(red("  未通过"))'),
    ('print(red(f"\\n{failures} exercise(s) failed"))',
     'print(red(f"\\n{failures} 个练习未通过"))'),
    ('print(green("\\nall selected exercises passed"))',
     'print(green("\\n选中的练习全部通过"))'),
    ('print(f"objective: {exercise.objective}")',
     'print(f"学习目标: {exercise.objective}")'),
    ('print(f"reference: {exercise.reference}")',
     'print(f"参考资料: {exercise.reference}")'),
    ('print(f"hint: {exercise.hint}")', 'print(f"提示: {exercise.hint}")'),
    ('print(red(f"missing solution: {exercise.solution_root}"))',
     'print(red(f"找不到参考答案: {exercise.solution_root}"))'),
    ('print(green(f"applied solution to {exercise.path.parent}"))',
     'print(green(f"已把参考答案写到 {exercise.path.parent}"))'),
    ('print(green(f"applied solution to {exercise.path}"))',
     'print(green(f"已把参考答案写到 {exercise.path}"))'),
    ('print(red(f"missing template: {exercise.template_root}"))',
     'print(red(f"找不到初始模板: {exercise.template_root}"))'),
    ('print(green(f"reset {exercise.ident}"))',
     'print(green(f"已重置 {exercise.ident}"))'),
    ('print(f"{red(\'FAIL\')} solution {exercise.ident}")',
     'print(f"{red(\'FAIL\')} 参考答案 {exercise.ident}")'),
    ('print(f"{red(\'FAIL\')} exercise {exercise.ident} already passes")',
     'print(f"{red(\'FAIL\')} 练习 {exercise.ident} 初始状态就通过了")'),
    ('print(red(f"\\n{failures} solution(s) failed"))',
     'print(red(f"\\n{failures} 个参考答案未通过"))'),
    ('print(green(f"\\nall {len(exercises)} solutions passed"))',
     'print(green(f"\\n{len(exercises)} 个参考答案全部通过"))'),
    ('print(red(f"\\n{failures} selftest failure(s)"))',
     'print(red(f"\\n{failures} 项自检未通过"))'),
    ('print(green(f"\\nall {len(exercises)} exercises behave correctly"))',
     'print(green(f"\\n{len(exercises)} 个练习的初始状态都符合预期"))'),
    ('print(f"python:   {platform.python_version()}")',
     'print(f"Python:   {platform.python_version()}")'),
    ('print(f"platform: {platform.platform()}")',
     'print(f"系统:     {platform.platform()}")'),
    ('print(f"root:     {ROOT}")', 'print(f"项目目录: {ROOT}")'),
    ('print(f"compiler: {compiler()}")', 'print(f"编译器:   {compiler()}")'),
    ('print(f"flags:    {\' \'.join(cflags())}")',
     'print(f"编译参数: {\' \'.join(cflags())}")'),
    ('print(result.stdout.splitlines()[0] if result.stdout else "compiler not found")',
     'print(result.stdout.splitlines()[0] if result.stdout else "没有找到编译器")'),
    ('print(f"watching {exercise.ident}; press Ctrl-C to stop")',
     'print(f"正在监视 {exercise.ident}；按 Ctrl-C 退出")'),
    ('print(green(f"removed {BUILD_DIR}"))',
     'print(green(f"已删除 {BUILD_DIR}"))'),
    ('print("nothing to clean")', 'print("没有需要清理的编译产物")'),
    ('print("\\ninterrupted")', 'print("\\n已中断")'),
]
