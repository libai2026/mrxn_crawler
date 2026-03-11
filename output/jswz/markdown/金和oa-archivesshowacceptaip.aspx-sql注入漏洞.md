---
title: "金和OA ArchivesShowAcceptAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowAcceptAip-sqli.html
asset_dir: assets/金和oa-archivesshowacceptaip.aspx-sql注入漏洞
---

# 金和OA ArchivesShowAcceptAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/15 13:30
* 1843浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

文本剥离工具

Windows安全工具

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowAcceptAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

物流软件安全

网络安全会议

编码转换工具

根据 `ArchivesShowAcceptAip.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowAcceptAip** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  this.GetInstanceId();
  string UserID = "";
  if (this.Session["UserCode"] != null)
    UserID = this.Session["UserCode"].ToString();
  this.strDeptList = new Role(UserID, "IOA_Distribute").GetRoleDepts();
  this.ReadLocal();
  this.GetList();
```

深入探索

漏洞预警服务

在线安全工具

JSON处理工具

参数`id`被带入`GetInstanceId`方法

```
private void GetInstanceId()
{
  if (string.IsNullOrEmpty(this.strArchID))
    return;
  this.strInstanceId = JHSoft.Archives.ArchivesDoc.GetAcceptInstanceId(this.strArchID);
```

跟进`GetAcceptInstanceId`方法

