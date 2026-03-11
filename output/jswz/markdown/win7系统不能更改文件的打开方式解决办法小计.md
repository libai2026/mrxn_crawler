---
title: "win7系统不能更改文件的打开方式解决办法小计"
source: https://mrxn.net/jswz/windows-file-relevance.html
asset_dir: assets/win7系统不能更改文件的打开方式解决办法小计
---

# win7系统不能更改文件的打开方式解决办法小计

[Mrxn](https://mrxn.net/author/1)* 发表于2016/2/15 15:37
* 5822浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

漏洞预警服务

防火墙软件

Docker加速服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

不知道大家有没有发现用WIN7时会出现“打开方式”无法添加这个问题，也就是你想对某个类型的文件（比如txt/php文件）更改或者是添加一种打开方式的时候不能添加/更改。我最近更新了sublimetext 3，是软件它提示我更新的，我就直接点击update-download，结果就出了这悲剧。。。想要更改php文件的打开方式为sublime时，死活添加不了：右击文件->选属性->选择“更改”->选"浏览"->找到sublime\_text.exe，之后就没任何反应，在 其他程序框下面也没有，压根儿就没有添加进去；然后又在控制面板里的"默认程序”的“将文件类型或协议与程序关联”，结果也一样，压根儿就没法添加呀！  
后来搜索知道原因大概是，windows文件关联的问题，和系统32/64无关。以前版本的sublime变换了路径一样会出问题，解决方法很简单：

在注册表里搜索sublime\_text.exe，确认每一个键值都指向最新的sublime\_text文件即可。”

物流软件安全

对注册表修改不熟的可看下面具体操作：

具体操作：1、按win键+R，出现“运行”，在对话框内打regedit,进入注册表，

               2、在注册表上菜单栏中，进入“编辑”－“查找”，打sublime\_text，回车

               3、在注册表右侧栏中，查看sublime\_text的路径是否是现在软件安装盘下的路径，不是的话点右键“修改”，将路径改为现在安装盘下的路径

               4、“编辑”－“查找下一个”，重复第三步，直至查找全部结束，退出注册表

完成以上，再右键-文件“打开方式”，看是否有sublimetext？不出意外应该有了。

深入探索

安全研究报告

安全认证考试

代码安全审计

还有一种更简单的方法，就是把软件的文件名修改一下，再去添加关联就可以了！！！只是这种方法会让快捷方式失效，需要我们自己修改一下快捷方式的目标文件名。

PS: win7这bug真特么逗！

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
文章标题：[win7系统不能更改文件的打开方式解决办法小计](https://mrxn.net/jswz/windows-file-relevance.html)  
文章链接：<https://mrxn.net/jswz/windows-file-relevance.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/windows-file-relevance.html"),
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
text: encodeURI("https://mrxn.net/jswz/windows-file-relevance.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 