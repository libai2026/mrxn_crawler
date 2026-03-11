---
title: "红帆ioffice MobileBind.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-MobileBind-sqli.html
asset_dir: assets/红帆ioffice-mobilebind.aspx-sql-注入漏洞
---

# 红帆ioffice MobileBind.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/29 08:20
* 713浏览
* [0评论](#comment)
* 34分钟阅读

深入探索

鉴权

身份验证

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

红帆iOffice的/ioffice/prg/Mobile/Base/MobileBind.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

SQL注入防护

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`MobileBind.aspx` 里引用的代码在哪里（Inherits）

深入探索

sql

SQL

在线安全工具

```
<%@ Page Language="vb" AutoEventWireup="false" CodeBehind="MobileBind.aspx.vb" Inherits="Mobile.MobileBind"
    MasterPageFile="~/prg/set/ioPage/ioPageEdit.master" %>
```

去bin目录找到`MobileBind.dll`后编译打开，看`MobileBind`它的实现逻辑

代码安全审计

```
public class MobileBind : WebPageBase
{
[field: AccessedThroughProperty("txtUDIDReqHisID")]
protected virtual TextBox txtUDIDReqHisID { get; [MethodImpl((MethodImplOptions) 32)] set; }

private bool SaveData()
{
  DataTable dataTable = Mobile.Mobile.GetclientUDIDReqHisByID(this.txtUDIDReqHisID.Text);
  if (dataTable.Rows.Count > 0)
  {
    switch (Mobile.Mobile.bindClientUDID((Array) new string[2]
    {
      Conversions.ToString(dataTable.Rows[0]["LoginID"]),
      Conversions.ToString(dataTable.Rows[0]["UDID"])
    }))
    {
      case -2:
        Page page1 = ((Control) this).Page;
        pf.ShowMessage(ref page1, "不允许绑定重复设备");
        ((Control) this).Page = page1;
        return false;
      case -1:
        Page page2 = ((Control) this).Page;
        pf.ShowMessage(ref page2, "当前登录号只允许绑定一个移动设备");
        ((Control) this).Page = page2;
        return false;
    }
  }
  return true;
}
```

深入探索

网络安全培训

文本剥离工具

编程语言教程

最开始的一些变量定义，前端按钮`cmdUDIDReqHis`以及`cmdClearAll`

[![红帆ioffice MobileBind.aspx SQL 注入漏洞](images/img-001-9546457d019b.webp)](https://image.mrxn.net/f8dee53ed1274dc68c09aae5b84aba08.webp)

对应后端的两个逻辑

漏洞预警服务

```
private void cmdUDIDReqHis_Click(object sender, EventArgs e)
{
  this.SaveData();
  this.BindDataGrid();
}

private void cmdClearAll_Click(object sender, EventArgs e)
{
  this.ClearSaveData();
  this.BindDataGrid();
}
```

跟进`SaveData`看下

```
private bool SaveData()
{
  DataTable dataTable = Mobile.Mobile.GetclientUDIDReqHisByID(this.txtUDIDReqHisID.Text);
  if (dataTable.Rows.Count > 0)
  {
    switch (Mobile.Mobile.bindClientUDID((Array) new string[2]
    {
      Conversions.ToString(dataTable.Rows[0]["LoginID"]),
      Conversions.ToString(dataTable.Rows[0]["UDID"])
    }))
    {
      case -2:
        Page page1 = ((Control) this).Page;
        pf.ShowMessage(ref page1, "不允许绑定重复设备");
        ((Control) this).Page = page1;
        return false;
      case -1:
        Page page2 = ((Control) this).Page;
        pf.ShowMessage(ref page2, "当前登录号只允许绑定一个移动设备");
        ((Control) this).Page = page2;
        return false;
    }
  }
  return true;
}
```

**txtUDIDReqHisID**被带入`Mobile.Mobile.GetclientUDIDReqHisByID` 方法，跟进看下

编程

```
public static DataTable GetclientUDIDReqHisByID(string ID)
{
  return SqlData.ExecuteDataset(Globals.ConnectString, (CommandType) 1, $"select * from clientUDIDReqHis where ID in ({ID})").Tables[0];
}
```

ok,到这里，漏洞成因就非常明了了，从前端TextBox获取的**txtUDIDReqHisID**最终经过一系列赋值传递后被直接拼接进`$"select * from clientUDIDReqHis where ID in ({ID})"` sql语句里，全程无过滤或者校验，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类

```
POST /ioffice/prg/Mobile/Base/MobileBind.aspx HTTP/1.1
Host: ioffice.mrxn.net
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=ctl00%24cntForm%24cmdUDIDReqHis&__EVENTARGUMENT=&__VIEWSTATE=xxxx&__VIEWSTATEGENERATOR=xxxxx&btVerify=&ctl00%24cntForm%24txtUDIDReqHisID=SQLI_POC&ctl00%24cntForm%24cmdUDIDReqHis=Button
```

[![红帆ioffice MobileBind.aspx SQL 注入漏洞](images/img-002-0c02a6f46b34.webp)](https://image.mrxn.net/111c291fbc9b41e4bc7c78f2ccd8428d.webp)

成功利用报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据库用户信息

网络安全

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[红帆ioffice MobileBind.aspx SQL 注入漏洞](https://mrxn.net/jswz/ioffice-MobileBind-sqli.html)  
文章链接：<https://mrxn.net/jswz/ioffice-MobileBind-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ioffice-MobileBind-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKqklEQVR4AeyagZbbOg5Dc/v///zWMB8kRpJlZ5qJs7vqCQsKACmPGE3aTv88Ho9//jb++feX+/y73OFVzn7h3mD7TbliS6cveX4S06ab6J5beviy529RA9l6rNe3nEAZyDb6xysx+gJcnzVzwAMirEOsgeHeEPrID6FBRe+V0bXGrDm3JoTaDyKf+VTThv1XMdeXgWRy5fedQDcQiHcFjHH2qNDX2J/fLSMOotaaMNe0ufQ2IHpAxVkdVB9Ebn/uDaFlbuTLunKIOhijPG10A2kNa/3ZE1gD+ex5n+721oH4Gmf0E0C9ttatZYTqMw+Vg8itvQP9PEKI/srbgNCg4jv2zz3eOpDceOU/O4G3DgTqOwciHz0W9JrfjSO/tRGO/DMOYm9gZit/RAdKPi14k/jWgZRnWsmPT2AN5MdH9zuF3UBG3xYyN3uM7HMOceVHdRAaMJIvcd5H6ALlDqB8ywFsOUXXH+Fpg81wVGt+s3SvbiCdYxEfPYEyEODpnQTz9egpIWpGmt8VQuvKHRC1XgshOPsh1oCpp2dWjQIovNYKFyh3mDtDiH5nPusQfriGrhOWgWix4v4TWAO5fwZPT/DH1/dv8KnjtoB6Vd13o8vLHPQ+OOZKg4MEotb9hfDMjUohPFB/DJB96qOYcdLfEeuG5FP+gvzlgUB9N0Hk/jpG7xBrEF7A1NMPpUzmHuaMWQP2D25rQuvKHeYg/FDRnhFC74Oecy30GrzOvTwQP8AN+H+xZRkIxDTzVw09Z93vPKE5CD/0aI8QQlfugOCgojXtofBaqHUbELXSHRBc69Xanneg+jkg9hz1tUdoXbmjDMTiwntPYA3k3vPvdp8OxNcI4goCpQGwf6hCRfuLaUvMZdzoSy+I3jZDrKGiNaH3gLEuD1TNfvFXwn4hRB/XQawBU6cI7GeYjdOBZOPKP3MCf+B5ShBrqJgfRe+Oo7Av6+ag7weVc439VxFqj1kNhM/7CEd+OPZBaEApBfZ3ufrNAsJXCg+SdUMODuYueg3krpM/2Hf6b1muyVfRHMQVhIozbdRjxLmH0LryNkYaxLNkr33GrEH4rQmz3ubSjwKiF9CW7WvX7YvJb+uGTA7nDmn6oe6pAvsHF1Ce0ZrQJLD7xLUBoQG2PyGw12YSnrncM/ucZ905RA/o0R7XZ4Ten/VZDn0tBJfrRvuvG5JP6AvyNZAvGEJ+hG4gvkZCG5U7zEFcQcBU+ef0QmwJsH8rcn3GTS6vzDu3CNEDerQnI1Rf5q/k7d6qGXFQ94D6gy15VaNQ3ob4WXQDmZmX9vsn8PJAIN4Z7eS1htCgongFVA4iz18eBAcVrau+jZE242YazPeE0N3jDP2sEHVAKQH27xgwxpcHUjqv5FdOYA3kV471503L39RhfIXgmZ9dR2v5cSDqMzfKXTvCkX/EQb+X+9kP4YGK9gih8hC5eIV7CLVWKG8DnuuOfOIVuX7dkHwa78t/3KkMRJNSjDqJd1j3WgjxjoBAezLK1waEHyhWoPvQswhVM3eGEDXeO/vNQXiAIlsTAt0zQXAugFgDpoY1RdwSYPdsaXmVgRRmJbeeQBkI9NPSu0MxekIIP9DJqmmjM21E9mzL/ZU558D+TvJauJu33yA0qH852+juBeHrhIZQbwWEH2gcz0t5Fc9sv5JHkRWtFZkrA8nkyu87gTWQ+85+uHMZiK5OG64A9m8ZUDF77TPntRCiRnkbEBpQJKDbq4gpGe1lGWoPc/ZnhPDZkzH7nI906HuM/BA+a0LouTKQvNnK7zuBMhCIaeVHgZ6zDqEBpso7uxApAYoOkSd5mOpdpBiJcK1HWwtRB7TS4RrYn13P4rDZ64wzDaIXjP8QUgbiJgvvPYE1kHvPv9t9OhBfw65qI6wJt+X+Uq6A/lqKd+zm7TevhRA1yh3wzG0l5WVPIbYEwr+l3QuOtc7cEN4LogdQHMD+7awQWwLBQY/uJdys3Ws6kM69iF8/gTIQTUwB/VTzU8ijgOrTWmGfcoc5OPbL0/qPOPEKiH7Kr8TV/hB9oUf3EELoyhUQaxh/WMujgOobPXcZyEhc3OdPYA3k82c+3bH7j3K6VrNwt+wxZ4R6LSFya0IIDiqKV8AxJ92R929ze4TWlLcBsZc9R+g6CD9gqmCuBQ4/6LPPxRB+4LFuyOO7fpUf4c4eC+oE7YPKQeTWRu+Cq5x7COG5L8QaKsrXxmgve7Lm3JoQordyh30ZrRkh6gBT5f+pqa6QKQG6m7RuSDqgb0jLZwj004LgNGGHH9proTkIP1QcaSMOosaaUL2PQroCog7Q8jSA/V0JFC9QOO9XxJTANZ9LoPrNZRztdcMNyY+08vYE1kDaE7l5XT7UR9fHHNSrB33ur8F+r4XmMoo/ipEPzvdUnXtC9bec12cIfQ/t4YDQR33sGeGZf92Q0QndyJUP9VefYTb9rI36Zr3NId55QCltPXldTCk5020F9g9zrzPmHhA+qGg917Q5VD/0uf1QtXVDfCpfgmsgXzIIP0b5UDdxhr6qUK9ZWwPHmrwQunIHBOf+QgjOnozQaxAc9Kh+itzDuXgHvFYL4Xe9EHrOe53huiFnJ/RhvXyoQ0x1tL+m7oDweS2E4Ea1EBpUVI0CKjeqlUdhDapfvMKaUGuFcofWinadOWtC8W1A7Jt5eOZU2waEB2ilw/X/zA05/Ar/y4Q1kC8bWDcQYP+zOTB8VF9boPNBcPYcIYQvb2Bv5pxD+O0RWssIvQ+Csw9iDfVn31C5mc9aRojazDnXc84C+tpuIG628J4TKAPxJPNjQD9B6/aP0J4zzLX2QuwJFe2Dytmf8arPNRD9XCe0ptwB4YOKrQ+q5jp7hBC68jbsF5aBtKa1vucE1kDuOffDXbuB6No4XAVx3WCM9hmh+kZc298eoTWh1gqIfsrbgNCAIqm2DYstrzVQ/oACfe7aEUL4swbBQUXto4Cey7XdQLK48s+fwPTfsjTRK+HHhpi+10cIxz4IDSjlo2co4sUE6G7BqNR7zTR5rCs/CnuEEPtnr/g21g1pT+Rp/flF929ZEJOE6+jHztN3DtHH64wQGlR0L6G9UHV4zu0RqkYB1aO1QnobED7pDug519kzQog6YCQXDig3tZApWTckHcY3pGsg3zCF9AxlIL6WVzH1KCnEdSxESiA0qJj3StYuzT7nNkHtB5FbE8IzB7EGJO/hnsKdaH4DyrcZiLyxnP63Ufu1h8McRE9g/Wfrx5f9KjfEzwV1WtDn9o2wnXz2WBNmvs2lO6DfH4Jznb0ZrQnNw3Nd1pTPwj1GHoi+0OPIP+LcX9gNZFSwuM+dwBrI58760k4fGwjUK+0ng56zJtQVVihXKHdofRT2CO1R3gbU/SFy+zNCr7W98tq1mXMO0QvG+LGB+CEXPh6zM/iVgUCd/mxzv2uEIx9EH+kKiDVQ7ED5I6lJqBwc5+qpcJ1Q6zbEHwX0/e2FqpnLvUfcrwzEGy18/QTWQF4/s1+t6AaSr9Qof/Vp3OPVOvnbWq+PUDWKI73lIb6lqOZK5Hr7M9fm9ggh9oKK9kPluoGoeMV9J1AGAnVKcJ7PHtmTF9qnvA1rQmtQ9xZ/FBC+rENwcA29Z+7hHGqPqz6oNYBbnaL7C8tATquW4SMnsAbykWO+vsl/AAAA//+k2hXeAAAABklEQVQDACNoIaFvb3e7AAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ioffice-MobileBind-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 