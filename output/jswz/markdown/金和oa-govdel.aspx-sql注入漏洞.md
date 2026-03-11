---
title: "金和OA GovDel.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GovDel-sqli.html
asset_dir: assets/金和oa-govdel.aspx-sql注入漏洞
---

# 金和OA GovDel.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/17 13:31
* 222浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

恶意软件分析工具

代码安全审计

漏洞修复方案


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GovDel.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GovDel.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.govsetaip.dll` 将其进行反编译后找到 **GovDel** 的处理逻辑

深入探索

网络安全课程

网络安全会议

服务器安全服务

```
  protected void Page_Load(object sender, EventArgs e)
  {
    string strID = string.Empty;
    if (this.Request["strId"] != null)
      strID = this.Request["strId"].ToString().Trim();
    this.getPaperName(strID);
  }

  private void getPaperName(string strID)
  {
    DataTable delPaperName = JHSoft.GovsetAip.DelPaper.getDelPaperName(strID);
```

跟进`getDelPaperName`方法

```
public static DataTable getDelPaperName(string strid)
{
  string str = $"select SysF_Id,SysF_Name,SysFile_Type from GovPaperAip where SysF_Id in ({strid})";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

参数`strId`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.govsetaip/GovDel.aspx/?strId=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

技术文章订阅

物流软件安全

编程语言教程

[![金和OA GovDel.aspx SQL注入漏洞](images/img-001-ff2c52ba57d9.webp)](https://image.mrxn.net/5d455e883a7d44f1bded241fb5120b19.webp)

成功延时 4 秒

代码安全审计

* 标签：
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
文章标题：[金和OA GovDel.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-GovDel-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-GovDel-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GovDel-sqli.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-GovDel-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 