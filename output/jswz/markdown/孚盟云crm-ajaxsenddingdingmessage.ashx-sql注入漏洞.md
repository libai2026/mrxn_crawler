---
title: "孚盟云CRM AjaxSendDingdingMessage.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxSendDingdingMessage-sqli.html
asset_dir: assets/孚盟云crm-ajaxsenddingdingmessage.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxSendDingdingMessage.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/22 08:26
* 608浏览
* [0评论](#comment)
* 28分钟阅读

深入探索

SaaS

SQL

软件即服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxSendDingdingMessage.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxSendDingdingMessage.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 **AjaxSendDingdingMessage** 方法的实现如下

```
try
{
  string empId = context.Request["empId"] == null ? "" : context.Request["empId"];
  if (string.IsNullOrWhiteSpace(empId))
  {
    o.Status = "E";
    o.Message = "empId is empty";
    context.Response.Write(JSON.Encode((object) o));
  }
  else
  {
    string str = context.Request["action"] == null ? "" : context.Request["action"];
    if (!string.IsNullOrWhiteSpace(str))
    {
      if (string.op_Equality(str, "SendDingMeg_Mail"))
        this.SendDingMeg_Mail(context, empId);
      else if (string.op_Equality(str, "StopSendDingdingMessage"))
        this.StopSendDingdingMessage(context, empId);
      else if (string.op_Equality(str, "GetSendDingdingMessageFlag"))
      {
        this.GetSendDingdingMessageFlag(context, empId);
      }
      else
      {
        if (!string.op_Equality(str, "SaveSendDingdingMessageFlag"))
          return;
        this.SaveSendDingdingMessageFlag(context, empId);
      }
    }
```

深入探索

编码转换工具

安全研究报告

网页浏览器

当 **method=SendDingMeg\_Mail** 时，进入**SendDingMeg\_Mail**方法

```
private void SendDingMeg_Mail(HttpContext context, string empId)
{
  ResultMessage resultMessage = new ResultMessage();
  ResultMessage o = this.SendDingMeg_Mail(context.Request["agentId"] == null ? "" : context.Request["agentId"], context.Request["headText"] == null ? "" : context.Request["headText"], context.Request["bodyTitle"] == null ? "" : context.Request["bodyTitle"], context.Request["bodyContent"] == null ? "" : context.Request["bodyContent"], context.Request["bodyFormList"] == null ? "" : context.Request["bodyFormList"], context.Request["messageUrl"] == null ? "" : context.Request["messageUrl"], empId, context);
  context.Response.Write(JSON.Encode((object) o));
}
```

跟进 **SendDingMeg\_Mail** 方法

```
public ResultMessage SendDingMeg_Mail(
  string agentId,
  string headText,
  string bodyTitle,
  string bodyContent,
  string bodyForm,
  string messageUrl,
  string empId,
  HttpContext context = null)
{
  ResultMessage resultMessage = new ResultMessage();
  try
  {
    object single = this.dbHelper.GetSingle($"select SendCount from sySendDingdingMessage where EmpId = '{empId}' and SendDate = '{DateTime.Now.ToString("yyyy-MM-dd")}'");
```

最终可以看到，未经过滤或参数化绑定的参数 **empId** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他当 action=**StopSendDingdingMessage**、**GetSendDingdingMessageFlag**和**SaveSendDingdingMessageFlag**时，均存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxSendDingdingMessage.ashx?method=SendDingMeg_Mail&empId=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxSendDingdingMessage.ashx SQL注入漏洞](images/img-001-eb88e358ac58.webp)](https://image.mrxn.net/d2fb6f8292614538a29fa33e438df803.webp)

成功通过报错注入在响应回显数据库版本信息

SQL注入防护

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
文章标题：[孚盟云CRM AjaxSendDingdingMessage.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-AjaxSendDingdingMessage-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-AjaxSendDingdingMessage-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxSendDingdingMessage-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxSendDingdingMessage-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 