```
public static string GetAcceptInstanceId(string strArchivesId)
{
  string acceptInstanceId = "";
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append(" select  DISTINCT(JHOA_Approve.Instance_ID) from ");
  stringBuilder.Append(" AcceptDoc INNER JOIN JHOA_Approve ");
  stringBuilder.Append(" on AcceptDoc.AcceptId = JHOA_Approve.AppO_ID ");
  stringBuilder.Append(" where AcceptDoc.ArchivesID =  " + strArchivesId);
  stringBuilder.Append(" and JHOA_Approve.AppT_ID = 'IOA_Accept' ");
  DataTable dataTable = dbOperator.ExecSQLReDataTable(stringBuilder.ToString());
  if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
    acceptInstanceId = dataTable.Rows[0][0].ToString();
  return acceptInstanceId;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesShowAcceptAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowAcceptAip.aspx SQL注入漏洞](images/img-001-730ee8e688b4.webp)](https://image.mrxn.net/9bc03078ee6a42fba27450c39e6638c2.webp)

成功延时 2 秒

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
文章标题：[金和OA ArchivesShowAcceptAip.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ArchivesShowAcceptAip-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesShowAcceptAip-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALX0lEQVR4Aezci3bjuK4E0Oz5/38+NxC6ZIp6xOlJt33PUVaQAgoFkCZE59Gz5p+Pj4///K7959dH6n+FC8zcHC+iX1+ucr8kp5DaESMOl3jE5GY80ozc6I+14Ufud/wayGfd/fkuJ7AO5HPCH8/a2ebxQVt6nWlHPlq6lsZRE5/O0Ri+MH3KL5tjugaVftqwvK4U0HH6FyYXLO5ZS03hOpAKbnv9CewGQk+fPZ5tN0/CmKfrR272aQ2Ncx+a54HpEe2IyQV51CH0gqlbgs8vibHcBuzeMT5l3/7k0Y+tf9RsN5Aj0c39vRP4kYHQk89TVpiXwDYXvrB0ZeWXsdVWLlb5sjmma3hg6b4yWv+V7ipP98CV7Fu5HxnIt1a8xZcn8KMDwfr+m1Wvnuhoglfa5HisgZRuEMs+UrNJngRsa6qW5tjiSYsfoX90ID+yo//xJn9mIP/jh/pvXv5uIHVVz+zfLJTasXe4IOdvDXQu2rHP7EcTnPNjHE2QXgehVhzrZn8VTc6sG+NJuoS7gSzs/eVlJ7AOBMs3Qr7Gs91eTZ/uO9bSXOqSm+Pij7ji6R6o8NCwvLYxSXNz38SF0ZdfRteEp2OEWhHLmnyNa9Gnsw7k078/3+AE/qnJ/65l/6nn8TQkR3OJr3DuM2o57pOawlE/+pUro3tgTWN5kitfRsdYNXEqXzbHZ1zx37X7huR03wRPB4LlyTnaJ+e56OcnIzxdi1ArYlkztWvi05k5WsseP+XLJ9vcQk5f5r5jOjm6z5j7yqdr2GNq2edOB5KiG//uCfzDfkpYd4HlqcXK5ckJgUUTvpDmoinuzGht8mzj4tlzxad/YcVHVrmyq1zly0ZNxc8avb/oxz7xk7vC/0835Op1/Nfk7oG82SjXgeRaBbPPxIXhOL6eNM/jX9t4cBz71buMzmedEStfFo7WFhebc2w1dIxIl7daHGJE6c+xDpHuEGvvOZm+I78OZCRv/3UnsP5imC3QE8306BiRrP/WvBIXTvocYcqwPEWJgzSPUCumH5ZaHriKfjl07le4gfQ5wo3wM4jm010+ExcuxOcXei0aP6nTT/aa+4acHtdrEruB1LTL2E8vW6RzbLHqYnRurklcGO2MlZuN7scWZ13Fc7+juHSjse3LPo4+/RIXHnHFX1lqRtwN5KrBnfvzJ7D7xTBLjlOLTz81iWctnUdSK841lcDm/b+4ryx9gkd6um9ybOPiaY7Go37hgrS26mejc9EGZ13FtLb8MjrGx31DPt7r4x7Ie83jY/2x9+qKZc/R0FcsPNs4fCGdo7G4WPoFaU3i6ArD0ZrizizaOU/XYk5dxljeWs/6jsW0duTOfFqbvoX3DTk7rRfx60DoaWUfbOPiaa4m+axV3VfGtu+Rnq812ROtpTH9kj9CttqqYcvRMY2liaVnYloT/gppLe5v6h9v9rHekGf2lSnTE72qoTWpCdI8duVY3qtpTM2Ic9GzudLNtWNc+dmSP+OTHzHakYtPv67EwdQUfmsgaXDjnzuB04HUtMqOli6+jO3E6ZjHn9+P6sPR+uo12pyndTyH6ZU+QR71RxyPPM+9hvQJ0j3O9lA6WkNjcbHTgURw4989gXUgmSg9NRqPtsM2R8fpUZg6Ope4crMl9x1Mj7HmiKs82z0UF5trEhdG8x2sujL2axY/WvrSWtw/ZX38mY/f7rrekN/ucBf+6AmcDiRXa1yNvlrJzThqZ5+uHXm2HNt47D/Wlc9WW1yMztE49ok/a8PTNZxjav8tZs2xz+lARtHt/70TWP895GxJHk9KNDw4Hn7yhTRfflmeBppn/2NlNEHOtdVzNlr/LF+6ea3iYskFwwfp9djjlWbOJS68b0idwhvZ+ud3esp5Guh43GtyM46a+LOG7jfyNEdjaoOjNlxwzM3+rEl8hPTa6TFq6Fy4aILhC8PNWLlYcomP8L4hR6fyQm4dyDPTyz7ZPjnhR6Q1NKY/HWOU/7aP9Q+Sv93ks5Du8+nuPukcjTvBQPC1JvKcSeLCdSAV3Pb6E7gH8voZbHaw/thLXzUaS3VmR1dt1s4aum/4EedaWssDZ03iqz6zJvERps93c7P+qg/9elLDNi7+viF1Cm9k64+9V5PNfumJssXkr/A7/aMdkV4za9Axe4xmRh7a5LIGnQtfeJWr/Gh0PVscNWd+1im8b8jZKb2I3w2kpnRm2WPyiY+QflKSYxuHP0LOtVdrn+XY96M5GlM7ItvcvNdRm1y4xCMmR/dNjo5x/3vIx5t97G4Ij2lhs915wokjwpe/pPHQ0H7qg3Pf4mdujkvDth8dR3uFVV9G16DCjaV+Q54EV9o5l7hwN5CT/jf9l05g93tITWk07J765J/ZY7TBsSbcjDzWZOuP9bOfPjPPtgdWCdbXh5U/crBok6NjHv+UQHPRZE+F4YLFlSUuvG9IncIb2QsG8kav/g23sv5iOO+N7dUb82xzde3KRs13fLofjdWrbOxRcVk4ttoxF01xZ/YdDb1Wao6QrYaO2eNRfbj7huQk3gRPB3L0ZGXPydHTn/nkCznXsM2lD81XfWzOzTFC7RDLN2MeuBNdENlDMNLE38XU0/tJXHg6kEre9vdPYB1IppwtsJ/eWY7WssfUBHlowgXnPYQ/wme09FpHWjqX3mzj8EdIaznH1PE9zTqQNLjxtSew+8WQnmieKjrGutPkgmticJILJpX4CKM5QizfB45yMzf3Tn7kw/F1X7aa9EmPwiOu+NGiCY65+PcNyUm8Cd4DeZNBZBvrL4a5RkG217QKaI7G4kZLbSHHmlHPVsM2HrXxq3fZHBfHcT3HfHoUVn0ZreXx96niy0pXRmuKi9Fc5UdLvpCtprjZ7hsynt4b+OtA6OnRmMmNewwX5Fw71n3l031mHc1jTWH55s4eI6JziYM0j1Dr/4wNS9818enQHI2f1PKZ178E3/gy19F9eeA6kG/0vaV/8ATWgWR6was16YnOWprn8f571Se5uU/iEaN9BlNH7yc14QvD0ZriZosmPK0NT8d87/XSdembfoXrQCq47fUnsA6EnhpbPNriPFm65khL59jj3Ccxe216R5P4Cp/RzhoeaydHc1mLbVw8zaWmuDKa54GzJnHhOpAqvu31J7D+6aSmM9rV1nhMG4dSLD+1jD1nn9awxcOGv0ha+ys8BFpDY9alYxzWzSSW1zDz6TfzFdM1NBb3ldFa3P9d1sebfdxvWZcD+fvJ9U8n89K5liNGM3LlH/HhgvS1TDxi9fjKRn35V/rKl0VT/mzJcb6v1ESbmH1NNDOmpjC58s/sviFnJ/Mifv2mTk+d5zF7zuR51M7cHLP/ZYpHPVs/9VkzyEMXLkjnEo/IeW7UlU9rs4dg5WajtTM/xmw16Vd435DxpN7AXwdS03nWzvY91s8a+qkYNTRH41zzTDz2m/XJcd4/mtQmLpy5xDzfLzUjVu8yug8PXAcyFtz+605gNxAe02Lrf2ebdG09CWWppXn230NKVxZt+TG6Ljk6Zo/RzJhehcnR9YmfwaovG7V0H7Z4pAlXPWbbDSTiG19zAvdAXnPup6v+yEDYXlOsC2L5e1Cu5pr4dDjORUvnOX97i/YI6frkPpdcP8MFae0quHB4Xpv+hWl5hT8ykKsF7tz3TuBHBlLTL7tamuefqqs+z+TotWpPZXQ81tIcjaUro2P2t5LOjX1mv3qUhadrePSjuSPNjwwkjW/89yewG0hN98y+Wu6sbuTHHuHpJ4Ytjtr4qUnMtgZJLd+72D+ZPLiIsejTvzC5YHFliUcsvixc+bOxXeNIuxtIRDe+5gTWgdDT42s82yrntWc1xc9PUnFlI0/3Lv7MRv3on+m/y7Pdw7gGneMc5/Vo7civAxnJ23/dCdwDed3ZH678fwAAAP//BexpRQAAAAZJREFUAwAnVZ+kxpLhlgAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesShowAcceptAip-sqli.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesShowAcceptAip-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 