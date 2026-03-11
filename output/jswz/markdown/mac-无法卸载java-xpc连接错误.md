---
title: "mac 无法卸载java xpc连接错误"
source: https://mrxn.net/jswz/java-update-uninstall-xpc-connection-error.html
asset_dir: assets/mac-无法卸载java-xpc连接错误
---

# mac 无法卸载java xpc连接错误

[Mrxn](https://mrxn.net/author/1)* 发表于2023/3/25 10:54
* 10808浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

控制面板

Java

Java平台


(adsbygoogle = window.adsbygoogle || []).push({});

---

## 前言

出现这个错误一半是在mac的系统设置界面里的[Java](#)选项中，打开其Java控制面板后，进行更新的时候，当下载更新后，会提示你是否删除缓存之类，然后你确认是，就会报这个错误。

Java（编程语言）

[[![mac 无法卸载java xpc连接错误](images/img-001-8b09cde031f5.png)](https://mrxn.net/content/uploadfile/202303/thum-66fb1679713213.png)](https://mrxn.net/content/uploadfile/202303/66fb1679713213.png)

## 正文

这个问题有一段时间了，只是一直没有去管他，也不影响日常使用，日常使用切换[java](#)版本都是通过jenv来搞定的。这个系统的Java只影响哪些你通过双击打开jar这类操作有影响，当然你也可以通过从终端用命令行去打开jar文件。  
碰巧今天在双击使用某个jar文件时提示更新，就去更新，然后就出现了文章开头提到的粗错误，刚好今天有时间，就将其解决了。  
首先通过搜索可以找到的相关文章不多，其中在apple社区找到了两篇文章[1](https://discussionschinese.apple.com/thread/252990563)|[2](https://discussionschinese.apple.com/thread/253957688)

第1篇没有回答，第2篇文章中提到了一个简单的删除系统自带Java版本，但不彻底。下面说下如何彻底卸载Java，迂回解决这个报错 哈哈

```
sudo rm -rf /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin
sudo rm -rf /Library/PreferencePanes/JavaControlPanel.prefPane
sudo rm -rf ~/Library/Application\ Support/Oracle/Java
```

深入探索

SQL注入防护

数据库

编码转换工具

其中第二条中的 `PreferencePanes` 和 网上和 oracle 提到的也不一样，它们的多了一个字母s: `PreferencesPanes` ,这个根据自己的路径决定吧，毕竟版本差别不一样。

软件实用程序

其次就是删除系统自带的那个旧版本

```
sudo rm -rf /Library/Java/JavaVirtualMachines/jdk*
```

然后重新去oracle下面新版dmg安装包重新安装即可。  
下载地址: <https://www.java.com/zh-CN/download/>  
卸载参考: <https://www.java.com/zh-CN/download/help/mac_uninstall_java.html>

其他参考  
<https://segmentfault.com/a/1190000042724793>  
<https://chiilabo.com/2021-10/java-update-uninstall-xpc-connection-error/>  
<https://cloud.tencent.com/developer/article/1680250>

* 标签：
* [#Java](https://mrxn.net/tag/Java)

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

* [1.前言](#toc-1-)
* [2.正文](#toc-2-)



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
文章标题：[mac 无法卸载java xpc连接错误](https://mrxn.net/jswz/java-update-uninstall-xpc-connection-error.html)  
文章链接：<https://mrxn.net/jswz/java-update-uninstall-xpc-connection-error.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows 操作系统

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/java-update-uninstall-xpc-connection-error.html"),
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

Java（编程语言）

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALD0lEQVR4Aeyc0XbcNhJEdfP//+zdcp9LgzWEZuQ41jxQZzuFrqpuQGjSGnlz8s/Hx8eP34kf9WUP6c6bb9288St17TUXd73VG1/167Pe/HcwA/l/3f2/d7mBYyD/n+7HK/Hqwe0FfMCvkBe7n7wIU2suWmcehPGqweQwKB9vAoaHa3zVr68xe7wSa90xkJW81993Aw8Dgc+fllePCtOnnxDrYXRzfeYw+o7Xd4XWNOqFc2996p3D+He6/A5h6uGMV/6HgVyZbu7v3cAfG0g/VZ3D+elovb9ldTjX6YMzDxw/A/WIMF5ze5vDWYdzrm+H3W/ne4X/YwN5ZbPb8/wG/vVAYJ4mGHRLOOf9FMHoMNh1MLx1or4rhKmBwSvPysH4unfna826ftW31jxb/+uBPNvg1r92Aw8DceqNu7b6TvoniX5RK8zTaq4OZ751fSvq2SGce8I5t27tua7h2m9d41q7rtuX/GEgIe/4vhs4BgIzdfgc+6gwficP17l1MLq5aL35qwjTD3ha0nvscuDn3y7YEM65vAjXOgwPn6N9gsdAktzx/Tfwj0/JV7GPDvMUyMN17j4wurl1Ioy+y+WtD8rtEKZnvAl9WSdgdHmYPFoCrnP9Yry/G/cb4i2+CT4MBOYpgME+JwwPg63vngx9MHX6nvHqjTB94BHb614iPNbAr9/09dkHxt+8ujyMDwbV4ZzLX+HDQK5MN/f3buAfmOnBoNMWPQqcdXmx/fJwXQfD6/tddN/gV3ukJrGri7YGnM+stquX1wdTD4PqK95vyHobb7A+BuIUPRPMFGGwefOuk99h++G6vz7x4+PjZ8vOYerh18+An8blHzAeKXvA8ObqMHznOx+Mv3XrGz/zHQPpojv/nhs4fg/Zbd/T7Bzm6YAz7vrB+NTt1whnn34YXr98EK619sL4UpOAc97+eBJw9oVbA651OPNwztce9xuy3sYbrB8+ZcF+ejkvjO5TJEZLdB4uAVOXdeKZTx1eq0vPDphaGGzdfLcXnOt2Pvs0wtRbt9NX/n5D1tt4g/XxM8Qpip4NzlNuXZ8I44dB+UYYHc646y8P1371IIwn60TvHW4NGH/7Ooezb+1xtbYepu7KEw5GBz7uN+Tjvb6OgcCvKQEPpwR+/n8EMNiGTDohn/VnoU/Uaw6f79P+1MG5Bs55PGvA5/rq/coazn09KwwPZ1QPHgP5yoa397+7geNTVqaTcKusE52HS8BMWR3OuXwjjC891oDhYXBXJw/jg1+otkMYr/rP/X/kX/6XOaP6DmH6wRnbD6PbXd0cRgfunyEfb/Z1/JEFM6WeXudw7evvC8YnD+d8x/d++hqvfM2ZN9oLrs+k3gjjh8FnfWF83ce865MfA9F04/fewMNA4DxVOOeZYmJ37Ghr7HwwffXqg2t+57PuKwif7wGj2xPOuWeBM69f1LfL5WH6APfPkI83+3r4Tf3Z+eDXNOHXup+GZ33a3zlMb/vAOZe3LgjjyTqhR4TRO483IZ91AsafdUK9Ea59MLx++DyP7+GPrJB3fN8NHAOB6+nlyUjA6FknPHLWCRhdXoTh41mjdXNR77Mcpj+g9UDgS3+7YCFM3S6Xb4Spe3b2rlvzYyArea+/7waOgTybqjqcnwK4zv2Wug7GD4OtWyeqm8PUwaB8UC+cNfl4EuYwPhiMdhX6RTj75cWPj4+fbTr/ST75xzGQJ75b/ks3cPxdFszUe6owPAyqw2u534d1ncP0ad4cRodB+4j6gjCerBN64MxHS6iL4RKdw7leXUxNAsYHg+HWaL/5ivcbst7YG6yP30NePQucpw+v5TA+n4ber3kYf/tgeBhs/Ss5TA8YtBbOufwO4doPw8MZd33C329IbuGN4hiITyhcT1O90e+l+c71NeqTh9nfXGyf+RVaA9e94MzbA6757gfjg0F1+zSqizB1MCgfPAaS5I7vv4Htpyyn3EeEx6nGA8PDYLgETG4/mBwG43kl4NoPwwOvtLn0AD9/o28RzrzfQ/s6h3Od+q4exg/cf9v78WZf9x9Z7zqQfp2Aj0Sft33q8mJqE53rF+NZQ7/6M9Qf3HmjJVoPt4a6nPkOd74db5/WzYP3G+ItvQk+/GLo05ppJTynfKP6DvW3nt5r7PTmze17hXoa3a95e7Teub6uN1dvVBfVOw9/vyHeypvg9mNvn8+nRVQ3z3QT8o365ONdQ15UM2/sfquuJtpLXL1Zty9cQr96uMSfyu2z4v2G5IbfKLY/Q3w6PKu52LxTbl1ef+fPePXG3if6rne0z6J7me/6qdvzT+Xpc78h3uqb4PEzxKdB9Hy7XF7MdBPm1jfGk9j5oiXUn+HaP3WJlcvaHlmvEW/imW6NPjG1idbNxfabq694vyHrbbzB+hhIJp3wTE4xXEI+68SzvOtTk/jx48fP/5yr9c8wNYlnvlWP/ypWz7rW65lX7WqtX8265tV3eOU/BrIruvm/ewPHQJyy2zs9+UZ98rtcXrSv+TPs/u1XD6plnTBvjJZo3rNFW6N9u9wadfPuqy7qCx4DUbzxe2/g+D3EKYqZVqKPp94Yb0K/unnjM12/PlH+M2xvzpXY1URLqHe9fGNqEvLWhUuYq7+C9xvyyi39Rc8xkEw00Xs7ZTGeNdr/LF9r13XXud+Ov9LXfllbqzdcQr4x2hrWNep5xusT3c+65qMfA0lyx/ffwPGbukdxak5xx6vr1ydv3rp8++RF6xrVr3DX0x7qYvP2VDfXJzZvLrZPvvvKr3i/IettvMH64VPW7kxOt6cv33X61M31da5PvXN560T5K2xP571H5/qbNxf1eQb5Xf4Zf78h3s6b4MNAnG5P3fO23j5zfdY1tm5doz7RPp2Ht1atMZ6EvqwTz/J4EvbLeo2v8ta6r/XBh4FovvF7buDppyyn6PE6z1QT6lkn9InhEvrkzaMlzHcYT8L6rA1r1Ha5vNj1z3h10f3sY67+FbzfkK/c1l/wHp+yeq/dlH0K9OuTN1d/FbvOftari63Hd8WtfOv2iiexy+XFeBOdh1tDfYeeZ9XvN2S9wTdYPwzEqYmecZ1i1uqiPnNRPjWJ5tXlxXgTO11+xfgTclknzEX3EOXFr/LWZa+EuX3E5juP72Egmm78nht4+JTlMTLphLmYKSbMd5jaRLwJfeES5tES5tESu1z+CtPnKvSm7xryezwra23Wqld7hlNvTO0aq36/IettvMH6+JS1Tizr3dmirbHz7fg8OYnf1a1bz9BrPY3ZNyFvnXm0hHzWa7RPTd66RnX9ovyK9xuy3sYbrI+fIU7tVXz17D4t9rXOXL1RXf8O9QV3nubjTci7t3lj6+Zi+9M70by5dfEk5IP3G5JbeKM4BuLUnmGfvf2t73Lr1POkrCEvtr/56HKN0RLyWSfMGz2HvLkov8P0Tuz0z/hjIJ+Zbu3v3cDDQHwKGr96pK7PE5OwT+vy8ayhT12Uv0I9jfZt3lxd3PHuqS7KN6q/gg8DeaXo9vx3N/CvB9JPg09Xo77mO9fnt6y+4/UF9TZGS3SPcGu0bh896s13rr95850e/l8PJE3u+HM38J8NxKfJo/bTIa9P1GeuT2zdPNg15mI8CfPGaAl59zSPlpBvjLaGde3rfK35zwbSm975azfwMJB1Wut6107PTn/1KdnVy7vPn+pn399Bz7DD7unZ5a0zX/FhIKt4r//+DRwDcWrPcHdEnwLrzXd+eX2ifKN95fXLB5szF7tWXmw9PRPyWSfMxa6Xb0xtQj7rjmMgmm783hu4B/K99/+w+/8AAAD///pg8osAAAAGSURBVAMAy8WDp9hWqwEAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/java-update-uninstall-xpc-connection-error.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 