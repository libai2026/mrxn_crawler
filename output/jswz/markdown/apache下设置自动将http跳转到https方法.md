---
title: "Apache下设置自动将http跳转到https方法"
source: https://mrxn.net/jswz/Apache-http-to-https-htaccess.html
asset_dir: assets/apache下设置自动将http跳转到https方法
---

# Apache下设置自动将http跳转到https方法

[Mrxn](https://mrxn.net/author/1)- 发表于2015/12/2 18:53
- 9667浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

虚拟机

软件

认证

---

今天有朋友问我怎么配置虚拟机，使其支持访问者打开首页时自动跳转到https，而非http，因为是虚拟机，重复-虚拟机，所以呢，配置服务器的那些方法不好使，搜索得到如下方法，利用修改 伪静态规则 文件- .htaccess ，使虚拟机也可以支持直接打开网站跳转到https，具体方法如下，在htaccess文件末尾添加如下代码即可实现：

计算机服务器

```
RewriteCond %{SERVER_PORT} !^443$
RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
```

[[![Apache下设置自动将http跳转到https方法](images/img-001-95b8eb10c4f8.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201512/thum-b5721449057345.jpg)](https://mrxn.net/content/uploadfile/201512/b5721449057345.jpg)

一行一条命令，其实就是利用伪静态将访问者跳转到443端口，从而实现了http到https的跳转。

**注：**此为虚拟机的方法，推荐使用服务器自己配置https，虚拟机的这样配置后，有可能导致蜘蛛不能抓取你的网站，对SEO不好，慎重选择！

操作前记得备份相关文件，以及数据！

服务器配置https方面可以参考如下文章：

操作系统

## [emlog 使用ssl证书开启HTTPS安全访问三步曲](https://mrxn.net/emlog-https-ssl.html)

## [nginx配置ssl加密（单双向认证、部分https）](https://mrxn.net/nginx-ssl.html)

## [NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳](https://mrxn.net/nginx-ua-https.html)转

深入探索

云安全解决方案

Nessus

数据库

## [SSL证书与Https应用部署小结](https://mrxn.net/https-apply-all.html)

- 标签：
- [#加密通讯](https://mrxn.net/tag/%E5%8A%A0%E5%AF%86%E9%80%9A%E8%AE%AF)
- [#emlog](https://mrxn.net/tag/emlog)
- [#http](https://mrxn.net/tag/http)
- [#ssl](https://mrxn.net/tag/ssl)
- [#https](https://mrxn.net/tag/https)
- [#nginx](https://mrxn.net/tag/nginx)
- [#vps](https://mrxn.net/tag/vps)
- [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)
- [#加密](https://mrxn.net/tag/%E5%8A%A0%E5%AF%86)

---

文章目录

- [1.
  emlog 使用ssl证书开启HTTPS安全访问三步曲](#toc-1-)
- [2.
  nginx配置ssl加密（单双向认证、部分https）](#toc-2-)
- [3.
  NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](#toc-3-)
- [4.
  SSL证书与Https应用部署小结](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
