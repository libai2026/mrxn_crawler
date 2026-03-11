---
title: "索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-statistics-countJztMonthsDetailArticle-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjztstatistics-多个sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/16 08:16
* 510浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

服务器安全服务

漏洞扫描器

Web安全课程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/Jzt/statistics/countJztArticle、countJztTWArticle和countJztMonthsDetailArticle接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

深入探索

技术文章订阅

漏洞修复方案

漏洞预警服务

## countJztArticle

根据漏洞信息看下`mch/Jzt/statistics/countJztArticle`的实现逻辑

```
public Response countJztArticle(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "startTime",required = false) Long startTime, @RequestParam(value = "endTime",required = false) Long endTime, @RequestParam(value = "isTw",required = false,defaultValue = "0") String isTw, @RequestParam(value = "isRenYuan",required = false,defaultValue = "0") String isRenYuan, @RequestParam(value = "userCode",required = false) String userCode) {
    List args = new ArrayList();
    StringBuffer sqlBuffer = new StringBuffer("select zcnarticle.id ");
    sqlBuffer.append(" , (select zcchannel.channelname from zcchannel inner join zccatalog on zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" where zccatalog.ID = zcnarticle.catalogID) as channelName ");
    sqlBuffer.append(" , (select zcchannel.channelid from zcchannel inner join zccatalog on zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" where zccatalog.ID = zcnarticle.catalogID) as channelid ");
    sqlBuffer.append("  from zcnarticle  ");
    sqlBuffer.append(" , ( select  distinct zcnarticle.id as articleid from zcnarticle where 1=1 ");
    if (isTw.equals("0")) {
        SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    } else {
        SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_WRITE_STATUS_LIST);
    }

    if (!isRenYuan.equals("0")) {
        sqlBuffer.append(String.format(" and zcnarticle.createUserCode= '%s' ", userCode));
    }
```

深入探索

网络安全课程

安全研究报告

