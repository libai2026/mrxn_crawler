---
title: "孚盟云CRM AjaxAttachment.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxAttachment-sqli.html
asset_dir: assets/孚盟云crm-ajaxattachment.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxAttachment.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/15 16:46
* 660浏览
* [0评论](#comment)
* 22分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxAttachment.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxAttachment.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxAttachment 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["method"].ToString();
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    this.empID = UserCookie.GetCookieValue("empId");
    this.empID = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.empID);
  }
  string str2 = str1;
  if (!string.op_Equality(str2, "AddMouldAttachFile"))
  {
    if (!string.op_Equality(str2, "saveAttach"))
    {
      if (!string.op_Equality(str2, "uploadFileToOss"))
        return;
      this.uploadFileToOss(context);
    }
    else
      this.saveAttach(context);
  }
  else
    this.AddMouldAttachFile(context);
}
```

当 method=saveAttach 时，进入saveAttach方法

SQL注入检测工具

```
private void saveAttach(HttpContext context)
{
  Helper.WriteLog("savePriceAttach进入方法", "products");
  try
  {
    UserCookie.GetCookieValue("corpId");
    string str1 = context.Request["FUIDs"] == null ? "" : context.Request["FUIDs"].ToString();
    string SQLString = $"SELECT A.*,B.DocExtDescrip AS FileTypeName,C.CNEmpName AS OwnerName,\n          D.CNEmpName AS KeyInName,E.CNEmpName AS NearEditEmpName \n          FROM dcFileMouldRelation F \n          JOIN dcFile A(nolock) ON F.FileFUID = A.FUID \n          LEFT JOIN dcDocType B(nolock) ON upper(A.FileType)=upper(B.DocExtSign) \n          LEFT JOIN bfEMP C(nolock) ON A.OwnerID=C.EmpID \n          LEFT JOIN bfEMP D(nolock) ON A.KeyInID=D.EmpID \n          LEFT JOIN bfEMP E(nolock) ON A.NearEditEmpID=E.EmpID \n          WHERE F.MouldID = '{(context.Request["MouldID"].ToString() == null ? "BF001" : context.Request["MouldID"].ToString())}'  and  A.FUID='{str1}'";
    if (((InternalDataCollectionBase) this.dbHelper.Query(SQLString).Tables[0].Rows).Count <= 0)
```

未经过滤或参数化绑定的参数 MouldID 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxAttachment.ashx?method=saveAttach&MouldID=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxAttachment.ashx SQL注入漏洞](images/img-001-5b285b2a2c7a.webp)](https://image.mrxn.net/113a076a70c04b90a45d2687c0082c9c.webp)

通过报错注入 成功在响应回显数据版本信息

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
文章标题：[孚盟云CRM AjaxAttachment.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-AjaxAttachment-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-AjaxAttachment-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxAttachment-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxAttachment-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 