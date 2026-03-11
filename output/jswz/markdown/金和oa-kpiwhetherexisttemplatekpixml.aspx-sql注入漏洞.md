---
title: "金和OA KpiWhetherExistTemplateKpiXml.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-KpiWhetherExistTemplateKpiXml-sqli.html
asset_dir: assets/金和oa-kpiwhetherexisttemplatekpixml.aspx-sql注入漏洞
---

# 金和OA KpiWhetherExistTemplateKpiXml.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/29 13:30
* 531浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

安全工具开发

Docker加速服务

文件大小转换


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `KpiWhetherExistTemplateKpiXml.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

授权

Web安全书籍

数据库

根据 `KpiWhetherExistTemplateKpiXml.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **KpiWhetherExistTemplateKpiXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  StreamReader streamReader = new StreamReader(this.Request.InputStream);
  if (this.Request["SelectValue"] == null)
    return;
  this.strSelectValue = this.Request["SelectValue"].ToString().Trim();
  this.Response.Write((object) this.m_AppraiseKip.GetTemplateKpiCount(this.strSelectValue));
  this.Response.End();
}
```

参数 `SelectValue` 被带入`GetTemplateKpiCount`方法

```
public int GetTemplateKpiCount(string SelectValueKpiID)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  string str = $"Select count(*) AS TemplateKpiCount  From  TemplateKPI where TemplateKPI in (select KPICode From KPI Where DelFlag=0 AND KPIID in ({SelectValueKpiID})) ";
  int templateKpiCount = 0;
  DataTable dataTable1 = new DataTable();
  DataTable dataTable2 = dbOperator.ExecSQLReDataTable(str);
```

至此，就非常明了了，`SelectValue` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

深入探索

网络安全课程

VPN服务

云安全解决方案

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/KpiWhetherExistTemplateKpiXml.aspx/?SelectValue=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA KpiWhetherExistTemplateKpiXml.aspx SQL注入漏洞](images/img-001-e5dcb93eb83a.webp)](https://image.mrxn.net/85f43a75541e481da2a3dcaab13923b1.webp)

成功延时 5 秒

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
文章标题：[金和OA KpiWhetherExistTemplateKpiXml.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-KpiWhetherExistTemplateKpiXml-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-KpiWhetherExistTemplateKpiXml-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-KpiWhetherExistTemplateKpiXml-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-KpiWhetherExistTemplateKpiXml-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 