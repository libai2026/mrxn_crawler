---
title: "金和OA LoginModeAdvanced.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LoginModeAdvanced-sqli.html
asset_dir: assets/金和oa-loginmodeadvanced.aspx-sql注入漏洞
---

# 金和OA LoginModeAdvanced.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/16 08:28
* 577浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

服务器

SQL

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LoginModeAdvanced.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LoginModeAdvanced.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 `LoginModeAdvanced` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.PageInit();

  if (this.Request.QueryString["ID"] != null)
  {
    this.strLoginID = this.Request.QueryString["ID"].ToString();
    this.GetLoginInfoByID(this.strLoginID);
  }
```

深入探索

安全工具开发

安全认证考试

安全研究报告

当 `ID` 参数存在且**不等于 null** 时，执行 `this.GetLoginInfoByID();`

```
private void GetLoginInfoByID(string loginID)
{
  DataTable wfLoginById = new WFLogin().GetWFLoginByID(loginID);
```

继续跟进`GetWFLoginByID`方法

```
public DataTable GetWFLoginByID(string loginID)
{
  return this.dbOperator.ExecSQLReDataTable("select * From WFLogin where ID = " + loginID);
}
```

至此，就非常明了了，参数 `ID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/LoginModeAdvanced.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LoginModeAdvanced.aspx SQL注入漏洞](images/img-001-78ae52f28191.webp)](https://image.mrxn.net/b2c9d3cddd6d49fb894bebc4a63e6558.webp)

成功延时 5 秒

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
文章标题：[金和OA LoginModeAdvanced.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-LoginModeAdvanced-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-LoginModeAdvanced-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LoginModeAdvanced-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-LoginModeAdvanced-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 