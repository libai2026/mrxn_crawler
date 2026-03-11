---
title: "金和OA LeaveInfo.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LeaveInfo-sqli.html
asset_dir: assets/金和oa-leaveinfo.aspx-sql注入漏洞
---

# 金和OA LeaveInfo.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/10 13:31
* 204浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

Windows安全工具

企业安全咨询

技术文章订阅


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LeaveInfo.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LeaveInfo.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.dossier.dll` 将其进行反编译后找到 **LeaveInfo** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.InitText();
  if (this.Request.QueryString["UserID"] != null)
    this.UserID = this.Request.QueryString["UserID"].ToString();
  if (this.IsPostBack)
    return;
  this.InitList();
}
```

跟进`InitList`方法

深入探索

身份验证

网络安全培训

Web安全课程

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
  private string GetListData()
  {
    StringBuilder stringBuilder = new StringBuilder();
    DataTable leaveInfo = this.dossier.GetLeaveInfo(this.UserID);
```

继续跟进`GetLeaveInfo`方法

```
public DataTable GetLeaveInfo(string UserID)
{
  DataTable leaveInfo = this.dboperator.ExecSQLReDataTable($"select a.LeaveID,a.LeaveType,a.LeaveTime,a.[filename],b.[filename] as handOverFileName from LeaveWorker a left join LeaveHandOver b on a.HandOverID=b.HandOverID Where a.LeaveID in (select LeaveID from LeaveWorkerAttach Where LeaveCode = '{UserID}' and LeaveState = 1) and a.LeaveFlag =1 and a.DelFlag =0 ");
  if (this.dboperator.IsError)
    this.strErrMessage = this.dboperator.ErrorMessage;
  return leaveInfo;
}
```

参数`UserID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.dossier/LeaveInfo.aspx/?UserID=SQLI_POC&gettype=getstation HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LeaveInfo.aspx SQL注入漏洞](images/img-001-ab14eda0f92c.webp)](https://image.mrxn.net/f7acb3a091864821a7ac66e51941af39.webp)

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
文章标题：[金和OA LeaveInfo.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-LeaveInfo-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-LeaveInfo-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LeaveInfo-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-LeaveInfo-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 