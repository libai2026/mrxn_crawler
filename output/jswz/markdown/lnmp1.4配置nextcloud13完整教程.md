---
title: "lnmp1.4配置nextcloud13完整教程"
source: https://mrxn.net/jswz/lnmp_install_nextcloud13.html
asset_dir: embedded-base64
---

首先下载nextcloud得最新压缩包，然后解压。

文件共享与托管

 在[nextcloud官网](https://nextcloud.com/install/#instructions-server "nextcloud-server")得页面下载最新的服务端安装包，我这里目前是13.0的，然后解压：

`wget -c https://download.nextcloud.com/server/releases/nextcloud-13.0.0.zip`

`unzip -q nextcloud-13.0.0.zip`

然后使用lnmp vhost add 添加网站，此处省略，请自行去lnmp.org查看教程。

计算机与电子产品

网站添加完成后，我们需要修改你网站的nginx配置文件，使其适应nextcloud的url重写规则：

`vi /usr/local/nginx/conf/vhost/demo.mrxn.net.conf`

注意：红色的部分是你自己的域名。

将其中的

include enable-php.conf; 修改成 include enable-php-pathinfo.conf; 然后重启nginx,lnmp nginx restart .

这时访问你的域名，即可开始配置nextcloud，设置登录账号，密码，数据库 用户名，数据库名，密码，数据库地址（端口），即可完成。（因为这些网上都有很详细的教程，此处省略）。

深入探索

网络安全

网络监控与管理

网络浏览器

配置完后出现的一些问题的解决：

计算机科学

#### 添加 fileinfo 扩展：

1、安装前建议先执行 /usr/local/php/bin/php -m (此命令显示目前已经安装好的PHP模块)看一下，要安装的模块是否已安装。

2、首先进入php安装目录的ext目录，找到并进入要安装扩展的文件夹，我们要安装fileinfo扩展，找到并进入fileinfo文件夹。

例如：/root/lnmp1.4/src/php-7.1.7/ext/fileinfo

3、再执行 /usr/local/php/bin/phpize 会返回如下类似信息：

`Configuring for:`  
`PHP Api Version: 20160303`  
`Zend Module Api No: 20160303`  
`Zend Extension Api No: 320160303`

深入探索

VPN 与远程访问

Linux

VPN

然后再执行以下命令来配置，编译安装fileinfo扩展:

软件

`./configure --with-php-config=/usr/local/php/bin/php-config`

`make && make install`

执行完后返回如下信息：

`Build complete.`  
`Don't forget to run 'make test'.`  
`Installing shared extensions: /usr/local/php/lib/php/extensions/no-debug-non-zts-20160303/`

表示编译安装成功，我们只需要修改 /usr/local/php/etc/php.ini 配置文件加入： extension=fileinfo.so ，然后执行 lnmp php-fpm restart 重启 php-fpm服务就完成了fileinfo扩展的安装。

#### 关于php /dev/urandom ：

[/dev/urandom is not readable by PHP which is highly discouraged for security reasons.](https://docs.nextcloud.com/server/13/admin_manual/configuration_server/harden_server.html "/dev/urandom")

深入探索

开发工具

开放源代码

vpn

那是因为lnmp默认在每个网站目录加了一个.user.ini文件，防止跨目录，且为只读文件，里面就是写得open\_basedir，根据nextcloud官方文档，只要我们添加了/dev/urandom到open\_basedir就可以了。

文件共享与托管

我们首先使用一下命令解锁文件权限，在写入进去就行：

chattr -i /path/to/yoursite/.user.ini #解锁文件

open\_basedir=/path/to/yoursite:/tmp/:/proc/:/dev/urandom

其中红色得部分就是我们添加得内容。

修改完后记得改回去，加上锁：

chattr +i /path/to/yoursite/.user.ini

PS:简单说一下这个命令，就当做笔记了

**chattr命令**：有时候你发现用root权限都不能修改某个文件，大部分原因是曾经用chattr命令锁定该文件了。chattr命令的作用很大，通过chattr命令修改属性能够提高系统的安全性，但是它并不适合所有的目录。chattr命令不能保护/、/dev、/tmp、/var目录。lsattr命令是显示chattr命令设置的文件属性。

数据管理

其中添加那个参考了这个链接：

<https://support.plesk.com/hc/en-us/articles/213368009-How-to-set-up-php-custom-php-settings-for-the-domain>

 Background jobs 推荐使用系统的crontab 来增加一个:

crontab -u www -e 进行编辑增加

\*/15 \* \* \* \* php -f /path/to/yoursite/cron.php 即可

软件

#### 其他：

如果你查看左边的日志发现了很多的 类似 scandir() has been disabled for security reasons at ...... 的提示，那么，你需要修改你的php.ini配置文件。

`vi /usr/local/php/etc/php.ini`

将disable\_functions后面的scandir去掉，保存后，重新启动php-fpm，`lnmp php-fpm restart`。

如果开启了zend的Opcache插件，那么需要修改一下其相关配置，使其性能最优（官方说的）。最好是使用phpinfo来查看的Opcache配置文件位置，lnmp的扩展配置文件一般是在 `/usr/local/php/conf.d/` 目录。

以下是我的Opcache配置，供参考：

`[Zend Opcache]`  
`zend_extension="opcache.so"`  
`opcache.enable=1`  
`opcache.save_comments=1`  
`opcache.memory_consumption=128`  
`opcache.interned_strings_buffer=8`  
`opcache.max_accelerated_files=10000`  
`opcache.revalidate_freq=1`  
`opcache.fast_shutdown=1`  
`opcache.enable_cli=1`

*PS：*

*开启APCU，Redis，Opcache，imageMagick等优化插件：*

计算机安全

*直接在lnmp1.4的源码目录里面执行 ./addons.sh 选择你需要的即可添加。*

下面是nginx的主要配置，仅供参考！**切忌无脑照抄！**：

`ssl_buffer_size 1400;`  
 `add_header Strict-Transport-Security max-age=15768000;`  
 `ssl_stapling on;`  
 `ssl_stapling_verify on;`  
 `if ($ssl_protocol = "") { return 301 https://$host$request_uri; }`

`include none.conf;`  
 `#error_page 404 /404.html;`

`# Deny access to PHP files in specific directory`  
 `#location ~ /(wp-content|uploads|wp-includes|images)/.*\.php$ { deny all; }`

`include enable-php-pathinfo.conf;`

`#这儿是为了支持日历和联系人，建议加上`  
 `location = /.well-known/carddav {`  
 `return 301 $scheme://$host/remote.php/dav;`  
 `}`  
 `location = /.well-known/caldav {`  
 `return 301 $scheme://$host/remote.php/dav;`  
 `}`  
 `#设置上传文件的最大大小(还和php里的那个设置有关)`  
 `client_max_body_size 512M;`  
 `fastcgi_buffers 64 4K;`  
 `#最主要的，将所有请求转发到index.php上`  
 `location / {`  
 `rewrite ^ /index.php$uri;`  
 `}`  
 `#安全设置，禁止访问部分敏感内容`  
 `location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)/ {`  
 `deny all;`  
 `}`  
 `location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {`  
 `deny all;`  
 `}`

`location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|ocs-provider/.+)\.php(?:$|/) {`  
 `fastcgi_split_path_info ^(.+\.php)(/.*)$;`  
 `fastcgi_param PATH_INFO $fastcgi_path_info;`  
 `fastcgi_param modHeadersAvailable true;`  
 `fastcgi_param front_controller_active true;`  
 `fastcgi_intercept_errors on;`  
 `fastcgi_request_buffering off;`  
 `include fastcgi.conf;`  
 `}`

`#安全设置，禁止访问部分敏感内容`  
 `location ~ ^/(?:updater|ocs-provider)(?:$|/) {`  
 `try_files $uri/ =404;`  
 `index index.php;`  
 `}`

`location ~ \.(?:css|js|woff|svg|gif)$ {`  
 `try_files $uri /index.php$uri$is_args$args;`  
 `add_header Cache-Control "public, max-age=15778463";`  
 `add_header X-Content-Type-Options nosniff;`  
 `add_header X-XSS-Protection "1; mode=block";`  
 `add_header X-Robots-Tag none;`  
 `add_header X-Download-Options noopen;`  
 `add_header X-Permitted-Cross-Domain-Policies none;`  
 `}`  
 `location ~ \.(?:png|html|ttf|ico|jpg|jpeg)$ {`  
 `try_files $uri /index.php$uri$is_args$args;`  
 `}`

`location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$`  
 `{`  
 `expires 30d;`  
 `}`

`location ~ .*\.(js|css)?$`  
 `{`  
 `expires 12h;`  
 `}`

`location ~ /.well-known {`  
 `allow all;`  
 `}`

`location ~ /\.`  
 `{`  
 `deny all;`  
 `}`

`location ~ /\.ht {`  
 `deny all;`  
 `}`  
 `access_log off;`

就到这里了，有啥问题，评论，以后有时间再更新（先挖个坑）。
