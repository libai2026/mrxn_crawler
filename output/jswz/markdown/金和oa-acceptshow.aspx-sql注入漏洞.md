---
title: "金和OA AcceptShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AcceptShow-sqli.html
asset_dir: assets/金和oa-acceptshow.aspx-sql注入漏洞
---

# 金和OA AcceptShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/5 08:11
* 631浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

Web安全课程

网络安全培训

网络安全会议


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AcceptShow.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 AcceptShow.aspx 的源码，在 bin 目录下查找 JHBase.Web.accept.dll 将其进行反编译后找到 `AcceptShow` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.strAppId = this.Request["appid"].ToString();
  if (this.Request["id"] == null)
    return;
  this.strAcceptID = this.Request["id"].ToString();
  this.strVersion = Paper.GetGovVersion(this.strAppId, this.strAcceptID);
```

参数 `id` 需要满足不为空 即可进入 `Paper.GetGovVersion` 方法中

跟进 `GetGovVersion` 方法

深入探索

漏洞扫描服务

授权

安全工具开发

```
public static string GetGovVersion(string strAppID, string strAppOID)
{
  string QueryString = $"select Version from JHOA_Approve_Instance where Instance_ID = (select Instance_ID from jhoa_approve where App_ID = '{strAppID}' and AppO_ID = '{strAppOID}')";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  return dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0 ? dataTable.Rows[0]["Version"].ToString() : "";
}
```

参数 `strAppID` 和 `strAppOID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.accept/AcceptShow.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

appid=SQLI_POC--/Temp/&id=-1
```

[![金和OA AcceptShow.aspx SQL注入漏洞](images/img-001-d70cbe93bdd1.webp)](https://image.mrxn.net/4b2dd2d62bc14d65a886a5db77c3dc89.webp)

成功延时 5 秒

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
文章标题：[金和OA AcceptShow.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AcceptShow-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AcceptShow-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AcceptShow-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AcceptShow-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 