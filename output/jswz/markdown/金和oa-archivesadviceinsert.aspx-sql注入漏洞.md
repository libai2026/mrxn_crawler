---
title: "金和OA ArchivesAdviceInsert.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesAdviceInsert-sqli.html
asset_dir: assets/金和oa-archivesadviceinsert.aspx-sql注入漏洞
---

# 金和OA ArchivesAdviceInsert.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/5 13:31
* 542浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

网络安全培训

在线安全工具

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesAdviceInsert.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

安全研究工具

安全研究报告

授权

根据 `ArchivesAdviceInsert.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesAdviceInsert** 的处理逻辑

```
  protected void Page_Load(object sender, EventArgs e)
  {
    this.Response.Expires = -1;
    this.ReadLocal();
    if (this.Request.QueryString["filetype"] != null)
      this.fileType = this.Request.QueryString["filetype"].ToString();
    if (this.Request.QueryString["fileid"] != null)
      this.fileID = this.Request.QueryString["fileid"].ToString();
    DataTable templet = Templet.getTemplet("9", "1");
    if (templet != null && ((InternalDataCollectionBase) templet.Rows).Count > 0)
      this.fileName = "../Resource/GovTemplet/" + templet.Rows[0]["ModelName"].ToString();
    else
      this.Response.Write("<script>alert(\"没有反馈意见模板\")</script>");
    this.JhWOC2.FileURL = this.fileName;
    this.JhWOC2.FileTransURL = "../JHSoft.Web.CustomQuery/FileDownLoad.aspx?FilePath=" + this.fileName;
    this.JhWOC2.InitializationType = JhWOC.DocumentType.doc;
    DataTable allAdvice = ArchivesAdvice.GetAllAdvice(this.fileType, this.fileID);
```

参数 `filetype`、`fileid` 被带入`GetAllAdvice`方法

```
  public static DataTable GetAllAdvice(string fileType, string fileID)
  {
    string QueryString = $"Select FileType,FileID,AdviceUserID,AdviceDetail,AdviceTime,UserName from ArchivesAdvice a,Users b where a.AdviceUserID = b.UserID and FileType like '%{fileType}%' and FileID = '{fileID}' order by AdviceTime";
    return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  }
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesAdviceInsert.aspx/?fileid=1&filetype=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesAdviceInsert.aspx SQL注入漏洞](images/img-001-3186fc9f673e.webp)](https://image.mrxn.net/e12e1c211b984e74ac25b6a9bfb9f08b.webp)

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
文章标题：[金和OA ArchivesAdviceInsert.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ArchivesAdviceInsert-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesAdviceInsert-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesAdviceInsert-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesAdviceInsert-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 