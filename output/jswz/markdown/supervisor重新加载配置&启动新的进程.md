---
title: "Supervisor重新加载配置&启动新的进程"
source: https://mrxn.net/jswz/Supervisor-reload-restart.html
asset_dir: assets/supervisor重新加载配置&启动新的进程
---

# Supervisor重新加载配置&启动新的进程

[Mrxn](https://mrxn.net/author/1)* 发表于2018/5/28 15:56
* 6227浏览
* [1评论](#comment)
* 20分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

一、添加好配置文件后。一般是在:/etc/supervisor/目录下,当然，我推荐大家在安装supervisor的时候呢，将主配置文件和其他需要守护的应用程序的配置文件分开，以便于管理和区别，这里把我的主配置文集贴出来，仅供参考：

操作系统

`[unix_http_server]  
;file=/tmp/supervisor.sock ; UNIX socket 文件，supervisorctl 会使用  
file=/home/supervisor/supervisor.sock ; (the path to the socket file)  
;chmod=0700 ; socket 文件的 mode，默认是 0700  
;chown=nobody:nogroup ; socket 文件的 owner，格式： uid:gid  
;[inet_http_server] ; HTTP 服务器，提供 web 管理界面  
;port=127.0.0.1:9001 ; Web 管理后台运行的 IP 和端口，如果开放到公网，需要注意安全性  
;username=usersuper ; 登录管理后台的用户名  
;password=yourpasswd.. ; 登录管理后台的密码  
[supervisord]  
;logfile=/tmp/supervisord.log ; 日志文件，默认是 $CWD/supervisord.log  
logfile=/var/log/supervisor/supervisord.log ;日志文件，修改为专门设置的目录  
logfile_maxbytes=50MB ; 日志文件大小，超出会 rotate，默认 50MB  
logfile_backups=10 ; 日志文件保留备份数量默认 10  
loglevel=info ; 日志级别，默认 info，其它: debug,warn,trace  
;pidfile=/tmp/supervisord.pid ; pid 文件  
pidfile=/home/supervisor/supervisord.pid ;  
nodaemon=false ; 是否在前台启动，默认是 false，即以 daemon 的方式启动  
minfds=1024 ; 可以打开的文件描述符的最小值，默认 1024  
minprocs=200 ; 可以打开的进程数的最小值，默认 200  
; the below section must remain in the config file for RPC  
; (supervisorctl/web interface) to work, additional interfaces may be  
; added by defining them in separate rpcinterface: sections  
[rpcinterface:supervisor]  
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface  
[supervisorctl]  
;serverurl=unix:///tmp/supervisor.sock ; 通过 UNIX socket 连接 supervisord，路径与 unix_http_server 部分的 file 一致  
serverurl=unix:///home/supervisor/supervisor.sock ;  
;serverurl=http://127.0.0.1:9001 ; 通过 HTTP 的方式连接 supervisord  
; 包含其他的配置文件  
[include]  
files = /etc/supervisor/*.conf ; 可以是 *.conf 或 *.ini`

二、更新新的配置到supervisord

`supervisorctl update`

三、重新启动配置中的所有程序

`supervisorctl reload`

四、启动某个进程(program\_name=你配置中写的程序名称)

`supervisorctl start program_name`

五、查看正在守候的进程

`supervisorctl`

六、停止某一进程 (program\_name=你配置中写的程序名称)

操作系统

`pervisorctl stop program_name`

七、重启某一进程 (program\_name=你配置中写的程序名称)

`supervisorctl restart program_name`

八、停止全部进程

`supervisorctl stop all`

注意：显示用stop停止掉的进程，用reload或者update都不会自动重启。

* 标签：
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

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
文章标题：[Supervisor重新加载配置&amp;启动新的进程](https://mrxn.net/jswz/Supervisor-reload-restart.html)  
文章链接：<https://mrxn.net/jswz/Supervisor-reload-restart.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读

安全工具开发


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Supervisor-reload-restart.html"),
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
text: encodeURI("https://mrxn.net/jswz/Supervisor-reload-restart.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 