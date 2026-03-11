---
title: "金和OA LeaveTypeEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LeaveTypeEdit-sqli.html
asset_dir: assets/金和oa-leavetypeedit.aspx-sql注入漏洞
---

# 金和OA LeaveTypeEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/11 13:31
* 234浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

数据库

服务器

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LeaveTypeEdit.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LeaveTypeEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.dossier.dll` 将其进行反编译后找到 **LeaveTypeEdit** 的处理逻辑

```
this.type = this.Request.QueryString["type"];
this.typeID = this.Request.QueryString["ID"];
this.type = this.type.ToUpper();
this.InitText();
if (this.IsPostBack)
  return;
if (!string.IsNullOrEmpty(this.type) && !string.IsNullOrEmpty(this.typeID))
{
  if (this.type.Equals("ADD"))
  {
    this.PageTitle = this.strPageTitle1;
  }
  else
  {
    if (!this.type.Equals("EDIT"))
      return;
    this.PageTitle = this.strPageTitle2;
    this.ShowTypeName(this.typeID);
  }
}
```

当**type=EDIT**且**ID参数不为空或null**时进入`ShowTypeName`方法

跟进`ShowTypeName`方法

```
  private void InitList()
  {
    string empty = string.Empty;
    this.List1.RecordCount = 2;
    this.List1.Identify = 0;
    string str = $"<root>{empty}{this.GetListData()}</root>";
    this.List1.WidthStyle = UserWebControl.DataGrid.DataGrid.EnumWidthStyle.Fix;
    this.List1.DataSource = (object) str;
  }
```

跟进`GetListData`方法

```
private void ShowTypeName(string typeID)
{
  this.txtTypeName.Text = this.leaveType.GetTypeNameByID(typeID);
}
```

继续跟进`GetTypeNameByID`方法

```
public string GetTypeNameByID(string typeID)
{
  object obj = this.db.ExecSQLReobject("select leaveTypeName from LeaveWorkerType where delflag=0 and leaveTypeid=" + typeID);
  return obj != DBNull.Value ? obj.ToString() : string.Empty;
}
```

参数`ID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.dossier/LeaveTypeEdit.aspx/?ID=SQLI_POC&type=EDIT HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LeaveTypeEdit.aspx SQL注入漏洞](images/img-001-20ac0546226d.webp)](https://image.mrxn.net/60a51351c7c243859741870e2684e7e0.webp)

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
文章标题：[金和OA LeaveTypeEdit.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-LeaveTypeEdit-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-LeaveTypeEdit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LeaveTypeEdit-sqli.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-LeaveTypeEdit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 