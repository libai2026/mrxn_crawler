---
title: "索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-Jzt-statistics-countJztArticleGroupByChannel2-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjztstatisticscountjztarticlegroupbychannel2-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/15 08:17
* 629浏览
* [0评论](#comment)
* 1小时阅读

深入探索

数据库

统计学

statistics


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/Jzt/[statistics](#)/countJztArticleGroupByChannel2 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

统计信息

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/Jzt/statistics/countJztArticleGroupByChannel2`的实现逻辑

```
@RequestMapping(
    value = {"countJztArticleGroupByChannel2"},
    method = {RequestMethod.GET}
)
public Response countArticleGroupByChannel2(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "startTime",required = false) Long startTime, @RequestParam(value = "endTime",required = false) Long endTime, @RequestParam(value = "channelId",required = false) String channelId, @RequestParam(value = "ID",required = false) String ID) {
    List args = new ArrayList();
    StringBuffer sqlBuffer = new StringBuffer("select a.num,a.channelName,a.cname from ");
    sqlBuffer.append(" (SELECT SUM(h.num) as num,h.channelName as channelName,'合计' as cname from  ");
    sqlBuffer.append(" (SELECT count(DISTINCT id) AS num,channelName,cname FROM(");
    sqlBuffer.append(" select zcnarticle.id ");
    sqlBuffer.append(" , (SELECT zcchannel.channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" WHERE zccatalog.ID = zcnarticle.catalogID ) AS channelName ");
    sqlBuffer.append(" ,(SELECT zccatalog.Name FROM zccatalog INNER JOIN zcchannel ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID ) AS cname  ");
    sqlBuffer.append("  from zcnarticle  ");
    sqlBuffer.append(" , (SELECT DISTINCT zcnarticle.id articleid FROM zcnarticle where 1=1 ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" UNION SELECT zcnwxarticlerela.articleid FROM zcnwxarticle INNER JOIN zcnwxarticlerela ON zcnwxarticlerela.wxarticleId = zcnwxarticle.id ");
    sqlBuffer.append("  where 1=1 ");
    sqlBuffer.append(" and zcnwxarticle.ifval = '1' ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnwxarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnwxarticle.publishDate");
    sqlBuffer.append(" ) zcnarticleids ");
    sqlBuffer.append(" where zcnarticleids.articleid =zcnarticle.id ");
    sqlBuffer.append(" and zcnarticle.ifval = '1' ");
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" AND EXISTS ( SELECT channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID LIMIT 1)");
    if (channelId != null && ID == null) {
        sqlBuffer.append("and  catalogID in  (select distinct ID from  zccatalog where  1 = 1 ");
        sqlBuffer.append(String.format(" and prop3  in (%s) ", channelId));
        sqlBuffer.append(" ) ");
    }

    if (ID != null) {
        sqlBuffer.append(String.format(" and  catalogID  in (%s) ", ID));
    }

    sqlBuffer.append(")tmp  where  1= 1 ");
    sqlBuffer.append("  group by cname) h GROUP BY channelName UNION ");
    sqlBuffer.append("(SELECT count(DISTINCT id) AS num,channelName,cname FROM(");
    sqlBuffer.append(" select zcnarticle.id ");
    sqlBuffer.append(" , (SELECT zcchannel.channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" WHERE zccatalog.ID = zcnarticle.catalogID ) AS channelName ");
    sqlBuffer.append(" ,(SELECT zccatalog.Name FROM zccatalog INNER JOIN zcchannel ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID ) AS cname  ");
    sqlBuffer.append("  from zcnarticle  ");
    sqlBuffer.append(" , (SELECT DISTINCT zcnarticle.id articleid FROM zcnarticle where 1=1 ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" UNION SELECT zcnwxarticlerela.articleid FROM zcnwxarticle INNER JOIN zcnwxarticlerela ON zcnwxarticlerela.wxarticleId = zcnwxarticle.id ");
    sqlBuffer.append("  where 1=1 ");
    sqlBuffer.append(" and zcnwxarticle.ifval = '1' ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnwxarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnwxarticle.publishDate");
    sqlBuffer.append(" ) zcnarticleids ");
    sqlBuffer.append(" where zcnarticleids.articleid =zcnarticle.id ");
    sqlBuffer.append(" and zcnarticle.ifval = '1' ");
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" AND EXISTS ( SELECT channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID LIMIT 1)");
    if (channelId != null && ID == null) {
        sqlBuffer.append("and  catalogID in  (select distinct ID from  zccatalog where  1 = 1 ");
        sqlBuffer.append(String.format(" and prop3  in (%s) ", channelId));
        sqlBuffer.append(" ) ");
    }

    if (ID != null) {
        sqlBuffer.append(String.format(" and  catalogID  in (%s) ", ID));
    }

    sqlBuffer.append(")tmp  where  1= 1 ");
    sqlBuffer.append("GROUP BY cname))as a ORDER BY a.channelName,a.cname DESC");
    QueryBuilder queryBuilder = new QueryBuilder("" + sqlBuffer, args.toArray());
    List<Map<String, Object>> data = queryBuilder.executeListMap();
    return Response.success(data);
}
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞](images/img-001-acf3ef0c1cef.webp)](https://image.mrxn.net/af9a1f2fe37e4c8aa2d15f998437a143.webp)

代码一看就很明了了，**channelId**和**ID**无任何过滤或校验，被直接拼接在in子语句中，从而造成了[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

如果没有String.format，就不存在，因为默认的append方法底层是参数化查询。

SQL注入防护

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/Jzt/statistics/countJztArticleGroupByChannel2?siteCode=&token=&userCode=admin&channelId=1&catalogid=1&channelId=SQLI_POC HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞](images/img-002-6ade200469c3.webp)](https://image.mrxn.net/5e02fa3ac6f24f31ba827d2d464165e8.webp)

成功利用报错注入在响应回显当前数据用户

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞](https://mrxn.net/jswz/sobey-Jzt-statistics-countJztArticleGroupByChannel2-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-Jzt-statistics-countJztArticleGroupByChannel2-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANtUlEQVR4Aeyb4Xbjxg6D9+v7v3NrDAKbpEeKm91N/EM9QUCCIDUryrGTc+8/v379+vf/4t/yX3ojJf8dnrOST841pNd4l0sTpk+aIF0sKBYU76BaxSue6j+LtZBft4Ev4Tbo6Su9wC/gXo8eTiH5GQNrVjzgHMyZdcbpPfPMGuzng3Uwz9lgfc5THu9nLK+wFqLgwnvcgbYQ8Kah89lRwd548iQkD08del984njBnuSqCbDXaw3sAbNqO4DruYZ455OmmqBYUCwo/gzg60Dn2dcWMotX/v134I8vBM6fgPlPhO4HpmW9nwD397lpgOeanlxheqUJwJqbOpDwzsDyyC+kANbBrJoAxPJl/uML+fJJrsZ1B35rIfB4IvSECGtq+Qasp6xIK5RXWMn4Bu5RXUgZrO9y6LV41C8kD0urkA77GWAdzOlTT4X0mn8l/q2FfOWCV8/5HWgL0YZ3OBpRvfFUrcbgpws6y5PeI5ZHmHVpE/FAvw7s8/j/Ns9zJp/XbQuZxS/nV+OX78BaCOyfHuj6vApwl4D2XgE9j/HoyVD9qAaedVZXf8X0HuXwmJ3+I2/qRww8lYB1X+Cc07gWkuTin78D/+Rp+D9cjw3efDToefTM3+WpQe+Fnqd3svqnBq/3pl8szFkzhz4bnNdexV/B9QqZd/uH87YQ8KbBPM8G1sFc6/NpSA3sBfPUlUOvSavI7KopBvfBg6UL6QlLqwD3VO0ohu6dM5ODffDgzARryY/4H+Bey+AIwHpDSj7rycXxwHkP9Lr61C8oFhQLiiug98ojyCMWFAvQveBcngp5BXAdHlx9iuUTwB7FFfJMQPfCPgfr7RVSh1/xz9yB9aYO3g6Yc5RsOzn0OpDSeiXB8x/5gFW7G0cADOWRzus/Ko6ANVs+eMTK7fi16sCv+R9wrwGrrL6KJd6+Act7C9dXPCu5fYNev0nLDyhcSE8YWJ5VvH2Lfr1Cbjfjnb7aQrKleUDwNlOvHG+0o/wzXfXMAF9PWsHhn9+rB9ybWaklh16PLh+4plgA59UjPTjSUxcfeY70thANuPCzd2B9yprbOsrBT0yODCR8YmD9jMyscIzJxdHC0gTwjOiT5RHg+b1resGz5BfAOZilzZ6jHNxzVJeueQLYC2bVBHAujwDOr1eI7s4bYX3KynnAW4I9a5MCuF7jOUM1YerJzxg8f3pgr9frzJ7k8gjgGYqF1OHxKgN7UpusPiG6YgGI9MSqC8D6yfFk+BCuV8jHjXgXWu8hOYw2WBE9DN5uPNJrrDwAe5OfMey9R7MzC577jnrA3tTBeWaJ4Vmr+uyF7lcdrIFZmqA5FdKEqim+XiG6C2+EtRDwNnMu6Hl0bVRILgZ7way6oFqFNKFqiuHxs1v5VwDc24D1MxrMumYFdP3eeAviu4XbLzjuTUNmhME9qU+GXl8LmaYr/7k70D5lzWNky2HwNsEsf2qKBXBt6qrtIB+4Z1eXBr2uHkG1I6guzLo0AT5mfhikfYSHJI8Avfew4VaQX7iF60uxAPsZ1ytk3ab3+bYWoo0JOZZiITl4m9KE6GI4rqkegH1HuXSwR9cQwLlqO8gjqAb2KhfAOexZPRXw8Kl/B7AnffHAQwfHYI4Xeh49M8LrYy90M/Q8ZrCePEPFsK+BdXkEeM4zLwz2JFefMHPoPtXlO4M8FWde8Px40pd8x0ee6NBnzhnrFTLFK/+5O7AWcrQ96NuML8eF54+s0HviTW84uhj2PaoJu56qA0oXgPWxNz3hVbx9A9fBnHrlm237Be6ZxfRKB3uqVnXFFWA/mNdCquGKf/YOtI+92epk8Pags44O1hRXgPXMSg26rnpqYWlC8jC4d+byQq/FE5ZHOMqjV5ZfgP1ssA7m2gvWwKw5FfFGS369QnIn3oTXQsBbzJnAOZizxcnxi89qqgfxJRdHA19PmgDOwSytovZVXTHse1QToNfBOaByQ64TbsWRxBMe5fX+Bo9rAEuLfy1kNl35b9+BLw9Yv4ekG7yt5Nlacuh16fGAa2BWrQK6Ds6Bu23OSiF68jCwni7l0zNzeYToYWlBNPBcMKf+GYP98ODPelIH91yvkNyRN+H2KStnmk/K1JPvOL3heGZedfDTES2cHnA9+axLjxYG94A5+hHXGYqFI++Zrr6KeMHnqLVdfL1CcsfehNdC5qbA28wZwTl0Vh2sKa4A67DneOH5t/3Uwjkf7GfBQ589szd1ePSA41lLb/Rw9HB0MXgWmKVVgHUwpwbO10IiXvzzd2AtBLwdMM/NJ5+s40dTXBF9cjxVB1931sA6mFMP1xmJU5ucOvRZ0eWHXgPnYJbnM2Te5PRFTz55LWSKV/5zd2At5LOt5Xjw+pMye6D3gnN4vIeAtfTmXJNTDwMJP+XMOjNOz8zTC6zfg3Z1cC3eybseedovhhIE2A87GqKeAPa9qYd3s6LBazPqrMRh8AzY87xWcnFmhOF8RnyVNUeo2i4Gz05tvUKSTL7y778DayHgLWmjFTkOuA6dVQdrioX0K66YOrhPOjgGc/rgtRzsA9J6Z83f4W44CdIXy8yB9SMLzPKBY+ismgBdz8zwWoiMF97jDmz/dALeYraWoyavPGvJwTNmXnsVqy6ukFYBfVb1zrj2KQb3QmfVKoB7Cqwn/y58BLDXP8rr/+GVeHLOOfWZX6+QeUd+OF+fsrI96E8AOD+q6+ypKX4F4JnxgnN4cGaG4/0TnJng69WZYG16ksf7WS7f9ECfPevqEa5XiO7CG6EtZG7ts1z/DvDmFQvQ86MZYF/qlTVnh3jAvdUDz1qtpzda8rD0Gis/AvRrwSPPDLCWPAzWwZxrgPO2kBQv/rk7sBYC3g6Yj7YJroN5d+z0huNJDr0XiOXOQPuUc9YL3Zsh6UkO9oF56slf4Tk7PeDZQKQ7A+vfdNQb41pIku/h6ypnd6D9HnK0vejhDITjPwxWD/jpgIc/s8TxHjG4X96K6q+64tQU75B6ZfB1wJw+6HntURyfWLmgWAD3ShOg59IqrldIvRtvEK+FaJMCeHtgnueDvT59yqF7NV+Arst7BNh7Ya9rDrgGnVWrANd1ponq28Xg3tTAORDpkOe1gPbeshZy2H0Vvv0OrN/UP7sq9C1WP+xrR09CesF9yuERK0+v4h1SD1dPtMnga4A5dXCuGeB4V1M9SD155bNa9SWe/vYKmcXZBP3A8scDriUPg3V5K1LfMbzWAw8fON7Nk1avrRi6H5BtAVg/RlZy+ya/cAvbl7SKVhxJfJGhXwOct4XEfPHP3YG2EPCWcpy51ZnD42NseqDPiD45s+B5xvQmB88Gc2aonhhcA7NqO8S/4+kHzwLzrCfXrMRhaULyydBntoVM85V//x1YvxhC39LRMcA+MGvz8IiVB5mRHOwDc+pisAbm2SNPRepVS3xWi2fHwF2eM2YOrPcYMN8bbwFYA/NNal+w12O6XiG5E2/C7WNvnoRwzgjeavQwPH7+gz2zJ3l6wtHFO+1Mh34teY8A9oJ5+sC6zpAaWDvK5a2A7ldf6uAamFUTUp98vUJ0d94I6z0kW5rngr5VcA7m6T/LYd+ja0OvQc8zV14hOdgHRLqzfBUpAIc//+NJ38yjQ59R9cTpDUcPR598vULmHfnhfC0E+sbBebZ5xtC9898D53X553xpArhXsQA9T59qAdgDnVPf9aQ2OV7wrP9br37wDOhcPYrXQhRceI87sP2UlaNB3yb0XL48RYoFsGfqqgnguuIAupbeMOzr6ZevxsqD6JNTD4OvAdytwHq/mZ674SNI/SNtlFo4xZlHv14huRNvwutTVs4C/YnIFidPPxBp/c8p5QfW03UvfASqCfBcB2tg/mi5z0wOroNZOjiGzqoJuqYAvQ7OVZNPgGj/rmtDz+WpgEcdHIM5PtjnYB3M1yskd+xNeC1ET0cFeFvzjNB19bzikQ967+yrufwC9B5pQvUqBkQN8lWkGG3m8PirQ2rAepWnB5zPes0Th6H3ZFbqM18LSTE8TVNPHUhpHRyO/1F340ewmxHtw7J+XEhLPlm1iXiA+5ngOU5f/DuenuTh9NQ88eR4J4PPFn27kBQv/v47sD72grcEr/HumHkiwDPiiZ4cXAez9COPahXw6Jl6zRVn5mTVdpAPPF+xsPNJA/sUHwHOPZovpF+xcL1CckfehNdCtJlXMM+snp0mPUj9szw+cbzgpwzMqu0g/9ThvCd+sA+IdGegvQ/dCx+BriuAfR/yIunCSk6+ySOAZ6yFnPiv0jffgbYQ8Jag89mZtF0hHnitF+xLnxisgVlzBdUExYJiAeyDB0vfAexRvwDOd95o8lVMHTwjHtXBGnRWTYCug3PVhLYQCRf+/h04u8JvLQS8XXhwnpbw2cWParM3Ofg6yV9h6D3gPNfOjOSVoXtrTfFZr+rCK57q+62FaNCFP3sH/thC8iSAnyow57jgPL7oyhNPBvdMfZeDvWCOR/MF6HrqYXkCsDd5PJPBvqrPHrAn+uT0gn1/bCEZfPHv3YG2kLm95EeXUP2spjp489OnmiAdugecqy7APlevAM9/Q5MugHsV7wCPOjxiecE5dFZN0NkExRPShamDZ01dXqEtZJqu/PvvwFoIeGtwzmfHA/fGAz2PHobzenxiPTkCvN6jPkF9O6h2hOmPLzr0c4Bz1eMFa8lf5bWQV82X7+/fgf8AAAD//z3cEZ8AAAAGSURBVAMAMufQzr0Jt8kAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-Jzt-statistics-countJztArticleGroupByChannel2-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/sobey-Jzt-statistics-countJztArticleGroupByChannel2-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 