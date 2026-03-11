---
title: "彻底关闭 Firefox（火狐浏览器）的警告提示-警告：面临潜在的安全风险"
source: https://mrxn.net/jswz/disable-Firefox-warning-potential-security-risk-ahead.html
asset_dir: assets/彻底关闭-firefox（火狐浏览器）的警告提示-警告：面临潜在的安全风险
---

# 彻底关闭 Firefox（火狐浏览器）的警告提示-警告：面临潜在的安全风险

[Mrxn](https://mrxn.net/author/1)* 发表于2021/9/21 23:01
* 14883浏览
* [3评论](#comment)
* 7分钟阅读

深入探索

传输层安全性协议

Firefox

浏览器


(adsbygoogle = window.adsbygoogle || []).push({});

---

前言：

有的时候我们访问某些网站，特别是对于证书过期或者是证书和域名不符合的时候，会提示：警告：面临潜在的安全风险！

网络浏览器

[[![彻底关闭 Firefox（火狐浏览器）的警告提示-警告：面临潜在的安全风险](images/img-001-5b9eb471ac20.png "警告：面临潜在的安全风险")](https://mrxn.net/content/uploadfile/202109/37571632236838.png)](https://mrxn.net/content/uploadfile/202109/37571632236838.png)

```
Firefox 检测到潜在的安全威胁，因此没有继续访问 www.xxxx.com。若您访问此网站，攻击者可能会尝试窃取您的密码、电子邮件、信用卡等信息。

您可以做什么？

这个问题大多与网站有关，无法通过您的操作解决。您可以向此网站的管理者反馈此问题。

详细了解…

各个网站通过证书证明自己的身份。Firefox 不能信任此网站，它使用的证书对 www.xxx.com 无效。该证书只适用于下列名称： aaa.com, www.aaa.com

错误代码：SSL_ERROR_BAD_CERT_DOMAIN
```

深入探索

企业安全咨询

SQL注入防护

漏洞扫描器

这个是时候如果我们访问的网站多了，这类提示每次都去手动点开高级选项卡，再接受风险并继续，就很恼火，搜了一下，国内暂时没有搜到，就用英文搜了下，解决了，记录下。

文件大小转换

首先：在浏览器地址栏输入 about:config 打开，然后搜索如下几项，并更改：

```
security.insecure_field_warning.contextual.enabled = false
security.certerrors.permanentOverride = false
network.stricttransportsecurity.preloadlist = false
security.enterprise_roots.enabled = true
```

然后重启就生效了！，如果对于以前已经打开过的网站，可以清楚所有浏览历史记录和 cookies这些。

* 标签：
* [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)

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
文章标题：[彻底关闭 Firefox（火狐浏览器）的警告提示-警告：面临潜在的安全风险](https://mrxn.net/jswz/disable-Firefox-warning-potential-security-risk-ahead.html)  
文章链接：<https://mrxn.net/jswz/disable-Firefox-warning-potential-security-risk-ahead.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALaElEQVR4AeycgXbbOLJEdef//3netCqXBpqAJMeJrfOWOttT7KrqBowmQ8fO2X9ut9u/vxP/bj722sjbtbrfPl9Be+56qO+w1z3zqfe6z+Q1kP/81//e5QSOgfw33dsrsds4cAN28l0DjjU0uqY5cPd2Xl1UX6EemHt1rz4R4oegvAjhYUb1jn29XT7WHQMZyev6507gNBCYpw/Jf3eLsK73boFZl3e9XQ5zXfkhXK8prQKiwxrLU7GrL63imV6eMeDxeqP3NJBRvK6//wT+2kAgd4Vf0lfvKushfXsOuNT9HQT73FoLzEX5V/F361b9/9pAVotd3PMT+PJAgPsd6VLeLaL8DvXBuo91MOsw5/peQUhtXxvCv9KjPNbX9Z+KLw/kT23k6pMTOA3EqXeM/fxffSrAjf/CvCPkLoSg+q5P57tffcRXPOXvPnOxPGPIw7x3+R2OPcbrlf80kJXp4r7vBI6BQKYOj7FvDeJ38l3f5foh9fogedfN9YkQPyB1QmB6z8E6dw14rPcFYParQ3h4jPoLj4FUcsXPn8A/3hWfxVe3bl/95pC7xlxdhMe6PusL5USYe8Cc66vaCph1+Fze+1XPz8b1hHiKb4KngUDuCgj2fUJ4CHbdOwKiQ3Dnk4f4rO88RN/xEB3Qsv3JMrB8p7g2RDe3oTlElxchPAQ7b/4ITwN5ZL60v38C24F4N7gFyNQ733P98iKkXl2E8DuffEfrOz/mkN56Yc7lrdnlkDoI6hef1amLkD7mI24HMpqu6+87gX9gP63VNiB+7w5IDkFrYM71d10e4jfvPuD+5z6sffoLIZ66roA5L64CwkOwuAqY8+JWAfHBjCtvcRBf/xpLM64nxJN4Ezz+HuJ+nB5kmhCUF2HmrYfHvL7eR76jvs5D1oEzdu+uh7zY6yC9X+XtI/Y6c5j7QnLgdj0ht/f6HAOBTKlvz2lDdAjK6++5vKgOqe+8eUdY++03+uVENUgPeRHCd5/5Dq3vOsz91PWL8hC/fOExEE0X/uwJHN9l1XQqIFPr2yptDIgPgt0PMw/J7dH9O16fOqRP50uX2yGkFoI7X/VahX5I/cpTnL66rjAXi6swh/QDrnfI7c0+x3dZkCn1/UF4mLEmXKEfopuXVtFzmH2QHIL6xepRAdHrugKS6yuEcBAs3xjlWQXMfj0QHoL2Uu8I8UHwVd2+hdc7pJ/aD+end0hNaQz3N3J1Deu7oLQK6yA+CMp3rJoKeOyDWYfkcP53w7s1ap0j/q1/kD87IT1l9ZqLEB8En/nUO0Lqgesdcnuzz+kdAh/TAk7bBe4/U+pTPhkb0f0w99HefZ3v+eiH9NSzQ5h99uj+Ha9vp8vDvI51sOZLv94hdQpvFKd3yLO9Of1nvmf6rg/k7oFg72MdrPXRD/FAcNRW1xCfa+iB8ObqMPMw5/qsE3d86dcTUqfwRnF6hzg90b1Cpg9r7D5z+8C6DsJ3/7M6detGVBNH7TPXkL3ZB5JDsPfSJw+zDx7nVXc9IXUKbxSndwhkihB0r06/o7qobg6P++jbof1EfTD3lS+EaBC0Fua8vGN0nxqkzlyfuQizT37nVx/xekLG03iD6+Md4l6cZkfI9CGoX9RvDrOv6/p2vDrMfeQf1XUN1j1gzfc17CdC6sw73m63ewv5e/Lif64n5MWD+i7baSCQ6cOMbsipQ/Sed5+5CKmDNXafudjXg48+XTMX7SHKQ3p03hwe690Hs1/d9XouX3gaiOYLf+YEju+yXL6mNIa8CPP04XFuL+vFzptD+pmLEB6C9hkRZg2SQ9Be1kB4cxHCQ1B+h7D2QXiYcden+OsJqVN4ozgGApmie4M59+7qqF/eHFIPM+qD8PrFrkN88t0nP6KejpBe8mNNXcuLxVWYQ+phRvXyrkJdhNSbj3gMZCSv6587gU8PBNbThfCrO6Q4v0SIz1yEma+aMWDWex0gtUX7Afff6WyNvwSYfdb/krcAc53GXT3ED1y/Mby92efTT8ib7f//3XaOH534OEEen/pKV6Gva/KQegjqU++5vKguwtxHXrSuUE4sbgx5EdIbZrRGX89/l4esYz9Ibr/C6wmpU3ijOAYC87SconuF6DCj+mcR5j6Q3D4w56/uB7DFy2hvcVcIPPxmAKLDjL0fRJd33cJjIIoX/uwJHAOp6Yyx25aenb7jIXfFrl4e1j4I3/tbV6hW1xWQGgiqi+WpgLWur2PVVHTevLSKV3PI+sD1be/tzT7HEwIfUwKObdakKySA+5+jxY0BM7/zw+yzB8w8zLn9xF4H539KqseaZwhZE4K9vuf26zw8roe1Xv2OgVRyxc+fwDGQPmW3Bpmm+c4nD/Gbi7t6iF9d7HXyIqROX2HXIJ7Ol7dCfocw1z/zVc+KnU++PBXmIx4DGcnr+udOYPsLKsjdUZMcA8LDGvX6JUF85rfb+qrXdddOh/QHjhK94iH8ugDu78Ff6acBUg9B14HkNoQ5l3+E1xPy6HR+QDt+lgXraUJ4CHo37PYK8al3P0SHYNetEyE+8+43L4R4YcbSKuyxw/JUdB3mfju9ait2OqSPOiSvGuN6QjydN8FjIE7o2b4gU9VnXUeYfd1vDrMP5rz7ILrrQXJA6/F/XKbnEJ5cAMt3S+9jLj5pe8g7P2Rd4Pqb+u3NPscT4r4g03KazxDihxmtg/D27/jMpy72+jHXA1kTZhy9q2vrRT2QPuYd9cPat9PlRzwNpC925d97Aqe/h/TlIVOHGfU5XXMR4leH5BDUJ+oTYfZBcnXrRoTZ073mIsx+e8Gat06fCLO/+yB695uPeD0h42m8wfV2IJCp9mmbQ3S/Bvld3nn9kD4Q1Nex+9XlC+U6llYBWQOC+mDOy1uhvkNIXXkrIDkEixvjWR/g+i7r9maf42/qu33BPG2Y817nHdF5c0g9BL/qh/SBj9+HwAcHH9e7tXa8e36GkDX09X4w6/pWuP0ja2W+uL9/AsdA4PEUIXqfvluE6OYizLz1or7P5r2u6lfcyMO8F/0irPXqUQHRIWhdaWPIw9q304s/BlLJFT9/AqeBjJMer90qzFOX36E9ug6P+8CsQ3KYcewLa809iGPNK9eQvr2+5xDfKz1Hj30KTwMZjdf195/AaSCQKUPQLdX0xoDoENQHcy5vbc/hNb91ov0g9fDxXZaaXvjwwNkH0fV3tB/EZ959r+bWi2PdaSCjeF1//wlsf5a1ml5tDx7fJc/qIPUQrJ5jwJrvfeHsg3AQtK+1ojzMPvkPnK+sh7kOHudzl9v9dy6QGuA2fq4nZDyNN7g+/qbu9MXd3p7pz+p29cD9zrEe5lxetM8K9TzDVW1xkLUh2PuUpwJmvbhVWA9rP4QHrp9l3d7sc7xD4GNK8Py6fx3eGZBadVjn+vX1XP4ZQvoDz6wv630vwPLp7T4XgNkvL1oHZ9/1DvGU3gSPgTi1Z9j3rb/z5uqQu+HVXJ99dqivcOeBrA1rtA5mvXpWdL24CvmOpVV0/pX8GMgr5svz90/gNBCY7xJI/tmtwOO6uoMqYPbBnO/WhfjgjLuaWm8V+rsG6b3jrRMhfphR/RU8DeSVosvz907gywOB+W7wbupblof4u26ur+ewrtNfaI0Icw0khxl3fnkRUldrVUBy9Y7lWUX3jfmXBzI2u66/fgJ/bCDeCX1LkLsIgvog+TM/zD7re90q1yt2jzxkjVdz++jfIaQvBK0TV3V/bCAucuHXTuA0kNXUitstU1oF5C6A4M4vXzVjyItqPYf077q+QjWIt7gKeRFmvTyvBMx1kByC9nAdUR5mn3zhaSBFXvFzJ3AMBDI1eIy7rfa7oOfWwbq/ugjx7fp0H3z8JhBS2z3mHfsa5vBaH/29L6QeZtQHMw9cP+29vdnneELebF//s9v5PwAAAP//W64fCgAAAAZJREFUAwCzSbPXEbGGWQAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/disable-Firefox-warning-potential-security-risk-ahead.html"),
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
text: encodeURI("https://mrxn.net/jswz/disable-Firefox-warning-potential-security-risk-ahead.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 