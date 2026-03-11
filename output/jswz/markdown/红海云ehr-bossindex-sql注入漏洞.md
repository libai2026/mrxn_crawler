---
title: "红海云eHR BossIndex SQL注入漏洞"
source: https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html
asset_dir: assets/红海云ehr-bossindex-sql注入漏洞
---

# 红海云eHR BossIndex SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/30 08:15
* 441浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

数据库

身份验证

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

红海云eHR系统中的BossIndexController（BossIndex.mc、BossIndex.mob等多个方法）模块存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL查询语句，绕过系统认证，实现对数据库的非法访问，获取敏感信息（如用户凭证、个人数据等），甚至在特定条件下可能导致数据库被完全控制，影响范围包括数据访问权限和系统控制权限。

SQL注入防护

# 影响版本

# fofa语法

> body="/RedseaPlatform/skins/images/favicon.ico"

# 漏洞分析

## 未授权路由

先看下 web.xml 里对于这些.mc、.mb和.mob后缀是如何校验的

最开始的CharacterEncodingFilter基础校验，编码校验，这里没有权限校验

代码安全审计

[![红海云eHR BossIndex SQL注入漏洞](images/img-001-ed961be18943.webp)](https://image.mrxn.net/32a0ccc6c44a487ba230a4e64682a829.webp)

接着往下看，进入AuthenticationProcessingFilter过滤器

漏洞扫描服务

[![红海云eHR BossIndex SQL注入漏洞](images/img-002-e5f059040959.webp)](https://image.mrxn.net/db7d3a1c731742c1a45e2f521273d8f0.webp)

这里是**权限校验**，**校验.mc后缀**，因此网上看到的poc都没有使用此后缀，因为需要权限校验！

接下来进入常见的dispatcherServlet过滤器

[![红海云eHR BossIndex SQL注入漏洞](images/img-003-134695d3e31c.webp)](https://image.mrxn.net/a8be342fbf624ecf8976395a2114fb2e.webp)

如图所示，这里没有权限校验，支持的url后缀列表如

编程

```
*.mc
*.mob
*.mb
/messageInteface
/cdata
/fdata
/devicecmd
/getrequest
/getrequest.none
/token
/ectpdata
```

## SQL注入

接下来进入本文的正题 **BossIndexController** ，看下它的实现逻辑

网络安全

[![红海云eHR BossIndex SQL注入漏洞](images/img-004-99d8dcb7fcfd.webp)](https://image.mrxn.net/1e843afaefd6463381ec3f84aa81b46d.webp)

如图所示，支持的路由有`"/BossIndex.mc", "/BossIndex.mob"` 两种，结合之前的权限分析可知，我们可选择`/BossIndex.mob` 达到[未授权访问](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)此接口的目的。

### getNumOfMembers

再看需要的参数`params = {"method=getNumOfMembers"}` 对应的 **getNumOfMembers** 方法里

`String tree_code = req.getParameter("struTreeCode");` 参数`struTreeCode` ==> `tree_code` 然后 `tree_code` 被直接拼接进 `sql1` 和 `sql12` sql语句后，无任何过滤或校验处理直接执行拼接后的SQL语句，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。其他几个方法亦如此，存在同样的sql注入漏洞，下面简单记录下它们的实现。

SQL注入防护

### getNewStaffJoin

[![红海云eHR BossIndex SQL注入漏洞](images/img-005-c103cfcb6141.webp)](https://image.mrxn.net/7c23c20874b94f8b8298a323a0584262.webp)

### getNewStaffLeave

[![红海云eHR BossIndex SQL注入漏洞](images/img-006-5eab265ce038.webp)](https://image.mrxn.net/b1036afcdb2240a38f8a4b14ca9cf8a2.webp)

### getNewStaffRetire

[![红海云eHR BossIndex SQL注入漏洞](images/img-007-b4f01f0f212e.webp)](https://image.mrxn.net/1df878a7a54d41b68c725a945d2bb0dd.webp)

### getJoinAndLeaveStaff

[![红海云eHR BossIndex SQL注入漏洞](images/img-008-caafd37ffed9.webp)](https://image.mrxn.net/57cd2277e9ce4650bc3d1dc00b071b37.webp)

### getTodayKaoQin

[![红海云eHR BossIndex SQL注入漏洞](images/img-009-da8b8fc9062b.webp)](https://image.mrxn.net/6f1c58bd6c5f4434a669e8c50282ef80.webp)

### getEarlierWorkStaff

[![红海云eHR BossIndex SQL注入漏洞](images/img-010-587511e012c5.webp)](https://image.mrxn.net/93795f05d0c44d86839da685cadb2d6c.webp)

### getAbsenceStaff

[![红海云eHR BossIndex SQL注入漏洞](images/img-011-402967f27e43.webp)](https://image.mrxn.net/e0d0238d3f524c04bff147af3bd3e236.webp)

所有上述这些方法均存在一个或多个参数的直接拼接导致的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /RedseaPlatform/BossIndex.mob HTTP/1.1
Host: redseaplatform.mrxn.net
Content-Type: application/x-www-form-urlencoded

method=getNumOfMembers&struTreeCode=SQLI_POC
```

[![红海云eHR BossIndex SQL注入漏洞](images/img-012-c77ef558d000.webp)](https://image.mrxn.net/71b1dd0da7734645a16d2c0e061fb371.webp)

成功延 6 秒（执行三次）

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

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
* [4.1.未授权路由](#toc-4-1-)
* [4.2.SQL注入](#toc-4-2-)
* [4.2.1.getNumOfMembers](#toc-4-2-1-)
* [4.2.2.getNewStaffJoin](#toc-4-2-2-)
* [4.2.3.getNewStaffLeave](#toc-4-2-3-)
* [4.2.4.getNewStaffRetire](#toc-4-2-4-)
* [4.2.5.getJoinAndLeaveStaff](#toc-4-2-5-)
* [4.2.6.getTodayKaoQin](#toc-4-2-6-)
* [4.2.7.getEarlierWorkStaff](#toc-4-2-7-)
* [4.2.8.getAbsenceStaff](#toc-4-2-8-)
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
文章标题：[红海云eHR BossIndex SQL注入漏洞](https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html)  
文章链接：<https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALf0lEQVR4AeycDXsbNw6E/fb//+eeZyfDBb9WiqvYunb9BBlgMAApYmnJzl3/+vj4+Pur9vfFV3qOkvDC5OTLxljcaKMm8RWmx0qT3BWu6sTVGsWyyn3F10A+6+4/73ICbSCf0/141sbNAx/QW3qN2vDCMQfuoZys5hXLwJrkwDEQqu0lhOpkiSuKr7bKAUfP5MDxrk66mnvkSx9rAwlx48+ewDQQ8PRhxt1WV0/AqIW5H5jbaSsPa+1Kk/0kB49ro301gteGGVdrTQNZiW7u+07gpQOB+SkAc8+8pDzZwVoTLlhzow9eE4ypAcdw4lgbrXDMjTHs+4zaZ+OXDuTZRW/d/gReOhA9VbEsmfgKow2Cn7xaA+bAGO0zCK6p/eKDc2Cs/cDcqK2aV/svHcirN/df7PdnBvJfPMkXveZpILmeK9ytCb7aNZ/6cDBroOegj1MrHPslXqH0sjEnLgZea9SAeSDS44dC4PIH5yYenLF/jQfpEU4DOdj7rx87gTYQoD0JcO0/s1twj2e0eWqiTQzuASQ1IdD2PSV/EWDNr3AJYE3WFkYoXwbWhAfHQKiGQNsXXPut6NNpA/n07z9vcAJ/afJftav9p2c0ieF8WkYucWqewdQIn9H/E43WkIFfg/xY+ib+Kt43JCf5JvhwIOCnAfaYpwFOzfj6wLnKw8zV/JUProUZx7qr/YHrx5oagzVgrLnRB2vAOOZrDLPm4UBqg9v/8yfwF3hKsMY8XcJsR74s8asQvIf00xqxkUtcMdogPO5X63d++gWjA/cHQl0icHzyimjsJ/7/6YZov/96uwfyZiPeDiTXCXzNgLZ1oLt60MdNWJz0q5h05eSHB/eFGaWTRVsRrFdelhyYh/PXIMlJJ0ssVCwD14mTiRtNfLXkKxcf3A+M4YXbgSh52/efQBvIbqLhhdmefNkYi4tBP31wDCemPgjOJV7hrr+04PpRAz2vvPQy+TKwRlwMzCkvA8fJr1A6Gcxa8dVSD9YCH20gH/fXW5xAGwh4StkVOIYTx1ymHb5icuD65MJXBGvCPaN9RpN+wdRcIXgvQJMB3XtmSxQHrAFjSW3d7KtiG8i26k586wlMA6nTkl93o7ga+GkAY9XCzNX8ygfXwB7r+vJrH3BdOOjj8BWh16hnrOrkhwfXwInJSfesgeurfhpITd7+95/APZDvP/PLFad/D7lSg68YGL9yTVf90ycYTWJhOPDaiStKJwsnX5YYXAuEmhA43sCBllMPWSN+OeJiwFH3K7UEeKy5b8jy6H6O3A4EPM08AcJsU74Mek3yVwiuASYZcDxl6i0DxzD/qiPFcGrA/i6nnjGwNnFqEgvDBWFdk/wjVE/ZqAP3Be4fDD/e7Kv9e8gz+9J0ZeCJypetasXLVrlw4D6Jg2Be9bHkRky+4k4D7guMkva/uZoSCwI4bnJN1fXl11x8mOuSC26/ZUVw4/eeQPuUlWXBU9SUZeGF0OfAMRilGU09dhYtuD668CuMBlxzpRlzqa0IfR9wDOf7FphLXfqCeSDUcXPgrG2JCyd9hfcNuTion0hN7yGakgxo0wb74mXgOBsWJ0u8QnANnBidamWJg3Bqofell0HPAymf3heA6TU18S9HPWO/qAke5VUA+7XAOelGu2/IeCKvib/c5R7Il4/uzxS2N3XwNQLj6lrCPqftgfOAwsOA49tE+q3wEH7+BdZ+uts/qV8JkgP3gR5XNSMHfQ0wSo7XA+cbt9YFDn4UK/fIwLXA/YPhx5t9tW9Z4xSv9gmeaDTQx+Jh5sRXg7Vm3EuNwTVgvOqXuqrZ+eB+qRFGK182xuAaIKkJgePmAFMuhHrH2kCSvPFnT6B97AWOSV5tJ1Mc8apmzIHXAVoKONZO35YoDlgTKtoVRgN9TXjhWCdOBq6B8z1CfDWwpnJjv8RVA66DHqvmviH1NN7AbwNZTXS3P/CEd3nxu37hVwjuCzOq58rg1K7y4rKW/J1FUzFa8BqJrxD22tpb/qpPG8gqeXPffwL3QL7/zC9XbD8YRgXnlQs3oq6bbMcrB+4jXzZqXxWrd2zsueOlA+8PelRutKs+r9beN2Q80R+Op4+9V08D9E8TOM5rAMfw+CMjkLIJr/YQMXB8VIYZR03i9F1hNFcIXiv1VQvOQY9VM/pgbeXvG1JP4w389h6SqYOnBsbwwuxXvixxUFwMXA89RlsRrEltcomFK078laUmCF4HCNVuWQhgy42axCtc7Ss68BqJK943pJ7GG/jtPeSZvWTq0E84fO0xcokrgvuESz2YTyyMBpwDo3IxMAfG8MH0EEKvESeLVgi9RpxMutHEy8KDa+FE5atFW7n7htTTeAO/vYdkL+PU4Jww2I8mCOZhxmjSH05NuCA4N8ZAqPbv5OkLtO/54YIpAmsSC0eNuJ1FGwT3gxPHXOJVz+TA9VVz35B6Gm/g/8BA3uBVv/EWvjQQmK/a+BrHawmuCS9MDTiXOChNLFwQ1jXKg3O72itNaoTSycD9wChuZ6qTwayFmRv7fGkgY5M7ft0JTB97oZ+ipr0z2GvBudSutpxccKUZOXDf8KkVgnPyZbCO4fzVDlgDxvQVqodMvky+TL5Mfgzm+lETrfid3TdkdzI/xLePveAJj1ME80DbInB81Iw2COaBSduIhQMc/RaphxS4FniozT6FwJfXVL3s4YKfAvA6cOInvf1z35Dt0fxMor2HaOIy8CSvtiOdbNSIG23UgPvDidFc1YL1O22tHTXgWjgx+lGbWAjWy18ZOA/ze9LYX/UjlxjOPvcN0Um9kd0DeaNhaCttIOBrk2ukpCyxEKwBo/K/a+oT+53asQa8BzACrR1wvGGDMbUVoc+14oWTOnDNQtKoaBtRHOjroY8lbQNRcNvPn8A0EPDUMmlwDOcb1yoHpw5OP9rVS00uGA2c9dD70aSmIlhbOflgPrVC8TL51cBaOF9v8tLLxlgcnHVw+srFUgfOh684DSRFN/7MCbQfDOuU5F9tBzzhaKQfLbkRwbVw4qhJXHuOXGI4+0Q/5kY+eSG4Xr4sWqFiGfQacAwnSl9NdTI4NYpl0YFz4mL3DclJvAm2gYCnBT2u9pkJB1eacOB+iVMjDPcMSi+70oLXAmO04BhOTE49ZXDmoPeVl401iVcovazmFMvCyZclFraBKLjt509g+tWJJia72hr0TxA4XtWoVzWwFmhyoPu5oSWKA70GHBfJ5GbdJBILw42oXCw58FpgDF8RnIMeV5rKyYez5r4hOpE3snsgl8P4/mT72DsunWtbMZrKyQ8P59UL9zuoXrJVjXhZcvJ3Fk0wusRCOPcK8w+B0ox1icG10sSSGzH5iuB6MNaa+4bUk3oDv72pg6cFz+O4/zrp+OB+0YYXhguCtcrJwDGcGG0Q9rmVBqxX/2rPaKO5QnD/laauV/2qvW9IPY038NtA6sQe+bt9g58OODFaODmwn1ww6yauuMuFF1a9fOjXkSam/J+wr/QH7xO4/1snH2/21W5I9gXntKD3o/kK5smpmD7hwOuFv0KwFmZMXfoGwwthroPz05ZqpJOBtfJlysnkx8Aa6DF5ITgnv5p6xaaBVOHtf/8J3AP5/jO/XPElA8l1W+G4OvjaAmOq/X8/gON3W7UfmEtRzcVPLgh9DTgGImlr7no0YXGAaX8lfbjpt0Jw/SEc/nrJQIaed/gPTuCPDQT2T0H2m6cHem346IQrTny1R5rkK0K/NjgGWuvoQ4xx+BUCx20CWvqq/o8NpK1+O791AtNAMr0VPuoM/NbTANbv+oLzcGL2BScHvT/2A+dHXnH6yR8tOXA97DHaYHolFoa7wmkgV+I79+dPoA0E9tOHPrfblp6CWDTQ1yYvjEa+DKwdeeXCBcXJEl+hdLKqgX4t6GNpoefUY2fSPzLo+0UP5oH7Vycfb/bVbsib7es/u53/AQAA//8KlLD6AAAABklEQVQDAJwvhJjT3nKWAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 