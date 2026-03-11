---
title: "Apache下设置自动将http跳转到https方法"
source: https://mrxn.net/jswz/Apache-http-to-https-htaccess.html
asset_dir: assets/apache下设置自动将http跳转到https方法
---

# Apache下设置自动将http跳转到https方法

[Mrxn](https://mrxn.net/author/1)* 发表于2015/12/2 18:53
* 9665浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

认证

ssl

加密


(adsbygoogle = window.adsbygoogle || []).push({});

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

在线安全工具

网络安全课程

文件大小转换

## [SSL证书与Https应用部署小结](https://mrxn.net/https-apply-all.html)

* 标签：
* [#加密通讯](https://mrxn.net/tag/%E5%8A%A0%E5%AF%86%E9%80%9A%E8%AE%AF)
* [#emlog](https://mrxn.net/tag/emlog)
* [#http](https://mrxn.net/tag/http)
* [#ssl](https://mrxn.net/tag/ssl)
* [#https](https://mrxn.net/tag/https)
* [#nginx](https://mrxn.net/tag/nginx)
* [#vps](https://mrxn.net/tag/vps)
* [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)
* [#加密](https://mrxn.net/tag/%E5%8A%A0%E5%AF%86)

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
  emlog 使用ssl证书开启HTTPS安全访问三步曲](#toc-1-)
* [2.
  nginx配置ssl加密（单双向认证、部分https）](#toc-2-)
* [3.
  NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](#toc-3-)
* [4.
  SSL证书与Https应用部署小结](#toc-4-)



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
文章标题：[Apache下设置自动将http跳转到https方法](https://mrxn.net/jswz/Apache-http-to-https-htaccess.html)  
文章链接：<https://mrxn.net/jswz/Apache-http-to-https-htaccess.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读

Windows安全工具


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Apache-http-to-https-htaccess.html"),
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
text: encodeURI("https://mrxn.net/jswz/Apache-http-to-https-htaccess.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 