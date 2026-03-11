---
title: "一条短信控制你的手机！ Android平台的SQL注入漏洞浅析"
source: https://mrxn.net/jswz/12.html
---

# 一条短信控制你的手机！ Android平台的SQL注入漏洞浅析

[Mrxn](https://mrxn.net/author/1)* 发表于2015/3/29 21:37
* 10545浏览
* [0评论](#comment)
* 43分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

**0x0前言**

14年11月笔者在百度xteam博客中看到其公开了此前报告给Google的CVE-2014-8507漏洞细节——系统代码在处理经由短信承载的WAP推送内容时产生的经典SQL注入漏洞，影响Android 5.0以下的系统。于是对这个漏洞产生了兴趣，想深入分析看看该漏洞的危害，以及是否能够通过一条短信来制作攻击PoC。

在断断续续的研究过程中，笔者发现了SQLite的一些安全特性演变和短信漏洞利用细节，本着技术探讨和共同进步的原则，结合以前掌握的SQLite安全知识一同整理分享出来，同各位安全专家一起探讨Android平台中SQLite的安全性，如有错误之处，也请大家斧正。

**0x1起：食之无味，弃之可惜**

鼎鼎大名的SQL注入漏洞在服务器上的杀伤力不用多说，可惜虎落平阳被犬欺，SQL注入漏洞在Android平台长期处于比较鸡肋的状态。比较典型的漏洞例子可以参考：
<http://www.wooyun.org/bugs/wooyun-2014-086899>

虽然Android平台大量使用SQLite存储数据导致SQL注入很常见，而SQL注入的发现也相对简单，但其危害十分有限：在无其他漏洞辅助的情况下，需要在受害者的手机上先安装一个恶意APP，通过这个恶意载体才可能盗取有SQL注入漏洞的APP的隐私数据（如图1）。很多人会说，都能够安装恶意APP了，可以利用的漏洞多了，还要你SQL注入干嘛。正是因为这个原因，导致SQL注入漏洞一直不被大家所关注。

![1](https://mrxn.net/content/uploadfile/201504/61dad5a4849e98a2f7c3fa65a187948320150418030914.png)

**0x2承：远程攻击的大杀器**

14年TSRC平台的白帽子雪人提出了一种存在已久，在Android平台却鲜未被提起的SQL注入利用方式：load\_extension。通过一些简单漏洞的配合，SQL注入漏洞可以达到远程代码执行的可怕威力。

简单来说，为了方便开发者可以很轻便的扩展功能，SQLite从3.3.6版本（http://www.sqlite.org/cgi/src/artifact/71405a8f9fedc0c2）开始提供了支持扩展的能力，通过sqlite\_load\_extension API（或者load\_extensionSQL语句），开发者可以在不改动SQLite源码的情况下，通过动态加载的库（so/dll/dylib）来扩展SQLite的能力。

![2](https://mrxn.net/content/uploadfile/201504/5f170bd6bbb88262ef9d6824953d287a20150418030916.png)

便利的功能总是最先被黑客利用来实施攻击。借助SQLite动态加载的这个特性，我们仅需要在可以预测的存储路径中预先放置一个覆盖SQLite扩展规范的动态库（Android平台的so库），然后通过SQL注入漏洞调用load\_extension，就可以很轻松的激活这个库中的代码，直接形成了远程代码执行漏洞。而在Android平台中有漏洞利用经验的同学应该都很清楚，想要把一个恶意文件下载到手机存储中，有许多实际可操作的方式，例如收到的图片、音频或者视频，网页的图片缓存等。类似的案例笔者也见到过，如下图远程利用SQL注入load\_extension在某APP中执行了恶意的SQLite扩展。

![3](https://mrxn.net/content/uploadfile/201504/0e4abcd21611a2bd46e29303a373193120150418030917.png)

**0x3转：攻与防的对立统一**

也许是SQLite官方也意识到了load\_extension API的能力过于强大，在放出load\_extension功能后仅20天，就在代码中（http://www.sqlite.org/cgi/src/info/4692319ccf28b0eb）将load\_extension的功能设置为默认关闭，需要在代码中通过sqlite3\_enable\_load\_extensionAPI显式打开后方可使用，而此API无法在SQL语句中调用，断绝了利用SQL注入打开的可能性。

![4](https://mrxn.net/content/uploadfile/201504/a69622a36b81ba8c69a5d8b14c11bec320150418030918.png)

凑巧的是，出于功能和优化的原因，Google从 Android 4.1.2开始通过预编译宏SQLITE\_OMIT\_LOAD\_EXTENSION，从代码上直接移除了SQLite动态加载扩展的能力（如图4）。

![5](https://mrxn.net/content/uploadfile/201504/08e96da2cdddad2ad06632e91d6af49d20150418030919.png)

虽然有了以上两层安全加固，但Android平台的安全问题往往不是这么容易就能够解决的。和Android平台五花八门的机型和系统版本一样，部分手机生厂商和第三方数据库组件并未跟随官方代码来关闭自身代码中SQLite动态加载扩展的能力，默认便可以直接使用SQL注入load\_extension，导致这些手机或者APP极易被远程攻击。

总结来说，利用SQLite的load\_extension远程实施攻击，适用于4.1.2以前的官方Android版本，或者是部分手机厂商的机器，又或者是使用到某些第三方数据库组件的APP。客观来看，这种攻击手法的攻击面并不算宽，并会随着高版本Android的普及和手机厂商的代码跟进而越来越窄。

那么除了最直接最暴力的load\_extension攻击方式之外，SQL注入是不是又变得一无是处了？在魔术师一般的安全人员手里，不管多么不起眼的攻击方式都可能被用到极致。百度xteam的CVE-2014-8507就是一个很好的例子。

**0x4合：一条短信就控制你的手机**

接下来，我们回到最开始的问题，如何通过一条短信来控制手机？

事实上在看到CVE-2014-8507后，笔者花费了大量时间尝试在标准Android机器中，通过彩信发送恶意so库，随后通过短信激活恶意so库的方式，来实现控制手机。最终由于SQLite自身的sqlite3\_enable\_load\_extension保护和系统代码其他若干个方面的限制，成功在smspush进程完成SQL注入后，却没有办法进一步利用恶意so库，无法完成正在意义上的控制手机。

另外一方面，百度xteam对CVE-2014-8507的利用已经很精彩，结合WAP推送处理代码的特点利用SQL注入提供数据，完成了打开通过短信任意APP的导出Activity的攻击，结合上其他的系统或者APP漏洞，不难达到真正意义上控制手机的效果。

作为狗尾续貂的补充，接下来和大家探讨一下如何在真实手机中通过自行构造PDU给任何Android 5.0以下机器发送含有SQL注入代码的WAP推送消息。

承载攻击的是WAP推送功能，而正常的短信APP无法通过短信发出WAP推送，通过短信群发等其他运营商提供的短信接口，也无法发出WAP推送消息。笔者通过一段时间对短信PDU格式的研究后发现，在Android vendor RIL之上进行一些修改，普通的手机也能够发出WAP推送消息。下图6的sendSMS函数（
<http://androidxref.com/4.4.4_r1/xref/frameworks/opt/telephony/src/java/com/android/internal/telephony/RIL.java>
）在每次发送短信前都会被系统调用，其中的第二个参数我们可以得到完整的原始PDU，通过对PDU内容进行一些修改，我们可以把普通的短信变成WAP推送消息。在此位置进行改动，随后PDU在替换后向底层传之后，也能成功的被基带解析并发送，接收方也能成功的接受并处理。

![6](https://mrxn.net/content/uploadfile/201504/4e1af5f1fe19aedccf30c84edb89514820150418030921.png)

普通短信的PDU中，包含了信息中心的号码，发送方的号码，接收方的号码，时间戳以及短信内容文本（如下图7）。而WAP推送和普通短信的最重要区别，就是WAP推送承载的是WBXML格式的多媒体消息而不是普通文本，通过修改PDU中的类型标志位并附加上WBXML格式的内容，一条合法的WAP推送消息就能成功的从手机中发出。

![7](https://mrxn.net/content/uploadfile/201504/d5dcb618891b77cccdd2c28ae1dc93ef20150418030923.jpg)

为了方便测试和演示，笔者写了一个转换WAP推送的Xposed模块（如下图）。激活后，通过短信APP中发送给任何人的普通短信都会自动转换成包含CVE-2014-8507 SQL注入漏洞的WAP推送，自动打开对方手机的设置界面。关键的PDU处理代码请点击
[这里下载](http://security.tencent.com/uploadimg_dir/other/tsrc-Hook.zip)
，请勿用于任何非测试用途。

![8](https://mrxn.net/content/uploadfile/201504/d74ebd6e3c653d6082c89cbf09831eba20150418030924.png)

**0x5后记：如何使APP的数据库使用更安全**

从2014年腾讯整体漏洞的数据来看，跟数据库安全相关的全部都跟SQL注入漏洞有关。因此，能够封堵SQL注入漏洞，基本上就能安全的使用数据库了。下面结合历史漏洞给出以下几点安全建议供大家参考（如果是腾讯的同学就方便多了，我们终端安全团队为业务定制了数据库安全组件）：

1.   不直接使用原始SQL语句，而是使用具备预编译参数能力的SQL API；

2.   如果一定要使用原始SQL语句，语句中不应有进行任何字符串拼接的操作；

3.   如非必要，记得主动调用SQL API关闭动态加载扩展的能力；

4.   使用数据加密（如SqlCipher）扩展SQLite数据存储的安全性。

**0x6相关链接**

[1]
[http://lcx.cc/?i=4428](https://lcx.cc/?i=4428)

[2]
<https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-8507>

[3]
<http://xteam.baidu.com/?p=167>

[4]
<http://www.sqlite.org/cgi/src/tree?ci=trunk>

[5]
<https://android.googlesource.com/platform/external/sqlite/>

[6]
<https://android.googlesource.com/platform/frameworks/base/+/android-4.4.4_r2.0.1/packages/WAPPushManager/>

[7]
[http://androidxref.com](http://androidxref.com/)

[8]
<http://www.gsm-modem.de/sms-pdu-mode.html>

* 标签：
* [#
  渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#
  黑客](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2)
* [#
  网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
* [#
  SQL](https://mrxn.net/tag/SQL)

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
[一条短信控制你的手机！ Android平台的SQL注入漏洞浅析](https://mrxn.net/jswz/12.html)
  
文章链接：
<https://mrxn.net/jswz/12.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/12.html"),
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
text: encodeURI("https://mrxn.net/jswz/12.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});