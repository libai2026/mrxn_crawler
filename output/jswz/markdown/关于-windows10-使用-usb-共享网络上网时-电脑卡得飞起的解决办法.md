---
title: "关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法"
source: https://mrxn.net/jswz/how-to-Improve-the-fluency-of-use-usb-sharing-network.html
asset_dir: assets/关于-windows10-使用-usb-共享网络上网时-电脑卡得飞起的解决办法
---

# 关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法

[Mrxn](https://mrxn.net/author/1)* 发表于2016/5/11 13:26
* 16513浏览
* [22评论](#comment)
* 9分钟阅读

深入探索

身份验证

代码安全审计

网络安全会议


(adsbygoogle = window.adsbygoogle || []).push({});

---

声明：以下内容来自于V2社区，个人收藏，如有侵权，还请告知，谢谢！

使用 USB 共享手机的网络时，电脑变得很卡，尤其是系统自带的应用，如打开网络与共享中心，使用 Cortana 搜索，甚至是在任何地方用系统自带输入法输入，都很卡！拔掉 USB 线之前卡掉的操作都瞬间完成了。 然而第三方软件并不受影响，比如我发这个帖子，我等了半分钟把输入法换成了手心，然后就非常顺畅的打完了字，发出来了，要使用自带输入法，特别是使用微软拼音中文状态下，大概标题还没输完。 有需要用 USB 共享网络的应该很少，不知道有没有人遇到同样的情况。我的手机是闲置的 MI4 ，当作免费的移动无线路由器

物流软件安全

系统是 win10 X64 10.0 版本是 10586 4 核 U 8G 内存 睿速 T9 256G 开机都是秒开，为毛我一插手机 USB 线，打开 USB 网络共享，电脑就卡成渣，但是 CPU 和内存都不怎么彪，这是嘛情况啊，各位有没有遇到过、、、？求解

通过搜索，说什么在设备管理中心禁用一下再启用这个网卡，可是还是没有效果.... 各位 V 友 有没有什么办法解决呢？或者是科普一下，这是什么原因！

## 解决办法：

设备管理器中，选择 usb 共享的那个网卡（一般是名字里有 NDIS 这几个字母的）， [[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-001-9cee93ba5633.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/05641462944522.png)](https://mrxn.net/content/uploadfile/201605/05641462944522.png)

深入探索

Web安全书籍

漏洞扫描服务

编程语言教程

然后右键，更新驱动程序，然后选下边那一项（从计算机设备列表中选取）  ， 

[[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-002-bbd35d4bb95a.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/4a471462944522.png)](https://mrxn.net/content/uploadfile/201605/4a471462944522.png)  
然后去掉“显示兼容设备”的对钩，[[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-003-5ad989d08405.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/10fb1462944522.png)](https://mrxn.net/content/uploadfile/201605/10fb1462944522.png)

深入探索

SQL注入防护

Windows安全工具

在线安全工具

然后在列表左边找到“ Microsoft ”，然后在右边拉到最下边，选择“远程 NDIS 兼容设备”这个，[[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-004-fd2f38f40ed0.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/09dd1462944522.png)](https://mrxn.net/content/uploadfile/201605/09dd1462944522.png)

之后确定即可。

 [[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-005-6cad39d5167b.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/82661462944522.png)](https://mrxn.net/content/uploadfile/201605/82661462944522.png)

**作者：杨晓恒**  
  
**链接：****<http://www.zhihu.com/question/35185870/answer/93712562>**  
  
**来源：知乎**  
  
**著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。**

* 标签：
* [#wifi](https://mrxn.net/tag/wifi)
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

* [1.
  解决办法：](#toc-1-)



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
文章标题：[关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](https://mrxn.net/jswz/how-to-Improve-the-fluency-of-use-usb-sharing-network.html)  
文章链接：<https://mrxn.net/jswz/how-to-Improve-the-fluency-of-use-usb-sharing-network.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/how-to-Improve-the-fluency-of-use-usb-sharing-network.html"),
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
text: encodeURI("https://mrxn.net/jswz/how-to-Improve-the-fluency-of-use-usb-sharing-network.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 