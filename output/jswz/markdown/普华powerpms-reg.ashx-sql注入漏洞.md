---
title: "普华Powerpms Reg.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-Reg-sqli.html
asset_dir: assets/普华powerpms-reg.ashx-sql注入漏洞
---

# 普华Powerpms Reg.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/29 08:30
* 918浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

安全认证考试

文件大小转换

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统Reg.ashx接口存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

看下Reg.ashx的实现逻辑

```
if (context.Request["hum"] != null && context.Request["hum"].ToString().Length > 0)
{
    string HumId = context.Request["hum"];
    Power.Systems.StdSystem.HumanBO bo = Power.Systems.StdSystem.HumanBO.FindByKey(HumId);
    if (bo != null)
```

当 **hum** 参数不为空且长度大于0时，进入Power.Systems.StdSystem.HumanBO使用FindByKey来查找，这个属于老熟人了。使用FindByKey查找，无过滤或校验，因此造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，就是朴实无华。

代码安全审计

# 漏洞复现

> weixin3.0/Reg.ashx
>
> 深入探索
>
> 安全研究工具
>
> 漏洞预警服务
>
> 网络安全培训
>
> weixin3.0/static/Reg.ashx
>
> PowerMobile2/Reg.ashx
>
> 逻辑一样

```
POST /weixin3.0/Reg.ashx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

hum=SQLI_POC
```

[![普华Powerpms Reg.ashx SQL注入漏洞](images/img-001-6fb5ce9990f6.webp)](https://image.mrxn.net/fffe07381a914af8a3ef32786d27a52e.webp)

通过[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)成功在响应回显数据库版本信息

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
文章标题：[普华Powerpms Reg.ashx SQL注入漏洞](https://mrxn.net/jswz/powerpms-Reg-sqli.html)  
文章链接：<https://mrxn.net/jswz/powerpms-Reg-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/powerpms-Reg-sqli.html"),
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

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/powerpms-Reg-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 