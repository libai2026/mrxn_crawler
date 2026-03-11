---
title: "金和OA GroupOuterRegisterAdd.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GroupOuterRegisterAdd-sqli.html
asset_dir: assets/金和oa-groupouterregisteradd.aspx-sql注入漏洞
---

# 金和OA GroupOuterRegisterAdd.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/15 08:29
* 500浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

SQL

数据库

木马


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GroupOuterRegisterAdd.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GroupOuterRegisterAdd.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **GroupOuterRegisterAdd** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request.QueryString["ID"] != null)
    this.strID = this.Request.QueryString["ID"].ToString();
  this.strPageTitle = !string.op_Equality(this.strID, string.Empty) ? "外部系统修改" : "外部系统添加";
  if (((Control) this).Page.IsPostBack || !string.op_Inequality(this.strID, string.Empty))
    return;
  this.ShowInfo(this.strID);
}
```

GET请求会将参数`ID`带入`ShowInfo`方法

```
private void ShowInfo(string systemID)
{
  DataTable systemBySystemId = OuterSystem.GetOuterSystemBySystemID(systemID);
```

继续跟进`GetOuterSystemBySystemID`方法

```
public static DataTable GetOuterSystemBySystemID(string systemID)
{
  string QueryString = $"select * from OuterSystem where System_ID='{systemID}'";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

至此，就非常明了了，参数 `ID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/GroupOuterRegisterAdd.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GroupOuterRegisterAdd.aspx SQL注入漏洞](images/img-001-a5e4cecae89e.webp)](https://image.mrxn.net/70ae5c7e9e9246d7a5bdd940d48c8b36.webp)

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
文章标题：[金和OA GroupOuterRegisterAdd.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-GroupOuterRegisterAdd-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-GroupOuterRegisterAdd-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GroupOuterRegisterAdd-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GroupOuterRegisterAdd-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 