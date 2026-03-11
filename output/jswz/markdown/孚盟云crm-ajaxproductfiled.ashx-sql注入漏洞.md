---
title: "孚盟云CRM AjaxProductFiled.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductFiled-sqli.html
asset_dir: assets/孚盟云crm-ajaxproductfiled.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxProductFiled.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/19 16:41
* 542浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

鉴权

SaaS

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxProductFiled.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxProductFiled.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxProductFiled 方法的实现如下

深入探索

SQL

身份验证

服务器

```
public void ProcessRequest(HttpContext context)
{
  try
  {
    context.Response.ContentType = "text/plain";
    string str = context.Request["method"].ToString();
    context.Request["MouldID"].ToString();
    if (!string.op_Equality(str, "savePuductFiled"))
      return;
    this.savePuductFiled(context);
  }
```

当 **method=savePuductFiled** 时，进入**savePuductFiled**方法

```
public void savePuductFiled(HttpContext context)
{
  string MouldID = context.Request["MouldID"].ToString();
  DataTable dataTable = this.GetsyFieldGroup(MouldID);
```

继续跟进 **GetsyFieldGroup** 方法

```
public DataTable GetsyFieldGroup(string MouldID)
{
  return this.dbHelper.Query($"select FUID, MouldID, GroupName, OrderNo from dbo.syFieldGroup  WHERE MouldID= '{MouldID}' ORDER BY OrderNo").Tables[0];
}
```

深入探索

数据库

木马

CRM