网络安全会议

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-001-df4931e0c420.webp)](https://image.mrxn.net/981c68908573488d997e0caa51384d61.webp)

代码一看就很明了了，当isRenYuan不等于0时，**userCode**无任何过滤或校验，被直接拼接在SQL语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

如果没有String.format，就不存在，因为默认的append方法底层是参数化查询。

代码安全审计

## countJztTWArticle

其实和上面的countJztArticle一样的处理逻辑

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-002-8c5ef393b254.webp)](https://image.mrxn.net/d831bcdc374f40819768ce830884255d.webp)

## countJztMonthsDetailArticle

和上面的countJztArticle一样的处理逻辑

漏洞扫描服务

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-003-097b39df2025.webp)](https://image.mrxn.net/bdb321b1ea7b4d98a5cdd69bf731f2af.webp)

# 漏洞复现

## countJztArticle

```
GET /sobey-mchEditor/js/..;/mch/Jzt/statistics/countJztArticle?siteCode=&token=&userCode=admin&channelId=1&isRenYuan=1&userCode='SQLI_POC HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-004-e760d250cba4.webp)](https://image.mrxn.net/9f2a7019b458492386125264842ca63f.webp)

成功利用报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据用户

编程

## countJztTWArticle

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-005-674e03af47c2.webp)](https://image.mrxn.net/9cf37094730040d9800d960b587e2921.webp)

同样的[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)

## countJztMonthsDetailArticle

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-006-7a2ede42ca07.webp)](https://image.mrxn.net/e0c8d3ed847043989fb32390c73a2eb1.webp)

也是同样的[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)

漏洞扫描服务

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
* [4.1.countJztArticle](#toc-4-1-)
* [4.2.countJztTWArticle](#toc-4-2-)
* [4.3.countJztMonthsDetailArticle](#toc-4-3-)
* [5.漏洞复现](#toc-5-)
* [5.1.countJztArticle](#toc-5-1-)
* [5.2.countJztTWArticle](#toc-5-2-)
* [5.3.countJztMonthsDetailArticle](#toc-5-3-)



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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](https://mrxn.net/jswz/sobey-statistics-countJztMonthsDetailArticle-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-statistics-countJztMonthsDetailArticle-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-statistics-countJztMonthsDetailArticle-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALWElEQVR4Aeybi3LbuBJEdfL//5zrUe+hiSEgyptcSVVLV5BmP2YIY6jIym5+3W633/9m/f7ny9p/6AFWvnpHG6h3fqaXb03H8mp1XV7ebHVfLlrTufpPsAbylb9+fcoJbAP5mu7tmbXaOHADDrY9u7HSgXsffRi5uv3ke9QTYezRdbm471XXkHp9CIegeseqfWbt67aB7MXr+n0ncBgIZOow4mqLPgH68FydebH36TqMfeGcr3p0vXNI7667R1H/DCH9YMRZ3WEgs9Clve4E/nggkKn71HTs3wokD0HzEL7Km+vY83sO6QnBvbe/hsf+Pju7dk8z76faHw/kpze88o9P4K8NBPKUwRxX24Dk9X3aYNT1IToE1Wdor+5BaiHYc533evmzOfPP4F8byDM3uzLnJ3AYiFPveNbK/D339Ztc/JKGX+odDanLIU+zXH+GZsSeURchvWFE/Y6QXNdXvN9fPssfBjILXdrrTmAbCGTq8Bh/ujVIv1UdjD6M3LrVUwXJA0YPCNw//Xej9+zcPMzrz3xIHTxG+xRuAylyrfefwC+fip+iW7cO8hTI9c/QPIz1MPJVH+sLzzLdh/EeMHLz1bsWxFeHkatX9t+u6xXiKX4ILgcC8+nDXPeJ6N+XOox1EA5Bc9bLIT4E9SEcjmimIyRrb30YdQiHEc33+s7NwVgP4Y/85UAsuvC1J7ANBDI9CK62sXoazEPqYcReJxet76gv6stnaAbme4Do5uzRuXrHnpOfoX0e5baBPApd3utO4DCQ1RQhTxUE+xZhrq/69frO4dDvHnnUD+Y198Kv32D07QXRYcSvkvsveE6H5O5Fu9+8z05aXh4GskxexktOYBvIs1M0B889DTDmej2MPoSvchAfgrNTsnbmPdKsE3tWHXJvuWgeRl99hdYXbgNZhS/9tSfwCzLNftuaVi31uq4FYx5G3vNyEeZ5/bpHLUiurmfLPCQHKB3Qeg05cP87rs4hOgStO0P7mIPUQ1C9I8QHbtcr5PZZX9vfZa22Bd/TAw7/79aqbqX7FInmIPeRd1+9o7k9mlE74zDe27xoH0iuc4je853D41zlr1dIncIHreV7CIzTdM8w1/tTY36FMPY5q4fkIWhfCIdv1OsI3xlgs733Cg3qA8N7T9dh9K0XIb58j9crZH8aH3B9OhCn39G9q8tFyFOw8rsOyfd6iN7z8hnaQ4T0kIvAja8lFyF5GFFfhNHve4HRt85c56WfDsSiC19zAttPWZBprm4L8WGO1tWU9wuS14eR77P7a/NqchHSB87RHh3t9SxC7tX7yO0DY07dHMSHoH7h9QqpU/igdRgIZGp9mvIVQur83iDcPMx5z0NyXZfbT1QvVBNLe7TOcvod7QnzvZo3J4cx33Xg+qR++7Cvw+eQPrW+X8iUYUTrev6MQ/qYO+sDyUPQukKIBkF7QXhlasFjXplakBwES6sF4b2/vDK1ILm6rnXmV+bwR1aJ13rfCWw/ZTk9yFTlolvsXB1SB8Gur+rURRjr1e3XufoezUB6yc3IIb46hOuL3ZeL5iD16iLMdf09Xq+Q/Wl8wPXpQGCcLozcp6N/LysdUq8P4dari+odH/mQnmYgvPfo/Kd5mPcF7n/XZf/eVz7D04HY9MLXnMD2UxaM04Y5d6puD8Zc9zu3riOkD8zRPIy++h69JyQr32ceXZ/l9UV7yUV1seuQ/cE3Xq8QT+tD8DCQPsW+T8g0u24djD6EQ7DXdW4f9c7VHyGM94JwCPbafg+Y53qdHJKHEVe++gwPA5mFLu11J7B9Dum37E+NvONZ3bO+fc13ri7qz7BnzjiMT7Y9rXsWretovXrn6oXXK8TT+RDcBlLTqXW2L8jT9GyuetYyD4/rIT4Ez+ogOcDohsDweWAzFhe1z1raMNaXV0t/hTDWmYNRh5FXbhtIkWu9/wSugbx/BsMOlh8MKzVb9ZKtNfNKg/FlCCOv2lqVfbQqUwvG+l5TGdcjrzKQXjBiebWsh/il1VLvCMl1vWpqdV0OYx2EA9d/oLp92Nfhjyz4nhawbRe4v0HCiAYgej0ZtdTF0mrJO8JYDyOv2lrWQXw4ohkRkpGL1a+WXCytFszrIHplalkH0WFEfbFq9ku98DCQEq/1vhPYPhg6Mbey4uqi+TOEPDU91/vAmINwCJoX9/26BmONWXMQH4L6EG5OXVSH5LreuXlRH1KvXni9QjydD8FtIJBp9X3V1GpBfAiaK2+/YPR7Dua+OXHfs67VRUif8lx6nXcdxlp9GHUI7z5E9z6iuc7VIXUQVN/jNpC9eF2/7wS2zyHPbuFs+s/2gTwlELTO/jDq+hDdnPoeIZm9Vtcw18urteqpLla2FqQfBEurBXPe6ytbC5IHrs8htw/72v7IcnoiZGrut+sQH4LmRPNy8ffv34d/Fme2ENKvrmtZ1xGS2+sQrepq6cGol1dL/6dYtbMFuc9ZP2tnuW0gM/PSXn8Ch4FApuwUIRyC6m5VLqpD8p3DqOt3hOQg2H3vB/Hh+x+kmjUjh2TlojmID0F9EaJDUF20j3yFkHrzezwMZNXk0l9zAtsndRin5u2dnhySk4sQ3byo3zkkrw/hPaffdUhevxBGDUa+6gHzXM/XPf5kQe7T+0J04Pop6/ZhX9vnEKcG39OC72v9jpCM3xeEQ1BdtF4urnR90dwMzcB4b7P6K+w5SB8I6osQ3X4Qrq/eufoMr/eQ2am8UdveQ/oe+lQh04cRrTO/QnOQ+s5h1O2zysGYN7fH3kMPUqsv6nfUh9R1H0YdHnPrYcyVfr1C6hQ+aG3vIc/uyadFtA4ybQh2XS5a31FfXPnq5grVxNL2C7K3lW8WxhyE64u9T+eQOnXR+hler5DZqbxR2wYCmeZqL04X5jl9EZJbce8Dyck7QnwIdn/PYcxAOATdizUQHUbsvlyE5OW9r1yEMW+daK5wG4jmhe89gW0gNZ1abgfmU61MLYhf17XO6p71zZ0h5P7wjdZANHlHmPv1fdQyX9e15GJpteSQfjDHytYy3xG+67aB9NDF33MC2+cQyJRqkrMF8SFoBsIhqO63A9Hl3VeHMQcjN2e9qF6oJpa2XzD2NCdC/M7tcabr97z8GbxeIc+c0gszh4FAnhIIuhenL6qL6vC4DuJD8Nl6c5A6CKo/QvfWM5AeEOx+r4Pkut7rnuX22eNhIM82u3L/nxNYflJ3av22kKdEfZXTP0PrYd4XRv1RP0gWgmYh3Ht1NNcRUqduHYw6hEPQPIRDsOvyPV6vkP1pfMD19lOW0xdXe+s+ZPoQXPn2O/PNiebFla5f2DNyyB5XXF2sXrXkMNari5WdLX3RjBzSF7j+i+Htw7629xD4nhKcX/t9OG1R/Vm0TrQOsocV7zqgtCFw/zct9hYh+hZsFxAfgta12L030OWlbhDYMoDyHa/3kPsxfM5v20B8Cs5wtXXgPvXu208d5jkYdetg1O0jmitUE0urBekBwdL2q+f11CF18jPs9Wf5vb8NZC9e1+87gcNAIE8DjHi2RZ8KSJ3cOpjr+ivsfcxB+sERzawQxprVPVa6fbsPY18INw/h1s3wMBCLL3zPCfzxQCBTh6BTh3AIrr49eOz3Ovs/g9aa7VwdsgcImhPNdYTHeetF6+VwrP/jgdj8wr9zAn88kLOpd3+1bXMi5OmBoHUQDkc0I8KYOdP7vc2LkH5y0To5JNd1/Y6QPHB9Ur992NfhFeJUO57te5WHTF8fRt5176PeUX+GkN4QXNV2XW5POaQPBNV7Ti6ag9Spw8jN7fEwEIsvfM8JbAOBTA8e42qbMNY59Z5XhzHfcytuvbjPqYl6kHvJRYgOczQnQnIrrr7C1b4gfYHrPeT2YV/bK+TD9vWf3c7/AAAA//+my40oAAAABklEQVQDAJNDzr9l7EJgAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-statistics-countJztMonthsDetailArticle-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 