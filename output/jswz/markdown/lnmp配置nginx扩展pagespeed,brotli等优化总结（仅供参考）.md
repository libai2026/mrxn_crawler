---
title: "lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）"
source: https://mrxn.net/jswz/lnmp_PageSpeed_Brotli.html
asset_dir: assets/lnmp配置nginx扩展pagespeed,brotli等优化总结（仅供参考）
---

# lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）

[Mrxn](https://mrxn.net/author/1)- 发表于2018/2/14 13:48
- 4817浏览
- [2评论](#comment)
- 1小时阅读

深入探索

GNU/Linux

应用程序接口

压缩

---

[***[i]***](#_edn1)*注：本文只适合有一定Linux基础知识的人阅读，如果没有请慎阅，以免带来不适。*

## Lnmp1.4配置nginx（Nginx已经安装好了）扩展ngx\_PageSpeed, Brotli , ngx\_http\_google\_filter\_module ,ngx\_http\_google\_filter\_module

**环境：lnmp1.4 + vultr-JP**

**OS****：#lsb\_release -a**

**Debian GNU/Linux 8.10 (jessie) , PHP-7.1.7 ,MySql-5.5.56 , Nginx-1.12.2**

先看一下我的优化后使用Google的[PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/?url=https%3A%2F%2Fmrxn.net) PC检测有99分，打开速度是挺快的！

[[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](images/img-001-0aca3b26b971.png "点击查看原图_Mrxn")](../content/uploadfile/201802/d41a1518587745.png)](../content/uploadfile/201802/d41a1518587745.png)[[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](images/img-002-e6f6969425f0.png "点击查看原图_Mrxn")](../content/uploadfile/201802/3fcd1518587743.png)](../content/uploadfile/201802/3fcd1518587743.png)

然后查看nginx配置：nginx –V (注意是大写的)，结果类似如下：

[[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](images/img-003-fc3c6aba06ee.png "点击查看原图_Mrxn")](../content/uploadfile/201802/thum-bc731518587744.png)](../content/uploadfile/201802/bc731518587744.png)

我们要做的就是再此基础上增加模块，Nginx增加模块比Apache麻烦点，Apache直接配置文件引用.so模块文件即可，Nginx需要编译。不多累述，想了解的自己Google。

首先我们在home目录下新建一个extends文件夹（mkdir /home/extends）用来装我们的扩展源码，接下来就是下载这些源码:

但是，在下载源码之前，我们需要更新一下系统和安装一些依赖：

apt-get update && apt-get install build-essential zlib1g-dev libpcre3 libpcre3-dev unzip uuid-dev git gcc g++ make -y

深入探索

Windows安全工具

Docker加速服务

漏洞扫描服务

git clone <https://github.com/google/ngx_brotli.git>

cd ngx\_brotli  
 git submodule update --init

wget <https://github.com/apache/incubator-pagespeed-ngx/archive/v1.13.35.2-stable.tar.gz>

tar xzvf v1.13.35.2-stable.tar.gz

cd incubator-pagespeed-ngx-1.13.35.2-stable

wget <https://dl.google.com/dl/page-speed/psol/1.12.34.2-x64.tar.gz>

tar xzvf 1.12.34.2-x64.tar.gz

git clone <https://github.com/cuber/ngx_http_google_filter_module>

git clone <https://github.com/yaoweibin/ngx_http_substitutions_filter_module>

备注：因为是lnmp1.4x + php7.1因此最后两个扩展所需要的这些模块已经自带了：pcre, openssl ,zlib以及nginx源码,如果你不是php7，请自行下载相关依赖并解压到扩展文件夹extends里面方便后面的使用。

接下来就是配置编译前的nginx了(在nginx源码所在的目录，里面包含configure的这个文件夹路径下):

可以创建预编译的目录或者是就在解压缩后的nginx源码目录也行。

