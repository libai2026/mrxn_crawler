---
title: "东胜物流 /MvcShipping/MsCodeAll/GetLanesList SQL 注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsCodeAll-GetLanesList-sqli.html
asset_dir: assets/东胜物流-mvcshippingmscodeallgetlaneslist-sql-注入漏洞
---

# 东胜物流 /MvcShipping/MsCodeAll/GetLanesList SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/4 15:31
* 327浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

计算机安全

鉴权

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 /MvcShipping/MsCodeAll/GetLanesList 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据.NET MVC特性找到MsCodeAllController下的GetLanesList方法，看下它的实现

```
public ContentResult GetLanesList(string condition, string sort)
{
  List<Code_lanesmb> lanesList = MsCodeAllDAL.GetLanesList(condition, sort);
  string str = JsonConvert.Serialize(new
  {
    Success = true,
    Message = "查询成功",
    totalCount = lanesList.Count,
    data = Enumerable.ToList<Code_lanesmb>((IEnumerable<Code_lanesmb>) lanesList)
  });
  return new ContentResult() { Content = str };
}
```

深入探索

安全认证考试

JSON处理工具

安全研究工具

参数condition、sort被带入MsCodeAllDAL.GetLanesList，跟进看下

```
public static List<Code_lanesmb> GetLanesList(string strCondition, string companyid, string sort = null)
{
  StringBuilder strSql = new StringBuilder();
  strSql.Append(" SELECT ");
  strSql.Append(" GID,LANEID,LANE,LANEEN,EDICODE,OP,DOC,CUSTSERVICE");
  strSql.Append(" from code_lanes ");
  if (!string.IsNullOrEmpty(strCondition))
    strSql.Append(" WHERE " + strCondition);
  string str = DatasetSort.Getsortstring(sort);
  if (!string.IsNullOrEmpty(str))
    strSql.Append(" order by " + str);
  else
    strSql.Append(" order by LANEID");
  return MsCodeAllDAL.SetLanesData(strSql);
}
```

深入探索

网络安全会议

防火墙软件

网络安全培训

