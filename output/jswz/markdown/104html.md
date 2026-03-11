---
title: "你还在为DNS被污染而烦恼吗？还在用google的8.8.8.8吗？现在改DNS为42.120.21.30吧，就可以进google了！"
source: https://mrxn.net/jswz/104.html
---

# 你还在为DNS被污染而烦恼吗？还在用google的8.8.8.8吗？现在改DNS为42.120.21.30吧，就可以进google了！

[Mrxn](https://mrxn.net/author/1)* 发表于2014/7/29 10:02
* 18782浏览
* [0评论](#comment)
* 47分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

下面介绍一下，方法在最下面，不喜欢的可以拖到最后看！

[openerdns](https://code.google.com/p/openerdns/)

[OpenerDNS: 是面向中国普通互联网用户开放的"高速 安全 免费"的域名解析服务器。](https://code.google.com/p/openerdns/)

# 介绍：

OpenerDNS: 是面向国内普通互联网用户开放的"高速 安全 免费"的域名解析服务器。 还在使用Google DNS或者Opendns吗？还在不断更改host文件吗？现在就切换到：

> OpenerDNS地址: 42.120.21.30

# 为什么使用OpenerDNS:

* 安全。我们保证解析数据的真实性，域名不被污染。你还在使用8.8.8.8吗？现在就切换到42.120.21.30，所有域名都准确解析了。
* 速度快。相比其他国外DNS，我们服务器托管在国内，速度更加快速，使你上网的反应更加迅速。
* 稳定。OpenerDNS自开通以来，短短半个月的时间就达到日均请求100万次。2014年6月，我们的日均请求数已经接近1亿次，我们依然很轻松。
* 加速访问Google。配合我们的动态3层代理技术，实现google的加速访问。
* 加速访问twitter。配合我们的动态3层代理技术，实现twitter的加速访问。
* 加速访问facebook。配合我们的动态3层代理技术，实现facebook的加速访问。
* 加速访问gmail。配合我们的动态3层代理技术，实现gmail的加速访问。
* 神奇吗？？还不快更改你的DNS：42.120.21.30

  # OpenerDNS 更新情况:
* 日期：2014.07.23
    
  最近由于用户数的激增，并且我们的技术升级还未最终完成，所以导致服务不太稳定，请大家耐心等待，我们很快就会克服这个问题。明天凌晨1点左右，我们要有短暂的down机，升级系统硬件，预计down机时间10分钟。
* 日期：2014.07.15
    
  添加line.me客户端的访问支持，解决line无法登录问题。测试安卓与windows客户端可以登录使用。其他平台未测，预计没有问题。line主页无法访问，因为他们不支持https模式。建立一Line群：OpenerDNS 有问题可以加群反映。
* 日期：2014.07.13
    
  onedrive已经恢复了。基本可以正确使用网页版，客户端版没有测试。域名解析到微软美国地址。 https模式访问即可：
  [https://onedrive.live.com](https://onedrive.live.com/)
* 日期：2014.07.09
    
  OpenerDNS 维护公告：由于近期DOS攻击以及访问人数的激增，从昨天开始OpenerDNS服务变得不稳定，中途有几次宕机。预计未来几天，由于我们要升级整个系统，OpenerDNS仍然会有不稳定的情况，请大家理解。预计升级以后，我们的服务能力将极大提高，敬请期待。
* 日期：2014.07.05
    
  OpenerDNS 更新。最近观察到BT客户端（迅雷等）在下载时会进行大量的无效域名查询，这会导致用户进入我们的临时黑名单中，从而暂时无法使用。为了应对，我们对于无效域名的A记录返回127.0.0.1。 普通用户应该可以正常使用类似客户端了。
* 日期：2014.06.24
    
  公告：到昨天为止，OpenerDNS经过半年多的成长，
  **日均查询次数已经突破了1亿，日代理流量超过100G**
  。这对我们来说是一个重大的里程碑，激励我们进一步提升服务质量。OpenerDNS还有很多不足，活跃的用户永远是我们强大的动力来源。
* 日期：2014.06.22
    
  play.google.com解析到美国地址。默认就可以在play上买设备了。
    
  [https://mobile.twitter.com设置三层代理。手机上可以用浏览器访问twitter.com了](https://mobile.twitter.xn--com-t28d02b1z5c361blctrkz.xn--twitter-fw3ks7dt6v8sgh33beon57t820a072em8g0r3c.xn--com-3h9d/)
    
  初步修复了安卓平台上的play商店，gmail客户端，以及账户同步功能。（完全顺畅使用还需我们进一步分析处理）
    
  wikipedia.org 可以用http访问，包括下属所有域名。https模式仍有问题。
    
  临时加入chromium.org的加速支持，方便国内的开发者吧！
    
  服务器分流工作初步完成, 现在比较少出现页面打不开的问题。如果还出现的话，请刷新页面即可。
* 日期：2014.06.20
    
  OpenerDNS 42.120.21.30 公告：从昨天开始由于流量巨大，我们解析到的地址可能会经常的访问断线。未来24小时，我们将加入分流服务器来解决这个问题。请大家及时刷新dns缓存。预计加入分流服务器后，大陆东部地区，联通、电信宽带的访问速度会非常好。
* 日期：2014.06.18
    
  针对google所有的服务（youtube暂时除外），提供访问支持。使用OPenerDNS google所有的web服务都可以继续访问，支持http模式，https模式（推荐使用）。
    
  在未来几天中，OPenerDNS: 42.120.21.30 预计可能出现不稳定情况。如果某个google服务无法访问，请告知地址（twitter:@Openervpn）我们将持续修复。
    
  鉴于我们的开发能力，我们现在希望寻找安卓与苹果手机平台app开发商的合作。 将我们的DNS服务通过App来快速设置到安卓与苹果手机上（类似DNS changer）。有意向的朋友mail：
  [[email protected]](/cdn-cgi/l/email-protection)
    

  **希望国内的朋友多多在微博、微信、博客等社交平台上宣传。我们会进一步的强大。**

  # OpenerDNS 加速的域名列表:
* 下列主域名及其子域名的A记录提供加速功能：
* appspot.com（考虑到节省我们的流量，暂时去除，仍然返回google地址）
* android.com
* blogger.com
* blogspot.com
* ggpht.com
* google-analytics.com
* google.cn
* google.com
* google.com.hk
* google.com.tw
* google.com.sg
* googleadservices.com
* googlesyndication.com
* googleapis.com
* googlecode.com
* googlelabs.com
* googleusercontent.com
* gstatic.com
* youtube.com
* ytimg.com
* [www.google.com](https://www.google.com/)
  |
  [google.com](https://google.com/)
* [Gmail](https://mail.google.com/)
* [twitter.com](https://twitter.com/)
  |
  [www.twitter.com](https://www.twitter.com/)
  |
* [www.facebook.com](https://www.facebook.com/)
  |
  [facebook.com](https://facebook.com/)
* [plus.google.com](https://plus.google.com/)
* [play.google.com](https://play.google.com/)
* [en.wikipedia.org](https://en.wikipedia.org/)
* [zh.wikipedia.org](https://zh.wikipedia.org/)
* [www.wikipedia.org](https://www.wikipedia.org/)
* [www.dropbox.com](https://www.dropbox.com/)
* [www.youtube.com](https://www.youtube.com/)
  ##实验性，需要chrome浏览器

  # OpenerDNS 安卓平台Google内置客户端程序支持情况：
* Google地图：完全支持。
* Gmail客户端：完全支持。
* Google+客户端：完全支持。
* 自动同步功能：完全支持。
* Keep：完全支持。
* 日历：完全支持。
* 环聊：完全支持。
* Google地球：完全支持。
* Play报亭：基本支持（首页图片加载可能会不全）。
* Play商店：支持浏览。暂不支持下载或者更新功能。
* Play音乐：未能测试。
* Play电影：未能测试。
* Play游戏：不支持。
* Google搜索：不能支持。（请使用chrome浏览器替代）
* 云端硬盘：不支持。
* youtube客户端：不支持。

  #

源地址：
<https://code.google.com/p/openerdns/>

[![你还在为DNS被污染而烦恼吗？还在用google的8.8.8.8吗？现在改DNS为42.120.21.30吧，就可以进google了！](https://mrxn.net/content/uploadfile/201504/6926eedf0bdbad6e74e39add80dfea3a20150419082555.png)](http://tietuku.com/2a6ffed0d2f7dd4b)

把第一DNS设置为42.120.21.30，就可以解析google了！然后可以用谷歌了哈哈！配合谷歌浏览器还可以看ｙｏｕｔｕｂｅ视频哦！可以不用工具上ｇｏｏｇｌｅ了，骚年门又可以干好多事！批量扫网址。。。。

第二DNS可以是你自己运营商的或者google的都可以！

欢迎转载，请注明https://mrxn.net/    谢谢！

* 标签：
* [#
  google](https://mrxn.net/tag/google)

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
[你还在为DNS被污染而烦恼吗？还在用google的8.8.8.8吗？现在改DNS为42.120.21.30吧，就可以进google了！](https://mrxn.net/jswz/104.html)
  
文章链接：
<https://mrxn.net/jswz/104.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/104.html"),
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
text: encodeURI("https://mrxn.net/jswz/104.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});