---
title: "lnmp1.4配置nextcloud13完整教程"
source: https://mrxn.net/jswz/lnmp_install_nextcloud13.html
---

# lnmp1.4配置nextcloud13完整教程

[Mrxn](https://mrxn.net/author/1)* 发表于2018/2/16 21:29
* 7385浏览
* [3评论](#comment)
* 49分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

首先下载nextcloud得最新压缩包，然后解压。

在
[nextcloud官网](https://nextcloud.com/install/#instructions-server "nextcloud-server")
得页面下载最新的服务端安装包，我这里目前是13.0的，然后解压：

`wget -c https://download.nextcloud.com/server/releases/nextcloud-13.0.0.zip`

`unzip -q nextcloud-13.0.0.zip`

然后使用lnmp vhost add 添加网站，此处省略，请自行去lnmp.org查看教程。

网站添加完成后，我们需要修改你网站的nginx配置文件，使其适应nextcloud的url重写规则：

`vi /usr/local/nginx/conf/vhost/
demo.mrxn.net
.conf`

注意：红色的部分是你自己的域名。

将其中的

include enable-php.conf; 修改成 include enable-php
-pathinfo
.conf; 然后重启nginx,lnmp nginx restart .

这时访问你的域名，即可开始配置nextcloud，设置登录账号，密码，数据库 用户名，数据库名，密码，数据库地址（端口），即可完成。（因为这些网上都有很详细的教程，此处省略）。

配置完后出现的一些问题的解决：

#### 添加 fileinfo 扩展：

1、安装前建议先执行 /usr/local/php/bin/php -m (此命令显示目前已经安装好的PHP模块)看一下，要安装的模块是否已安装。

2、首先进入php安装目录的ext目录，找到并进入要安装扩展的文件夹，我们要安装fileinfo扩展，找到并进入fileinfo文件夹。

例如：/root/lnmp1.4/src/php-7.1.7/ext/fileinfo

3、再执行 /usr/local/php/bin/phpize 会返回如下类似信息：

`Configuring for:`
  
`PHP Api Version: 20160303`
  
`Zend Module Api No: 20160303`
  
`Zend Extension Api No: 320160303`

然后再执行以下命令来配置，编译安装fileinfo扩展:

`./configure --with-php-config=/usr/local/php/bin/php-config`

`make && make install`

执行完后返回如下信息：

`Build complete.`
  
`Don't forget to run 'make test'.`
  
`Installing shared extensions: /usr/local/php/lib/php/extensions/no-debug-non-zts-20160303/`

表示编译安装成功，我们只需要修改 /usr/local/php/etc/php.ini 配置文件加入： extension=fileinfo.so ，然后执行 lnmp php-fpm restart 重启 php-fpm服务就完成了fileinfo扩展的安装。

#### 关于php /dev/urandom ：

[/dev/urandom is not readable by PHP which is highly discouraged for security reasons.](https://docs.nextcloud.com/server/13/admin_manual/configuration_server/harden_server.html "/dev/urandom")

那是因为lnmp默认在每个网站目录加了一个.user.ini文件，防止跨目录，且为只读文件，里面就是写得open\_basedir，根据nextcloud官方文档，只要我们添加了/dev/urandom到open\_basedir就可以了。

我们首先使用一下命令解锁文件权限，在写入进去就行：

chattr -i /path/to/yoursite/.user.ini #解锁文件

open\_basedir=/path/to/yoursite:/tmp/:/proc/
:/dev/urandom

其中红色得部分就是我们添加得内容。

修改完后记得改回去，加上锁：

chattr +i /path/to/yoursite/.user.ini

PS:简单说一下这个命令，就当做笔记了

**chattr命令**
：有时候你发现用root权限都不能修改某个文件，大部分原因是曾经用chattr命令锁定该文件了。chattr命令的作用很大，通过chattr命令修改属性能够提高系统的安全性，但是它并不适合所有的目录。chattr命令不能保护/、/dev、/tmp、/var目录。lsattr命令是显示chattr命令设置的文件属性。

其中添加那个参考了这个链接：

<https://support.plesk.com/hc/en-us/articles/213368009-How-to-set-up-php-custom-php-settings-for-the-domain>

Background jobs 推荐使用系统的crontab 来增加一个:

crontab -u www -e 进行编辑增加

\*/15 \* \* \* \* php -f /path/to/yoursite/cron.php 即可

#### 其他：

如果你查看左边的日志发现了很多的 类似 scandir() has been disabled for security reasons at ...... 的提示，那么，你需要修改你的php.ini配置文件。

`vi /usr/local/php/etc/php.ini`

将disable\_functions后面的scandir去掉，保存后，重新启动php-fpm，
`lnmp php-fpm restart`
。

如果开启了zend的Opcache插件，那么需要修改一下其相关配置，使其性能最优（官方说的）。最好是使用phpinfo来查看的Opcache配置文件位置，lnmp的扩展配置文件一般是在
`/usr/local/php/conf.d/`
目录。

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

*直接在lnmp1.4的源码目录里面执行 ./addons.sh 选择你需要的即可添加。*

下面是nginx的主要配置，仅供参考！
**切忌无脑照抄！**
：

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

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录

×



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[lnmp1.4配置nextcloud13完整教程](https://mrxn.net/jswz/lnmp_install_nextcloud13.html)
  
文章链接：
<https://mrxn.net/jswz/lnmp_install_nextcloud13.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/lnmp\_install\_nextcloud13.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/lnmp\_install\_nextcloud13.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});