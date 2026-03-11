---
title: "时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞"
source: https://mrxn.net/jswz/bjskzy-getRemoteAddr-getClientIP-xff-df.html
asset_dir: assets/时空智友企业流程化管控系统-getremoteaddr-设计缺陷漏洞
---

# 时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/14 08:29
- 612浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

JSON处理工具

安全研究工具

SQL注入检测工具

---

# 漏洞简介

时空智友企业流程化管控系统是一款基于JAVA开发的企业信息管理[软件](#)，致力于协助大健康企业构建内部信息化，解决GSP管理、多组织管理、财务管理、税控管理、线上线下一体化等问题，帮助企业实现流程化管控，提高工作效率和管理水平。时空智友企业流程化管控系统 `getRemoteAddr` 存在设计缺陷[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，攻击者可利用header头伪造访问IP。

漏洞扫描服务

# 影响版本

# fofa语法

> `app="时空智友V10.1" || app="时空智友-企业信息系统" || app="时空智友-企业管理"`

# 漏洞分析

直接看 `GeneralUtility.getRemoteAddr` 方法的实现，如下

```
public static String getRemoteAddr(HttpServletRequest request) {
    if (request == null) {
        return "unknown";
    } else {
        String ip = request.getHeader("x-forwarded-for");
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Proxy-Client-IP");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("X-Forwarded-For");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("WL-Proxy-Client-IP");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Cdn-Src-Ip");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("X-Real-IP");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }

        return "0:0:0:0:0:0:0:1".equals(ip) ? "127.0.0.1" : ip;
    }
}
```

执行流程如下

软件

[![时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞](images/img-001-2ac6b28d7949.webp)](https://image.mrxn.net/ff670b1a7a904b0ca68bc7897d81fed0.webp)

再找一个调用 `GeneralUtility.getRemoteAddr` 方法的地方

漏洞扫描服务

```
public class UtilityServiceImpl {
    private static Logger a = LoggerFactory.getLogger(UtilityServiceImpl.class);

    public String getClientIP(HttpServletRequest var1, HttpServletResponse var2) {
        return GeneralUtility.getRemoteAddr(var1);
    }
```

# 漏洞复现

```
GET /formservice?service=utility.getClientIP HTTP/1.1
Host: bjskzy.mrxn.net
X-Forwarded-For: 127.0.0.2
```

在响应里可以看到获取到的IP就是我们header的xff伪造IP。

[![时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞](images/img-002-bae3fc0a8d00.webp)](https://image.mrxn.net/e088c6e97cbf4d18a8ec13cd37c5d527.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
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
