---
title: "金和OA ArchivesShowSend.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowSend-sqli.html
asset_dir: assets/金和oa-archivesshowsend.aspx-sql注入漏洞
---

# 金和OA ArchivesShowSend.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/18 13:30
* 1922浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

JSON处理工具

物流软件安全

Web安全课程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowSend.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesShowSend.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowSend** 的处理逻辑

深入探索

安全

服务器安全服务

漏洞修复方案

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  if (this.Session["UserCode"] != null)
    this.strUserCode = this.Session["UserCode"].ToString();
  this.Depts = new Role(this.strUserCode, "IOA_ArchivesModify").GetRoleDepts();
  if (this.Depts.Length > 0)
    ((HtmlControl) this.btnModify).Style.Add("display", "");
  else
    ((HtmlControl) this.btnModify).Style.Add("display", "none");
  this.strDeptList = new Role(this.strUserCode, "IOA_Distribute").GetRoleDepts();
  this.ReadLocal();
  this.GetList();
```

深入探索

Web安全书籍

在线安全工具

漏洞扫描器

参数`id`被带入`GetList`方法

```
private void GetList()
{
  DataTable archivesInfo = JHSoft.Archives.ArchivesDoc.getArchivesInfo(this.strArchID);
  if (((InternalDataCollectionBase) archivesInfo.Rows).Count > 0)
```

跟进`getArchivesInfo`方法

```
public static DataTable getArchivesInfo(string archID)
{
  Page page = new Page();
  StringBuilder stringBuilder = new StringBuilder();
  if (page.GroupConfig.IsUseGroup)
    stringBuilder.Append("select ArchivesType,ArchivesTitle,[dbo].[fn_FromOuterDeptIDGetOuterSystemName](SubDeptID,ArchivesFrom) as ArchivesFrom,ArchivesKey,ArchivesWH,a.SecretID,SecretName,");
  else
    stringBuilder.Append("select ArchivesType,ArchivesTitle,ArchivesFrom,ArchivesKey,ArchivesWH,a.SecretID,SecretName,");
  stringBuilder.Append("a.ExigenceID,ExigenceName,TypeName,ArchivesFs,ArchivesBH,DeptName,SubDate,UserName,");
  stringBuilder.Append("ArchivesZsdw,ArchivesCsdw,ArchivesDate,ArchivesMan,ArchivesFj,FileName,ArchivesSource,DossID,");
  stringBuilder.Append("ArchivesGD,Field1,Field2,Field3,Field4,Field5,Field6,Field7,Field8,Field9,Field0,SubTime,AskMoney,DocID ");
  stringBuilder.Append("FROM Archives a left join Secret s on a.SecretID=s.SecretID ");
  stringBuilder.Append($"left join Exigence e on e.ExigenceID=a.ExigenceId where ArchivesID='{archID}'");
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(stringBuilder.ToString());
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesShowSend.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowSend.aspx SQL注入漏洞](images/img-001-e4ffb01c1cf3.webp)](https://image.mrxn.net/1b5163fe82e44426bfea0be68c2befcf.webp)

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
文章标题：[金和OA ArchivesShowSend.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ArchivesShowSend-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesShowSend-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesShowSend-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesShowSend-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 