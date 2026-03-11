---
title: "快普M6 WebService/SeatManageService.asmx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/kuaipu-M6-WebService-SeatManageService-sqli.html
asset_dir: assets/快普m6-webserviceseatmanageservice.asmx-多处sql注入漏洞
---

# 快普M6 WebService/SeatManageService.asmx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/24 08:25
- 806浏览
- [0评论](#comment)
- 34分钟阅读

深入探索

WebService

软件

数据库

---

# 漏洞简介

快普M6整合管理平台的[WebService](#)/SeatManageService.asmx接口下多个方法存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，绕过参数过滤机制，实现对数据库的任意查询、修改或删除操作，甚至可能获取系统控制权限。

网络服务

# 影响版本

# fofa语法

> body="Resource/JavaScript/jKPM6.DateTime.js"

# 漏洞分析

深入探索

物流软件安全

防火墙软件

在线安全工具

根据漏洞通告，看下 WebService/SeatManageService.asmx 里的cs引用

```
<%@ WebService Language="C#" CodeBehind="SeatManageService.asmx.cs" Class="KPMIIS.Web.WebService.SeatManageService" %>
```

ok,根据引用去找到bin目录下的**KPMIIS.Web.dll**文件，反编译后找到`WebService`下的**SeatManageService**实现

```
public class SeatManageService : System.Web.Services.WebService
{
  [WebMethod]

public string GetCallInfo(string strCallNo)
{
  DataSet dataSet = Gateway.Default.FromCustomSql($"SELECT A.CManName,A.CPosting,C.CustName FROM dbo.Common_CustomerLinkman A LEFT JOIN COMMON_CustomerToLinkMan  B ON A.CManId=B.LinkMan_ID LEFT JOIN dbo.Common_Customer C ON C.CustId=B.CUSTOMER_ID  WHERE A.COfficeTel1 LIKE '%{strCallNo}%' OR A.CMobile1 LIKE '%{strCallNo}%' ORDER BY B.IS_IMPORTANCE_LINKMAN DESC, B.IS_IMPORTANCE_CUSTOMER DESC").ToDataSet();

  public string GetCustInfo(string strCallNo)
{
  DataSet dataSet = Gateway.Default.FromCustomSql($"SELECT A.CManId,C.CustId FROM dbo.Common_CustomerLinkman A LEFT JOIN COMMON_CustomerToLinkMan  B ON A.CManId=B.LinkMan_ID LEFT JOIN dbo.Common_Customer C ON C.CustId=B.CUSTOMER_ID  WHERE A.COfficeTel1 = '{strCallNo}' OR A.CMobile1 = '{strCallNo}' ORDER BY B.IS_IMPORTANCE_LINKMAN DESC, B.IS_IMPORTANCE_CUSTOMER DESC").ToDataSet();

  private void AddPhoneRecordInfo(
  int intPhoneTypeId,
  string strPhoneNo,
  string strTelNumber,
  string strStartTime,
  string strEndTime,
  string strPath,
  int intTime,
  string strUniqueId)
{
  strPath = strPath.Replace("/", "\\");
  string empty = string.Empty;
  int num1 = 0;
  CRM_PhoneRecordInfo model = new CRM_PhoneRecordInfo();
  model.ACCOUNT = "";
  model.IS_DELETE = new int?(0);
  model.PHONE_TYPE_ID = new int?(intPhoneTypeId);
  if (intPhoneTypeId != 3)
  {
    string[] strArray = this.GetCustInfo(strTelNumber).Split(new char[1]
    {
      ','
    });
    model.CUSTOMER_ID = new int?(strArray[0].ToInt());
    model.LINKMAN_ID = new int?(strArray[1].ToInt());
  }
  if (strPhoneNo.Length > 0)
  {
    int num2 = strPhoneNo.IndexOf('(') + 1;
    int num3 = strPhoneNo.IndexOf(')');
    if (num2 > 0)
      strPhoneNo = strPhoneNo.Substring(num2, num3 - num2);
    string sql = $"SELECT csi.STAFF_ID,csi.STAFF_NAME FROM COMMON_UserPhoneNo cupn LEFT JOIN COMMON_StaffInfo csi ON csi.USER_INT_ID = cupn.USER_INT_ID WHERE cupn.PHONE_NO='{strPhoneNo}'";
    DataTable table = Gateway.Default.FromCustomSql(sql).ToDataSet().Tables[0];
```

三个方法 `GetCallInfo`、`GetCustInfo`和`AddPhoneRecordInfo`都是差不多的处理逻辑，其中都存在关键参数`strCallNo`、`strPhoneNo`，没有经过任何过滤或校验检查就被拼接进SQL语句中进行执行了，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，非常的朴实无华。

SQL注入检测工具

# 漏洞复现

> 漏洞复现，可以用过SOAPUI 或者 burp的Wsdler插件解析后直接测试

```
POST /WebService/SeatManageService.asmx HTTP/1.1
Host: kuaipu.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="http://tempuri.org/GetCallInfo"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:GetCallInfo>
         <!--Optional:-->
         <tem:strCallNo>SQLI_POC</tem:strCallNo>
      </tem:GetCallInfo>
   </soap:Body>
</soap:Envelope>
```

[![快普M6 WebService/SeatManageService.asmx 多处SQL注入漏洞](images/img-001-caaae7f587b8.webp)](https://image.mrxn.net/aa6690004d8840e28e86599d08ea366d.webp)

成功通过[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显数据库默认用户dbo

代码安全审计

其他两个方法的sql注入也类似，只是需要的参数不同罢了，同时给接口还支持常规的GET、POST请求方式。

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

编程
