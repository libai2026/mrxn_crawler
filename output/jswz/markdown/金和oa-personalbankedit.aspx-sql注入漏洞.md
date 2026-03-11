---
title: "金和OA PersonalBankEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-PersonalBankEdit-sqli.html
asset_dir: assets/金和oa-personalbankedit.aspx-sql注入漏洞
---

# 金和OA PersonalBankEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/9 13:30
* 435浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

云安全解决方案

物流软件安全

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `PersonalBankEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

Web安全书籍

安全研究报告

网络安全会议

根据 `PersonalBankEdit.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **PersonalBankEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  CostManager costManager = new CostManager();
  DataTable dataTable = new DataTable();
  if (this.Request["ID"] == null)
    return;
  ((HtmlInputControl) this.HiddID).Value = this.Request["ID"].ToString();
  DataTable info = costManager.Budget_Bank_GetInfo(this.Request["ID"].ToString());
```

跟进`Budget_Bank_GetInfo`方法

```
public DataTable Budget_Bank_GetInfo(string ID)
{
  return this.db.ExecSQLReDataTable($"select * from Budget_Bank where  BankID='{ID}'");
}
```

至此，就非常明了了，参数**ID**是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.CostControl/PersonalBankEdit.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

在线安全工具

企业安全咨询

网页浏览器

[![金和OA PersonalBankEdit.aspx SQL注入漏洞](images/img-001-b2a97f38d8ab.webp)](https://image.mrxn.net/19365347427646869fb6984a41b6e50d.webp)

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
文章标题：[金和OA PersonalBankEdit.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-PersonalBankEdit-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-PersonalBankEdit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKO0lEQVR4AeycjZbbuA6D8/X933lvYAYSY9GKM5MmubvqKQcUANKqaM1Pu2f/XC6Xf34b/9x+uc9tuYG5jJtw/ZC5Kr9att9ntc384EPVK3NVedad733mf4sayLXH+v0tJ9AGcp345Zmo/gCuBy4QYZ81obmM4hWZcy5+HxD9Mw/BQUf3gOCy31qFEH6gkqdcfsaZPDdrA8nkyj93AsNAgPZ2w5if2Wr1VuQ6iL6PuKwrh6gDtNwCaPudPdcadP/W4PrBmvC63H4rd2zE7gNEnx19t4TwQI135ttiGMiNX/ChE1gD+dDBHz32pQOB8Wr6wdC16lNBxUGvAR5+01E9C+572JMRuifzs7za78x/VnvpQM4+dPmOT+ClA/Fbk9GPzhzEG2lNCCOXa5TLdybkPYpH9RD7gI6Pal6pv3QgbWMr+fEJrIH8+Oj+TuEwkKOrbv7MNmC87jBy7pmx6g9RmzV4joPR7+fmvhWX9Wdy9zrCqtcwkMq0uPedQBsIxBsE57DaIkRtfiNg5H5aC9EL+rfAcI7zMx/tDaJf9s1qrWWE6AHnMNe2gWRy5Z87gTWQz519+eQ/+Wr+NHdn10O/qtYy2neWg+jnOqFrlTvMZYSoNQexBky1v5yEOdcKrsn+mV7/FtcNuR7uN/0eBgK0N8Ybhc7BmO99+S3ZazDWA7a1Z0Pn3A9ougugcxC5tbPo/sKqRrwCoj+MWNVlDqImc84hNOAyDOTyvb/+EzsbBqI3weET8Fo446xBn7hqFNaEWiuUOyBqvD6L6uNwjdeP0P4Kcy3E3jK3r4HwAHvpbg20Ww6RZ8MwkCyu/P0nsAby/jOfPnE6EBivlLtBaICp8h+QgO2KNtMTCdzX5k8ZEBp0tJ4fAaGbg1gDpn6E+2d5LQSGP7N4RX6Y1orMTQeSjSt/zwn8gXGafrSmp4DwAJbubkMjJ4n6OCpbpZkDtjcOOlrLCKFX/c1lv3NrGSF6Qf97s0rPnHP3hd5jr8kDoSt3rBvik/oSXAP5kkF4G9OBwHilfLUgNOjopn8L/WyhnwHPPR+6H8ZcvRXunxG6Xx6FdegaRC7dAcHZnxFCA9ZP6pfLd/1qNwT6lCByT7fasrWMEHWVv+Kq2sxVNXsu+51D7APY2+++GbF/MO0IYPumwn4hBLezbkvpim1x+6C14rY8hDaQQ8cS3noCayBvPe7HD2sD0XVSPC4JB8SVBYK4flS94poOv4Ht2kPHbFKdAkZdvAJGDUYu953lELXq7bDfa6G5CqUrsgbRN3POITTA1B22gdyxa/GxE2j/hAtsb3DeCRxzeiscroHwQ0d7KnRdxuwzD9EvaxCcPY8Qjv0QGtDaANt5ACXnvTTxQQJs/VwndIlyx7ohPpUvwTWQLxmEtzEdiK8RxHUDXLddP+AO7W+mlED3JnpIYfRVfc1ldLPM7XN7hHtNa4jnS3eIV3gthNEn/ihUr8i61gqIXsD6Sf3yd379uOv0hlRdNdGjsD/rENO3JoTgYETpRwGjH85x7gndb67C/Geo9Bnn2pnnSHt6IEeNFv+aExj+gcrTFfoRyh3m4Lk3zXXCfS9xDmtCcxDP8looXaHcofU+rEH0yDoEZ4/QuvJ9WBNag7HHXoPwQI32C9cN0Sl8UayBfNEwtJX2k7oWCqivFdzzurYOCE31R2Gv0B7lDnMQvaCjPRkh9MxVPaxby2gNohecR/dxD6+FEH2sPYPrhugEvyimX9Q92bxfcxBvAfT/KgOCy/6zuftWWPWwb6bJA8d7gtDk20fuay1zziF6eC2s/DD6IDjouG6ITvCLYg3ki4ahrbSBVNcM4irJuA/7hXsNog467j1aQ9chcvEOCA5GrDzmZgi9l/auyH4IPXPO5XXsOa+P0HUQ/YHS2gZSqot8+wm0b3uBu7+5BaabAQa/34JcWHEQtY98Va1rYOxhrUL3ylj5Kg7GZ7kPhOa1EIKDEav+mVs3JJ/GF+RrIF8whLyF9nOIrpoii1rvA+Ia7nmtIbTcA0bOumoc5iD8gKnT/3EbMHwadRM41uw5wv0e5YPop1wBsQa03MJ1j3Az3z6sG3I7iG+BYSB5mt4k0N68ioPQc+0+d53QmnIHjD0gOAi0V1j1mHHWMsLYV72PAsIPHFk23s/YFrcPwHaGt+UGMHLDQDbn+vCxE2gDgZgWjFjtzm+BsNJnHMQzZp5Kg6iDjpVPe3JUurnKU3EQz7OW0b0eoWuyr+LaQLLx7+ar++wE1kBmp/MBbRiIr1HGal8Q1xjmf/0O4cs93PsRl3XlrhNqvQ+IZ0HHZz0Qtfu6o7X2sg847gGhQcfcexhIFlf+/hNoA/GUz27BfqFrlCugT19rBXTOfphzqsvhuoxZr3KIZ+SaV+Tws77VHjPXBvKKTa4evz+BNZDfn+FLOwx//V51z1fKOcSVBVoJcPjTqOuErSAlcFybbNMUogd0dAEE57VQe1FAaIDoIeRRANufDxg8wKEmM4SufBbrhsxO5wPaMBCISUKN3qPeGIe5Cmcea0LXKt8HxF7syQihQf/2O9dnr/KsQdSK30f2Was4GHvY5zqhOQg/IHqIYSCD4/+E+Ldscw3kyyY5/AOVr1bGas9A+yIGkduXa+Fes0cIoUH/dCP+TPgZ2Qu9H0RunzH7K846RD1gqkT3yFgZge28sg+Cg47rhlSn90Fu+LYX+rQg8jxV77XirEHUAaYeIrC9QTDiw+KbwXu6LTeA6LctDj64TnhgOaQh+sMc1VuRG2m9j3VD8gl9Qb4G8gVDyFuYflG3Efp1rDhfO2teC82dRdUcBfR9QORV36oewg9zrPqZg15r7jcI0S/3WDckn8YX5O2LerWX6k2zL2vmKrQP4m0AKlvJAXdf6EvTAxKih23eT0ZrGR/p9mbfPrdHCPf7EOeA0ID1Pw64TH+9X2xfQ6BPCZ7LvW2/IV4fIUT/rLsWQoP+w6K1CnMP5zD2sFbh2b5VrTnozzSX0c/IXJWvryHVqXyQWwP54OFXj24D8ZU6i1UziGubNRg56/lZEL6Kg9BclzH7zVectbMI8Uyglcz6zrTW4ETSBnLCuyxvOIFhIMDdt5pwv352T/nNce4e0HvvNXseIfQeMOaP6qXDWOf9CCF0efcBocGI2QuhZ865nuEYBmLTws+cwBrIZ8798KkvHYivXX4ajFe18rkGwg+YmqJ7CW1U7thzwPAp2V6h/RnFK2ac9H1kf5XbD31PLx1I9dDFjScwY146EIhJzx4oDc755M0BUQcds+43LnPQvVD/9J/9sx7ZB9H3rD/XzvKXDmT2oKWdO4E1kHPn9DbXMBBfwSOc7cw1lQfiigOV3L7QukfGsuBGAq32RrU1jJ+iYPS7Tghdh8i9F4g1IOsWwN3zgI3XB9dlFO8AttqsDwOxeeFnTqANBGJacA5n24XeY+bLb4Z90GshcmuVP3MQ/oqDUXNfCA0wVWLua0PmnFsDthsAHa1lhK63gWTDyj93Amsgnzv78sn/AwAA//+BU/6mAAAABklEQVQDAKjZKLOz0BinAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-PersonalBankEdit-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-PersonalBankEdit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 