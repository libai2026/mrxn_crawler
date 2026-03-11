---
title: "天地伟业Easy7 queryDataByTypeEx SQL注入漏洞"
source: https://mrxn.net/jswz/easy7-workbook-queryDataByTypeEx-sqli.html
asset_dir: assets/天地伟业easy7-querydatabytypeex-sql注入漏洞
---

# 天地伟业Easy7 queryDataByTypeEx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/13 08:32
* 261浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

表现层状态转换

REST

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

SQL注入防护

该系统的 /Easy7/rest/workbook/queryDataByTypeEx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意请求执行任意SQL语句，可能导致敏感信息泄露或数据库被篡改。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

深入探索

安全

软件

企业安全咨询

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

代码安全审计

再来看本次的漏洞接口 /Easy7/rest/workbook/queryDataByTypeEx 对应的 `queryDataByTypeEx()` 方法实现逻辑

```
@Controller
@RequestMapping({"/workbook"})
public class CLS_REST_WorkBook {
    @Resource(
        name = "boWorkBook"
    )
    private CLS_BO_WorkBook boWorkBook;

    @RequestMapping({"/queryDataByTypeEx"})
    public void queryDataByTypeEx(HttpServletRequest req, HttpServletResponse resp, CLS_VO_WorkBookPageEx voPage) throws IOException {
        resp.getWriter().print(JSONObject.fromObject(this.boWorkBook.queryDataByTypeEx(voPage)));
    }
```

深入探索

rest

数据库

计算机安全

参数对象`voPage`被直接带入`boWorkBook.queryDataByTypeEx`方法

```
@Transactional(
    propagation = Propagation.REQUIRED
)
public CLS_VO_Result queryDataByTypeEx(CLS_VO_WorkBookPageEx voPage) throws UnsupportedEncodingException {
    return this.daoWorkBook.queryDataByTypeEx(voPage.getTabname());
}
```

继续跟进 `daoWorkBook.queryDataByTypeEx(voPage.getTabname())`方法

