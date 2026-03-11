---
title: "利用file_put_contents()函数写shell的小trick"
source: https://mrxn.net/jswz/php-file_put_contents_w-shell.html
asset_dir: assets/利用file_put_contents()函数写shell的小trick
---

# 利用file\_put\_contents()函数写shell的小trick

[Mrxn](https://mrxn.net/author/1)- 发表于2017/9/20 20:55
- 7439浏览
- [2评论](#comment)
- 10分钟阅读

深入探索

传输层安全性协议

数据库

安全研究工具

---

首先不了解PHP的file\_put\_contents()函数的自己去这里看一下官方给出的解释：

软件

[http://php.net/manual/zh/function.file-put-contents.php](http://php.net/manual/zh/function.file-put-contents.php "put_file_contents()")

[[![利用file_put_contents()函数写shell的小trick](images/img-001-b3795a248dbe.png "点击查看原图")](../content/uploadfile/201709/1c6e1505914096.png)](../content/uploadfile/201709/1c6e1505914096.png)

思路大致如下：

深入探索

SQL

恶意软件分析工具

服务器安全服务

file\_put\_contents()在写入文件时的第二个参数可以传入数组，如果是数组的话，将被连接成字符串再进行写入。在正则匹配前，传入的是一个数组。得益于PHP的弱类型特性，数组会被强制转换成字符串，也就是**Array**，**Array**肯定是满足正则**\A[ \_a-zA-Z0-9]+\z**的，所以不会被拦截。这样就可以绕过类似检测*“<?”*之类的waf。

> 下面是测试的代码：
>
> <?php  
> header("Content-type: text/html; charset=utf-8");  
> /\*  
> 测试file\_put\_contents数组写shell  
> modify:Mrxn  
> Blog:https://mrxn.net/  
>  \*/  
> echo "just a shell test!";   
> $text = $\_GET['text'];  
> if (preg\_match('[<>?]', $text)) {  
>  die('erro!');  
> }  
> echo '<br>'.'下面就是text的内容:'.'<br>';  
> echo $text;  
> echo '<br>';  
> var\_dump($text) ;  
> file\_put\_contents('config.php', $text);  
>  ?>

我们访问后,通过自己定义text可以实时得到反馈,便于测试:

软件

[[![利用file_put_contents()函数写shell的小trick](images/img-002-545953762c4c.png "点击查看原图")](../content/uploadfile/201709/bbb71505914096.png)](../content/uploadfile/201709/bbb71505914096.png)

代码检测了写入的内容是否存在“<”“>”“?”等字符。根据上面的trick，我们可以通过传入一个数组来达到写入shell的目的。可以看到虽然有个警告。但config.php确实被写入了。<? php phpinfo(); 如下所示:[[![利用file_put_contents()函数写shell的小trick](images/img-003-34745c01a32e.png "点击查看原图")](../content/uploadfile/201709/12031505914096.png)](../content/uploadfile/201709/12031505914096.png)

注:这个不是我发现的,是在P牛的小蜜圈发现的.只是自己亲自测试了一下,将代码略作修改,便于新手理解!)\_我就是说我自己是个新手-\_- 囧| 逃 :)

技术文章订阅

我们下次再见...

ps:友情链接里面,有看到的自己帮忙加上,一个月后没有加的我就删除了.

- 标签：
- [#shell](https://mrxn.net/tag/shell)
- [#php](https://mrxn.net/tag/php)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
