---
title: "金和OA BorrowShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BorrowShow-sqli.html
asset_dir: assets/金和oa-borrowshow.aspx-sql注入漏洞
---

# 金和OA BorrowShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/20 13:28
* 344浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

服务器

SQL

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BorrowShow.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BorrowShow.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **BorrowShow** 的处理逻辑

深入探索

文本剥离工具

企业安全咨询

编程语言教程

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.ReadLocal();
  this.initDiv();
  if (!((Control) this).Page.IsPostBack)
  {
    this.strBorrID = this.Request["borrId"].ToString();
    ((Control) this).ViewState["borrid"] = (object) this.strBorrID;
    this.BoundGrid();
    this.Reading1.ModuleMessageID = this.strBorrID;
    this.Reading1.ModuleID = "IOA_Borrow";
  }
  else
    this.strBorrID = ((Control) this).ViewState["borrid"].ToString();
  this.initText();
}
```

深入探索

SQL注入检测工具

Web安全书籍

安全工具开发

参数`id`被带入`initText`方法

```
private void initText()
{
  DataTable borrowInfo = ArchivesBorrow.GetBorrowInfo(this.strBorrID);
```

跟进`GetBorrowInfo`方法

```
public static DataTable GetBorrowInfo(string strBorrID)
{
  string QueryString = "select a.UserID,a.DeptID,BorrDate,BorrbackDate,DocIDs,b.UserName,c.DeptName from ArchivesBorrow a inner join Users b on a.UserID=b.UserID and b.UserType <> 2 inner join Department c on a.DeptID=c.DeptID where BorrID=" + strBorrID;
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/BorrowShow.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA BorrowShow.aspx SQL注入漏洞](images/img-001-263c2641eb07.webp)](https://image.mrxn.net/5d1856068b394f39a253a738cf51838c.webp)

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
文章标题：[金和OA BorrowShow.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-BorrowShow-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-BorrowShow-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKcklEQVR4AeyagXrbNgyE/ff933nzCT0SJilaSp1IW5kv2IF3B1AhzNht9+vxePzzp/HP7y/3+b3c4Ci3mb/wH/f/FM4eIe/R+rL2J7kG8qxf33c5gTKQ58QfZ2L2AwAPiLAPYg2YKh6g5EV8JlB5GOejZ36Wfvkb+n3cLO8F4bOWMfuO5Lm2DCSTK7/uBLqBQEwexjh7VL8asmfGWcv4rta6a7wWQjyzNaH4vZC+F6MaiP7ASO44oNx86POu4El0A3ly6/vCE1gDufDwR1t/dCAQ1zJvBD2XdefQ+6Dn7B+hf/1kbcRZh6/1d0+he30KPzqQTz3U39znWwaiV84sIF6ZUNFDgJ4b9YLwuU4IPSdeMeohXgFRB2h5aXzLQB6X/kj/7c3XQG42v24go6udubPPD2yfxd/VeY/sMwfRAyraB+c5iBr3d6+M1oQQfugx17S5amfR+rXuBiJyxXUnUAYC/fRhn/vEI+dXD8ReMy7vad87LuvKXSeE/T3lbUM1jlbLa4i+cAxzbRlIJld+3QmsgVx39sOdf/kK/gm6s3t4LTzKybsXEFc/6xCc+wuz7hzC5/UIITxA+ScIqJxroHLaT2FN+Sdi3RCf6E1wOhCIV8ToWSE0YCR/mQO2j8lQX61uNnoFQvVD5COfe4ww++FrPXJfiB7Q4zvfdCC5+Ab5X/EIv+B1ivmn9isncxB+a0IIzj6INWCqvOphzqmfw8VeA6VPq8ljDvZ99pxBiH7awwHBuQ/EGurNtlc48pnLuG5IPo0b5GsgNxhCfoTysdck1KsHkVvLCKFBvaLWdUUdIw6i1h6hfTOUzzHyzTSIPUd1mTvSA+rPDH1f6Lm8R5t7T+G6Ie3pXLzuBqIptQExcaivjOyBqgMvPxJQ3oghctdCrIGXmr0F0PXKXgjd/YXwymX/KIfwZ0192si68qxrrYDoBfXcxLcB1dcNpDWv9c+ewBrIz573293Kn0N85aBeH4jcmtAdITTAVPl7oEKkRLWORJd0pgHbryp7MkJoQOk1SoCtB1S0Dyrn3lC5kQ9Cn/mtCeHVL859lTvWDfGp3ASnA/HUIKYLlMe2JjQJbK9Cr4XSFRAaVJTugOC9FkLPiVdAaOrtEN9Gq3mdMddA9B1xoxro/fblHkfz6UCONlm+z53AGsjnzvIjnbqB+LoJRztAXFGoKK9i5DcnvQ1rQmtQ+4rPAfuafO6h/Ey47h1C3b/1vtvP/pEPat9uIKOCxf3cCZSBQJ0SvOaertCPptxh7ihC9M9+CM49hdaV7wVEHYyx7eF1Rqi15qFyEHl+BgjO/ozQa9BzucZ5GYiJhdeewBrIteff7V4G4uuYHSPOOsQVBEwVBLY/j0DFIqbE/YWmYV7T+lTrsJYRop85iDVUdL3QvrOoWsfRWvszloEcbbJ8h07gy6buH6jytNwVxq8me+3zeoRQe9gPPZdrRz6IGvsg1oDtQwS2W5tF98gcHPO1tRB1QG5X8tZfhGcCbM8GPNYNedzrq/xtL8SU8uNBcJ6u0DqEBhVnmmod9mX8qna0h33eR2guo3hF5kY51J8beLGoXgGUVz5Eno3Qc+uG5BO6Qb4GcoMh5Ecob+q6YgqIawTjfweG0OV15IZtbg9EHdBatjXQXe+21mvhVvT8j3IHRI8nXb6tmYDwAKa6faH+7KovxpSI3wtg65n1VFpS64V4JuuGPA/hTt/dm7qnJvSDQkwcMLW9AoAN5VUUMSUQnkSd/qde9VbkHhB9oWLWnUPoXo9QvduAqANKCbD9vMCQAza9iIMEwgMVs23dkHwaN8jXQG4whPwIZSC+slCvko3W9tA+457PvH0ZRxrEs9gHsYb6pmtNOOohfi8g+mUdes66+wshfMoV9gi1Vig/G2UgZwuX/3tOoHzshZh43gZ6zjqEBpja3tCAIRbTM4Hw6FXkgOCe8rd8e593zUc+iGeDivZBcF4LITioONtXNY51Q2YndYG2BnLBoc+2LAPxlRmZob969gshdOVtuB+EBzA1RKD8ynMvG70WQviUOyA4+4Wt5nVG+RwQPbI+yu23BlEHWHpB+zI54spAsnHl153AoT+pjx4PKK9k61A5iNyvghG6TjjSIXpIV0CsYf6xN/dSXQ6oPTLf5tD7oHLwmuf6vL9zCL/XQtdAaMD6B6rHzb7KryxNTJGfT2tF5iCmKd6RdeXmhRB+qCiPAioHkYt3qF4BoSl32AOhAabKzQVKXsSUQOiJGqbQ+/wcxmHhGxKir3sIy0De1H5QXq1mJ7AGMjudC7TTf1LXtVJAXDeob7DiFUd/DnkdroHaFyJvPfYKrQkh/OId4nOYF5pX3oY1oTXlDoi9INC8EIJznVC8QrlDawWEH1hv6o+bfZVfWZqUIj+f1m1Yz7w5qJOGyLPPOYQGFa251zuEqM0+98hoHXo/9FzrB0xNEZh+gJgV5+ctA5kVLO3nTmAN5OfO+tBOZSAQV+5Q1dME4Qeeq3Pf+Yo6B7Yrf67Tqxve9/B+GSHqoH5AyZ3tfcdl/UwOdf8ykDMNlvf7TmA6EKiTg8j9KH7VCFvO6zOoPm2cqd/zQjy3e+/5zEP4vc4IoUFF6+4vNPcOIfqoxjEdyLuGd9L/L8+yBnKzSZa/fveVyc834iCuGexj7jHKIWqzBj3X7g/hAUopsH0YgPEbso0QPq+F0HPiFd5bqLVC+V5Id9jjtRD294LQgPUn9cfNvsrfZfm5oE4LIreW0a+CjFlvc4heQJGA8uo2CZWDyK2NMO8P4YeKrrHPa6G5EULtAZGrpg3oNQgOKrZ1Wntf5Y71HuKTuAmugdxkEH6M8qZuIuPoSlmH/jranxHClzn3OMrZ/xX0Hq6FeB4Yo32uy2hNCFGvXAGxBrTswn2A8msaIrcmXDekO7prie5NXVNy+NG83kP7ICYOFa1ldB/ofdBzuda5e3h9FF0ndI1yB9T9YT8f1bqH0R4hRC9rQvEKCA1YH3sf06+fF8t7CNQpwbncj62pK7zeQ4j+WVedYsZJd0D0gIqutUcIoVs7iqp1uMZroTkjxD6AqcOofo71HnL42H7GuAbyM+d8eJcyEF+ZozjbYdQDKB/3RrUQeq5tfRAeoJV21+4HlP0h8lGR/SNtxrlOOPKJV0DsDRQbUJ6tDKSoK7n0BLqBQJ0W9PlXn1avDod7eJ3RmhBif+VtuKbl2zW89nCdsPVqDa9+cbOA8EOPuQ5C174O614Lu4HYtPCaE1gDuebcd3f96EAgriX0mJ9AV1MB1WcdKiePAoJT7oCem/VwnT17OPNB7AnslW/8rMdm+P2fke+jA/m9z4I3JzCTPzoQTzyjNwfKRzuI3NoewqsPYg2UEqD0NTnb3x6hfcrbgHlf146w7aW1fcrbgLrXRwfSbrTW509gDeT8mX1rRTcQX609/OTT5D3cN3POR5q5jK1/pEH99ZB15xC610L3hdDgGLpOqD5tQPSR7ugG0hat9c+eQBkIxLTgGM4eE2oPT37mzxrUWojcPSDWUP8fLGtC94Hqg9fcHiG8alD7Sj8S2lcx8kLff+TLXBlIJld+3QmsgVx39sOd/wUAAP//b+EftwAAAAZJREFUAwC6OWe5dxbtxwAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-BorrowShow-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-BorrowShow-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 