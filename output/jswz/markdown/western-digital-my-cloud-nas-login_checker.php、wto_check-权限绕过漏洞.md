---
title: "Western Digital My Cloud NAS login_checker.php、wto_check 权限绕过漏洞"
source: https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-login_checker-authbypass.html
asset_dir: assets/western-digital-my-cloud-nas-login_checker.php、wto_check-权限绕过漏洞
---

# Western Digital My Cloud NAS login\_checker.php、wto\_check 权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/3 08:18
* 732浏览
* [0评论](#comment)
* 27分钟阅读

深入探索

My Cloud

Western-Digital-My-Cloud-NAS

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital My Cloud NAS是美国西部数据（Western Digital）公司的一款应用广泛的网络连接云存储设备，可用于托管文件，并自动备份和同步该文件与各种云和基于Web的服务。Western Digital My Cloud NAS `login_checker.php` 接口文件未对用户会话进行严格验证，存在[身份验证绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)漏洞，攻击者可通过构造恶意 Cookie 绕过身份认证机制，直接获取普通用户或管理员权限。

硬盘驱动器

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> `icon_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"`

# 漏洞分析

## login\_check

直接看 `/lib/login_checker.php` 登录相关逻辑的实现

漏洞修复方案

```
function login_check()
{
        $ret = 0;
        if (isset($_SESSION['username']))
        {
                if (isset($_SESSION['username']) && $_SESSION['username'] != "")
                $ret = 2; //login, normal user

                if ($_SESSION['isAdmin'] == 1)
                        $ret = 1; //login, admin
        }
        else if (isset($_COOKIE['username']))
        {
                if (isset($_COOKIE['username']) && $_COOKIE['username'] != "")
                $ret = 2; //login, normal user

                if ($_COOKIE['isAdmin'] == 1)
                        $ret = 1; //login, admin
        }
        return $ret;
}
```

* `login_check()` 函数直接使用客户端可控的 `$_COOKIE['username']` 和 `$_COOKIE['isAdmin']` 进行权限判断，但未进行任何有效性校验。
* 当用户未登录（无有效 SESSION）时，系统直接信任 Cookie 中的 `username` 和 `isAdmin` 值，导致攻击者可[绕过权限](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)伪造身份。
* 即使存在 SESSION，由于逻辑缺陷，Cookie 仍可能影响权限判断，存在权限混淆风险。

因此只需要在请求header部分添加如下cookie即可绕过鉴权

计算机驱动器和存储设备

```
Cookie: username=admin; isAdmin=1
```

## wto\_check

在另一个检查管理员是否登陆超时的函数wto\_check()校验中也是存在漏洞的

```
/*
  return value: 1: Login, 0: No login
*/
function wto_check($username)
{
        if (empty($username))
                return 0;

        exec(sprintf("wto -n \"%s\" -i '%s' -c", escapeshellcmd($username), $_SERVER["REMOTE_ADDR"]), $login_status);
        if ($login_status[0] === "WTO CHECK OK")
                return 1;
        else
                return 0;
}

/* ret: 0: no login, 1: login, admin, 2: login, normal user */
```

`wto_check()`的PHP函数，会检查某个用户（$username）是不是已经超时,它会调用一个系统里的“wto”程序，检查某个用户名和IP对应的定时器（也就是登录状态是不是还有效）。

数据备份与恢复

`wto_check()`的PHP函数，会检查某个用户（$username）是不是已经超时,它会调用一个系统里的“wto”程序，检查某个用户名和IP对应的定时器（也就是登录状态是不是还有效）。

```
# wto --h
Usage: wto [parm]
-h        help
-n        user name
-i        ip address
-s        set timeout
-g        get timer
-c        check timeout
-r        reset timer
-a        remove all
-x        del timeout item
-z        show all
-d        del user
```

* 代码里用`exec()`函数去执行系统命令，把用户名和IP拼到命令里。
* 为了安全，开发者本来想对用户名做过滤，防止有人恶意输入特殊内容，结果用了`escapeshellcmd()`这个PHP函数。
* **但这个函数只适合过滤整个命令，不适合单独过滤某个参数！**
* 正确应该用`escapeshellarg()`，它会把参数用引号括起来，防止参数里带特殊字符或多余命令。

因此这会导致因为过滤不严，攻击者可以在用户名后面加特殊内容，比如加上`-s 99999`（意思是设置超时时间为99999）。这样系统本来只是想“查一下你是不是超时”，结果攻击者却能“顺便重置自己的超时时间”，让自己一直保持登录状态。这样攻击者就可以**绕过超时机制**，一直以管理员身份操作系统。

网络安全

可在cookie里添加 `username=admin" -s 9999 -c "` 这个来设置超时时间，从而让系统认为管理员没超时，从而绕过鉴权。

相当于调用 wto 程序的 -s 参数来设置超时时间为 9999 从而绕过了系统本有鉴权检查。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

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
* [4.1.login\_check](#toc-4-1-)
* [4.2.wto\_check](#toc-4-2-)



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
文章标题：[Western Digital My Cloud NAS login\_checker.php、wto\_check 权限绕过漏洞](https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-login_checker-authbypass.html)  
文章链接：<https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-login_checker-authbypass.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-login\_checker-authbypass.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-login\_checker-authbypass.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 