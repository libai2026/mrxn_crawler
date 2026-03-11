---
title: "雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人"
source: https://mrxn.net/jswz/627.html
---

# 雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人

[Mrxn](https://mrxn.net/author/1)* 发表于2019/9/30 21:44
* 14485浏览
* [7评论](#comment)
* 34分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

前言：
  
  

我们在做
**[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)**

的时候,我们往往需要使用
**[burpsuite](https://mrxn.net/tag/burpsuite)**

抓取 APP流量，需要抓取APP数据进行测试，因为往往通过APP都能有不错的发现，但是为了方便测试，我们如果没有安卓机的情况下，使用模拟器就是一个不错的选择，其一不需要另行准备安卓手机，其二也可以避免一些垃圾APP给自己造成不必要的麻烦，如锁机APP或者是近段时间闹得沸沸扬扬的送给最好的TA,这些APP。
  
  

需要准备的软件如下：雷电模拟器、burpsuite、需要测试的APP，雷电模拟器和 APP 直接去官网下载安装即可，burpsuite 相关软件资料可以查看我在
**[GitHub](https://mrxn.net/hacktools/burpsuite_pro_quick_start.html)**

上面的资源，应该还算全面，同时也希望大家贡献好的插件或则是文章，我会收录进去，最后夹带点私货(: 帮我点点star啊！谢谢！
  
  

总的步骤大致分为以下几步，其中每一步我都会在下面都有详细的图文介绍：1)电脑端设置好
[burpsuite](https://mrxn.net/tag/burpsuite)

的代理;2)模拟器设置代理;3)模拟器下载并安装证书并使用Android浏览器访问SSL网站验证SSL代理是否成功;4)打开APP开始抓取流量测试
  
  

0x01 电脑端设置好 burpsuite 的代理
  
  

首先我们通过 windows+R 运行 cmd, 通过 ipconfig /all 命令 找到自己的网卡的 IPv4 地址，这一步也可以根据自己的习惯了操作，比如通过 控制面板\网络和 Internet\网络连接 或 其他方式。我这里的 IPv4 地址是 192.168.6.244 ，这个 IPv4 地址记住，后面设置 burpsuite 的代理和 模拟器设置代理 都需要用到。
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/9b801569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/9b801569852670.png)
  
  

确认自己的 IPv4 地址后就可以设置 burpsuite 的代理设置了：绑定监听端口(Bind to port) 8080 (端口必须是未占用的端口，你可以设置高位端口),绑定监听地址( Bind to address) 我们选择 Specific address 192.168.6.244 在列表里选择刚刚查到的 IPv4 地址。自此 burpsuite 就设置好了。
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/db0f1569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/db0f1569852670.png)
  
  

0x02 模拟器设置代理
  
  

模拟器设置代理需要修改 设置 --> WLAN --> 鼠标左键长按 tplink --> 修改网络 --> 代理选择手动 --> 代理服务器主机名填写 刚刚的 IPv4 地址 192.168.6.244,代理服务器端口 填写刚刚 burpsuite 设置的 8080 ,然后保存，现在使用 Android 浏览器打开 http 网站在 burpsuite 就可以看到流量了。
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/2d931569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/2d931569852670.png)


  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/575b1569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/575b1569852670.png)
  
  

0x03 模拟器下载并安装证书并使用Android浏览器访问SSL网站验证SSL代理是否成功
  
  

如上面设置后好，就会发现打开使用了SSL证书的 https 站点会提示: 该网站的安全证书有问题。
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/902e1569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/902e1569852670.png)
  
  

burpsuite 此时肯定是不能抓到流量的，因此我们需要给模拟器配置 burpsuite 的证书，我们使用 Android 浏览器访问
<http://burp/>
或者
<http://192.168.6.244:8080/>
即可看到 burpsuite 的证书下载页面，我们点击 CA Certificate 即可下载证书:
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/e9b41569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/e9b41569852670.png)
  
  

一般默认在 文件管理器的 Download 目录下 文件名为 cacert.der 我们需要把它后缀改为pem,即重名为 cacert.pem
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/73231569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/73231569852670.png)
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/d5811569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/d5811569852670.png)


  
  

然后打开 设置 --> 安全 --> 从SD卡安装(从SD卡安装证书),找到下载的证书路径，默认就是 内部储存的 Download目录下,我们刚刚重命名过的证书，如果不重命名，Android 是不识别的。
  
  


