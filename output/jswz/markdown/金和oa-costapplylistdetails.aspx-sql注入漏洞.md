---
title: "金和OA CostApplyListDetails.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CostApplyListDetails-sqli.html
asset_dir: assets/金和oa-costapplylistdetails.aspx-sql注入漏洞
---

# 金和OA CostApplyListDetails.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/12 13:22
* 299浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

软件

代码安全审计

文本剥离工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CostApplyListDetails.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

Web安全书籍

Docker加速服务

恶意软件分析工具

根据 `CostApplyListDetails.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CostApplyListDetails** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.KeyCtrl("JHCostControl");
  this.dataBind();
}
```

在`dataBind`方法里根据不同的`strGetType`值处理进入不同的处理

代码安全审计

[![金和OA CostApplyListDetails.aspx SQL注入漏洞](images/img-001-43c6a199710e.webp)](https://image.mrxn.net/901952f3de0d49b9a4cfb9e62e1b55c2.webp)

以**strGetType=Travel**为例，其处理逻辑如下

```
if (string.op_Equality(str1, "Travel"))
{
  DataTable travelApplyDetails = costHelper.GetTravelApplyDetails(RecordNo);
```

跟进`GetTravelApplyDetails`方法

```
public DataTable GetTravelApplyDetails(string RecordNo)
{
  return this.db.ExecSQLReDataTable($"Select Distinct Budget_TravelCostApply.AppID, RecordNo, AppDeptID, AppUserID, SubTime, YearPeriod, Period, EntityID, EntityObjectID, Budget_TravelCostApply.Remark, PositionID, SumMoney, AppFlag, DelFlag  from Budget_TravelCostApply left outer join Budget_TravelCostApplySub on Budget_TravelCostApplySub.AppID = Budget_TravelCostApply.AppID where RecordNo = '{RecordNo}'");
}
```

至此，就非常明了了，参数`RecordNo`被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

其他几个处理逻辑差不多如下图所示

漏洞修复方案

[![金和OA CostApplyListDetails.aspx SQL注入漏洞](images/img-002-b3c30117029a.webp)](https://image.mrxn.net/2455cc22a42248a8ba55f2fe89e89764.webp)

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/CostApplyListDetails.aspx/?RecordNo=SQLI_POC&strGetType=Travel HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA CostApplyListDetails.aspx SQL注入漏洞](images/img-003-939c32574a68.webp)](https://image.mrxn.net/7f353dfc5f4445198c9cb79284b7079b.webp)

成功延时 4 秒

编程

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
文章标题：[金和OA CostApplyListDetails.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-CostApplyListDetails-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-CostApplyListDetails-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CostApplyListDetails-sqli.html"),
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

安全研究工具


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CostApplyListDetails-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 