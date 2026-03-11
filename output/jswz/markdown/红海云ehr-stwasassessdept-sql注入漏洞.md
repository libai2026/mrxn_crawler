---
title: "红海云eHR StWasAssessDept SQL注入漏洞"
source: https://mrxn.net/jswz/redseaplatform-submitStWasAssessDept-StWasAssessDept-sqli.html
asset_dir: assets/红海云ehr-stwasassessdept-sql注入漏洞
---

# 红海云eHR StWasAssessDept SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/2 08:28
* 357浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

软件

身份验证

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

红海云eHR系统中的StWasAssessDeptController（submitStWasAssessDept/StWasAssessDept.mob）模块存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL查询语句，绕过系统认证，实现对数据库的非法访问，获取敏感信息（如用户凭证、个人数据等），甚至在特定条件下可能导致数据库被完全控制，影响范围包括数据访问权限和系统控制权限。

SQL注入检测工具

# 影响版本

# fofa语法

> body="/RedseaPlatform/skins/images/favicon.ico"

# 漏洞分析

> 鉴权相关看之前的 [红海云eHR BossIndex SQL注入漏洞](https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html) 分析鉴权部分

进入本文的正题 `StWasAssessDeptController` ，看下它的 **submitStWasAssessDept/StWasAssessDept** 方法实现逻辑

代码安全审计

深入探索

Web安全课程

安全运维咨询

防火墙软件

