---
title: "金和OA ArchivesDossierExec.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesDossierExec-sqli.html
asset_dir: assets/金和oa-archivesdossierexec.aspx-sql注入漏洞
---

# 金和OA ArchivesDossierExec.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/7 13:30
* 396浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

VPN服务

技术文章订阅

安全研究工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesDossierExec.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesDossierExec.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesDossierExec** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  string strDossID = this.Request["id"].ToString();
  if (string.op_Equality(this.Request["op"].ToString(), "closeDossier"))
    JHSoft.Archives.ArchivesDossier.CloseDoss(strDossID);
  if (string.op_Equality(this.Request["op"].ToString(), "openDossier"))
    JHSoft.Archives.ArchivesDossier.OpenDoss(strDossID);
  if (string.op_Equality(this.Request["op"].ToString(), "update"))
    this.Response.Write(JHSoft.Archives.ArchivesDossier.getDossFlg(strDossID));
  if (!string.op_Equality(this.Request["op"].ToString(), "delete"))
    return;
  this.Response.Write(JHSoft.Archives.ArchivesDossier.getUsedDossFlg(strDossID));
}
```

深入探索

安全运维咨询

企业安全咨询

Web安全课程

根据op的值进入不同的处理逻辑

代码安全审计

当`op=CloseDoss`时，参数`id`被带入`CloseDoss`方法

```
public static void CloseDoss(string strDossID)
{
  string QueryString = $"update ArchivesDossier set DossFlg=1 where DossID in ('{strDossID.Replace(",", "','")}')";
  DBOperatorFactory.GetDBOperator().ExecSQLReInt(QueryString);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

其他几个处理逻辑差不多

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-001-fcb03d225873.webp)](https://image.mrxn.net/da5f717fa75941b8a5305face0b21606.webp)

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-002-758f54d744a4.webp)](https://image.mrxn.net/5c4aa1bd228e445a82c0819850567ce0.webp)

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-003-b1cf53067374.webp)](https://image.mrxn.net/2e786b178c26457687a76c5fd2e0863f.webp)

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesDossierExec.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-004-d5d714250457.webp)](https://image.mrxn.net/97b7926cfdb849a8874d4b3c9f6748fa.webp)

成功延时 5 秒

漏洞修复方案

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
文章标题：[金和OA ArchivesDossierExec.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ArchivesDossierExec-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesDossierExec-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesDossierExec-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesDossierExec-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 