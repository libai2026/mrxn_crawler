---
title: "孚盟云CRM AjaxProductTemplateList.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductTemplateList-sqli.html
asset_dir: assets/孚盟云crm-ajaxproducttemplatelist.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxProductTemplateList.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/23 16:18
* 724浏览
* [0评论](#comment)
* 28分钟阅读

深入探索

SQL

鉴权

CRM


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxProductTemplateList.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

网络安全课程

网络安全会议

安全工具开发

直接看 AjaxProductTemplateList.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxProductTemplateList 方法的实现如下

```
      string str = context.Request["method"].ToString();
      if (!string.op_Equality(str, "LoadAllProductTemplateList"))
      {
        if (!string.op_Equality(str, "AddNewPrjTemplate"))
        {
          if (!string.op_Equality(str, "SendMail"))
          {
            if (!string.op_Equality(str, "DeletePrdTemplate"))
            {
              if (!string.op_Equality(str, "GetPrdTemplate"))
                return;
              this.GetPrdTemplate(context);
            }
            else
              this.DeletePrdTemplate(context);
          }
          else
            this.SendMail(context);
        }
        else
          this.AddNewPrjTemplate(context);
      }
      else
        this.LoadAllProductTemplateList(context);
    }
```

当 **method=SendMail** 时，进入**SendMail**方法

```
private void SendMail(HttpContext context)
{
  InfoMessage infoMessage = new InfoMessage();
  try
  {
    string Fid = context.Request["fid"] == null ? "" : context.Request["fid"];
    string str1 = context.Request["templateId"] == null ? "" : context.Request["templateId"];
    string str2 = context.Request["mailTo"] == null ? "" : context.Request["mailTo"];
    string empty = string.Empty;
    if (!string.IsNullOrWhiteSpace(str2) && str2.IndexOf('@') > 0)
      empty = str2.Split(new char[1]{ '@' })[0];
    string toName = $"{str2}|{empty}";
    DataSet dataSet = this.dbHelper.Query("select  ID,Subject,ReportId,AttachFormat,TemplateContent   from  bpProductTemplate where id= " + str1);
```

最终可以看到，未经过滤或参数化绑定的参数 **templateId** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

**DeletePrdTemplate** 方法存在同样的sql注入漏洞

SQL注入检测工具

```
private void DeletePrdTemplate(HttpContext context)
{
  InfoMessage infoMessage = new InfoMessage();
  try
  {
    if (this.dbHelper.ExecuteSql("delete from  bpProductTemplate where id = " + (context.Request["templateId"] == null ? "" : context.Request["templateId"])) > 0)
```

**GetPrdTemplate** 方法也存在同样的SQL注入漏洞

```
private void GetPrdTemplate(HttpContext context)
{
  InfoMessage infoMessage = new InfoMessage();
  try
  {
    DataSet dataSet = this.dbHelper.Query("select  ID,Subject,ReportId,AttachFormat,TemplateContent  from  bpProductTemplate where id = " + (context.Request["templateId"] == null ? "" : context.Request["templateId"]));
```

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxProductTemplateList.ashx?method=SendMail&templateId=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxProductTemplateList.ashx SQL注入漏洞](images/img-001-07089b64387f.webp)](https://image.mrxn.net/3a096792e4f64e39953c274fbf4af5da.webp)

通过报错注入，成功在响应里回显数据库版本信息

代码安全审计

**method=DeletePrdTemplate**与**method=GetPrdTemplate**亦如此，就不在此赘述了。

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
文章标题：[孚盟云CRM AjaxProductTemplateList.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductTemplateList-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductTemplateList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductTemplateList-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductTemplateList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 