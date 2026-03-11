---
title: "金和OA ArchivesShowAsk.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowAsk-sqli.html
asset_dir: assets/金和oa-archivesshowask.aspx-sql注入漏洞
---

# 金和OA ArchivesShowAsk.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/16 13:38
* 1853浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

安全工具开发

网页浏览器

漏洞扫描服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowAsk.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

网络安全培训

授权

文本剥离工具

根据 `ArchivesShowAsk.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowAsk** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  string UserID = "";
  if (this.Session["UserCode"] != null)
    UserID = this.Session["UserCode"].ToString();
  this.Depts = new Role(UserID, "IOA_ArchivesModify").GetRoleDepts();
  if (this.Depts.Length > 0)
    ((HtmlControl) this.btnModify).Style.Add("display", "");
  else
    ((HtmlControl) this.btnModify).Style.Add("display", "none");
  this.strDeptList = new Role(UserID, "IOA_Distribute").GetRoleDepts();
  this.ReadLocal();
  this.GetList();
```

深入探索

Web安全课程

文件大小转换

VPN服务

参数`id`被带入`GetList`方法

```
private void GetList()
{
  DataTable archivesInfo = JHSoft.Archives.ArchivesDoc.getArchivesInfo(this.strArchID);
  if (((InternalDataCollectionBase) archivesInfo.Rows).Count > 0)
```

跟进`getArchivesInfo`方法

