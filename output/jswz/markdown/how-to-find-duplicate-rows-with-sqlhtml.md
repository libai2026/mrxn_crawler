---
title: "MySQL 如何查找并删除重复行？"
source: https://mrxn.net/jswz/how-to-find-duplicate-rows-with-sql.html
---

# MySQL 如何查找并删除重复行？

[Mrxn](https://mrxn.net/author/1)* 发表于2019/4/15 22:50
* 2270浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

## 如何查找重复行

第一步是定义什么样的行才是重复行。多数情况下很简单：它们某一列具有相同的值。本文采用这一定义，或许你对“重复”的定义比这复杂，你需要对sql做些修改。
  
本文要用到的数据样本

```
create table test(id int not null primary key, day date not null);

insert into test(id, day) values(1, '2006-10-08');
insert into test(id, day) values(2, '2006-10-08');
insert into test(id, day) values(3, '2006-10-09');

select * from test;
+----+------------+
| id | day        |
+----+------------+
|  1 | 2006-10-08 |
|  2 | 2006-10-08 |
|  3 | 2006-10-09 |
+----+------------+
```

前面两行在day字段具有相同的值，因此如何我将他们当做重复行，这里有一查询语句可以查找。查询语句使用GROUP BY子句把具有相同字段值的行归为一组，然后计算组的大小。

```
select day, count(*) from test GROUP BY day;
+------------+----------+
| day        | count(*) |
+------------+----------+
| 2006-10-08 |        2 |
| 2006-10-09 |        1 |
+------------+----------+
```

重复行的组大小大于1。如何希望只显示重复行，必须使用HAVING子句，比如

```
select day, count(*) from test group by day HAVING count(*) > 1;
+------------+----------+
| day        | count(*) |
+------------+----------+
| 2006-10-08 |        2 |
+------------+----------+
```

这是基本的技巧：根据具有相同值的字段分组，然后知显示大小大于1的组。

### 为什么不能使用WHERE子句？

因为WHERE子句过滤的是分组之前的行，HAVING子句过滤的是分组之后的行。

## 如何删除重复行

一个相关的问题是如何删除重复行。一个常见的任务是，重复行只保留一行，其他删除，然后你可以创建适当的索引，防止以后再有重复的行写入数据库。
  
同样，首先是弄清楚重复行的定义。你要保留的是哪一行呢？第一行，或者某个字段具有最大值的行？本文中，假设要保留的是第一行——id字段具有最小值的行，意味着你要删除其他的行。
  
也许最简单的方法是通过临时表。尤其对于MYSQL，有些限制是不能在一个查询语句中select的同时update一个表。在我的另一篇文章中
[MySQL 在 SELECT 的同时 UPDATE 同一张表](https://mrxn.net/jswz/how-to-select-from-an-update-target-in-mysql.html)
(
[How to select from an update target in MySQL](http://www.xaprb.com/blog/2006/06/23/how-to-select-from-an-update-target-in-mysql/)
), 讲述了如何绕过这些限制。简单起见，这里只用到了临时表的方法。
  
我们的任务是：删除所有重复行，除了分组中id字段具有最小值的行。因此，需要找出大小大于1的分组，以及希望保留的行。你可以使用MIN()函数。这里的语句是创建临时表，以及查找需要用DELETE删除的行。

```
create temporary table to_delete (day date not null, min_id int not null);

insert into to_delete(day, min_id)
   select day, MIN(id) from test group by day having count(*) > 1;

select * from to_delete;
+------------+--------+
| day        | min_id |
+------------+--------+
| 2006-10-08 |      1 |
+------------+--------+
```

有了这些数据，你可以开始删除“脏数据”行了。可以有几种方法，各有优劣（详见我的文章many-to-one problems in SQL），但这里不做详细比较，只是说明在支持查询子句的关系数据库中，使用的标准方法。

```
delete from test
   where exists(
      select * from to_delete
      where to_delete.day = test.day and to_delete.min_id <> test.id
   )
```

### 如何查找多列上的重复行

有人最近问到这样的问题：
  

我的一个表上有两个字段b和c，分别关联到其他两个表的b和c字段。我想要找出在b字段或者c字段上具有重复值的行。
  
咋看很难明白，通过对话后我理解了：他想要对b和c分别创建unique索引。如上所述，查找在某一字段上具有重复值的行很简单，只要用group分组，然后计算组的大小。并且查找全部字段重复的行也很简单，只要把所有字段放到group子句。但如果是判断b字段重复或者c字段重复，问题困难得多。这里提问者用到的样本数据

```
create table a_b_c(
   a int not null primary key auto_increment,
   b int,
   c int
);

insert into a_b_c(b,c) values (1, 1);
insert into a_b_c(b,c) values (1, 2);
insert into a_b_c(b,c) values (1, 3);
insert into a_b_c(b,c) values (2, 1);
insert into a_b_c(b,c) values (2, 2);
insert into a_b_c(b,c) values (2, 3);
insert into a_b_c(b,c) values (3, 1);
insert into a_b_c(b,c) values (3, 2);
insert into a_b_c(b,c) values (3, 3);
```

现在，你可以轻易看到表里面有一些重复的行，但找不到两行具有相同的二元组{b, c}。这就是为什么问题会变得困难了。

### 错误的查询语句

如果把两列放在一起分组，你会得到不同的结果，具体看如何分组和计算大小。提问者恰恰是困在了这里。有时候查询语句找到一些重复行却漏了其他的。这是他用到了查询

```
select b, c, count(*) from a_b_c
group by b, c
having count(distinct b > 1)
   or count(distinct c > 1);
```

结果返回所有的行，因为CONT(\*)总是1.为什么？因为 >1 写在COUNT()里面。这个错误很容易被忽略，事实上等效于

```
select b, c, count(*) from a_b_c
group by b, c
having count(1)
   or count(1);
```

为什么？因为 (b> 1) 是一个布尔值，根本不是你想要的结果。你要的是：

```
    select b, c, count(*) from a_b_c
    group by b, c
    having count(distinct b) > 1
       or count(distinct c) > 1;
```

返回空结果。很显然，因为没有重复的{b,c}。这人试了很多其他的OR和AND的组合，用来分组的是一个字段，计算大小的是另一个字段，像这样

```
select b, count(*) from a_b_c group by b having count(distinct c) > 1;
+------+----------+
| b    | count(*) |
+------+----------+
|    1 |        3 |
|    2 |        3 |
|    3 |        3 |
+------+----------+
```

没有一个能够找出全部的重复行。而且最令人沮丧的是，对于某些情况，这种语句是有效的，如果错误地以为就是这么写法，然而对于另外的情况，很可能得到错误结果。

事实上，单纯用GROUP BY 是不可行的。为什么？因为当你对某一字段使用group by时，就会把另一字段的值分散到不同的分组里。对这些字段排序可以看到这些效果，正如分组做的那样。首先，对b字段排序，看看它是如何分组的

| a | b | c |
| --- | --- | --- |
| 7 | 1 | 1 |
| 8 | 1 | 2 |
| 9 | 1 | 3 |
| 10 | 2 | 1 |
| 11 | 2 | 2 |
| 12 | 2 | 3 |
| 13 | 3 | 1 |
| 14 | 3 | 2 |
| 15 | 3 | 3 |

当你对b字段排序（分组），相同值的c被分到不同的组，因此不能用COUNT(DISTINCT c)来计算大小。COUNT()之类的内部函数只作用于同一个分组，对于不同分组的行就无能为力了。类似，如果排序的是c字段，相同值的b也会分到不同的组，无论如何是不能达到我们的目的的。

### 几种正确的方法

也许最简单的方法是分别对某个字段查找重复行，然后用UNION拼在一起，像这样：

```
 select b as value, count(*) as cnt, 'b' as what_col
 from a_b_c group by b having count(*) > 1
 union
 select c as value, count(*) as cnt, 'c' as what_col
 from a_b_c group by c having count(*) > 1;
+-------+-----+----------+
| value | cnt | what_col |
+-------+-----+----------+
|     1 |   3 | b        |
|     2 |   3 | b        |
|     3 |   3 | b        |
|     1 |   3 | c        |
|     2 |   3 | c        |
|     3 |   3 | c        |
+-------+-----+----------+
```

输出what\_col字段为了提示重复的是哪个字段。另一个办法是使用嵌套查询：

```
select a, b, c from a_b_c
    where b in (select b from a_b_c group by b having count(*) > 1)
        or c in (select c from a_b_c group by c having count(*) > 1);
+----+------+------+
| a  | b    | c    |
+----+------+------+
|  7 |    1 |    1 |
|  8 |    1 |    2 |
|  9 |    1 |    3 |
| 10 |    2 |    1 |
| 11 |    2 |    2 |
| 12 |    2 |    3 |
| 13 |    3 |    1 |
| 14 |    3 |    2 |
| 15 |    3 |    3 |
+----+------+------+
```

这种方法的效率要比使用UNION低许多，并且显示每一重复的行，而不是重复的字段值。还有一种方法，将自己跟group的嵌套查询结果联表查询。写法比较复杂，但对于复杂的数据或者对效率有较高要求的情况，是很有必要的。

```
    select a, a_b_c.b, a_b_c.c
    from a_b_c
       left outer join (
          select b from a_b_c group by b having count(*) > 1
       ) as b on a_b_c.b = b.b
       left outer join (
          select c from a_b_c group by c having count(*) > 1
       ) as c on a_b_c.c = c.c
    where b.b is not null or c.c is not null
```

以上方法可行，我敢肯定还有其他的方法。如果UNION能用，我想会是最简单不过的了。
  
  
原文地址：
<https://www.xaprb.com/blog/2006/10/09/how-to-find-duplicate-rows-with-sql/>

* 标签：
* [#
  分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#
  SQL](https://mrxn.net/tag/SQL)
* [#
  MySQL](https://mrxn.net/tag/MySQL)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[MySQL 如何查找并删除重复行？](https://mrxn.net/jswz/how-to-find-duplicate-rows-with-sql.html)
  
文章链接：
<https://mrxn.net/jswz/how-to-find-duplicate-rows-with-sql.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/how-to-find-duplicate-rows-with-sql.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/how-to-find-duplicate-rows-with-sql.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});