---
title: "天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞"
source: https://mrxn.net/jswz/trwfe-checkDbAvailalbe-ssrf.html
asset_dir: assets/天锐绿盾审批系统-checkdbavailalbe.do-ssrf漏洞
---

# 天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/6 08:28
* 564浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

数据库

物流软件安全

VPN服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控，旨在保护企业和组织的敏感信息，防止未经授权的访问和泄漏。

漏洞修复方案

该系统的 `checkDbAvailalbe.do` 接口存在服务器端请求伪造（[SSRF](https://mrxn.net/tag/SSRF)）漏洞。此漏洞的产生是由于系统在处理用户提供的URL或相关输入时，未能进行充分的验证和过滤，导致攻击者可以操纵服务器发起任意的HTTP请求。

成功利用此[SSRF](https://mrxn.net/tag/SSRF)漏洞，攻击者可以强制服务器向任意内部或外部地址发送请求。这可能导致攻击者绕过防火墙，访问通常无法从外部网络直接访问的内部系统、服务或敏感数据。此外，攻击者还可以利用该漏洞进行内网端口扫描、资产探测，甚至发现并利用内部系统中存在的其他漏洞，从而进一步扩大攻击范围，窃取敏感信息，或在极端情况下实现远程代码执行，对企业数据安全造成严重威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

Windows安全工具

在线安全工具

编码转换工具

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全运维咨询

# 漏洞分析

先看`checkDbAvailalbe.do`的实现

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-001-c5edd048067e.webp)](https://image.mrxn.net/8d9d5ab544dd42fc8b226e0cfc395af5.webp)

参数`dbIp`, `dbPort`, `dbName`, `dbAccount`, `dbPwd`被带入`MySQLDbUtil.connectable`中，跟进看下它的实现

深入探索

漏洞扫描服务

安全研究报告

安全

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-002-2f25649c5ddb.webp)](https://image.mrxn.net/07641941ef544895a70653306a78fbe4.webp)

非常经典的jdbc链接，但是版本为mysql-connector-java-5.1.49为，已经修复了，不能反序列化利用了。不过可以进行探测内网端口开放情况，如果端口开放，则响应时间比较长，否则响应时间很短。

# 漏洞复现

存在且端口开放

漏洞修复方案

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-003-87b7955bca01.webp)](https://image.mrxn.net/f5ecace4c71645379a4ca168d038e36f.webp)

端口不存在

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-004-e7668cd3eb59.webp)](https://image.mrxn.net/2f522f0d046c4606a646d6aa5bbe0bdb.webp)

二则响应时间长短不同来判断端口开放情况。

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
文章标题：[天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](https://mrxn.net/jswz/trwfe-checkDbAvailalbe-ssrf.html)  
文章链接：<https://mrxn.net/jswz/trwfe-checkDbAvailalbe-ssrf.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKHElEQVR4AeyagXobNw6E8/f93/lOI+bfhbjQSk5sSXdlP00HHAywDLG0Hbf//Pr16z9/i//8/sc+v5c3ZK5yNVT9K3Ht0cVzr85Ttdn/aG3tI9+z+Qzk4l2fTzmBbSCXSf/6Cs7+AMAvGOh8PgeGB9hs5sKKiQPXlYGnnpX6oNYaw94jnmdgbcfP1FdP7bENpIorft8JHAYC+9sCx/g7t1rfEuNn+3d+OO4XbrXaH0bOXuGaP4vjDc48MPpDz13tYSCdaWmvO4E1kNed9VNP+taB5AoH9ckwrmvVuhiGD3ZOr6Dzd1q893Dmh/2Z+uComQvDyCf+TnzrQL5zY//WXi8bSH1zPWwYbxmw/cht7hHDqK19YWiPas3D8D/qAcMHO9vju/lnBvLdu/wX9VsD+bBhHwZSr28Xn+0fxpWuHntUzdhcuNPg2G/2wfAApra/ucOumQS2/JmWPT0De3T8qL6rOQykMy3tdSewDQT2Nwcex2dbrG8GjF7VD89pteaZ2OeeefWE9SUWapXha/uF4YfnuD5rG0gVV/y+E1gDed/Zt0/+x6v6Nzx3hv2q2nf2zGt9sNfe88RrLrGAUes6DEPTD2MNKG3f5GHXtuQlSJ/gEt79JP8dWDfk7hG/J3EYCHDzxsDt2m3CrqvJ9U1Re8Qw+tVaYxi52gOGBjvPfth/A2DuWYa9b32usX1g98FtrLcy3Hrgdn0YSC3+sPhfsZ1/4HZCTj7cnQAMf/IChqYfxhpQurl1cx3sb/JWUAL9RdpCc2Hg+pzEYjP+DmB4YOffqSvB0K0PXxOXf8HIwc4X+e4Hzn3pHdQG64bU0/iAeA3kA4ZQt3D4sbcmjXOthBrs19Fcx/prDkZtp+kPw/DB4GjCWhg5wNT1yxZwZUUYa+vCcw72L50w/LBzaoS1rjvWU7n61Ku2boin8iF8+KZe9+XkoH9LujxQW7SxdTV5pnU54HoDzN1juPXBWMN+G2otjHzV3CeMHKB03QPQ8ma6BDA8l/D0s27I6fG8PrkG8vozP33i9k39zPXs9dVXe8HxqsLQ4Mi1do5h95uDXYNj7J5g5FyH7VE5egDDD/uXts6nlhpxpsHeVx/s2rohnsqH8OlAYJ8cjNh9+zZUhuGBnc3DrnU91CrDXgP7m5qe+hLPMPeI4bY/7Otna/XBsRaOWt0rjLw9wqcDiWHhtSewBvLa8374tD8eCIzrBmwPqdfRGLj+jO668lZ4CdRh+GH/EnVJ3/3A7tdkr/Cswe5P/hnAqOm8c/94Oi16YC6c9Yw/HkgaLnz/CRwGAuNtgP0NrVN0C51mrrK+qsH+DBhxzRvDbQ7GGs73BrsPRmxP9xOG21w8cNTiDZIXMHzRAxhr2PcGu2ZdZRj5qh0GUpMrfv0JrIG8/sxPn3gYSK6f6CphXDPYufOpwe6DEZv7KruvsLUwegJK2/9JH58Arj9cwM7mtsJLoAa77yIfPrPPdRhGbWJhAxg5QOlmX4eBbK4V/M0J/HHt9uv3sw7ANkUnXnmuhaO/eqytGowacx3D8ABbafUB131uyUsAR+0iXz9wzMF9DUYOdvb5sGvX5pd/wa7BiPVXvli3z7oh21F8RnAYCIxJAqc7BK5vI7D5gKt2b/oa4eizRk8Yhg8GRxMwNNjZXGX7yl0O9h76nmX7dX5zj7jWHgbyqHjlf/YE1kB+9ny/3H0biNfmUQcY11t/2JrEgeswDH9iEU8AIweYun7JA668iU2Q+hnaYNTDzuYqw8g/q8Hww87WwlEz9xXeBvKVouX9uRPY/hMujAnXt87HdhoMPxzZunsMo6br+0gzf6/3rM9+12G9iWeYq1w9VU/c5apmDOPPDqTsgHVDDkfyXmEN5L3nf3j64W/qwPUbKvDr4L4IXr0zvti2T+fbkk2Q5wrT8zq6WuXo91B9xve893TrwrMn2hn01/Po/OuGeFIfwts3dSdX99VNsNNqzb241umpmrG5sHuS9YSTn6GvcryB3ppTS/4M+s5qa66Lu/6db90QT/tDeA3kQwbhNg7f1LtrVDULq+Z1NFf5LFd7WFO1ubbmjK0Lz/5oovOb61h/2Lz9w2pyNHGmpZ/QX3ndEE/vQ/h0IE6u26u58JyPJuZcXesJqycWZ2+Sfj1hNevD0YPEgZ57HG8Qr8g6qDVZ30P1zbE9w1396UDmZmv98ydwOhAnmGkKtY711G3r6zRzYfOJRaeZ656lv+O5LvVqla3tNHOV0yd4pJmvfVM343QgNvleXt3OTmAN5Ox03pDbBuLVeXYP+sNzTb2W5qqWmsDcPY4nMJ9YqFX2GVUzPqszF579VbN/OHqQOEgs7BF9hrnK1bMNpBpW/L4TOPwuyylXrhN0q51mrtYam7vH9tMfnjXXleObUfM+r2rGXc5eesL6zIVnzXU4NUFikZrAdTieILFYN8ST+BBeA/mQQbiN7XdZuU5BrpDQFP0Z6P8b9tnhuU+3h/hm1Dprqmb8TC4e/R3Pz846NUHnjy66/Loh3am8UdsGkskGz+4l3hnWznrWvhXhrAP94egzoj9CrdFbtTwnUNNT2Vw43qDLV804NTO6nFrluS7rbSDV+L8Y/7/seQ3kwyZ5OpBc3aDbc67XjHiDzt9ptd586oV513rCnRY9MBfOOkgc2DOcdZC8iB5EfwbWVe7qat64850OxMLFrzuBw0Dydsyok3RrnWadnkd81iO9HtUnX3ukJogusg5cV79aZfNVS31QtT+N7R+2R3qLw0A0LX7PCayBvOfc7z71MJBcpRlep7C5xELNp6iH1SpHD6pmbK/K5iqnPqiaNdFFzc/xmcdcuOsbPZh7Zh19xlkPc+HDQNJw4X0nsP36/WwLmZzQ5zqsJkcTvimuw/oesbWdL30CPWF90YVa8oHrynrD8QQ1n3VQNePU3IOeytWrnt5i3RBPpeXXi4ff9jqpr7Dbdvq11lynmQtbm1jMmuvw7KmaucrJB3UfWQdVqzXG8QSuO37Uo+aN03PGuiHd6b5RWwN54+F3j94GMl+dR+uuWafZp+Y6zWtcfWod66u5M82czw5bay4cPUgsOp85OTVCrWM9YftW3gbSFS/t9SdwGEidVhefbVF/58kbITrfnItHreunpies9iynJuj80c9gTfZ5D3rC9qpeteTFYSAmFr/nBNZA3nPud5/64wPxit7dwZTwGoetTTxjKvujZddf7RG7Hx/sOvxVTX/4xweShyzcnsDZ6i0DyVsU1I35RlYtnqBqxp3fXGpmnPnNhee6rLu+anJqRaeZ6zjPEG8ZiBtefDyBNZDjmbxVOQzEq3OPz3ZrTeepV7XLq535aq57lnl7VdavJ2zeXDh6YO4exxN0+fQJznL38oeBdE2W9roT2AaSaX8Fz24xb0LwVX9q3I+10YS5yub0V9ZXNf3mwmdaV1s14/QJXFeOLnxWzW8DqeKK33cCayDvO/v2yf8FAAD//0O8GVsAAAAGSURBVAMAUaQeqvnggzwAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-checkDbAvailalbe-ssrf.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-checkDbAvailalbe-ssrf.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 