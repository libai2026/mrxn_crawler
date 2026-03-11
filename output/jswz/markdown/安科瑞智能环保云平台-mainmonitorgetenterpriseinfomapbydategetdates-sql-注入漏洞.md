---
title: "安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞"
source: https://mrxn.net/jswz/acreldny-GetEnterpriseInfoMapByDate-GetDates-sqli.html
asset_dir: assets/安科瑞智能环保云平台-mainmonitorgetenterpriseinfomapbydategetdates-sql-注入漏洞
---

# 安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/27 08:11
* 384浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

安全认证考试

网络安全会议

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

安科瑞智能环保云平台是一款用于环境监测和管理的云平台。该漏洞存在于/MainMonitor/GetEnterpriseInfoMapByDate/GetDates接口中，攻击者可以通过构造恶意的[SQL语句注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)到接口参数中，进而获取数据库信息或对数据库进行未授权操作，可能导致敏感信息泄露或数据篡改。

云存储

# 影响版本

# fofa语法

> body="myCss/phone.css" || body="/signInIcon/iconfont.css" || (body="环保用电监管云平台" && body="Acrel") || body="var ecloginname = $(\"#LoginName\").val();" || title="安科瑞环保用电"

# 漏洞分析

先看下`Global.asax`的代码引用

```
<%@ Application Codebehind="Global.asax.cs" Inherits="JuCheap.Web.MvcApplication" Language="C#" %>
```

在`bin`目录下找到`JuCheap.Web.dll`文件，反编译后找到`MvcApplication`相关实现

SQL注入检测工具

[![安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](images/img-001-cea253dd6c71.webp)](https://image.mrxn.net/4c4c933c8fc64f2f97948fc42da98229.webp)

[![安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](images/img-002-c6f2b95d164c.webp)](https://image.mrxn.net/a4c14490973142228bcb974d1e3c41b0.webp)

一个常规的`ASP`**`.`**``` NET`` MVC ```框架的架构，针对MVC架构，先看路由设置方式，打开`RouteConfig`看下路由定义

代码安全审计

深入探索

Web安全课程

物流软件安全

SQL注入防护

[![安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](images/img-003-82cdf955edc1.webp)](https://image.mrxn.net/ce4d86bbe41c4f7c9893ffe28627d754.webp)

访问模式为`{controller}/{action}/{id}`

根据漏洞通告，本次漏洞的路径为`/MainMonitor/GetEnterpriseInfoMapByDate/GetDates` 那么就可以先在controller下找到`MainMonitorController`，然后在其中找到`GetEnterpriseInfoMapByDate`的实现方式

[![安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](images/img-004-c3a929bc76b8.webp)](https://image.mrxn.net/a94424ca6d894370a0aab94da0f010aa.webp)

可以看到在方法顶部有`IgnoreRightFilter` **Attribute（特性），它的作用是告诉权限系统：“忽略权限检查”，因此这个接口是可以未授权访问。**

我们跟进Service层的**GetEnterpriseInfoMapByDate**方法看下，对传入的参数是如何处理的

漏洞修复方案

[![安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](images/img-005-c4a6ada6abf1.webp)](https://image.mrxn.net/8e1adfaf8a254e2a815bfb82723b5b03.webp)

右键在此方法上选择 转到-派生符号 或者 CTRL+F12 进入

[![安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](images/img-006-1ddedaffe024.webp)](https://image.mrxn.net/5358064bc8ae43689e3105ea56e78855.webp)

到这里就可以看到造成SQL注入漏洞原因：参数userid、tradename被直接拼接进了SQL语句中执行，但是userid在action处的定义为`this.User.Identity.GetLoginUserId();`获取不受用户可控，我们可控的只有**tradename**参数

```
    if (string.op_Inequality(tradename, "") && tradename != null)
      SQL = tradename.Contains("机关单位") || tradename.Contains("学校") ? SQL + "  and t.tradename like '%机关单位%' or  t.tradename like '%学校%' " : (tradename.Contains("一般") || tradename.Contains("普通") ? SQL + "  and t.tradename like '%普通%' " : $"{SQL}  and t.tradename like '%{tradename}%' ");
```

这段**嵌套的三元运算符**（`条件 ? 结果A : 结果B`）代码的整体逻辑流程如下：

1. **前置检查**：首先确认 `tradename` 有效（非空且非 null）。
2. **特定逻辑 A**：如果 `tradename` 是“机关单位”或“学校”，SQL 语句追加针对这两个词的 `OR` 查询。
3. **特定逻辑 B**：否则，如果 `tradename` 是“一般”或“普通”，SQL 语句强制追加针对“普通”的查询。
4. **默认逻辑**：否则，直接使用 `tradename` 的值进行模糊匹配（`LIKE %value%`）。

那我们只需要传参时使其不等于“机关单位”或“学校”、“一般”或“普通”这些即可进入like语句的模糊匹配逻辑进行[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)测试。

# 漏洞复现

```
POST /MainMonitor/GetEnterpriseInfoMapByDate/GetDates HTTP/1.1
Host: acreldny.mrxn.net
Content-Type: application/x-www-form-urlencoded

userid=admin&state=1&time=2025-02-02&tradename=SQLI_POC
```

[![安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](images/img-007-522922ab3972.webp)](https://image.mrxn.net/ca0cb5362e7446728d4de634be45be0a.webp)

成功利用报错注入，在响应回显数据库用户信息

网络安全

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
文章标题：[安科瑞智能环保云平台 /MainMonitor/GetEnterpriseInfoMapByDate/GetDates SQL 注入漏洞](https://mrxn.net/jswz/acreldny-GetEnterpriseInfoMapByDate-GetDates-sqli.html)  
文章链接：<https://mrxn.net/jswz/acreldny-GetEnterpriseInfoMapByDate-GetDates-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/acreldny-GetEnterpriseInfoMapByDate-GetDates-sqli.html"),
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

云存储

  

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
text: encodeURI("https://mrxn.net/jswz/acreldny-GetEnterpriseInfoMapByDate-GetDates-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 