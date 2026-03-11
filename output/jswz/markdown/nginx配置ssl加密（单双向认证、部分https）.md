---
title: "nginx配置ssl加密（单双向认证、部分https）"
source: https://mrxn.net/jswz/nginx-ssl.html
asset_dir: assets/nginx配置ssl加密（单双向认证、部分https）
---

# nginx配置ssl加密（单双向认证、部分https）

[Mrxn](https://mrxn.net/author/1)* 发表于2015/9/24 21:48
* 13246浏览
* [0评论](#comment)
* 1小时阅读

深入探索

云安全解决方案

防火墙软件

网络安全培训


(adsbygoogle = window.adsbygoogle || []).push({});

---

nginx下配置ssl本来是很简单的，无论是去认证中心买SSL安全证书还是自签署证书，但最近公司OA的一个需求，得以有个机会实际折腾一番。一开始采用的是全站加密，所有访问http:80的请求强制转换（rewrite）到https，后来自动化测试结果说响应速度太慢，https比http慢慢30倍，心想怎么可能，鬼知道他们怎么测的。所以就试了一下部分页面https（不能只针对某类动态请求才加密）和双向认证。下面分节介绍。

安全运维咨询

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

Docker加速服务

计算机安全

编码转换工具

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

漏洞预警服务

`ssl_ciphers`选择加密套件，不同的浏览器所支持的套件（和顺序）可能会不同。这里指定的是OpenSSL库能够识别的写法，你可以通过 `openssl -v cipher 'RC4:HIGH:!aNULL:!MD5'`（后面是你所指定的套件加密算法） 来看所支持算法。

`ssl_prefer_server_ciphers on`设置协商加密算法时，优先使用我们服务端的加密套件，而不是客户端浏览器的加密套件。

## https优化参数

* `ssl_session_cache shared:SSL:10m;` : 设置ssl/tls会话缓存的类型和大小。如果设置了这个参数一般是`shared`，`buildin`可能会参数内存碎片，默认是`none`，和`off`差不多，停用缓存。如`shared:SSL:10m`表示我所有的nginx工作进程共享ssl会话缓存，官网介绍说1M可以存放约4000个sessions。 详细参考serverfault上的问答[ssl\_session\_cache](http://serverfault.com/questions/695258/when-shoud-i-use-ssl-session-cache-paramter-in-nginx-ssl-settings)。
* `ssl_session_timeout` ： 客户端可以重用会话缓存中ssl参数的过期时间，内网系统默认5分钟太短了，可以设成`30m`即30分钟甚至`4h`。

设置较长的`keepalive_timeout`也可以减少请求ssl会话协商的开销，但同时得考虑线程的并发数了。

深入探索

编程语言教程

企业安全咨询

Web安全课程

**提示**：在生成证书请求csr文件时，如果输入了密码，nginx每次启动时都会提示输入这个密码，可以使用私钥来生成解密后的key来代替，效果是一样的，达到免密码重启的效果：

```
openssl rsa -in ittest.key -out ittest_unsecure.key
```

导入证书

如果你是找一个知名的ssl证书颁发机构如VeriSign、Wosign、StartSSL签发的证书，浏览器已经内置并信任了这些根证书，如果你是自建C或获得二级CA授权，都需要将CA证书添加到浏览器，这样在访问站点时才不会显示不安全连接。各个浏览的添加方法不在本文探讨范围内。

安全运维咨询

# 2. 部分页面ssl

一个站点并不是所有信息都是非常机密的，如网上商城，一般的商品浏览可以不通过https，而用户登录以及支付的时候就强制经过https传输，这样用户访问速度和安全性都得到兼顾。

安全运维咨询

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

安全运维咨询

* 上面配置中使用了`proxy_set_header X-Forwarded-Proto $scheme`，在jsp页面使用`request.getScheme()`得到的是https 。如果不把请求的$scheme协议设置在header里，后端jsp页面会一直认为是http，将导致响应异常。
* ssl配置块还有个与不加密的80端口类似的`location /`，它的作用是当用户直接通过https访问首页时，自动跳转到不加密端口，你可以去掉它允许用户这样做。

# 3. 实现双向ssl认证

上面的两种配置都是去认证被访问的站点域名是否真实可信，并对传输过程加密，但服务器端并没有认证客户端是否可信。（实际上除非特别重要的场景，也没必要去认证访问者，除非像银行U盾这样的情况）

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

* [Nginx部署部分https与部分http](http://blog.csdn.net/na_tion/article/details/17334669)
* [Linux+Nginx/Apache/Tomcat新增SSL证书，开启https访问教程](https://www.zhoufengjie.cn/?p=185)
* [SSL & SPDY 已全面部署](https://www.sinosky.org/ssl-and-spdy-enabled.html)
* [SSL证书与Https应用部署小结](http://han.guokai.blog.163.com/blog/static/136718271201211631456811/)
* [ngx\_http\_ssl\_module docs](http://nginx.org/en/docs/http/ngx_http_ssl_module.html)
* [Optimizing HTTPS on Nginx](https://bjornjohansen.no/optimizing-https-nginx)
* [http://zhangge.net/4861.html](https://zhangge.net/4861.html)
* <http://blog.chinaunix.net/uid-192074-id-3135733.html>

原文地址：<http://seanlook.com/2015/05/28/nginx-ssl/>

* 标签：
* [#http](https://mrxn.net/tag/http)
* [#ssl](https://mrxn.net/tag/ssl)
* [#https](https://mrxn.net/tag/https)
* [#nginx](https://mrxn.net/tag/nginx)
* [#vps](https://mrxn.net/tag/vps)
* [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

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

* [1.
  1. 全站ssl](#toc-1-)
* [1.1.
  https优化参数](#toc-1-1-)
* [2.
  2. 部分页面ssl](#toc-2-)
* [3.
  3. 实现双向ssl认证](#toc-3-)



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

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[nginx配置ssl加密（单双向认证、部分https）](https://mrxn.net/jswz/nginx-ssl.html)  
文章链接：<https://mrxn.net/jswz/nginx-ssl.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/nginx-ssl.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/nginx-ssl.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 