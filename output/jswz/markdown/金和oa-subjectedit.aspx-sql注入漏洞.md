---
title: "金和OA SubjectEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/Jhsoft-Web-accept-SubjectEdit-sqli.html
asset_dir: assets/金和oa-subjectedit.aspx-sql注入漏洞
---

# 金和OA SubjectEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/30 16:26
* 691浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

网络安全会议

网页浏览器

云安全解决方案


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SubjectEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 SubjectEdit.aspx 的源码，在 bin 目录下查找 JHBase.Web.accept.dll 将其进行反编译后找到 **SubjectEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.InitText();
  this.but_Save.Text = this.QD;
  this.id = this.Request.QueryString["id"].ToString();
  if (((Control) this).Page.IsPostBack)
    return;
  this.txt_id.Text = subject.GetSubject(this.id).Rows[0]["name"].ToString();
}
```

深入探索

漏洞扫描器

安全认证考试

服务器安全服务

当不为POST请求时，参数 `id` 带入 `GetSubject` 方法中

跟进 `GetSubject` 方法

```
public static DataTable GetSubject(string id)
{
  string QueryString = $"select *  from subject where id=({id}) ";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

参数 `id` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.accept/SubjectEdit.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA SubjectEdit.aspx SQL注入漏洞](images/img-001-6b83ca4cc23b.webp)](https://image.mrxn.net/794a032295bf472abcf5ac0563b677bd.webp)

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
文章标题：[金和OA SubjectEdit.aspx SQL注入漏洞](https://mrxn.net/jswz/Jhsoft-Web-accept-SubjectEdit-sqli.html)  
文章链接：<https://mrxn.net/jswz/Jhsoft-Web-accept-SubjectEdit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Jhsoft-Web-accept-SubjectEdit-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/Jhsoft-Web-accept-SubjectEdit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 