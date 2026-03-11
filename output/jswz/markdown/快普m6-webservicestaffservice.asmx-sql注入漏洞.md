---
title: "快普M6 WebService/StaffService.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/kuaipu-WebService-StaffService-GetPositionOfStaff-sqli.html
asset_dir: assets/快普m6-webservicestaffservice.asmx-sql注入漏洞
---

# 快普M6 WebService/StaffService.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/1 08:28
* 745浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

企业安全咨询

安全认证考试

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

快普M6整合管理平台的WebService/StaffService.asmx接口下多个方法存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，绕过参数过滤机制，实现对数据库的任意查询、修改或删除操作，甚至可能获取系统控制权限。

SQL注入防护

# 影响版本

# fofa语法

> body="Resource/JavaScript/jKPM6.DateTime.js"

# 漏洞分析

深入探索

Web安全书籍

编程语言教程

漏洞修复方案

根据漏洞通告，看下 WebService/StaffService.asmx 里的cs引用

```
<%@ WebService Language="C#" CodeBehind="StaffService.asmx.cs" Class="KPMIIS.Web.WebService.StaffService" %>
```

ok,根据引用去找到bin目录下的KPMIIS.Web.dll文件，反编译后找到WebService下的StaffService实现

代码安全审计

```
[System.Web.Services.WebService(Namespace = "http://tempuri.org/")]
[ToolboxItem(false)]
[ScriptService]
[WebServiceBinding]
public class StaffService : System.Web.Services.WebService
{
  [WebMethod]
  public string GetPositionOfStaff()
  {
    string str = HttpContext.Current.Request.Form["sid"];
    DataRow row = Gateway.Default.FromCustomSql("select top 1 organization_name,position_id from dbo.COMMON_PositionToStaff p,dbo.COMMON_Organization o \r\n                                    where p.position_id=o.organization_id and staff_id=" + str).ToDataSet().Tables[0].Rows[0];
    return $"{row[0]},{row[1]}";
  }
}
```

深入探索

文本剥离工具

技术文章订阅

恶意软件分析工具

参数**sid**，没有经过任何过滤或校验检查就被拼接进SQL语句中进行执行了，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，非常的朴实无华。

漏洞扫描服务

# 漏洞复现

> 因参数使用**HttpContext.Current.Request.Form**获取，使用常规的GET或POST传参即可

```
POST /WebService/StaffService.asmx/GetPositionOfStaff HTTP/1.1
Host: kuaipu.mrxn.net
Content-Type: application/x-www-form-urlencoded

sid=SQLI_POC
```

