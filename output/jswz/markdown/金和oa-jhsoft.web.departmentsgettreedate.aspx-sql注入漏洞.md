---
title: "金和OA JHSoft.Web.Departments/GetTreeDate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Departments-GetTreeDate-sqli.html
asset_dir: assets/金和oa-jhsoft.web.departmentsgettreedate.aspx-sql注入漏洞
---

# 金和OA JHSoft.Web.Departments/GetTreeDate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/8 13:31
* 198浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

数据库

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetTreeDate.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

SQL注入检测工具

Windows安全工具

技术文章订阅

根据 `GetTreeDate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Departments.dll` 将其进行反编译后找到 **GetTreeDate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Session["UserCode"] != null)
    this.strUser = this.Session["UserCode"].ToString();
  if (this.Request["id"] != null)
    this.loadDeptChild(this.Request["id"].ToString());
  else
    this.loadDate();
}
```

跟进`loadDeptChild`方法

```
public void loadDeptChild(string deptID)
{
  DataTable firstSubDeptByDeptId = new Role().GetFirstSubDeptByDeptID(deptID);
```

继续跟进`GetFirstSubDeptByDeptID`方法

```
public DataTable GetFirstSubDeptByDeptID(string deptID)
{
  DataTable firstSubDeptByDeptId = (DataTable) null;
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("select  a.DeptID, a.DeptName,case when exists(select * from dbo.department where deptparentid=a.deptid and deptdelflag=0) then 1 else 0 end as haschild ");
  stringBuilder.Append("   from dbo.Department  a left outer join dbo.Sort b on a.DeptID =b.SortObjectID  ");
  stringBuilder.Append($" where  a.deptparentid={deptID} and b.SortType = 'Dept' and a.DeptDelFlag = 0");
  stringBuilder.Append(" order by sortid ");
  try
  {
    firstSubDeptByDeptId = this.ObjDAL.ExecSQLReDataTable(stringBuilder.ToString());
```

参数`id`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.Departments/GetTreeDate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA JHSoft.Web.Departments/GetTreeDate.aspx SQL注入漏洞](images/img-001-4265fe0aa136.webp)](https://image.mrxn.net/f05b183a8b4d4dbb9340d398fd5b586b.webp)

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
文章标题：[金和OA JHSoft.Web.Departments/GetTreeDate.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-Departments-GetTreeDate-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-Departments-GetTreeDate-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Departments-GetTreeDate-sqli.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-Departments-GetTreeDate-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 