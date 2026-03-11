---
title: "金和OA AccountSet.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AccountSet-sqli.html
asset_dir: assets/金和oa-accountset.aspx-sql注入漏洞
---

# 金和OA AccountSet.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/29 13:05
* 237浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

服务器安全服务

安全运维咨询

技术文章订阅


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AccountSet.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AccountSet.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AccountSet** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack || string.IsNullOrEmpty(this.Request.QueryString["OperType"]) || string.IsNullOrEmpty(this.Request.QueryString["ID"]) || !string.op_Equality(this.Request.QueryString["OperType"], "Edit"))
    return;
  DataTable accInfo = this.Acc.GetAccInfo(this.Request.QueryString["ID"]);
```

要执行 `GetAccInfo` 方法，必须同时满足以下所有条件：

代码安全审计

1. 不是页面回发（`IsPostBack` 为 `false`）。
2. URL参数 `OperType` 的值必须为 "Edit"。
3. URL参数 `ID` 不能为空。

跟进`GetAccInfo`方法

深入探索

安全研究报告

文件大小转换

Windows安全工具

```
public DataTable GetAccInfo(string id)
{
  return this.db.ExecSQLReDataTable("select * from EAI_Accounts where id=" + id);
}
```

参数`ID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/subClass/AccountSet.aspx/?ID=SQLI_POC&OperType=Edit HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AccountSet.aspx SQL注入漏洞](images/img-001-e0d3195aca8b.webp)](https://image.mrxn.net/f526c9347c614e419f047c4bd4929ba1.webp)

成功延时 4 秒

漏洞扫描服务

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
文章标题：[金和OA AccountSet.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AccountSet-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AccountSet-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKIElEQVR4Aeybi3IbuQ5EffL//7yrFnM4EIczkuWHVLvcMtJgdwNkCDFOfOv++fj4+Oer8c/f/+zzd3kFuRleDX9/uaf/tXXQ34lLIlfxQt98VW2W35iHRfUP0pfv0N4ZyCVfX+9yA30gl4l/fCbOfgPAB7TQN+sNzQNouzmDJND7QctnmnuoPYPQ+sOG9rF/EJquVjH6Z6LW9oFUcuWvu4HdQKBNHuZ4dlQ/FdUjB1s/dbWKakFoNcnHsKby0PxqQWhc9ZlHPwo9X0Foe8McZ713A5mZFvd7N7AG8nt3/dBO3zoQaE+z7gyNq380VN0cmg82VJshNF/ta37mrxq0HpU7y6H5gf6XjzP/M9q3DuSZA6ya2xv4kYH4Sa1Yt4XtkwYtr/qY1z7moydr2PfSP8PUJKDVAVkeRu1xaPqi8CMD+fjiof7P5Wsgbzb93UDqs5zlnz0/cP1X9r0696o+OWg9YEN98HkOWo397VVRLQjND3usNWOe2rMY/VnvBhJyxetuoA8E9tOHY+47jlw/PdD2OuPqnvrucVVPbl0QjveMd4zUGKNW19D6wmNYa/tAKrny193AGsjr7n668x+f4FfQzvZwHXyUi/cooD39qkPj7B+sujk0n+sZQvPA9i9w2DhrYOOyX0It+XfEeiHe6Jvg6UCgfSJmZ4WmATP5aQ64/jUZtk+rzWafQNj80PKZzx4zrH54rkftC60H7PGe73QgtfgN8v/FEf7A7RTv/a6h+eunyhpoGmw40864WV852PdVCz7SV89nENq+2cOAxsEe9VR0P9j8chXXC6m38Qb5GsgbDKEeof+1VxLOn9TMB62mPlFz/a6DsPfrO8PUGjPfmQZtz1ld5R7pAfu/cNQe0PaCDas+5u4ZXC9kvJ0Xr3cDyZTGgG3So5a1vwdoPtdBaBxsmJoEbFy89wI2P7S81kDj0tuAW676Zzk0f9XsVbHqyWda5czjHQPansDHbiAf67+X3sAayEuvf795/3fI7ElBe0pqQVtA02D7Bhc9oadieKPy5mcatL30VISmAbaaItB/AgAt1whtDdvvBTZu5oOmexZoa0D7DQLX/fUHNSQ31gvxVt4EdwOBNkk4/7Q40SBsNcDNby16Arh+QmDD8AY0vhbDnlOHplkfVKsYPlE58/AJ10FofZMb0Lh4jVFzHRw94R6N3UAeLVy+n7mBNZCfudenu+4G4nMLzrpCe76wYbyJmV8u+hiw7wEbZ60Ix1o89odjn55gahLJxwhvqMHWV07Ue4RnPtj67gZy1HDxv3MDfSCwTQluc6cb9FjJDTkRbusBpSsC12/w1gdhz13Nl1+iJy5p/8o6Aa0ONuymksSbgM0H+7yU7NLUG9Bqd6YLAXsN9py9KvaBXPqsrze4gTWQNxhCPUIfiM+mijNOHdoTBKS+hO4FXP84A3o/4Mp14pJA46w7Qmi+S8n168gnfzUNv8Btj0G+Lq0PXoknf+kDebJ+lc1v4Gl29z9QZcKGXaF9QmD717ueoL7kY6jBvgdsHLS81ls7Q31Vg9YDNqx6cjjWqp7cmO01cnDe116w98HGrRfiTb0J9p/2QptSPRc0zk9DUB2aBhvONLl7mN4J2PplXaP2gM0HLddbfSPnOlh95uETru8htL2rL/UJaBrQ5fAGsPveuF5Iv6r3SNZA3mMO/RT9m/r4jGD7Bt7dlwTaM9MfvNCHX9ET1QCtxz1OHZo/fQw110FoPrUZQvMAXQauf3TAhulnaIRNl9NTEZqvcvorqlduvZB6G2+Q776pO7Wg54M2cUDq5hMVb6KLJQGu3kKd/p/u08ewZlyHl4PWHwh9GMDuHJrtVRGaH9DWzx2fJHDtCxuqVUxNAjYftLz61gupt/EG+RrIGwyhHqEPJM8pAe0ZAR8aw5+FPvHMG01fxfCJyuUMCbnkhlzF1Ccqd+afaTOu9jPXl/0S8sGsE8kN/a6PsA/kyLD4372B/tfe2QRnnMdTC8648DX0BOXzKTLkov9EuM+93jOfZ6uoT672latY9TG3V3C9kPF2XrxeA3nxAMbt+0DyXBKjIevZ04vXUHddMfUJPcGsjyK6YR+9roOjp3L6g+ETM3/4RHzGmS9eQ/+jOKubcX0gjzZevp+9gT6Qs09GPYK+ilVPXjU/BTOM15jp9tHjOqhfLShXMXyN1BqVH3M9QbXkY6jNsJ7DuspZoxbsA1Fc+Nob6D/LevQYdcLmY618MFMfQ//IZ60WTH0ifCK5ET0R3sg64bpi+DHUR35cz3ye4wzHPuPavrXHC17IeKy1rjewBlJv4w3y/i91z+IzCsrNMLrhk3M9888464Lq9qgYPaGnYnjDmiM9vplWOfN4jRnnXqKeIxx7xSdnj+B6IbmZN4o+EKdVMRNLVM6zn3GpMarPXK2imv3vobXVZ4+K6jP/jBv98cidYXyGPtdBuRnW8/aBzIyL+/0bWAP5/Ts/3bEPJM9qDJ/SrMPoreuZv3L2rWh99X02f6RH3dPcuqBc3ftRzpr0SVgXVJthvEYfyMy4uN+/gd1AMk3DqVX0iHpmqOcz+B197FH39exqroPVZx4+4bpi+DHU7R+Uu4f2So2xG8i9Ju+q/1fOtQbyZpPsP1z0ydTzzTif2RnWHvrucVU3d/9ZDz1qFdUqqtszKFd95tGNGacm6gnOuLO91ILrheQG3yhOf5aViSVm5/VTUFFf5czTx9Dn+h7aw7qKakH52k8uesJ1xfBj1B7mtcZ8pslV1F/RPSu3Xki9jTfI10DeYAj1CP2beiXNZ09KbfYcz/xqFe1VsermdS/zWmOuf4Z6rA+ecWc9Upf6RPJEciPrMeynp6JacL2Q8eZevN59U8+UDM/m+gj11ambP6LFY2/rKqrFZ8y4WjPmY531I451dW2PimN9XVeffWa6WnC9kHpru/z3if49JNN5Njy203cdtKdaxeifiVpr34r2qj45fa6DMy584qxH6uKpEc6ovLn9XFdUC64XUm/mDfI1kDcYQj1CH0iey2eiNhnzWZ/qmT1tubNaPcHa7ywf+6XWmNXpP9PiGfVwxqjVtXsH5ZMbfSCKC197A7uBOKkj/M7j+omqONt3tqc1M23G2de64Jlvps04+85w5s++hrrr4G4gmha+5gbWQF5z74e7futAZs9Wrp4gTzOhFqy6eTyJ6InkRtYJ10Hrwhty0ROujzCexJEuH0/CdcXwicqN54kWTyK58a0DsenC8xs4U791IJn2GG7uJ6Si2hHqVXcdPOPqGUaf66C+5GNkD0PNdVDOHhXVKqpXzjz9jG8diBssfP4G1kCev7sfqdwNxKd1hN95irqHfStnPtPkKo7+meYfDcGqm4dPuA7O+sZzL6wLps8Y1kc3dgMZi9b6d2+gD8RpPYpnx6w9nPyZv2q11tweroNyFe0T/Sj0BGce+0V/JM78s/73evaB3DMu/XduYA3kd+754V3+BQAA//8aFH3yAAAABklEQVQDABboqbmpme69AAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AccountSet-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AccountSet-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 