[![天地伟业Easy7 queryDataByTypeEx SQL注入漏洞](images/img-001-12e241507063.webp)](https://image.mrxn.net/5014933c669a48989690e64dfd858c45.webp)

最终在dao层，参数`tabname`是未经任何过滤或校验直接拼接在SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /Easy7/rest/workbook/queryDataByTypeEx HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

tabname=TAB_WORKBOOK_TYPE SQLI_POC
```

[![天地伟业Easy7 queryDataByTypeEx SQL注入漏洞](images/img-002-fbabc42bf97f.webp)](https://image.mrxn.net/692d14e1ec034384845b6fd202394058.webp)

成功延时5秒

漏洞修复方案

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
文章标题：[天地伟业Easy7 queryDataByTypeEx SQL注入漏洞](https://mrxn.net/jswz/easy7-workbook-queryDataByTypeEx-sqli.html)  
文章链接：<https://mrxn.net/jswz/easy7-workbook-queryDataByTypeEx-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-workbook-queryDataByTypeEx-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALeklEQVR4Aeyb0XbbSA5Edef//9m7UPmSbJAtyp5MxAf6LFKNqgK63SAjJ7P55/F4fP0mvr6/rP1OF5D/KdpgVvdK79os77x7yYvyHdVF9Z7L/wRrIP/33/+7yg0sA/n/dB/vxOzgwAPW6L16nXrnIT06P/PLF0Jqa10Bye0FySEoX94Kc4heXIW8CNEhKN+xat+Jbd0ykC15rz93A7uBQKYOI/72iJA+s3qfoJneeUi/n9S964WxN4y5fcR+tlkO6QMjHvl3Azky3dzfu4F/PZD+tLybw/i0nNX1K4HUb3l7QDTzrafWP+Uh/SBYPbYx67f1vLv+1wN5d6Pb994N/PGBwPgUQfL+FJmLHvcs1ydC+sOKaiJE6727bi7qF+XFGa/+G/zjA/nNIe6a9QZ2A3HqHdeScQV5+mSfdV9fy59JzNU7QuohONM7b98j1AvpqQeSq88QRh8k/2kf+1vXUX2Lu4FsxXv9929gGQjkKYDXODui04fU99w6iG4uzvzqM4T0A3aW3nOW7wp/SADP3xF6GYSH17itWwayJe/1527gH5+an2I/MuQpsA+8zq3Xby7Ccb26aH2hXMfSKiA91SF5aRXyta6A6PLvYtX+Nu435N1b/ku+3UAgTwWM6HkgvLnoEwHRz3LrREidea+XFyF+2KMeEeKxp9h1c3Hm67x+yD4woroIow5rvhuIRTd+5gaWgUCm5PQ7ejx5GP1dNxch/llu367Li+rmW1TrqOddXh+MZ5bv+G5/SD/94rbfMpAtea8/dwPTgUCmCUGPCMc5hIcR+1PQ895XXVR/PB7PpTyM+wC7/+L5LDj4Bcba3tMSefMZQvrpFyG8dZ2HUS/fdCAl3vH3b+DHA3HK/agzvvvM9cP4lMCY6xdh1O1TOPN0vrwVnTf/KVavil5XXAUcn7n7K//xQKrojv/uBv6BTK8mWXG2FYz+qqmAY773g/g6Xz0qOg+jvzzb2Pph9MKYb7213vbZrkurgNRvtVqXVgHR4TVWTUXVVED8xfW435C6oQvF8ndZkKlBsE/OM8ubd4TUw4jWiRDdekg+07sP4ocV9djDHOI5y2H0nfWxnz6x8zD2VYc9f78h3s5FcDoQ2E+vzgzhYUSfjhlC/NVjG/q33DvrV3VwvJd9e625qA/GPuow8jDm+uxjDqNPHcIDj+lAHvfXR25g91OW0/Q0sE4P1j8Nq4sQ3yyX7whjXdfN4dzXz36WP3sf/ALZq9dD+IOSgYLRB8l7v6HoO7nfkO+LuAosP2X1A/VpmsM4bXnrYdTlZzir1991eVG9ELK3WkeIDiPqg/A9h/C1R4V6rbcB8alDcj0w5vrUC+83xFu5CC6fIZDp9XPV1Cogeq0rILn+4irMIToES6uA5N1nLpa3wnyGkH7AYqm6ColaV/S8uIrOz3Jg+H+XwJhXrwrrRRh9kLy8FfoK7zekbuFCsXyG1KQqINObnRGil7ei+4rbxpmut/vMYdzvzG9dIaQWgr0WwsOI3Ve9KuQ7llYB6VPrV2E9xA8r3m/Iq5v7gDb9DIFMrZ/J6crD6IPkEOx+62bY/eaQfr1OvfCVVjqkBwSLq+h1EB2C5amA5DCi9eWpMO9YWoV8rXvcb4i3cxFcBtInZd7PCePToQ/Cm4u9/iyH9Om+3/SDsZc9RPc4y2Hs0+tgp2t5Yu8P8UPwafr+ZRnId37Dh29g+SkLMi0I9nM55Y5w7IfwEOz9IDwEu95ziA+CXa/cs8HogeMcRt766nUU6qIec3ivn37RPoX3G1K3cKFYfsrq04JMG17ju98LjH2s6/vKw+jvPhh1WHN79JrOq8NaC+u6+81h9cC6Vhdh1QDpBYHnn/xhxfsNWa7nGovdZ4hPjegxzTuqi5Bp65OfIcSvbp0oD699+gutEYurMBchPUurkK/1NuTPcFuzXc/q9Gz1+w3Z3sYF1stnSD8L5Ol5l9fn1CH15qI+UV6E1EFQXn9HiA/o0i4Hnr9nK/Te5hAfjGjdGULqZj6Y6/cbMru1D/H3QD508bNtlw/1/rpWXtELi6vofM/LUyEP89dUzxartmLLHa3LYxzpW04f5CwQ3Hpqra/WR6Euds+M16cO+/3vN8Rbugi+/aEOmSaM6Pfh1M1h9KmL+kSIv+vwmofosKI9RYhmLva95OHYf6ZD6mBE60SIfrT//YZ4SxfB5TME5lOrszrNjqVVQOprXTHzlVahXuujgLEfjPlRjZy94bhGXX/HrpvDcb936/W96ne/Id7SRXD5DHFqZ+eCPCUQPPN3HcY6SP7u/r2fdVvsnp5D9oQRu88c4jMXIfx271qr17rCHOKHYGkV6oX3G1K3cKHYDQQyPc9YE6yA8LXeRveZi5A6cxFe89s9jta9D6QfrKjHeojWefN30X7irA6yHwT1i7DndwOZNb/5v3MD04E4xX4MyFQhqA+SQ3BW9/X19fwH/urWm3eE9IMR9VlfKCcWVzHLIT3VITkE5avHNiA6BPVBcgha03VzEeIH7n+w87jY1/TPIbBODViO7dRF4PlX2ubiUtAWEL80jPlZ/ZleffXA2BvGXN8ZQuog2P0QvvauUIdjvjyzmP6WNSu4+f/2Bk7/HOK0PQb8bOq93ryj/UXIPvrO+NK71xzGXp2H6NVjGxBev6gHXuszP6TOPvoK7zfEW7kILgOBTA2C/Xw1vW2ow+iH5BDUd4YQPwRnfs8A8cGK1sDKwfoPVeGYt66je8lD6s3PdIi/+3puv8JlIJXc8fkbWH7K6lPrOWTaMGL39dxvUR7Gekjefeai9bNcfou9Rk0exr3VITwE5UUIDyN23X3key4Pa5/7DfFWLoLLT1mQKfUpwsjPdIhv9n3BsT7rJw+pg2Dvr68Q4ql1BSS3prgKOOb1ieWtgNHf9Z5XTQWkDoL6xPL0uN8Qb+ciuHyGzM7jBNUh0+68OUTXL6rPcvmOvQ6O+1dd9xb3Krof5r23fayDYz+85mHUITlw/13W42Jfy2dIPxdkap3vT8csl+/15pD+EJSfYe8HqYM5zmrcA1Jr3v3yM9QvwtjPOvWzvHz3Z4i3dBGcfobUtCo8J2T6ECytQr3WFRAdjlH/DKtHhTqkj7lYnh5q76L1+iF7ycOYdx6iQ9A+M7S+65B64P4MeVzsa/dbFqzTApbjOl1RAXj+9xAIys+w1+vrPLzuB3vdHqK9YfSe6dbN0PoZWqduDuM5ILm+wt1ALL7xMzcw/SmrplXRjwWZKgTVy3sUXYfUdS+Eh2DX7dMR4oc9du8sn++VChh7h30MvzPA6nl8f8HKwfq3zt/yArD67jdkuZZrLJafss6eEo8780GmrK8jRLdeHUZ+pusX9R2hHhh7d95chPjNO7qX/CyXF/V3VN/i/Yb0W/pwvnyGQJ4OeA8993a6tYbUd90cRl3+twjpB+xa1HkqulBchTzw/DworkK+1tuA+NRnCMc+GHlIDiveb8jsVj/ELwPZPgmv1rNzQqasDskhaE/1jhBf589y+xZ2L4w9y1MB4SF4VjfT4bi+9qjodcVVyNe6xzIQTTd+9gZ2A4FMHUacHRPi65M2tw5GH4y5fggPQes7QnTYY/f23L3kzSG95EU45tVFiA9GVBdhru8GYtGNn7mB/2wgkKegf1sQ3qey6/Id9XV+m+vpCNkTRuw+c3tC/OZdfzfXJ9pPhOwD3H/b+7jY1x9/QyDTdvqi33fP5SF1EOz8LJcv7L3NZ1g1RwE5g3V6zGHUYcz1i71OHlJnXvjHB1JN7/j9DewG4jQ7zrbQB5m2efd3HuKHYPfDMd99r3JIDzhGayG6+Qxh9MFxDsd879vvpPTdQIq843M3sAwEMlV4jbOjHk1764X03XK1tu4My1uhD477lcfQa95RfYaQPSA4q5fvfeQ7QvpBcKsvA9mS9/pzN3AP5HN3f7jz/wAAAP///EKsowAAAAZJREFUAwBXdvWkCLQ6ngAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-workbook-queryDataByTypeEx-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 