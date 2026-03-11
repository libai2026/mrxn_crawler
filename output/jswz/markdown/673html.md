---
title: "关于Nessus的新插件包使用和AWVS最新版的使用方式"
source: https://mrxn.net/jswz/673.html
---

# 关于Nessus的新插件包使用和AWVS最新版的使用方式

[Mrxn](https://mrxn.net/author/1)* 发表于2020/8/31 19:23
* 10819浏览
* [44评论](#comment)
* 22分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

一直都有朋友在留言或者邮件找我，问我是不是
[Nessus](https://mrxn.net/tag/nessus)
新的插件包不能在旧版本使用了，我今天测试了，是可以使用的。还是结合我之前发的哪个版本的，具体的可以看这里：
[**Nessus v8.9.1 系列Windows10上安装激活无IP限制版本**](https://mrxn.net/hacktools/659.html)
，今天我测试了下新的插件包：all-2.0(20200825).tar 为例，简单的说下如何使用，
  
  
前提：先停止
[Nessus](https://mrxn.net/tag/nessus)
服务，
net stop "Tenable Nessus" （需要管理员权限），详细的可以看上面的文章，有说明。
  
  
一句话总结：
  
  
关闭 Nessus 服务，下载插件包 all-2.0(20200825).tar ，然后解压到一个地方，然后以管理员权限打开命令提示符cmd窗口，使用 copy 命令覆盖替换到 Nessus 的插件包目录，开启 Nessus 服务，打开浏览器，等待重新加载插件即可。
  
  
啰嗦的解释：
  
  
一般路径为
[Nessus](https://mrxn.net/tag/nessus)
的安装路径下的 Nessus\nessus\plugins ,请自行查看你的安装路径，找到 plugin 目录，复制路径。然后进入到你的 Nessus 安装路径，我的路径是 D:\
Nessus\nessus\plugins\,
然后记住解压后的路径，例如解压在 D:\downlods\all-2.0(20200825)\ ，就在 命令行 cd
D:\

Nessus\nessus\plugins\  回车后，执行：copy

D:\downlods\

all-2.0(20200825)\* ./
/Y
  
  
回车后 等待几分钟，文件有点多，十二万三千多个，推荐这种命令行方式复制，图形界面，怕你卡死了....
  
  
复制完毕，开启 Nessus 服务。，打开浏览器，等待加载插件完毕即可使用。
  
[![关于Nessus的新插件包使用和AWVS最新版的使用方式](https://mrxn.net/content/uploadfile/202008/thum-3e8b1598878678.png "点击查看原图")](https://mrxn.net/content/uploadfile/202008/3e8b1598878678.png)
  
  
下面简单说下
[awvs acunetix\_13.0.200807155](https://mrxn.net/tag/Acunetix)
windows版本的和谐使用，目前最新版本可以使用的，激活状态如下：
[![关于Nessus的新插件包使用和AWVS最新版的使用方式](https://mrxn.net/content/uploadfile/202008/thum-5f3c1598878678.png "点击查看原图")](https://mrxn.net/content/uploadfile/202008/5f3c1598878678.png)
  
[![关于Nessus的新插件包使用和AWVS最新版的使用方式](https://mrxn.net/content/uploadfile/202008/thum-98071598878678.png "点击查看原图")](https://mrxn.net/content/uploadfile/202008/98071598878678.png)
  
  
也可以设置中文，路径在 administer-profile-language 选择中文即可，前提是上面要求填写的都需要填写好，然后保存即可。
  
[![关于Nessus的新插件包使用和AWVS最新版的使用方式](https://mrxn.net/content/uploadfile/202008/thum-bd251598878678.png "点击查看原图")](https://mrxn.net/content/uploadfile/202008/bd251598878678.png)
  
  
目前只有windows版本的工具 patch4awvs13.0.200715107 可以使用，对于目前最新版的 也适用acunetix\_13.0.200807155。
  
  
awvs 13.0.200807155

windows下载：
[Acunetix Windows and Linux 13.0.200807155 and macOS: 13.0.200807156 download now](https://mrxn.net/hacktools/670.html)

  
  
相关插件包和工具下载：
  
[Nessus](https://mrxn.net/tag/nessus)
插件包all-2.0(20200825).tar：
  
  
<https://cloud.189.cn/t/E7Zja27bM32y（访问码：qp4h>
）
  
  
也提供一个我上篇文章的初始版本的插件包all-2.0(20200321).tar：
  
  
<https://cloud.189.cn/t/nmYzyuZni2ey（访问码：mvj5>
）
  
[awvs](https://mrxn.net/tag/Acunetix)
工具：
<https://cloud.189.cn/t/a2QRn2FBFJNj（访问码：9hs9>
）

---

鉴于大家各种安装错误，我自己在虚拟机全部安装了一遍，做个总结：
  
  
1.Nessus 8.9.1 是可以成功安装，并且可以更新到最新插件包：all-2.0\_20200828.tar.gz 也是可以扫描的！不要再问重复的问题了,头大。
  
[![关于Nessus的新插件包使用和AWVS最新版的使用方式](https://mrxn.net/content/uploadfile/202009/thum-d6f01599107737.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/d6f01599107737.png)
  
  
2.Nessus的插件更新还是可以使用这种方法来更新，你可以在安装完毕后，停止Nessus服务直接更新到最新的插件包：
  
[![关于Nessus的新插件包使用和AWVS最新版的使用方式](https://mrxn.net/content/uploadfile/202009/thum-cc6b1599107737.png "点击查看原图")](https://mrxn.net/content/uploadfile/202009/cc6b1599107737.png)
  
  
3.awvs最新版的acunetix\_13.0.200807155 也是可以通过
patch4awvs13.0.200715107破解的(貌似没法扫描。。。暂解决).
  
  
4.如果安装完毕了之后，打开页面是空白的或者是其他错误，更换下浏览器试试，我测试的机器是chrome最新版，Firefox浏览器有几率打开awvs的页面是空白，推荐统一使用最新版的chrome浏览器。
  
  
5.终极大招：我把上述的工具打包成了虚拟机。你实在需要使用，但是自己没有配置安装好的，可以下载使用。
  

all-2.0\_20200828.tar.gz
插件下载：
  
  
<https://cloud.189.cn/t/yUr2qeZra2Ab（访问码：0iic>
）
  
  
<https://mega.nz/folder/LRFCiIAC#zIilB3PQU8nrZu4DVEIAQw>
  
  
虚拟机文件还在上传，上传完毕更新到这里。
  
  
parallels desktop 16 ：
<https://cloud.189.cn/t/Vzy6ZraEZVni（访问码：5njj>
）
  
  
Mac 平台pd虚拟机镜像：
<https://cloud.189.cn/t/ArQrIfMRnqui（访问码：rno0>
）

windows vmware可用的镜像：
<https://cloud.189.cn/t/ui2QvqQ7ZzQz（访问码：dz5d>
）

Nessus-8.9.1-debian6\_amd64.deb下载: https://cloud.189.cn/t/EBju6jVJn6z2 (访问码:zc7w)

* 标签：
* [#
  黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#
  nessus](https://mrxn.net/tag/nessus)
* [#
  Acunetix](https://mrxn.net/tag/Acunetix)

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
[关于Nessus的新插件包使用和AWVS最新版的使用方式](https://mrxn.net/jswz/673.html)
  
文章链接：
<https://mrxn.net/jswz/673.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/673.html"),
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
text: encodeURI("https://mrxn.net/jswz/673.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});