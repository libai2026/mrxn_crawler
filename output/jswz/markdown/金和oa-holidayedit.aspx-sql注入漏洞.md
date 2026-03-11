---
title: "金和OA HolidayEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-HolidayEdit-sqli.html
asset_dir: assets/金和oa-holidayedit.aspx-sql注入漏洞
---

# 金和OA HolidayEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/13 13:31
* 232浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

授权

编码转换工具

网页浏览器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `HolidayEdit.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `HolidayEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.FlowStat.dll` 将其进行反编译后找到 **HolidayEdit** 的处理逻辑

深入探索

文件大小转换

VPN服务

SQL注入检测工具

```
protected void Page_Load(object sender, EventArgs e)
{
  this.type = this.Request["type"];
  if (((Control) this).Page.IsPostBack)
    return;
  ((WebControl) this.save).Attributes.Add("onclick", "return CheckInput()");
  DateTime dateTime = DateTime.Now;
  int year = dateTime.Year;
  if (string.op_Equality(this.type, "new"))
  {
    for (int index = year - 3; index < year + 3; ++index)
      ((ListControl) this.drop_Year).Items.Add(new ListItem(index.ToString(), index.ToString()));
    HtmlInputText txtStartTime = this.txt_StartTime;
    dateTime = DateTime.Now;
    string shortDateString1 = dateTime.ToShortDateString();
    ((HtmlInputControl) txtStartTime).Value = shortDateString1;
    HtmlInputText txtEndTime = this.txt_endTime;
    dateTime = DateTime.Now;
    string shortDateString2 = dateTime.ToShortDateString();
    ((HtmlInputControl) txtEndTime).Value = shortDateString2;
    ((ListControl) this.drop_Year).Items.FindByValue(year.ToString()).Selected = true;
  }
  else
  {
    DataTable dataTable = stat.HolidaySearch(this.Request["id"]);
    for (int index = year - 20; index < year + 5; ++index)
```

深入探索

防火墙软件

安全工具开发

网络安全培训

当type不等于new时，参数id带入`HolidaySearch`方法

跟进`HolidaySearch`方法

```
public static DataTable HolidaySearch(string id)
{
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($" select * from HolidayData where hid='{id}' ");
}
```

参数`id`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.FlowStat/HolidayEdit.aspx/?id=SQLI_POC&type=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA HolidayEdit.aspx SQL注入漏洞](images/img-001-2835498300fc.webp)](https://image.mrxn.net/aa77fa9bb73a4be18e3bd7c07c58a947.webp)

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
文章标题：[金和OA HolidayEdit.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-HolidayEdit-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-HolidayEdit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-HolidayEdit-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-HolidayEdit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 