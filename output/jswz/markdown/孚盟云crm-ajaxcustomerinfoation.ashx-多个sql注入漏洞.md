---
title: "孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerInfoAtion-sqli.html
asset_dir: assets/孚盟云crm-ajaxcustomerinfoation.ashx-多个sql注入漏洞
---

# 孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/15 08:30
* 249浏览
* [0评论](#comment)
* 11分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxCustomerInfoAtion.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxCustomerInfoAtion.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxCustomerInfoAtion** 方法的实现如下

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-001-818348b3f3af.webp)](https://image.mrxn.net/37d69eefcca344ca909567631f98f7e7.webp)

当**method**=**getTitle**时，看下`getTitle`方法的实现

代码安全审计

```
private void getTitle(HttpContext context, string empID)
{
  string custid = context.Request["custid"].ToString();
  string FID = new CreatePageDao().GetDataSource($"select FID from bfCustomers where CustID='{custid}'").Rows[0][0].ToString();
```

参数**custid**未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

当**method=locationSave**时，一样的存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-002-84e3632077f6.webp)](https://image.mrxn.net/dbf4e788e0bb4c9c86aebbf2c6b965ef.webp)

method=frommail

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-003-443536942459.webp)](https://image.mrxn.net/ce29bc723de945ca904cffdebc7444e5.webp)

method=FocusedChecked

漏洞修复方案

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-004-95e1da0b8118.webp)](https://image.mrxn.net/4b626afe4a4b4ddbb3da19fedaf4cab8.webp)

method=GetContactEmail

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-005-a3f36074e1aa.webp)](https://image.mrxn.net/78ec151397704c8cbc976d7b483c48b0.webp)

method=SendMessage

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-006-748a6d77ab0d.webp)](https://image.mrxn.net/2cca2c966e054ddc99e13f416a0c1301.webp)

method=moreTrack

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-007-5801a614eb45.webp)](https://image.mrxn.net/f9613c63913346e895cc233f2cb5263b.webp)

method=uploadFileToOss

物流软件安全

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-008-04cc6239d12a.webp)](https://image.mrxn.net/6a7a3263d2d540b19fb01b188d678aed.webp)

method=UpCustomerPower

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-009-171341d03737.webp)](https://image.mrxn.net/f7266347e44d4eaeac42cebe7ef1f84c.webp)

method=DingTrack

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-010-29d4595fdf47.webp)](https://image.mrxn.net/290dca7041924f4bafc05952a19f5bab.webp)

method=CommentLoad

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-011-7cba3f31dcfe.webp)](https://image.mrxn.net/60c61762b7ad444d803fde9113442fc8.webp)

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-012-3c92d1cb8127.webp)](https://image.mrxn.net/3171900f81a349c488584ef59a6363bf.webp)

method=savePriceAttach

编程

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-013-5d83b7e35327.webp)](https://image.mrxn.net/7bd37378c0cc483599baea46ca587230.webp)

method=DelContact

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-014-87f9e4dec18f.webp)](https://image.mrxn.net/929344ecd0834102983b9e30cdc085d4.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxCustomerInfoAtion.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

method=getTitle&custid='SQLI_POC--
```

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-015-5ffbae7d698c.webp)](https://image.mrxn.net/19c3c3bc84964a558c7750fedf8ac5f2.webp)

通过报错注入在响应里回显数据库版本信息

漏洞修复方案

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
文章标题：[孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerInfoAtion-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerInfoAtion-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerInfoAtion-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerInfoAtion-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 