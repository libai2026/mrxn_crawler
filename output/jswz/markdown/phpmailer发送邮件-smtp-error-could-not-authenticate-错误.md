---
title: "phpmailer发送邮件 SMTP Error: Could not authenticate 错误"
source: https://mrxn.net/jswz/phpmailer.html
asset_dir: assets/phpmailer发送邮件-smtp-error-could-not-authenticate-错误
---

# phpmailer发送邮件 SMTP Error: Could not authenticate 错误

[Mrxn](https://mrxn.net/author/1)* 发表于2015/10/8 20:33
* 9792浏览
* [3评论](#comment)
* 18分钟阅读

深入探索

服务器

server

sendmail


(adsbygoogle = window.adsbygoogle || []).push({});

---

今天在使用sendmail插件(phpmailer)发送邮件时居然提示SMTP Error: Could not authenticate，这个感觉是smtp设置的问题，下面我在网上找到了几种解决办法。

电子邮件与即时消息

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

网络安全

深入探索

安全研究报告

漏洞扫描服务

数据库

这个错误说明虚拟主机不支持PHPMailer默认调用的fsockopen函数，找到class.smtp.php文件，搜索fsockopen，就找到了这样一段代码：

```
// connect to the smtp server
$this->smtp_conn = @fsockopen($host,// the host of the server
    $port,// the port to use
    $errno,   // error number if any
    $errstr,  // error message if any
    $tval);   // give up after ? secs
```

  

**方法1：将fsockopen函数替换成pfsockopen函数**

首先，在php.ini中去掉下面的两个分号

;extension=php\_sockets.dll

;extension=php\_openssl.dll

然后重启一下

计算机服务器

因为pfsockopen的参数与fsockopen基本一致，所以只需要将@fsockopen替换成@pfsockopen就可以了。

**方法2：使用stream\_socket\_client函数**

一般fsockopen()被禁，pfsockopen也有可能被禁，所以这里介绍另一个函数stream\_socket\_client()。

stream\_socket\_client的参数与fsockopen有所不同，所以代码要修改为：

```
$this->smtp_conn = stream_socket_client("tcp://".$host.":".$port, $errno,  $errstr,  $tval);
```

  

这样就可以了。

如果上面办法还是没有解决可能是邮箱自动过滤你机器自动登录邮箱发邮件了哦,我是使用下面办法解决的

刚开始使用的qq的帐号，提示上面错误。换成新注册的163帐号可以正常发送。

之后换了一个qq等级比较高的帐号，这下可以正常发送，没有报任何错误。

因为收件人用的是qq邮箱帐号，所以发件帐号用qq的邮箱比较好，这样发送过多不会轻易的被拦截或判为垃圾邮件。

所以结论就是配置中使用一个qq等级比较高的帐号（我的一个小号等级2个月亮可以正常使用，当然等级越高越好，）

ps：也要查看邮箱中“设置邮件地址黑名单”及“收信规则”，有时系统会自动将一些邮箱自动加入黑名单的

* 标签：
* [#编程](https://mrxn.net/tag/%E7%BC%96%E7%A8%8B)
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#php](https://mrxn.net/tag/php)
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
文章标题：[phpmailer发送邮件 SMTP Error: Could not authenticate 错误](https://mrxn.net/jswz/phpmailer.html)  
文章链接：<https://mrxn.net/jswz/phpmailer.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

技术文章订阅

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/phpmailer.html"),
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

电子邮件与即时消息

  

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
text: encodeURI("https://mrxn.net/jswz/phpmailer.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 