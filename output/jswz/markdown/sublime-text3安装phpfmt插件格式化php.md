---
title: "sublime text3安装phpfmt插件格式化php"
source: https://mrxn.net/jswz/sublime-text-3-phpfmt-how-work-installation.html
asset_dir: assets/sublime-text3安装phpfmt插件格式化php
---

# sublime text3安装phpfmt插件格式化php

[Mrxn](https://mrxn.net/author/1)* 发表于2015/12/9 12:18
* 22639浏览
* [0评论](#comment)
* 40分钟阅读

深入探索

软件

plugin

安装程序


(adsbygoogle = window.adsbygoogle || []).push({});

---

sublime text3也支持php格式化的插件了，在这里向作者致敬，感谢他开发出这个插件，如果你不知道sublime就不要往下看了，免得浪费你的时间，[[![sublime text3安装phpfmt插件格式化php](images/img-001-30ce4780af7f.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201512/thum-faab1449638381.jpg)](https://mrxn.net/content/uploadfile/201512/faab1449638381.jpg)

首先是你的sublime安装了package control（插件管理包），如果没有安装，请自行百度搜索安装，一大堆教程，在你安装了package control之后，引用原作者的话就是：

开发工具

#### Install this plugin through Package Manager.

* In Sublime Text press `ctrl+shift+P`
* Choose `Package Control: Install Package`
* Choose `phpfmt`

1. 打开sublime，在sublime界面 按 Ctrl+shift+P 组合键，
2. 输入 install package,找到Install Package，并回车打开，
3. 输入 phpfmt 找到并回车安装，等待安装结束，

做完上面的工作，还不能使用phpfmt插件的，还需要配置插件所需要的php环境，最新版的phpfmt插件需要php5.6或者更高版本，这里，博主离线了两个在百度网盘，分别是php5.6和php7.0的非安全线程压缩包（都是64位的），直接解压到你想放的目录即可，如果需要其他版本或者是32位的请自行前往php官网下载，百度网盘地址：<http://pan.baidu.com/s/1kUn5zxl>  官方下载页面：<http://www.php.net/downloads.php>

深入探索

计算机安全

数据库

网页浏览器

将自己需要的安装包下载下载后，解压到你想放的地方，比如博主，防止wampserver的php目录里面，这是方便我的wampserver使用，你们可以根据自己的需要放置；接下来就是打开phpfmt配置：

Preferences > Package Settings > phpfmt > Settings - User

我将我的配置贴出来，供大家参考：

```
{
    "enable_auto_align":true,//自动调整对齐
    "indent_with_space": true,//自动空格
    "psr1": true,
    "psr2": true,
    "version": 4,
    "php_bin":"D:/wamp/bin/php/php5.6.16/php.exe",//php路径
    "format_on_save":true,//保存的时候自动格式化
    "option": "value"
}
```

深入探索

Web安全书籍

漏洞扫描器

安全研究工具

其中的php\_bin 很重要，就是你存放php的路径，其中的有些配置我在百度没有搜搜到，在国外的网站上看到的，试了一下还不错，原地址：<http://stackoverflow.com/questions/29350807/sublime-text-3-php-fmt-wont-work> 有兴趣的童鞋可以去看看。

安全运维咨询

配置完之后，重启sublime text3，打开你需要格式化的php文件，快捷键：Ctrl+F11 或则是在按下组合键Ctrl+shift+P后输入phpfmt 即可选择想要执行的操作，下面是一些常用命令：

```
The following features are available through command palette (ctrl+shift+P or cmd+shift+P) :

phpfmt: format now //立即格式化 ctrl+F11
phpfmt: indentation with spaces
phpfmt: toggle additional transformations
phpfmt: toggle excluded transformations
phpfmt: toggle skip execution when .php.tools.ini is missing
phpfmt: toggle auto align
phpfmt: toggle autocomplete
phpfmt: toggle dependency autoimport
phpfmt: toggle format on save
phpfmt: toggle PSR1 - Class and Methods names
phpfmt: toggle PSR1
phpfmt: toggle PSR2
phpfmt: toggle smart linebreak after open curly
phpfmt: toggle visibility order
phpfmt: toggle yoda mode
phpfmt: analyse this //Ctrl+F10
phpfmt: build autocomplete database
phpfmt: getter and setter (camelCase)
phpfmt: getter and setter (Go)
phpfmt: getter and setter (snake_case)
phpfmt: generate PHPDoc block
phpfmt: look for .php.tools.ini
phpfmt: reorganize content of class
phpfmt: refactor
phpfmt: toggle PHP 5.5 compatibility mode
phpfmt: enable/disable additional transformations
phpfmt: troubleshoot information
```

phpfmt插件作者项目在github的主页：<https://github.com/phpfmt/sublime-phpfmt>

实际效果看下面是我的亲测的code：

```
<?php
for($i = 0; $i < 10; $i++)
{
if($i%2==0)
echo "Flipflop";
}

// 格式化之后的样子
<?php
for ($i = 0; $i < 10; $i++) {
    if ($i % 2 == 0) {
        echo "Flipflop";
    }

}
?>

<?php
$a = 10;
$otherVar = 20;
$third = 30;

// 格式化之后的样子
<?php
$a        = 10;
$otherVar = 20;
$third    = 30;

<?php
namespace NS\Something;
use \OtherNS\C;
use \OtherNS\B;
use \OtherNS\A;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();

// 格式化之后的样子
<?php
namespace NS\Something;

use \OtherNS\A;
use \OtherNS\C;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();

// PSR version

<?php
for($i = 0; $i < 10; $i++)
{
if($i%2==0)
echo "Flipflop";
}

// 格式化之后的样子
<?php
for ($i = 0; $i < 10; $i++) {
    if ($i % 2 == 0) {
        echo "Flipflop";
    }

}

<?php
class A {
function a(){
return 10;
}
}

// 格式化之后的样子
<?php
class A
{
    public function a()
    {
        return 10;
    }
}

<?php
namespace NS\Something;
use \OtherNS\C;
use \OtherNS\B;
use \OtherNS\A;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();

// 格式化之后的样子

<?php
namespace NS\Something;

use \OtherNS\A;
use \OtherNS\C;
use \OtherNS\D;

$a = new A();
$b = new C();
$d = new D();
```

如果需要下载使用新版sublime text3 并且免费注册，请查看这篇文章：

## [(Mrxn分享)Sublime Text 3 Build 3065 安装版注册+汉化](https://mrxn.net/tools/3.html)

* 标签：
* [#编程](https://mrxn.net/tag/%E7%BC%96%E7%A8%8B)
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#php](https://mrxn.net/tag/php)
* [#mrxn](https://mrxn.net/tag/mrxn)

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

* [1.
  Install this plugin through Package Manager.](#toc-1-)
* [1.
  (Mrxn分享)Sublime Text 3 Build 3065 安装版注册+汉化](#toc-1-)



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
文章标题：[sublime text3安装phpfmt插件格式化php](https://mrxn.net/jswz/sublime-text-3-phpfmt-how-work-installation.html)  
文章链接：<https://mrxn.net/jswz/sublime-text-3-phpfmt-how-work-installation.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

开发工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sublime-text-3-phpfmt-how-work-installation.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sublime-text-3-phpfmt-how-work-installation.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 