./configure --user=www --group=www --prefix=/usr/local/nginx --with-cc-opt=-Wno-deprecated-declarations --with-http\_stub\_status\_module --with-http\_ssl\_module --with-http\_v2\_module --with-http\_gzip\_static\_module --with-http\_realip\_module  --with-http\_sub\_module --with-openssl=/root/lnmp1.4/src/openssl-1.0.2l --add-module=/home/extends/ngx\_http\_google\_filter\_module --add-module=/home/extends/ngx\_http\_substitutions\_filter\_module --add-module=/home/extends/ngx\_brotli --add-module=/home/extends/incubator-pagespeed-ngx-1.13.35.2-stable

需要注意的是：上面的命令你可以根据你自己的路径来修改，注意拼写，推荐使用Tab键补全获得准确的pwd，最重要的就是你需要会看系统的提示，我觉得Linux的系统提示是非常完善的，你根据提示去搜索基本上都是可以找到答案的，特别是像这些流行的应用出现的问题。如果有搞不定的，可以联系我（YWRtaW5AbXJ4bi5uZXQ=）有空会给你解答，当然也可以付费帮你配置这些，毕竟时间就是金钱，而且一个人的精力有限。

如果提示：make[1]: Leaving directory '/root/nginx-1.12.2'这类的，你可能是配置好后编译失败了，需要清除，重新配置。在nginx源码目录执行，make clean ,然后再重新./configure就行。如果还是不行，就自行去预编译的目录下查看是否有nginx二进制文件，如果没有，肯定失败了，否则，停止Nginx，备份已安装的nginx，再将这个预编译好的复制到旧Nginx所在目录，然后启动Nginx,执行nginx –t ,检查看是否出错，如果不出错就打开网页看看是否正常，正常就OK了。不正常的话就慢慢排查吧。

## 下面贴一下nginx 的主要配置代码：

nginx.conf :

        gzip on;

        gzip\_min\_length  1k;

        gzip\_buffers     4 16k;

        gzip\_http\_version 1.1;

        gzip\_comp\_level 2;

        gzip\_types     text/plain application/javascript application/x-javascript text/javascript text/css application/xml application/xml+rss;

        gzip\_vary on;

        gzip\_proxied   expired no-cache no-store private auth;

        gzip\_disable   "MSIE [1-6]\.";

              brotli on;

              brotli\_types text/plain text/css text/xml application/xml application/json text/javascript application/javascript application/x-javascript

              brotli\_static off;

              brotli\_comp\_level 11;

              brotli\_buffers 16 8k;

              brotli\_window 512k;

              brotli\_min\_length 20;

vhost/mrxn.net.conf:

        # 启用ngx\_pagespeed

        pagespeed on;

        pagespeed FileCachePath /tmp/cache/ngx\_pagespeed\_cache;

        # 禁用CoreFilters

        pagespeed RewriteLevel PassThrough;

        # 启用压缩空白过滤器

        pagespeed EnableFilters collapse\_whitespace;

        # 启用JavaScript库卸载

        pagespeed EnableFilters canonicalize\_javascript\_libraries; #谷歌被墙，国内服务器用不了，国外的不存在

        # 把多个CSS文件合并成一个CSS文件

        pagespeed EnableFilters combine\_css;

        # 把多个JavaScript文件合并成一个JavaScript文件

        pagespeed EnableFilters combine\_javascript;

        # 删除带默认属性的标签

        pagespeed EnableFilters elide\_attributes;

        # 改善资源的可缓存性

        pagespeed EnableFilters extend\_cache;

        # 更换被导入文件的@import，精简CSS文件

        pagespeed EnableFilters flatten\_css\_imports;

        pagespeed CssFlattenMaxBytes 5120;

        # 延时加载客户端看不见的图片

        pagespeed EnableFilters lazyload\_images;

        # 启用JavaScript缩小机制

        pagespeed EnableFilters rewrite\_javascript;

        # 启用图片优化机制

        pagespeed EnableFilters rewrite\_images;

        # 预解析DNS查询

        pagespeed EnableFilters insert\_dns\_prefetch;

        # 重写CSS，首先加载渲染页面的CSS规则

        pagespeed EnableFilters prioritize\_critical\_css;

        # Example 禁止pagespeed 处理/admin/目录(可选配置，可参考使用)

        pagespeed Disallow "\*/admin/\*";

