---
title: "nginx配置ssl加密（单双向认证、部分https）"
source: https://mrxn.net/jswz/nginx-ssl.html
asset_dir: embedded-base64
---

# nginx配置ssl加密（单双向认证、部分https）

[Mrxn](https://mrxn.net/author/1)- 发表于2015/9/24 21:48
- 13252浏览
- [0评论](#comment)
- 1小时阅读

深入探索

安全

软件

网络安全会议

---

nginx下配置ssl本来是很简单的，无论是去认证中心买SSL安全证书还是自签署证书，但最近公司OA的一个需求，得以有个机会实际折腾一番。一开始采用的是全站加密，所有访问http:80的请求强制转换（rewrite）到https，后来自动化测试结果说响应速度太慢，https比http慢慢30倍，心想怎么可能，鬼知道他们怎么测的。所以就试了一下部分页面https（不能只针对某类动态请求才加密）和双向认证。下面分节介绍。

Windows安全工具

默认nginx是没有安装ssl模块的，需要编译安装nginx时加入`--with-http_ssl_module`选项。

关于SSL/TLS原理请参考 [这里](https://mrxn.net/tls-ssl-understand.html)，如果你只是想测试或者自签发ssl证书，参考 [这里](https://mrxn.net/openssl-self-sign-ca.html) 。

**提示**：nignx到后端服务器由于一般是内网，所以不加密。

# 1. 全站ssl

全站做ssl是最常见的一个使用场景，默认端口443，而且一般是单向认证。

```
server {
        listen 443;
        server_name example.com;
        root /apps/www;
        index index.html index.htm;
        ssl on;
        ssl_certificate ../SSL/ittest.pem;
        ssl_certificate_key ../SSL/ittest.key;
#        ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
#        ssl_ciphers ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
#        ssl_prefer_server_ciphers on;
}
```

深入探索

在线安全工具

传输层安全性协议

服务器安全服务

如果想把http的请求强制转到https的话：

```
server {
  listen      80;
  server_name example.me;
  rewrite     ^   https://$server_name$request_uri? permanent;
### 使用return的效率会更高 
#  return 301 https://$server_name$request_uri;
}
```

`ssl_certificate`证书其实是个公钥，它会被发送到连接服务器的每个客户端，`ssl_certificate_key`私钥是用来解密的，所以它的权限要得到保护但nginx的主进程能够读取。当然私钥和证书可以放在一个证书文件中，这种方式也只有公钥证书才发送到client。

`ssl_protocols`指令用于启动特定的加密协议，nginx在1.1.13和1.0.12版本后默认是`ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2`，TLSv1.1与TLSv1.2要确保OpenSSL >= 1.0.1 ，SSLv3 现在还有很多地方在用但有不少被攻击的漏洞。

漏洞修复方案

`ssl_ciphers`选择加密套件，不同的浏览器所支持的套件（和顺序）可能会不同。这里指定的是OpenSSL库能够识别的写法，你可以通过 `openssl -v cipher 'RC4:HIGH:!aNULL:!MD5'`（后面是你所指定的套件加密算法） 来看所支持算法。

`ssl_prefer_server_ciphers on`设置协商加密算法时，优先使用我们服务端的加密套件，而不是客户端浏览器的加密套件。

## https优化参数

- `ssl_session_cache shared:SSL:10m;` : 设置ssl/tls会话缓存的类型和大小。如果设置了这个参数一般是`shared`，`buildin`可能会参数内存碎片，默认是`none`，和`off`差不多，停用缓存。如`shared:SSL:10m`表示我所有的nginx工作进程共享ssl会话缓存，官网介绍说1M可以存放约4000个sessions。 详细参考serverfault上的问答[ssl\_session\_cache](http://serverfault.com/questions/695258/when-shoud-i-use-ssl-session-cache-paramter-in-nginx-ssl-settings)。
- `ssl_session_timeout` ： 客户端可以重用会话缓存中ssl参数的过期时间，内网系统默认5分钟太短了，可以设成`30m`即30分钟甚至`4h`。

设置较长的`keepalive_timeout`也可以减少请求ssl会话协商的开销，但同时得考虑线程的并发数了。

深入探索

文件大小转换

编程语言教程

SQL注入防护

**提示**：在生成证书请求csr文件时，如果输入了密码，nginx每次启动时都会提示输入这个密码，可以使用私钥来生成解密后的key来代替，效果是一样的，达到免密码重启的效果：

```
openssl rsa -in ittest.key -out ittest_unsecure.key
```

导入证书

如果你是找一个知名的ssl证书颁发机构如VeriSign、Wosign、StartSSL签发的证书，浏览器已经内置并信任了这些根证书，如果你是自建C或获得二级CA授权，都需要将CA证书添加到浏览器，这样在访问站点时才不会显示不安全连接。各个浏览的添加方法不在本文探讨范围内。

网络安全

# 2. 部分页面ssl

一个站点并不是所有信息都是非常机密的，如网上商城，一般的商品浏览可以不通过https，而用户登录以及支付的时候就强制经过https传输，这样用户访问速度和安全性都得到兼顾。

但是请注意不要理解错了，是对页面加密而不能针对某个请求加密，一个页面或地址栏的URL一般会发起许多请求的，包括css/png/js等静态文件和动态的java或php请求，所以要加密的内容包含页面内的其它资源文件，否则就会出现http与https内容混合的问题。在http页面混有https内容时，页面排版不会发生乱排现象；在https页面中包含以http方式引入的图片、js等资源时，浏览器为了安全起见会阻止加载。

下面是只对`example.com/account/login`登录页面进行加密的例子：

```
root /apps/www;
index index.html index.htm;
server {
    listen      80;
    server_name example.com;
    location ^~ /account/login {
        rewrite ^ https://$server_name:443$request_uri? permanent;
    }
    location / {
        proxy_pass  http://localhost:8080;

        ### Set headers ####
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect     off; 
    }
}
server {
    listen 443 ssl;
    server_name example.com;
    ssl on;
    ssl_certificate ../SSL/ittest.pem;
    ssl_certificate_key ../SSL/ittest.key;
    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
    ssl_prefer_server_ciphers on;
    location ^~ /account/login {
        proxy_pass  http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect     off; 
        ### Most PHP, Python, Rails, Java App can use this header -> https ###
        proxy_set_header X-Forwarded-Proto  $scheme;
    }
    location / {
        rewrite  ^  http://$server_name$request_uri? permanent;
    }
}
```

关于rewrite与location的写法参考[这里](https://mrxn.net/nginx-location-rewrite.html)。当浏览器访问`http://example.com/account/login.xx`时，被301到`https://example.com/account/login.xx`，在这个ssl加密的虚拟主机里也匹配到`/account/login`，反向代理到后端服务器，后面的传输过程是没有https的。这个login.xx页面下的其它资源也是经过https请求nginx的，登录成功后跳转到首页时的链接使用http，这个可能需要开发代码里面控制。

Windows安全工具

- 上面配置中使用了`proxy_set_header X-Forwarded-Proto $scheme`，在jsp页面使用`request.getScheme()`得到的是https 。如果不把请求的$scheme协议设置在header里，后端jsp页面会一直认为是http，将导致响应异常。
- ssl配置块还有个与不加密的80端口类似的`location /`，它的作用是当用户直接通过https访问首页时，自动跳转到不加密端口，你可以去掉它允许用户这样做。

# 3. 实现双向ssl认证

上面的两种配置都是去认证被访问的站点域名是否真实可信，并对传输过程加密，但服务器端并没有认证客户端是否可信。（实际上除非特别重要的场景，也没必要去认证访问者，除非像银行U盾这样的情况）

代理与过滤

要实现双向认证HTTPS，nginx服务器上必须导入CA证书（根证书/中间级证书），因为现在是由服务器端通过CA去验证客户端的信息。还有必须在申请服务器证书的同时，用同样的方法生成客户证书。取得客户证书后，还要将它转换成浏览器识别的格式（大部分浏览器都认识PKCS12格式）：

```
openssl pkcs12 -export -clcerts -in client.crt -inkey client.key -out client.p12
```

然后把这个`client.p12`发给你相信的人，让它导入到浏览器中，访问站点建立连接的时候nginx会要求客户端把这个证书发给自己验证，如果没有这个证书就拒绝访问。

同时别忘了在 nginx.conf 里配置信任的CA：（如果是二级CA，请把根CA放在后面，形成CA证书链）

```
proxy_ignore_client_abort on；
    ssl on;
    ...
    ssl_verify_client on;
    ssl_verify_depth 2;
    ssl_client_certificate ../SSL/ca-chain.pem;
# 在双向location下加入：
    proxy_set_header X-SSL-Client-Cert $ssl_client_cert;
```

拓展：使用geo模块

nginx默认安装了一个`ngx_http_geo_module`，这个geo模块可以根据客户端IP来创建变量的值，用在如来自172.29.73.0/24段的IP访问login时使用双向认证，其它段使用一般的单向认证。

```
geo $duplexing_user {
    default 1;
    include geo.conf;  # 注意在0.6.7版本以后，include是相对于nginx.conf所在目录而言的
}
```

语法 `geo [$address] $variable { … }`，位于http段，默认地址是`$reoute_addr`，假设 `conf/geo.conf` 内容：

```
127.0.0.1/32    LOCAL;  # 本地
172.29.73.23/32 SEAN;   # 某个IP
172.29.73.0/24  1;      # IP段，可以按国家或地域定义后面的不同的值
```

需要配置另外一个虚拟主机server{ssl 445}，里面使用上面双向认证的写法，然后在80或443里使用变量`$duplexing_user`去判断，如果为1就rewrite到445，否则rewrite到443。具体用法可以参考[nginx geo使用方法](http://www.ttlsa.com/nginx/using-nginx-geo-method/)。

**参考**

- [Nginx部署部分https与部分http](http://blog.csdn.net/na_tion/article/details/17334669)
- [Linux+Nginx/Apache/Tomcat新增SSL证书，开启https访问教程](https://www.zhoufengjie.cn/?p=185)
- [SSL & SPDY 已全面部署](https://www.sinosky.org/ssl-and-spdy-enabled.html)
- [SSL证书与Https应用部署小结](http://han.guokai.blog.163.com/blog/static/136718271201211631456811/)
- [ngx\_http\_ssl\_module docs](http://nginx.org/en/docs/http/ngx_http_ssl_module.html)
- [Optimizing HTTPS on Nginx](https://bjornjohansen.no/optimizing-https-nginx)
- [http://zhangge.net/4861.html](https://zhangge.net/4861.html)
- <http://blog.chinaunix.net/uid-192074-id-3135733.html>

原文地址：<http://seanlook.com/2015/05/28/nginx-ssl/>

- 标签：
- [#http](https://mrxn.net/tag/http)
- [#ssl](https://mrxn.net/tag/ssl)
- [#https](https://mrxn.net/tag/https)
- [#nginx](https://mrxn.net/tag/nginx)
- [#vps](https://mrxn.net/tag/vps)
- [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

---

文章目录

- [1.
  1. 全站ssl](#toc-1-)
- [1.1.
  https优化参数](#toc-1-1-)
- [2.
  2. 部分页面ssl](#toc-2-)
- [3.
  3. 实现双向ssl认证](#toc-3-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAI9UlEQVR4AeydgXLbOAxE/fr//9wzhIJYSaApJbGs9tgxguUCC9KE4YuTzNyvx+Px+yfs94F/sY+mBtfzo9xeXPnAukfFfSVudVT3XWwNedaYj7vcQGvIs9OPr1j1RIAH7K3K1T2r+BluVEvj4OfT+lVcOcWqC6zxMzj05ltDbDHt8zcwG/L5HqxOUDYEfJyh9qsKxaI3rkXqigqdkpBnqOKaO8LwvVqQ+jN7QerAcU9fNqSXPPn338BsyPvv+NQOlzYk3nLAxxZqr88gNOaVDwx1DdjzViMMPB51zINzgC0/Ypc25CPP8C/b9D0NOXEJ8YpVf0I+/OzUqxX7aTw49UD7TKW86n4Sf7whP/lk/oVasyE362LZEB3NCo+eA+SYwx5rzVGtKq56yPqaC85XHNBordVIARoH2tuXpJRQdRUuRU+ybMiTn48P3cBsyIcuvrdtawjkOMJx3CscvI5rcOoh91K+wuC5VazHfXV/OL8XuAbOeT17a4iSE3/uBn7pK+g7+MhTiPpHciMH8tUWethzFguNeVubGQ6zdRh4jYiZB+eA9vnG+LDQmg/OvK1/yuaE2I3eyP6mhtzo2t53lMMNgRxneI11fPXo4DrlFMP5OLgG1l7rBobMCW7kITWQWHWQPDjWeIXB84BV+HBDVqq5eNsNzIa87Wq/VrhsCLD7EYG+DVVYt4fUQ+LQwZ6LmHmtVWHLGVnoIPcKzvxID67r5VmNrWmuxsBrKdfLLRuiwomvvYHZkGvve7jbL/BxgvSVCjIOe6ya3jiC6zQOzgFaomHNDdyCTwDs3l6fdHuEZutbggDY14I9ZxJIPmobHwYZf8VFLPyckLiJm/iyIdFx83FOw0ctNOYrjfE/ZVr/TE3wV7BqRrXANYDKGgbKaY26LXEDIHVlQzb5//byZs9uNuRuDanGCXKE4ryQHOxx5L3y4DrNif3Ng8cNh4FzQJMB5VtDSzgBoK4V+6vvlQWvofGRDlwD+ZNl08wJ0Vu8AZ4NuUET9Ajtc4iSisFHSzkbra2B50HfRw3InODOeN1bdZB1wbHGRxhcA7Xv6fU8gSFrVLrIM6/xOSF6GzfA7Ve4Z84C2X1wbJ0O01rBmQ/ecFhw5oMDrwkYvTOg/UcdEofefIgg48GZt5ytGR8WsVibD27rLWYGuZfmgPOWM7I5IaMbujg+G3LxhY+2Kxui4zYqELmaF5z5ilcOfJwhvekqU12FIWuM4uC5mqd7wj6uuRUW/eotNXjVgNcHlH6UDVllzMWlNzAbcul1jzcbfg6Jcet5YDWe0F/HcSBzgjMfe0DGYY8j7ye87VtZ1K5ixsH+XJBc6M2D86YLMz4sOPNzQuwWbmStIdEt83o+2HdX45Z/1GBfS7VRt+IsFjx4HVh7ywmDdQyI0MoD5YSvkv4sIHP/UIuLc6mHOncRvPjSGvIiZ4YuvIHZkAsv+8hWrSHwtRED1x3ZTEc6MLge0mutyDMPnmO4MvA40EpoXiOfAFjeqp7w8ENrKYZjtVTT27Q1pJcw+WtvYDbk2vse7tYaouMEPoLAsEDogOUtAOhqgJYDjqtk8BisfZWrXJxFvcYVR07FWQx8b8NhmgseBxoNtOfXSAGQcUgsKfNHJ3oZd8BtQu5wmHmGR04IcHjc9OLAdTHW5sE5WPvQWU5YcOojZr7ilYP1HuBrzakwvM6zvc3A84CqzIqz/Fe2SpYF0O5+TohczB3g8Fe4Vcf14BGH7HJw5jX3KIasdVSzzQOvoTw4B/m3UL04eK7Ge9iep5nGwfWQXuOKTRs2J0Rv5gZ4NuQGTdAjtN+HxMiY1wTwkVNOMXjcdGEaVzyKa27g0JgH3wvSR95ZD15DdbbH1jQOrgGULrHWiQTlFEfc/JwQu4Ub2QcacqNnf8OjtIYA7XthHafAvbOP4qoD30O50Pc8uAZQWYmrGmXik4zcJywfwHIfkWdeE20dFjy4Bghq8ZEHLDVh7ZekP19aQ/6sp/vwDZSfQ2DdQViv9czgMeUUx6vDvPIVBq8F6U33yqo6xkHWAMfGb01rg+cBLQ1or2rNbQlPAJ7zhO0BzgGNU9CrNSdEb+kGeDbkBk3QI7TPIUrqOFW4ylVOMdBGPnhIDhJHXPcMTj3sNRo3HDUMvzLIWqHpechcSPyqvsXAcw2PbE7I6IYujs+GXHzho+3ad1k6ppUIfOyAVRhob0ngeJUgC92jwpEKXgcIavHAslelNQ48DumNrww8ZylcfIHXcZVU9StONeD1AaXzF1Qr9i9c/CtHLt+ygOWVCOl7T7h6JcBY16u35WFfC5KDxF85i2q2e2/XmqsY8gywx9s62zWkpmzIVjDX193AbMh1d31op/Y5BHJsRkrIXNjjnh6O50YNfWsYYcj6oVcPGY9akJzmVnHIXEisuqM46m/9nJCjN3hR3mzIRRd9dJvyc8h2jM6ue5tXdSBHfxSv6kKtr3K1Priu4oAm13gjn0D5Cj9T2gNYvmvVPHAOaHkG5oTYLdzIZkNu1Aw7SvldFrCMGBz3Vuwr1htj8L3P1ATXAGdkZS7wAMrYlgSW+9ry2zV4HuQf6tnz17w5IXobN8CtIdapr9joOWhNyFcI7HHUUo3iiKsfxTUXcs/QwZ6zWOgg48FtveWbbflYW8ws1uYh60Li1hBLmvb5G5gN+XwPVicoGwI5QrDHqwqDBaTexnZrlRxSA6+x6rU2uE7jiuF1XGsFrvTgdWDtq1zloqZ55cuGaMLE197AbMi19z3c7S0NsTGsDHysR6eqtD0OvCYwKruKV/VWCcWi0hhXpLb/7V4vrhrLCXtLQ3Szic/dwNsbAiyfYiE/ncKes1fI6OjgOs0zXRh4HNCUhiPPfCM7AGjnBsed1MO07WtmBl4TWOnf3pDVbnMxvIHZkOEVXZtQNsRG6pWdOaLWAZa3gZ4+cjUOroF8y9P4dzFkfa1VnUXjiqtcyLoRh+RUr7hsiCZMfO0NzIZce9/D3VpDIMcJjuPRDpC1YnTVQ8ajFiSnuRFXD8dzK51yisHrjvY3DRzPtfytgeuB+aekj5v9axNys3P9b4/zHwAAAP//729TZQAAAAZJREFUAwA9AhGG4KWaeQAAAABJRU5ErkJggg==)

手机扫码阅读
