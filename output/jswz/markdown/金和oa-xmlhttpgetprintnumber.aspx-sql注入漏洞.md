---
title: "金和OA XmlHttpGetPrintNumber.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-XmlHttpGetPrintNumber-sqli.html
asset_dir: assets/金和oa-xmlhttpgetprintnumber.aspx-sql注入漏洞
---

# 金和OA XmlHttpGetPrintNumber.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/22 13:35
* 292浏览
* [0评论](#comment)
* 22分钟阅读

深入探索

云安全解决方案

文本剥离工具

网络安全培训


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `XmlHttpGetPrintNumber.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `XmlHttpGetPrintNumber.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **XmlHttpGetPrintNumber** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (((Control) this).Page.IsPostBack)
    return;
  string strModelCode = this.Request["tid"];
  string strFileId = this.Request["gfid"];
  if (string.IsNullOrEmpty(strModelCode) || string.IsNullOrEmpty(strFileId))
  {
    this.Response.Write("");
    this.Response.End();
  }
  else
  {
    this.Response.Write($"{GovType.getFilePrintNum(strModelCode, strFileId)}|{GovType.getFileSourcePrintNum(strModelCode, strFileId)}");
    this.Response.End();
  }
}
```

深入探索

物流软件安全

技术文章订阅

Web安全书籍

参数`strModelCode`、`strFileId`被带入`getFilePrintNum`或`getFileSourcePrintNum`方法

```
public static string getFilePrintNum(string strModelCode, string strFileId)
{
  string QueryString = "";
  if (string.op_Equality(strModelCode, "IOA_Send"))
    QueryString = $"{QueryString} select (convert(int,SendFs)) - (convert(int,SendFsResult)) as strPrintNum from SendDoc where SendID = '{strFileId}' ";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  return ((InternalDataCollectionBase) dataTable.Rows).Count <= 0 ? "0" : dataTable.Rows[0]["strPrintNum"].ToString();
}
```

```
public static string getFileSourcePrintNum(string strModelCode, string strFileId)
{
  string QueryString = "";
  if (string.op_Equality(strModelCode, "IOA_Send"))
    QueryString = $"{QueryString} select SendFs as strPrintNum from SendDoc where SendID = '{strFileId}' ";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  return ((InternalDataCollectionBase) dataTable.Rows).Count <= 0 ? "0" : dataTable.Rows[0]["strPrintNum"].ToString();
}
```

至此，就非常明了了，当**`tid`**`=`**`IOA_Send`** 时**，gfid**参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/XmlHttpGetPrintNumber.aspx/?tid=IOA_Send&gfid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA XmlHttpGetPrintNumber.aspx SQL注入漏洞](images/img-001-546d1a27e457.webp)](https://image.mrxn.net/f07b8d356312409b87430e183f332aaf.webp)

成功延时 8 秒

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
文章标题：[金和OA XmlHttpGetPrintNumber.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-XmlHttpGetPrintNumber-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-XmlHttpGetPrintNumber-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-XmlHttpGetPrintNumber-sqli.html"),
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-XmlHttpGetPrintNumber-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 