[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/d93f1569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/d93f1569852670.png)
  
  
  
  

选择证书后，如果提示 需要先设置锁屏 PIN 或 密码才能使用凭据，就先去设置好 PIN 或 密码
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/13731569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/13731569852670.png)


  
  

然后根据提示填写 证书名字、凭据用途默认 WLAN 即可，然后确定，
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/937a1569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/937a1569852670.png)


  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/77c01569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/77c01569852670.png)
  
  

系统会提示安装成功!我们也可以从 设置 --> 安全 --> 信任的凭据 --> 用户 可以看到我们安装的 PortSwigger。最后使用浏览器访问
<https://www.baidu.com>
burpsuite 应该就可以抓到流量了。
  
  


[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/dd491569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/dd491569852670.png)
  
  

0x04 打开APP开始抓取流量测试
  
  

打开APP开始抓取流量测试，如果APP没有做其他的防护措施比如加固等等，burpsuite 应该就可以看到流量了。如果不能抓到 APP 流量但是可以抓取 Android 浏览器流量，这个时候就需要 脱壳APP或者是借助 Frida 这些来协助抓取，下次写。
  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/8d111569852671.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/8d111569852671.png)


  
  
[![雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/content/uploadfile/201909/8f001569852670.png "点击查看原图")](https://mrxn.net/content/uploadfile/201909/8f001569852670.png)
  
  
  
  

下面简单说一下 如何通过雷电模拟器的 adb.exe 来直接执行命令进行 清空和导入联系人到模拟器的通讯录(比如批量生成一定范围的手机号，去做QQ好友/微信匹配等等，希望你看到了不作恶)。
  
  

雷电模拟器通讯录格式如下：
  
  

BEGIN:VCARD
  
  

VERSION:2.1
  
  

N:;1-300-000-0000;;;
  
  

FN:1-300-000-0000
  
  

TEL;CELL:1-300-000-0000
  
  

END:VCARD
  
  

BEGIN:VCARD
  
  

VERSION:2.1
  
  

N:;1-300-933-0788;;;
  
  

FN:1-300-933-0788
  
  

TEL;CELL:1-300-933-0788
  
  

END:VCARD
  
  

其他模拟器或手机的通讯录格式，可以通过手动添加一个号码，然后导出到 sdcard 查看，即可使用python这些小脚本批量生成，不做过多的陈述。
  
  

雷电模拟器 adb 清空、导入联系人如下：
  
  

# 列出设备
  
  

PS D:\ChangZhi\dnplayer2> .\adb.exe  devices
  
  

List of devices attached
  
  

emulator-5554   device
  
  

127.0.0.1:5555  offline
  
  

# 先清除原通讯录联系人
  
  

PS D:\ChangZhi\dnplayer2> .\adb.exe -s emulator-5554 shell pm clear com.android.providers.contacts
  
  

Success
  
  

# 将正确格式的通讯录文件contacts.vcf, 导入android模拟器中, 并等待模拟器刷新几秒钟
  
  

PS D:\ChangZhi\dnplayer2> .\adb.exe -s emulator-5554 push contacts.vcf /sdcard/contacts.vcf
  
  

2596 KB/s (12978 bytes in 0.004s)
  
  

PS D:\ChangZhi\dnplayer2> sleep 3
  
  

#从文件中, 将联系人import到android模拟器的通讯录中, 导入过程耗时依联系人数量而定.
  
  

PS D:\ChangZhi\dnplayer2> .\adb.exe -s emulator-5554 shell am start -t "text/x-vcard" -d "file:///sdcard/contacts.vcf" -a android.intent.action.VIEW com.android.contacts
  
  

Starting: Intent { act=android.intent.action.VIEW dat=file:///sdcard/contacts.vcf typ=text/x-vcard pkg=com.android.contacts }
  
  

PS D:\ChangZhi\dnplayer2> sleep 10

* 标签：
* [#
  burpsuite](https://mrxn.net/tag/burpsuite)

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
[雷电模拟器配合Burpsuite抓取模拟器APP数据+使用adb清空和导入联系人](https://mrxn.net/jswz/627.html)
  
文章链接：
<https://mrxn.net/jswz/627.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/627.html"),
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
text: encodeURI("https://mrxn.net/jswz/627.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});