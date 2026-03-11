---
title: "在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强"
source: https://mrxn.net/jswz/detect-cms-online-tools.html
asset_dir: assets/在web渗透测试中，如何快速识别目标站所使用的应用程序类别-cms指纹识别哪家强
---

# 在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强

[Mrxn](https://mrxn.net/author/1)* 发表于2019/5/10 21:42
* 10647浏览
* [2评论](#comment)
* 22分钟阅读

深入探索

漏洞扫描器

恶意软件分析工具

Web安全书籍


(adsbygoogle = window.adsbygoogle || []).push({});

---

**前言：**  
  
 在**Web**[**渗透测试**](https://mrxn.net/tag/渗透)当中的信息收集环节，对于目标站的指纹收集是很重要的一个环节，同时收集的指纹准确与否在很大程度上对我们[渗透](https://mrxn.net/tag/渗透)测试的快慢和结果有着莫大的关系，今天我就我日常使用的[**cms识别**](https://mrxn.net/tag/CMS识别)方法、国内外的常见的公开的在线cms指纹识别网站、和开源/闭源工具以及一些[扫描](https://mrxn.net/tag/扫描)器等方面来说一下如何在web渗透测试实战中快速的判断出目标站所使用的程序类型。  
  
 注：以下测试排名不分前后，其中也包括我自己的一些手动测试方法！  
  
 首先说一下针对我国的基本国情来说，因为**GFW**的存在，国外的在线网站cms指纹识别几乎对国内的**CMS**识别不出来的！故我主要讲国内的几个流行的cms指纹识别网站。  
  
 一：  
  
 名称：云悉WEB资产梳理|在线CMS指纹识别平台  
  
 官网：<http://www.yunsee.cn/>   
  
 简介：云悉安全专注于网络资产自动化梳理，cms检测**web指纹识别**，让网络资产更清晰。  
  
 简评：国内后起之秀，目前指纹特征量：6394，云溪比较全面，在识别指纹的同时会收集操作系统，服务器，web容器,数据库，程序语言等基本web信息；域名信息：备案单位，邮箱，域名所有者，备案号，DNS，域名注册商；ip信息：IDC，IP(支持查看同IP域名网站，同网段IP及域名---即C段查询)；常见子域名挖掘等功能模块，**支持API调用**，不过需要你提供指纹申请，通过了后会发放邀请码，注册就可以使用。PS:单独的指纹识别还支持**CDN**，**WAF**识别。  
  
 下图所示为我测试一个网站的时候用云溪识别的，但是没有识别出来，我用第二个即将介绍的识别出来了，第三种也没有识别出来，最后介绍手工判断出来的方法。 [[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-001-1c78e5966c79.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/8e821557497818.png)](https://mrxn.net/content/uploadfile/201905/8e821557497818.png)  
  
 二：  
  
 名称：bugscaner博客出品，在线指纹识别,在线**cms识别**小插件--在线工具  
  
 官网：<http://whatweb.bugscaner.com/look/>  
  
 简介：一款简洁快速的在线指纹,网站源码识别工具,目前已支持**2000多种**cms的识别!  
  
 简评：这个是bugscaner博主自己写的线上工具，出来的时间也比较久了，速度比较快！支持种类多，支持批量cms识别（每次最多100个，一天1000次）**支持API接口**，支持同IP网站查询，ICP备案查询等功能，博主最近又更新了这个工具，增加了几百种源码正则，增加了对https网址的识别，增加批量**cms识别**，重新优化了识别代码,减去了大部分命中率低的path路径,识别速度更快，增加通过查询历史,来统计互联网常见的cms建站系统所占使用比例,哪些cms最受欢迎,结果仅供参考,并不准确（仅通过历史查询计算）；  
  
 下图就是刚刚云溪没有识别到的，但是在这里秒识别！ [[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-002-fa090f4baef2.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/d86c1557497819.png)](https://mrxn.net/content/uploadfile/201905/d86c1557497819.png)   
  
 三：  
  
名称：TideFinger 潮汐指纹  
  
官网：<http://finger.tidesec.net/>  
  
简介：Tide 安全团队(山东新潮信息技术有限公司)出品的开源**cms指纹识别工具**  
  
简评：**开源！**但是只是后端开源，如果有需求做成web版的，需要自己又板砖实力，自己搭建前端。详细的介绍，cms指纹识别相关技术实现细节，后端源码等等在**GitHub**，地址：<https://github.com/TideSec/TideFinger>  
  
下图是同上两个图一样的网站识别结果，但是等了好久**cms信息**一直在转圈，也没有结果。。。但是其他的像网站标题,Banner，IP地址，CDN信息,操作系统,其他的信息显示还是很快的。  
  
[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-003-be58d5f5e8c5.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/5ffa1557497819.png)](https://mrxn.net/content/uploadfile/201905/5ffa1557497819.png)  
  
 四：  
  
 手工判断cms类型：   
  
下图所示是同上面三个在线cms指纹识别网站的同一个域名,通过简单的手工也可以快速识别处cms类型，看图，我们可以通过更改目标url的参数名或者参数值来进行**fuzz测试**，往往会有意想不到的记结果！这也是**fuzz**这门技术的魅力所在！  
  
通常fuzz除了一些专门的工具：  
  
<https://github.com/xmendez/wfuzz>  
  
<https://github.com/google/oss-fuzz>  
  
fuzz相关文章介绍：  
  
<https://github.com/wcventure/FuzzingPaper>  
  
<https://www.zhihu.com/question/28303982>  
  
<https://zhuanlan.zhihu.com/p/43432370>  
  
 我还推荐使用[**burpsuite**](https://mrxn.net/tag/burpsuite)配合这些工具或者是burp插件来进行fuzz测试，也很顺手！相关**burpsuite汉化**、**burpsuite**[**破解**](https://mrxn.net/tag/破解)可以在博客搜索[burp](https://mrxn.net/tag/burpsuite)关键词查看相关文章。  
  
  
  
[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-004-d623d0ef5eb1.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/b50d1557497818.png)](https://mrxn.net/content/uploadfile/201905/b50d1557497818.png)  
  
  
  
[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-005-f540fb792d65.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/0ceb1557497818.png)[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-006-5000d3b20027.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/a3631557497819.png)](https://mrxn.net/content/uploadfile/201905/a3631557497819.png)[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-007-568678fd4ef3.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/1c771557497820.png)](https://mrxn.net/content/uploadfile/201905/1c771557497820.png)  
  
  
  
[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-008-6e1031d8d221.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/673f1557497817.png)  
  
五：  
  
借助扫描器，特别是DIR扫描器这些，比如御剑，Arachni，XssPy，w3af，Nikto，OWASP ZAP，Grabber，Nmap，Netsparker，Acunetix.Web.Vulnerability.Scanner(AWS)等工具进行扫描，同时也可以使用类似JavaScript源码提取分析工具，往往能从JavaScript源码当中发现一些隐藏的子域名，文件内容等等。  
  
六：  
  
国外在线cms指纹识别网站：  
  
<https://whatcms.org>  
  
<http://cmsdetect.com/>  
  
<https://itrack.ru/whatcms/>  
  
不过由于你懂的原因，对于国内程序识别不怎么友好。

安全运维咨询

* 标签：
* [#渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
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
文章标题：[在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](https://mrxn.net/jswz/detect-cms-online-tools.html)  
文章链接：<https://mrxn.net/jswz/detect-cms-online-tools.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/detect-cms-online-tools.html"),
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

技术文章订阅

  

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
text: encodeURI("https://mrxn.net/jswz/detect-cms-online-tools.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 