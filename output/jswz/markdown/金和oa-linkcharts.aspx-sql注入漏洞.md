---
title: "金和OA LinkCharts.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LinkCharts-sqli.html
asset_dir: assets/金和oa-linkcharts.aspx-sql注入漏洞
---

# 金和OA LinkCharts.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/7 13:31
* 256浏览
* [0评论](#comment)
* 19分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LinkCharts.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LinkCharts.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CrmWorkFlat.dll` 将其进行反编译后找到 **LinkCharts** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strChartArea = this.CustomerDistribute(this.Request["DeptID"]);
}

public string CustomerDistribute(string strDept)
{
  this.fc.ChartDivID = nameof (CustomerDistribute);
  this.fc.Position = "static";
  this.fc.ChartHeight = "100%";
  this.fc.ChartWidth = "100%";
  this.fc.ChartPath = "../FusionCharts/Column2D.swf";
  DataSet dataSet = new DataSet();
  StringBuilder stringBuilder = new StringBuilder();
  DataSet customerDistribute = this.an.GetCustomerDistribute(strDept);
```

跟进`GetCustomerDistribute`方法

```
public DataSet GetCustomerDistribute(string strDept)
{
  return this.dbo.ExecSQLReDataSet($"select d.deptid,deptname,deptparentid,s.sortlevel from department d inner join sort s on d.deptid=s.sortobjectid where s.sorttype = 'dept' and deptparentid='{strDept}'" + " select sum(isnull(a.c,0)) c,sum(isnull(b.s,0)) s,a.deptid from(select count(customer_id) c,customer_manager,r.deptid from jhbj_crm_customer c inner join relationshipusers r on c.customer_manager = r.userid where customer_state <3 and isfromcompany = 0 group by customer_manager,r.deptid) a left join (select count(customer_id) s,customer_manager,r.deptid from jhbj_crm_customer c inner join relationshipusers r on c.customer_manager = r.userid where customer_state <3 and isfromcompany = 1 group by customer_manager,r.deptid) b on a.customer_manager=b.customer_manager group by a.deptid");
}
```

参数`DeptID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CrmWorkFlat/LinkCharts.aspx/?DeptID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LinkCharts.aspx SQL注入漏洞](images/img-001-19474f6cda41.webp)](https://image.mrxn.net/7470b4c96e4940d8a0454ea79827430c.webp)

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
文章标题：[金和OA LinkCharts.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-LinkCharts-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-LinkCharts-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LinkCharts-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKY0lEQVR4AeyagXrbOAyD8+/93/muMAuJkWjH6dLE3536jQMFgJQnRkm77c/tdvvnb+Of7y/3+V7egbWM2ZD5Mc8+56Mnr+0RZv5Mrpq9yPWjJ2t/k2sgX/Xr11VOoA3ka+K3Z+LoDwDc4D6y3/tA91i3JjQH3QeRS1fYI9RaAeEB2p9J+pmAXguRu069HeYqtOcs5h5tIJlc+edOYBoIxKsCajx6VL8isqfiIHpby/ioNutjDnNfuOdyTd53zLOvyiH6Vpo5CA/UaF/GaSBZXPn7T2AN5P1nfrjjSwcCcTXzjjBzfnuofBB+6Jh9ziF098poT0YI/yMu62MO0QOe/2Zh7LW3fulA9jZZ/PkT+JWB5FdrlUN/pUHkR49c9aj8MPeqas25B0QdYKpE1wlLwwvIXxnI7QUP9n9tsQZysclPA9F1PIpnnx/Yfmp/VOc9s88cRA/oaB88z0HUuL97ZbQmhPDDjLlmzFV7FKNf62kgIld87gTaQGCePuxzr3jk/OqB2OuIy3va94jLunLXCWF/T3nHUI1j1PIaoi+cw1zbBpLJlX/uBNZAPnf25c5/fAX/Bt3ZPbwWnuXk3QuIq591CM79hVl3DuHzukIID/SfwKFzroHOaT+FNeWviHVDfKIXwcOBQLwiqmeF0IBK/jEHbN8mQ3+1uln1CoTuh8grn3tUmP3wsx65L0QPmPGR73AgufgC+f/iEf5ATNF/Wog1zK9Qe4TVqwp6LUQurwJiDWi5BdBuw0Z8/Zb7fi23X+bgnB/2fVvDJ3+D6OfnEEJwMKP0MbwldL+5jOuG5NO4QL4GcoEh5Edo3/ZCXKUsVjmEDzqOvnxdrWUOojZz9h3hI7/1qgfEnpWWuTM94PjtHM7t5X29p3DdEJ/KRXAaiKbkgJg0dLSW8ejPAr0WInctxBo4atE0oH0TAJE38SuB4NxfCPfcl+3wF4Q/m9RnjKwrH3WtxTu0VnidEWJP4DYN5La+PnoCayAfPf558/ZziK6TYrbc2n/HzDr0ayY+x9ke2ef6zDmH2MuejBAaYHuJwO7bHXTNvaFzbgidg8grP4TmOiEEZ79QvEK5Y90QnciFYhoIxCShf2sHnfOze6JC6Drc59IVcM9D75919xdC1EhXiHPAvSbdYY9w5LzOKJ8Doq/XQgiuqoHQ5HPY5/UzOA3kmeLlff0JrIG8/kz/quM0EF83YdUZ4opCR3kVR37pY8DcAzrnftA5iNzaswhRDx3H5xrX3gP2a+zZQ/esdOh9p4FUBYt73wm0gUCfEtznnq7Qj6bcYc5oPqM1IUR/5Q4Ibq/GPqN9EHVQ4+j3Wlj1EK+A3k9rhf1CCF38GDBrMHOuUz9HG4jFhZ89gTWQz57/tHsbiK9MdlScdYgrCJg6jVVfc0D7idoNrXkthPApH8N+IYQPAsU5XOe10NwjlFdhn3KHubMI8WzA+svF2+98/bhr+wcqd/CUheagT1D8GPaZ93oPIfrt6ebdD2a/NXv3cPRB9IKOuRaCz9zYI2vOIeoAUw+x6tvesh5WL8NbTqD9bS+wvXfnXSE4T1JoHUKDjkcazD77M2oPh/lxLR6in7WMEBog6xZZH/PN8P2bte/lLgDbeUFgNroHhAY0GbirA5qmZN0QncKFYg3kQsPQo7QP9eqamZPRAWxXzprQWoXSx6h8EH2zBsFB4NhH68pfcRA9oKN90DmIXL0dlc9ahbDfo/K7v3DdEJ3ChWL6UM8T9HNCTBwwtd0SYEPXNDElEJ5EtX8SzpxzCD/c/wOW9rBHCN0HkYsfQ3WKkc9r6WNA9ASaNXtMAtsZQEdrGV0L3QeRZ9+6Ifk0LpCvgVxgCPkR2kCqK2WjtT20z1j5rO1hVQP3VxpiDf3tLPdzj8xB1GTOOcwazJz9GSF81Z4VB+HPPaq8DaQSF/f+E2jf9sI8QQgOOvoR4ZiDrgMu2xDYPgj9ShJCcJvhF37THopHreVRZB/Es0FHeRTZ5xy6DyK3VqH6ONYNqU7og9wayAcPv9q6DcRXpjJZE0JcQeUOmDlr7gfhAUyVCGxvZzB/cLunEMKn3AHB5caj5nXG7IfokfUqdw3MfmsZ3eMR1waSjSv/3Akc/qReTdWPCvHKAEw1BKZXuXtlbAVfSeadQ/T5krdfEGuYb48MrssoPgf0Hpkfc5h90DmI3HUQa6ifDUKvng1CA9Y/4d4u9tXesjy5/HzQJweRW7c/Y6VB1EFH+6BzELk1oXtDaF4LpSsgNEDLLYB2QyHyTRh+g30tW2H26RkU9il3HHHWhBB9XSdsA5HhPbF2OTqBNZCj0/mANv2kDnGNgPJxdK0UwKm3hbLJN6k+jm9q6gn1h6T9rhdCPJM1ofgc4hzmvc5oTWheuQPmveyr0HVZMwfRC1gf6reLfbW3LE8ro5/1EWcd+qQhcmsZITToaN17PkKI2uxzj4zWYfbDzI1+wNQhAuXthuCPivPztoEcFSztfSewBvK+sz61UxsIxNWCjr5KVSfoPoi88lWc+2aE53pUfeFxj7ync4g6qL+BsC/vWXFZV26PUOu9gL5/G8ieefHvPYFpIJqmA/rkIHI/nj2P0P5HWPVxDdzvbf4MQtS6/6MaCH/lg9Cgo33uLzT3CCH6qMYxDeRRk6vq/5XnWgO52CTbX7/7yuTnqziIawbPYe4Lc23WnY/7Q6+zBzpnP3Su8kHo1ip0L6F15Xthj9Ae5Q7Y3xNCA9ZP6reLfbW/y/JzQZ8WRG4to18FGbM+5hC9gFG6WwPTT7x5D+cu8loIUavcUfnOaBC9oKN7ZYTQKw5CA7Lc8vE5JKzPEJ3ChWIN5ELD0KO0D3UtxqiulD1Ae2sxZ/9PsOphzgjzntA572u/sOLEK6DXQuTiFa7LKN4B936INWDLHboP0M4NIrcmXDfk7tg+v5g+1DUlhx/P6z20D2LicIyV/4izltHPkjk43hfI9pa7lxCYXsEQXCtIiWr2ItkOU4j+wPq293b49X6xfYZAnxI8l/ux/Urx+ifoHsKxXpzDmtfCI87aWVQ/x5ka6GdW+SF09xTap9yxPkN8KhfBNZCLDMKP0QbiK3MW3aDCRz2qGogrXWnmIDxQo30Z/SzmoNeayzj6s3aUu05Y+cQrYN4fOtcGUjVZ3PtPYBoI9GnBnP/0EWHupVfMGNB9P90r10H0M5f3M5cR7v1Zq3IIP8xY+av9MzcNpGqyuPedwBrI+8761E4vHQjM1xaCy9fSOYQGlA87+rwWukC5wxzQftq2ZrRnD498MPet+lQ9IGqzv/K9dCB5s5Xvn8CR8tKBeOIZvTnEKwQ6WttDCK91iDVgqt0E6NzR/q3wK7HvK51+Aa23RfuFFSdeYS2jeEXmnEPf66UD8QYLf34CayA/P7tfqZwGomt1FK98iryP+2bOeaWZyzj6Kw3620PWnUPoXgvdF0KDc+g6ofqMAdFHumMayFi01u89gTYQiGnBOTx6TOg9PPkjf9ag10Lk7gGxhv6foq0J3Qe6D+5ze4Rwr0HvK/1MaF9F5YW5f+XLXBtIJlf+uRNYA/nc2Zc7/wsAAP//mXv6OAAAAAZJREFUAwBoyMS5ymdqGAAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LinkCharts-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 