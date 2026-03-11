---
title: "NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转"
source: https://mrxn.net/jswz/nginx-ua-https.html
asset_dir: assets/nginxrewrite规则判断普通用户与搜索引擎爬虫（ua）实现https跳转
---

# NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转

[Mrxn](https://mrxn.net/author/1)- 发表于2015/9/24 21:26
- 22510浏览
- [16评论](#comment)
- 11分钟阅读

深入探索

user\_agent

用户代理

软件

---

[[![NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](images/img-001-c514461eb26d.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201509/187f1443105009.jpg)](https://mrxn.net/content/uploadfile/201509/187f1443105009.jpg)

前段时间写了一篇关于给博客安装证书加密访问的文章，在站长平台，百度说支持https，一个月后发现网站的流量排名跌成了狗，为了逼格保留这个https，又为了不和百度做对，查阅相关资料后选择用user\_agent来解决，nginx本身就能判断UA，以下代码供大家参考，添加到nginxRewr**it**e配置文件里即可，**域名**换成自己的。

[[![NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](images/img-002-64736030295c.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201509/36e51443105060.jpg)](https://mrxn.net/content/uploadfile/201509/36e51443105060.jpg)

具体的代码如下（复制吧-骚年）：

搜索引擎优化与营销

深入探索

安全认证考试

VPN服务

安全研究工具

```
server {
listen 80;
server_name mrxn.net mrxn.net;
set $flag 0;
if ($host != 'mrxn.net') {
 set $flag 1;
}
if ($server_port = 80) {
 set $flag 1;
}
if ($scheme = http) {
 set $flag 1;
}
if ($http_user_agent ~* (baiduspider|soso|sogou|yahoo|sohu-search|yodao|YoudaoBot|robozilla|msnbot|MJ12bot|NHN|Twiceler)){
 set $flag 2;
}
if ($flag = 1){
 rewrite ^/(.*)$ https://mrxn.net/$1 redirect;
}
error_page 497 https://mrxn.net$request_uri;

}
```

深入探索

SQL注入防护

Web安全课程

网络安全课程

这段规则具体作用是：将国内部分对https支持不好的[搜索引擎](#)蜘蛛定向到http页面，将普通用户和其他搜索引擎定向到https页面（谷歌更喜欢https站点）。

互联网与电信

相关文章：

## [一段代码让nginx实现网站资源防盗链](https://mrxn.net/block-file-nginx-protect.html "链接到 一段代码让nginx实现网站资源防盗链")

## [nginx配置location总结及rewrite规则写法](https://mrxn.net/nginx-location-rewrite.html "链接到 nginx配置location总结及rewrite规则写法")

## [nginx配置ssl加密（单双向认证、部分https）](https://mrxn.net/nginx-ssl.html "链接到 nginx配置ssl加密（单双向认证、部分https）")

## [NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](https://mrxn.net/nginx-ua-https.html "链接到 NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转")

## [SSL/TLS原理详解](https://mrxn.net/tls-ssl-understand.html "链接到 SSL/TLS原理详解")

## [OpenSSL 与 SSL 数字证书概念贴](https://mrxn.net/openssl-certificate-encryption.html "链接到 OpenSSL 与 SSL 数字证书概念贴")

## [基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/openssl-self-sign-ca.html "链接到 基于OpenSSL自建CA和颁发SSL证书")

原文属于博友创造：https://tmy123.com/user-agent.html

技术文章订阅

- 标签：
- [#ssl](https://mrxn.net/tag/ssl)
- [#https](https://mrxn.net/tag/https)
- [#nginx](https://mrxn.net/tag/nginx)
- [#vps](https://mrxn.net/tag/vps)
- [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

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
