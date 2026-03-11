---
title: "解决AMD双显卡win10开机黑屏很久，关闭ULPS"
source: https://mrxn.net/jswz/Disable-AMD-ULPS-to-improve-win10-openspeed.html
asset_dir: assets/解决amd双显卡win10开机黑屏很久，关闭ulps
---

# 解决AMD双显卡win10开机黑屏很久，关闭ULPS

[Mrxn](https://mrxn.net/author/1)* 发表于2016/12/7 13:46
* 8628浏览
* [1评论](#comment)
* 17分钟阅读

深入探索

桌面

显卡

SSD


(adsbygoogle = window.adsbygoogle || []).push({});

---

我的本本加了个256的[SSD](#)，一直用的win10 速度速度都还可以的，但是前两天自动更新后（AMD），我就发现电脑开机特别慢啊，之前都是几秒钟就到了刷指纹的界面，手指一扫就到桌面了，农企给我自动更新后，开机就要黑屏几十秒。。。。一开始还以为电脑中毒了，系统坏了啥的。。。折腾就不说了。

声卡与显卡

后来在搜索到了一些百度经验的文章，很多都没用。。。。其中有两篇说的就是按摩店（AMD）的双[显卡](#)，win10升级后开机慢。果然，禁用ulps后，开机立马好了，终于恢复了几秒钟！

### 注：这个方法只适用于双AND显卡的电脑哈，其他的没有测试，你也没有ulps这个东西，哈哈。

下面说一下方法哈：

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0000]
"EnableULPS"=dword:00000000

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0001]
"EnableULPS"=dword:00000000
```

把上面这段代码保存为后缀为reg的格式，比如ULPS\_Disable.reg 双击导入注册表，重启即可测试效果。

计算机驱动器和存储设备

下面这段代码就是开启ulps的，使用方法同上：

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0000]
"EnableULPS"=dword:00000001

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0001]
"EnableULPS"=dword:00000001
```

深入探索

恶意软件分析工具

安全认证考试

Web安全书籍

这是作者原话：

```
This zip contains two files:

ULPS_Disable.reg
ULPS_Enable.reg

Basically it will just change the value of "EnableUlps" in the registry from "0" (disable) or "1" (enable) at locations:
[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\[b]0000[/b]]
[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\[b]0001[/b]]

Double click the one you want and reboot your computer.

ULPS stands for "Ultra Low Power State".

Disabling it allows your system to overclock. Specific drivers may still be required.

 -HTWingNut
```

深入探索

服务器安全服务

VPN服务

技术文章订阅

百度经验的很多链接失效了，我通过搜索作者的名字，找到了他的网盘，哈哈，然后找到了这个，其实没有找到之前，我也解决了，自己手动搜索注册表修改一样的。不过有上面这两个脚本还是快多了啊！so,分享在这里，以方便有需要的朋友。

计算机硬件

* 标签：
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#windows](https://mrxn.net/tag/windows)
* [#注册表](https://mrxn.net/tag/%E6%B3%A8%E5%86%8C%E8%A1%A8)

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

* [1.
  注：这个方法只适用于双AND显卡的电脑哈，其他的没有测试，你也没有ulps这个东西，哈哈。](#toc-1-)



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
文章标题：[解决AMD双显卡win10开机黑屏很久，关闭ULPS](https://mrxn.net/jswz/Disable-AMD-ULPS-to-improve-win10-openspeed.html)  
文章链接：<https://mrxn.net/jswz/Disable-AMD-ULPS-to-improve-win10-openspeed.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Disable-AMD-ULPS-to-improve-win10-openspeed.html"),
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

台式机

  

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
text: encodeURI("https://mrxn.net/jswz/Disable-AMD-ULPS-to-improve-win10-openspeed.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 