配置后测试没有问题的话基本是这个样子的：

[[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](images/img-004-39832dc1afbf.png "点击查看原图_Mrxn")](../content/uploadfile/201802/37371518587743.png)](../content/uploadfile/201802/37371518587743.png)

如果配置过程中有其他的错误，请根据错误提示Google或自查。实在不行就找人吧。

上面的步骤都顺利通过了之后就可以去配置nginx了，主要是配置Google的反代。可以参考我之前写的文章，下面简单记录一下：

备份原有已安装好的nginx:

cp /usr/local/nginx/sbin/nginx /usr/local/nginx/sbin/nginx.bak  
 service nginx stop

然后将刚刚编译好的nginx覆盖掉原有的nginx（这个时候nginx要停止状态,通过上面的命令,已经停止了）:

cp ./objs/nginx /usr/local/nginx/sbin/

然后启动nginx (service nginx start)，就可以通过命令nginx -V 查看第三方扩展是否已经加入成功.

## 下面说下在PHP7下如何使emlog支持，其实就是修改几个变量：

1.首先在/include/lib/option.php

大约11行位置

//默认MySQL链接方，mysql或mysqli

把const DEFAULT\_MYSQLCONN = 'mysql';

改为 const DEFAULT\_MYSQLCONN = 'mysqli';

2.在/include/lib/cache.php

大约195行

把$$row['option\_name'] = $row['option\_value'];

改为 ${$row['option\_name']} = $row['option\_value'];

3.在admim/seo.php

大约在15行、19行共两上

把 $$t改为

 ${$t}

4.在admim/views/admin\_log.php

大约在86行、88行、90行共三个

把$$a $$b $$a

改为 ${$a} ${$b} ${$a}

5.在admim/views/comment.php

大约在18行

把 $$a = "class=\"filter\"";

改为 ${$a} = "class=\"filter\"";

另外有些插件和主题是固定了使用mysql连接类，这样还需要修改插件和主题中的数据库连接方式，不然直接报数据库错误。

比如：

$DB = MySql::getInstance();

都要改为$DB = Database::getInstance();

小提示：我是使用的[sublime text](../index.php?keyword=sublime+text)  使用正则匹配搜索—正则如下：^(\$)(\$)a，不然你会搜不到$$a的，可以使用sublime的指定文件夹搜索，在你的整个网站目录所有文件里搜索相关变量，进行批量替换。

[[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](images/img-005-2cc8dd2f095c.png "点击查看原图_Mrxn")](../content/uploadfile/201802/006b1518587744.png)](../content/uploadfile/201802/006b1518587744.png)

我之前发的相关文章（仅供参考）：

两种方式反代Google(镜像)--nginx反代和nginx扩展

[https://mrxn.net/Linux/nginx\_http\_google\_filter.html](../Linux/nginx_http_google_filter.html)

为nginx添加这些额外的第三方扩展加速你的web吧

[https://mrxn.net/Linux/nginx\_add\_module.html](../Linux/nginx_add_module.html)

参考文章—感谢他们的分享：

<https://www.modpagespeed.com/doc/build_ngx_pagespeed_from_source>

<https://www.lvtao.net/config/nginx-google-brotli.html>

<https://zhangge.net/5063.html>

---

文章目录

- [1.Lnmp1.4配置nginx（Nginx已经安装好了）扩展ngx\_PageSpeed, Brotli , ngx\_http\_google\_filter\_module ,ngx\_http\_google\_filter\_module](#toc-1-)
- [2.下面贴一下nginx 的主要配置代码：](#toc-2-)
- [3.下面说下在PHP7下如何使emlog支持，其实就是修改几个变量：](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