[![红海云eHR StWasAssessDept SQL注入漏洞](images/img-001-ceabda68abf1.webp)](https://image.mrxn.net/b75b308825944ef9a3f76e01e78f7a8d.webp)

如图所示，参数 `String userId = req.getParameter("userId");` 被直接拼接进 `"SELECT USER_NAME FROM PT_USERS WHERE USER_ID='" + userId + "'";` SQL语句中执行，无任何过滤或校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，朴实无华。

# 漏洞复现

```
POST /RedseaPlatform/submitStWasAssessDept/StWasAssessDept.mob HTTP/1.1
Host: redseaplatform.mrxn.net
Content-Type: application/x-www-form-urlencoded

userId=SQLI_POC
```

[![红海云eHR StWasAssessDept SQL注入漏洞](images/img-002-20ff06eff68f.webp)](https://image.mrxn.net/7584ab3e759745bab375004ba5d367c0.webp)

成功延 2 秒

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[红海云eHR StWasAssessDept SQL注入漏洞](https://mrxn.net/jswz/redseaplatform-submitStWasAssessDept-StWasAssessDept-sqli.html)  
文章链接：<https://mrxn.net/jswz/redseaplatform-submitStWasAssessDept-StWasAssessDept-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANf0lEQVR4AeycC3LkSA5D/eb+d55tJP1KzHSqPva07YjVRMMgATAli1X+bcT+8/b29u+r+Pf9v93cu/XhTPWVc8aq2cfrUJe796j+zIxnPprV7+zsq5yFvP056Cn8OfzDP2c1gDfA9sbA0GHmzENpt/B7Ea8DKgfF77EtObeaZ3rPPcqsPpzfj9lH7PXHQmwu/vknMC0EatMw89ltZuv3vPhncA64vTvVVoa6H3XP7H2v46891BlQnEzQc9Zy/ADmGZh78/cYagZmXmemhazm1X//E/jSQuDYdl5JHeunAkcWuNmZuTXvBTC+37y3N0o2uAnvBRzvMtjPvkdv70aYc3CcYRYqk2sG6qkDmH3AyKf5Swv59FWvwdMn8NcXAkyv9ryyOqB8ONi7hdLsZfiow0fN/I77PaROBvZnQOkwc2Y6PKdrr9Z/fSGv3tD/e35aSDa8wysPCfavIs+F8j0zuvXK8YJVt4+3Qk+G+XrqMpTfz9Hr2q429wzv5qOts9NCVvPT/TX46ScwFgL1KoH7vLtKthxAzaYOzKYOYPahenPh5ILUrwB4GM+5ATB9T+uDMHtwv++zqYHQBGBcD+6zQ2MhNhf//BP4J6+aV+FtZw5q86kDmPuejb/rowdQs2ae5cyuWaiz4gVQ/Zqzh+P3EKhs5gJ4rvescOY+g+sdkqf3i7BdCNQrYr1P2OvJwd6D0qE42QCqB9IOrK+oIf75oP6nnP4BH74+T4E/DVTGM+Q/1vQv+iRsGqiztGDu1TtDZWBmMzDr/wB6t09OARiafW46sA+n3yFesHpQZ6onA6WlDuB+n0zgGZ2jB11LDXUmFCfTAaXD8aVLP/PB2kcLum4txw/WHup66vL2HaJ58fc/gbEQqG1lk4G3kTqwh8rBwXoylGf/FYY6K/cQvHIW1OwrM7lGsM7A/bMyE2QOKgvF0Z5B5oOxkGcGrsz3PIHpx971klBbhuJsMOg5KA+K4wdmoHQoXvX0yQepg9Qd0d7e3sb3Mzi+xkOdCRi5sfPAmLOXDfYeKgszm5Fh9uHozXg+lHfWr/nrHeKT+iU8fsqCeYvr1uxhn9MPwz6zfr7JBtFhnoHX+pzxLKDOhpl387m/QA9qxl5OJrAPpw9Sd0TrgDoTiq93SH9av6AeC3Fj3g/UttRh7tXNd9aDmoHinkkNH3X4qCXrmak71MMwz0L18YI+t6uTETu/a+ZkqGv1jLUZWX1l/bGQ1bz6n3sC46csqA1DsbcD1bs9qB6KzYVh1pyJFzzqe2bNxrsH4Gavs8D4KcvA6quHYc7C3CcTwKzvzoTKwH12Fip3vUPyhH8RxkLc0qP7Mifv8lCbhuI1u+t35+y0dRaOa5iHQzMfhtLN7Ti5HXbZR9p6jvlVh/m+xkIMX/zzT2D8HuJtuD37lWHeZnwozdmVoXyYObMBEBoApq/3Q/zzAWZ9dw21P/G7/6DOuuXf01A6nPM68z467hnqLwhqMtR5aw+zrn+9Q3wSv4THT1nrvfhKkKG2ad/zqwaVNaO/Mhw5PWfg8KKd+TDndtlogWfIULP2u0y0Z+AZwMO42bPgeIcA421nCKqHYg+B6qE4eagaitdsMgGUD8XmwvGD1B1Q2XgdPWOtD/sZ2OvO7diz5V1m1WC+ziuzOWssJMWF3/EEtgs526q6DPWNzD7sp5U6gHrFpO4w1xkqq2YeZl0fSoeD9WQo79k+OagZKI52D3Dknr1nc+u524Wsoav/vicwFuK2oDYNxereDpQOxfH1ZCjPXobSYWb9zlAZtVwnsIfZjx4/SH0PyQRmUotVs4e6HhSveXNhqEzqz2As5DOD18zfeQLTQtbNw7xtfXl3S2femZ4zoK6zZqD0ZB4BKrue4Zw6VE5dhtIBpRs7K9+M90J9x++RG5lRsJenhRi6+MtP4NMHjD+dAOP3ECj2NLcGpUOxPmB5m78JLxRe54WRD1HPAMa9GFA/6+HIm4VDyxzc75MJoHJwcPQOODygW6O+3iHjMfyeD2MhvjJkbw8YrzZ1GQ4djjq+s3K0ACq36vZhuJ+B8nNekJkgNcweVB9/h8ysMHemQ52pD9VDceb15GivYCzklYEr+3efwFgIHBveXQ7Kh2IzcPym3jWoHBy8vmKgPOfCZuRoAcxZ+NgnF8BHD0oDEhkAxrt/NO8foDSY+d2+EZR/E1oB5cHMRvzcZHWo/FiI4sU//wTGn9/dFtSW1tvSXzk5mGfMxAvOenWoeSDxAWB69ZodZvug3llbzV6G+WyoHj6+28/O8Kydr7ayM3BcD1C+/T9MXO+Q2yP5HcX4PeTZWwGmV+5uDirjK2TNQPmr3ntnobJQrN6zqYHQBGDcqzPyFGpN/NaOEuqM0bz4AfazuU7gcVA5KB7vEKgmwQ6HZD37zjCfoQel28tQumeGoTQoNhsvsF9550ULzEKdGS1Ql6F8QOnGyXfcjDuF+TuRyTI/FjI5rbnK738C24UA4+3u7UD1MLN+2A3DPgOlm5OhdDi+qerJOX8HOGah6jUHpa9nrf06l94M1BnROqB0c/GgNJg5XgClpw76bPrtQmJc+JknMBbilqC2Z7/e0k5Xg5p1Rn3toXJQnJwZGcqDYvWVMxusenq4P5tMR84R6rA/w5wMlbPv7FlqZz3UGWMhhi7++ScwfjGE2o5bhOq9vVW31w+ryTCfkUyHua5Bzey85GD24ejjB49moWagODMBVA8fv5fFD+DIwFF7TTg0qDpzHWdZM9c7xCfxS3j8YujWvCd7GWrba588lJe6w6zcvV4DvR01MH7KcxbmfoTaB+DWAdOsZ9wC78WZHhvqjNSBWTlaB8z5eI+y+itf75A8vV+EaSHwcdP9XqF8txqv1+mhMjBzvA4oP/PqqTvUZagZe7PpreVoAZzPxF/zXYOahZmTCZztHD2Amkm9A8w+VD8tZDf432vXifeewLQQN+0A1NbUZSjdXGczavZQM/ZyctZQGZg5meAsFz1+ADWbOogXpA5g9qOJ5IK1j9ahv+Oe67VZNfuVp4Ws5tV//xOYfg+BevVAsduE6qFYPQylwczxAig9dQDV+6kClrf/kSa5HYDxE5QDZtJDeWpQfbwdoHwoTgaqhuJoO3gNPTjycNT6naF8z4C5v94h/Wn9gnosxG2t7P2tOtRW9Z9hqBnPciY9lAfFeisn29F9dXjuDGedC68azGfBvs9s4HwYKgszJxdA6amDzARjIVAmFMcIoHqYOV4Ax58Z0gc5PEgdpA5SB7A/K56AxxmzYTjy6XfIPQRQ2dSBWcDyAwPTl0oDmQ/sw+mD1B3RArXUgT3UNcZCFC/++Sew/dPJ2W1lo8HOjx7oQW0citVXBm5S5js0gPEKhWJ1eTejBvsZKB2Kk/c8OLToK8zd47MZqLOdherNX+8Qn8wv4fFj76N7cXswbzNzUFrqAObeWTmZwL5z9ADunwGzD7xlLvC8aEG0IHWgv3Iyj5D54F4u/j143fUMZ653yPpkfrgf30O8B7fntp7tk/OMlT1LTjboOT05fmBGXY4X6Pe6a9GF+sqeueq9P8uc6X3W68vd29XXO2T3VH5Qe2khviLcdnrvPXVgb8ZeTibo/Vn2THdW7ud1LbrwLHu5687Ka8asvmwubEaO1uGMbE5+aSEecvHfewJjIW7Qy7itM91c+Cyz6skGnp06SB8OUgfrbLQgmY6e63XPZC4483d68kE/J7VZOZkgXtDrNRMvSK7DnDwW0gNX/bNPYLsQt7Xemrq8+un18moIonXod22tMxes+tonE0QPB6k7nrme+cwHzqQO1j5asM6lN5s6sD/jZDq2C+mBq/7eJzD9pu4Ws/178BZ7ZtU8S112Rj+st3K8jjN/1Xvv9brWa/2w10odvL315Nv09zSzK7+d/JfzAu3Uwdpf7xCfyC/hsZBsqsOtr/eobtY+bDZ1YG9Wjhd03zp6YO/M2icTqIfTd5zNJhvoOxNNqMnqzsirbr/j9Sx7z7IfC1kPMPSMbvaMPcMLmlMP66UO7OXdTHLqnaMHzqbuMNu1tTYj669n6nddbWXPkPX7bLztQmJc+JknMP646JaeZW81W7Z+NLvmep9zArXUHepew16Obr1yvOBM9zrJ9Dq9OJtd9d6fza7XcEb9eof4RH4Jj4W4nUe8u+dHr4R1ZneNNfNqnzPPZuIF3qccLehzqxc/6JnU0YLUZ4gfnPln+ljImXnp3/8EpoX4Cln5K7eVV0ngGZ7de+vkAjPy6tvrd9bLOYH9ys6seno9OVrHquc6QTJ6K8cL1JPviBdMC4lw4e8/gXtX+NJCsu17h3evvxpSd8865wXxg1W3j9cRvfepo+0QL9DL9QL7zskFaqk71DMfxFOTowX2Z5z54EsLOTv80j//BL60kGz+DN5Sth6sfbRAPexZqYO1T36H5JIP9FMH9skE9vHOkFxwllWXkw3OztvpzspmvrQQD7n4v3sC00Ky5R3uXW7dsFl1z1t7dfNhM6l32M2suTVjf3a2fmezal5D3X71o6vJ0QL7leMF6tNCYlz42ScwFuLmH/HuVt3sOqu+zpjr+k7r/tlZZjLf696ry54lJxvEDwc7L7566o7MCHV7edXtVx4LWcWr/7kn8D8AAAD//xohYNUAAAAGSURBVAMARFo20bv3fFUAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/redseaplatform-submitStWasAssessDept-StWasAssessDept-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/redseaplatform-submitStWasAssessDept-StWasAssessDept-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 