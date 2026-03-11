---
title: "金和OA Budget_CostApply.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Budget_CostApply-sqli.html
asset_dir: assets/金和oa-budget_costapply.aspx-sql注入漏洞
---

# 金和OA Budget\_CostApply.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/11 13:30
* 303浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

安全运维咨询

服务器安全服务

漏洞扫描器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Budget_CostApply.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `Budget_CostApply.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **Budget\_CostApply** 的处理逻辑

深入探索

安全

VPN服务

Docker加速服务

```
protected void Page_Load(object sender, EventArgs e)
{
  Utility.RegisterTypeForAjax(typeof (Budget_CostApply));
  this.KeyCtrl("JHCostControl");
  ((HtmlInputControl) this.hidShowKyMoney).Value = this.cc.GetCkKyMoney();
  this.ToolBar1.IdeaUrl = "../../Control/";
  if (this.Request.QueryString["From"] != null && string.op_Equality(this.Request.QueryString["From"].ToString(), "GiveOutShow"))
  {
    this.ToolBar1.Style["display"] = "none";
    this.UploadFile1.ButtonAdd.Disabled = true;
    this.UploadFile1.ButtonDel.Disabled = true;
    this.UploadFile1.ButtonEditor.Disabled = true;
  }
  if (this.Request.QueryString["Projid"] != null)
  {
    string str = this.Request.QueryString["Projid"].ToString();
    this.ProName = this.costManager.GetProjName(str);
    DataRow row = this.costManager.GetProjPeriod(str).Rows[0];
```

深入探索

安全认证考试

软件

物流软件安全

跟进`GetProjName`方法

```
public string GetProjName(string pid)
{
  return this.db.ExecSQLReobject($"select projname from ProjectList  where ProjID='{pid}'").ToString();
}
```

至此，就非常明了了，参数**Projid**是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/Budget_CostApply.aspx/?Projid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA Budget_CostApply.aspx SQL注入漏洞](images/img-001-7c81b39a37ce.webp)](https://image.mrxn.net/3ebed55abb984390ac1e58516b8100b8.webp)

成功延时 4 秒

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
文章标题：[金和OA Budget\_CostApply.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-Budget_CostApply-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-Budget_CostApply-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Budget\_CostApply-sqli.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Budget\_CostApply-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 