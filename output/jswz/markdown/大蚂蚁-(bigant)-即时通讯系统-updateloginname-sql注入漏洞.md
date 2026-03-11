---
title: "大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞"
source: https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-updateloginname-sql注入漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/1 13:16
* 298浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

身份验证

Api

MySQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 \Api\Controller\UserController::updateLoginName 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过在 updateLoginName 功能的相关参数中插入恶意构造的 SQL 查询语句，实现对后端数据库的非法操作，可能导致敏感信息泄露、数据篡改、绕过身份验证，甚至在特定配置下实现任意命令执行或获取系统控制权限。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

SQL注入防护

深入探索

在线安全工具

安全运维咨询

安全研究报告

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

系统是基于thinkphp 3.2架构，大部分采用数组形式的参数传递不存在sql注入

在 ThinkPHP 3.2 中：

* `->where(array条件)` 使用**数组方式**传参是安全的（框架会自动参数绑定/转义）
* `->where("字符串拼接")` 使用**字符串拼接**外部输入是**危险的**
* `->query($sql)` / `->execute($sql)` 直接执行原生 SQL，如果拼接了用户输入则存在注入风险
* `I()` 函数虽有基本过滤，但不能完全防止 [SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)（特别是在字符串拼接场景下）

但是部分控制器的部分方法如**UserController.class.php**下的**updateLoginName()**方法中

深入探索

漏洞扫描器

网络安全培训

计算机安全

```
public function updateLoginName()
{
        $userId = $this->q('user_id',1);
        $newLogin = $this->q('user_login',1);

        //查看user_login是否存在
        $loginMap = [];
        $loginMap['user_id'] = array('neq',$userId);
        $loginMap['user_login'] = $newLogin;
        $hasLogin = $this->model->field('user_id')->where($loginMap)->select();
        if (!empty($hasLogin)) {
                $this->responseFail(ERR_OP_ERR,L('_USER_UPDATE_ERROR_')) ;
        }

        //查看user_login是否未变更
        $oldLogin = $this->model->where('user_id = '.$userId)->getField('user_login');
        if ($oldLogin == $newLogin) {
                $this->responseSuccess(L('_EDIT_SUCCESS_'));
        }
```

`$userId`来自用户请求参数 `$this->q('user_id',1);`，直接拼接到 `where('user_id = '.$userId)->getField('user_login')`字符串中，攻击者可通过构造恶意 `user_id`参数注入SQL payload造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 认证码参考[大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html) 的权限分析部分
>
> 代码安全审计

```
POST /api/user/updateLoginName HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

authen=cc7e6a614831d1c6b351a5f12678ed4b94cf98b2a52b1050d6c19433fdeff37d&uid=1&user_login=1&user_id=SQLI_POC
```

[![大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](images/img-002-0378e7462b13.webp)](https://image.mrxn.net/37defb6f8c0e49a7862f1e881bd7a5b1.webp)

成功利用报错注入获取到数据库用户信息。

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#MySQL](https://mrxn.net/tag/MySQL)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)  
文章链接：<https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 