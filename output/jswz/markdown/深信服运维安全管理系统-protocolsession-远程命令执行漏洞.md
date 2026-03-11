---
title: "深信服运维安全管理系统 protocol/session 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor-osm-protocol-session-rce.html
asset_dir: assets/深信服运维安全管理系统-protocolsession-远程命令执行漏洞
---

# 深信服运维安全管理系统 protocol/session 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/19 07:20
* 1305浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

SSH

Secure Shell

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 protocol/session 接口存在远程命令执行漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上[执行任意命令](https://mrxn.net/tag/rce)，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。

安全运维咨询

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

深入探索

数据库

安全

身份验证

直接看 `com.sbr.isomp.protocol.controller.session.SessionController` 的实现方式

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-001-a2b8caa3a3ac.webp)](https://image.mrxn.net/df21ae1f2c154f6e904d29c671fa19a2.webp)

从上图可以看到要进入此方法的路径是 **/protocol/session**

深入探索

网页浏览器

VPN服务

编码转换工具

## ssh

然后继续看下面的实现

漏洞修复方案

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-002-ef3957992712.webp)](https://image.mrxn.net/0185645f597b488e8e0ccb0fe1f946a0.webp)

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-003-bc393b960c82.webp)](https://image.mrxn.net/e4c4418372864ad28cc46d10da1f6830.webp)

当 **protocol=ssh** 时，尝试从请求参数中获取 `keyPath`（私钥文件的路径）。如果路径存在且当前不是 SSH Daemon 模式（`sshd` 参数为 false）：

计算机服务器

1. **文件读取与类型检查**：它尝试读取用户提供的 `keyPath` 指向的文件内容。
2. **格式转换（如果需要）**：如果读取到的私钥内容不包含 PEM 格式的标识符（`RSA PRIVATE KEY` 或 `DSA PRIVATE KEY`），代码会尝试使用 `ssh-keygen` 命令行工具对该私钥文件进行格式转换，将其转换为 PEM 格式。
3. **命令行执行**：在格式转换过程中，它将用户提供的 `keypassword` 参数（如果存在）直接拼接到 `ssh-keygen` 的命令行参数中执行。
4. **会话存储**：无论是否发生异常，私钥文件的内容和私钥密码（`keypassword`）最终都会被读取并存储到会话对象中。

命令注入的关键点在于用户提供的 `keyPath` 和 `keypassword` 两个参数在未经过任何严格的沙盒或转义处理的情况下，直接拼接进了 `ShellExecutor.service().exe()` 执行的系统命令字符串中。

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-004-05b5b40cff26.webp)](https://image.mrxn.net/8631c889dc0e44ad98e44e2e86c02637.webp)

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-005-91d9c5904155.webp)](https://image.mrxn.net/1f9d687c06584d678914fd745bdeeaeb.webp)

攻击者可以通过在这些参数中注入分号或管道符等，造成任意[命令注入](https://mrxn.net/tag/rce)漏洞，执行任意的操作系统命令。

数据格式与协议

## x11

同样的问题也出现在当 **protocol=x11** 时，

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-006-ce4cea31f5eb.webp)](https://image.mrxn.net/22c2caddeab94c0886b58579ef38d176.webp)

首先尝试从 `resolution` 参数中解析出期望的会话宽度和高度，如果该参数为空，则使用默认值 1024x768。随后，它调用 `ShellExecutor` 执行一个 Bash 脚本 (`/usr/local/bin/sh/x11vnc.sh`)，并传入解析出的宽度、高度以及用户提供的 `hostname` 和 `port` 参数作为脚本的命令行参数。脚本执行结果会被记录并解析，如果成功，它会将脚本返回的新端口号更新到会话中。

代码安全审计

命令注入漏洞的关键在于处理用户提供的 `hostname` 和 `port` 参数，以及间接控制的 `resolution` 参数（如果解析失败或被恶意构造），都未经任何安全处理或转义，直接拼接到了 `bash` 命令的末尾。攻击者可以通过在 `hostname` 或 `port` 参数中注入 shell 元字符（如 `;`、`|`、`&`），在执行 `/usr/local/bin/sh/x11vnc.sh` 脚本的同时，执行任意的附加系统命令，从而实现[远程代码执行](https://mrxn.net/tag/rce)。

# 漏洞复现

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-007-788e654dca5b.webp)](https://image.mrxn.net/10424b4d902246808b34a079f0ac6837.webp)

## POC

### ssh

```
POST /isomp-protocol/protocol/session HTTP/1.1
Host: osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

protocol=ssh&keyPath=/etc/group&sshd=1&keypassword=RCE_POC
```

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-008-0fb5d9b02f6e.webp)](https://image.mrxn.net/6248f86bd94e4d819c8ab3aef327c1c9.webp)

获取到[命令执行](https://mrxn.net/tag/rce)的结果

### x11

```
POST /isomp-protocol/protocol/session HTTP/1.1
Host: osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

protocol=x11&port=1337&hostname=RCE_POC
```

[![深信服运维安全管理系统 protocol/session 远程命令执行漏洞](images/img-009-6a1e3b9ae482.webp)](https://image.mrxn.net/75a45f1dd44748ff9af8167f73e5e98f.webp)

获取到[命令执行](https://mrxn.net/tag/rce)的结果（两个参数**hostname**和**port**均存在同样的命令注入漏洞）

漏洞修复方案

# 参考

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)

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
* [4.1.ssh](#toc-4-1-)
* [4.2.x11](#toc-4-2-)
* [5.漏洞复现](#toc-5-)
* [5.1.POC](#toc-5-1-)
* [5.1.1.ssh](#toc-5-1-1-)
* [5.1.2.x11](#toc-5-1-2-)
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
文章标题：[深信服运维安全管理系统 protocol/session 远程命令执行漏洞](https://mrxn.net/jswz/sangfor-osm-protocol-session-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor-osm-protocol-session-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor-osm-protocol-session-rce.html"),
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

代码安全审计

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALRUlEQVR4AeyaiVIkOQxEefP//zxLVpIuX3VwdffGmFiRUiolG8sGlpg/b29vf79qf08++p4n0rL+Hc1Z36Nc+Lp/uB5rTfxoEgfDC2ec+M+aBvJes/57lRMoA3mf8Ntdu7P59DrTAm9AkQBNXBLvzp1+vQa+1+992el/4L5ZT9gLxd21urYMpCaX/7wTGAYCnj6MeLVN2GuizS1JDKMmuWjBmvBCGLmaB+eB4aVLJ4NdA/azZhDMAyrZLLkt+OQnYHv1MOKs1TCQmWhxjzuBXxsI+EacfSm5eUFoa8AxUNpEGyJxjcB2K3tNYmH0YC0YlYvByCUnBOcBhT9ivzaQH9ndP9jkRwYCNDdS55gbKP+zltoZQrsWOIYd+/XAubpfNDV35IPrwZja38AfGchvbOxf7fk7A/lXT/MHvu5hIEfPVvzResrJ6jz4eYMxOeli0OaiAfOwY3LB9JhhNMFo4LgfOJcaIZhL/RlKP7PP1gwDmTVd3ONOoAwEfBvgGvvtgWvq2xBNOLAm/Bmm5kyTHLgvEGpAYPulI32FYG4QnxDQ1oBjYKgCtjXhGuviMpCaXP7zTuCPbstX7Wzb6RlNH4sPB75FiZW7a6kR9jXw9b7qpZ4ycB9xVyb9d2y9kKsTfnB+GAj4NoBxth9wDozRgGMgVPk+GgIoHNhPLghzPnkhWAMjKi/LTZUvg12rWAbm5F9Z+sFYA+bAmF7gGAh1isNATtUr+esn8AdobmxWzG1ILARrkwsq1xu0Wmjj1ApTC9eaaGeoXrLkwP3AGP4MwVrY8Uzf57S+DFzf5xVDmwPHwNv/6YW8/QsfayAvNuXLgcD+nPQUZbBzQPmSlOsN2L4lhi/iEwdcU0vAXPrMEFpNXS+/rlEsCye/t+SC0PYPX2Pfo47B9eGgjcVfDkSiZY87gTKQesryswX5MfBEE/eYGiFYK18GjmFH8bK+T2LljgzcZ5YH5/o+YB4oZcD2ggtROeAcGJOCNhYPLZe1a5ROVnPyxcXKQEIsfO4JHA4E2onX2wTnwJgcOAZCDagbEUsSaG4pOIYd72ij6fuHn2G0wVoTLphcH4vvOfDelYvd0RwOJE0WPvYEyh8Xsyy0kwXHcP3vnXIDzjDrzBC8VupnmnDR1JgcuE/iWhM/OTjW9pq+NnkhuA8YZ1pwDozR1LheiE7zhWwN5IWGoa1c/i2rfk7gpwbGOicfzMOIWkwGe07xmaln7EzX51IDXqvPK44mCNbCjtLNDHYN2E+f6MF8YmE0QXG9rRfSn8iT4+GH+tn0kgvCeAv6r+dMC219tOkBzgOhCgLNr8olMXHAWhixl2cPQrBevgzauK4F52pOPpiHe7heiE7thWwYCHiS2SM4BkJtNxOOYwl1o2TyZfKvTLor63tc6et8XVvz8pMDDr++aKQ/smjO8KhW/DAQkcuedwKHAwHflHprYO5o+jNtOHAt3MfU1giur7n42RdYkzgY3RlGK4xOvgzcF4ziekvNDMF1s1y4w4FEsPCxJ3A5kPoGZGvgSYMxfK2ND9YkjlYYLihOlrhG8bJw8mXg/oDCzaIBys8DaP0jzdbg41Ov+aBPAdp1anH6BZNLLLwcSIoWfuoEvixeA/ny0f1OYfnTSdrr2cgSw/4EwykvSwy7BuwnJ50MzMuPRQNtDhzDjqkBc6kNLwwH1oiTha8R5howDxS5etRWEpUDbN8ea518MA9UarvKyxz583ohPoeX+Tz86eTOzoDtNvRaTTvW52YxtH2gjdNLCG0OHMOIWQucU70s/BlKF4sO3Cdx8mAeSGo7F6BgSVQOOB8KHAPrH8q9vdhH+ZaVqWd/fSw+XI/Kfcf6fonPekYzw9Qll3iG4Ns508I8B+brfqnvsdbAWFfn5ZeBKFj2/BMYfsvKluB4mnCcS/1nENp+0MZnvcBaYJAB5Xs5MOTvEsDtPmDtnd4watcLuXNyD9SsgTzwsO8sdTqQowb5wdXnwU8QRowW9ly49APnwoNjINSAqRX2SXGy8PJjPQds35bCC4+0PS9t7CzXa2baLw0kjRf+/AmUgYBvCBhnS4Fz0GK0mfgMzzR9ro/VL1wQ2j3AHvca1ctg1yiWgbnUfBXBfaDFup/Wk9Vc75eB9IkVP+cELgeiicayxT4OD+3tgD2eaWYc7P9kFcb61BztQfk+B+4TXihdbeJkYC3sKF5W6+WLiymuLXyN4J7RgeNaczmQFC98zAmUPy7WU6r92TZgnKxqZtqvcDDvrzVi6ZtYGA5cn1g5GZgHkjpF1cgiArbfxMAYXihdbeJkYC2gcDNg6xP9Rn58Wi/k4yBeBQ7/dHK2wdlkpQ9fo3hZOPm9Jddjr6tj8C2DHZNPn8RgTXhhcvJlfSwOXJfcHYS2Rn1ifT20WuXXC9EpvJA9YSAv9NW/4FbKD3Vonw+0cb13cA6Mde7IB2vzfIVH2hkPrk9O9bLEQsUyaLXK9QZzDZgHSgmw/RAuxMQBa7S+DBzDjpOygVovZDiS5xJlIJqqDDxR+TJwDJSdipcVYuIA262SrraJdNMBJQUUDuynBziOOLwQnJMv6zWJZwhtrepjvT48uAb2/5nttXWcumBysPcpA0ly4XNPoPzaC55StgOOM01hn0scBNcAoYabXhKVo94yYNPL7w2cSxk4hh1TE80Z3tGCe5/1SQ7m2qwjhGvNeiE50RfB8ltWvx9NVNbzisXL5NcmLhY+cTC8ENob02vAeUDyzaIJbuQXPgHbawRj+oFj2H8uJPeFZZqSvk9i2NdcL6Q5sucHayDPn0Gzg8OBgJ9Ro/4I4Dj3IRkAXAM7DqITon/ekYYXhguKk8G+JtgXXxuMfPoEo088Q2j7nGmSS1/h4UAiXvjYExgGoinVBp44UHaWfCE+HKD8oDzSfEgbANc15EUAYw2YgxZne4FWc7YcWBsNtLH4rBGEUQMjp1owD6x/bP32Yh/lhWSyZ/uLBjzRo1g8WJN+4mSJv4vqJQOvAxy2BLaXK31vh0XvCWjrwPF7avgPnAPjIKiI7AFGbRlIpV/uE0+gDAQ8LWhxtrdMOLnEsNcm9xmEvR5oSoHtloeENhafffSoXG8w1veaxGBt+oav8SgHrgVq+aFfBnKoWImHnkD542ImHDzbBXB5W1MPrTb9a4y25uSHFyqWyT8y8Fpg7HVgHigp9awN2L42OP7TSfSlybsDrnt3v/XfeiHfOr6fL14DOT3Txycv/9qb5ynM9uTLEp+hdDK4/6Rh1ELLqeeRZT9wXQPWgDG1NcJxLrqrvUgXjXxZ4hrXC9HJvJCVH+rgWwD38c7XAe6XWwCOYcc+l7juP+OUh72P4tpSE4RRm9wMwfq6p3yY85/NwdhnvRCd4gtZGcjshhxx/f6jq/lwQRhvQ59LXPe58lMjPNKC15YmBub6GjAP9KlbcfqfiYHtV+towTGw/rj49mIf5YVkX7BPC1o/mjsIru21uRXC5OTLoK0RF4s2CNbCiL3mqEd0dxG81qwfOAct1r37OrA2vHAYSN1g+Y8/gTWQx5/56Yo/MhAYn16/qp6jrOcVg+vly6CNa049ZOJk8q8M3A92TI161Ba+xjovH9xHfm91Xe+D61KTPJgH1g/1txf7+JEXcudrAt+CWgstlxsTrLXhoK2pNb0P1qa2z89icA3sONMdceC6o7z4fj+JhQ8biDay7PoEhoFoSkd21C76Oh8OfGMS15r4fQ5cAyP2NTBqwFy00MbhawRrshdhnb/ypZdFB+4HOyoviyYIu2YYSEQLn3MCZSCwTwnO/e9sFfbeui2y9APnEit3ZGea5Hqse4HXAmNyfY3i5HpU7srqGvBaYExtrSkDSXLhc09gDeS55z+s/h8AAAD//7jLw/0AAAAGSURBVAMAtcBRiTqlFBcAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor-osm-protocol-session-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 