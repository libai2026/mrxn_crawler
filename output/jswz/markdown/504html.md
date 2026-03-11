---
title: "Nessus v8.9.1 系列的最新(20220407)插件更新方法说明"
source: https://mrxn.net/jswz/504.html
---

# Nessus v8.9.1 系列的最新(20220407)插件更新方法说明

[Mrxn](https://mrxn.net/author/1)* 发表于2020/10/17 20:04
* 26058浏览
* [75评论](#comment)
* 29分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

之前写个一篇关于
[Nessus](https://mrxn.net/tag/nessus)
8.9.1版本在windows上的激活无IP限制的方法文章：
[**Nessus v8.9.1 系列Windows10上安装激活无IP限制版本**](https://mrxn.net/hacktools/659.html)
其中介绍了详细的安装过程，这里不做重复介绍，需要看的去自行查看，评论里面包含了大部分人的疑惑解答，不懂得可以先看看。

但是，后面还是有很多朋友在我的另一篇
[**关于Nessus的新插件包使用和AWVS最新版的使用方式**](https://mrxn.net/jswz/673.html)
下面还是说有问题不行，so,就有了今天这篇文章，最后一次说明了，不明白的请先看上面提到的两篇文章的内容和评论回答自行摸索解决，当然，你也可以提问评论，我有时间看到了肯定会回答你，今天的文章开始：

首先！本文是在
[Nessus](https://mrxn.net/tag/nessus)
8.9.1 的X64 windows版本测试进行，其他系统的可以Google搜索下，大同小异，需要下载对应的软件可以在上面两篇文章里或者评论区找到下载链接，如果链接有挂掉的，请留言等候我更新，着急使用的可以直接去下载上面文章更新的虚拟机链接导入虚拟机即可食用！

更新插件包得有插件包，对吧，插件包 你可以去官网登录参考我第一篇文章的内容去操作，下载的插件包可能是普通的插件包，另外也可以看我分享的插件包，一般是 pro 版本的插件包，比如今天写这篇文章更新的插件包：all-2.0(20201015).tar.gz 即使当前最新的Nessus插件包，先看下未更新之前的插件版本是202008282357：

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202010/thum-037c1602937152.png "点击查看原图")](https://mrxn.net/content/uploadfile/202010/037c1602937152.png)

下面说下更新
[Nessus](https://mrxn.net/tag/nessus)
插件包的步骤，很简单的四步曲：

第一步：下载插件包 all-2.0(20201015).tar.gz

第二步：以管理员权限打开CMD，切换到你的 Nessus 安装目录，默认是在 C:\Program Files\Tenable\Nessus ,请自行确定自己的安装路径，复制出来安装路径即可

第三步：使用 nessuscli.exe 来更新插件包即可，语句如下：nessuscli.exe update "C:\Users\mrxn.net\Desktop\all-2.0(20201015).tar.gz" 其中最后面引号内的内容为插件包所在的位置。

第四步：每次更新完插件包，Nessus 会自动更改我们的版本为家庭版配置：PLUGIN\_FEED = "HomeFeed (Non-commercial use only)" 所以我们需要手动更改两处（位置参考第一篇文章内容） plugin\_feed\_info.inc 文件内容中的 PLUGIN\_FEED 为：PLUGIN\_FEED = "ProfessionalFeed (Direct)";

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202010/thum-11f61602940761.png "点击查看原图")](https://mrxn.net/content/uploadfile/202010/11f61602940761.png)

更新完后的版本和更新的命令截图如下，仅供参考：

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202010/thum-62ff1602937152.png "点击查看原图")](https://mrxn.net/content/uploadfile/202010/62ff1602937152.png)

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202010/thum-7a831602937152.png "点击查看原图")](https://mrxn.net/content/uploadfile/202010/7a831602937152.png)

也是可以扫描的：

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202010/thum-84bd1602937575.png "点击查看原图")](https://mrxn.net/content/uploadfile/202010/84bd1602937575.png)

2020年10月15更新的
[Nessus](https://mrxn.net/tag/nessus)
插件包：all-2.0(20201015).tar.gz 下载：

https://cloud.189.cn/t/UVvauiq6vQJj（访问码：9nj9）

https://mega.nz/folder/LRFCiIAC#zIilB3PQU8nrZu4DVEIAQw

2020年10月24日更新的Nessus插件包：
all-2.0\_202010242256.tar.gz下载

https://cloud.189.cn/t/YfEZrinauqYv（访问码：le4p）

https://mega.nz/folder/LRFCiIAC#zIilB3PQU8nrZu4DVEIAQw

2020年11月10日更新Nessus插件包：all-2.0-202011100309.tar.gz下载

链接：https://cloud.189.cn/t/qAJVZjBrERfa 访问码：977y

2020年11月29日更新Nessus插件包：all-2.0\_202011270400.tar.gz下载

https://cloud.189.cn/t/ANrAJzZnU7ze（访问码：6no5）

2020年12月12日更新Nessus插件包：all-2.0\_202012111356.tar.gz下载

https://cloud.189.cn/t/yYrEJrjAF3Yn（访问码：ypk6）

2020年12月19日更新Nessus插件包：all-2.0\_202012161432.tar.gz下载

https://cloud.189.cn/t/eUZFFnmm2MFb（访问码：cl2u）

2020年12月22日更新Nessus插件包：all-2.0\_202012210107.tar.gz下载

https://cloud.189.cn/t/a2Y3i2UB7Vj2（访问码：wh4g）

2020年12月28日更新Nessus插件包：all-2.0\_202012250002.tar.gz下载

https://cloud.189.cn/t/r26NNnieAbmy（访问码：xqb4）

2020年12月29日更新Nessus插件包：all-2.0\_202012280300.tar.gz下载

https://cloud.189.cn/t/YVNjIn6nIzam（访问码：n416）

2021年01月12日更新Nessus插件包：all-2.0\_202101081846.tar.gz下载

https://cloud.189.cn/t/iY32Q3uuqYv2（访问码：qpa8）

2021年03月21日更新Nessus插件包：all-2.0\_202103152331.tar.gz下载

https://cloud.189.cn/t/zEf2MjziuaUz（访问码：f8v4）

https://mega.nz/file/bcdzQCKY#21KJVJ14immtKNhokV78FmtTG6qM\_2DOXujYi8AD2Js
  
2021年09月11日下载更新 Pro 插件，后续更新都在此文件夹更新：
  
https://mega.nz/folder/LRFCiIAC#zIilB3PQU8nrZu4DVEIAQw

更新方法不变：

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202012/thum-11f61608372626.png "点击查看原图")](https://mrxn.net/content/uploadfile/202012/11f61608372626.png)

更新成功后，不要着急！看你的任务管理器cpu占用，使用降低后，就更新成功了，再次登录即可看到更新成功的版本号：

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202012/thum-04fe1608372626.png "点击查看原图")](https://mrxn.net/content/uploadfile/202012/04fe1608372626.png)

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202012/thum-1f691608372625.png "点击查看原图")](https://mrxn.net/content/uploadfile/202012/1f691608372625.png)

测试更新于——2020/12/19日冬天

[![Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/content/uploadfile/202012/thum-24f31608650876.png "点击查看原图")](https://mrxn.net/content/uploadfile/202012/24f31608650876.png)

* 标签：
* [#
  黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#
  nessus](https://mrxn.net/tag/nessus)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[Nessus v8.9.1 系列的最新(20220407)插件更新方法说明](https://mrxn.net/jswz/504.html)
  
文章链接：
<https://mrxn.net/jswz/504.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/504.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/504.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});