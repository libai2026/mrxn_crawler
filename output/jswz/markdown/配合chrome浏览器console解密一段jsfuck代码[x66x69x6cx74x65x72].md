---
title: "配合chrome浏览器console解密一段JSFuck代码[\"\x66\x69\x6c\x74\x65\x72\"]"
source: https://mrxn.net/jswz/decode-jsfuck.html
asset_dir: assets/配合chrome浏览器console解密一段jsfuck代码[x66x69x6cx74x65x72]
---

# 配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]

[Mrxn](https://mrxn.net/author/1)* 发表于2019/11/16 11:05
* 5730浏览
* [1评论](#comment)
* 23分钟阅读

深入探索

浏览器

chrome

网页浏览器


(adsbygoogle = window.adsbygoogle || []).push({});

---

在测试某个项目的时候，发现一段[JavaScript](https://mrxn.net/tag/JavaScript)代码，省略不重要的部分如下：  
  
// 原内容如下，只知道有个正则  
  
['mmh']["\x66\x69\x6c\x74\x65\x72"]["\x63\x6f\x6e\x73\x74\x72\x75\x63\x74\x6f\x72"](((['mmh'] + [])[  
  
    "\x63\x6f\x6e\x73\x74\x72\x75\x63\x74\x6f\x72"]['\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65'][  
  
    '\x61\x70\x70\x6c\x79'](null,  
  
    "33s102Y117y110O99L116H105n111u110Z40g41U123u102m117c110M99m116T105y111d110" ['\x73\x70\x6c\x69\x74'](/[a-zA-Z]{1,}/))))('mmh');  
  
// 在JavaScript中对于\x66这种开头的，\x代表这是一个16进制，直接在console里面打印出来就ok  
  
// console.log('\x66\x69\x6c\x74\x65\x72') => filter  
  
// 然后依次打印所有的类似字节即可得到如下转码后的[JavaScript](https://mrxn.net/tag/JavaScript)代码  
  
// 如果你到这里不知道如何下手的话，怎么办？搜索啊！Google搜索以下 XXXX是什么 就有结果了  
  
// 或者把全部\x66这种解密后得到的相关字符串去搜索就有结果了  
  
[[![配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]](images/img-001-7ecf5319e36e.png "点击查看原图")](https://mrxn.net/content/uploadfile/201911/61fc1573873681.png)](https://mrxn.net/content/uploadfile/201911/61fc1573873681.png)  
  
// 下面看一下jsfuck对照表，然后解密  
  
// false       =>  ![]  
  
// true        =>  !![]  
  
// undefined   =>  [][[]]  
  
// NaN         =>  +[![]]  
  
// 0           =>  +[]  
  
// 1           =>  +!+[]  
  
// 2           =>  !+[]+!+[]  
  
// 10          =>  [+!+[]]+[+[]]  
  
// Array       =>  []  
  
// Number      =>  +[]  
  
// String      =>  []+[]  
  
// Boolean     =>  ![]  
  
// Function    =>  []["filter"]  
  
// eval        =>  []["filter"]["constructor"](CODE)()  
  
// window      =>  []["filter"]["constructor"]("return this")()  
  
// 解码后的代码如下，为了节省字符，使用mrxn123代替代码中的超长字符串  
  
['mmh']["filter"]["constructor"](((['mmh'] + [])["constructor"]['fromCharCode']['apply'](null,"mrxn123"['split'](/[a-zA-Z]{1,}/))))('mmh');  
  
// 根据jsfuck对照表，我们去掉mmh，这样就是熟悉的原滋原味的jsfuck格式的代码了  
  
[]["filter"]["constructor"]((([] + [])["constructor"]['fromCharCode']['apply'](null,"mrxn123"['split'](/[a-zA-Z]{1,}/))))();  
  
// 根据eval对照[]["filter"]["constructor"](CODE)()，我们只需要把code部分代码直接console.log()出来就好  
  
console.log(((([] + [])["constructor"]['fromCharCode']['apply'](null,"mrxn123"['split'](/[a-zA-Z]{1,}/)))));  
  
// 输出：{  
  
[[![配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]](images/img-002-4ed42df0c86a.png "点击查看原图")](https://mrxn.net/content/uploadfile/201911/fcf41573873681.png)](https://mrxn.net/content/uploadfile/201911/fcf41573873681.png)  
  
// 同样的姿势将开始用mrxn123替换掉的字符串替换回去，回车，OK！JavaScript源码就出现在控制台了

[[![配合chrome浏览器console解密一段JSFuck代码["\x66\x69\x6c\x74\x65\x72"]](images/img-003-54a82761d9bd.png "点击查看原图")](https://mrxn.net/content/uploadfile/201911/8fcd1573873681.png)](https://mrxn.net/content/uploadfile/201911/8fcd1573873681.png)   
注意：上面的步骤中，替换需要去掉原内容中的空格，不然会报错。

* 标签：
* [#JavaScript](https://mrxn.net/tag/JavaScript)

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
文章标题：[配合chrome浏览器console解密一段JSFuck代码[&quot;\x66\x69\x6c\x74\x65\x72&quot;]](https://mrxn.net/jswz/decode-jsfuck.html)  
文章链接：<https://mrxn.net/jswz/decode-jsfuck.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络浏览器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/decode-jsfuck.html"),
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

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/decode-jsfuck.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 