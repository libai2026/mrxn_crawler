---
title: "孚盟云CRM AjaxCustomizeReport.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxCustomizeReport-sqli.html
asset_dir: assets/孚盟云crm-ajaxcustomizereport.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxCustomizeReport.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/18 16:39
* 624浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

软件

软件即服务

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxCustomizeReport.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxCustomizeReport.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxCustomizeReport 方法的实现如下

深入探索

服务器

CRM

数据库

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["action"];
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    this.userId = UserCookie.GetCookieValue("empId");
    Helper.WriteLog("ShowCustomizeReportData userId:" + this.userId, "ddSaas");
    this.userId = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.userId);
    Helper.WriteLog("ShowCustomizeReportData DesDecrypt userId:" + this.userId, "ddSaas");
  }
  try
  {
    string str2 = "";
    string str3 = str1;
    if (!string.op_Equality(str3, "SetQueryConditionAndControlType"))
    {
      if (!string.op_Equality(str3, "GetMouldList"))
      {
        if (!string.op_Equality(str3, "GetCustomizeReportSelectItem"))
        {
          if (string.op_Equality(str3, "GetCustomizeReportDataPage"))
            str2 = this.GetCustomizeReportDataPage(context);
        }
        else
          str2 = this.GetCustomizeReportSelectItem(context);
      }
      else
        str2 = this.GetMouldList(context);
    }
    else
      str2 = this.SetQueryConditionAndControlType(context);
    context.Response.Write(str2);
  }
```

深入探索

鉴权

SQL

SaaS

当 **method=GetMouldList** 时，进入**GetMouldList**方法

```
private string GetMouldList(HttpContext context)
{
  string mouldList = "";
  DataTable table = this.dbHelper.Query($"select * from syMouldFile where BMouldType=4 and MouldName like '%{context.Request["searchTxt"]}%'").Tables[0];
```

最终可以看到，未经过滤或参数化绑定的参数 **searchTxt** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxCustomizeReport.ashx?method=GetMouldList&searchTxt=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxCustomizeReport.ashx SQL注入漏洞](images/img-001-4ddb92dc96c3.webp)](https://image.mrxn.net/838b059cd1cc491e9eea1f2bca8da9e9.webp)

成功延时 4 秒

SQL注入检测工具

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
文章标题：[孚盟云CRM AjaxCustomizeReport.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-AjaxCustomizeReport-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-AjaxCustomizeReport-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxCustomizeReport-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxCustomizeReport-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 