至此[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞成因就非常明显了：

* 在 `MsCodeAllDAL.GetLanesList` 方法中，程序通过字符串拼接的方式构建 SQL 查询语句。
* 参数 `strCondition` 直接来源于控制器 `MsCodeAllController.GetLanesList` 的输入参数 `condition`。该参数未经过任何参数化处理、类型转换或白名单过滤，直接拼接到 SQL 字符串中。
* 虽然使用了 `DatasetSort.Getsortstring` 转换，但如果该工具类未进行严格的字段白名单过滤，攻击者可以通过 `sort` 参数注入 SQL 片段（如基于报错的注入或时间盲注）。
* 使用了 `DatabaseFactory.CreateDatabase().ExecuteReader` 执行原始 SQL 字符串。

# 漏洞复现

```
GET /MvcShipping/MsCodeAll/GetLanesList?condition=SQLI_POC&sort=LANEID HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流 /MvcShipping/MsCodeAll/GetLanesList SQL 注入漏洞](images/img-001-f4b3be9a1b51.webp)](https://image.mrxn.net/baa40d4e91494d13995ae8ae19e39743.webp)

通过联合注入，成功在响应回显当前数据库版本信息

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
文章标题：[东胜物流 /MvcShipping/MsCodeAll/GetLanesList SQL 注入漏洞](https://mrxn.net/jswz/dongsheng-MsCodeAll-GetLanesList-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-MsCodeAll-GetLanesList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALZklEQVR4Aeyd4XrbuA5Effr+77xbeHpkESItt01j/1C+RYYzGIAMITVJ791vf9xut//+JP779bGq/ZXeestfRfvqX3H1wjOvebFq9qEumlvxlW7dn2AN5Gfd9c+n3MA2kJ/Tvr0Sq4Nb2/PqwA3Y0sBTbp0FnXe98pCeta6AcL0QDkH18lZAdAia7wjJQ7Dn5dXzldBfuA2kyBXvv4HDQCBThxFfPapPBKS+18Fc7z45jH4Yub5n6JmeeSqnTyxtH+riPvdsDTkzjDirOQxkZrq077uBvx6ITwtk+v3oEF2f+c7VIX4Irnwzv154XqvPHmcI6QfB7v/dfr1+z/96IPtm1/rvb+DLBrJ6StQhT5e8H73rckhd9884zL0Q3Z69FpLvuv6O+tTlX4FfNpCvOMzV43Y7DMSpd1xdFnD/fQKCd9/kk/0mqbsEqdcHI7+bdp/0zVAbjD0g3HxHmOdh1GHkvU/nszOW1n3FDwMp8Yr33cA2EMjU4TmujloTr4DU17oCwq2DOS9vBSRf6woIt74jJA/01PY3D8D9La5+FTByCytXAcmrnyHM/RAdnuO+/zaQvXit33cDP+qJ+JPoR4Y8BfaCcH0QvsrrWyGkvuftV9hzMNZAeHkrYM7tA8mf8epVoa/WfxrXG+ItfggeBgJ5KmBEzwvR5aJPBCQvP8vrg9TpP0OIH45orb1F9RXq66hfvXM4ngEemn4RHjkY14eBWHThe25gGwhkUj4FHT2eOoz+npeLEP+K27fn1UXzf4OQs5z1hPjcC8J7Xef6uw5jfc9X3TaQIle8/waWA4FM0yNCOASdLoTDHPXZp3N1SL150fztdrsv1cW7+OuTmgjp+Su9BBh9EG4fC+WQvDqEm++63DzED0HzhcuBVPKK77+B04FApuh0RZjrr34JvY91kL7yjrDOQ3IQdA97yMWuw7xOH8zzq37qkDr7qMv3eDqQvfla//sb+AGZ3rOp7Y8Bcz+M+qofxLfvWetX/Stf9TBWHhj3hpH3OkheXXQfSB7mqG9V1/Plu94Qb+VDcPu7LMiUPVdNax9dl3eE9IER971qDclbD+GVq4Bw8yJEh6B6YdVVwDFX+R7lrVCHsa5yFau8enn2oQ7pB0F10Rp54fWG1C18UPz2QCDThhGd9goh/v616+9655B6/eLeB/HstVrDqMPIy1PRe8LoMw+jDiPXVz0r5DD6IBwe+NsDqQ2u+Hc3sPwpCx5Tg8faafcjQTzqMHL1jvCar9e9wiG9PXPHe4/JJxjrtEB0+QohPveDkVtnXl54vSF1Cx8U209ZZ2dympBp61eXQ/JdN9+x+yD1+syLkDwE9RXqqfUsIDXwHK2F0df7y0WIv9f3vFyfvPB6Q7yVD8HtewiM061p7QOS32u1hlH364LoECxvBYR3n1wsb4W8Y+V6dE/n3S/Xd8bh+dl7vX3heZ2+wusNqVv4oDgMBMZp9rNC8hA0DyNfPS3qHe2jLof0haB5CIcjWtsR4lWHOe97yFe46qfe0T6Q/eGBh4H04ot/7w1sP2U5NXF1DPNi96lDpi7vvs71QerMq8shefUZ6jUnF2HsoS7CPA/RYUTrVvut8vr3eL0h3taH4DYQmE+9nxNG3366tdZf6woY/eY7QnxVUwHh+kqrkD/D8lXAvEflKuxR64rOIfUQNC9WTQUc8lruWJ6KO/n5CeKH4E9p+2cbyKZci7fewHIgME6vJjwLGH0w8tVXB6PP3jDqMHJ9s74wevXAqEM4BPX13iu+0uF5v75P71P55UAqecX338D2m7pbOzURMnWYo3WQvPwM7a8PxnrzIiQPa+y9rFUX1UVY9wQs2xC4//smMOJm+LWA38sDx3+l7XZ9vPUGtj+yfFpWpzHfsfvNq8tFyFNjHkaufob2m2Gv1dN1yN7mRX1yUX2F+jqe+ff5bSB78Vq/7wa239QhT4tHgZGf6T4VkDoIWid2n7yjfpj36XlAaYnA/c9+De4phzEP4RDUd4bw3A/r/PWGnN3uN+evgXzzhZ9ttw3E1xfyOhWv6A1Kq+h65+Wp6PoZh+zffdWrYqXPcisvZA8I6qseszAvdo+6aF7e0TyM+5dvG0iRK95/A9svhjBOC+YcokOwfwlOv+tnHNJvVQ/J2wfC4Yh6RIhHLva9ID4YUb8I8zyMOoRb17HvX/nrDalb+KDYBuK0xH5G9Y76IE8DzFHfCu0LY/3KP9PtYQ7SSy52n7rY8yve9Vfr9cHxfNtANF343hvYfjF89RiQqULwrG71FK3qur/zXme+0FytK+QdIWeHEaum4lU/pF5/1VasOMQPwfJW6C+83pC6hQ+Kw09ZkOl5xppgBUSv9T66b8Uh9eZFiA5BdffovOuQOjhir4V4ui5/FfsZOrcPZD8I6hPhqF9viLf3IbgNxKl5LjmMU4RwCHaf9ZA8BNVvt6ys6wjxQzDu2/0vBSEacPNjX68mmltx4N7XPIRDUN0+Iox5CIcR9dtHhPg6B67/ger2YR/bT1mQqTlVCPe8EG5ehLluXUeIv+ty+4ow+tX1z/AVT9XpE0urkIuQM0BQXayafahD/Ptcrc3Xusf2R1ZPXPw9N7D9lPVsanU08zBOXb08+1AXzXWu3hGyT/fDXK/6lbdy+9AH6QXBM33fo9aQulrPwn7mIH4IqusrvN4Qb+VDcBsIZGoQ7OeD6DXFCvMQvXMYdfMrhPghuPLV3hUQHzzQGogm7wjJV5+Kni9tHz1/xiH9IWgv6+SieuE2kCJXvP8Gtp+y+rRWHDJ1CK58/UvTB6mDEfXrk4td71zfHvVA9trnag3PdXiet3/1mkXPd24NZB/g+j3k9mEf209ZkCn1KZ5xSB0EV18fzPO9P8SnDuEQ7P31FUI8ta7oXpjny1vR/aVVQOp6vvPyVqhD6iCo/gyv7yHPbucNue17yKt7w3za9WRUwPO8+5S3Qr7C8lSYh/SHoHph+Spq/SwgteWt0AvR5SusmgoY/RBeuYpeD8nDiOU1rjek39qb+fY95OwckKk6ye6HMb/yWQfxQ1B9hat+kHo4or16rRxSs/Kpr9A+HeF53+7f97/ekP1tfMD6n30PgTwlMOLZ1+zTow9SLxf17dFcR0gPveY7h9EHI9cP0WGO9u9ovToc6683xNv5EDwMBMapeU6n29E8pE6+Qut7vuvwvB8kDw+0hwjJuReM/Exf9VE/Q/uLMN9/3+cwEIsvfM8NLH/Kcmr9WDBOWd8KrTcPqZeLEB2C6iJEt98MIR4IWtu9kLy6PlEdRh/MOUSHEXuf3l8Oj7rrDfHWPgS3n7Kclrg6X8/DY7rAquz+/+4Atv+UnUbgnrOv2PNyUd8M9Yh6Vlwdcha5aL3Y9c71ieZXqK/wekNWt/QmffseAnk64DX0vDXVCnnHyu0D0r/7YK7rs4dchNQBSqcI3N9KCFrQ95BDfBDUv0KY+2DUIRweeL0hq1t9k74NxKfhDM/OCY9pw2N9Vue+Z76et66w5yD7q5enonMYfTDyqqmwDpKHoLpY3gq5WFpF56UZ20A0XfjeGzgMBDJ1GHF1TIhvlVeHuc8nA8Y8hJu3jwjJwxH1rNCekNrOrYPkIai+QogPRux+WOcPA+nFF//eG/iygfiUrY6/ykOellXefnDuW/WA1MKIK3/X/5T3Or8WdREe5/qygbjZhX93A18+EKfeEfIUqHvsztXP8FmduTOEnAmC7gkjV7cfJL/i+mHu63l54ZcPpJpe8ec3cBiIU++42kIf5GmAOeqzD8x95s8QUj/zQXLwHHutZ+yoD9LvjEN89oFw60Tz8sLDQEq84n03sA0EMkV4jquj9ml3/modZP/uf7Vf1ekVS3sW3Qc5A4zYe/Q6uQip73UQHYL7/DaQvXit33cD10Ded/fTnf8HAAD//1LcZJMAAAAGSURBVAMA8z77y/e6OfMAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsCodeAll-GetLanesList-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALZklEQVR4Aeyd4XrbuA5Effr+77xbeHpkESItt01j/1C+RYYzGIAMITVJ791vf9xut//+JP779bGq/ZXeestfRfvqX3H1wjOvebFq9qEumlvxlW7dn2AN5Gfd9c+n3MA2kJ/Tvr0Sq4Nb2/PqwA3Y0sBTbp0FnXe98pCeta6AcL0QDkH18lZAdAia7wjJQ7Dn5dXzldBfuA2kyBXvv4HDQCBThxFfPapPBKS+18Fc7z45jH4Yub5n6JmeeSqnTyxtH+riPvdsDTkzjDirOQxkZrq077uBvx6ITwtk+v3oEF2f+c7VIX4Irnwzv154XqvPHmcI6QfB7v/dfr1+z/96IPtm1/rvb+DLBrJ6StQhT5e8H73rckhd9884zL0Q3Z69FpLvuv6O+tTlX4FfNpCvOMzV43Y7DMSpd1xdFnD/fQKCd9/kk/0mqbsEqdcHI7+bdp/0zVAbjD0g3HxHmOdh1GHkvU/nszOW1n3FDwMp8Yr33cA2EMjU4TmujloTr4DU17oCwq2DOS9vBSRf6woIt74jJA/01PY3D8D9La5+FTByCytXAcmrnyHM/RAdnuO+/zaQvXit33cDP+qJ+JPoR4Y8BfaCcH0QvsrrWyGkvuftV9hzMNZAeHkrYM7tA8mf8epVoa/WfxrXG+ItfggeBgJ5KmBEzwvR5aJPBCQvP8vrg9TpP0OIH45orb1F9RXq66hfvXM4ngEemn4RHjkY14eBWHThe25gGwhkUj4FHT2eOoz+npeLEP+K27fn1UXzf4OQs5z1hPjcC8J7Xef6uw5jfc9X3TaQIle8/waWA4FM0yNCOASdLoTDHPXZp3N1SL150fztdrsv1cW7+OuTmgjp+Su9BBh9EG4fC+WQvDqEm++63DzED0HzhcuBVPKK77+B04FApuh0RZjrr34JvY91kL7yjrDOQ3IQdA97yMWuw7xOH8zzq37qkDr7qMv3eDqQvfla//sb+AGZ3rOp7Y8Bcz+M+qofxLfvWetX/Stf9TBWHhj3hpH3OkheXXQfSB7mqG9V1/Plu94Qb+VDcPu7LMiUPVdNax9dl3eE9IER971qDclbD+GVq4Bw8yJEh6B6YdVVwDFX+R7lrVCHsa5yFau8enn2oQ7pB0F10Rp54fWG1C18UPz2QCDThhGd9goh/v616+9655B6/eLeB/HstVrDqMPIy1PRe8LoMw+jDiPXVz0r5DD6IBwe+NsDqQ2u+Hc3sPwpCx5Tg8faafcjQTzqMHL1jvCar9e9wiG9PXPHe4/JJxjrtEB0+QohPveDkVtnXl54vSF1Cx8U209ZZ2dympBp61eXQ/JdN9+x+yD1+syLkDwE9RXqqfUsIDXwHK2F0df7y0WIv9f3vFyfvPB6Q7yVD8HtewiM061p7QOS32u1hlH364LoECxvBYR3n1wsb4W8Y+V6dE/n3S/Xd8bh+dl7vX3heZ2+wusNqVv4oDgMBMZp9rNC8hA0DyNfPS3qHe2jLof0haB5CIcjWtsR4lWHOe97yFe46qfe0T6Q/eGBh4H04ot/7w1sP2U5NXF1DPNi96lDpi7vvs71QerMq8shefUZ6jUnF2HsoS7CPA/RYUTrVvut8vr3eL0h3taH4DYQmE+9nxNG3366tdZf6woY/eY7QnxVUwHh+kqrkD/D8lXAvEflKuxR64rOIfUQNC9WTQUc8lruWJ6KO/n5CeKH4E9p+2cbyKZci7fewHIgME6vJjwLGH0w8tVXB6PP3jDqMHJ9s74wevXAqEM4BPX13iu+0uF5v75P71P55UAqecX338D2m7pbOzURMnWYo3WQvPwM7a8PxnrzIiQPa+y9rFUX1UVY9wQs2xC4//smMOJm+LWA38sDx3+l7XZ9vPUGtj+yfFpWpzHfsfvNq8tFyFNjHkaufob2m2Gv1dN1yN7mRX1yUX2F+jqe+ff5bSB78Vq/7wa239QhT4tHgZGf6T4VkDoIWid2n7yjfpj36XlAaYnA/c9+De4phzEP4RDUd4bw3A/r/PWGnN3uN+evgXzzhZ9ttw3E1xfyOhWv6A1Kq+h65+Wp6PoZh+zffdWrYqXPcisvZA8I6qseszAvdo+6aF7e0TyM+5dvG0iRK95/A9svhjBOC+YcokOwfwlOv+tnHNJvVQ/J2wfC4Yh6RIhHLva9ID4YUb8I8zyMOoRb17HvX/nrDalb+KDYBuK0xH5G9Y76IE8DzFHfCu0LY/3KP9PtYQ7SSy52n7rY8yve9Vfr9cHxfNtANF343hvYfjF89RiQqULwrG71FK3qur/zXme+0FytK+QdIWeHEaum4lU/pF5/1VasOMQPwfJW6C+83pC6hQ+Kw09ZkOl5xppgBUSv9T66b8Uh9eZFiA5BdffovOuQOjhir4V4ui5/FfsZOrcPZD8I6hPhqF9viLf3IbgNxKl5LjmMU4RwCHaf9ZA8BNVvt6ys6wjxQzDu2/0vBSEacPNjX68mmltx4N7XPIRDUN0+Iox5CIcR9dtHhPg6B67/ger2YR/bT1mQqTlVCPe8EG5ehLluXUeIv+ty+4ow+tX1z/AVT9XpE0urkIuQM0BQXayafahD/Ptcrc3Xusf2R1ZPXPw9N7D9lPVsanU08zBOXb08+1AXzXWu3hGyT/fDXK/6lbdy+9AH6QXBM33fo9aQulrPwn7mIH4IqusrvN4Qb+VDcBsIZGoQ7OeD6DXFCvMQvXMYdfMrhPghuPLV3hUQHzzQGogm7wjJV5+Kni9tHz1/xiH9IWgv6+SieuE2kCJXvP8Gtp+y+rRWHDJ1CK58/UvTB6mDEfXrk4td71zfHvVA9trnag3PdXiet3/1mkXPd24NZB/g+j3k9mEf209ZkCn1KZ5xSB0EV18fzPO9P8SnDuEQ7P31FUI8ta7oXpjny1vR/aVVQOp6vvPyVqhD6iCo/gyv7yHPbucNue17yKt7w3za9WRUwPO8+5S3Qr7C8lSYh/SHoHph+Spq/SwgteWt0AvR5SusmgoY/RBeuYpeD8nDiOU1rjek39qb+fY95OwckKk6ye6HMb/yWQfxQ1B9hat+kHo4or16rRxSs/Kpr9A+HeF53+7f97/ekP1tfMD6n30PgTwlMOLZ1+zTow9SLxf17dFcR0gPveY7h9EHI9cP0WGO9u9ovToc6683xNv5EDwMBMapeU6n29E8pE6+Qut7vuvwvB8kDw+0hwjJuReM/Exf9VE/Q/uLMN9/3+cwEIsvfM8NLH/Kcmr9WDBOWd8KrTcPqZeLEB2C6iJEt98MIR4IWtu9kLy6PlEdRh/MOUSHEXuf3l8Oj7rrDfHWPgS3n7Kclrg6X8/DY7rAquz+/+4Atv+UnUbgnrOv2PNyUd8M9Yh6Vlwdcha5aL3Y9c71ieZXqK/wekNWt/QmffseAnk64DX0vDXVCnnHyu0D0r/7YK7rs4dchNQBSqcI3N9KCFrQ95BDfBDUv0KY+2DUIRweeL0hq1t9k74NxKfhDM/OCY9pw2N9Vue+Z76et66w5yD7q5enonMYfTDyqqmwDpKHoLpY3gq5WFpF56UZ20A0XfjeGzgMBDJ1GHF1TIhvlVeHuc8nA8Y8hJu3jwjJwxH1rNCekNrOrYPkIai+QogPRux+WOcPA+nFF//eG/iygfiUrY6/ykOellXefnDuW/WA1MKIK3/X/5T3Or8WdREe5/qygbjZhX93A18+EKfeEfIUqHvsztXP8FmduTOEnAmC7gkjV7cfJL/i+mHu63l54ZcPpJpe8ec3cBiIU++42kIf5GmAOeqzD8x95s8QUj/zQXLwHHutZ+yoD9LvjEN89oFw60Tz8sLDQEq84n03sA0EMkV4jquj9ml3/modZP/uf7Vf1ekVS3sW3Qc5A4zYe/Q6uQip73UQHYL7/DaQvXit33cD10Ded/fTnf8HAAD//1LcZJMAAAAGSURBVAMA8z77y/e6OfMAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsCodeAll-GetLanesList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 