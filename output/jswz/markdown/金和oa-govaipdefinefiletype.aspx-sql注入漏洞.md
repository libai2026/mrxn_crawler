---
title: "金和OA GovAIPDefineFileType.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GovAIPDefineFileType-sqli.html
asset_dir: assets/金和oa-govaipdefinefiletype.aspx-sql注入漏洞
---

# 金和OA GovAIPDefineFileType.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/16 13:31
* 221浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

SQL注入防护

漏洞扫描服务

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GovAIPDefineFileType.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GovAIPDefineFileType.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.govsetaip.dll` 将其进行反编译后找到 **GovAIPDefineFileType** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (((Control) this).Page.IsPostBack)
    return;
  this.initPage();
  string strId = this.Request["intId"].ToString();
  if (!string.op_Inequality(strId, ""))
    return;
  DataTable searchFileType = new GovType().getSearchFileType(strId);
```

跟进`getSearchFileType`方法

```
public DataTable getSearchFileType(string strId)
{
  string str = $"declare @strFileType varchar(50)  select @strFileType=sysFile_Type from govpaperaip where sysF_ID='{strId}'" + " if(@strFileType='IOA_Send')" + " select TypeID,TypeName from sendType where DelFlag=0 " + " if(@strFileType='IOA_Accept')" + " select TypeID,TypeName from AcceptType where DelFlag=0" + " if(@strFileType='IOA_Ask')" + " select TypeID,TypeName from AskType where DelFlag=0";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

参数`intId`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.govsetaip/GovAIPDefineFileType.aspx/?intId=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

网络安全会议

防火墙软件

编程语言教程

[![金和OA GovAIPDefineFileType.aspx SQL注入漏洞](images/img-001-7b8b526c7a67.webp)](https://image.mrxn.net/6fac9cd80ceb4620ae65eb64d062763c.webp)

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
文章标题：[金和OA GovAIPDefineFileType.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-GovAIPDefineFileType-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-GovAIPDefineFileType-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GovAIPDefineFileType-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALJUlEQVR4AeybgXbrNgxDe/f//7wVRiHTsuQkfVmSnamnLEgQpFTRStPu7a+vr6+/f2t//3yM6n9SrXcfq6bnEj+C6tNb6sMnrphcjyNN5apfa8NX7je+BvJdtz4/5QTaQL4n/HWv/cnm6xrpEy7xFQJfwFDS9+ljYKsFhvX3ksDWJ/2Ffa24e63WtoFUcvnvO4HTQMDThzPOtpknoebB9eHgGIevCHMNHHNwjEd9YK6pevmj72HESfuIgfcAZxz1OQ1kJFrc607gKQMBTz9PlHD2LYC1sGO0qpOBc+GF4quJk1UOznXSwJlPnfIzg3Nd1YLzQKX/yH/KQP5oB6v4cAJPHQiwvfsA2iJXT2JyQKsDWm11gKEGdr7q5ae/fFlioeJqsPcB+9LJwDEYa92z/acO5Nmb+z/2+3cG8n88ySd9z6eB6IrO7Blr1t7pFy7xCHtN4hGO6nsOxi8/tV9fU3O932sT97oaR1PxNJCaXP7rT6ANBPzEwG2cbfPW9Ps68Fo9nz7gPNBLWgy0H/aNfMDJWqMScO9owHG04BgI1RBo+4JrvxV9O20g3/76/IAT+CvT/w1m/6lN/CxMX+Gsp3KxmWbE9zV9fE/NlSb9HsV1Q0an+kZuOhDw695obzDPRZ8nA25rU3OFcOwDjuGM6QPO9XsBImkIbK/5jfh2+rpv6u5PcD84Y5rAOTcdSIoWvvYE/oLjlLJ8no7EQrA2OXAMRmlicORGNT2XOD2ucKQNF+zrwwthvL++5ipWn9iV7pHcf+mGPPJ9/We1ayAfNrrTQMBXGc6YvYNziX97bcF9Ug+OwZj+IwRrUiuMDpxLPELpZaNcOHAf6WTgGOaY2isE16unrGpPA6nJ5b/+BE4D0cRko62IH9lI23NwfCrUJxpwLrFyssQjVF4GrgWaTHy1JIDtrS0QqsXAyU+PiGex+GjAfRKPUHrZKHcayEi0uNedQBuIJiaD2xMGa2CO93wLWq/aVU3VyQevXWvgzNX8oz64HxhTr/VlYB5o/6YtmhGqRtbnxMXaQHrRit9zAu2Pi1k+kwqGr9jnEt+DtQ/4CQuXejAPO0YTjDbxCMH1V7n0uQfh2K/WgHPhsmZiIVgDxmjAMfC1bsjXZ32sgXzWPG7fEF21WPYOvmJ9DOZhjqmpCEd9zcUHaxIHszdhODhq4RhHN0KwFmhpYHtLrDVk4LgJigPHHDgGisoucOir3uuG+Gw+5mv7a292BJ4azFGTfNRG/dMjuVksPpognPeXnPTVRnw4cJ/EFWGcS++qHXHKh79C8DrA7Zesr/Xx0hM4vWRlkqNdJAeeaDRwjMXDkUutcjODY03VpR6sSTxCsKbW937qwoNrwguT6xGs7XnFqpPJ7w3GddLHTgPpm6z4tSfQfjGE4/QysdF2rnLR36OB45qpDYLzsGOfSywE6+5ZW3pZtEFwD9j/HJKc9LcMXH9VA9aAsfZcN6Sexgf4bSCZKHhqYAwvzH7BOTDOeHAeiGSI6l1tKPoho/sJt/fxwIazXHiwDkj5Vgc0jFbYRD8OWPcTDkF1MjhrxVdLA7AWWO+yvv6dj193bTfk1x1W4VNPYDqQXK26Gvhq9bnEFWudfHCt/N5gnKv94qc2ccXk4Ha/aFOfGFwLOyZ3hWD9labP9WsrPx2IkstefwKnP51kauCJw47ZHpibxeLTR74scUXxI4sGvA7QZED7AQxjv4l/HLDuJzwAOJc1a3LE1Ty4Fmg0sO0vBDiGHftcYuG6ITqFD7KHfjHME9Pjb7+fvg/4KUq/mod5rurk9/WJRyi9DI79pYUjJ101aWKVr37ywvDyZ7ZuyOxk3sS3gfTTg+PTUfcH81x0cFsTbY/gWtix319qYNeEezbCvgZw2R44/Ay5Eo++pzaQq8KVe90JrIG87qzvWqm97QVfNTDqOslGXcTLRrlwyssSg/smrgjOSS+ruVu+9LFeC+4bHhwDoU6YXsIk5csSX6F0spEGGL6cSR9bN2R0cm/k2kAyoewFztMEc3DE1Iyw71s14D6Vm/lw1IJjOGN6ZO0RwrEuNb9FOPYDx4/2awN5tHDp/50TaL8YPtI+T1xq+lg8+AkB40jTc2Ct6meWmitMLbgfnDGaYPrBru25aIPJC8NdoXQy2NeAo79uyNUJviE3HYgmOTPwVLNfcAw79rXRjjDaUS7cTAP7mjPtqDZcENwnsXDWLzy4BgjV/rcE1cta4tsBtndZ4mXf1PYpPzYdyKZcX15+Au33kH5l8DR7XnGmKV/Wx+J6g3k/GOfSVwhjTb+OYrBWdTJxMvkxsAaMysvAMewo/l4D10Wf9Sr2OXANsP6b+teHfbzhJevDTuDDttMGAr42/f7APNBSwPbDqREXDlibKwuOgYuqcyr1yQCnPYC5e7TRXOHVWsn1mH7gvcCOvRacq3wbSCWX/74TOA0kE86WEgtH3IyH8/RVL30MrjXS37L0Es60yslqHsZrg3mgyVVbrSWKkzyw3dzEFcE5MKa8ak4DiWjhe06g/ekkU8o2+ji8EDxhOKJysVk97DXRBmc1yoPr5MuutMqPDNwD9n9IHR04l77C5O5BcH2vBfNwXjNa2DXrhuRUPgTbQGCfEoz97FlPjyxxEPa6cNLJ+lhcb9FcIexrAAdp+gHb6/gh+R0kL/wOD5/iZJVULINxv5G2cjNfPatVXRtIJZf/vhNYA3nf2Q9XPg0kV2mkBl9dMEaTmopw1ERbEW5rqr76WSucEK77gfOwo+pksHNgX7ysXwuOeWlmllohHOvAsXKx00BmjRf/mhOY/rU3E6vbCBesud6PBvwU9Pkaw1gD5oEmf6RvK/pxUlsR2N4AhPuRHgCsOZBdANakDziusuQqJx+sBdZfe78+7GP6i+HVPsET7TVgHmipPBXA9iTCjk3UOWBNaoWdpIVgLZx/8YI9B7QaOcC2H/WWiesNjhpwHJ3qeoOjJtqKYE1qa279DKmn8QF+Gwh4anDE0R4z2SC4ZqTtudQIk5MvSxwE9wVCbU817HFLfDvAlv92t0/1rLaRky9wrJUstXDOKQ/mAYWbpWYLvr8A255gx16TWNgG8l27Pj/gBNq7LE2n2tXeYJ82MJQC25ORZHonrgj3a2vdM/3R/uC4r6x3pYVxTWpHCK4B1rusrw/7WC9ZlwN5fbK97e2XzrWsGE3l5IevKF4WDvZrCfaVl8004YXSyeTL5M9MeRl4HfkycAwo3AzYXlrBuJHdl6zT0Ycwmh6rKLnK9f66If2JvDluP9TBTwjcj9n7aPJw7BNNRbAmXPqNEKztc2Ae6FOXcdYMXomB7RZdaZKD21o4arIH4bohOckPwTYQTedeu2fv6RUt+KmAHXtNH6f2ClMj7HXiZOA1ax7MgVG63qr+Xj89rvTRgNeGHdtArhqs3OtO4DQQ2KcFR/+RbYFrU5OnomJyYC0Yw4+0yYG1cMZoerzq12tHcerBa1YNmIMjjjTh0q/iaSARL3zPCayBvOfcp6s+ZSDga1pXqddQfnJgLeyYnHTV4Lam6nsfXB8+6whHnPiRPaLt61MrTO4KnzKQqwVW7rETeMpANH1ZXRr8dIYDx9LFkguCNWAM/yiC67MOOK59wFyvAfOw/xdIMFfrZ376JQ+uhXk/2DVPGUgWX/jnJ3AaSCY8wlvLjWrA00/uVo+aT40wPLgfnDGaP0GtFUufPg5fsdf0sbTgPfe5xMLTQFS47H0n0AYCnh7cxtl24VyrqctSA7tG/JXBrk19rw8vBOujAcfK3WvgGthxVpt1hLDrYfdnteLBOvmxNpAQC997Amsg7z3/0+r/AAAA///E1D9nAAAABklEQVQDAIgChaQKRCorAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GovAIPDefineFileType-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 