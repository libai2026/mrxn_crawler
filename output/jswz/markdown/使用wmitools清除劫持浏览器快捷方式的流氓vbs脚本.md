---
title: "使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本"
source: https://mrxn.net/jswz/WMITools-del_del_vbs_link.html
asset_dir: assets/使用wmitools清除劫持浏览器快捷方式的流氓vbs脚本
---

# 使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本

[Mrxn](https://mrxn.net/author/1)* 发表于2017/9/28 13:57
* 7369浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

Script

浏览器

注册表


(adsbygoogle = window.adsbygoogle || []).push({});

---

昨天无聊下载了个小游戏玩...emmmm,结果今天发现我的浏览器都被强奸了...所有的浏览器快捷方式都被添加恶心的推广链接....[[![使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本](images/img-001-4498e7f05ab7.png "点击查看原图")](../content/uploadfile/201709/54d31506578489.png)](../content/uploadfile/201709/54d31506578489.png)

> http://hao643.com/?r=ggggg&m=e19
>
> 网络浏览器

就是这个煞笔...开始以为是常规的注册表修改,使用pchunter注册表搜索常见的位置没有发现...那就Google搜索吧...发现了下面几个帖子,使用WMITools成功删除了此流氓...瞬间开心好多...估计也会有人不小心中招,在此记录一下,一是自己记性不好,备忘录.其次是万一博客读者遇到了看了这篇文章可以帮助到你们.也是一件好事.

深入探索

安全认证考试

漏洞扫描器

代码安全审计

下载WMITools:<https://pan.lanzou.com/1741009/>

然后去WMITools的安装目录,默认是:

C:\Program Files (x86)\WMI Tools\

直接以管理员的身份打开WMI Event Viewer,然后删除这个事件,取消任务栏的快捷方式,修改快捷方式里被添加的链接后,重新固定到任务栏即可...[[![使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本](images/img-002-3fb1f2607838.png "点击查看原图")](../content/uploadfile/201709/aa3c1506578489.png)](../content/uploadfile/201709/aa3c1506578489.png)[[![使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本](images/img-003-f65992f196e7.png "点击查看原图")](../content/uploadfile/201709/3fa41506578489.png)](../content/uploadfile/201709/3fa41506578489.png)

其他详细的解释请看下面的链接:

脚本语言

2008年的关于这个流氓方式的始末:<http://bbs.myhack58.com/read.php?tid-185642-uid-1515.html>

2012年一位前辈发现的这个方法:<http://blog.sina.com.cn/s/blog_8627ac3c010195ri.html>

Script Text里面就是vb[脚本](#),具体的事例可以看这里:<https://pastebin.com/x1da51N3>

到此完毕.下次见.Mrxn\_posted\_on\_mrxn.net\_2017\_09\_28

* 标签：
* [#脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)

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
文章标题：[使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本](https://mrxn.net/jswz/WMITools-del_del_vbs_link.html)  
文章链接：<https://mrxn.net/jswz/WMITools-del_del_vbs_link.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/WMITools-del\_del\_vbs\_link.html"),
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

Windows 操作系统

  

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
text: encodeURI("https://mrxn.net/jswz/WMITools-del\_del\_vbs\_link.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 