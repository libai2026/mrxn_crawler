---
title: "金和OA AskAttachment.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AskAttachment-sqli.html
asset_dir: assets/金和oa-askattachment.aspx-sql注入漏洞
---

# 金和OA AskAttachment.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/23 13:31
* 325浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

服务器

数据库

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AskAttachment.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AskAttachment.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Ask.dll` 将其进行反编译后找到 **AskAttachment** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Expires = -1;
  string strFileIdList = this.Request["AttachmentIdList"];
  if (!string.IsNullOrEmpty(strFileIdList))
    this.Response.Write(JHSoft.Ask.Ask.GetAttachmentName(strFileIdList));
  this.Response.End();
}
```

参数`AttachmentIdList`被带入`GetAttachmentName`方法

```
public static string GetAttachmentName(string strFileIdList)
{
  string str = string.Empty;
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select FileName from files where FileId in ({strFileIdList})");
  for (int index = 0; index < ((InternalDataCollectionBase) dataTable.Rows).Count; ++index)
    str = $"{str}{dataTable.Rows[index]["FileName"].ToString()},";
  return !string.IsNullOrEmpty(str) ? str.Substring(0, str.Length - 1) : str;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

深入探索

身份验证

漏洞预警服务

网络安全会议

# 漏洞复现

```
GET /c6/Jhsoft.Web.Ask/AskAttachment.aspx/?AttachmentIdList=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AskAttachment.aspx SQL注入漏洞](images/img-001-c99a9e3d8743.webp)](https://image.mrxn.net/7bec9eb961eb43d58f408023c2b31657.webp)

成功延时 4 秒

代码安全审计

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
文章标题：[金和OA AskAttachment.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AskAttachment-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AskAttachment-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AskAttachment-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AskAttachment-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 