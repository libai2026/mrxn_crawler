---
title: "金和OA GetTreeDate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GetTreeDate-sqli.html
asset_dir: assets/金和oa-gettreedate.aspx-sql注入漏洞
---

# 金和OA GetTreeDate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/25 13:34
* 476浏览
* [0评论](#comment)
* 17分钟阅读

深入探索

服务器

SQL

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetTreeDate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GetTreeDate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **GetTreeDate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.InitText();
  if (this.Session["UserCode"] != null)
    this.strUser = this.Session["UserCode"].ToString();
  if (this.Request["id"] != null)
    this.loadDeptChild(this.Request["id"].ToString());
```

参数 `id` 被带入`loadDeptChild`方法

深入探索

防火墙软件

编码转换工具

授权

```
public void loadDeptChild(string deptID)
{
  DataTable firstSubDeptByDeptId = new Role().GetFirstSubDeptByDeptID(deptID);
```

跟进`GetFirstSubDeptByDeptID`

```
public DataTable GetFirstSubDeptByDeptID(string deptID)
{
  DataTable firstSubDeptByDeptId = (DataTable) null;
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("select  a.DeptID, a.DeptName,case when exists(select * from dbo.department where deptparentid=a.deptid and deptdelflag=0) then 1 else 0 end as haschild ");
  stringBuilder.Append("   from dbo.Department  a left outer join dbo.Sort b on a.DeptID =b.SortObjectID  ");
  stringBuilder.Append($" where  a.deptparentid={deptID} and b.SortType = 'Dept' and a.DeptDelFlag = 0");
  stringBuilder.Append(" order by sortid ");
```

至此，就非常明了了，`id` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/GetTreeDate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GetTreeDate.aspx SQL注入漏洞](images/img-001-21ae55bb63b4.webp)](https://image.mrxn.net/dfa571224d0b42bda8d69f8c8a935475.webp)

成功延时 5 秒

代码安全审计

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
文章标题：[金和OA GetTreeDate.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-GetTreeDate-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-GetTreeDate-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKgUlEQVR4AeybgXYbuQ5Dffv//7zPGBYSPNKM7cRxfF6VExYUAHIU0YqTdvfP5XL577vx39+P7/ZR/d9WG2it2BbXP5Q7rsvt02vhRlz/UO64Lg8/7Um0+VFu5s/aZ3MN5FqzPj/lBNpArpO+PBPf+QL8nOwx41JXbo9Q630AF+CGBjYOClNUH0VyzsU7oGq9FkJx9idKfyaytg0kyZX/3gkMA4GaPMzxbKuzV4X9qc04GJ9nH5TmdWL2neX2WvNaCNXXmhCKk34W8irOPFC9YI6z2mEgM9Pi3ncCayDvO+uHnvTSgcB4Nb0L6NqM0/Xfh33mvRZC9VP+SED5oaP7wjnn/tB95l6NLx3Iqzf3L/b7kYH4lXeEUK+0PHAoDjqm/kwOvcfRHsQ/01Ne1Ti0/on4kYFcfmKn/0jPNZAPG/QwEF/JI3xk/9C/ZUDls7p8xpluDaoXYGr6W/isL7B5W+Gd5KwHVC/gtEv2mOWz4mEgM9Pi3ncCbSDA9gqCx/Bsi/lqOPPNtKyF2suZb6ZB1QEzuXHA9jU/+0z5W5NJAtUXHsNs0QaS5Mp/7wTWQH7v7KdP/qPr991wZ/fx+gjtg36lzR3ViLdHCFWr3CHPPqB8ez7XUB6g/RMEdM5e6Nz+mV5/F9cN8Wl/CJ4OBOoVMdsrlAYMMrC9WQKDlkS+mswDT9VC90Pl7iX0M5QroDyAllvYIwS25yvfx2Z+4A+oHjBilsOonw4kiz8g/ye28AdupzT7quHWA/17rV5Fsxpz0hVeJ0Lva15ehzkjdD9Ubu1RdO/Ee7VQz8oaKA5GTJ9zPwO631ziuiF5Gh+Qr4F8wBByC8OPvXB+pVwM3QeVW/M1FZpLhPJLd0Bx6dvn9iamx3xyUH3PtPTPfNahekH/lm3tK+hnJa4b8pWT/MGapweS03Tu/UG9grwWQnHQ0XXQOXnvBYx+9xJC6cod93rudageybtXovXknFtLPNPS9/RAsnjlrz+BNZDXn+m3OraBwHhV3dnXTQjlg457n9dHCFWbunorZhyUX7oDioOOWXuUw+iH13DQ+wA3WwCGvwG4MfxdtIH8Xf978GFfcRuIX3m5vxln3ZrQHNSrADpKPwrXCaFqlO/D9cnPuNSdn/lm2oyD2ps1ofsbxe3D2hFC9U29DSTJlf/eCayB/N7ZT5/c/nLRal47c1BXCzC1vUEBG7rGotdCKA90tC9RXgUc+6BrUHn2cA6lAaa2fUL/DVvPamIkwOYNqv2jVXJQPvVRQK2BtLVcHkUjIgG2ZwKXdUMun/XR/i4L+pTgNs8ta8r7SF059HqtFVmj9VHMfFD9UnOefcwlWjfndaI1YfL7HGof0G/a3qM1lE+5A0ZOz1PYI1w3RKfwQbEG8kHD0FbaQHR1FCIdWiu8ToS6gkDSW66afQDtjQsqTw8UBx23ZvEHHGuyQdehcvH3AsoL3LM2Hdi+HhP5tZi7h1A9srYN5F7x0p86gS+b20BgnNZZ15yqfea8TrSWmLrzmZ6cc/sTrSVah/r6vE6c+e9x1t0Hqj9g6gbtB7abBf0HA+hcG8hN9Vr82gkMvxhCnxZU7ukKvVMoDTDVJg+03CJ0DsZcvRX2fwWh+mYtjFzq+1x7UCQPYw8oDgrTr3oFlAYd0wfFJ7duSJ7GB+RrIB8whNxC+01dV2wfaXQOdc3SC7ecvd9FqL7uA7WGjrkP+xKtJ+ccqo/XQigOOoo/CvdPhKpNzvXJObcmXDdEp/BB0d7Uoaaae/MEoTSgycDhG3czHSTuO5Oh9937vBa6Frrf3BnCuV+9FWc9pMmjgN4PKpd+FFAe6JjedUPyND4gXwP5gCHkFtpAdP0U0K8SVC7+kXDj9MLYw74ZzmqhekBH+7LHjIOqsc+eRGtCuPWLmwWUz33S8yiXNc7bQEws/N0TaD/2ehuebiLUqwHO0T2g+9zHmhBKV+6AkbPmHonWZgjVC2iyaxtxTYDtB5Nr2j5nPotQfhj/Hsp1wpkfqla6wz6vheuG+FQ+BNdAPmQQ3sbwewjU1YKONgt1rfYhPiN16H2gcnvTZw7KA+O3BegaVJ49oDj3ElqHY00+B5TPdUdov3WvhXDcA0oDZN0C2L51Auu/Orl82MfwLcsTF57tFfpU5c2ArrlH6uag+1J3DqV77TrhjBOvsCbUWqFcAdUTEH0YQHvV2gSdg+Pc/hlqD/tI3zCQFFf+/hNoP/Z6atAnf7Yd+4V7n7h9pMdaclDPTc45jBoUBx3dFzoHt7l7PoNQPbLGzzLndaI1IYw9oLis+YUbou2tODqBNZCjk/kl/nQgeZWce59Q1w1GtEcIow7FuadQXgWUBmi5hfR9bML1j+SB7Y34Sn/7M/u6WXJw/CwoDTq61r0SoftOB5JFK3/PCbSBQE3JkxSebUG6wz6voXpB/+XOnkQYfe4hTO9RDo/1UD9F9oGqTc45lAaYehj1nH2cFae3DeSsYGnvO4E1kPed9UNPGgYCbG+MQGsAPMW1wkjyWppODvozoHL7Zuja1ODxOtcLoeqAbNdyeRSNiES8IqjhrFKb5UCrGQYyK1jc+06gDURT3gfU5JKHkUtd+Wz7UHVAk4H2ylCdoonXRGvFNR0+oWpTkFcx46D80DF9zlW/D2vQa+2B4uz5CrqXsA3kK40+qeb/ZS9rIB82yfYPVLN96QopZhrUVYUR0w+lJzfL4dgHx5r253BfKD9gqv2vzfYKge1bpnJHK7iTwG1t2me9oPzpcw6lAesfqC4f9tH++t37gj4tGHP7/CpIfESTJ2vOcnmPwnUz3ZrQOoxfi3QFjBqMnHslQvlmHJQGpNxyPVvRiGuy3kOuh/BJn2sgnzSN614eelPXtdoHsL0hAtc29WkP0DSo3Jqw3JfBA+WFwssLPuC2l57vgNK8PsJHtgHVC5ja3RsYvm5rwnVDpsf3e+Twpq4pOc62ZY/QPqjpi3NY+wpC9ZvVwqhBcdDRtbP9zDioWtcJZz7xCmszlL6P9FmDeiawfuy9nH68X2zvIdCnBM/l3ranD73eGoyc/UfoWiOMPazdQ+i1UPlZDZQHOLM1DWjvDY2MBLoOlVvOr3+9h/hUPgTXQD5kEN5GG0hem0dyN/gKQl1Z6Og+MHLejz1Cc9D95qQ79pzXQnug9zA3Q9U49rp54V7TWrxC+T6gP78NZG9a6985gWEg0KcFY/5T24R6ll5FjmefBdUj62DkUj/KvQfhkUc8VH8YUboDSvc6Uc9wDANJ48rffwJrIO8/89MnvnQgMF5LX8UZznYG1QMe+4/ssu+sX+rK0wP1LPH7SJ9zKD+c7829XCd8lHvpQPTgFfdP4Mzx0oH4VZDoh0N/dUHlM5/9QigfFIrbB5QGNGnWF2i/SUPl9rXCSKA80DHklrpHYhMnycwH/RkvHcjk+Yt68gTWQJ48sJ+2DwPJKzXLn90Q1HWc1UFp0N8kX/lMoD3WfRtxkADbt7aUZ7VQPjhG1wmzn3OoWumOYSA2L/ydE2gDgZoWPIZn24Xew5NP/4yDXgOVu8b+GdojtK7cAdULCu0RQnHQUbzC9fdQXsXMB73vTJ9xbSAzcXHvP4E1kPef+ekT/wcAAP//bOaQwQAAAAZJREFUAwAE9VitUApFCwAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-GetTreeDate-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-GetTreeDate-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 