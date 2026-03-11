---
title: "金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForCenterBudgetDecompose-sqli.html
asset_dir: assets/金和oa-ajaxforcenterbudgetdecompose.ashx-sql注入漏洞
---

# 金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/24 13:05
* 290浏览
* [0评论](#comment)
* 33分钟阅读

深入探索

云安全解决方案

企业安全咨询

Windows安全工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForCenterBudgetDecompose.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

漏洞扫描器

漏洞扫描服务

数据库

根据 `AjaxForCenterBudgetDecompose.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForCenterBudgetDecompose** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["strType"];
  string strYear = context.Request["strYear"];
  if (string.op_Equality(str1, "getBudgetTime"))
  {
    string strDeptId = context.Request["strDeptId"];
    string type = context.Request["type"];
    string timeType = context.Request["TimeType"];
    context.Response.Write(this.DataPeriodList(strYear, strDeptId, type, timeType));
  }
  else if (string.op_Equality(str1, "getDectomposeDepartment"))
  {
    string strDeptId = context.Request["strDeptId"];
    context.Response.Write(this.DataDectomposeDepartment(strDeptId));
  }
  else if (string.op_Equality(str1, "getBudgetManage"))
  {
    string strDeptId = context.Request["strDeptId"];
    string strTime = context.Request["strTime"];
    string decomposeMoneyInfo1;
    string decomposeMoneyInfo2;
    if (string.op_Equality(context.Request["type"], "Center"))
    {
      decomposeMoneyInfo1 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "Company");
      decomposeMoneyInfo2 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "Center");
    }
    else
    {
      decomposeMoneyInfo1 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "center");
      decomposeMoneyInfo2 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "Department");
    }
    Decimal num = Decimal.op_Subtraction(Convert.ToDecimal(decomposeMoneyInfo1), Convert.ToDecimal(decomposeMoneyInfo2));
    string str2 = $"{Convert.ToDecimal(decomposeMoneyInfo1):N2}".ToString();
    context.Response.Write($"{str2}|{$"{num:N2}".ToString()}");
  }
```

当 `strType=getBudgetTime` 时，**strYear**、**strDeptId**、**type**被带入`DataPeriodList`方法

```
protected string DataPeriodList(string strYear, string strDeptId, string type, string timeType)
{
  string str1 = string.Empty;
  DataTable budgetTime = this.bdDao.GetBudgetTime(strYear, strDeptId, type);
```

跟进`GetBudgetTime`方法

```
public DataTable GetBudgetTime(string strYear, string strDeptId, string strType)
{
  this.strSql = $"select distinct DecomposeTime from DecomposeList where DecomposeState = 0 and DecomposeYear = {strYear} and DecomposeType = '{strType}'";
  if (!string.IsNullOrEmpty(strDeptId))
  {
    BudgetDecomposeDao budgetDecomposeDao = this;
    budgetDecomposeDao.strSql = $"{budgetDecomposeDao.strSql} and DeptID in ({strDeptId})";
  }
  this.strSql += " order by DecomposeTime asc";
  return this.db.ExecSQLReDataTable(this.strSql);
}
```

参数**strYear**、**strDeptId**、**type**被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

整体执行流程如下，当中其他几个方法也存在同样的[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，就不赘述了

代码安全审计

[![金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞](images/img-001-cf4bbfa84e5d.webp)](https://image.mrxn.net/e895bcc069c84779acf816225988a8b0.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/AjaxForCenterBudgetDecompose.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getBudgetTime&strDeptId=1&strYear=2012&type=SQLI_POC&TimeType=1
```

[![金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞](images/img-002-927c26c90880.webp)](https://image.mrxn.net/ea8a5fa734c74bada80ec0476dd770d1.webp)

成功延时 4 秒

漏洞修复方案

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
文章标题：[金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AjaxForCenterBudgetDecompose-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AjaxForCenterBudgetDecompose-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALqklEQVR4AeycAXLjxg5E9XL/O+d/uPMoAuRI8u7GUlWoCtzTjQY4HpB2pN3av26329+/En+Plz2GfOj93fz0P+JzDyuuvsJ5DX1Tl8+8/FewBvL/uuu/TzmBbSD/n/btlZgbB27AVgvh02dvSB6C6vohOgTVReg6hMN6DxDPvNbkq2vog/SBjtZNtO4Z7uu2gezFa/2+EzgMBPr0IXy1RacPj32z3rqVbh7SF4L6IVxfIXRNb+Uq4Dw/fXIRel31qjD/DCH10PGs7jCQM9Ol/dwJ/LGB1B1Tsdo65O4oTwWEQ7C0CgiH4OxXngp1iA/uv0PMiRCPXITo1a9CfWLlKiD+VX7qv8L/2EB+5eJXzfEE/rWBQO6murP2AV0/binKvma/htTH1b9CchC0TpcckleHcAjqMy9OfXJ9v4P/2kB+Z1P/5drDQJz6xNUhQe4qCH7V/V1v0FMB0SEY9fb13gXuP/cheeshHIK38dJ3hsN6eI90VrPXoF8TwqHjvM6K73vv12f+w0DOTJf2cyewDQT69OGcr7bm5CF1cv0rDt0PnVu/QogfWFmWT6MFwJdHvsL5PeiD83qIDo/RPoXbQIpc8f4T+Mupfxfn1iF3gX2+m9e/qjc/UX/hzEH2NHU5JF+1Feq1roCeh871T6zaX43rCZmn+Wb+dCCQuwLOcd4Jfj8Q/8xDdH3moesQ/iwP8cEdZ2+5aE853GvhvjY/Ee4eYKa/fh8BGx4M/wgQzz/0C54O5Mt1ffmxE9gGAn1a0Ll31USIDzrq8zuB5KduXh3Ofea/g3DeC7puz7mXla5P1Afpqy7CuT7rgNs2kNv1+ogT+AsyvTktubuE+KCj+RVC/PaDcP0QDsGpy2+329cSzn3AV/7RF+Dr5/r0wLmuD3re70XUt8JnPvOF1xOyOsU36dv7EOh3gfupqVVMXlrF1OWQfuWpgHDzYuUqJi+tQh16PYSXx4Bo1ojQ9ZVffVW30uG8v/2g5yEcjng9IZ7yh+Dhd8hqX3PakOlOvz4R4pOLEN36qUPPT9+ZX4+oZ+IqD+fX1P+n0X3t+15PyP40PmC9DQRyd5xNrfYJr+UhvqqpmP2g56HzqtkHJL/qo164r6s1pBY6Vu6VqJ4VeiF95GJ5KuQQHwQrV2G+1hWTl7YNxOSF7z2BbSA1nQrIVFfbgsf56lEB3QfhldvHvM4+V2vzkHr5GZa/AuKt9VlYC/HJVzh76INer8+8HLoPwiGov3AbSJEr3n8C20DgOK2z7Tl1c3IReh8IN2/dM4TUveoDnlm3PPD1jv1rT7s//9cAyUNH86s68yuE9FvlS98GUuSK95/A9k59bgXOpwnf05/19W6D877P6vd5SI/ZE6LrNS+f+CwP6bfyrXSvM/OQfsD1ae/tw17bO/Vn+3Kq4vSri+blkLtAbh66Dp1P/+T2KTQHvUflKiA6BEurgHDrS9uHOsRnDsKho3nRehHil+/x+h3iqX0ILn+HzP1BpgpBp7ryTV0OqYegumhf6Hn16VMvNCdC76E+sWor1OFxXXkr9Ne6Qi5C+kBH82d4PSFnp/JGbRtITbjCvdS6AjLdZzrEVzUV+sXS9jF1OfQ+ED7z8j1C9+5ztd5fv9alVUDqIFi5ispVQPRaV0B4eSpKeyXKW6EX0gfuuA1E04XvPYFtIJAp1QQrIHxuD7oO4VVTMf2Tw7kfug7hs/4Rr+s/CkhP6DhrVtdY+SD9zAOnnwRAfLO/dYXbQKbp4u85gcP7EMgUa1oVc1ulnYU+SP2Kq4vQ/eqvIqQejmgPSO5s36VB8hC0TixPBSQPHStXAdGtg87Vy7sP9cLrCalT+KA4DMTJrfYImTp01D/r5RC/XL+oDvFNXS5C96nvEboHHvN97dnaPc4c9L4zL7ce1v7DQCy+8D0nsBwI9Ck63YmrbeuD9JHrh65DuHkRokNQ3X5nOD2TQ3rNWn2Q/IqrT5z95NM3OeR6wPVp7+3DXttnWU4TMq3VPuFx3jqI79W++qyXi+oTIdcBZurAga/3B4fEiwKk/tU9zbaQ+qnv+fJH1t50rX/uBK6B/NxZv3Sl5UDqsayYXUqrmDr0x7E8FdD1WTd51VRMfcXLa0wP5NrmJ0Lys2765PrgvM789Ku/gsuBvFJ8ef78CRwGspou5K6Ajm7JOkh+6ubVReh+9YmzHlIHR7T2WY0+SA+5CNEhOPtNDvFBR/tNv/oeDwPZJ6/1z5/A8sNFyJTdktMV1Seu8pB+ENQnzj4QnzqE638FITX2EK2dfKXrg8f9Zr11Kx2O/a4nxFP7EHw6kDldyFRXOiQPQb9P/SL0vD7oOnSu7xFCaua15LMW4leHcAiqWy+qw2MfnOett1/h04FYdOHPnMD20Qn0KXp56HpNscK8WFqFXIRer17eCjnEV1qFeq0r5BCffI+QXPkrIHzv2a/LU6EG8ZdWoT4R4pv65PCab193PSH70/iA9TaQuiPOwj1Cpg1B9Yn2mDpYNzPnfNVHHZ730yvCeY150R1NDr0eOrduon2g+9X3/m0ge/Fav+8EDgOBPsW5tbOplgdSB8HS9mEdJA9BPas8dN/0ywvtUesK6LXmIToEy/sorNPzjEP6rnyQvP0gHLj+gOr2Ya/DE+L+IFOTO23ouvmJ+kXodVOH5NVnPznEJ98j9NzsBT1vLUSHoLoIXYfw2V//CiF15iHcPoXLgVh04c+ewPZZFhynVRNzO9Dz0Hl5K/SLEJ+8PBXwPb1qKuwDqYc7rnLqVX8W5idCeqtbK58I3W8euv6oz/WEeGofgttAnBr0abrPmZ8cUjd160XoPv3mxanDeZ2+QmsnQmqnLq/afaiL5uQr1CdCrisXoev7fttA9uK1ft8JbJ9lvboFp7zyQ6Zvfvrl0H36X0VIPQTh/g/7e42JcPcCTy9lPfD114cg+KwQug/CIfio/npCHp3OG3KHgXhXuJfJoU955ieH7ofw6ZvXg/jURTjXzRfCY8/q2lW7DzjvM+shPgjue9Rav1haBcQPdzwMpIxXvO8EDgOBTMstQedOGV7T7WOdqD4Rel8It+4RQryz5+QQHwRnXu61JofUQXDlU4f4IGg/UV/hYSCaLnzPCWwDgUyvplThdmpdAclD0Dx0Xt4K87WugO6Dx7xqKuwD8cMay19hjQipqdw+Zh7ig476nqG99UH6TF0u6i/cBlLkivefwGEgkKlC0C06TXHqcO6HrkO4faBz+67QulW+9JUHci0ITp9crF77gNSp6YPo0FGfqF8O3Q9cfx5y+7DX9mnv3NecpnnIVM1D5yuffhF6HYQ/q4fu018IyUHHyu3DPey1/RpSf7vt1fv6Wf3dmRU87hdXvh5+ZEW+vr7rBLbPspy6uNrQKg+5CyA4fRAdgqv+6rNeXTR/hnpEPXIR+l6gc33i7APdb36i9fDcfz0hntaH4PY7BDI9eA1X+/fuWOWnDrmedaI+SB6C6iJEB5ReRq8lzkJ1cZWfOvD16fDU5bDOX0+Ip/QhuA3Eu+AZfnff0O8G+9tncnV4XKfP+kI1sbQK+Qoh1yrvPiC6dRAOHc2L9pCLU4feB7jeh9w+7LU9Ie4LjlMDTL+MwNfP0XlXrBpA/BCcPug6hMMRV7Xf3Yt9INewfuL0QfwQnHm5uO93GIimC99zAr89kP10a736NipXAblral2hv9b7UH+GZzVq1k4O2QME9Yn6J5qH1EFw5dNvXi4XIX2A63fI7cNev/2E+P3Afcpw/xsgEF3fREgegjPvXSSal0Pq4H5NPXDPAco3axXkwNfvPXXoXH0idJ/9pk8O5/6q+2MD8WIX/t4JHAZSUzqLZ5eZNdDvAuv1QfJyEbpuHUSXnyF0jz31QvIQNA+d6xcheQiqWy//LkLvV/WHgZR4xftOYBsIZFrwGJ9tFVLv3SOu6iB+8/ohOgTV9UF0eeHKoz6xavYB6QnBfa7Wq3r18pwFpN/KB8kD1/9l3T7stT0hH7av/+x2/gcAAP//pLUIogAAAAZJREFUAwBruNGtoUyfzwAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForCenterBudgetDecompose-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForCenterBudgetDecompose-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 