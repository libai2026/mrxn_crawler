---
title: "孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPrice-sqli.html
asset_dir: assets/孚盟云crm-ajaxbusinessprice.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/13 08:31
* 263浏览
* [0评论](#comment)
* 46分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxBusinessPrice.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxBusinessPrice.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxBusinessPrice** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["action"];
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    this.userId = UserCookie.GetCookieValue("empId");
    this.userId = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.userId);
  }
  else
  {
    Helper.WriteLog("empID：空", "ajaxbusiness");
    context.Response.Write("-1");
  }
  string s = str;
  // ISSUE: reference to a compiler-generated method
  switch (\u003CPrivateImplementationDetails\u003E.ComputeStringHash(s))
  {
    case 315799074:
      if (!string.op_Equality(s, "insertBusiPrice"))
        break;
      this.insertBusiPrice(context);
      break;
    case 323632542:
      if (!string.op_Equality(s, "ImportBusinessPriceFiles"))
        break;
      this.ImportBusinessPriceFiles(context);
      break;
```

首先判断Cookie里的`empId`是否为空，如果为空直接响应“-1”，因此跟进`GetCookieValue`方法看下Cookie取值如何取的

代码安全审计

```
public static string GetCookieValue(string key)
{
  if (HttpContext.Current == null)
    return "";
  HttpCookie cookie = HttpContext.Current.Request.Cookies[nameof (UserCookie)];
  try
  {
    string cookieValue = "";
    if (cookie != null && JsonConvert.DeserializeObject(cookie.Value, typeof (Hashtable)) is Hashtable hashtable && hashtable.ContainsKey((object) key))
      cookieValue = hashtable[(object) key].ToString();
    return cookieValue;
  }
  catch (Exception ex)
  {
    UserCookie.WriteLog("cookie err:" + ex.Message, "ddSaas");
    return "";
  }
}
```

OJBK,看到 JsonConvert类的使用，非常明了，请求里的Cookie就是一串json，类似`{"UserId":"12345","UserName":"张三","Role":"Admin"}` 这种格式，cookie的键名就是**UserCookie**

漏洞预警服务

根据代码逻辑，我们的请求cookie只需要存在**UserCookie**=**{"empId":"xxxx"}** 这种格式就可满足条件了**。**

再看看`FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.userId)`相关解密实现

物流软件安全

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-001-b5baf86a241b.webp)](https://image.mrxn.net/37d2d83f539a49a5af5fa61288195a31.webp)

朴实无华的DES解密，key（密钥）在代码里硬编码为 **fumasoft**

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-002-27a90c9a7429.webp)](https://image.mrxn.net/243ba5b0e5fa49439479cb7210f9a17f.webp)

且一般c#的DES加密模式为**ECB，**填充模式**PKCS7，**我们也可以据此伪造要给合法的empId，比如 1 经过 des ECB PKCS7 加密后为 e0a40f1c63e6b84f。

根据参数action的值进入不同的处理逻辑，当**action=ImportBusinessPriceFiles**时，看`ImportBusinessPriceFiles`方法的实现

```
public void ImportBusinessPriceFiles(HttpContext context)
{
  try
  {
    Helper.WriteLog("ImportBusinessPriceFiles: start", "products");
    string str1 = context.Request["templateId"] == null ? "18" : context.Request["templateId"].ToString();
    int num = context.Request["Fid"] == null ? 927 : Convert.ToInt32(context.Request["Fid"].ToString());
    int int32 = context.Request["type"] == null ? 0 : Convert.ToInt32(context.Request["type"].ToString());
    Helper.WriteLog("ImportBusinessPriceFiles: templateId:" + str1, "products");
    Helper.WriteLog("ImportBusinessPriceFiles: Fid:" + (object) num, "products");
    Helper.WriteLog("ImportBusinessPriceFiles: type:" + (object) int32, "products");
    DataTable table = MySqlHelper.ExecuteDataSet(new EncryptData().DecryptString(MySqlHelper.DBConnectionString), (CommandType) 1, $"select * from Tempelate where TempelateId = '{str1}' ").Tables[0];
```

templateId 参数未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，这里需要注意数据库相关操作为MySQL数据库，而非sql server ！

编程

当**action**=**checkBusinessPrice时**

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-003-1db58491f7d0.webp)](https://image.mrxn.net/dac4ef59a6574c9aa2ecf218ea6b2f76.webp)

跟进`getEmpAllMouldByEmpId`方法

```
public string getEmpAllMouldByEmpId(string empId)
{
  if (string.IsNullOrEmpty(empId) && !string.IsNullOrEmpty(UserCookie.GetCookieValue(nameof (empId))))
  {
    empId = UserCookie.GetCookieValue(nameof (empId));
    empId = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(empId);
  }
  string empAllMouldByEmpId = "";
  if (!string.IsNullOrEmpty(empId))
  {
    StringBuilder stringBuilder = new StringBuilder();
    DataTable table = this.dbHelper.Query($" select MouldID from syLicMouldDtl where MouldKey  in (select MouldKey from syLicMouldEmp where EmpID = '{empId}')").Tables[0];
```

OK,参数**empId**被直接拼接进SQL语句执行，同样造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，还是这么朴实无华！

以及**ImportBusinessPriceToDingPan**

漏洞预警服务

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-004-ccb2a1c6d17f.webp)](https://image.mrxn.net/a8a031a1f0e84c27b8dafdd3a0e46e35.webp)

GetContactEmailByFid

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-005-6fee1820ecb0.webp)](https://image.mrxn.net/31ac55b0be5a465db3e41d364832805e.webp)

GetContacts

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-006-cdc718de23af.webp)](https://image.mrxn.net/c16b764d6b304b239f6e01906ab13b93.webp)

GetContactEmail

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-007-c74eae5249cd.webp)](https://image.mrxn.net/86f75081b8344315b0190a6aaea45897.webp)

getCustReturnValue

编程

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-008-8c7b8e5ea31f.webp)](https://image.mrxn.net/51cdf9f57bcf409d8e3febe9523df1ea.webp)

getBusinessPriceHtml

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-009-40367981825d.webp)](https://image.mrxn.net/586036e491334a7992ac38c3778d195b.webp)

moreLoad

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-010-986c5b5178c2.webp)](https://image.mrxn.net/8896b535fe9b433089954ed0ec8fac94.webp)

GetBmailByFid

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-011-c6b5e1d68d63.webp)](https://image.mrxn.net/8ac0ab679fc5451bbfe8450919d9c216.webp)

GetCqnoByFid

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-012-61b097835e61.webp)](https://image.mrxn.net/7f0f4aa3379a4cb68b5693e86f859ce2.webp)

saveBusinessPriceForPdf

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-013-cf8f455d0345.webp)](https://image.mrxn.net/b1381e096f444fc893b4d550c291c2c0.webp)

sendBusinessPriceMessage

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-014-4bc1c6e95b45.webp)](https://image.mrxn.net/8608bd7e1d8447228880afb8f6f9ae09.webp)

createShoppingCart

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-015-125404eee382.webp)](https://image.mrxn.net/4e29f6d14e88489cbc60d8220f8623dd.webp)

# 漏洞复现

> 漏洞利用需要注意，此处是MySQL数据库相关操作，并非mssql ！
>
> 漏洞预警服务

```
POST /m/Dingding/Ajax/AjaxBusinessPrice.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=ImportBusinessPriceFiles&templateId='SQLI_POC&Fid=1&type=1
```

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-016-9f213ed00f8a.webp)](https://image.mrxn.net/5ec2d10cec634f10a8eca7b78a640177.webp)

成功延时 4 秒

编程

以及 **action**=**checkBusinessPrice 时**

[![孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](images/img-017-dcdc843785f4.webp)](https://image.mrxn.net/52e1a3a5bc2e41ae95c199495a693533.webp)

通过报错注入，成功在响应里回显数据库版本信息

此类的其余诸多的[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)方法就不一一复现了

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
文章标题：[孚盟云CRM AjaxBusinessPrice.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPrice-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPrice-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPrice-sqli.html"),
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

安全工具开发

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPrice-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 