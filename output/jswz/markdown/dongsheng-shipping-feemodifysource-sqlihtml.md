---
title: "东胜物流软件 FeeModifySource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-Shipping-FeeModifySource-sqli.html
---

# 东胜物流软件 FeeModifySource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/4 08:26
* 353浏览
* [0评论](#comment)
* 40分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 Shipping/FeeModifySource.aspx 接口存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据 Shipping/FeeModifySource.aspx 的代码引用
`<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="FeeModifySource.aspx.cs" Inherits="DSWeb.Shipping.FeeModifySource" %>`
，在dll中找到
`DSWeb.Shipping.FeeModifySource`
的逻辑实现

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request.QueryString["handle"] != null)
    this.strHandle = this.Request.QueryString["handle"].ToString().Trim().ToLower();
  if (this.Request.QueryString["oplb"] != null)
    this.stroplb = this.Request.QueryString["oplb"].ToString();
  if (this.Request.QueryString["id"] != null)
    this.strFeeID = this.Request.QueryString["id"].ToString().Trim().ToLower();
  if (this.Request.QueryString["applytype"] != null)
    this.iApplyType = int.Parse(this.Request.QueryString["applytype"].ToString().Trim());
  if (this.Request.QueryString["applystate"] != null)
    this.iApplyState = int.Parse(this.Request.QueryString["applystate"].ToString().Trim());
  if (this.Request.QueryString["checkstate"] != null)
    this.iCheckState = int.Parse(this.Request.QueryString["checkstate"].ToString().Trim());
  if (this.strHandle.Equals("apply"))
  {
    string cells = this.GetCells(this.strFeeID, this.iApplyType, this.iApplyState, this.iCheckState);
    this.Response.ContentType = "text/xml";
    cells.Replace("&", "&amp;");
    this.Response.Write(cells);
  }
  else if (this.strHandle.Equals("exist"))
  {
    this.Response.Write(this.IsExistFee(this.strFeeID));
  }
  else
  {
    this.Response.ContentType = "text/xml";
    this.Response.Write("-2");
  }
}
```

当
**handle=apply且applystate=0**
时，跟进
`GetCells`
方法

```
private string GetCells(
  string tempFeeID,
  int tempApplyType,
  int tempApplyState,
  int tempCheckState)
{
  FeeDA feeDa = new FeeDA();
  FeeModifyDA feeModifyDa = new FeeModifyDA();
  if (tempApplyState == 0)
  {
    DataTable dataTable = new DataTable();
    string strSql = $" SELECT {""} GID, FEESTATUS, FEENAME, CUSTOMERNAME, UNIT, UNITPRICE, QUANTITY,COMMISSIONRATE,AMOUNT, CURRENCY,  EXCHANGERATE,FEEFRT,REMARK,ISADVANCEDPAY  FROM ch_fee WHERE 1> 0 {$" AND GID = '{tempFeeID}'"} {" ORDER BY ENTERDATE ASC "}";
    DataTable statusNameTable = this.getStatusNameTable(feeDa.GetExcuteSql(strSql).Tables[0]);
......
```

参数
`tempFeeID`
即外部用户可控参数
**id**
被直接拼接在
`string strSql = $" SELECT {""} GID, FEESTATUS, FEENAME, CUSTOMERNAME, UNIT, UNITPRICE, QUANTITY,COMMISSIONRATE,AMOUNT, CURRENCY, EXCHANGERATE,FEEFRT,REMARK,ISADVANCEDPAY FROM ch_fee WHERE 1> 0 {$" AND GID = '{tempFeeID}'"} {" ORDER BY ENTERDATE ASC "}";`
SQL语句中执行，无任何过滤或校验，从而造成
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

以及
**当 applystate!=0 时的多个分支**

例如
`applytype=1, checkstate=1`
时：

```
strSql1 = $"SELECT GID,APPLYSTATUS, FEENAME, CUSTOMERNAME, UNIT, UNITPRICE, QUANTITY,COMMISSIONRATE,AMOUNT, CURRENCY,EXCHANGERATE,FRT,REMARK,ISADVANCEDPAY FROM ch_fee_modify WHERE FEEID = '{tempFeeID}' AND APPLYTYPE = {tempApplyType} AND APPLYSTATUS = {1} ";
```

1. **参数类型确认**
   ：
   `tempFeeID`
   为字符串类型（在SQL中使用单引号包裹）
2. **过滤机制缺失**
   ：仅进行了
   `.Trim().ToLower()`
   处理，未做SQL注入防护
3. **拼接方式**
   ：使用字符串插值
   `$"{tempFeeID}"`
   直接拼接，未使用参数化查询
4. **执行方式**
   ：通过
   `feeDa.GetExcuteSql(strSql)`
   直接执行拼接的SQL

根据代码逻辑，触发不同SQL注入需要满足以下条件：

| 场景 | handle | applystate | applytype | checkstate | 触发位置 |
| --- | --- | --- | --- | --- | --- |
| 场景1 | apply | 0 | 任意 | 任意 | ch\_fee表查询 |
| 场景2 | apply | 非0 | 1 | 1 | ch\_fee\_modify表(APPLYSTATUS=1) |
| 场景3 | apply | 非0 | 1 | 2 | ch\_fee\_modify表(APPLYSTATUS=2或3) |
| 场景4 | apply | 非0 | 1 | 3 | ch\_fee\_modify表(所有记录) |
| 场景5 | apply | 非0 | 2 | 1 | ch\_fee\_modify表(APPLYSTATUS=1) |
| 场景6 | apply | 非0 | 2 | 2 | ch\_fee\_modify表(APPLYSTATUS=2或3) |
| 场景7 | apply | 非0 | 2 | 3 | ch\_fee\_modify表(所有记录) |

# 漏洞复现

```
GET /Shipping/FeeModifySource.aspx?handle=apply&applystate=1&checkstate=1&applytype=1&oplb=1&id=SQLI_POC&val=b9733091-e978-4cb5-a845-765a82ca1217 HTTP/1.1
Host: dongsheng.mrxn.net
```

![东胜物流软件 FeeModifySource.aspx SQL注入漏洞](https://image.mrxn.net/6635ba5969ac4949b74f432bfeda5ed0.webp)

成功延时 5 秒

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  asp.net](https://mrxn.net/tag/asp.net)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[东胜物流软件 FeeModifySource.aspx SQL注入漏洞](https://mrxn.net/jswz/dongsheng-Shipping-FeeModifySource-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/dongsheng-Shipping-FeeModifySource-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-Shipping-FeeModifySource-sqli.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-Shipping-FeeModifySource-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});