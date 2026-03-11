---
title: "【一日一技】快速从一堆jar包找到包含特定包名的jar"
source: https://mrxn.net/jswz/find-class-in-multiple-jars.html
asset_dir: assets/【一日一技】快速从一堆jar包找到包含特定包名的jar
---

# 【一日一技】快速从一堆jar包找到包含特定包名的jar

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/19 19:26
* 760浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

库

函数库

find


(adsbygoogle = window.adsbygoogle || []).push({});

---

在日常[java](https://mrxn.net/tag/Java)代码审计中，经常遇到项目包含一大堆jar包，全部放入库中会增加巨大的索引耗时，

编程

除了常见的spring struts2 等框架jar包可以放入库中，方便搜索相关路由外，我们只需要搜索到包含我们需要审计的jar包即可，方法也很简单，直接使用`jar tf`命令配合`grep -q`命令即可完成

这里以亿赛通为例，切到jar所在目录，或者直接写上完整路径也可以

> 搜索指定位置的jar

```
for jar in ./*.jar; do
    if jar tf "$jar" | grep -q 'com/esafenet/'; then
        echo "$jar"
    fi
done
```

脚本大致逻辑: 使用 `jar tf` 命令列出 JAR 包中的文件，如果找到包含 `com/esafenet/` 的路径，则输出该 JAR 包的名称。

开发工具

[![【一日一技】快速从一堆jar包找到包含特定包名的jar](images/img-001-bf545e9898e9.webp)](https://image.mrxn.net/13faa623bc334d02bd12fb7903688dcf.webp)

即可快速筛选出我们需要的jar包，然后直接右键加入库即可开始正常[审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)。

[![【一日一技】快速从一堆jar包找到包含特定包名的jar](images/img-002-c5c0483b17e0.webp)](https://image.mrxn.net/31e1491ce9be47a09246bd58bbb93ffa.webp)

win参考如下（[AI](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)生成，自测）

深入探索

安全运维咨询

编码转换工具

计算机安全

```
Get-ChildItem -Filter *.jar | ForEach-Object {
    if (jar tf $_.FullName | Select-String -Quiet 'com/esafenet/') {
        $_.Name
    }
}
```

# 改进版本

搜索当前目录及其子目录下所有jar

```
find . -name "*.jar" | while read jar; do
    if jar tf "$jar" | grep -q 'nc/bs/oa/oaco/im/'; then
        echo "$jar"
    fi
done
```

深入探索

文本剥离工具

物流软件安全

网络安全课程

win参考如下（[AI](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)生成，自测）

```
Get-ChildItem -Recurse -Filter *.jar | ForEach-Object {
    if (jar tf $_.FullName | Select-String -Quiet 'nc/bs/oa/oaco/im/') {
        $_.FullName
    }
}
```

比如今天有朋友问在[用友NC importExcelTemplate 任意文件上传漏洞](https://mrxn.net/jswz/yonyou-nc-importExcelTemplate-upload-rce.html) 文章下面问如何查看importExcelTemplate方法对应的jar包是哪一个，在nc的安装目录的`/home/modules`下使用如下命令查找包含`uap/lfw/dbl/cpdoc/impt/action` 包名的jar包

```
#modules find . -name "*.jar" | while read jar; do                           
    if jar tf "$jar" | grep -q 'uap/lfw/dbl/cpdoc/impt/action'; then
        echo "$jar"
    fi
done
./webdbl/lib/pubwebdbl_dblLevel-1.jar
```

成功获取到`uap/lfw/dbl/cpdoc/impt/action` 包名所在jar包`/home/modules/webdbl/lib/pubwebdbl_dblLevel-1.jar`

然后可以导入IDEA的库里用作类或者直接使用`jd-gui` 来查看

[![【一日一技】快速从一堆jar包找到包含特定包名的jar](images/img-003-9a1cbbd26b15.webp)](https://image.mrxn.net/4c3b10b9d0ef4c489d8aaad5e7025456.webp)

符合上面漏洞分析部分，对吧。

编程

其次是还可以使用批量反编译jar包成class，然后导入IDEA进行搜索，亦或者使用许少开发的`jar-analyzer`来进行处理后，再导入IDEA进行[代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)。

PS: 现在有[AI](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)辅助，代码审计、解释代码、写命令，写docker compose、写代码等等之前繁琐的工作变得更加方便快捷。

* 标签：
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#大模型](https://mrxn.net/tag/%E5%A4%A7%E6%A8%A1%E5%9E%8B)

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

* [1.改进版本](#toc-1-)



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
文章标题：[【一日一技】快速从一堆jar包找到包含特定包名的jar](https://mrxn.net/jswz/find-class-in-multiple-jars.html)  
文章链接：<https://mrxn.net/jswz/find-class-in-multiple-jars.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/find-class-in-multiple-jars.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/find-class-in-multiple-jars.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 