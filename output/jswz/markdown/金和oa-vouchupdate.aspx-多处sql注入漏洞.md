---
title: "金和OA VouchUpdate.aspx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-VouchUpdate-sqli.html
asset_dir: assets/金和oa-vouchupdate.aspx-多处sql注入漏洞
---

# 金和OA VouchUpdate.aspx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/14 13:28
* 298浏览
* [0评论](#comment)
* 27分钟阅读

深入探索

代码安全审计

漏洞扫描服务

安全研究工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `VouchUpdate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

身份验证

网络安全课程

数据库

根据 `VouchUpdate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **VouchUpdate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  if (!string.IsNullOrEmpty(this.Request["no"].ToString()))
    ((HtmlInputControl) this.hidAppNo).Value = this.Request["no"].ToString();
  if (!string.IsNullOrEmpty(this.Request["type"].ToString()))
    ((HtmlInputControl) this.hidAccType).Value = this.Request["type"].ToString();
  this.cm.BindDropDownList(this.ddlAccount, this.cm.dtAccount(), "请选择", "");
  this.cm.BindDropDownList(this.ddlVoucherType, this.cm.dtVoucherType(), "请选择", "");
  ((ListControl) this.ddlAccount).SelectedValue = this.cm.GetAccByRecordNo(((HtmlInputControl) this.hidAppNo).Value);
  ((ListControl) this.ddlVoucherType).SelectedValue = this.cm.GetVoucherByRecordNo(((HtmlInputControl) this.hidAppNo).Value);
  this.getAccSubData(((HtmlInputControl) this.hidAppNo).Value, ((HtmlInputControl) this.hidAccType).Value);
  this.fType = this.cm.getFinanceType();
}
```

深入探索

恶意软件分析工具

文件大小转换

VPN服务

参数**no**和**type**赋值给**hidAppNo**和**hidAccType**后被带入`GetAccByRecordNo`、`GetVoucherByRecordNo`与`getAccSubData`方法中，它们的实现如下

代码安全审计

## GetAccByRecordNo

```
public string GetAccByRecordNo(string strRecordNo)
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"SELECT ZT FROM dbo.Budget_RecordNoVouch WHERE RecordNo='{strRecordNo}'");
  return ((InternalDataCollectionBase) dataTable.Rows).Count == 1 ? dataTable.Rows[0][0].ToString() : "";
}
```

至此，就非常明了了，参数`projid`被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

## GetVoucherByRecordNo

```
public string GetVoucherByRecordNo(string strRecordNo)
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"SELECT VoucherType FROM dbo.Budget_RecordNoVouch WHERE RecordNo='{strRecordNo}'");
  return ((InternalDataCollectionBase) dataTable.Rows).Count == 1 ? dataTable.Rows[0][0].ToString() : "";
}
```

## getAccSubData

```
public void getAccSubData(string recordNo, string accType)
{
  DataTable dataTable = this.cm.Budget_AccountSubject_Search(recordNo, accType);

public DataTable Budget_AccountSubject_Search(string AppNo, string accType)
{
  return this.db.ExecSQLReDataTable($"select Budget_AccountSubject.*,Budget_Subject.SubjectCode from Budget_AccountSubject\r\nleft join Budget_Subject on Budget_AccountSubject.ItemCode = Budget_Subject.SubjectNo and Budget_Subject.DelFlag=0 where AppNo = '{AppNo}' and acctype='{accType}'");
}
```

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/VouchUpdate.aspx/?no=SQLI_POC&type=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA VouchUpdate.aspx 多处SQL注入漏洞](images/img-001-cfe170f49a54.webp)](https://image.mrxn.net/2cb5d0ca3b8f4b06a557abb11b118a7a.webp)

成功延时 4 秒

漏洞预警服务

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
* [4.1.GetAccByRecordNo](#toc-4-1-)
* [4.2.GetVoucherByRecordNo](#toc-4-2-)
* [4.3.getAccSubData](#toc-4-3-)
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
文章标题：[金和OA VouchUpdate.aspx 多处SQL注入漏洞](https://mrxn.net/jswz/jhsoft-VouchUpdate-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-VouchUpdate-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-VouchUpdate-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-VouchUpdate-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 