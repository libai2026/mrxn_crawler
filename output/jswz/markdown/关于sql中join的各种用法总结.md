---
title: "关于SQL中join的各种用法总结"
source: https://mrxn.net/jswz/Visual-Representation-of-SQL-Joins.html
asset_dir: assets/关于sql中join的各种用法总结
---

# 关于SQL中join的各种用法总结

[Mrxn](https://mrxn.net/author/1)* 发表于2019/4/17 20:58
* 3057浏览
* [0评论](#comment)
* 55分钟阅读

深入探索

SQL

数据库

MySQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

首先声明：文章来源于国外的 **codeproject** 我这里只是由于复习**[SQL](https://mrxn.net/tag/SQL)**的时候需要就**Google**搜索[可以用我个人搭建的[**Googl**e搜索](https://g.mrxn.net/)供大家搜索文章学习使用]了一下，找到这篇文章,再次做个简单的记录同时也方便以后的有缘人，如有侵权的地方还请来信注明，感谢原文的作者的勤劳付出，留下如此详细全面的关于**[SQL](https://mrxn.net/tag/MySQL)**的join的用法。  
  
**codeproject**是国外一个免费的可以公开自己写的代码与程序的优秀网站有点类似于**[GitHub](https://mrxn.net/tag/github)**只不过是社区版，在这个网站所有用户都可以发布自己写过的代码，程序，或者是详细的文档说明。比国内的cnblog、csdn都要好，如果要说缺点的话，就是全英文的，当然大部分还是比较容易理解的。但是**codeproject**也有中文区: <https://www.codeproject.com/Forums/1580230/General-Chinese-Topics.aspx> ,感兴趣的可以去注册玩。  
  
我们先用一张图来看一下 LEFT JOIN、RIGHT JOIN、INNER JOIN、OUTER JOIN 等七种 join 相关的用法：  
  
 [[![关于SQL中join的各种用法总结](images/img-001-1c4a15475938.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201904/69891555507304.jpg)](https://mrxn.net/content/uploadfile/201904/69891555507304.jpg)下面分开说明这七种用法，先说第一种：  
  
**`1.INNER JOIN（内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-002-91bc50373ad2.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/73071555507921.png)](https://mrxn.net/content/uploadfile/201904/73071555507921.png)这是最简单，最容易理解的Join，也是最常见的。此查询将返回左表（表A）中右表（表B）中都具有匹配记录的所有记录(共同拥有的相同的部分)。此Join用法的代码大致如下：

```
SELECT <select_list> 
FROM Table_A A
INNER JOIN Table_B B
ON A.Key = B.Key
```

**`2.LEFT JOIN（左连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-003-929394749987.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/bfdb1555508227.png)](https://mrxn.net/content/uploadfile/201904/bfdb1555508227.png)LEFT JOIN 关键字会从左表 (table\_name1) 那里返回所有的行，即使在右表 (table\_name2) 中没有匹配的行。此Join用法的代码大致如下：

```
SELECT <select_list>
FROM Table_A A
LEFT JOIN Table_B B
ON A.Key = B.Key
```

**`3.RIGHT JOIN（右连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-004-860575589443.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/28821555508227.png)](https://mrxn.net/content/uploadfile/201904/28821555508227.png)   
  
RIGHT JOIN 关键字从右表（table2）返回所有的行，即使左表（table1）中没有匹配。如果左表中没有匹配，则结果为 NULL。此Join用法的代码大致如下：

```
SELECT <select_list>
FROM Table_A A
RIGHT JOIN Table_B B
ON A.Key = B.Key
```

**`4.OUTER JOIN（外连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-005-1c19511192a3.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/de141555508227.png)](https://mrxn.net/content/uploadfile/201904/de141555508227.png)   
  
FULL OUTER JOIN 关键字只要左表（table1）和右表（table2）其中一个表中存在匹配，则返回行. FULL OUTER JOIN 关键字结合了 LEFT JOIN 和 RIGHT JOIN 的结果。此Join用法的代码大致如下：

```
SELECT <select_list>
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.Key = B.Key
```

**`5.LEFT JOIN EXCLUDING INNER JOIN（左连接-内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-006-3848e9fa3f39.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/41161555508227.png)](https://mrxn.net/content/uploadfile/201904/41161555508227.png)   
  
此查询将返回左表（表A）中与右表（表B）中的任何记录都不匹配的所有记录。此Join的编写如下：

编程

```
SELECT <select_list> 
FROM Table_A A
LEFT JOIN Table_B B
ON A.Key = B.Key
WHERE B.Key IS NULL
```

**`6.RIGHT JOIN EXCLUDING INNER JOIN（右连接-内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-007-b884fadb4576.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/bf0b1555508227.png)](https://mrxn.net/content/uploadfile/201904/bf0b1555508227.png)   
  
此查询将返回右表（表B）中与左表（表A）中的任何记录都不匹配的所有记录。此Join的编写如下：

```
SELECT <select_list>
FROM Table_A A
RIGHT JOIN Table_B B
ON A.Key = B.Key
WHERE A.Key IS NULL
```

**`7.OUTER JOIN EXCLUDING INNER JOIN（外连接-内连接）`**  
  
[[![关于SQL中join的各种用法总结](images/img-008-1173d2785ce7.png "点击查看原图")](https://mrxn.net/content/uploadfile/201904/01931555508227.png)](https://mrxn.net/content/uploadfile/201904/01931555508227.png)   
  
  
  
此查询将返回左表（表A）中的所有记录以及右表（表B）中都不匹配的所有记录。我还没有需要使用这种类型的Join，但是其他的类型，我经常使用。此Join的编写如下：

```
SELECT <select_list>
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.Key = B.Key
WHERE A.Key IS NULL OR B.Key IS NULL
```

下面举一些例子：

假设我们有两个表，Table\_A和Table\_B。这些表中的数据如下所示：  

```
TABLE_A
  PK Value
---- ----------
   1 FOX
   2 COP
   3 TAXI
   6 WASHINGTON
   7 DELL
   5 ARIZONA
   4 LINCOLN
  10 LUCENT

TABLE_B
  PK Value
---- ----------
   1 TROT
   2 CAR
   3 CAB
   6 MONUMENT
   7 PC
   8 MICROSOFT
   9 APPLE
  11 SCOTCH
```

这七种连接方式的结果如下所示：  

```
-- INNER JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
       B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
INNER JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7

(5 row(s) affected)
```

```
-- LEFT JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
LEFT JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   4 LINCOLN    NULL       NULL
   5 ARIZONA    NULL       NULL
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7
  10 LUCENT     NULL       NULL

(8 row(s) affected)
```

```
-- RIGHT JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
RIGHT JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11

(8 row(s) affected)
```

```
-- OUTER JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.PK = B.PK

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   1 FOX        TROT          1
   2 COP        CAR           2
   3 TAXI       CAB           3
   6 WASHINGTON MONUMENT      6
   7 DELL       PC            7
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11
   5 ARIZONA    NULL       NULL
   4 LINCOLN    NULL       NULL
  10 LUCENT     NULL       NULL

(11 row(s) affected)
```

```
-- LEFT EXCLUDING JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
LEFT JOIN Table_B B
ON A.PK = B.PK
WHERE B.PK IS NULL

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
   4 LINCOLN    NULL       NULL
   5 ARIZONA    NULL       NULL
  10 LUCENT     NULL       NULL
(3 row(s) affected)
```

```
-- RIGHT EXCLUDING JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
RIGHT JOIN Table_B B
ON A.PK = B.PK
WHERE A.PK IS NULL

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11

(3 row(s) affected)
```

```
-- OUTER EXCLUDING JOIN
SELECT A.PK AS A_PK, A.Value AS A_Value,
B.Value AS B_Value, B.PK AS B_PK
FROM Table_A A
FULL OUTER JOIN Table_B B
ON A.PK = B.PK
WHERE A.PK IS NULL
OR B.PK IS NULL

A_PK A_Value    B_Value    B_PK
---- ---------- ---------- ----
NULL NULL       MICROSOFT     8
NULL NULL       APPLE         9
NULL NULL       SCOTCH       11
   5 ARIZONA    NULL       NULL
   4 LINCOLN    NULL       NULL
  10 LUCENT     NULL       NULL

(6 row(s) affected)
```

注：原文连接：https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins

* 标签：
* [#编程](https://mrxn.net/tag/%E7%BC%96%E7%A8%8B)
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#SQL](https://mrxn.net/tag/SQL)
* [#MySQL](https://mrxn.net/tag/MySQL)
* [#数据库](https://mrxn.net/tag/%E6%95%B0%E6%8D%AE%E5%BA%93)

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
文章标题：[关于SQL中join的各种用法总结](https://mrxn.net/jswz/Visual-Representation-of-SQL-Joins.html)  
文章链接：<https://mrxn.net/jswz/Visual-Representation-of-SQL-Joins.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Visual-Representation-of-SQL-Joins.html"),
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

安全运维咨询

  

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
text: encodeURI("https://mrxn.net/jswz/Visual-Representation-of-SQL-Joins.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 