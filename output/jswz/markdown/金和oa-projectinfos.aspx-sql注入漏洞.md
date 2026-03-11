---
title: "金和OA ProjectInfos.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ProjectInfos-sqli.html
asset_dir: assets/金和oa-projectinfos.aspx-sql注入漏洞
---

# 金和OA ProjectInfos.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/13 13:15
* 317浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

数据库

漏洞扫描器

安全认证考试


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ProjectInfos.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ProjectInfos.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **ProjectInfos** 的处理逻辑

深入探索

云安全解决方案

安全

技术文章订阅

```
protected void Page_Load(object sender, EventArgs e)
{
  this.projid = this.Request["projid"];
  if (((Control) this).Page.IsPostBack)
    return;
  DataSet projectinfos = this.ch.GetProjectinfos(this.projid);
```

跟进`GetProjectinfos`方法

```
public DataSet GetProjectinfos(string projid)
{
  return this.db.ExecSQLReDataSet($"{$"{$"select top 1 * from vw_hyz_project where 项目主键={projid}; "}select distinct 自定义名称,自定义值 from vw_hyz_project where 项目主键={projid}; "}select distinct 项目成员 from vw_hyz_project where 项目主键={projid}; ");
}
```

至此，就非常明了了，参数`projid`被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/ProjectInfos.aspx/?projid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ProjectInfos.aspx SQL注入漏洞](images/img-001-6f9301c3c60c.webp)](https://image.mrxn.net/5d48e4c6c926441a9a11841d02b0d4ae.webp)

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
文章标题：[金和OA ProjectInfos.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ProjectInfos-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ProjectInfos-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ProjectInfos-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ProjectInfos-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 