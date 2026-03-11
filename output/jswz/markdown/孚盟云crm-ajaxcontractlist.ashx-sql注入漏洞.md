---
title: "孚盟云CRM AjaxContractList.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxContractList-sqli.html
asset_dir: assets/孚盟云crm-ajaxcontractlist.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxContractList.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/16 17:03
* 571浏览
* [0评论](#comment)
* 24分钟阅读

深入探索

木马

客户关系管理

软件即服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxContractList.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxContractList.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxContractList 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["method"].ToString();
  if (!string.op_Equality(str, "moreLoad"))
  {
    if (!string.op_Equality(str, "getTitle"))
      return;
    this.getTitle(context);
  }
  else
    this.moreLoad(context);
}
```

深入探索

身份验证

软件

CRM

当 **method=getTitle** 时，进入**getTitle**方法

```
private void getTitle(HttpContext context)
{
  string ScNo = context.Request["ScNo"];
  string str1 = context.Request["type"];
  string FID = context.Request["FID"];
  string str2 = string.Empty;
  string str3 = str1;
  if (!string.op_Equality(str3, "C"))
  {
    if (!string.op_Equality(str3, "L"))
    {
      if (string.op_Equality(str3, "F"))
        str2 = this.GetFieldAttach(this.mouldId, FID);
    }
    else
      str2 = this.GetProductList(ScNo);
  }
  context.Response.Write(str2);
}
```

深入探索

服务器

数据库

鉴权

当 **type=F** 时进入 **GetFieldAttach**

SQL注入防护

```
public string GetFieldAttach(string mouldId, string FID)
{
  DataTable attachList = new CreatePageManager().GetAttachList(mouldId, FID);
  DataTable dataTable = new DataTable();
```

继续跟进 **GetAttachList**

```
public DataTable GetAttachList(string MouldID, string FID)
{
  return this.GetDataSource($" SELECT A.*,B.DocExtDescrip AS FileTypeName,C.CNEmpName AS OwnerName,\r\n        \tD.CNEmpName AS KeyInName,E.CNEmpName AS NearEditEmpName \r\n        \tFROM dcFileMouldRelation F \r\n        \tJOIN dcFile A(nolock) ON F.FileFUID = A.FUID \r\n\t      \tLEFT JOIN dcDocType B(nolock) ON upper(A.FileType)=upper(B.DocExtSign) \r\n        \tLEFT JOIN bfEMP C(nolock) ON A.OwnerID=C.EmpID \r\n        \tLEFT JOIN bfEMP D(nolock) ON A.KeyInID=D.EmpID \r\n        \tLEFT JOIN bfEMP E(nolock) ON A.NearEditEmpID=E.EmpID \r\n        \tWHERE F.MouldID = '{MouldID}'\r\n         AND F.PKFieldValue = '{FID}'\r\n        \tAND ISNULL(A.IsDeleted,0) = 0 \r\n        \tORDER BY A.KeyInDate");
}
```

最终可以看到，未经过滤或参数化绑定的参数 **MouldID** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxContractList.ashx?method=getTitle&type=F&FID=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxContractList.ashx SQL注入漏洞](images/img-001-293498727caf.webp)](https://image.mrxn.net/e4a7b5a294cd4ac7b9b46e2051af8616.webp)

通过报错注入 成功在响应回显数据版本信息

代码安全审计

以及当 **type=L** 时，进入**GetProductList**方法的**ScNo**参数的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞

[![孚盟云CRM AjaxContractList.ashx SQL注入漏洞](images/img-002-da1b780e6e7e.webp)](https://image.mrxn.net/382f788c9b794cf8acba646dacce5ace.webp)

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
文章标题：[孚盟云CRM AjaxContractList.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-AjaxContractList-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-AjaxContractList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxContractList-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxContractList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 