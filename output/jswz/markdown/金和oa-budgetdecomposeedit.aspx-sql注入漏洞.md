---
title: "金和OA BudgetDecomposeEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BudgetDecomposeEdit-sqli.html
asset_dir: assets/金和oa-budgetdecomposeedit.aspx-sql注入漏洞
---

# 金和OA BudgetDecomposeEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/27 13:05
* 271浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

SQL

数据库

木马


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BudgetDecomposeEdit.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BudgetDecomposeEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **BudgetDecomposeEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strAppId = this.Request["httpAppID"].ToString();
  this.strBudgetDecomposeId = this.Request["httpOID"].ToString();
  this.strAppNow = this.GetAppNow("Budget_Decompose", this.strAppId);
  if (!this.IsPostBack)
    this.BindBudgetDecomposeInfo();
  this.InitPrive();
}
```

跟进`GetAppNow`方法

```
private string GetAppNow(string appt_id, string app_id)
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"select appd_id,Instance_ID from jhoa_approve where app_id='{app_id}'");
  string str1 = dataTable.Rows[0]["appd_id"].ToString();
  string str2 = dataTable.Rows[0]["Instance_ID"].ToString();
  ((MarshalByValueComponent) dataTable).Dispose();
  string str3 = this.db.ExecSQLReobject($"select version FROM JHOA_Approve_Instance WHERE (Instance_ID = '{str2}')").ToString();
  return this.db.ExecSQLReobject($"select appds_level from dbo.jhoa_approve_temp_dispose_sort where appt_id='{appt_id}' and version='{str3}' and appd_id='{str1}'").ToString();
}
```

参数`httpAppID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

深入探索

身份验证

安全

技术文章订阅

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/BudgetDecomposeEdit.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

httpAppID=SQLI_POC&httpOID=1
```

[![金和OA BudgetDecomposeEdit.aspx SQL注入漏洞](images/img-001-c222dd727371.webp)](https://image.mrxn.net/d70a8d33cb674ff9b1cae5934fa14fac.webp)

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
文章标题：[金和OA BudgetDecomposeEdit.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-BudgetDecomposeEdit-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-BudgetDecomposeEdit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-BudgetDecomposeEdit-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-BudgetDecomposeEdit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 