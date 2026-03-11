---
title: "金和OA AppraiseStationSetUpdate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AppraiseStationSetUpdate-sqli.html
asset_dir: assets/金和oa-appraisestationsetupdate.aspx-sql注入漏洞
---

# 金和OA AppraiseStationSetUpdate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/23 13:26
* 558浏览
* [4评论](#comment)
* 20分钟阅读

深入探索

服务器

数据库

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AppraiseStationSetUpdate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

防火墙软件

企业安全咨询

Web安全课程

根据 `AppraiseStationSetUpdate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **AppraiseStationSetUpdate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  Localization.SessionCulture((Page) this);
  this.InitText();
  ((HtmlControl) this.txt_BehaveCodeName).Attributes.Add("title", this.SelectPerson);
  if (!((Control) this).Page.IsPostBack)
  {
    this.ToolsBar1.Buttons.Add("../images/ico_28.gif", this.btnCreateColl);
    this.ToolsBar1.Buttons.Add("../images/ico_26.gif", this.btnDelColl);
  }
  ((HtmlControl) this.txt_BehaveCodeName).Disabled = true;
  if (this.Request["id"] != null)
  {
    ((HtmlInputControl) this.txt_BehaveCode).Value = this.Request["id"].ToString().Trim();
    ((HtmlInputControl) this.txt_BehaveCodeName).Value = this.Request["Name"].ToString().Trim();
    this.m_dss = this.m_AppraiseTemplate.GetAppraiseStationInfo(((HtmlInputControl) this.txt_BehaveCode).Value);
```

深入探索

漏洞扫描服务

授权

漏洞预警服务

参数 `id` 被带入`GetAppraiseStationInfo`方法

```
public DataSet GetAppraiseStationInfo(string regCode)
{
  if (string.op_Equality(regCode.ToString().Trim(), ""))
    return (DataSet) null;
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  DataSet dataSet = new DataSet();
  string str = $"Select * From  AppraiseStation Where regCode ='{regCode}'";
  DataSet appraiseStationInfo = dbOperator.ExecSQLReDataSet(str);
```

至此，就非常明了了，`id` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/AppraiseStationSetUpdate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AppraiseStationSetUpdate.aspx SQL注入漏洞](images/img-001-393ae449d073.webp)](https://image.mrxn.net/c8496455fdef4503bfc4fcdee1bd1c63.webp)

成功延时 5 秒

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[金和OA AppraiseStationSetUpdate.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AppraiseStationSetUpdate-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AppraiseStationSetUpdate-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AppraiseStationSetUpdate-sqli.html"),
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

漏洞修复方案

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALHklEQVR4Aeyci07lxhJFWfn/f+bOprRMu9x97CEEI11HqWzvR5Ubl48YGCn/vL29vX+l3ts/fYa2eufqYvflHc2Lo9+1FVdf4Tgz1z0XbSx9NflXMAv50/f8+1uewLaQP9t9u1L94MAbsPV2Xw7Xcj3feT+jflAP6l7RUlBcP1qq82gpqHyuU+ZEKB8Kk5mV+TMce7eFjOJzfd8TOCwEauuwx9UR3T5U3hwU1++6XB+u5aFysEZnit5LVIeaIdfvCJVTP8ubE6H6YY/6Ix4WMprP9c8/gW9fiG+PCPVWrL40KP9q3pw4zp1p8a/q5sT0puRQZ402lv6offX62xfy1YM8ffUEvn0hUG8RFK7enq7DPq/fESoHhfVl1H+hNCgs9fhf2PtQHAqPHaV4lmJ/foB7f//406X8O/DbF/Idh/p/nnFYiG9Bx9VDgv1b9dH3580xD3MfSjcvQumwR+eJ5mdoBl7PMNcRqk8disMe9c9wdsZos77DQmahR/u5J7AtBPbbhzlfHS0bT0H15TplPtcp2PtQ3JyYbEq+Qqh+4BBJf+pgLIRkUwv74/vFzAc+flvR+6B0eI1j37aQUXyu73sC/2TjX6l+ZKi3wFl/65tf9et3NB/sHtSZut55elNdh+qPl4I5733JfrWeT0h/mjfz04VAvRUwR9+E/nVA5fVFc1D+GbcP5nkoHT7RmSvsM6F6zevLRXXY5/VFKB8K1TvC0T9dSB/y8P/2CRwWAsetjUfwLVGDfR6K91zP63eE1/09P+PeS08uQt1DLsJeX/WbF83B3/Xb55zgYSERn7rvCfwD17bqNmGfXx0dKgeFq5w6vM69v79//BzQ81B98In9rJ074yrC52xga3PuJly8AKY/t6T9+YTkKfyi2n4OgdoaFPYzQun9rZCL9nUO1a8Pe67e+9Q7mhtxlYG615gdr+1Tk4srXR/287sO5au/wucT8urp3OBt30P6WwC1VXUR9joU9+zm5KK6qC6qQ82DQn0R5rr+DPvsWWbUYH8PKO6cMTu7NifOMivt+YSsnsxN+rYQqLfg7BxuHfZ5KA6FzjEvh70Pe25OhL2/mgfYskR7gY8/5UChDfCam+u4mgv7efaZl4+4LWQUn+v7nsDlhUBtGwrd8gqhcn5pULzn9TuaU4fql8/QHqgs7NEecyuuLva8OtR8eUf7RH2oPihUD15eSMJP/fdPYFtI32LnHkUd9tuF4lBoHoqv+sx1hOrruhyOPuw17ynCxB/+/t/Z4t/2mbdfhLovFKrPcFvIzHy0n38C20/qV28N8y37doirefpQc1bcfn05VJ98hvZAZaFQfdYzauag+kYv11C6uWhjrXQz3YeaB7w9n5C33/XPYSFuD2prHlddVBeh8lCoLkLpUNh150L5nZt/hfaY6Rxqtr4Ipfe8vgiV6xxKh0J90bkiVE4+4mEhDnnwniewLQRqa1Do1jwWlA6F3V/xrjtPXew61H263rn9QT0RXs8wl96UHF73JZsyn+uUXISaA3vUn+G2kJn5aD//BLaFZMNj9aOMXq5hv3UoHi9lP+z1eKnud55MSl2MloKaqz4ilJfcWGagfCjs+tiTa30Rqi9eSv0Mk02Zg5oDn7gtxNCD9z6BbSFQW/I4UBzmaC4bH0td1JPDfp4+lC43L0L5UDjT1USoLBSqew+x63KoPig0L/acOvDx22R5z8lFc8FtIZoP3vsEtr8x9BiwfxvUxWwxJYfKdw6lQ6G+mBkpmPvmxGRTKx4dalZys4Lyk01BcdhjvFnBPgfFvRcUtxf2XN28qB58PiF5Cr+oDr/Lmm1tPC/Mtz5mZtdQfX2+XITKOWOlwz5nPgjlQWG0saB0Z4tjJtfqHeONBTVv1GbXzoF1/vmEzJ7cjdr2PcTteRbYb1G/Y8/rq3eufhWhztHnyGfobD2YzzDXESoPe+y5zr1fx57rHD7v83xC+tO5mW8Lgc8twfr/7gOVOzu3bwlUvnP7oXy5CKWv+noOUFoi8PHzwTJwYkD1e6ZVHCrXfdjrUNx5wW0hvfnh9zyBZyH3PPflXbeF5OMyFvCW6p1mur7iq3xmp7ovF5NJyft91IPdS18q3qzipXrfLBvNXHpS0VLqYrSUfIXJpDLL2hayanr0n30C2w+GbkjM5lIeR72j/grNdz+zUyt/pTtHf4ZmMj8l79muy8Wez6yUfseel5tLb0o+w+cTMnsqN2rbQrK5sdzuqI3XZ2fu/XL7zrj36nl1UX9EPe8hjpnx2rxoXj5mx+ueW+VXuv3jzG0ho/hc3/cEtoW4LXF1JP3V1ld9q7y66HzRefpyUT2oJkYbS73j6l5d733OXun6fY66ffLgthDNB+99AqcLOdvu2fFX/XkbUr0/Wko91yl5n6ceTC6V61TPxkvFS+U6letUz0e7Uqu+rsvF2ezThcyaHu2/ewLbQvKmzMpbu1VRXbR35atD/ULNPrH7zuv+ikfvM6KNpT9que73ipbqeu/vPD2zcs4Kx55tIaP4XN/3BLa/oHLb4upIbnnlX9X7fZwr6ovO1RfVg2pitLG6vpq90u1fofey35y6qN959OcT4lP5Jbj9LsvzrLaqni2OZZ+a3HzH7stF56z69F+hszras9L1vbc59Y76KzS/8mf68wmZPZUbte17iGfoW+1vy4p3vc9zrjl5z3XfnLr5V2hPzzijozl1eZ9z5tvX0Tli950bfD4h/enczLeFZDtjeS632tFsz3VdX3SOXLSv+12X977oamK0VJ+pLyaTWuXipcyfYbIpc7lOyV/htpBXocf7uSdw+FOWt/ZtyWZT6rlO6auL6qK6mN6xznL2nWH8cW6u++zO0zOrVa7ruUeqzzAXL9W5eXV58PmE5Cn8ojosxK1lsym5Z5bHS6mL0VLyjvarJ5vq/Cxn3lywa/LMT8mTTck7Jpvq+opn1lir3Eofew8LWTU9+s88gcNC8mak3Fo/RryUvhgtJV/1JZPqvrz3n/HMsnpW3dly8Wre/o72O6/7nZvvuv3Bw0J6+OE/+wS2hfTtZVtjeSxzo5dr/VynOrevozl1eWak5N3venw1MVpqxVd6elLdz3nG0hdHL9fqHeONNfrbQkbxub7vCRwWkjdjLI82bjTX6itMJuWsnouXWvk9f4VnXspsrlPeI9cp/RUmk7LPnFxMJiVf5dSTTcntG/GwEMMP3vMEDr/t9RjZZEouuk252PXOM2usle+8jvZ2feR9ZudjNtermZ99SR3rq33HSUfl+YQcn8mtyva7LLcurk7Vfd8m9c673n3vo77i6qJzZ2hGNCNfYT9D7+t8lTcner8r+ecT4tP6Jbh9D3F7V7Gf3z7fCnnPyfXNn6F5+0X1oNoKk5nVKq/u2eTiSvce5jq+8p9PSH9aN/NtIW77DK+e1zk9ry52X97folVePWivGC3lrFyn9DvGG8u+M1zNOdNnc7eF9OaH3/MEDguZbS3aV4+X3lTvj/aqfFPtM9u5+ohmOppR7/dQ7zl18x317evYfbk4zjssxNCD9zyBf72Qcbu5Xn0Z8VK+Pbl+Vc4xL+84ztBTk/8t9v7OPZOof4aew5x8xH+9kHHYc/3vn8C3L8S3ZnW01dux6jMvOlduX1DNTEd9UV+eGSn1q5iesexTk4srPf63LyRDn/r6EzgsxLel49kt3Lp9Pa/f9avcfufLx/6ZNvN7Tu7ssSfX+mK0VM93nszf1mEhfzvgyX/vE9gW4vbP8Oz29l/NneX1r7x9PdN79cV+RvNi9+0T9eWrPnVz9on6wW0hmg/e+wSehdz7/A93/x8AAAD//ywW8YQAAAAGSURBVAMAGzVBv6FmTNIAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AppraiseStationSetUpdate-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 