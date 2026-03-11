---
title: "东胜物流软件 /MvcShipping/MsBaseInfo/GetProParentModuTreeList SQL 注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsBaseInfo-GetProParentModuTreeList-sqli.html
asset_dir: assets/东胜物流软件-mvcshippingmsbaseinfogetproparentmodutreelist-sql-注入漏洞
---

# 东胜物流软件 /MvcShipping/MsBaseInfo/GetProParentModuTreeList SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/30 15:31
* 272浏览
* [0评论](#comment)
* 43分钟阅读

深入探索

数据库

软件

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 MvcShipping/MsBaseInfo/GetProParentModuTreeList 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据.NET MVC框架特点找到DSWeb.MvcShipping中对于路由的定义

```
using System.Web.Mvc;

#nullable disable
namespace DSWeb.MvcShipping;

public class MvcShippingRegistration : AreaRegistration
{
  public override string AreaName => "MvcShipping";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("MvcShipping_default", "MvcShipping/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

深入探索

安全研究工具

服务器安全服务

网络安全会议

## `GetProParentModuTreeList`

在DSWeb.MvcShipping.Controllers下找到MsBaseInfoController里的**GetProParentModuTreeList()**方法

```
public ContentResult GetProParentModuTreeList(string PARENTID)
{
  List<CustomDbParamter> dbparams = new List<CustomDbParamter>();
  CustomDbParamter customDbParamter1 = new CustomDbParamter();
  ((DbParameter) customDbParamter1).ParameterName = "@oper";
  ((DbParameter) customDbParamter1).DbType = (DbType) 16 /*0x10*/;
  ((DbParameter) customDbParamter1).Direction = (ParameterDirection) 1;
  ((DbParameter) customDbParamter1).Value = (object) Convert.ToString(this.Session["USERID"]);
  dbparams.Add(customDbParamter1);
  CustomDbParamter customDbParamter2 = new CustomDbParamter();
  ((DbParameter) customDbParamter2).ParameterName = "@strCondition";
  ((DbParameter) customDbParamter2).DbType = (DbType) 16 /*0x10*/;
  ((DbParameter) customDbParamter2).Direction = (ParameterDirection) 1;
  ((DbParameter) customDbParamter2).Value = (object) $" and PARENTID='{PARENTID}'";
  dbparams.Add(customDbParamter2);
  string str = Convert.ToString(this.Session["LANGUAGES"]);
  string prcName = "P_userRight";
  if (string.op_Equality(str, "en-us"))
    prcName = "P_userRight_Ename";
  string rptJsonResult = RptHelper.GetRptJsonResult(0, 100, PubSysDAL.GetMsSqlPrcDataSet(prcName, dbparams, "Result_Set"), "Result_Set", false);
  return new ContentResult() { Content = rptJsonResult };
}
```

深入探索

安全工具开发

VPN服务

网络安全培训

非常明显的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞：参数`PARENTID`被直接拼接进SQL语句中`$" and PARENTID='{PARENTID}'";`执行，从而导致的注入漏洞。

SQL注入检测工具

当然，此Controller下的多个方法也存在类似的SQL注入漏洞

## `GetCustomerRefList`

```
// MsBaseInfoDAL.cs
public static List<CustomerRefModel> GetCustomerRefList(string strCondition) {
    // ...
    if (!string.IsNullOrEmpty(strCondition))
        strSql.Append(" and " + strCondition); // 直接拼接外部输入
    // ...
    using (IDataReader idataReader = DatabaseFactory.CreateDatabase().ExecuteReader((CommandType) 1, strSql.ToString())) 
    // CommandType 1 是 CommandType.Text，直接执行拼接后的字符串
}
```

`condition` 参数完全受控于用户，攻击者可以构造恶意 SQL 语句，绕过正常的业务逻辑。由于是 MSSQL 环境，攻击者可以利用 `UNION SELECT` 获取其他表（如 `[user]`）的数据，或者利用 `WAITFOR DELAY` 进行时间盲注。

代码安全审计

## `GetModuTreeRefList`

```
// MsBaseInfoController.cs
public ContentResult GetModuTreeRefList(string PARENTID) {
    string strCondition = $"PARENTID='{PARENTID}'"; // 字符串插值拼接
    // 后续逻辑中虽然有 if else 判断 PARENTID 的值，但如果传入的值不匹配任何 if 条件，
    // strCondition 依然保持初始的拼接结果，并传入 DAL。
    List<ModuTreeRefModel> moduTreeRefList = DSWeb.MvcShipping.DAL.MsBaseInfoDAL.MsBaseInfoDAL.GetModuTreeRefList(strCondition, ...);
}
```

虽然代码中有针对特定 GUID 的 `if` 判断，但攻击者只需传入一个不符合这些条件的恶意字符串，即可绕过逻辑。

## `SaveUserQuerySetting`

```
// MsBaseInfoDAL.cs
public static DBResult SaveUserQuerySetting(..., string userid, string formname, ...) {
    // 虽然部分参数使用了参数化查询，但 Delete 语句是拼接的：
    DbCommand sqlStringCommand2 = database.GetSqlStringCommand($"Delete from user_query_setting where formname='{formname}' and userid='{userid}' ");
    database.ExecuteNonQuery(sqlStringCommand2, transaction);
}
```

攻击者可以通过 `formname` 参数注入恶意 SQL。由于紧接着会执行删除操作，这可能导致 `user_query_setting` 表中的数据被全部清空（通过 `1' OR '1'='1`）。

以及其他接口均存在类似的 `condition` 拼接问题，分析逻辑一致：

漏洞修复方案

* `GetPortRefList`
* `GetOurPortRefList`
* `GetOpEdiLog`
* `GetGoodsRefList`
* `GetStlModeList`
* `GetAllBANKList`
* `GetCodeRptFeeGroup`
* `GetCwAccitemsCurrencyList`

# 漏洞复现

```
GET /MvcShipping/MsBaseInfo/GetProParentModuTreeList?PARENTID=SQLI_POC&&_dc=1678901234567&page=1&start=0&limit=25 HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 /MvcShipping/MsBaseInfo/GetProParentModuTreeList SQL 注入漏洞](images/img-001-b3f4a1ee994d.webp)](https://image.mrxn.net/40d2a866e39444f98dab740acbba4193.webp)

成功延时 5 秒

网络安全

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
* [4.1.GetProParentModuTreeList](#toc-4-1-)
* [4.2.GetCustomerRefList](#toc-4-2-)
* [4.3.GetModuTreeRefList](#toc-4-3-)
* [4.4.SaveUserQuerySetting](#toc-4-4-)
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
文章标题：[东胜物流软件 /MvcShipping/MsBaseInfo/GetProParentModuTreeList SQL 注入漏洞](https://mrxn.net/jswz/dongsheng-MsBaseInfo-GetProParentModuTreeList-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-MsBaseInfo-GetProParentModuTreeList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsBaseInfo-GetProParentModuTreeList-sqli.html"),
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

编程

  

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

SQL注入检测工具


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsBaseInfo-GetProParentModuTreeList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 