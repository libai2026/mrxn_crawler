---
title: "快普M6 WebService/SeatManageService.asmx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/kuaipu-M6-WebService-SeatManageService-sqli.html
asset_dir: assets/快普m6-webserviceseatmanageservice.asmx-多处sql注入漏洞
---

# 快普M6 WebService/SeatManageService.asmx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/24 08:25
* 803浏览
* [0评论](#comment)
* 34分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

快普M6整合管理平台的[WebService](#)/SeatManageService.asmx接口下多个方法存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，绕过参数过滤机制，实现对数据库的任意查询、修改或删除操作，甚至可能获取系统控制权限。

网络服务

# 影响版本

# fofa语法

> body="Resource/JavaScript/jKPM6.DateTime.js"

# 漏洞分析

根据漏洞通告，看下 WebService/SeatManageService.asmx 里的cs引用

```
<%@ WebService Language="C#" CodeBehind="SeatManageService.asmx.cs" Class="KPMIIS.Web.WebService.SeatManageService" %>
```

ok,根据引用去找到bin目录下的**KPMIIS.Web.dll**文件，反编译后找到`WebService`下的**SeatManageService**实现

```
public class SeatManageService : System.Web.Services.WebService
{
  [WebMethod]

public string GetCallInfo(string strCallNo)
{
  DataSet dataSet = Gateway.Default.FromCustomSql($"SELECT A.CManName,A.CPosting,C.CustName FROM dbo.Common_CustomerLinkman A LEFT JOIN COMMON_CustomerToLinkMan  B ON A.CManId=B.LinkMan_ID LEFT JOIN dbo.Common_Customer C ON C.CustId=B.CUSTOMER_ID  WHERE A.COfficeTel1 LIKE '%{strCallNo}%' OR A.CMobile1 LIKE '%{strCallNo}%' ORDER BY B.IS_IMPORTANCE_LINKMAN DESC, B.IS_IMPORTANCE_CUSTOMER DESC").ToDataSet();

  public string GetCustInfo(string strCallNo)
{
  DataSet dataSet = Gateway.Default.FromCustomSql($"SELECT A.CManId,C.CustId FROM dbo.Common_CustomerLinkman A LEFT JOIN COMMON_CustomerToLinkMan  B ON A.CManId=B.LinkMan_ID LEFT JOIN dbo.Common_Customer C ON C.CustId=B.CUSTOMER_ID  WHERE A.COfficeTel1 = '{strCallNo}' OR A.CMobile1 = '{strCallNo}' ORDER BY B.IS_IMPORTANCE_LINKMAN DESC, B.IS_IMPORTANCE_CUSTOMER DESC").ToDataSet();

  private void AddPhoneRecordInfo(
  int intPhoneTypeId,
  string strPhoneNo,
  string strTelNumber,
  string strStartTime,
  string strEndTime,
  string strPath,
  int intTime,
  string strUniqueId)
{
  strPath = strPath.Replace("/", "\\");
  string empty = string.Empty;
  int num1 = 0;
  CRM_PhoneRecordInfo model = new CRM_PhoneRecordInfo();
  model.ACCOUNT = "";
  model.IS_DELETE = new int?(0);
  model.PHONE_TYPE_ID = new int?(intPhoneTypeId);
  if (intPhoneTypeId != 3)
  {
    string[] strArray = this.GetCustInfo(strTelNumber).Split(new char[1]
    {
      ','
    });
    model.CUSTOMER_ID = new int?(strArray[0].ToInt());
    model.LINKMAN_ID = new int?(strArray[1].ToInt());
  }
  if (strPhoneNo.Length > 0)
  {
    int num2 = strPhoneNo.IndexOf('(') + 1;
    int num3 = strPhoneNo.IndexOf(')');
    if (num2 > 0)
      strPhoneNo = strPhoneNo.Substring(num2, num3 - num2);
    string sql = $"SELECT csi.STAFF_ID,csi.STAFF_NAME FROM COMMON_UserPhoneNo cupn LEFT JOIN COMMON_StaffInfo csi ON csi.USER_INT_ID = cupn.USER_INT_ID WHERE cupn.PHONE_NO='{strPhoneNo}'";
    DataTable table = Gateway.Default.FromCustomSql(sql).ToDataSet().Tables[0];
```

三个方法 `GetCallInfo`、`GetCustInfo`和`AddPhoneRecordInfo`都是差不多的处理逻辑，其中都存在关键参数`strCallNo`、`strPhoneNo`，没有经过任何过滤或校验检查就被拼接进SQL语句中进行执行了，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，非常的朴实无华。

SQL注入防护

# 漏洞复现

> 漏洞复现，可以用过SOAPUI 或者 burp的Wsdler插件解析后直接测试

```
POST /WebService/SeatManageService.asmx HTTP/1.1
Host: kuaipu.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="http://tempuri.org/GetCallInfo"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:GetCallInfo>
         <!--Optional:-->
         <tem:strCallNo>SQLI_POC</tem:strCallNo>
      </tem:GetCallInfo>
   </soap:Body>
</soap:Envelope>
```

[![快普M6 WebService/SeatManageService.asmx 多处SQL注入漏洞](images/img-001-caaae7f587b8.webp)](https://image.mrxn.net/aa6690004d8840e28e86599d08ea366d.webp)

成功通过[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显数据库默认用户dbo

代码安全审计

其他两个方法的sql注入也类似，只是需要的参数不同罢了，同时给接口还支持常规的GET、POST请求方式。

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
文章标题：[快普M6 WebService/SeatManageService.asmx 多处SQL注入漏洞](https://mrxn.net/jswz/kuaipu-M6-WebService-SeatManageService-sqli.html)  
文章链接：<https://mrxn.net/jswz/kuaipu-M6-WebService-SeatManageService-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/kuaipu-M6-WebService-SeatManageService-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/kuaipu-M6-WebService-SeatManageService-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 