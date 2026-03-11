---
title: "金和OA GroupUserSynchState.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GroupUserSynchState-sqli.html
asset_dir: assets/金和oa-groupusersynchstate.aspx-sql注入漏洞
---

# 金和OA GroupUserSynchState.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/15 11:33
* 633浏览
* [0评论](#comment)
* 18分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GroupUserSynchState.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GroupUserSynchState.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **GroupUserSynchState** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitTxt();
  if (this.IsPostBack)
    return;
  if (this.Request.Params["UserID"] != null)
    this.strUserID = this.Request.Params["UserID"].ToString();
  string str;
  if (this.Request.Params["op"] == null || (str = this.Request.Params["op"]) == null)
    return;
  if (!string.op_Equality(str, "set"))
  {
    if (!string.op_Equality(str, "view"))
      return;
    this.InitGridView();
```

当 `op` 参数存在且等于 "**view**" 时，执行 `this.InitGridView();`

```
private void InitGridView()
{
  string str1 = "<root>{0}</root>";
  string str2 = "";
  int num = 0;
  string str3 = $"<record><SystemName ColumnName='{this.strSystemName}' Width='1.0'><![CDATA[{{0}}]]></SystemName><Flag ColumnName='成功标识'>{{1}}</Flag></record>";
  DataTable systemTableByUserId = new OpenGroup().GetUserPublishSystemTableByUserID(this.strUserID);
```

继续跟进`GetUserPublishSystemTableByUserID`方法

```
public DataTable GetUserPublishSystemTableByUserID(string UserID)
{
  string str = $"select a.*,b.System_ID, b.System_Name from outeruserrange  a inner join OuterSystem b on a.OuterSystemID = b.System_ID where a.UserID='{UserID}')";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

至此，就非常明了了，参数 `UserID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/GroupUserSynchState.aspx/?UserID=SQLI_POC&op=view HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GroupUserSynchState.aspx SQL注入漏洞](images/img-001-467d5fc72aba.webp)](https://image.mrxn.net/4b6b3c5a93d1422893f3dd48d8594d6f.webp)

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
文章标题：[金和OA GroupUserSynchState.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-GroupUserSynchState-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-GroupUserSynchState-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GroupUserSynchState-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-GroupUserSynchState-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 