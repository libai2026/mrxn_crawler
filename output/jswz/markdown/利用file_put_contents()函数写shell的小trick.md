---
title: "利用file_put_contents()函数写shell的小trick"
source: https://mrxn.net/jswz/php-file_put_contents_w-shell.html
asset_dir: assets/利用file_put_contents()函数写shell的小trick
---

# 利用file\_put\_contents()函数写shell的小trick

[Mrxn](https://mrxn.net/author/1)* 发表于2017/9/20 20:55
* 7434浏览
* [2评论](#comment)
* 10分钟阅读

深入探索

shell

脚本

脚本语言


(adsbygoogle = window.adsbygoogle || []).push({});

---

首先不了解PHP的file\_put\_contents()函数的自己去这里看一下官方给出的解释：

[http://php.net/manual/zh/function.file-put-contents.php](http://php.net/manual/zh/function.file-put-contents.php "put_file_contents()")

[[![利用file_put_contents()函数写shell的小trick](images/img-001-b3795a248dbe.png "点击查看原图")](../content/uploadfile/201709/1c6e1505914096.png)](../content/uploadfile/201709/1c6e1505914096.png)

思路大致如下：

file\_put\_contents()在写入文件时的第二个参数可以传入数组，如果是数组的话，将被连接成字符串再进行写入。在正则匹配前，传入的是一个数组。得益于PHP的弱类型特性，数组会被强制转换成字符串，也就是**Array**，**Array**肯定是满足正则**\A[ \_a-zA-Z0-9]+\z**的，所以不会被拦截。这样就可以绕过类似检测*“<?”*之类的waf。

> 下面是测试的代码：
>
> <?php  
> header("Content-type: text/html; charset=utf-8");  
> /\*  
> 测试file\_put\_contents数组写shell  
> modify:Mrxn  
> Blog:https://mrxn.net/  
>  \*/  
> echo "just a shell test!";   
> $text = $\_GET['text'];  
> if (preg\_match('[<>?]', $text)) {  
>  die('erro!');  
> }  
> echo '<br>'.'下面就是text的内容:'.'<br>';  
> echo $text;  
> echo '<br>';  
> var\_dump($text) ;  
> file\_put\_contents('config.php', $text);  
>  ?>

我们访问后,通过自己定义text可以实时得到反馈,便于测试:

技术文章订阅

[[![利用file_put_contents()函数写shell的小trick](images/img-002-545953762c4c.png "点击查看原图")](../content/uploadfile/201709/bbb71505914096.png)](../content/uploadfile/201709/bbb71505914096.png)

代码检测了写入的内容是否存在“<”“>”“?”等字符。根据上面的trick，我们可以通过传入一个数组来达到写入shell的目的。可以看到虽然有个警告。但config.php确实被写入了。<? php phpinfo(); 如下所示:[[![利用file_put_contents()函数写shell的小trick](images/img-003-34745c01a32e.png "点击查看原图")](../content/uploadfile/201709/12031505914096.png)](../content/uploadfile/201709/12031505914096.png)

注:这个不是我发现的,是在P牛的小蜜圈发现的.只是自己亲自测试了一下,将代码略作修改,便于新手理解!)\_我就是说我自己是个新手-\_- 囧| 逃 :)

我们下次再见...

ps:友情链接里面,有看到的自己帮忙加上,一个月后没有加的我就删除了.

* 标签：
* [#shell](https://mrxn.net/tag/shell)
* [#php](https://mrxn.net/tag/php)

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
文章标题：[利用file\_put\_contents()函数写shell的小trick](https://mrxn.net/jswz/php-file_put_contents_w-shell.html)  
文章链接：<https://mrxn.net/jswz/php-file_put_contents_w-shell.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/php-file\_put\_contents\_w-shell.html"),
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
text: encodeURI("https://mrxn.net/jswz/php-file\_put\_contents\_w-shell.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 