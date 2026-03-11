---
title: "金和OA SubjectHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-SubjectHandler-sqli.html
asset_dir: assets/金和oa-subjecthandler.ashx-sql注入漏洞
---

# 金和OA SubjectHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/31 13:20
* 258浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

数据库

软件

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SubjectHandler.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

漏洞扫描器

物流软件安全

SQL注入检测工具

根据 `SubjectHandler.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **SubjectHandler** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  string str = string.Empty;
  if (!string.IsNullOrEmpty(this.Action))
  {
    string action;
    str = (action = this.Action) == null || !string.op_Equality(action, "updateactive") ? "{\"result\":false}" : str + this.UpdateActive();
  }
  context.Response.ContentType = "application/json";
  context.Response.Write(str);
  context.Response.Expires = 0;
  context.Response.Buffer = true;
  context.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  context.Response.AddHeader("pragma", "no-cache");
  context.Response.CacheControl = "no-cache";
}

private string UpdateActive()
{
  string empty = string.Empty;
  return this.Budget_Subject.UpdateActive(this.SubjectCode, this.IsActive) <= 0 ? "{\"result\":false}" : "{\"result\":true}";
}
```

深入探索

Windows安全工具

授权

安全

当 `Action=updateactive` 时，**SubjectCode**、**IsActive** 被带入`UpdateActive`方法

```
public int UpdateActive(string subjectCode, int IsActive)
{
  StringBuilder stringBuilder = new StringBuilder();
  if (IsActive == 0)
  {
    stringBuilder.Append("update Budget_Subject set IsActive=" + (object) IsActive);
    stringBuilder.Append($" where SubjectCode='{subjectCode}' or ParentID='{subjectCode}'");
    return this.dblib.ExecSQLReInt(stringBuilder.ToString());
  }
  stringBuilder.Append("update Budget_Subject set IsActive=" + (object) IsActive);
  stringBuilder.Append($" where SubjectCode='{subjectCode}'");
  return this.dblib.ExecSQLReInt(stringBuilder.ToString());
}
```

深入探索

恶意软件分析工具

VPN服务

网络安全课程