最终可以看到，未经过滤或参数化绑定的参数 **MouldID** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxProductFiled.ashx?method=savePuductFiled&MouldID=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxProductFiled.ashx SQL注入漏洞](images/img-001-6d80a096d75c.webp)](https://image.mrxn.net/ec1df2062d4f4857b41687f79677d938.webp)

成功延时 5 秒

SQL注入检测工具

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
文章标题：[孚盟云CRM AjaxProductFiled.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductFiled-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductFiled-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALRUlEQVR4AeycgXLkNg5E5+X//zm3cO+TRUgcadeOZ6qOruCa6G6ANCGt7XUu/zwej3//Jv79/WHt73QD+Y6bYbLQr9xzeVG9sHPmYnn2IT/DvXe/7n41efO/wRrIr7r1z7vcwDaQX9N93ImrgwMPYLPZUwIYdEgOQX0zhNFn/0KIVusKe8BzvvsgfvmOEB2CXTevM9wJ/YXbQCpZ8fobOAwEMnUY8eqoEH9/ImZ1EP+Vbj+I3/ysTg3i7R4Yef36zMUZ33V9M4TsCyOe+Q8DOTMt7udu4MsD6U8LPH8K9It+qle5Phj7w2eux14QTX6GMPrgPIeRt5/7mX8FvzyQr2y+ao838G0D8SkR3QrOnyr17pcX4Xm9vkKIF4LF7ePuXvo67nvVWr3W3xXfNpDvOtD/e5/DQJx6x9lFwfg0Ag9+hX77mEP8EJQXu7/n3ae+x5kHsqdeGHPrIHzPe536FVrX8azuMJAz0+J+7ga2gUCeCniOd4/m0wDpZ269OUSXh/Ncvz4R4gekDgh8/O2APeB5fmhwQUD6dRuEh+e4r9sGsifX+nU38I9PzZ/i7Mj2Ue+5/Az1Q54q8yt/+a486uWt6DlkT/mOEL1qK9RrXdHz4v401hviLb4JHgYCeQpgRM8L4c1FCA9BeRHC+8RA8q5D+Jlv5ofUAVoOCHx8LekChHdPEUa+15lDfHCO+kQ49wGPw0Ae6+OlN/APZFr9FD4lMx7GOv2idTD65LtPXoSxDsbc+j1aKwepgWDn9c9Q/0yXn/nkIfvr76ivcL0h/XZenG/fZd09B2TaNc19QPhZH70QHwTlb+DwG83ZPsVDetd6HxDevdTMITqMOPPJQ/z2EdWvckg9sL6GPN7sY/saApmS04Tk/bzqVzyM9TDm9oGRhzF3HwgPc9Tb0b3k4bxH95lD/NZ3vPLB8/p9v/U1ZH8bb7A+DAQyTafezwjRr/hZfa+78kH20/cMe++r3F76IHuZz9A6iB+CV7z9YPTLFx4GUuSK193ANhCn248iD/OpVk33FVchX+uKnkP6lnYW3X/m6dxVzUyf8faH87NaB6Mu3+s7b164DcSiha+9gW0gME4XkkPQY8J5DuFryhXdX1wFxKdeXMUsh9Gv72+w9qmAsWdxFRC+1hUw5u4J4XteNfuA0afW6yA+YP0c8nizj+0N8Vx9ip3ves/1i1e6Pvh8SuBz3fVZLl8Iqe97wwlfBZPo9eZiL4P0l9cH4SHYdX2Fh4FoXviaG7gcSE2tAjJdGNFjl6fCvCOkbsZXbUXXzUurgPM++grLV1HrfRRXAekBQT2lVZhDdBhRXayafchD6vZardVFiA9YX0Meb/axvSE1uQrItGpd4XlrvQ95EVIHQfmO9oBzn7poPcQvL0J4QOsBgY/fFELQWtECiG6u3rHrkDoIqosQHkZU3/ffBqK48LU3sA0EMj2nBckh6DHhPLdOhNE3q+9+OK+zXoT4rC/smrlYngpIrTwkL62i8xAdgl03r9oKGH3qYnkqID74xG0gmhe+9gZu/8YQMsWa7Fn4acDok7em53Du7z5zGP2QHNBywNne3Qj80dea3rf363n3m+9xvSH91l6cb78xdEqQp8Tc85lDdHkRnvMQvfe5yiF17nMH7dm9kF4Q7Lq59RAfBNVFOOcfj4eWD7TfR/LrfyB1EPxFbf+sN2S7ivdYbAOB47TOjjibtrwIYz/53hPi63rPe92zHNKze+wpznR5fXcRxn2ts58oL8oXbgOpZMXrb2AbyNm09seDTB9G3HtqDdHtJ0J4CJa3Qr3WFTDqxZ0F3POd1c44SE8Ysfth1CH5le9KB9bfZT3e7GP7OQTOp+x5fZI7qkPq1SG5unxHOPdZJ1rXc/k96ukI417q+9pay19heSv01fos1O/g9kfWHfPy/Pc3cPg5xAnPtobnT1mvg/ghqA7J+34QHoLqkNx6EcIDUhsCw0/eCjDykFzdPc1h1OVnCM/9EL3vU/3WG1K38EaxBvJGw6ijbAOBvEbwiUB5hjh7zfYG4OOPiSvfTJcX7d3zzpcuJxZ3J/R37LXq8uYdr/Tu3+fbQPbkWr/uBqYD6VOGPPkwokeH8LNcXoT4YcSv6oAtNgQ+3tqN+L2AkYfkcI6/yz56AaYbApsGn+vN8Hvh3UI85oXTgfyuXfDDN7D9YOi+NaUKOE6veKP7zUV9HeFe396n571v5d1jLkL2Nherdh/yohqk3ly9Y9fNIfX65c0L1xtSt/BGsf1g2M/UpweZLgRn/qu6mT7rB9mv13V/5Veerve8elR0Hs7PACPf66rXWUDqILj3rDdkfxtvsN4GcjVddbGfHY7T3ntmdZ2HsY86hIfgvrdriAYjqovwXNfXEVJ3l/fs3W9+pm8D0bTwtTdw+C6rHwfyVMCIThfCm1sP4c1FOOfV7QPxQVBe1A/RgeE/LKBvj9aIauaQXuaiPhFGX+chOgTtI+o3h/iA9Quqx5t9HP7IgkzLczrNjuoipA6C8iI85+Fcd18YdRhz9ymEUYPkEJz1nPGQuupdoU+E53rVVOiv9SwOA5kZF/8zNzD9OQQydXiOd6Zen8pdH2S/qtmH9RDdfO/pazj3wj2+7wGpgxH1ibNz3OHXG9Jv6cX59l0WZOr9PH3qPYfUdb7nEN+f9tcPz+trP721rjCH1Ba3DwivT80cRl1enwjxwTl236xP+dYb4u28CW4DqemchedUgzwFV7z6DCF9IDjzzXhIHczRM9sD4jWf6RBf162D6OZ30X6QejjiNpC7TZfvv72Bw3dZkKm5LYy5U1bvqA5jnT518xl231VeffSIkDOYl+dOdP9Vbk99HdXFru/z9YZ4S2+Ch++ynBaMTxckh6Dnh+TWyXec6fJir4P0l9cHI6++R717rtaQWhix++GeXj0rIP5aV0ByCBZXAWNenLHeEG/iTXA6kP60eN7Om0OmDkH9IoSHoHxHGHX764PonS8dotX6WVgr6oXn9TDq1ov26TjTYexXddOBlLji52/gjwcC41RhzH0aRD+lnstD6iHYfRBevwjh9e9Rjwjxmosw8vZQF+VFSB2MqB/C6++8uQjxA+v3IY83+zi8IfA5LWA7rtMWFcxFeeDj3+KTh+Tq8qI8jL7Oz/yA1ilaCwxn6wUw6pAcgvrtN0N9oj5zUb7wMBBNC19zA4ef1D1GTavCXIQ8JaVVdN68Y3kr5CF9ICh/hTD3QzQI3u1V56qAsQ7GvDwV9oXo8GdYPfYBn/XrDfF23wS3n9T3E6v17HylVahDptvz8lTAqOsTy1Mxy+U7Vs0s9MLzvfWJ9pvlMPab+eXFWb/Ol3+9Id7Km+D2NQQyfbiHnr+mug/5jpC+ertuDvFBUH6GEB8ws2z/vhbwV99d2dizi/IdIftc8RAffOJ6Q/qtvTjfBuLUr3B2XsiUrdfX885D6jpvnajeUb2wa+Yw7iFfNRUQvdYVMObFVUB4GNF+YnkrzMXiKnpenLENRNPC197AYSAwTh+Sz44Jow7JIXhV55MhQupgRHX7wajDZ65HtFaUh9TIQ/Kuw8ird4T4YMQr314/DGQvrvXP38C3DcSnrH8KkKel8/ohOgTlRevgXNf3DCG19rpCe8186n+K9ut1kPMB6297H2/28W1vCGTK3/X5wdjPp8r+EB2O2D2zvPfsPvWOMO7Z6+C53v3mhd82kGq24us3cBhIfxrMZ1upi1c+yNOj76t11hfaE7JHcWehT4T4za0xF+G5b1Znfccz/2EgvWjlP3sD20Ag04fnePd4ffqQvvKQHIKdn+V9f0g9HP8/ht3bc0ite4n6IDoE5UU452d9eh0c67eBaF742htYA3nt/R92/x8AAAD//1V546UAAAAGSURBVAMA8kcrwuzCcPIAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductFiled-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductFiled-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 