---
title: "金和OA isCheckXml.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-isCheckXml-sqli.html
asset_dir: assets/金和oa-ischeckxml.aspx-sql注入漏洞
---

# 金和OA isCheckXml.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/18 13:31
* 227浏览
* [0评论](#comment)
* 16分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `isCheckXml.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `isCheckXml.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Groups.dll` 将其进行反编译后找到 **isCheckXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["GroupName"] != null)
    this.reqGroupName = this.Request["GroupName"].ToString().Trim();
  if (this.Request.QueryString["GroupID"] != null)
    this.groupID = this.Request.QueryString["GroupID"].ToString();
  if (string.op_Inequality(this.reqGroupName, "") && string.op_Equality(this.groupID, ""))
  {
    if (!this.m_Group.IsCheckName(this.reqGroupName))
      this.Response.Write("ok");
    else
      this.Response.Write("");
  }
  if (string.op_Inequality(this.reqGroupName, "") && string.op_Inequality(this.groupID, ""))
  {
    if (!this.m_Group.IsCheckName(this.reqGroupName, this.groupID))
      this.Response.Write("ok");
    else
      this.Response.Write("");
  }
  this.Response.End();
}
```

跟进`IsCheckName`方法

```
public bool IsCheckName(string GroupName)
{
  if (string.op_Equality(GroupName.Trim(), ""))
    return false;
  string str = $"select GroupName From UserGroup Where GroupName='{GroupName.Trim()}'";
  DataSet dataSet1 = new DataSet();
  DataSet dataSet2 = this.svr.ExecSQLReDataSet(str);
```

参数`GroupName`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.groups/isCheckXml.aspx/?GroupName=SQLI_POC&GroupID=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA isCheckXml.aspx SQL注入漏洞](images/img-001-cd536458afab.webp)](https://image.mrxn.net/749b991f015e4c5cafb176e644d0e776.webp)

成功延时 4 秒

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
文章标题：[金和OA isCheckXml.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-isCheckXml-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-isCheckXml-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-isCheckXml-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-isCheckXml-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 