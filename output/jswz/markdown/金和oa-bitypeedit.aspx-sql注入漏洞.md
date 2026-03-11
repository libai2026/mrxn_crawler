---
title: "金和OA BITypeEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BITypeEdit-sqli.html
asset_dir: assets/金和oa-bitypeedit.aspx-sql注入漏洞
---

# 金和OA BITypeEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/26 13:30
* 439浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

SQL

数据库

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BITypeEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BITypeEdit.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.BIframe.dll` 将其进行反编译后找到 **BITypeEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.mod = new commonMethod();
  this.type = this.Request.QueryString["type"].ToString();
  if (string.op_Equality(this.type, "edit"))
    this.strTitle = "修改报表类型";
  if (((Control) this).Page.IsPostBack || !string.op_Equality(this.type, "edit"))
    return;
  ((HtmlInputControl) this.txt_Name).Value = this.mod.GetTypeNameByCode(this.Request.QueryString["id"].ToString());
}
```

当`type=edit`时，参数`id`被带入`GetTypeNameByCode`方法

```
public string GetTypeNameByCode(string typeCode)
{
  string empty = string.Empty;
  DataTable tableDate = this.GetTableDate($"select typename from BI_ReportType where typecode='{typeCode}'");
  if (tableDate != null && ((InternalDataCollectionBase) tableDate.Rows).Count > 0)
    empty = tableDate.Rows[0][0].ToString();
  return empty;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

深入探索

网络安全会议

安全工具开发

安全认证考试

```
GET /c6/Jhsoft.Web.BIframe/BITypeEdit.aspx/?type=edit&id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA BITypeEdit.aspx SQL注入漏洞](images/img-001-bbcdc7f421f5.webp)](https://image.mrxn.net/87d7a800743e469e80ce6c0334515f7e.webp)

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
文章标题：[金和OA BITypeEdit.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-BITypeEdit-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-BITypeEdit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-BITypeEdit-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKS0lEQVR4AeycgXbbuA5Ec/f//3mfR+gIsAjRchvHflvuCTLgzABUCDFN2nP2n6+vr3//NP698N+jPboWrum0jvtdv+sqdv1nXK39k1wDudWvj085gX0gt+l/PRPdFwB8AZ10x3X73Bl+Lez7tWwB2PYEpnonun+H1Q/se0DkVT/mXb8ZV+v3gVRy5e87gWEgEG8A9Dh7VL8FM88jDXJfeyE4r4Uwct3+Rw6iDlCbLYD9BmzE7ROMnHsJb5aHH5A9YMy7BsNAOtPifu4E1kB+7qwv7fSSgUBez9lTQPog8qt++/Ttw2EOoheMaK8QQlfugODcS3jUANEviZcM5CVP+pc0fclA/EYJfY7KHcD2h6i1M4Twua5iVwPnftfO6oD9R//O5x7CTv8O7iUD+fqOJ/tLe6yBfNjgh4HoOs5i9vwQ3zJgxFrn/h1nrSJEv+p3DqFBfruB5OwzQmp1D+f2eS00B1kLkVvrULWz6GqGgXSmxf3cCewDgZg4XMPZI9a3ovNB7FF9EFz1Q3D2Qawhb0P1z3KIWvcSQnC1Ds451ThqzTGH6AHXsNbvA6nkyt93Amsg7zv7dud/fAX/BNvOv0j3/bXcoOM24eQTxNWvMgTnXsKqO4fwed0hhAfyWyEk5xpITvsprCn/jlg3xCf6IXhpIJBvBpznfkPq1waj3zqk5lpIzj5rFa1VhKit3DGH8EDehkd9q+4coo/7Q6wh0doZQnirfmkgteCN+V+x9TAQiKlBot+KM/RJQdR4LexqYPTJewzXwug/apBv/LFPXbtOaB6iPyRaO0PVK8508ZD9IHLxDtUrIDTgaxjI1/rvrSewBvLW4x83/wfiuoxSMhAeYCeB7a/QIb9V6PopIDUYc3kUe7OTBKLWMsQaEq0JIXj1dohXeA3hAUT/dgDb1+8G7i/sOPEKa2e4bsjZybyJ338x9P6a4iwg3ozqca2xal3e+WactYruWznnEM8IeXutdeheFTsfZF/rkBxEbq0ijBoEV/ddN6Se2gfkayAfMIT6CPsf6hDXB+bo6wWjrzZ+Re69hRD7P9oHwgeBqnVAcDBi19d1QuvKj2Gtoj2Vcw65/7ohPpUPwekf6n5GT1cIMU3lx7AfwgOJ1irCqENy7u8aONfkOfrFOa5o9hzRPWC+v31GSH/HHffRet0Qn9SH4BrIhwzCj7EPRNdFYaEizK+evRA+9XFYqwijD865WuscRr81713RGkQd5O8okFzng9CtVYTQINH7Vp9za0JzkLX7QCwufO8J7D/2+jEgp2WuQ03YAVFjH8Qa8i209gy6v2u8FpqD3MvcDFXr6HwQ/arW+SF81irCqNV+zmH0rRvi0/kQXAP5kEH4MaYDqdfQuQshrhuM35bsFdpfUbwCxh6QnGvkVcCo2VMR0geRW4dYQ6J6H8N+IYS3esQ/ExA9ao37VW46kGpc+VMn8NvmYSCemhBiqpAo/hje3TykHyK3RwjXOHkVMPrFK7ynUOtjiFcc+bqG6A+JVe9y9VRA1kDk9kOsAVN3CGz/yAWJw0DuKtbix09g/7ssyClB5HoDjgGhwTnWGn9FkH5zjxCixr6urzUh3Ps77lGPqjtXn7OYeawJu3rxiqqtG1JP4wPyNZAPGEJ9hH0gujqKKs5yeR32eQ3xrQPyR2JrQvs7lH6MzneVcy/IZ4LIrdVeEFrlrvjsEdbaZ/N9IM8WLv9rTmD4u6xH2+gNUEC8ScBeAmw/xu1ESSA06G+NeipKydYLqNSey6vYiZKIdxR6S80LgW0P5Y7NdPIJwg/sDmDrsRO3pOtlDsIPidaE64bcDvCTPtZAPmkat2fZfw+55duHro0D8lrBfW5Pxa3BhU9w3wv69YVWrQWynw1+Tkit4+yvCFFjf0X7IDwwx1rrHLJm3RCf6IfgdCCeYIeQU4XIO1/3ddpXtaucayD29LqiewnNQ/jFOaw9ws4P9/1qD/s7rL4unw6kK1jca09gDeS15/t09/33EIgrWDtAcDBidx0hfLWH8+qHc5/9Qjj3uR+EB1DJEMDd7wkQa0h0r4qQupvCyFnrENIPkXe+yq0bUk/jA/L9x16/HVefCWLiwFACbG8lJFbTbC9rHUL2g8gf+ax7f68rWnuEXQ2MzwEj59puD2vCdUO6E3ojtw8EYqr1WTSxY1ivPEStOXuEHQf3fnnkVUBokCj+SkDUqJ/Ddce1eSFEHaDlFvYLN+Lkk3RFJwP7dwrrMOf2gbjg9bh2mJ3AGsjsdN6g7T/2em+YXyldTwWkT2uFe1SE9EHkVXcOoamPw1qHncccRC9gLwX2bx8Q+S6WBM61Ypumfo6KLqgcjHutG+KT+hDcf+z18zyaYOczN8Pat/NZh3hrIP8hy357hOaeRdU6IPbyuiKEBj16XwjdayEEByNKd3g/r4XrhugUPijWQD5oGHqUYSCQ18xXqqKKFJA+rRUQnHKHa70WdhyMtTByqlfAqEFw7i+U9yykKyDqgNYqz1m4ANh/aDDX1Vg7w2EgZ8bF/8wJDD/21qn6EWA+fftc6/UZQvSr+qwWwg+JtXaWQ9TYA7EGTO3/A349A7C96bt4SyA4GFE1x7iVbB+Q/o04+VTr/zM35ORr/b+j10A+bGT77yG+NpDXDCLvnhlCg8SrPu/V+Stnn7FqXW4f5DOZ67DrMeNqD/sg9vL6DCF8kGgvJLduiE/lQ/DpgUBMs74tziG0+rVZqxyEDxKr7hxC99q9hOYeIdz3gFhDYu2h3orKdbk8ik6bcapxdL6nB9I1Wdz3ncAayPed5bd02n8PgbjCvk6PEMIPic8+Ud3DtR1nDXIv+6wJIXTlx4DQXCe0B0KDRGtCeRWQOkQuXQGxBrS8FMDwO8+6IZeO7udMw4+9V7fWG3MM11beXIcQbwjQyTsHbG9S7QvBQaL1vfCWdNyNfvjhOuHMLP0sap09MH/edUPqqQ35zxPDnyGQE4Rr+bOP7belIsRes14QHsh/vKo9ZrXWYOxhTeh+kD7xjwKu+d1f2PVcN6Q7lTdyayBvPPxu630gukLPRNes4yCucqdVzntXbpZD9IURax2E7v4V7aschN+aEEZOfI3ao/LOYewBwdXafSAuXPjeExgGAjE16PF3H7e+BTD2dl9IrdYot0eotUL5lYDsC/d5rVfPY1T9mMN9L8h19bpn5ZxD1gwDsWnhe05gDeQ9536667cOpLuW5iCvpZ/GmhBCV+6A4Ox/hK6rOKuxD2If6NG+iu5bOeedZg5yD3MVv3UgtfHKz09gprxkIJBvAUReH8JvEoQG+Zt39TmH8LlOCMHZc4bynkVXY2+nQewJ+bwQXPXPelgT1hrnLxmImy98/gTWQJ4/s5dWDAPRVZrFlafp6msdjNe86ldy79F5IfoDnTxw7iUcxEJIdwDbPwkUeU9h1GDk9oKSDAMp2krfcAL7QCAmCNdw9qyQPWY+v21C+2Csla6Ac026e1SErIHHea095pD11rSvAkYNRs51FVXv2AdSDSt/3wmsgbzv7Nud/wcAAP//4dWcHgAAAAZJREFUAwDlfny5OJui7AAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-BITypeEdit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 