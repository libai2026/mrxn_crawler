---
title: "深信服运维安全管理系统 protocol/session 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor-osm-protocol-session-rce.html
asset_dir: assets/深信服运维安全管理系统-protocolsession-远程命令执行漏洞
---

# 深信服运维安全管理系统 protocol/session 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/19 07:20
- 1307浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

服务器

ssh

SSH

---

# 漏洞简介

深信服运维安全管理系统 protocol/session 接口存在远程命令执行漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上[执行任意命令](https://mrxn.net/tag/rce)，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。

安全工具开发

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

直接看 `com.sbr.isomp.protocol.controller.session.SessionController` 的实现方式

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-001-a2b8caa3a3ac.webp)](https://image.mrxn.net/df21ae1f2c154f6e904d29c671fa19a2.webp)

从上图可以看到要进入此方法的路径是 **/protocol/session**

## ssh

然后继续看下面的实现

漏洞修复方案

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-002-ef3957992712.webp)](https://image.mrxn.net/0185645f597b488e8e0ccb0fe1f946a0.webp)

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-003-bc393b960c82.webp)](https://image.mrxn.net/e4c4418372864ad28cc46d10da1f6830.webp)

当 **protocol=ssh** 时，尝试从请求参数中获取 `keyPath`（私钥文件的路径）。如果路径存在且当前不是 SSH Daemon 模式（`sshd` 参数为 false）：

计算机服务器

1. **文件读取与类型检查**：它尝试读取用户提供的 `keyPath` 指向的文件内容。
2. **格式转换（如果需要）**：如果读取到的私钥内容不包含 PEM 格式的标识符（`RSA PRIVATE KEY` 或 `DSA PRIVATE KEY`），代码会尝试使用 `ssh-keygen` 命令行工具对该私钥文件进行格式转换，将其转换为 PEM 格式。
3. **命令行执行**：在格式转换过程中，它将用户提供的 `keypassword` 参数（如果存在）直接拼接到 `ssh-keygen` 的命令行参数中执行。
4. **会话存储**：无论是否发生异常，私钥文件的内容和私钥密码（`keypassword`）最终都会被读取并存储到会话对象中。

命令注入的关键点在于用户提供的 `keyPath` 和 `keypassword` 两个参数在未经过任何严格的沙盒或转义处理的情况下，直接拼接进了 `ShellExecutor.service().exe()` 执行的系统命令字符串中。

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-004-05b5b40cff26.webp)](https://image.mrxn.net/8631c889dc0e44ad98e44e2e86c02637.webp)

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-005-91d9c5904155.webp)](https://image.mrxn.net/1f9d687c06584d678914fd745bdeeaeb.webp)

攻击者可以通过在这些参数中注入分号或管道符等，造成任意[命令注入](https://mrxn.net/tag/rce)漏洞，执行任意的操作系统命令。

数据格式与协议

## x11

同样的问题也出现在当 **protocol=x11** 时，

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-006-ce4cea31f5eb.webp)](https://image.mrxn.net/22c2caddeab94c0886b58579ef38d176.webp)

首先尝试从 `resolution` 参数中解析出期望的会话宽度和高度，如果该参数为空，则使用默认值 1024x768。随后，它调用 `ShellExecutor` 执行一个 Bash 脚本 (`/usr/local/bin/sh/x11vnc.sh`)，并传入解析出的宽度、高度以及用户提供的 `hostname` 和 `port` 参数作为脚本的命令行参数。脚本执行结果会被记录并解析，如果成功，它会将脚本返回的新端口号更新到会话中。

代码安全审计

命令注入漏洞的关键在于处理用户提供的 `hostname` 和 `port` 参数，以及间接控制的 `resolution` 参数（如果解析失败或被恶意构造），都未经任何安全处理或转义，直接拼接到了 `bash` 命令的末尾。攻击者可以通过在 `hostname` 或 `port` 参数中注入 shell 元字符（如 `;`、`|`、`&`），在执行 `/usr/local/bin/sh/x11vnc.sh` 脚本的同时，执行任意的附加系统命令，从而实现[远程代码执行](https://mrxn.net/tag/rce)。

# 漏洞复现

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-007-788e654dca5b.webp)](https://image.mrxn.net/10424b4d902246808b34a079f0ac6837.webp)

## POC

### ssh

```
POST /isomp-protocol/protocol/session HTTP/1.1
Host: osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

protocol=ssh&keyPath=/etc/group&sshd=1&keypassword=RCE_POC
```

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-008-0fb5d9b02f6e.webp)](https://image.mrxn.net/6248f86bd94e4d819c8ab3aef327c1c9.webp)

获取到[命令执行](https://mrxn.net/tag/rce)的结果

### x11

```
POST /isomp-protocol/protocol/session HTTP/1.1
Host: osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

protocol=x11&port=1337&hostname=RCE_POC
```

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-009-6a1e3b9ae482.webp)](https://image.mrxn.net/75a45f1dd44748ff9af8167f73e5e98f.webp)

获取到[命令执行](https://mrxn.net/tag/rce)的结果（两个参数**hostname**和**port**均存在同样的命令注入漏洞）

漏洞修复方案

# 参考

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.ssh](#toc-4-1-)
- [4.2.x11](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [5.1.POC](#toc-5-1-)
- [5.1.1.ssh](#toc-5-1-1-)
- [5.1.2.x11](#toc-5-1-2-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
