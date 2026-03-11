---
title: "金和OA GetSubjectTreeData.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GetSubjectTreeData-sqli.html
asset_dir: assets/金和oa-getsubjecttreedata.aspx-sql注入漏洞
---

# 金和OA GetSubjectTreeData.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/30 13:05
* 219浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

软件

数据库

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetSubjectTreeData.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GetSubjectTreeData.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **GetSubjectTreeData** 的处理逻辑

深入探索

服务器

网络安全会议

编程语言教程

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  if (this.Request["id"] != null)
    this.loadDeptChild(this.Request["id"].ToString());
```

跟进`loadDeptChild`方法

```
public void loadDeptChild(string deptID)
{
  DataTable table = this.biz.GetList($" ParentID='{deptID}' and  DelFlag=0 ").Tables[0];
```

参数`ID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/subClass/GetSubjectTreeData.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GetSubjectTreeData.aspx SQL注入漏洞](images/img-001-e0e256d0d20d.webp)](https://image.mrxn.net/420886cd1dcd44a9be8a1ac45de4fa7b.webp)

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
文章标题：[金和OA GetSubjectTreeData.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-GetSubjectTreeData-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-GetSubjectTreeData-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GetSubjectTreeData-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-GetSubjectTreeData-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 