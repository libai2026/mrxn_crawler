---
title: "利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有"
source: https://mrxn.net/jswz/diy-myself-badusb.html
asset_dir: assets/利用u盘制作简单badusb，插谁谁怀孕，价格便宜，人人都可以拥有
---

# 利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有

[Mrxn](https://mrxn.net/author/1)* 发表于2016/4/1 13:34
* 26623浏览
* [28评论](#comment)
* 22分钟阅读

深入探索

恶意软件分析工具

漏洞扫描器

网页浏览器


(adsbygoogle = window.adsbygoogle || []).push({});

---

首先 来看一下 图(如果刷坏或者想更改Payload,需要短接39和40针，再用官方刷写工具刷新),注意红色箭头标志：

[[![利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有](images/img-001-d6c7b3dbf082.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201604/54de1459488860.jpg)](https://mrxn.net/content/uploadfile/201604/54de1459488860.jpg)

深入探索

数据库

安全工具开发

安全研究工具

**0x00 前言**

关于Badusb可以参看这个视屏：http://v.qq.com/boke/page/l/g/w/l01425u2igw.html

不是很新的东西，其他作者已对此做过研究测试，本文仅用来记录操作过程，保存日志，说明细节。

**0x01参考资料**

> https://github.com/adamcaudill/Psychson   
> https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads   
> http://zone.wooyun.org/content/20001

**0x02环境搭建**

1、硬件

```
U盘 ：东芝（TOSHIBA） 速闪系列 U盘 16GB （黑色） USB3.0 主控版本：Phison 2251-03 购买地址： http://item.jd.com/929732.html
```

2、软件

物流软件安全

Windows x64主机

（1）Java Runtime Environment ：Java环境，用于支持Duckencoder

（2）SDCC ：刷写U盘的环境，用于支持Psychson

（3）Visual Studio 2012 ：编译Psychson的开发环境

深入探索

安全

软件

漏洞预警服务

（4）Psychson ：BasUSB写入工具 （https://github.com/adamcaudill/Psychson）

（5）Burner File ：BN03V104M.BIN，必要的burner

（6）USB-Rubber-Ducky Payload ：编写Payload的参考代码 （https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads）

（7）Duckencoder ：用于编译Payload

（8）chipgenius 芯片检测工具 ：用于确定U盘型号

**0x03操作流程**

1、配置Payload

进入DuckEncoder文件夹

执行：

```
java -jar encoder.jar -i payload.txt -o inject.bin
```

说明：

```
encoder.jar：文件夹自带 
payload.txt：可参考USB-Rubber-Ducky Payload 
inject.bin：执行代码后生成的文件
```

2、生成固件

执行：

```
Psychson-master\firmware\build.bat
```

生成fw.bin文件

3、将Payload写入fw.bin文件

执行：

```
EmbedPayload.exe inject.bin fw.bin
```

说明：

```
EmbedPayload.exe：编译EmbedPayload工程得来 
inject.bin：操作1生成 
fw.bin：操作2生成
```

4、将生成的固件写入U盘

（1）执行

```
DriveCom.exe /drive=E /action=SetBootMode
```

设置U盘模式

（2）执行

```
DriveCom.exe /drive=E /action=SendExecutable /burner=BN03V104M.BIN
```

操作burner

（3）执行

```
DriveCom.exe /drive=E /action=SendFirmware /burner=BN03V104M.BIN /firmware=fw.bin
```

将fw.bin刷入U盘

**0x04 小结**

刷入成功后，下次插入U盘会模拟键盘操作，自动执行Payload

**0x05 补充**

如果刷坏或者想更改Payload,需要短接39和40针，再用官方刷写工具刷新

相关工具以及国外的工具资料包请在这里下载：[[![利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有](images/img-002-d52be2001975.png "点击查看原图")](https://mrxn.net/content/uploadfile/201604/b2f81459489784.png)](https://mrxn.net/content/uploadfile/201604/b2f81459489784.png)

链接: http://pan.baidu.com/s/1jIm22bk 密码: mrxn

欢迎私聊博主个人定制哦！价格实惠，保你满意，远控女神？试卷？老师的秘密？报复？格盘？改后缀？木马？都可以！哈哈

我只负责制作，怎么用那是你的事儿！你也可以自己按照教程制作，喜欢折腾的慢慢折腾去吧！

* 标签：
* [#攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
* [#渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#隐私窃取](https://mrxn.net/tag/%E9%9A%90%E7%A7%81%E7%AA%83%E5%8F%96)
* [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#badusb](https://mrxn.net/tag/badusb)

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

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有](https://mrxn.net/jswz/diy-myself-badusb.html)  
文章链接：<https://mrxn.net/jswz/diy-myself-badusb.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/diy-myself-badusb.html"),
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
text: encodeURI("https://mrxn.net/jswz/diy-myself-badusb.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 