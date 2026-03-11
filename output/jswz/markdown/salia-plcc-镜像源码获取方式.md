---
title: "Salia PLCC 镜像源码获取方式"
source: https://mrxn.net/jswz/salia-plcc-source-code-extraction.html
asset_dir: assets/salia-plcc-镜像源码获取方式
---

# Salia PLCC 镜像源码获取方式

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/8 08:34
* 697浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

firmware

固件

文件系统


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 下载镜像

从官网下载镜像

`http://salia.echarge.de/firmware/`

[![Salia PLCC 镜像源码获取方式](images/img-001-6b449a9a7fe4.webp)](https://image.mrxn.net/00f39d8af68b45ea8ed62bb917727074.webp)

目前可以下载 1.50.0 以及 2.2.0 两个版本的镜像

深入探索

SQL注入防护

物流软件安全

技术文章订阅

`http://salia.echarge.de/firmware/firmware_2.2.0.image`

`http://salia.echarge.de/firmware/firmware_1.50.0.image`

# 剥离镜像

对下载下来的镜像使用 `binwalk` 的 `-e` 参数对镜像进行解压剥离

```
# binwalk -e firmware_1.50.0.image
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Squashfs filesystem, little endian, version 4.0, compression:gzip, size: 65128626 bytes, 18 inodes, blocksize: 131072 bytes, created: 2021-10-15 17:56:28
65130496      0x3E1D000       Object signature in DER format (PKCS header length: 4, sequence length: 2439
65130554      0x3E1D03A       Certificate in DER format (x509 v3), header length: 4, sequence length: 1466
```

得到解压后的 ext4 文件系统镜像文件 `file _firmware_1.50.0.image.extracted/squashfs-root/core-image-minimal-tarragon.ext4`

# 提取源码

主要就是 创建一个挂载点目录后直接挂载上面得到 `ext4` 文件系统镜像文件

计算机驱动器和存储设备

```
sudo mkdir /mnt/ext4image
sudo mount -o loop _firmware_1.50.0.image.extracted/squashfs-root/core-image-minimal-tarragon.ext4 /mnt/ext4image
cd /mnt/ext4image
# 访问文件后 卸载
sudo umount /mnt/ext4image
```

深入探索

编程语言教程

Docker加速服务

网页浏览器

然后再进入目录即可 得到完整的系统文件

```
总计 39
drwxr-xr-x  2 root root  3072 2022-02-03 21:27 bin
drwxr-xr-x  2 root root  1024 2022-02-03 21:27 boot
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 dev
drwxr-xr-x 40 root root  3072 2021-10-16 01:55 etc
drwxr-xr-x  3 root root  1024 2022-02-03 21:26 home
drwxr-xr-x  9 root root  4096 2021-10-16 02:12 lib
drwx------  2 root root 12288 2022-02-03 21:28 lost+found
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 media
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 mnt
dr-xr-xr-x  2 root root  1024 2021-11-30 17:50 proc
drwxr-xr-x  2 root root  1024 2021-11-30 17:50 run
drwxr-xr-x  2 root root  3072 2021-10-16 02:10 sbin
dr-xr-xr-x  2 root root  1024 2021-11-30 17:50 sys
drwxrwxrwt  2 root root  1024 2021-11-30 17:50 tmp
drwxr-xr-x 11 root root  1024 2022-02-03 21:27 usr
drwxr-xr-x 10 root root  1024 2021-10-16 02:10 var
drwxrwxrwx 24 root root  3072 2021-10-16 01:47 www
```

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

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

* [1.下载镜像](#toc-1-)
* [2.剥离镜像](#toc-2-)
* [3.提取源码](#toc-3-)



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
文章标题：[Salia PLCC 镜像源码获取方式](https://mrxn.net/jswz/salia-plcc-source-code-extraction.html)  
文章链接：<https://mrxn.net/jswz/salia-plcc-source-code-extraction.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/salia-plcc-source-code-extraction.html"),
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
text: encodeURI("https://mrxn.net/jswz/salia-plcc-source-code-extraction.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 