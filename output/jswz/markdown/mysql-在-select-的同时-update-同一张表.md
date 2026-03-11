---
title: "MySQL 在 SELECT 的同时 UPDATE 同一张表"
source: https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html
asset_dir: assets/mysql-在-select-的同时-update-同一张表
---

# MySQL 在 SELECT 的同时 UPDATE 同一张表

[Mrxn](https://mrxn.net/author/1)* 发表于2019/4/15 22:54
* 2494浏览
* [1评论](#comment)
* 14分钟阅读

深入探索

防火墙软件

漏洞预警服务

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

MySQL 不允许 SELECT FROM 后面指向用作 UPDATE 的表，有时候让人纠结。当然，有比创建无休止的临时表更好的办法。本文解释如何 UPDATE 一张表，同时在查询子句中使用 SELECT.

编程

## 问题描述

假设我要 UPDATE 的表跟查询子句是同一张表，这样做有许多种原因，例如用统计数据更新表的字段（此时需要用 group 子句返回统计值），从某一条记录的字段 update 另一条记录，而不必使用非标准的语句，等等。举个例子：

```
create table apples(variety char(10) primary key, price int);

insert into apples values('fuji', 5), ('gala', 6);

update apples
    set price = (select price from apples where variety = 'gala')
    where variety = 'fuji';
```

错误提示是：ERROR 1093 (HY000): You can't specify target table'apples' for update in FROM clause. MySQL 手册 [UPDATE documentation](http://dev.mysql.com/doc/refman/5.0/en/update.html) 这下面有说明 : “Currently, you cannot update a table and select from the same table in a subquery.”  
  
在这个例子中，要解决问题也十分简单，但有时候不得不通过查询子句来 update 目标。好在我们有办法。

## 解决办法

既然 MySQL 是通过临时表来实现 FROM 子句里面的嵌套查询，那么把嵌套查询装进另外一个嵌套查询里，可使 FROM 子句查询和保存都是在临时表里进行，然后间接地在外围查询被引用。下面的语句是正确的：

```
update apples
   set price = (
      select price from (
         select * from apples
      ) as x
      where variety = 'gala')
   where variety = 'fuji';
```

如果你想了解更多其中的机制，请阅读 [MySQL Internals Manual](http://dev.mysql.com/doc/internals/en/select-derived.html) 相关章节。

## 没有解决的问题

一个常见的问题是，IN() 子句优化废品，被重写成相关的嵌套查询，有时（往往？）造成性能低下。把嵌套查询装进另外一个嵌套查询里并不能阻止它重写成相关嵌套，除非我下狠招。这种情况下，最好用 JOIN 重构查询（[rewrite such a query as a join](http://www.xaprb.com/blog/2006/04/30/how-to-optimize-subqueries-and-joins-in-mysql/)）。  
另一个没解决的问题是临时表被引用多次。“装进嵌套查询” 的技巧无法解决这些问题，因为它们在编译时被创建，而上面讨论的 update 问题是在运行时。（译者注：个人认为跟文章讨论的主题没几毛钱关系）  
原文地址：<http://www.xaprb.com/blog/2006/06/23/how-to-select-from-an-update-target-in-mysql/>

* 标签：
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#SQL](https://mrxn.net/tag/SQL)
* [#MySQL](https://mrxn.net/tag/MySQL)

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

* [1.
  问题描述](#toc-1-)
* [2.
  解决办法](#toc-2-)
* [3.
  没有解决的问题](#toc-3-)



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
文章标题：[MySQL 在 SELECT 的同时 UPDATE 同一张表](https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html)  
文章链接：<https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALSklEQVR4Aeybi3LbxhJEdfL//+zr1uTAQBNLUpZjsupClUlv9/TMrnaA6OH4n4+Pjx+/Ez8WH91rYdvklb91+Vb470L9DP+13Hx+rctFe8kfYfvlv4MZyM+66593uYFtID+fgo9nYnVw4AO46QGjdx2M3nvCUbdOn1xU36M5mF5yPXIRxgeDrctFGB8Mqje63yPc120D2YvX+nU3cDMQmKnDEVdHhPGZh+Ew6NPReXUYHwzqE9unDud+83u0x17LeqUndxYwe/5uHUw9DJ7tcTOQM9Ol/b0b+GMD8akR+1OA86dCv9h1jzhMX2BpBT6/vq0M7t2oH56r1/8d/GMD+c4hrtpfN/DtgfhUwfEpUncruaguwrEejtw6OOrWB+GYsya5BEweBqMl4Mij7aP7mFvp5n8Hvz2Q39n0qlnfwM1AnHrjusVJZifBPH1wHy1xXzlMnVzUd4Z6GttrXl3eCMczwJG3v7n9G9sXfjOQiFe87ga2gcBMHe5jHxXG7/RhePvMq684TH3nrWuE8QOdWnLg8F0XnPM+Q3M3gGN96zB5OEf9wW0gIVe8/gb+cepfRY9uHcz0m+uDyTf/qt960fqgmgjP7ZnaBIw/64R9RJi8XIw30TzaV+N6Q7zFN8HlQGCeBhj0vDAcBtVFONf7SWn/Kq+vEWYfuMX2yt1jxdXh2NO6Rv3PIhz7ntUtB3JmvrT//gb+gZmaW8HwfhrgqD/yd3375fpg+quL5kV1UT2o9ghh9oIjdl16JtTh6Ievcfvcw+sNuXc7L8htA4GZdp8BjjoMz5OT0A+jN4fRYTA1ifZFS8D4zO/wcxlP4pP8/BeMH/jJ5p/kzwL4/PnD3Lg/tj/llD9C60X9clFdVBfVYc4FfGwD+bg+3uIGtoH01DydeiPMVNX1w1E3L8Lk9as3bx2OdSt/6mC8MNje5nDug6NuHYwOg63Lc5aEHMYPg+p73AayF6/1625gORA4ThGGw2Amn/DoWe8DxgeD7ZPDMd86HPMw3L1gOGDpzdcE4PNrhwY4cnt1Xh3GL9cnqoswfvOieRFufcuB2OTCv3sD20BgpuX0PAYcdfMwOgzqF/XJYXwwaF6E0fWrN2/dfBCmBwxGS1gDo8uTS8BRNw+jx3MW+szBfT9MHgat3+M2EJte+NobuPltL8z0+lgwOgzup5o1jG4dDE8uoS7C5OWPEI5+GJ7eHfZSl4swtTCoD4brU5c3wrm/65qv+gDXzyEfb/ax/E+WU13ho8/DOpinSG6dHCavDsNhUF2//AxhavTCcBi0xvwn/vjx+R0Y/Pr/kmH8MKjPerF1GL/5xpVfPbgcSDe7+N+5gZvf9mZKidX2ME8BDOpLTUIOxzwMjyehL+uzMC/C1MOgNeb3COcea2Dy1qg3V4fxw6A+OHJ1ESYPR7SvqD94vSG5hTeK7bsszwTHacKRn001tXD0RbsXcO6H0bv2mX31iDC9HnEYn3vCkavbR1QXV/oqD7f7XG+It/UmuA0EZlpOWexzwvjU4cjVG+0H45eLcK6bt19z9SBMDxiMdi/u9drXtQ/O+8PoMGidCKPD4Jm+DWR/gGv9uhvYvstyWo+O0j65+KjePMxTIm+EycNg5+Xuew/hvAeMbq09RZi8XGw/jK91/Y3tkwevN6Rv68X8ZiAw0/ZcmVpCDpOPloDh5hvjSax0OK9PTcI6GB98HdMnYa9GOPZc5dVh/PL0Tsg/Pj5Ol/EkTMKxT/SbgUS84nU38PRAMtl9rI6892QN8xTAYLQEHLn9YHQYVE/NWZjfY/tgeqnDcGvU5aK6qN4I0w8GH+VhfGd9nx5Ib3Lx/+YGtoHA+dRgdDhHjwWTl4v9FMD41OHI1a0XYXxwRPN7hPHstf3aPUS474dj3jpx33u/hufqYHzA9echH2/28fB3WZ7Xp6Gx83IRZvpdB6O3D0Zvv1y//Az1wLFX63J7yEV4rl6/fRrNw/SDQfW9f/tPlskLX3sD20Ccksdprg7H6a50GJ99YDgMqjfaT4Txyxth8kCnvsz7LHJg+1NF+PUni6sNYPydt59oHsYPXF9DPt7sY3tD3uxc/7fH2QYC89p4E8BHQi7266YupiYhF60T40mYzzphXv0R6g+uvOmbMB9vIlpC/VlMzT66Lr0Tre9rsjYfr7ENxOSFr72Bm1+/O6k+ViZ6Fu3r+rOaaI/qzHc/9fRYhR6xe1inLhetE/XJV2h9o/7u077w6w3xtt4Et4FkOok+V091xdXTIyEX7dtcPTX7eKSbt98eO2ff1ldcvevUG91bvbn6M/22gVh04WtvYPvViVPtKT7L2+entdJX+610+91D97KHXrl5dbnYvhW3/qtoP+vke7zeEG/nTXAbSD8lnm8/vbP1yte63H3kjeZ7L32t6w/qaUwuYW3WCbkYLdH1zfWLnZebF9M70Vx/cBtIyBWvv4Gbn0MywcTqaMklzDttuRhPQq7vx48fn38pM7nEV/P6xe4bnr770LtCvebTI9G8fXIxNQm59c3V402YD15viLfzJrh9l5XpJDKxfUTbhznPv89lrS5G24d691HX23n19qkHzXWtejwJeWPXxbsP82pdr77yqVvX/uSvN8TbeRO8+RrS58rU9uFUxX0u69btl1xCrk8uxpMwL5oX40nI9/hsjb70Sdjjq3pqE9av0L6dVw9eb0jfzov5zUAypcTqXHkS9tE+c+mR6Hxz/Y/09qV3Qj246pFcIv5E+6Ltw7yaXFRPz4R61gnz6o3m4+24GUgXX/zv3sDDgTjNFXpc83LRJ8C8aF5Ub7S+ffKvYPd6xLu3frHP2v4Vt978vs/DgVh04d+5gZuB9PQ8hnpj5/8r7lO06h+9PdES6qKfgzyehNx8YzwJfVkn9KnLk9uHur59zvXNQExc+Job2H5Sd/t704vHvBgtIW9MLqHeT4l6PAnzWSce5eMxrBW7Vp+oT77CR326Tr/9xdatMx+83hBv5U1w+0nd82RKCbm4mu5KT4/EKm/fZzG9Es/644s/kXUi64RnEpM7C/OpSZx59lo8ib2WtX2yTjSPZlxviDfxJrh9DVlNLRNPeN6Vr/XmXZ+eidatE82L6s+gNdknseLqjalJuFfnm6986ZHQn3VC/x6vN8RbehO8Gch+Wll7zkz0XugT9crF1h9x63KWhPwMu1d7Up9Q1y+qN5pPbUKuL1pCXYyW0Neob6/fDGSfvNZ//wZuvsvyCGfTSy4TT2SdyDqx8qvHk0jNvYgnocd6Uf0MU5c4y51p8e5Dzy9t/kaA/NEZ9IndT34Przfk3u28ILd9l+X0xdVZHuWt66dEfYXP9rVe/xnq8QyiumitXFQX1e0jqov6G82L1ot7//WGeEtvgtvXEKf1LK7O77TN20/eaF40bx910byoHlQT7SEX492HumhOvsJH/Vd16ta7X/B6Q7ydN8FtIE7rEfa59atnyonWm+tfYXokzK/q1YN6G5NLqGedWHF1Md6zMN+ot3V55+XBbSCaL3ztDdwMJE/lWayO2V596vJG83kqEuazTjTXry4/Qz2invRNqK8wnoR1on65uNI7n56J9suDNwOJeMXrbuCPDSSTvxd+ij41euWdl/8O2tva5uqiZ9AnNy+udPOifRqtF83Lg39sIB7mwu/dwLcH4pQ9RqacaB4t0bq8+8hTk9D3HUyfRPdY7aW+QvuYl4vZax/qK3/y3x5Imlzx527gZiBOr/HZLa3zyZBb31xdNG+9umhevkdz1op7z9m6fd3HGn1i6yuu3n27T3w3A4l4xetuYBuI03qEq6NaZ96nQS62r3XzXd/cOvXgqra9j3j3aZ69EvZpTC7R+jN9toF08cVfcwPXQF5z78td/wcAAP//TbMhYAAAAAZJREFUAwAf0SvFry249gAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 