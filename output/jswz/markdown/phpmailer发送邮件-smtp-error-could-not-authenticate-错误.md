---
title: "phpmailer发送邮件 SMTP Error: Could not authenticate 错误"
source: https://mrxn.net/jswz/phpmailer.html
asset_dir: assets/phpmailer发送邮件-smtp-error-could-not-authenticate-错误
---

# phpmailer发送邮件 SMTP Error: Could not authenticate 错误

[Mrxn](https://mrxn.net/author/1)- 发表于2015/10/8 20:33
- 9796浏览
- [3评论](#comment)
- 18分钟阅读

深入探索

Sendmail

authenticate

库

---

今天在使用sendmail插件(phpmailer)发送邮件时居然提示SMTP Error: Could not authenticate，这个感觉是smtp设置的问题，下面我在网上找到了几种解决办法。

电子邮件与即时消息

今天在使用phpmailer发送smtp邮件时提示 SMTP Error: Could not authenticate 错误，其中密码帐号都是正确的，邮箱也设置开启了SMTP功能。

上谷歌百度了一遍，有的说是服务器禁用了端口，有的说把class.phpmailer.php中的:

```
function IsSMTP() {
$this->Mailer = 'smtp';
}改为
function IsSMTP() {
$this->Mailer = 'SMTP';
}
```

  

测试以后还是不行，心中郁闷的一米。最后在一篇博客中找到了解决方法，先分享出来让更多遇到同样问题的人能得到帮助！

网络安全

这个错误说明虚拟主机不支持PHPMailer默认调用的fsockopen函数，找到class.smtp.php文件，搜索fsockopen，就找到了这样一段代码：

```
// connect to the smtp server
$this->smtp_conn = @fsockopen($host,// the host of the server
    $port,// the port to use
    $errno,   // error number if any
    $errstr,  // error message if any
    $tval);   // give up after ? secs
```

  

**方法1：将fsockopen函数替换成pfsockopen函数**

深入探索

VPN服务

计算机安全

JSON处理工具

首先，在php.ini中去掉下面的两个分号

;extension=php\_sockets.dll

;extension=php\_openssl.dll

然后重启一下

计算机服务器

因为pfsockopen的参数与fsockopen基本一致，所以只需要将@fsockopen替换成@pfsockopen就可以了。

**方法2：使用stream\_socket\_client函数**

一般fsockopen()被禁，pfsockopen也有可能被禁，所以这里介绍另一个函数stream\_socket\_client()。

stream\_socket\_client的参数与fsockopen有所不同，所以代码要修改为：

```
$this->smtp_conn = stream_socket_client("tcp://".$host.":".$port, $errno,  $errstr,  $tval);
```

  

这样就可以了。

深入探索

恶意软件分析工具

漏洞预警服务

Nessus

如果上面办法还是没有解决可能是邮箱自动过滤你机器自动登录邮箱发邮件了哦,我是使用下面办法解决的

刚开始使用的qq的帐号，提示上面错误。换成新注册的163帐号可以正常发送。

之后换了一个qq等级比较高的帐号，这下可以正常发送，没有报任何错误。

因为收件人用的是qq邮箱帐号，所以发件帐号用qq的邮箱比较好，这样发送过多不会轻易的被拦截或判为垃圾邮件。

所以结论就是配置中使用一个qq等级比较高的帐号（我的一个小号等级2个月亮可以正常使用，当然等级越高越好，）

ps：也要查看邮箱中“设置邮件地址黑名单”及“收信规则”，有时系统会自动将一些邮箱自动加入黑名单的

- 标签：
- [#编程](https://mrxn.net/tag/%E7%BC%96%E7%A8%8B)
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#php](https://mrxn.net/tag/php)
- [#vps](https://mrxn.net/tag/vps)
- [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
