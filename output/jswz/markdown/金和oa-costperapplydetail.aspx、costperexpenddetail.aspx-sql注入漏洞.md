---
title: "金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CostPerApplyDetail-sqli.html
asset_dir: assets/金和oa-costperapplydetail.aspx、costperexpenddetail.aspx-sql注入漏洞
---

# 金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/21 13:31
* 270浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

编程语言教程

恶意软件分析工具

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CostPerApplyDetail.aspx` 、`CostPerExpendDetail.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

服务器安全服务

网页浏览器

身份验证

根据 `CostPerApplyDetail.aspx` 的源码（与`CostPerExpendDetail.aspx` 相同），在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CostPerApplyDetail** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (!((Control) this).Page.IsPostBack)
  {
    if (this.Request.QueryString["DeptID"] != null)
    {
      this.strDeptID = this.Request.QueryString["DeptID"].ToString();
      ((HtmlInputControl) this.hiddenDeptID).Value = this.strDeptID;
      this.txtDeptName.Text = this.cc.GetDeptName(this.strDeptID);
    }
    if (this.Request.QueryString["UserID"] != null)
    {
      this.strUserID = this.Request.QueryString["UserID"].ToString();
      ((HtmlInputControl) this.hiddenUserID).Value = this.strUserID;
      this.txtUserName.Text = this.cc.GetUserName(this.strUserID);
    }
  }
  this.DataBindData(1, this.page_size, (DataSet) null);
}
```

深入探索

在线安全工具

防火墙软件

安全研究工具

**GetDeptName**

```
public string GetDeptName(string DeptID)
{
  string empty = string.Empty;
  DataTable dataTable = this.db.ExecSQLReDataTable($"select DeptName from Department where DeptID = '{DeptID}'");
  if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
    empty = dataTable.Rows[0]["DeptName"].ToString();
  return empty;
}
```

**GetUserName**

```
public string GetUserName(string UserID)
{
  string empty = string.Empty;
  DataTable dataTable = this.db.ExecSQLReDataTable($"select UserName from Users where UserID = '{UserID}'");
  if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
    empty = dataTable.Rows[0]["UserName"].ToString();
  return empty;
}
```

参数`DeptID`、`UserID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/Cost/CostPerApplyDetail.aspx/?DeptID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞](images/img-001-1255b595344b.webp)](https://image.mrxn.net/992b205052ad45b4bbd7b693e9c3ad04.webp)

[![金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞](images/img-002-4217b532d2d9.webp)](https://image.mrxn.net/50f9de4521024360b22920b1278da7b3.webp)

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
文章标题：[金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-CostPerApplyDetail-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-CostPerApplyDetail-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CostPerApplyDetail-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-CostPerApplyDetail-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 