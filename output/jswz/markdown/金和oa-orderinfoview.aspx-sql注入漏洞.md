---
title: "金和OA OrderInfoView.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-OrderInfoView-sqli.html
asset_dir: assets/金和oa-orderinfoview.aspx-sql注入漏洞
---

# 金和OA OrderInfoView.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/6 13:31
* 268浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

服务器

木马

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `OrderInfoView.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OrderInfoView.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CrmOrder.dll` 将其进行反编译后找到 **OrderInfoView** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Bind();
  if (this.Request["DataID"] != null)
    this.strOrderID = this.Request["DataID"].ToString();
  this.PageInit();
  this.BindOrderData(this.strOrderID);
}
```

深入探索

网络安全课程

VPN服务

网络安全会议

跟进`BindOrderData`方法

```
private void BindOrderData(string OrderID)
{
  DataSet dataSet = this.CrmOrd.ReadOrderData(OrderID);
```

跟进`ReadOrderData`方法

[![金和OA OrderInfoView.aspx SQL注入漏洞](images/img-001-5d57916b5a5c.webp)](https://image.mrxn.net/cf4f2a71c4c34432b9397ff81efa73a5.webp)

参数`DataID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CrmOrder/OrderInfoView.aspx/?DataID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA OrderInfoView.aspx SQL注入漏洞](images/img-002-e9617f698e23.webp)](https://image.mrxn.net/ac761d07de574aaf8c3fe009b984d743.webp)

成功延时 6 秒

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[金和OA OrderInfoView.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-OrderInfoView-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-OrderInfoView-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAJsUlEQVR4AeyZAXLcuA5E/fb+d96/PawnIRSkkZ3YM/XDrUUa7G6AGkKM7fifj4+Pf383/r3xX7fHjbKH5aq20yr3aFD+6LTKdbnlVZMTq/Y7eQbyX/36/11OYBvIf5P++Ex0HwD4gF+j87lP1eDXOqDKj9y64IOY/gg/B/B4psn6WMLQas1D+M0/ar87ed1uG0glV/66EzgMBMZbAz1ePWr3NsDoUzUYHOyo3vVXg92vTy0oB0efWnyGHOx+tYr6KsKoqdycw/BAj7M/68NAQq543Qmsgbzu7Nudv30gXv26u1xFGNe6+ua8+mctaxg9Oh8MLT6j+sxh+OCI1gX1J/+T8e0D+ZMP+zf0eslAYLx99YC7Nw5+9cFYw461hznsun1FPRXh6K+6uT2Ccn8av2cgf/op/6J+ayBvNuzDQHIdr+Lq+WG/+jDyzm9/GB5gs6lVBJ7+tA1sPe4mwKNv3cvaypnD8MOO+ju07gy7msNAOtPifu4EtoHAPnV4nl89Yn0jYPSqfhjcZ321h7XPOHUYe7o+Qzj6YHDuGTyrDw/DD/cwNcY2EImFrz2BNZDXnv9h939y/X435q6wX9VZy9r9kn81YOxhr6C9khswfGodwvAA268gYOesgZ2zv5rr38V1QzzRN8FbA4H9zYDz3Lej+2xwrHvmsx+M2md+GD7Yca6Bo+Y+wdmfdfg5YPSJnoCxhh3DXwUMb/XcGkgteGH+V2z95YHUN8aTgjHxqpnrqQjDD2y0/iDw+MFNMZzRcWoVr3xqMPaBHdXO0D3UXQflYO8HI1cLxpuAoQEfXx7Ix/rvW05gDeRbjvXrTf+B/bpAn9f2uWIJ2L3q4ROwazDy8Ib+ip02czB6AVsp8PhrDXbcxCaB3Tf3b+ynFOx9gFOfwt291g3xxN4Etx8MfR4nGew44PFGRjf0ifIV1YKVNw+fgNEfyPI0rKuoGXg8IyB1ibWHeVcAnPaFo2avIAy961u5dUPqabxBvgbyBkOoj7B9Ua/knRzGFYT933+u6mD3X/mutFx948p3pVkfhP2ZYOR3a2df+hmzlvUdLZ51Q3JabxTbQDKdRPdsMN4e2G9DvEZXIwej1nUQjlz4s3AfGHWwY63RV7k7uXVBGL2TG/aAoQFSGwKHL/hwzcGuw8i3gWydV/LSE1gDeenxHzc//BxytHxsv7TJFYZxtWBHa2BwroOpmSP8nYDRDwbWPtbD0GDH6jOHXYeRq9nrDOFXv3XBriZ84kqLblTfuiH1NN4gP3zbC+NtANrHc6oVgccXtK4AhgY76oMjpxZ0j+QJOPr1VIx3jqqbw+hXvbMG+zcy1QejVn9FOGq1ds5r7boh8+m8eL0G8uIBzNtfDsSrBOMKAls98PhrCvYr3fnlKtqk49SCMPZIPoe1MDzAbLm9BrbPcrvok0YYe9QyGBzseDmQWrzyT53Al82HgfjmBWFMrnaHwUU31OFc0xOc68IZas8Qxl7WVYShAZX+VF73Bx43qDZQh6HBjvrgHqc/eBhIyBWvO4HtB0MY0+wexbchqA7DDztGT8DO6a8Iuw6/5tV3lWefOWD0qjwMDo541R92v/06/x1NT7D2yDpRuXVD6mm8Qb4G8gZDqI+wDSRXJ1HFrBOVMw8/R6fJwf5XgFytl6sIew30efXbr+M6TZ9aUK4i9HsDmy21xkaWBHh8Y6AnWOQt3QayMSt56Qkc/i2rPg2MqVYuk03A0IBNBh5vwUaUJDVzFPkyta6aOg7G/nCOd3vYP1hr5hzGXpVPTaJyXQ6jNl5j3ZDupF7IrYG88PC7rbefQxRhXCPgw2uUfA61oJo9OtRzhtZUfeZcP8M8052wT7enWvCqV/RE7dHl9ojXkKv+dUM8nTfBW1/UnWTQ565TlYuecB3Ul9yIZw61ileerm+tnXP9Hc7eO2v76K3PKvcVXDfkK6f2jTVrIN94uF9pffiiXq+eudcz6CZqQTkxPiP6HGoV9dgjWPXk4Qz94Q21irNm3TO0Lmi/5IacfeSDcnqC4RPJjawTroPrhuQU3igOA8nE5nDiFatH3s/lOijXYXTDfq4rWls5/WpnaI26dRXVnqG9gnrtE87oOP0dWhc8DKQrWNzPncD2be/dqXY+uSusHylvQqLjag/1eBNVy3oO/RWtkZtrstYT7HxyHaY+kVpDn+tgPInkRud7wQ3xMRZ2J7AG0p3KC7ltILlOCa9TMOtEcsNndR2Uu8L4jM7XaR3X1crlWRPWBbOuEc6wruKVVn1Xed3PXL/rimrBbSBZrHj9CRwG0k2ucl1+52PUus5fdfPZJx9U840OynUYPZFaI+uE64rhr8I99Lg+wytf3fcwkLOGi/+ZE1gD+Zlzvr3Lpwfi1avolet2vdKqv/Yzv6qdPfF2XN1jzlOTsK5i9cYzR9WTV90+4Q1112f46YGcNVr8nzmBbSDdVK+2cOJBfcnnUKvoXhWt63xy1S93F+3f9VCrWPtaU7nqTa4nqC+5IfcMt4E8M767/v/yfGsgbzbJ7RdUuXYJr1jF7pmrbv5ZX/YzrHUdlLvqr6ei/g6f+apunmdJuA7OvaMb0eeY/VnrSW6sG+KpvAneGojTC/oWdBh9Dn3d561e9Y676mFdsPPNnOuKqTXc33Ww48J/Jc72tdetgWhe+P0nsAby/Wf8qR2+/BtDr3FFd+6uZcfpv4u1h/mz/dXdw3VQzl5BuYrhE5Wb8/QzZu1s3fnXDTk7rRfxh29763PkrfhM1No7ee3t21I5e6hVVOv8asGqJw9n1H7mahXVKqqn51noCeqpPeSiG+uGeBIt/jx5+BpSJ3g3nx+71s1aXVefb0vl9Kq5DupLbsh1qMdeFdWClTcP/yzqnldeewY737oh3am8kFsDeeHhd1tvA8kV+kx0ze5y3T5e+U7r+uqzLtj5Zi6+OWbPvHavma9rPcHKm7un66BcaoxtIDGseP0JHAbi1M7ws49sn1onV1H9itNzhr5lFfXa13XFzl/1q9y+HV7VVa3WHgZSjSv/+RNYA/n5M7/c8Y8OxKvf7VivZafL2SNojdpdtC54pya+O1F75fnOQl/V5Z7hHx3Is82WPk7g6s9vH4hvSX0IuQ6rz7zz+UbrCcp1frn4rqLzdZx7ibVn56/6Vf7tA7nafGnHE1gDOZ7JS5nDQLxuZ3jnaWtt5/ead3jlr5p7VM689pUTrTtDfR3Wmk6Xc3/XQWuTX8VhIFfmpX3/CWwDcap38erRao/O59vS4VXtldbtE67WJA83R3hj1upaT1DezxDOUHNdUa2iPYLbQKph5a87gTWQ1519u/P/AAAA//+l4K0KAAAABklEQVQDAAncNLlGbhBvAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-OrderInfoView-sqli.html"),
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

漏洞预警服务

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAJsUlEQVR4AeyZAXLcuA5E/fb+d96/PawnIRSkkZ3YM/XDrUUa7G6AGkKM7fifj4+Pf383/r3xX7fHjbKH5aq20yr3aFD+6LTKdbnlVZMTq/Y7eQbyX/36/11OYBvIf5P++Ex0HwD4gF+j87lP1eDXOqDKj9y64IOY/gg/B/B4psn6WMLQas1D+M0/ar87ed1uG0glV/66EzgMBMZbAz1ePWr3NsDoUzUYHOyo3vVXg92vTy0oB0efWnyGHOx+tYr6KsKoqdycw/BAj7M/68NAQq543Qmsgbzu7Nudv30gXv26u1xFGNe6+ua8+mctaxg9Oh8MLT6j+sxh+OCI1gX1J/+T8e0D+ZMP+zf0eslAYLx99YC7Nw5+9cFYw461hznsun1FPRXh6K+6uT2Ccn8av2cgf/op/6J+ayBvNuzDQHIdr+Lq+WG/+jDyzm9/GB5gs6lVBJ7+tA1sPe4mwKNv3cvaypnD8MOO+ju07gy7msNAOtPifu4EtoHAPnV4nl89Yn0jYPSqfhjcZ321h7XPOHUYe7o+Qzj6YHDuGTyrDw/DD/cwNcY2EImFrz2BNZDXnv9h939y/X435q6wX9VZy9r9kn81YOxhr6C9khswfGodwvAA268gYOesgZ2zv5rr38V1QzzRN8FbA4H9zYDz3Lej+2xwrHvmsx+M2md+GD7Yca6Bo+Y+wdmfdfg5YPSJnoCxhh3DXwUMb/XcGkgteGH+V2z95YHUN8aTgjHxqpnrqQjDD2y0/iDw+MFNMZzRcWoVr3xqMPaBHdXO0D3UXQflYO8HI1cLxpuAoQEfXx7Ix/rvW05gDeRbjvXrTf+B/bpAn9f2uWIJ2L3q4ROwazDy8Ib+ip02czB6AVsp8PhrDXbcxCaB3Tf3b+ynFOx9gFOfwt291g3xxN4Etx8MfR4nGew44PFGRjf0ifIV1YKVNw+fgNEfyPI0rKuoGXg8IyB1ibWHeVcAnPaFo2avIAy961u5dUPqabxBvgbyBkOoj7B9Ua/knRzGFYT933+u6mD3X/mutFx948p3pVkfhP2ZYOR3a2df+hmzlvUdLZ51Q3JabxTbQDKdRPdsMN4e2G9DvEZXIwej1nUQjlz4s3AfGHWwY63RV7k7uXVBGL2TG/aAoQFSGwKHL/hwzcGuw8i3gWydV/LSE1gDeenxHzc//BxytHxsv7TJFYZxtWBHa2BwroOpmSP8nYDRDwbWPtbD0GDH6jOHXYeRq9nrDOFXv3XBriZ84kqLblTfuiH1NN4gP3zbC+NtANrHc6oVgccXtK4AhgY76oMjpxZ0j+QJOPr1VIx3jqqbw+hXvbMG+zcy1QejVn9FOGq1ds5r7boh8+m8eL0G8uIBzNtfDsSrBOMKAls98PhrCvYr3fnlKtqk49SCMPZIPoe1MDzAbLm9BrbPcrvok0YYe9QyGBzseDmQWrzyT53Al82HgfjmBWFMrnaHwUU31OFc0xOc68IZas8Qxl7WVYShAZX+VF73Bx43qDZQh6HBjvrgHqc/eBhIyBWvO4HtB0MY0+wexbchqA7DDztGT8DO6a8Iuw6/5tV3lWefOWD0qjwMDo541R92v/06/x1NT7D2yDpRuXVD6mm8Qb4G8gZDqI+wDSRXJ1HFrBOVMw8/R6fJwf5XgFytl6sIew30efXbr+M6TZ9aUK4i9HsDmy21xkaWBHh8Y6AnWOQt3QayMSt56Qkc/i2rPg2MqVYuk03A0IBNBh5vwUaUJDVzFPkyta6aOg7G/nCOd3vYP1hr5hzGXpVPTaJyXQ6jNl5j3ZDupF7IrYG88PC7rbefQxRhXCPgw2uUfA61oJo9OtRzhtZUfeZcP8M8052wT7enWvCqV/RE7dHl9ojXkKv+dUM8nTfBW1/UnWTQ565TlYuecB3Ul9yIZw61ileerm+tnXP9Hc7eO2v76K3PKvcVXDfkK6f2jTVrIN94uF9pffiiXq+eudcz6CZqQTkxPiP6HGoV9dgjWPXk4Qz94Q21irNm3TO0Lmi/5IacfeSDcnqC4RPJjawTroPrhuQU3igOA8nE5nDiFatH3s/lOijXYXTDfq4rWls5/WpnaI26dRXVnqG9gnrtE87oOP0dWhc8DKQrWNzPncD2be/dqXY+uSusHylvQqLjag/1eBNVy3oO/RWtkZtrstYT7HxyHaY+kVpDn+tgPInkRud7wQ3xMRZ2J7AG0p3KC7ltILlOCa9TMOtEcsNndR2Uu8L4jM7XaR3X1crlWRPWBbOuEc6wruKVVn1Xed3PXL/rimrBbSBZrHj9CRwG0k2ucl1+52PUus5fdfPZJx9U840OynUYPZFaI+uE64rhr8I99Lg+wytf3fcwkLOGi/+ZE1gD+Zlzvr3Lpwfi1avolet2vdKqv/Yzv6qdPfF2XN1jzlOTsK5i9cYzR9WTV90+4Q1112f46YGcNVr8nzmBbSDdVK+2cOJBfcnnUKvoXhWt63xy1S93F+3f9VCrWPtaU7nqTa4nqC+5IfcMt4E8M767/v/yfGsgbzbJ7RdUuXYJr1jF7pmrbv5ZX/YzrHUdlLvqr6ei/g6f+apunmdJuA7OvaMb0eeY/VnrSW6sG+KpvAneGojTC/oWdBh9Dn3d561e9Y676mFdsPPNnOuKqTXc33Ww48J/Jc72tdetgWhe+P0nsAby/Wf8qR2+/BtDr3FFd+6uZcfpv4u1h/mz/dXdw3VQzl5BuYrhE5Wb8/QzZu1s3fnXDTk7rRfxh29763PkrfhM1No7ee3t21I5e6hVVOv8asGqJw9n1H7mahXVKqqn51noCeqpPeSiG+uGeBIt/jx5+BpSJ3g3nx+71s1aXVefb0vl9Kq5DupLbsh1qMdeFdWClTcP/yzqnldeewY737oh3am8kFsDeeHhd1tvA8kV+kx0ze5y3T5e+U7r+uqzLtj5Zi6+OWbPvHavma9rPcHKm7un66BcaoxtIDGseP0JHAbi1M7ws49sn1onV1H9itNzhr5lFfXa13XFzl/1q9y+HV7VVa3WHgZSjSv/+RNYA/n5M7/c8Y8OxKvf7VivZafL2SNojdpdtC54pya+O1F75fnOQl/V5Z7hHx3Is82WPk7g6s9vH4hvSX0IuQ6rz7zz+UbrCcp1frn4rqLzdZx7ibVn56/6Vf7tA7nafGnHE1gDOZ7JS5nDQLxuZ3jnaWtt5/ead3jlr5p7VM689pUTrTtDfR3Wmk6Xc3/XQWuTX8VhIFfmpX3/CWwDcap38erRao/O59vS4VXtldbtE67WJA83R3hj1upaT1DezxDOUHNdUa2iPYLbQKph5a87gTWQ1519u/P/AAAA//+l4K0KAAAABklEQVQDAAncNLlGbhBvAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-OrderInfoView-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 