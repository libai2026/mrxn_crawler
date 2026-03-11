---
title: "金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForGetBudgetTime-sqli.html
asset_dir: assets/金和oa-ajaxforgetbudgettime.ashx-sql注入漏洞
---

# 金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/15 13:29
* 295浏览
* [0评论](#comment)
* 22分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForGetBudgetTime.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForGetBudgetTime.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForGetBudgetTime** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string strType = context.Request["strType"];
  string strPeriod = context.Request["strTime"];
  string str1 = context.Request["strYear"];
  string str2 = string.Empty;
  if (string.op_Equality(strType, "getTime"))
  {
    DataTable periodByYear = this.cc.GetPeriodByYear(str1);

else
{
  string strSubjectCode = context.Request["strSubjectCode"];
  string strValue = context.Request["strValue"];
  DataTable budgetImportData = this.deptCostSet.GetBudgetImportData(strType, strValue, str1, strPeriod, strSubjectCode);
```

根据**strType**的值进入不同的处理流程

[![金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞](images/img-001-e077d17e9c25.webp)](https://image.mrxn.net/09f03d61453146b6a7546b3df23e5521.webp)

当 `strType=getTime` 时，`strYear`被带入`GetPeriodByYear`方法

```
context.Response.ContentType = "text/plain";
string strType = context.Request["strType"];
string strPeriod = context.Request["strTime"];
string str1 = context.Request["strYear"];
string str2 = string.Empty;
if (string.op_Equality(strType, "getTime"))
{
  DataTable periodByYear = this.cc.GetPeriodByYear(str1);
```

跟进 `GetPeriodByYear` 方法

```
public DataTable GetPeriodByYear(string Year)
{
  return this.db.ExecSQLReDataTable($"{" Select distinct Budget_PeriodManage.Period " + " from Budget_PeriodManage " + " Left outer join Budget_PeriodDivert " + " on Budget_PeriodDivert.YearPeriod = Budget_PeriodManage.YearPeriod " + " and  Budget_PeriodDivert.Period = Budget_PeriodManage.Period "} where Budget_PeriodDivert.Status is null and Budget_PeriodManage.YearPeriod ='{Year}'" + " order by Period asc ");
}
```

非常明显的直接将strYear参数拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

GetBudgetImportData

[![金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞](images/img-002-60a520ad8673.webp)](https://image.mrxn.net/e2c271f4795d4bcaa4b670081f3e015c.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/BudgetExecution/Handlers/AjaxForGetBudgetTime.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getTime&strTime=&strYear=SQLI_POC
```

[![金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞](images/img-003-3e6f7cd9827a.webp)](https://image.mrxn.net/a4e5bf2b49b645e1b0ede8b930f8c196.webp)

成功延时 4 秒

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
文章标题：[金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AjaxForGetBudgetTime-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AjaxForGetBudgetTime-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForGetBudgetTime-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForGetBudgetTime-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 