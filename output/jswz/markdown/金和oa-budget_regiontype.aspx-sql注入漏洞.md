---
title: "金和OA Budget_RegionType.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Budget_RegionType-sqli.html
asset_dir: assets/金和oa-budget_regiontype.aspx-sql注入漏洞
---

# 金和OA Budget\_RegionType.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/1 13:31
* 242浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

软件

数据库

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SubjectHandler.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `SubjectHandler.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **SubjectHandler** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitPage();
  if (this.Request.QueryString["RegionID"] == null || string.op_Equality(this.Request.QueryString["RegionID"], ""))
  {
    this.title = "区域添加";
    this.btnOK.Text = "添 加";
  }
  else
  {
    this.title = "区域修改";
    this.btnOK.Text = "修 改";
    ((WebControl) this.txtRegionID).Enabled = false;
    if (((Control) this).Page.IsPostBack)
      return;
    this.getInfomation();
  }
}
```

深入探索

JSON处理工具

在线安全工具

Web安全课程

跟进`getInfomation`方法看下其实现

代码安全审计

```
protected void getInfomation()
{
  DataSet typeInfomationById = this.costManager.Get_Budget_RegionTypeInfomationByID(this.Request.QueryString["RegionID"]);
```

`RegionID` 被带入`Get_Budget_RegionTypeInfomationByID`方法

```
public DataSet Get_Budget_RegionTypeInfomationByID(string RegionID)
{
  return this.GetDS_BySQL($" Select RegionName,remark from Budget_RegionType where RegionID = '{RegionID}' ");
}
```

参数`RegionID`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/CostManagement/TravelBasicSetting/Budget_RegionType.aspx/?RegionID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA Budget_RegionType.aspx SQL注入漏洞](images/img-001-d7f3e6743557.webp)](https://image.mrxn.net/14820c48be0d42d58156e4e8845add71.webp)

成功延时 4 秒

漏洞预警服务

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
文章标题：[金和OA Budget\_RegionType.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-Budget_RegionType-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-Budget_RegionType-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Budget\_RegionType-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-Budget\_RegionType-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 