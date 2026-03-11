---
title: "lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）"
source: https://mrxn.net/jswz/lnmp_PageSpeed_Brotli.html
---

# lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）

[Mrxn](https://mrxn.net/author/1)* 发表于2018/2/14 13:48
* 4813浏览
* [2评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

[***[i]***](#_edn1)
*注：本文只适合有一定Linux基础知识的人阅读，如果没有请慎阅，以免带来不适。*

## Lnmp1.4配置nginx（Nginx已经安装好了）扩展ngx\_PageSpeed, Brotli , ngx\_http\_google\_filter\_module ,ngx\_http\_google\_filter\_module

**环境：lnmp1.4 + vultr-JP**

**OS**
**：#lsb\_release -a**

**Debian GNU/Linux 8.10 (jessie) , PHP-7.1.7 ,MySql-5.5.56 , Nginx-1.12.2**

先看一下我的优化后使用Google的
[PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/?url=https%3A%2F%2Fmrxn.net)
PC检测有99分，打开速度是挺快的！

[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](../content/uploadfile/201802/d41a1518587745.png "点击查看原图_Mrxn")](../content/uploadfile/201802/d41a1518587745.png)
[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](../content/uploadfile/201802/3fcd1518587743.png "点击查看原图_Mrxn")](../content/uploadfile/201802/3fcd1518587743.png)

然后查看nginx配置：nginx –V (注意是大写的)，结果类似如下：

[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](../content/uploadfile/201802/thum-bc731518587744.png "点击查看原图_Mrxn")](../content/uploadfile/201802/bc731518587744.png)

我们要做的就是再此基础上增加模块，Nginx增加模块比Apache麻烦点，Apache直接配置文件引用.so模块文件即可，Nginx需要编译。不多累述，想了解的自己Google。

首先我们在home目录下新建一个extends文件夹（mkdir /home/extends）用来装我们的扩展源码，接下来就是下载这些源码:

但是，在下载源码之前，我们需要更新一下系统和安装一些依赖：

apt-get update && apt-get install build-essential zlib1g-dev libpcre3 libpcre3-dev unzip uuid-dev git gcc g++ make -y

git clone
<https://github.com/google/ngx_brotli.git>

cd ngx\_brotli
  
git submodule update --init

wget
<https://github.com/apache/incubator-pagespeed-ngx/archive/v1.13.35.2-stable.tar.gz>

tar xzvf v1.13.35.2-stable.tar.gz

cd incubator-pagespeed-ngx-1.13.35.2-stable

wget
<https://dl.google.com/dl/page-speed/psol/1.12.34.2-x64.tar.gz>

tar xzvf 1.12.34.2-x64.tar.gz

git clone
<https://github.com/cuber/ngx_http_google_filter_module>

git clone
<https://github.com/yaoweibin/ngx_http_substitutions_filter_module>

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

[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](../content/uploadfile/201802/37371518587743.png "点击查看原图_Mrxn")](../content/uploadfile/201802/37371518587743.png)

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

小提示：我是使用的
[sublime text](../index.php?keyword=sublime+text)
使用正则匹配搜索—正则如下：^(\$)(\$)a，不然你会搜不到$$a的，可以使用sublime的指定文件夹搜索，在你的整个网站目录所有文件里搜索相关变量，进行批量替换。

[![lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](../content/uploadfile/201802/006b1518587744.png "点击查看原图_Mrxn")](../content/uploadfile/201802/006b1518587744.png)

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
[lnmp配置nginx扩展PageSpeed,Brotli等优化总结（仅供参考）](https://mrxn.net/jswz/lnmp_PageSpeed_Brotli.html)
  
文章链接：
<https://mrxn.net/jswz/lnmp_PageSpeed_Brotli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/lnmp\_PageSpeed\_Brotli.html"),
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
text: encodeURI("https://mrxn.net/jswz/lnmp\_PageSpeed\_Brotli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});