```
public static DataTable getArchivesInfo(string archID)
{
  Page page = new Page();
  StringBuilder stringBuilder = new StringBuilder();
  if (page.GroupConfig.IsUseGroup)
    stringBuilder.Append("select ArchivesType,ArchivesTitle,[dbo].[fn_FromOuterDeptIDGetOuterSystemName](SubDeptID,ArchivesFrom) as ArchivesFrom,ArchivesKey,ArchivesWH,a.SecretID,SecretName,");
  else
    stringBuilder.Append("select ArchivesType,ArchivesTitle,ArchivesFrom,ArchivesKey,ArchivesWH,a.SecretID,SecretName,");
  stringBuilder.Append("a.ExigenceID,ExigenceName,TypeName,ArchivesFs,ArchivesBH,DeptName,SubDate,UserName,");
  stringBuilder.Append("ArchivesZsdw,ArchivesCsdw,ArchivesDate,ArchivesMan,ArchivesFj,FileName,ArchivesSource,DossID,");
  stringBuilder.Append("ArchivesGD,Field1,Field2,Field3,Field4,Field5,Field6,Field7,Field8,Field9,Field0,SubTime,AskMoney,DocID ");
  stringBuilder.Append("FROM Archives a left join Secret s on a.SecretID=s.SecretID ");
  stringBuilder.Append($"left join Exigence e on e.ExigenceID=a.ExigenceId where ArchivesID='{archID}'");
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(stringBuilder.ToString());
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesShowAsk.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowAsk.aspx SQL注入漏洞](images/img-001-4c2d89354287.webp)](https://image.mrxn.net/eb6b7ec39ea64045aa1588df050f673b.webp)

成功延时 4 秒

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
文章标题：[金和OA ArchivesShowAsk.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ArchivesShowAsk-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesShowAsk-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKh0lEQVR4AeybgVojOQ6E+ef933mPalGWYrudDkMSbtfzIUquKqk9VhtY5u7Px8fHP38b/3z9cZ+v5Q1YE94IXwvxiq/lAVorjkX3SfxZdNZjeeYVfxgWn+RRLCx/fYbqr9BAPnF//JYTaAP5nP7HIzH7C7h+pckDfMBtuAaSl1cByUHk9kt3mKsI5/5ZHdz61euqT16F/VdRNY42EBMb33sCw0Ag3hCY42q7EDUrT9XqG2R+xlmraB/EM4F2wyG5WtPnEL7Ku2/lnEP4IZ9lbYaQfhjzWc0wkJlpc687gT2Q1531pSf96ECuXvfZzla1Mz/El4CZ5l4znPkrB9EXEq3XfhC6tZ/CHx3IT23qv9znRwcC8dZAog+3vl3mIH0QuTUhBOdacY4ZB+GHRPuv4rP6Xn3+jw6kPXQn3z6BPZBvH91zCoeB+Mqe4Wobs5qZf+YzV/0zrurK7ako/izg2pez2m+Vnz1H/KpOmjx9DAPpDXv92hNoA4F8c+B+PtsmRF3V4Ge52ls5RH9Ay9MAjt+f6c10zMwQvqrBNc41EH64hq4TtoFoseP9J7AH8v4Z3Ozgj6/v3+BNx27hvpDXt7Mcy5nP3GH4/OS1EKKfcsen5fjwWngQn5+UKyDqgE/22ofqFMDxZQ/GXy5K/4nYN+TaTF7menggkG8JRO7d+g3x+hGE6OUeQtdDaF4LpSsgNED0EUB7kyHyQ/j8pJo+IDyQbz4k91l29wNGPzzOPTyQuzt7nuE/0fkPxBRnf1sIDRL7t0tr10L4vBbCyKlGIb0PCD8k9h6tIXTlq9BzFPZA1AGm/gqB4zbqGQ4IbtbYHiGET7lj35DZqb2R2wN54+HPHt0GAnF9INHXqCKkDpG7sX0QPOQ3SWtCSB0iF99H39drob3KHRC9vK4I51r1OXd/IUStcgcEZz/EGjB1F92rGttAKrnz953AciDA8Q2rbs9TrVj1PofHekD4IW9X31NrCF/dxyyHW59qVwHhn3kgNGCQZ8+uHDCcJYzcciDDUzfx9BPYA3n6ET/2gPa7LJfVa+Yc4mrBHF27QhhrZ34/UzjTzUlXQPa1tkLVOCBqvRbOasX30fsgegG9dKxdfyy+Ps24fUO+Due3QBuIpwUc33wgcbZZ+4WQXshvxtJmtTMObnsAgw0Y9qZnOFwA6ZtxEHpfZ68QwgNoeQTQnn8Qn59mPSB9cJt/lrQPuNWAjzaQj/3nV5zAHsivGENuog0E4vr4CgrTlpl4BYQf8ktUusZMNX2MrjXT12sNuQ+IXPyVgPDXp87qIHxXNfeb+a0JZ3obiAw73n8Cy4F4grNtWhPC7RsEsQZmpY0D2jdJ9VE0cZJA+iHyalO9onJ9DlEHNAlo+2jkXyTagwLGvpAcjPlyIH+xp136zRPYA/nmwT2r7NJAdP0cMF6zfnP2CnvtbA3Rt+oQHARWTb0VlYPRZx1CU43DmtdCCB8kilfYL4TQlfcBoanG0Xvq2h7hpYHU4p1fOoFvm37k39Q1WcVqFxBvDSSq5rsxe5Z7QT4DIp9p7gHhAUzdIHB8078huwWEB2gKcNQBjfM+hCaB5ts3xKfyS7ANRBNT1H1p3QfkNOE2r7XOXe+1cMaJ7wNu+0Oue29du39FiNrqm+WuqZo5iB6Q/zFsrfpnOURt1Wa1bSDVuPP3ncAeyPvOfvrkYSAQVwvm6Gs2Qz8Bxtrqn/lmXK3pc4hnVB6Cg0T3tc9robmK4hWVg+gnvg8YNdf23n4NUWu/cBhIX7TXrz2BNhAYp+WtaHIOcxB+SLRmb0VrFWd65SB61xrn9kF4IL/R2iOE1CE9qpeugFsPIHoI1Tgsel1xpQHtR1zX2C9sA9Fix/tPYA/k/TO42cFyILMrBXHlrAndEUKDa+i6ipC16q2A4GY+6Y6qO7dmhOgFifYK7VPeB4w1EFz1QnCQWPVVvhzIqnBrzzmBYSCQU4Ux9zYgNXN+u+6h/ZA9IHJrQgjO/SDWgOTTsF8IHN9EbRbnMDdDiDqgya4TAkdf5Ypm+ky0Vnym7QPC34iTZBjIiW/TLzqBPZAXHfTVx7T/KamumOJqobyOvgbiesIcXVfRPSrnfKVBPsO+in2Pqs1yiH6uE9oHoQGmGgLHlzBIVK3DRq+F5iBr9g3xqfwSXP4DlaZ4FpBTtQeCq383a5WDcx+EBomuheQgcmtCOOcgNEic7U19+rCvYu+5t3btPd++IfdO6MX6pYFAvlUQuScu9J6VK7w+Q3kUEL0gsdbIozCn3LHiIPvZb3TdGa58MPY96yMe0g+Ri1/FpYGsGjyu7YrVCeyBrE7nDVr7sRfiSvnKCmHkvEcIDUa0p6L6OSBqvBbaq9wB4YNAe87QdRXthWs9ej9EHdz+6h6Ct7+in3+Pg+hhv3DfkHpqvyBvA9F0FBBTA6bbk+eRAI7/YJo2e5CE6AX5ttYWkDpEbn22Z2sznPkhesL4/Op3v8pB1kLk9lVsA6nkzt93Ansg7zv76ZPbQOD8GkFoQGsCHF+KgMbNEl/bqpkDWg9zM5+1ihC19/xw64NYQ+KsL6Ren+EcQve6Ipxr1eccwg/s/9Pnxy/7036X5bek7m/GWbcmhJwwYMtDCBy3pRZBcDBi9V3JIXpov45Z3UyDqJ35zUF4AFPH3wc4sJEl8bMqti9Zxfd/mf5bNr0H8ssm2QYCcbXq9YGR8/4hNBh/JrenIqQfIq/PshdCA0w1nPmbeJLUGuXA8SUEct+QnNvI24e1ihC11Wu9crPcPogewP6m/vHL/rQb4glCTstc3TOEbk1YdeUQHkiUrw9IXXWK3lPX0vuAsQeMnOtqPwhf5eybYfX1OUQvyJtXe0DoM672agOpxp2/7wT2QN539tMnXxoIxHWDvI6Q3LTzF+nr+LU8AKLWmvAQuk8Qvo6+WarWAeH3WgjBwYjSFZCam8Oag9QBlx0ItB8cIHI9RwGxhvlZXhrI8ZT96SUn0P6Byk/TFB2PcvZXhHgjKtf3l2YOwg+IvgmgvXkWILlVD2sVIWor575Xsdb2+Xd67BuyPLXXi+13WRBvCzyO3nb/htQ1jH1dd4aun+kzDeIZ1irOepiDqINEa1cR1rUQ+r1++4bcO6EX63sgLz7we49rA6nX+0o+awxxLSHRvtrTHFzz2T/rUTnnMPZ1j+8gRL9VrZ8tfNQH0R/Yv8v6+GV/2g3xviCnBWNu3wz1dihmGmSvmT7jIGuAGwvQfgSG21x7cLgIbj2ApbvY96oFwOk+qm+Vu79wGMiqcGvPP4E9kOef8UNPeMpAdPUcq93YI4S4+jO/dMVKqzpEL0h0rXwOc/cQok/1uccM7Vtp8kD0hcSnDEQP23F+AivlKQOBnDhEXt+W1Yaq5prK9TlEf8jfnrpO2PuvrlXrWNVAPh8itx9iDYnWKvo5wqcMpD5s54+dwB7IY+f1dPcwEF2bVVzZ0ay+1lmfcZDXGyK3D2IN6y9PkD7XGiG11T7sr2i/0Lzys7CnIozPh+SGgdTinb/+BNpAIKcE9/PVViHr7YORsyaE0OvbJr5G1SD8kGhv9Zlb4cwP2df6rAekD27z6l/1sCZsA6nFO3/fCeyBvO/sp0/+HwAAAP//XfRkjwAAAAZJREFUAwAFiQChzokoLQAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesShowAsk-sqli.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesShowAsk-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 