---
title: "孚盟云CRM ReportShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-ReportShow-sqli.html
asset_dir: assets/孚盟云crm-reportshow.aspx-sql注入漏洞
---

# 孚盟云CRM ReportShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/11 11:08
* 759浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

SQL

服务器

客户关系管理


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云ReportShow.aspx接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

漏洞扫描器

技术文章订阅

安全运维咨询

直接看 `ReportShow.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **ReportShow** 方法的实现如下

[![孚盟云CRM ReportShow.aspx SQL注入漏洞](images/img-001-0ea89697735b.webp)](https://image.mrxn.net/eb6fea39c5fc4f71af27fbb275407ebf.webp)

GET请求里的参数**templateId**未过滤或校验就被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。只不过需要注意的是此处使用的是MySQL数据库，因此在进行测试需要使用MySQL相关payload。

深入探索

安全认证考试

网页浏览器

网络安全会议

# 漏洞复现

```
GET /m/Dingding/ActiveReport/ReportShow.aspx?templateId=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"admin","corpId": "1","loginUser":"admin"}
```

[![孚盟云CRM ReportShow.aspx SQL注入漏洞](images/img-002-ca3e947ed82b.webp)](https://image.mrxn.net/29d46cfc098d43c78b9c8cdcf972ac6e.webp)

成功延时 3 秒

SQL注入检测工具

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
文章标题：[孚盟云CRM ReportShow.aspx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-ReportShow-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-ReportShow-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-ReportShow-sqli.html"),
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

代码安全审计

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKVElEQVR4AeycgXbbuA5Ec/v//7zPI2RImIRoJZvYflv2BBloZgDKhOjUOT398/Hx8c+/jX+GP4/6DfbjclVzGE6+5TpbMud8pdnzCN2jwke1V3UN5ObdX++yA20gt6l/fCWqFwB8AA/7VLXm8j2Yg+gLM9qTMfdwnvUxt0c4aroWr4Dvr6/6s9AajjYQExtfuwPTQGB+CqBzq9v1EwDdD5Gv6rIG4QcyfZp7TSFwnNBT802Qz3G7PL4g6oDjWt/sEepaoXwM8WcBHPcDNVZ100Aq0+aetwN7IM/b60sr/fpAfMRhPrb5Du27irnWuWthvdbo93VGmHvAzOWan8h/fSA/cZN/U49fGYifVGG1meIVMD9x0LmqduTgmh/CN9Z/5Vr3PMZX6q94f2UgH1dW3p5yB/ZAym15HTkNZDyS4/XqVmF+W4CZc4/cu+Lgca3rhBD+VV/5xsj+VQ7RHzqOvfL1qpe07HU+DcTCxtfsQBsI9KnD4/yrt6snwgHR/6s9IOqAsnTsD/33asDxqTkXwtc49xfmPmMO0ReuYa5vA8nkzl+3A3sgr9v7cuU/On7/NsrOAwn9+FqCzvkeoHP2Ge0RQvisPULVKB75rEP0B0wdb3nAgY38TNT7J2KfkM8NfRe4NBCIpwLW6CcEus9chXkTIGoqH4SW/c6zH8JXcRCa64T2KXdc5ew3QvSHjtbOEMKb9UsDyQUvzP+KpdtAIKYFHVc74CcpI0RtVQehQcdc6xroOkRunz2PEKIOaNaqB3D8PIAZ7Re6ifIxIGrtyQihQcesuxd0vQ0kG3f+uh3YA3nd3pcr/4E4LpUKofloZYTQgKk0+ybxRli/pcuvqz43qfzmgOntyXUVwtoPobt/hbmv9cxB9MjcPiF5N94gbx8MfS+eZEZrQoipVro5+cawJrQG0QswdfdvukwCp083dM1+reGoOGsrdF1GmNeyDueaPBC6cofX97VwnxDtwhvFHsgbDUO30gZSHR8ZFBDHDdDlEUB7GzmIk2/QfXCfe82MuQ2E31z2ObcmhHv/GSc+B0QdkOmWe60KgWMfsgYzZ701PUnaQE70/z79Zq+w/bUXYqrQsbpXTzoj9Bq4z6seKw56/eiDrkHk+T6cQ2hAawEcTzJ0tOg6IYRuTQjBwYyqUUDXVKOANQehq96xT4h27o1iD+SNhqFbaZ9DfGRErgLimEFH+92jQnse4Vdrod8HRJ7XGPtlbZXnOvsqDs7XdF3G3MM5RA/gY5+Qj/f6Mw3EUxNCTE75lYDwVy+xqq98mYPod7X2qs9rQPT3tdA9IDRA9BT2VQgcf4HI2tTghJgGcuLb9JN2YA/kSRt9dZlpIBDHDeZ/ZAa0vsBxLIHGrRKg+WHOXQtdqzgIPb8dOK/8I+frjBA9oWPW3R+6DpFn3yqH2Q8zNw1k1XRrl3fg28bpk7qfBiHEBJU7vJKvhSMHUQcd7RGqZgzxZ2HvmW4eYj1fZ3SPCrPPefZVnHWINaGj/XCNs1+4T4h24Y1i+cFw9RTAPH2/LtdltCaEXgv3uXSH6yE85oUwc/ZnlFcBsx9mzrUQGqDyKYDjZ6L9k+FGWMt4o9uX+Ubckn1CbpvwTl97IO80jdu9LAcC98dSR+xWc3wpd0D4DuH2DeIauF3Fl73CYO6/ix/DDvO+zggcbx3QsdIzN+buL4Tokz0QHHSUV2Gfcoe5jBC19giz7nw5EJs2Pm8H2l97vSTEJKF/MLQm1GQVsPbJq4DwKR9DfRwQPuhoPwRn7xmOfuivwTX2CCtOvMKaUNdjQNwTBGZdNYrMVTlErbyOfUKqnXohtwfyws2vlm6fQ2A+PlWBOR8xobkVQvSH/jYCnatqIXStoVh5gCbL6wDufug30y2Bew24sfOXe1VoN3C3Dtxfu9Z+oTno3n1CtDNvFNNAoE8L5tz3Dl0zZ/TkheYyQtRKHyP7nEP4oaO1R+j+9kHvMWryVJz4MSD6jHy+di+heYg6wNQdTgO5U/fF03dgD+TpW75esH0O0bEaoyoFjh9e2Vv5zGWfc2sQvQBTd2i/8U78vLAm/KRKkK7IIjC9FggOOroGZs6aeo9hTQhRmz0wc/uEaLfeKNpAIKaV783TrDgIP3S0D65x7i90rXKHua8izOu7h3tntCY0r3wMa8JR+861+ihybRtIJnf+uh1YDgTiSdMUHb5VX2eE2Q/Bue4RQviBZgWm9/ompiTfi/MkTylEX+g4mS4S0HvAnPt+oGtuDZ1bDsQFP4u722oH9kBWu/MCrQ3ERyrfQ8VZh37MzBmha1WPioOosSaE4Kq+cK/JA8HBjNIV0DVdjwGhZx5mzrruc4xKW3HWhG0gutjx+h1ov+31rUA8DVCjffmpgPBmzjmE5johBAcd7ZfuGDlfZ4TeY6yTz1yF0s+i8sO8FnQOIl/VZg1m/z4heYfeIN8DeYMh5FtoA4E4PvkIZ+OYQ/iBJgHH54VG3JLcz/mNPr58LTyI2zeIHtDxRh9fMHOH8PlNfRSflyVId0DvB/d5LrY/o/XMObeWcaVlXxtIJnf+uh2Yfttb3YqnK4R4kpQ7xhoID9R4Vqc+1jKKHwOid+YhOOjoPtk35vacIfR+ELm9Y698DeEFMt3yqsd/5oS0V/l/nuyBvNkAl59Dqnv1MQOOH+BAs1lrREqsCU0DUw9rP4XQ1wDu2upeFMC37wOi9q5xcQHhgxmzfZ+QvBtvkE8D0RMzBsxTHT26hvBVrwtCAyp5+YSq91ciL+A6c8ByLeg6RO7ajHCuZd+Y+34yZs80kCzu/Pk7sAfy/D1frtg+h0AcQei4qoTug8grv4/mSpPHOkQvwFT5FgM0HiJ3gfo5Ks4aRJ2vhfZXKN0x6hC9gFE6vQaO15AN+4Tk3XiDvP2115PP6PvL3Cq3PyPEU5DrrENogKkSXQscTxT0f7BtTVgVQ68BKkvrCbVeFn2SWvcsPi0H2AO09cwdhs9v+4R8bkQNz2eXP0OgTxPO8/G2PfmM0OtHf77ONZlXvtKkV5FrlFeezMkzRtbPcli/Pgg996567RNS7coLuT2QF25+tXQbSD5KV/KqmTmI4wmYKv8L8bxOMxYJ0H4Qwn1e2EsK7uuA0leRvk+g3cfos0c4amfXEP1U42gDOSva/HN3YBoIxNSgxu/eHsz9ql4w+/z0XPVXvopb9a38FQfz/UJw2b9aC8IP7P8E8+PN/kwn5M3u76+7nR8diI9lRojjmLlql61nzRzMPaxVmHt8NYdYC2aseq3WzxpEv6pH5n50ILnxzs93YKX8ykAgngbov3OCzlU3BKHnp6ryfZWD6Hu1zutn/4qDuf/Kn/tW+a8MpFpoc9d2YA/k2j49zTUNxMftDK/cWa61P3POrQkrTnwOiLcHWGOuGXOvIxw1XUP0Vj6Gahxw7oNZg5kb++t6GojIHa/bgTYQiAnCNVzdMvQe9sGag9Dtz+inMmPWnVuH6AX9LxX2ZITwuS5j9jmH8AOm2u/ogOn3XNA5926FKbEmbANJ+k5fuAN7IC/c/Grp/wEAAP//3r+wQAAAAAZJREFUAwDhd4Kb53eD4wAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-ReportShow-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 