[![快普M6 WebService/StaffService.asmx SQL注入漏洞](images/img-001-c9781b4b1005.webp)](https://image.mrxn.net/28df3967fff04a4babdc2d4e2c694294.webp)

成功通过报错注入在响应回显数据库默认用户信息

编程

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
文章标题：[快普M6 WebService/StaffService.asmx SQL注入漏洞](https://mrxn.net/jswz/kuaipu-WebService-StaffService-GetPositionOfStaff-sqli.html)  
文章链接：<https://mrxn.net/jswz/kuaipu-WebService-StaffService-GetPositionOfStaff-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/kuaipu-WebService-StaffService-GetPositionOfStaff-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALmklEQVR4Aeyd7XbjNgxEfff933lbZM6VRYiUnP2yf8in2NEMBiBNSImT7ml/PB6Pn78SP9vLHk3eeqt3n3yF1ondpz5DvT230vX1vFzUJ3Zd/itYA/m/7v7nU05gG8j/0368ElcbBx7wjO53DXX5CvW9gvBcF9jeD7ym9zUgderuEaJD0HxH/Ve4r9sGshfv6/edwGEgkKnDiKstQnzeBd3XdYi/++Qwz0N0+4kQHZ5PhL1EvfIVQnr1vPWQvLz7VhxSByPO/IeBzEy39u9O4I8NBDL9q7vHPMTvW4Xwnodz3fpCiLeuKyAcgqVVQLhriZWr6Bzir9wsun/meVX7YwN5dcHbd34Cvz2Q1d3RdTi/y/o2f7d+36/3MgfZEwRXvu/q9v8V/O2B/Mqid836BA4D8W7ouG6RjP4vdvIH5G7UAuHWQ7h5dXGlmy/Uc4Xl3cfKD+OeYOSrOvX9Gvtr83s8DGSfvK///QlsA4FMHc6xbxHiV4c5987Q17l6Rxj7rfJATx1+Ul+tCXz9dsEGEN79nXe/XIT0gXPUX7gNpMgd7z+BH079u+jWresccleoXyHEbz+Y895Hf2HPrXh5K8zXdQWMa67y6nDur57fjfsJ8XQ/BJcDgUwfgu4XwiF4pfe8/FWEcR3rIDocUY/oXQrxqnfsPogfgit/11cc0geCM99yIDPzrf39EzgMBNbTq+14F4mlzcJ8x5m3NH11vQ91cZ+ra/UZVn4fetTg/L3qWyGkHua4qjvTDwM5M9+5v38Ch4F4F3WE+V0A0a+2CvHZV3/n6iKk7vF4KC0Rzr2QPAT72hDdBcyLr+r6IP0gqN77QfLA4zCQx/166wlsA4HnlOB47VQ7unt1OaSHfIUw+iDcfmKvX+nlg/SAEStXcVZbeQNSL7cOokPQPIxcv3kR4oOgeuE2kCJ3vP8EfsA4pe9OtfvlIqS/3LcMc928CPFBsOvyQtdYYXlmAWPvXg9jvvfofvnKpz7z3U+Ip/MhePhdFszvBqcprvYPqYdg90P0Vb06zH32EyE+eGLvAcmtdHuZFyF1q3zXIX4I2keE6L1OXng/IZ7Wh+A2EBinV9PaByQPI/o+ILrcWjkkry5CdH2ieVFdhHmd+UJrxdJmAemlD8K7F0YdRm69aH3n6iKkD3D/HPL4sNfhUxZkWu4Twp1yR33qckid3DxEh6B5sftWur496hUha0BQXfyq/Vl/QT8KxKcuJvv8U118ZnIF6RP2/FM/JA/Bp+NxPyH7w/iE68OnrKtNAdN//wyjbh+Y694t3QejH8IhqP8MIV7X6HhWO8vB2E8PRIegugjRYUTz7kteuH1TL3LH+0/gMBCnBpnqq1yf6FvrXB3SX959V9w6SB94/u13ayG57l3lf1W3/xXaX4TsT154GMhV0zv/d0/g25+yIFNdbQvO83UXVPR6SF3lKmDk+itXId8jpAaC5auA8L13f12eChh9EA7Bfc3sGuKrXrOA5CGoB8KB+1PW48Ne26cs9+XUOkKmqK5/hd0Hqdff8+riVb77yt81yJqVqzC/wvJUmK/rWZjvqBeybs/L9XVe+v09xFP5ENy+h8B8qhC9plcB4e4fwiHYdbkI8UGweu5j5VM/Q/tAeuuF8Ks8xNfr4Fy3r3WPx2N62X0w9q2i+wmpU/ig2L6HXE0PMs3uu3ovcF4HydsHwq/WgfisK4RRs4cIycur5k8EpC8Ee0+IDiPO9nE/If303syXA5lNr/YKmXJdz8K6jt1r/krXB1kXgtZBOKC0xN5raWwJ65Q7V+8IDL/3s07UD/EB988hjw97bU8IPKcEHLbpVDt2IzDcFRAOQf0Qbr+uQ/IQNC9aN0M98P3a6md9XVfIRUjfylWo1/UszEPqIKi+x20ge/G+ft8JbANxsldbgfV0q9Y+MPeZF+HcVz3PAlIPHGx9DWB4eg8FCwFSB0H7LuxfawCHtHUi8OXdG7eB7MX7+n0ncA/kfWc/XXn71cksO9N83HpupXcfjI+pdRBd3utWXH/hyqNengrIWhA0D+HlqYCRd5+8Y9VWdB3SD4Ll6XE/If3U3sy3gUCmttoPJA8jdj8k3/V+J8Dct6rrOqQejqgXkuv81b3os/4KIevBiNb1fjD6gPsHw8eHvbYnpO8LMr2uO2Xx1TykHwStg3OuT3RdUf07COOavRckD0F7r3xd79x6mPfTX7gciE1u/LcnsPz1u9uoqVXIYZxy1yF5CFbtPvTvtf21eUg9BPVAuL4Z6u25rkN6QdB8R0jefublMObVRf0dzUPqgft7yOPDXocvWX2KkOm5b/MQXW6+I8TX9c5h9NlX1C+H+OV7hOSsEWGuW3vlg7HeOtH6K4R1n8NArprd+b97AttAYJwahPfpw6jDyPt2e/3j0R3h3QfpC8G4nn92f2UgXnNi5So6L60CUgfB7pOLVVMB8UPQPIy8vGcB8QP395DHh722J2Q1Xcj0zIur92FehNTrV5eLEF/Pd67/DCG99PQeclGfCGO9ugjzPES3L4TDiD1v38JtIEXueP8JHAbi9Nxa55BpmxchOgTVX63XD6m3DsLNixAdnmiNqFeEeDvXL/Y8pA6C5kXrRIhPru8VPAzklaLb8/dOYBsIZKouBSNXv5q6eZjX20eE+KxTfxWtK7QG0rPz8lSoixA/BNXLWyFfIczr4Ht6rbUNZLXYrf/bEzj8G0MYpwrhMKLbrKlWyCG+0iq6LhfLUyEX4bxP1VRAfPDE0ivsVdcVcrG0CrlYWoVcLG0f6h0he1G3BqLLRYgO3D+HPD7sdfhtr1Pr+1QXIVPVpy7CmNf3KvY+kH7qvU/xs1zlDUgvuWg9JA9B8xAOQXXr5B1h9MPIrS+8v4f003sz3wYC49TcV02tApKHYGkVEA4jVq7CPmJpFXIRUl+5CnWxtAo5xC8vhKM206tPReVmUbl96Nlrda0uwnz98lboq+sKiB+euA1E843vPYHtU1ZNrMLt1HVF56VVXOnmxaqpgOfdAM/rylXAU4PnfwzAPmJ5K+R7hPTYa7NrGH0wcmtqnQo5zH3my7sPGP0w8r33fkI8xQ/B7VMWjFPr+4Pk4Rytg9Gn7t0gv0JIH30QDkH7zRDisVaE6LOa0rpvxdU7QvpD0Hz1rpCLEB9w/xzy+LDX4UsWPKcFbNutye5jSywu9t66XtgO/1sifVWzD+DwV/f1doS5F6Lb96qu++Si9TD27fnuk898h4FovvE9J7B9yurLz6ZXHhjvhtL20esgfhhRH0SXi/aEMa8uQvLwRHPiqic8awDtX08iFI8EfGlhj69r4NFfwJYDenr7amAC+PLLC+8npE7hg2L7lOVdJK72eJWH49Sr13frIH2sg/DqVaE+w8rvA+a1e8/+2p57ra4hfVZ59Y5VWwGpr+t97P33E7I/mQ+43r6HQKYHr2Hf+37KdQ3ps/Kpl3cf6h31dB2yDtBTh6/ZGoCvr92v9ITnbwu6v/PeX75C6yH7Ae6fQx4f9tq+ZDmtK+z71991uXl43gWA6a87FTigBkhO3tH+hT0nr9wszK/QmlV+pV/V9by8cBvIqvmt/9sTOAwEckfCiKttweiD8Jp2BYRbX1qFfIXlqVjlIX3hiNbAmOu6vNap6BzO6yF56yAcRjRfa1TIIT554WEgJd7xvhP4YwOpyVe8+lYgd0fV7KPXm1OXz7B7OodxTQiHoD1h5F3vfc1fIaQvBO0D4cD9KevxYa/ffkK8KyBTln/3fcK8HqJD0L4QDk/sOfcC8fS8fOUzD6nXJ5rvCPHDiPqsF9ULf3sg1eSOP3cCh4E4tY6vLgm5K/TbRw7Jq8PIu0+uf8XV9wjprWYPUR3iUxdh1CEcgr1evsLeF8Y+VXcYSIl3vO8EtoFApgXnuNqq0+95SL+V3usg/pXe++grPMvt8zBfw3oY8zDy6lWhv64rOi+tQh3O+5RvG0iRO95/AvdA3j+DYQf/AQAA//8mr5t5AAAABklEQVQDABzAB63aJFybAAAAAElFTkSuQmCC)

手机扫码阅读

代码安全审计


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/kuaipu-WebService-StaffService-GetPositionOfStaff-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 