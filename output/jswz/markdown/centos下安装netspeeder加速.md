---
title: "CentOS下安装netspeeder加速"
source: https://mrxn.net/jswz/net-speeder-vsp.html
asset_dir: assets/centos下安装netspeeder加速
---

# CentOS下安装netspeeder加速

[Mrxn](https://mrxn.net/author/1)* 发表于2015/10/18 22:47
* 36217浏览
* [7评论](#comment)
* 27分钟阅读

深入探索

OS

操作系统

安装


(adsbygoogle = window.adsbygoogle || []).push({});

---

1、作者项目主页，~~https://code.google.com/p/net-speeder/~~

已经迁移到github了：<https://github.com/snooda/net-speeder> （作者主页也有教程）

安装步骤如下：

Linux 与 Unix

安装[脚本](#)

获得安装包： wget http://linux.linzhihao.cn/shell/netspeeder.sh

运行安装包：sh netspeeder.sh

然后再看看进程，如果能找到net\_speeder ，说明它正在运行，安装就成功了

使用方法(需要root权限启动）：

参数：./net\_speeder 网卡名 加速规则（bpf规则）

最简单用法： # ./net\_speeder venet0 "ip" 加速所有ip协议数据

关闭net\_speeder方法：killall net\_speeder

2、net-speeder是一个由snooda.com博主写的Linux脚本程序，主要目的是为了解决丢包问题，实现TCP双倍发送，即同一份数据包发送两份。这样的话在服务器带宽充足情况下，丢包率会平方级降低。

3、net-speeder对于不加速就可以跑满带宽的类型来讲（多线程下载），开启后反而由于多出来的无效流量，导致速度减半，性能开销稍大和自由度有损失。所以，如果你的VPS连接国内速度一切正常，请不要启用net-speeder。

操作系统

4、安装net-speeder的方法也很简单，这里提供由lazyzhu.com博主写的net-speeder一键安装包。执行以下命令：

```
 wget --no-check-certificate https://gist.github.com/LazyZhu/dc3f2f84c336a08fd6a5/raw/d8aa4bcf955409e28a262ccf52921a65fe49da99/net_speeder_lazyinstall.sh
sh net_speeder_lazyinstall.sh
```

深入探索

vps

Linux

虚拟专用服务器

[[![CentOS下安装netspeeder加速](images/img-001-724c3ddf3079.gif "点击查看原图")](https://mrxn.net/content/uploadfile/201510/52061445183476.gif)](https://mrxn.net/content/uploadfile/201510/52061445183476.gif)

5、日后如果一键安装[脚本](#)下载链接失效了，这里给出脚本的具体内容，大家可以将将它保存为.sh文件，然后就可以执行了。

脚本语言

```
#!/bin/sh

# Set Linux PATH Environment Variables
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# Check If You Are Root
if [ $(id -u) != "0" ]; then
    clear
    echo -e "\033[31m Error: You must be root to run this script! \033[0m"
    exit 1
fi

if [ $(arch) == x86_64 ]; then
    OSB=x86_64
elif [ $(arch) == i686 ]; then
    OSB=i386
else
    echo "\033[31m Error: Unable to Determine OS Bit. \033[0m"
    exit 1
fi
if egrep -q "5.*" /etc/issue; then
    OST=5
    wget http://dl.fedoraproject.org/pub/epel/5/${OSB}/epel-release-5-4.noarch.rpm
elif egrep -q "6.*" /etc/issue; then
    OST=6
    wget http://dl.fedoraproject.org/pub/epel/6/${OSB}/epel-release-6-8.noarch.rpm
else
    echo "\033[31m Error: Unable to Determine OS Version. \033[0m"
    exit 1
fi

rpm -Uvh epel-release*rpm
yum install -y libnet libnet-devel libpcap libpcap-devel gcc

wget http://net-speeder.googlecode.com/files/net_speeder-v0.1.tar.gz -O -|tar xz
cd net_speeder
if [ -f /proc/user_beancounters ] || [ -d /proc/bc ]; then
    sh build.sh -DCOOKED
    INTERFACE=venet0
else
    sh build.sh
    INTERFACE=eth0
fi

NS_PATH=/usr/local/net_speeder
mkdir -p $NS_PATH
cp -Rf net_speeder $NS_PATH

echo -e "\033[36m net_speeder installed. \033[0m"
echo -e "\033[36m Usage: nohup ${NS_PATH}/net_speeder $INTERFACE \"ip\" >/dev/null 2>&1 & \033[0m"
```

5、安装完成后，会给出[脚本](#)用法，最简单的就是开启所有IP协议加速。执行以下命令：

```
nohup /usr/local/net_speeder/net_speeder venet0 "ip" >/dev/null 2>&1 &
```

6、net-speeder对于VPS速度有没有优化？就我自己的测试来看，速度和ping值都有所提升，但是流量也是双倍呀！所以对于流量吃紧的童鞋们来说，就别尝试了。。。当然，流量多的就无视。

互联网软件

* 标签：
* [#Linux](https://mrxn.net/tag/Linux)
* [#流量](https://mrxn.net/tag/%E6%B5%81%E9%87%8F)
* [#性能优化](https://mrxn.net/tag/%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96)
* [#vps](https://mrxn.net/tag/vps)
* [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)
* [#tcp](https://mrxn.net/tag/tcp)

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
文章标题：[CentOS下安装netspeeder加速](https://mrxn.net/jswz/net-speeder-vsp.html)  
文章链接：<https://mrxn.net/jswz/net-speeder-vsp.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/net-speeder-vsp.html"),
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
text: encodeURI("https://mrxn.net/jswz/net-speeder-vsp.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 