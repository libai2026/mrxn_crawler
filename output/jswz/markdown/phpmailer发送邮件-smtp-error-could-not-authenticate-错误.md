---
title: "phpmailer发送邮件 SMTP Error: Could not authenticate 错误"
source: https://mrxn.net/jswz/phpmailer.html
asset_dir: embedded-base64
---

今天在使用sendmail插件(phpmailer)发送邮件时居然提示SMTP Error: Could not authenticate，这个感觉是smtp设置的问题，下面我在网上找到了几种解决办法。

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

这个错误说明虚拟主机不支持PHPMailer默认调用的fsockopen函数，找到class.smtp.php文件，[搜索](#)fsockopen，就找到了这样一段代码：

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

编程

数据管理

客户关系管理

首先，在php.ini中去掉下面的两个分号

;extension=php\_sockets.dll

;extension=php\_openssl.dll

然后重启一下

因为pfsockopen的参数与fsockopen基本一致，所以只需要将@fsockopen替换成@pfsockopen就可以了。

**方法2：使用stream\_socket\_client函数**

一般fsockopen()被禁，pfsockopen也有可能被禁，所以这里介绍另一个函数stream\_socket\_client()。

stream\_socket\_client的参数与fsockopen有所不同，所以代码要修改为：

```
$this->smtp_conn = stream_socket_client("tcp://".$host.":".$port, $errno,  $errstr,  $tval);
```

  

这样就可以了。

深入探索

商务软件和生产力软件

软件

编程

如果上面办法还是没有解决可能是邮箱自动过滤你机器自动登录邮箱发邮件了哦,我是使用下面办法解决的

刚开始使用的qq的帐号，提示上面错误。换成新注册的163帐号可以正常发送。

之后换了一个qq等级比较高的帐号，这下可以正常发送，没有报任何错误。

因为收件人用的是qq邮箱帐号，所以发件帐号用qq的邮箱比较好，这样发送过多不会轻易的被拦截或判为垃圾邮件。

所以结论就是配置中使用一个qq等级比较高的帐号（我的一个小号等级2个月亮可以正常使用，当然等级越高越好，）

ps：也要查看邮箱中“设置邮件地址黑名单”及“收信规则”，有时系统会自动将一些邮箱自动加入黑名单的
