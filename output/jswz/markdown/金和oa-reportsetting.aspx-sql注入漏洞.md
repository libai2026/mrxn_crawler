---
title: "金和OA ReportSetting.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ReportSetting-sqli.html
asset_dir: assets/金和oa-reportsetting.aspx-sql注入漏洞
---

# 金和OA ReportSetting.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/28 13:31
* 312浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

软件

服务器

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ReportSetting.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ReportSetting.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.BIframe.dll` 将其进行反编译后找到 **ReportSetting** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitParam();
  Utility.RegisterTypeForAjax(typeof (ReportSetting), ((Control) this).Page);
  if (!this.IsPostBack)
  {
    this.InitControl();
    this.RptID = string.Empty;
    if (this.Request.QueryString["Reportid"] != null)
    {
      this.strAddFlag = "1";
      DataTable setinglist = this.cmd.getSetinglist($" and BIno='{this.Request.QueryString["Reportid"].ToString()}'");
      ((HtmlInputControl) this.txtName).Value = setinglist.Rows[0]["CNname"].ToString();
```

深入探索

数据库

防火墙软件

计算机安全

参数`Reportid`被带入`getSetinglist`方法

```
public DataTable getSetinglist(string condition)
{
  return this.db.ExecSQLReDataTable("select a.*,a.reporttype,b.typename from BI_ReportInfo a left join BI_ReportType b on a.typecode = b.typecode where a.delflag =0 " + condition);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.BIframe/ReportSetting.aspx/?Reportid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ReportSetting.aspx SQL注入漏洞](images/img-001-d9183359d1af.webp)](https://image.mrxn.net/a00e2f42d65041f6b6ea8cff5dcdf979.webp)

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
文章标题：[金和OA ReportSetting.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ReportSetting-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ReportSetting-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ReportSetting-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ReportSetting-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 