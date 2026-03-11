---
title: "友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞"
source: https://mrxn.net/jswz/youjiasoft-Sysconfig-GetZTList-unauthcation.html
---

# 友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/27 08:30
* 869浏览
* [0评论](#comment)
* 19分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理软件，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

该系统的
`Sysconfig/GetZTList`
接口存在
[未授权访问](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)
漏洞，攻击者无需任何认证即可直接访问该接口，从而获取敏感信息。此漏洞可能导致企业内部数据
[泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)
，包括但不限于用户列表、配置信息等，对企业的运营安全和数据隐私构成严重威胁。

# 影响版本

13.7004.1053.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

在 SysconfigController 找到 GetZTList 方法处理逻辑如下

![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](https://image.mrxn.net/b7f08d7492b545e0b3c9f649581e3108.webp)

表明需要一个pwd参数，即可返回
`DBOperation.GetZTList`
的内容，跟进看下它的实现逻辑

![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](https://image.mrxn.net/6220a59dd3ed4ddb81e888da5e747198.webp)

1. **框架行为:**
   在 ASP.NET (或 ASP.NET Core) MVC/Web API 框架中，当一个 Action 方法的参数是引用类型（如
   `string`
   ）且在 HTTP 请求中未提供该参数时，模型绑定器会为该参数赋其默认值。对于
   `string`
   类型，其默认值为
   `null`
   。
2. **代码执行路径:**
   因此，当攻击者请求
   `GetZTList`
   接口而不带
   `pwd`
   参数时，
   `GetZTList(string pwd)`
   方法中的
   `pwd`
   变量值为
   `null`
   。
3. **条件判断绕过:**
   代码会执行
   `if (string.op_Inequality(pwd, "-1"))`
   ，这等同于
   `if (pwd != "-1")`
   。由于
   `pwd`
   是
   `null`
   ，
   `null != "-1"`
   的结果为
   `true`
   。因此，程序会进入
   `if`
   代码块，而不是
   `else`
   分支。
4. **过滤逻辑缺陷:**
   在
   `if`
   代码块内部，程序会执行
   `Where`
   条件进行过滤：
   `m => string.op_Equality(m.ZTPwd, "") || m.ZTPwd == null || string.op_Equality(m.ZTPwd, jmPwd)`
   * 由于
     `pwd`
     为
     `null`
     ，
     `jmPwd = EncDecString.EncryptPWD(null)`
     的结果很可能是
     `null`
     或空字符串
     `""`
     (取决于
     `EncryptPWD`
     方法的实现)。
   * **情况一：
     `jmPwd`
     为
     `null`
     。**
     过滤条件变为
     `m.ZTPwd == "" || m.ZTPwd == null || m.ZTPwd == null`
     ，简化为
     `m.ZTPwd == "" || m.ZTPwd == null`
     。
   * **情况二：
     `jmPwd`
     为
     `""`
     。**
     过滤条件变为
     `m.ZTPwd == "" || m.ZTPwd == null || m.ZTPwd == ""`
     ，同样简化为
     `m.ZTPwd == "" || m.ZTPwd == null`
     。
5. **最终结果:**
   无论
   `EncryptPWD(null)`
   的具体返回值是什么，最终的过滤逻辑都会返回所有
   `ZTPwd`
   字段为
   **空字符串或
   `null`**
   的账套列表。这实质上是列出了系统中所有
   **未设置密码**
   的账套。

![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](https://image.mrxn.net/052fb996c47b4dbaab6394673c3a6ae0.webp)

1. 代码的业务逻辑是通过
   `pwd`
   参数来验证用户身份，并返回其有权访问的账套列表。
2. 代码中存在一个关键的条件判断：
   `if (string.op_Inequality(pwd, "-1"))`
   ，这等同于
   `if (pwd != "-1")`
   。
3. **正常逻辑分支 (
   `pwd`
   不等于
   `"-1"`
   )**
   : 当
   `pwd`
   不为
   `"-1"`
   时，程序会执行
   `if`
   代码块。此代码块会将传入的
   `pwd`
   参数进行加密（
   `EncDecString.EncryptPWD(pwd)`
   ），然后与配置文件中每个账套的
   `ZTPwd`
   字段进行比对。只有密码为空、
   `null`
   或匹配成功的账套才会被返回。这是预期的、受保护的业务逻辑。
4. **漏洞逻辑分支 (
   `pwd`
   等于
   `"-1"`
   )**
   : 当
   `pwd`
   参数的值
   **正好为字符串
   `"-1"`**
   时，程序会跳过
   `if`
   代码块，执行
   `else if`
   代码块。在此分支中，代码会遍历
   `zts`
   （即从配置文件
   `sysconfig_zts`
   中加载的
   **所有**
   账套列表），并
   **不做任何密码校验**
   ，直接将所有账套的详细信息添加到
   `ztList`
   中并返回。

再看前端 js 里有关此路由的调用如下，
`pwd`
参数可有可无

![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](https://image.mrxn.net/01a07707ca7048f8a7813cddb51b71c2.webp)

或者是
`pwd=-1`

![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](https://image.mrxn.net/ff4bcae60f7b44b784bca69135c148f3.webp)

# 漏洞复现

```
GET /Sysconfig/GetZTList HTTP/1.1
Host: youjiasoft.mrxn.net
```

![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](https://image.mrxn.net/72bc8cef116f46cbae42042007b5e23f.webp)

响应包含数据库连接信息、应用安装物理路径等敏感信息。

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  0day](https://mrxn.net/tag/0day)
* [#
  未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)
* [#
  asp.net](https://mrxn.net/tag/asp.net)
* [#
  泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
[友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](https://mrxn.net/jswz/youjiasoft-Sysconfig-GetZTList-unauthcation.html)
  
文章链接：
<https://mrxn.net/jswz/youjiasoft-Sysconfig-GetZTList-unauthcation.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/youjiasoft-Sysconfig-GetZTList-unauthcation.html"),
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
text: encodeURI("https://mrxn.net/jswz/youjiasoft-Sysconfig-GetZTList-unauthcation.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});