参数`subjectCode`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/subClass/Handlers/SubjectHandler.ashx?SubjectCode=SQLI_POC&Action=updateactive HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA SubjectHandler.ashx SQL注入漏洞](images/img-001-7e3958c1224b.webp)](https://image.mrxn.net/0de29e53786641d89a36600ef279e94d.webp)

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
文章标题：[金和OA SubjectHandler.ashx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-SubjectHandler-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-SubjectHandler-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-SubjectHandler-sqli.html"),
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

漏洞预警服务

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKNUlEQVR4Aeybi3YjOQ5Dc+f//3nWMAOJllhyOUk7tdPqEzYoAGQpYqnzmN1/Pj4+/v1u/Dv8yf0sZa7Kz/jsOcKq74o76iN+VZc1eRWZ+06ugdzq98dVTqAN5Dblj1fi1U+g6l31yD7r5rzOCHxAhH0rzLWv5lXfqkflW3G5RxtIJnf+eycwDQTibYMaX90qRJ+qLr811iH8gKl2A4CWNzElEHqiWgqhPXsmzD7XQGhA67tKgLZfmPOqdhpIZdrc+05gD+R9Z33qSX9kIL7iQu8C1lcWQleNw7VeZ4TZb911GSsNosdZn3sIc81P5n9kID+5wb+t148OBM69cXrDFBB+oJ070L4QmoTOQeSqV9gjhNCUOyA4CDT/Cuo5CogewCvlL3l/dCDtyTv58gnsgXz56P5M4TQQXc1VrLbhOqD9swORWxPCzLmvdIc5o3khRA9rGSE0oP32wTp0zZz6OSB0a0KYOfHPwj2PsKqfBlKZNve+E2gDgXgL4BxWW4SozW9E5XuVcz+I/tDffJi5VX/3Eq58laYaB8RzKx+EBucw92gDyeTOf+8E9kB+7+zLJ//jK/gdLDsvSD8L+pVecW5ljxCi1lpG6Q549EGsof+zl2udQ/etOGt+3ndx3xCf6EVwGgj0NwMir/YKoUHHyuc3Bta+qnbkYN0Dug6Rjz28H+GoPVurZgyI50BH94GZs3aE00COjBfg/4ot/AMxxeqz9dsA4QGazZqwkZ8J0H4w/KTaD2jZr9wBUeO1EIKDQHFjuH/G0aO1dYhegKmnqHoF0D4viLwqhuca0EqB1nffkHYs10j2QK4xh7aLLw8E+jVr3T4TXW/HJ9WuJGDqKXemR2t2S+wHWu8bffgB4csG98icc2sZrWXMuvOsO4d4vj3CLw/ETTf+7AlMA9GUHH6U10KYpyo+B4QHcIuHL+rA/Q1u4i1x/S2dPioNooc14VR4IyB8t/T+Id8YEB7g7tFf2aP1GMD9c8g+5xDaWKO1PUKtx5gGMhr2+r0nsAfy3vN++rRpIBDXDVgWA/crCzNWhdB9K11X2WEfRK35jPYcYfYqh+gFtBLxDmD6vGyErtlv7RlCr4XIq5ppIJXpP81d7JNrv+31vjx5IRxPUrpjrPVaCOd6uBeEHzpaU79VQNRkD8ycdZg1PysjzD73MEJ4YP1bZPszQq/dNySfzAXyPZALDCFv4dQvF3OBrzL0a2YdgvM6o+syQviBZs26SWD6QgszZ3/u4RzCb4/QmvIxIPzAKN3XwH1P98XwF4QGHW3xM4XmMu4bkk/jAnkbCPRpwvNcE3aMn4d5oTXoPc1Jd5iD7rNmtEdoLqN4BfQeWivsUz4GHPtVZ79yh7kKK89Zrg2kary595/AHsj7z3z5xOnnkKU7iTBfc8twrMkDoStfBYQPAn3thRDcqv6spn4OOO4LoQFTa9cLJ/EJoRrHviFPDuuL8pfLpoF4UkJ3Vb6Kla/SzGUE7t9G5udk/SiHqIP+E/JP9IBzfSF8eX8Q3LN9QPhy7TSQLO78/Sdw6gdDiEkCbYfA/Y0GGrdKgOb3mwPnuFXfSoPe1zoE52cLrWWE8GWuylWfI3vMQ/SCjpUvc/uG5NO4QL4HcoEh5C20b3ura5aNziGun/0ZITTomHXn7uW10FxGiD6ZG3PVOiD8XgshuLFOawhNPod4hddCrceAqIVjVK3D9TD7rQn3DdEpXCimgXiiQohp5v2KV0Bo0DH7VjlETfbAzOk5ObLfPEQd9G97Yebsr3o84yD6PfNZ97Mg6gBLJQLtG55pIGXFJt92Ansgbzvqcw9qA4F+bSByX73cCh41ebKuXJwDwg8d5RnD/owQNfZCrKGjNSEEn3uIPwoIf9Zh5qxDaNDRz7LnCO3LWHnbQCpxc+8/gTaQPDnn1XaswfyWVNqqR6VVHMSzKu0sB9EDOnq/uceKs5bRtc846M+FyKvaNhCLG3/3BPZAfvf8p6e3gUBcI+hod76OEHrF2Z/RvsxB9IAZs2/M3Us4alqLV0DvK/4ooPsg8iPvyEP4IXDUtYbQoP+MpP055FFA97WBSNjx+ycw/frd0xNCnxxE7i1DrKFPH4KzJ6P6rcJeiB7Q+6603NO+CrPPeeUzB30fFeceRnsyWhOah95X/Bj7hvikLoJtIJ4U9Al6j9aEZzh7hND7wXGu3grVOCD8Xkt3mIPwQEdrQug8POZjL/mrgKjLGgQHM2afcwif10IIDjq2gcjwnthPWZ3AHsjqdH5Ba/+Bys/2Nc4I/UrZB52DyK3l2hVnTQiPPcS5j3IFhAc62iOU51nI57DXayFEb2tC8QrlY4gfwx6IXoCph//zayNTsm9IOowrpMuBAPf/cJI3Or4NeW0fRB30b12hc/bl2iq3r0L7s2YuY9bHHGJPI6/1O3rkZzhfDkQb2/HeE9gDee95P33a9JM6xDWG/s9N1QW6zzoE5/UR+npC+GGNR31GHqLPyGtdPXPFqcYBx33tqRCiDqjk+5cD4AH3DSmP6vfI9m0vxKTObsVvl3CsEeeA6Ou1EIIb68a1vArzyh3mKoToD0yy64XA/e1U7pgKboS1jDf68APmvq6F0ICy/j9zQ8rP7v+Q3AO52NDaF3Vfqbw/YLrSEBzMWPVwP+h+c/YfoX3fQff+To+qduwL/fMbNdVD6Mod9mXcN8SncxFsX9S9nzwt59aE5iqUroB4GwAtp3AtcL+BUKMLK7+1Cu0XVvrIQf18CH7057WeocgcRB10zLpzCN1r4b4hOoULxR7IhYahrbSBQFwf+D6qsUPXWeG1EOIZyseQ1wHHPtdBeKD+zQJ0HR5zP8e9jhAe62BeH9W+yreBvFq4/X/mBNpA/LZ8B73F3MNcRusVB/3tq3yugfDZIxw1qG+NfUbVOr7DuYfRvYTmMopXQHwuwEcbyMf+U5zA+6n2gyH0KcFr+avbhuif3xYILveCRy77nUN4oKM1Ye6nXJxD6zGswdxv9OY1dH/mz+R+pnDfkDMn9kbPHsgbD/vMo9pAdF1eiaq567MGcZWtZYTQYP3FF8KX+1a5e0P4gcp2inMvIXD/jcKqUD7Hype1yt8Gko07/70TmAYC8TZAjV/dKsz9/IYI3Vf5UcDrPdz3TyHMe4LgqmdCaECTgfsNBPa3vR8X+zPdkIvt76/bzo8OBOLqVadY/TNU+TIHx/3sg/BAjfb5+V5nhLk266vcfSvMdRDPyD4ILvt+dCC58c6PT2ClXG4gEG8NsNp3+x8tL003Ebh/wbyl0weElt9a59l8lnMNzH2tZaz6Xm4gecN/Y74HcrGpTwPxNTrC1f5dA3FlgZX9/k8J8IDukdFNKs6a0LryMeDxOcBoua+B+37ui8+/4JiD0KCj9wGd+2z1ABC6/cJpIA8Ve/H2E2gDgZgWnMPVTjXpMVb+rEF/vnkIzmshHHPjs4/W6qOA6AXr36nJO4Z7j7zW1jKKX0UbyMq0tfedwB7I+8761JP+BwAA///FHAckAAAABklEQVQDAAJ5fH3qdctBAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-SubjectHandler-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 