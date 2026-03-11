---
title: "【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上"
source: https://mrxn.net/jswz/dg-ghope-vm-gho-no-iso.html
asset_dir: assets/【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上
---

# 【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上

[Mrxn](https://mrxn.net/author/1)* 发表于2016/1/20 19:36
* 7159浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

磁盘

硬盘

虚拟机


(adsbygoogle = window.adsbygoogle || []).push({});

---

首先说一下，博主写这篇文章是因为博主在学习过程中恰好遇到了这个问题--如何将gho格式后缀的系统文件安装在空白的虚拟机上，并且最终解决了我的问题，所以在此小计一下。这时候系统文件是gho，没有安装菜单，不支持分区怎么办？那么看下面的方法，不需要iso虚拟机测试安装gho系统的方法.

还有一种情况是物理机安装了系统发现不对劲，怀疑是安装工具修改了系统，排查重装系统又太麻烦，就可以用虚拟机测试了.

操作系统

准备工作：gho文件，DiskGenius，GhostExp，两个软件的下载地址：<https://userscloud.com/lfbb6g8jv10m>  <http://pan.baidu.com/s/1eRcw5xC>

大致步骤我说一下，其中一些不需需要改变的步骤我就不说了，需要注意的地方和重要的地方我会贴图，详情请看图：

自定义创建：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-001-a200d16ef0aa.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/0d391453289955.png)](https://mrxn.net/content/uploadfile/201601/0d391453289955.png)

深入探索

安全运维咨询

企业安全咨询

网络安全课程

不需要加载光驱，选择稍后安装系统：

物流软件安全

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-002-32ee39c22872.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/2bf01453289955.png)](https://mrxn.net/content/uploadfile/201601/2bf01453289955.png)

深入探索

文本剥离工具

安全认证考试

服务器安全服务

这里可选择创建的虚拟系统的版本，这里是选择XP：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-003-3275bb2fefde.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/86291453289955.png)](https://mrxn.net/content/uploadfile/201601/86291453289955.png)

虚拟系统保存目录选择，可自定义，但是一定要记得保存的路径：

操作系统

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-004-ab39b82d0156.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/01b81453289956.png)](https://mrxn.net/content/uploadfile/201601/01b81453289956.png)[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-005-237353b07d14.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/30eb1453289956.png)](https://mrxn.net/content/uploadfile/201601/30eb1453289956.png)

创建完虚拟机后打开DG分区工具，打开虚拟硬盘文件，就是虚拟系统的文件：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-006-514b52df7c45.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/f0631453289956.png)](https://mrxn.net/content/uploadfile/201601/f0631453289956.png)

看好了，别选错了，一般就是你命名以为vdmk之类的结尾的：

硬盘驱动器

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-007-7ca560211183.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/4f8b1453289956.png)](https://mrxn.net/content/uploadfile/201601/4f8b1453289956.png)

这里只是作为演示，我就知分了一个区，在实际使用中，可以根据自己的需求来分区，然后格式化：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-008-c8b4023663a2.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/55f51453289956.png)](https://mrxn.net/content/uploadfile/201601/55f51453289956.png)

然后打开虚拟机的[磁盘](#)管理，加载到物理机Z盘：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-009-198d678b4b26.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/7b2d1453289956.png)](https://mrxn.net/content/uploadfile/201601/7b2d1453289956.png)

[选择虚拟机的C盘，去掉读写保护：](https://mrxn.net/content/uploadfile/201601/04241453289956.png)

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-010-2f6d0848d8ab.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/04241453289956.png)](https://mrxn.net/content/uploadfile/201601/04241453289956.png)

打开我的电脑就出现了Z盘：

操作系统

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-011-e4bb1f7a93ea.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/19451453289956.png)](https://mrxn.net/content/uploadfile/201601/19451453289956.png)

然后用gho镜像浏览器打开gho系统镜像文件，全选，右键提取到Z盘：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-012-be74d3b625c9.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/28021453289956.png)](https://mrxn.net/content/uploadfile/201601/28021453289956.png)

**切记**--提取复制完后别忘了虚拟机磁盘管理取消共享的Z盘：

硬盘驱动器

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-013-beaba9446680.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/9b1f1453289956.png)](https://mrxn.net/content/uploadfile/201601/9b1f1453289956.png)

然后打开虚拟机电源启动虚拟系统，看见这个启动界面就是成功了..：如下图

计算机硬件

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-014-023a81eb4f90.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/c6351453289955.png)](https://mrxn.net/content/uploadfile/201601/c6351453289955.png)

以上是vm虚拟机安装测试系统的方法只用到了虚拟机和另外两个小工具，并没有用任何iso文件或者是什么PE系统....

操作系统

掌握了这个方法以后遇到下载的gho就不用担心没法测试了.同时也方便大家在虚拟机安装gho格式的系统。不懂得可以评论留言，我看见了就会尽快回复。

* 标签：
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#windows](https://mrxn.net/tag/windows)

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
文章标题：[【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](https://mrxn.net/jswz/dg-ghope-vm-gho-no-iso.html)  
文章链接：<https://mrxn.net/jswz/dg-ghope-vm-gho-no-iso.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dg-ghope-vm-gho-no-iso.html"),
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

Windows安全工具


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dg-ghope-vm-gho-no-iso.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 