---
title: "金和OA CompanyBudgetCollectEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CompanyBudgetCollectEdit-sqli.html
asset_dir: assets/金和oa-companybudgetcollectedit.aspx-sql注入漏洞
---

# 金和OA CompanyBudgetCollectEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/20 13:32
* 297浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

服务器

软件

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CompanyBudgetCollectEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

文本剥离工具

网络安全会议

安全

根据 `CompanyBudgetCollectEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CompanyBudgetCollectEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strAppId = this.Request["httpAppID"].ToString();
  this.strCollectId = this.Request["httpOID"].ToString();
  if (!this.IsPostBack)
  {
    this.strAppNow = this.GetAppNow("Budget_Collect", this.strAppId);
```

参数`httpAppID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Collect/CompanyBudgetCollectEdit.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

httpAppID=SQLI_POC&httpOID=1
```

[![金和OA CompanyBudgetCollectEdit.aspx SQL注入漏洞](images/img-001-6ebb0cacb203.webp)](https://image.mrxn.net/b29702f8efb64d9da967ca3a2c98f3f5.webp)

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
文章标题：[金和OA CompanyBudgetCollectEdit.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-CompanyBudgetCollectEdit-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-CompanyBudgetCollectEdit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALDElEQVR4AeyaC5LbRgxE9XL/Oztuox49BGdE2Y5XqspsBdXsD0DugMp6nfzzeDy+/U59e/Grz7btTu+5zu1XD3ZtxdVXmFlj9dzo5Vo/1yn572AW8r1v//MpJ3As5PtmH69Uf3DgAetyZu/rHGqGOsy580TzQTV43ptsynyux4JzvzkRyofCsXe8Nn+HY8+xkFHc1+87gctCoLYOZ1w9ottf+V2Hmtt1ufM66sO5H4rDT1z1OkMfqkcumhOhcvJVTr8jVD+csefCLwuJuOt9J/DXFuJbBPVW+C2qy0V1qDycsefkIzpj1HL9q3p6xrIf6plGL9f6uf7T+msL+dMH+7/2/7WFQL1Nq7en63DO63eEykHhuDgoDQpHb7yGsw/FodB7jj257nrnyfxp/bWF/OmD/V/7Lwtx6x1XBwT1Vun/6PuWX/5LgbNf6uP43cW8CJWHMz7al/kZGoXnM8yJzoLqU4ficEb9O3Rux1nfZSGz0Na+7gSOhcB5+zDnq0dz+1B9cvNyOPtQ3JxoXr5CqH7gEnl1xqVxIazmAT8+8b0NSofnOPYdCxnFff2+E/jHrf8q9keGeguc86u++VW/fkfzwe7B82e6y8O8P/dKQfl9Trzfrf0J6af5Zn67EKi3AObom9C/D6i8vmgOyr/j9sE8D6XDT3SmvXJxpev/KcLPZwGW44DLz57bhSynbeOvnMBlIXDd2nhn3y5x9HIN1f+qb06E5/3mcq+UfMToKahZuR4LSofC0RuvnTlquYZznzk468mmYK73PuBxWchjf731BP6B8/bcmk8lF+GchzO3D0qHQvUVwvPct2/ffvwXTft9HnkQakb3oHQoTHYs8+Lo5RqqDwqjpVb5eM8K5nMyb39Cnp3cG7zj9xCorUGhzwLFoTBbTEFxc9FSKw7nPJz5qk+9I1Q//MSeyfPMquegZnRd7gx5R6j+nut81Tfq+xMynsYHXB8/Q/o24bx1fTjr/Xswt9LvfKj5UNjnwFl3XrBn5TDv0U9vSg7nPBRPJmVuhcmkVn7XoeYD+09Zjw/7Ov6VBbWlu+fL5lPmcp2C6ofC7svh7MOZmxPh7OdeKf1nCNWbfKpno6XUofIrrt4xM1JQ/VBoLl6q82i9joUY3vjeE7gsxI31x4LaOhR23z4Rzjkori/2OfLuQ/V3H0oHfvyekj4ozSwUh0J1Eea6fmam5CI874PyobD3wVmPf1lIxF3vO4FjIXkDUj5KrlNyMVoKztuF4lBoHoqnJwXF9VcIz3Pw3M/c3G9WMPR+D5r5fjn9B17L9zmdw3nO7GbHQmbm1r7+BI7f1L01PN8izH3fBtF5HfWh5qy4ffpyqD75iFCePVAczqg/9o7Xdz7UvFVupXuP7kPNA/bvIY8P+1r+Kwtqaz6vWxXVRag8FKqLUDoUdt25UP6Kq9v/DF/Nwvmezuz9UDl9KA5n1BedI0Ll5SMuF+KwjV97AsdCoLa2uj2UD4Vu1fyKd73nuy+Huo/5juZGNAPVC4XqZuVi1+F5X8937lyoOXBG/RkeC5mZW/v6EzgW0re84upw3joU1/dbgbO+8ld5dRFqHhSqB/tsuZhMCqoXCqOloPgqn0wK5rl4z2o1F2oesP+U9fiwr+MTArUltwjFYY5+H+ZF9RXCeZ45KL3PkUP55kUoHVC6/J0WcPr/n5wp2tg5vNYHlbMf+HE/ufOhcnLRXPBYiObG957A8V8MfQyoLWZbKXUxWkoOle8cSk82pS9GG0tdhOqXd7S36yM3I8J5JhSHMzrDPhHOOSjeffuhfLloXlQP7k9ITuGD6vJ3WbOtjc8L861D6faLUPo4Y7yG8s3ryWHuQ+nmg1AanDHeWFC+9xDHTK6hcrlOvZpLdlb2w3numN2fkPE0PuD6WIjb85ngvEX9juZXaF6/c3UR5vfVF50zw56BmmlWf4VQeX04c/WOzu/Yc51DzQf27yGPD/v65T9lQW2zfx++FV2HeR7mep8DlYPC1XygWxcO/Pj94GK8KED192fs7VC5Ox0q57zg8a+s3rz5e05gL+Q957686/KPvcAj1TvzsUp1PdlU1+XxUvLMSMlXmMxYPffMy/1SY2a8jpd6NnPMm0tPSk9dXOn6ornMsvYnxNP5EDx+qLsh0e35nOod9cVf9b2PfX2OvKP5GZp1trxnuy4Xe341b5W3X7/3q4+4PyHjaXzA9e3PELfa8e7ZV3l1+/tb1Pkq1+eYC+o5S4w3K/Oiebk96nL9jvqivlzs86LvT0hO4YPqspDZ1sbn1e9bl4vm7FWXiytd3znmRH15UE2MNpZ6R++hbk/Xuy/vOfvFlW+/ueBlIYY2vucEbhdyt927x+795vM2pORitNSKr+Yln75UrlM9Gy8VL5XrVK5TPR9trGRTdzl7Xs2ZD94uJKFdX3cCx0Ky+Vn5KG5bVO+48tWh/kKt98nN+SxdX/Ho9orRxlrp/V72dL33d25fxz5Hf6YfCzG08b0nsPxNffVYs62uss/0/nY5V9QXnaUvqgfVOsZLqec6tZq90tOTck7HeCn79aONpa8mD+5PiKfyIbj8Td3nc8titjiWOTW5+Y7dl4vOWfXpP8M+q2f1RX2595Z3v/Oes3+VMz/D/QmZncobteNniM+w2qq62zcvF9VF+0Rz8p7rvjl188+w99i7wtUs5+jbL19h75OL9smdG9yfEE/nQ/BYSLYz1ur5+lbNrXR90Zxc9N7d77q890VXE/ss9Y7pTa3y8VL25TrV89HG6nm5aFYePBYSsuv9J3D5U5aP5PZFdbfadX11UV20X7zL2XeH8Z0pRkt5j47xZmWue+piv4/57ndubob7EzI7lTdql4W4TZ+pvwXd77znnSPe5e2/yzlvhvY6y4xcVO945/e89xPt7/yuL/nLQnrT5l97ApeFuF0xW0v5WOpyUT3ZlLqoL6p3TG9KPdepFVcPJpfK9VireyabMttznZsT05syJ0ZLdR4tZb9oLnhZiKGN7zmBYyHZXKo/RraWUk8mJe+YbEo916n0zMqcnjw9KXn3ux5fTYz2rHrujud5xjLf0Yz3XvnmRv9YyCju6/edwGUhblX00dym2HW5aK7PedU3t0Lnz9Aevc67ri/q92eXiz2nLjpPNC83N+JlIYY3vucELn/b62P0baq7TbnY9c6dJ65853W0T93+GfaMXLSnz+z+46FyxlXfOfV7bH9Cfu/c/lrX8XdZbl1c3VFf7G9b5z3Xfe+jvuLqonNnaEY0s+Lq/RnUxT6n5/U72v9Kfn9CPK0PweNniNt7Ffvz2+fbIe85ub75OzRvv6geVFthMin9XKfkHfszrfyuZ2aq6/J4KfmI+xMynsYHXB8L6W/Dir/6zPb3vLrYfXneoJR8lVcPmhWjpTInletUrlO5TvV8tFQyKf1cz0pfTG9KLkZLyWezjoUY2vjeE7gsZLa1aL/7mOlN9f5oz2qVV/+V3t4jX6Gz9eV5u2fVc+bF7svFceZlIYY2vucE/ngh43Zzvfo24qX6WxNtVqs5r+jOeyWbTM93nsxYfg+i+Y72qMs7Vw/+8UIyZNd/dwL/+UJ8a3xE34Y7XV+0zzmiuqgenGnRLX3Re+l3rn6H9omv5me5/3whs5ts7fUTuCzEt6fj3UjfDvvMd11f3VxHfdG+nhu52VEbr/VFZ3Y+9ozX5tTsX3H13qc+w8tCZqGtfd0JHAtxi3e4erT+tphT73PVe26lmxOdZ37EVzLJmxOdKaqL6Rmr66u+npOL9gWPhWhufO8J7IW89/wvd/8XAAD//xJuPBcAAAAGSURBVAMAmzd3norOr6wAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CompanyBudgetCollectEdit-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-CompanyBudgetCollectEdit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 