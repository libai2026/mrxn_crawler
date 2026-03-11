---
title: "emlog 使用ssl证书开启HTTPS安全访问三步曲"
source: https://mrxn.net/jswz/emlog-https-ssl.html
asset_dir: assets/emlog-使用ssl证书开启https安全访问三步曲
---

# emlog 使用ssl证书开启HTTPS安全访问三步曲

[Mrxn](https://mrxn.net/author/1)- 发表于2015/9/17 18:45
- 29796浏览
- [39评论](#comment)
- 29分钟阅读

深入探索

网络安全课程

在线安全工具

Web安全课程

---

[[![emlog 使用ssl证书开启HTTPS安全访问三步曲](images/img-001-f92e88c39ee6.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201509/3fb51442491145.jpg)](https://mrxn.net/content/uploadfile/201509/3fb51442491145.jpg)

最近在研究ssl，所以就给自己得博客使用了ssl，拿自己的博客实战研究ssl，哈哈，废话不说，如果你也想体验一下ssl，那就开始吧：

科普一下（ssl有啥好处呢）：参考-[浅谈HTTPS链接的重要性和安全性](https://mrxn.net/ssl-https.html "链接到 浅谈HTTPS链接的重要性和安全性") 这篇文章。

ssl传送大概示意图：[[![emlog 使用ssl证书开启HTTPS安全访问三步曲](images/img-002-a4919b02ba55.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201509/4efd1442491145.jpg)](https://mrxn.net/content/uploadfile/201509/4efd1442491145.jpg)

emlog配置ssl很简单，只需要三步：

安全研究工具

深入探索

Web安全书籍

安全

传输层安全性协议

第一步：申请ssl证书，学习研究推荐使用免费的ssl证书（如果你是土豪，请无视-\_-|），申请教程不写了，没时间，google搜索一大把。

技术文章订阅

第一个：https://www.startssl.com/ 第二个：https://www.wosign.com/  第一个是英语的，如果看不懂就用第二个国内的，但是国内的只支持sha1算法，国外的可以选择sha2-256位RSA公钥，和4096位的服务器crt身份密钥，更高的加密算法。效果请查看[我的网站](https://mrxn.net)。

申请成功解压之后，文件目录结构如下图所示：

[[![emlog 使用ssl证书开启HTTPS安全访问三步曲](images/img-003-d416576e88aa.png "点击查看原图")](https://mrxn.net/content/uploadfile/201509/thum-96751442492124.png)](https://mrxn.net/content/uploadfile/201509/96751442492124.png)

因为这里我们是用NGINX WEB环境的，所以我们需要解压FOR NGINX.ZIP文件包，然后看到一个CRT一个KEY文件。

搜索引擎

第二步、上传和部署SSL证书
A - 把上面的一个CRT一个KEY文件上传到VPS ROOT目录中，然后对应修改成SSL.CRT和SSL.KEY文件名，或者我们用作其他命令都可以。
B - 解密私钥和设置权限

```
openssl rsa -in ssl.key -out /root/ssl.key
chmod 600 /root/ssl.key
```

登录SSH，执行上述两行脚本，解密私钥和授权。

第三步、在LNMP环境部署站点SSL设置

我们需要在已有的LNMP添加了站点，然后在站点对应的CONF文件设置。

深入探索

网络安全培训

编码转换工具

Nessus

在"/usr/local/nginx/conf/vhost/"目录文件中，找到对应站点的conf文件，然后修改设置如下

网络安全

```
server
{
 listen 80;
 listen 443 ssl;
#listen [::]:80;
ssl on;
        ssl_certificate /root/ssl.crt;
        ssl_certificate_key /root/ssl.key;
server_name mrxn.net mrxn.net;
```

/root/ssl.crt 是我自己的设置，对应路径我们要与之前上传的CRT和KEY文件路径对应以及文件名不要搞错。

最后，我们重启LNMP，可以看到SSL证书生效，且HTTPS可以访问站点。

[[![emlog 使用ssl证书开启HTTPS安全访问三步曲](images/img-004-fee787b444dd.png "点击查看原图")](https://mrxn.net/content/uploadfile/201509/5f3b1442492780.png)](https://mrxn.net/content/uploadfile/201509/5f3b1442492780.png)

这是在网站所有资源都在本域名下，而且是https 加密安全访问的情况下。一般你一操作完都不是这样的，而是这样的：

安全研究工具

[[![emlog 使用ssl证书开启HTTPS安全访问三步曲](images/img-005-fe6f0b02330b.png "点击查看原图")](https://mrxn.net/content/uploadfile/201509/79d51442492780.png)](https://mrxn.net/content/uploadfile/201509/79d51442492780.png)

小锁头上面有一个感叹号标志的，如何解决呢：

首先是在后台设置域名地址为：https://mrxn.net 然后，修改 /include/lib/function.base.php ，把头像获取的链接修改成https://开头的：$avatar = "https://cn.gravatar.com/avatar/$hash?s=$s&d=$d&r=$g"; 再回来  数据--更新缓存 之后，打开首页 Ctrl + F5 基本上就是绿色的小箭头了。

如果还没有呢，那多半就是你文章的图片地址是 https://mrxn.net 这样开头的，所以，直接更新数据库的blog表的content和excerpt字段即可：

```
update emlog_blog set content=replace(content,'https://mrxn.net','https://mrxn.net');
```

```
update emlog_blog set excerpt=replace(excerpt,'https://mrxn.net','https://mrxn.net'); 
```

这样更新完数据库之后，你的网站就基本上全部替换完了非加密连接了（内容页和摘要都更新了，其他的地方貌似没有了，自己写的不算）。  
**如果我们需要强制使用HTTPS网址访问，那我们就需要取掉 listen 80;脚本。或者是在 **listen 80;前面加上# 修改成：**#**listen 80;****

最终修改配置大概如下：

```
server
    {
        #listen 80;
        listen 443 ssl;
        #listen [::]:80;
        ssl on;
        ssl_certificate 存放ssl证书文件路径.crt;
        ssl_certificate_key 存放ssl证书文件路径.key;
        server_name mrxn.net mrxn.net;
        index index.html index.htm index.php default.html default.htm default.php;
        root  网站存放文件路径;
        keepalive_timeout   60;
       .......此处省略.......
    }
server {
listen 80;
server_name mrxn.net mrxn.net;
return 301 https://mrxn.net$request_uri;
}
```

注意将域名修改成你自己的域名。至此，基本上就完成了ssl证书的安装，开启https访问了。

**相关文章：**

## [一段代码让nginx实现网站资源防盗链](https://mrxn.net/block-file-nginx-protect.html "链接到 一段代码让nginx实现网站资源防盗链")

## [nginx配置location总结及rewrite规则写法](https://mrxn.net/nginx-location-rewrite.html "链接到 nginx配置location总结及rewrite规则写法")

## [nginx配置ssl加密（单双向认证、部分https）](https://mrxn.net/nginx-ssl.html "链接到 nginx配置ssl加密（单双向认证、部分https）")

## [NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](https://mrxn.net/nginx-ua-https.html "链接到 NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转")

## [SSL/TLS原理详解](https://mrxn.net/tls-ssl-understand.html "链接到 SSL/TLS原理详解")

## [OpenSSL 与 SSL 数字证书概念贴](https://mrxn.net/openssl-certificate-encryption.html "链接到 OpenSSL 与 SSL 数字证书概念贴")

## [基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/openssl-self-sign-ca.html "链接到 基于OpenSSL自建CA和颁发SSL证书")

最后呢，希望有高手带我学习https方面的东西呀，这篇文章呢，也希望对想要使用ssl的童鞋一点帮助，如果哪位看官有更好的方法或者是建议，欢迎留言/评论 不吝赐教啊，我洗耳恭听，多帮忙吧 谢谢。

- 标签：
- [#攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
- [#黑客](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2)
- [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
- [#防范](https://mrxn.net/tag/%E9%98%B2%E8%8C%83)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#ssl](https://mrxn.net/tag/ssl)
- [#https](https://mrxn.net/tag/https)

---

文章目录

- [1.
  一段代码让nginx实现网站资源防盗链](#toc-1-)
- [2.
  nginx配置location总结及rewrite规则写法](#toc-2-)
- [3.
  nginx配置ssl加密（单双向认证、部分https）](#toc-3-)
- [4.
  NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](#toc-4-)
- [5.
  SSL/TLS原理详解](#toc-5-)
- [6.
  OpenSSL 与 SSL 数字证书概念贴](#toc-6-)
- [7.
  基于OpenSSL自建CA和颁发SSL证书](#toc-7-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
