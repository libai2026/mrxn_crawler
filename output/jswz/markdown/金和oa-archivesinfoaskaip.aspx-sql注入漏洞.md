---
title: "金和OA ArchivesInfoAskAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesInfoAskAip-sqli.html
asset_dir: assets/金和oa-archivesinfoaskaip.aspx-sql注入漏洞
---

# 金和OA ArchivesInfoAskAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/10 13:25
* 1939浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

安全认证考试

编码转换工具

JSON处理工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesInfoAskAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesInfoAskAip.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesInfoAskAip** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  this.ReadLocal();
  this.GetList();
```

参数`id`被带入`GetList`方法

深入探索

Docker加速服务

安全工具开发

漏洞修复方案

```
private void GetList()
{
  DataTable archivesInfo = JHSoft.Archives.ArchivesDoc.getArchivesInfo(this.strArchID);
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
GET /c6/Jhsoft.Web.Archives/ArchivesInfoAskAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesInfoAskAip.aspx SQL注入漏洞](images/img-001-1bc62260641f.webp)](https://image.mrxn.net/5fe912f88805403ba1c2009e459c07e5.webp)

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
文章标题：[金和OA ArchivesInfoAskAip.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ArchivesInfoAskAip-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesInfoAskAip-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesInfoAskAip-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesInfoAskAip-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 