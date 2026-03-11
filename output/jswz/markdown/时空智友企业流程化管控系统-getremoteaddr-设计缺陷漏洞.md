---
title: "时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞"
source: https://mrxn.net/jswz/bjskzy-getRemoteAddr-getClientIP-xff-df.html
asset_dir: assets/时空智友企业流程化管控系统-getremoteaddr-设计缺陷漏洞
---

# 时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/14 08:29
* 608浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

云安全解决方案

网络安全会议

SQL注入检测工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

时空智友企业流程化管控系统是一款基于JAVA开发的企业信息管理软件，致力于协助大健康企业构建内部信息化，解决GSP管理、多组织管理、财务管理、税控管理、线上线下一体化等问题，帮助企业实现流程化管控，提高工作效率和管理水平。时空智友企业流程化管控系统 `getRemoteAddr` 存在设计缺陷[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，攻击者可利用header头伪造访问IP。

漏洞预警服务

# 影响版本

# fofa语法

> `app="时空智友V10.1" || app="时空智友-企业信息系统" || app="时空智友-企业管理"`

# 漏洞分析

直接看 `GeneralUtility.getRemoteAddr` 方法的实现，如下

```
public static String getRemoteAddr(HttpServletRequest request) {
    if (request == null) {
        return "unknown";
    } else {
        String ip = request.getHeader("x-forwarded-for");
        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Proxy-Client-IP");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("X-Forwarded-For");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("WL-Proxy-Client-IP");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Cdn-Src-Ip");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("X-Real-IP");
        }

        if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }

        return "0:0:0:0:0:0:0:1".equals(ip) ? "127.0.0.1" : ip;
    }
}
```

执行流程如下

物流软件安全

[![时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞](images/img-001-2ac6b28d7949.webp)](https://image.mrxn.net/ff670b1a7a904b0ca68bc7897d81fed0.webp)

再找一个调用 `GeneralUtility.getRemoteAddr` 方法的地方

漏洞预警服务

```
public class UtilityServiceImpl {
    private static Logger a = LoggerFactory.getLogger(UtilityServiceImpl.class);

    public String getClientIP(HttpServletRequest var1, HttpServletResponse var2) {
        return GeneralUtility.getRemoteAddr(var1);
    }
```

# 漏洞复现

```
GET /formservice?service=utility.getClientIP HTTP/1.1
Host: bjskzy.mrxn.net
X-Forwarded-For: 127.0.0.2
```

在响应里可以看到获取到的IP就是我们header的xff伪造IP。

[![时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞](images/img-002-bae3fc0a8d00.webp)](https://image.mrxn.net/e088c6e97cbf4d18a8ec13cd37c5d527.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
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
文章标题：[时空智友企业流程化管控系统 getRemoteAddr 设计缺陷漏洞](https://mrxn.net/jswz/bjskzy-getRemoteAddr-getClientIP-xff-df.html)  
文章链接：<https://mrxn.net/jswz/bjskzy-getRemoteAddr-getClientIP-xff-df.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读

安全运维咨询


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bjskzy-getRemoteAddr-getClientIP-xff-df.html"),
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
text: encodeURI("https://mrxn.net/jswz/bjskzy-getRemoteAddr-getClientIP-xff-df.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 