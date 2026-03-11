---
title: "在Windows平台下搭建WiFi蜜罐小计（附工具下载）"
source: https://mrxn.net/jswz/28.html
---

# 在Windows平台下搭建WiFi蜜罐小计（附工具下载）

[Mrxn](https://mrxn.net/author/1)* 发表于2014/12/26 08:48
* 22282浏览
* [0评论](#comment)
* 48分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

不知道大家对蜜罐了解多少，服务器上的蜜罐或许很多人都知道的，WiFi蜜罐你知道多少呢？

今天就小记一下自己搭建WiFi蜜罐的一些过程和心得体会。-----寒假闭关修炼 ^\_^ 更新少，但是我会把他们呢记录在doc里，

出关之时，分享给大家的。嘿嘿，下面就开始正文(所有用到的工具在后面贴出来了，此处应有掌声！)：

**目的**


**：捕获某APP的网络数据**

**Tcpdump抓包方式**

Tcpdump可以将网络中传送的数据包的“头”完全截获下来提供分析。

1.首先你的安卓手机得拥有root，手机开启调试模式与电脑连接。

2.将tcpdump拷贝到安卓的/data/local/tmp目录，adb命令如下：adb push c:\wherever\_you\_put\tcpdump /data/local/tcpdump。

3.修改tcpdump属性为可执行，adb命令如下：adb shell chmod 777/data/local/tcpdump。

4.进入adb模式，adb命令如下：adb shell

5.获得root权限，命令如下：su

6.到达指定目录/data/local/tmp，命令如下：cd /data/local/tmp

7.启动tcpdump开始抓包，命令如下：./tcpdump -i any -p -s 0 -w /sdcard/capture.pcap。参数说明:

# "-i any": 监听任何网络端口

# "-p": 混杂模式

# "-s 0": 捕获整个包

# "-w": 将数据写入指定文件

现在已经开始抓包了，停止抓包后将文件/sdcard/capture.pcap拷贝出来(adb pull /sdcard/capture.pcap d:/)，使用wireshark打开即可对其网络数据包分析了。

这种方式抓包我个人觉得很不方便，不过也可以很完全的捕获网络数据包，但是缺点很明显，手机系统为安卓，手机得root，反复的执行adb命令操作很是麻烦，而且不能在用户不知道情况下截获数据包，当时不知道别的方式就用这种方式分析网络数据包。

**Fiddler抓包方式**

Fiddler是最强大最好用的Web调试工具之一，它能记录所有客户端和服务器的http和https请求，允许你监视，设置断点，甚至修改输入输出数据. 使用Fiddler无论对开发还是测试来说，都有很大的帮助。

1.     电脑与手机连入同一局域网。

2.     打开Fiddler,     Tools->Fiddler Options 。 （配置完后记得要重启Fiddler）。

3.     选中"Decrpt HTTPS traffic",   Fiddler就可以截获HTTPS请求。

4.     选中"Allow remote computers to connect".  是允许别的机器把HTTP/HTTPS请求发送到Fiddler上来。

[![1.png](https://mrxn.net/content/uploadfile/201504/6ef1c3fa6c7a57b3ba723c687c14cdc320150418123057.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/4a471419558926.png)

[![2.png](https://mrxn.net/content/uploadfile/201504/cc8b6922aab3de29467962b78ca94d6420150418123102.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/fb5c1419558926.png)

5. 将手机设置代{过}{滤}理为fiddler机器的ip，端口为8888。

此时已经完成了HTTP抓包设置，如果要捕获HTTPS的包，只需要在手机端访问IP:8888，然后安装证书即可。

这种方式设置以及操作都很简单，而且不限制平台(IOS Android PC…)，均可捕获HTTP以及HTTPS，而且Fiddler还有更多强大的功能方便自己在测试调试时候使用，但是不能在用户不知道情况下截获数据              包，不可能让目标机器设置代{过}{滤}理，然后数据走向你的电脑。

Windows下WIFI蜜罐

最后想到了架设一个无密码WIFI，让目标自动连接后再来分析其机器的网络数据。

曾今在看雪看过一篇文章《Windows下的无线热点蜜罐》
<http://bbs.pediy.com/showthread.php?t=179529&highlight=%E8%9C%9C%E7%BD%90>

，读者也可以参考下，本人也实践过，确实比较方便，            但是本人机器出现分享的网络不稳定情况，所以放弃这种方式，换了一种更加简便的方式。

**工具：


**360随身WIFI**

，猎豹WIFI等**

**[![3.jpg](https://mrxn.net/content/uploadfile/201504/faeaa2e1fb205db7f900620a1ff687e820150418123104.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201412/799b1419558926.jpg)**

本人使用360随身WIFI搭建了一个无密码热点。使用
[wireshark](https://mrxn.net/tools/30.html)
监听本地网卡数据，等待目标机器连接。

不懂怎么使用wireshark的可以看我这篇文章：
[抓包利器----Wireshark---从入门到精通谢列教程](https://mrxn.net/tools/30.html "抓包利器----Wireshark---从入门到精通谢列教程")

[![4.png](https://mrxn.net/content/uploadfile/201504/ee25cf9e186d5190ff21cdef4d1b64b020150418123106.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/09dd1419558926.png)

这里使用
[吾爱破解](http://www.52pojie.cn)

的客户端APP做了测试，连接此免费WIFI蜜罐后，顺利抓到需要的东西。

[![5.png](https://mrxn.net/content/uploadfile/201504/78b3318c9de3f685ca05ff2c49197b3120150418123118.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/82661419558926.png)

只要APP使用明文传输数据，在WIFI蜜罐下均可能泄露重要信息，有人可能会说使用HTTPS传输就安全，下面将演示由于编码不规范造成的HTTPS在WIFI蜜罐下也可能被嗅探。

Windows下WIFI热点嗅探HTTPS原理与实现

在安卓APP中通常在进行账号密码验证中使用HTTPS，谷歌提供了安全的API供开发者调用，但是开发者由于各种原因未能按照规范进行使用，导致 自身产品出现漏洞。原理说明，最重要的一点就是开发者未能严格校验证书导致漏洞存在，谷歌提供的HTTPS API要求开发者对签名CA是否合法，域名是否匹配，是不是自签名证书，证书是否过期做检查，但是大多数开发者实现的代码如下：

|  |
| --- |
| class ae implements X509TrustManager    {    ae(ad paramad)    {    }    public void checkClientTrusted(X509Certificate[] paramArrayOfX509Certificate, String paramString)    {    }    public void checkServerTrusted(X509Certificate[] paramArrayOfX509Certificate, String paramString)    {    }    public X509Certificate[] getAcceptedIssuers()    {    return null;    }    } |

这段代码已经很清晰的暴露了问题。

实现WIFI蜜罐下嗅探HTTPS

开启两台虚拟机，一台用于用于搭建WIFI蜜罐，一台用于嗅探HTTPS。WIFI蜜罐如上一步已经搭建完成，在另外一台机器开启cain。

首先激活网卡

[![6.png](https://mrxn.net/content/uploadfile/201504/2d3260080a6e674dedaf9b1687391b6320150418123123.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/f19c1419558927.png)

选择ARP

[![7.png](https://mrxn.net/content/uploadfile/201504/679dd28cefbe1337b4aba2099153433120150418123140.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/9eb91419558927.png)

选择欺骗对象，左边选中网关，右边选择欺骗对象（也就是搭建WIFI蜜罐的机器）。

[![8.png](https://mrxn.net/content/uploadfile/201504/2420250792e30dd6f148e78f1f25afa820150418123144.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/602e1419559360.png)

选择HTTPS，输入需要嗅探的HTTPS IP，下载证书，然后进行欺骗。环境已经OK，然后坐等数据吧。Cain很人性化的将HTTPS请求与返回数据都捕获到了。

[![9.png](https://mrxn.net/content/uploadfile/201504/d31a4aa2c06c6d30e6534b36dd20020420150418123158.png "点击查看原图")](https://mrxn.net/content/uploadfile/201412/7afb1419559360.png)

从 刚开始不知道如何捕获移动端网络数据包，到最后完成一次完整的HTTP以及HTTPS数据包也是花了大概一周时间，期间遇见了不少的坑，当然也在 windows以及linux做了多次尝试，最后发现windows上面是最适合我的。现在移动端APP编码规范称次不齐，笔者已经在多款APP发现有这 些问题，在这里也提醒大家不要去连接未知的WIFI，即使写明了密码，如果实在需要连接也不要使用密码操作等敏感行为。

[Tools\_tcpdump\_cain\_fiddler\_wireshark\_download](https://mega.co.nz/#!BVBymDDY)

密钥：wvt4EtZ37iKwO0iS7IJ41c6lhimc7IpxPjlSAKzstR0

在此提醒大家，免费的未知WiFi，一定要小心啊！
大家可以跟着步骤走，练习一下。请勿用于非法用途！

* 标签：
* [#
  渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
* [#
  wireshark](https://mrxn.net/tag/wireshark)
* [#
  抓包](https://mrxn.net/tag/%E6%8A%93%E5%8C%85)
* [#
  隐私窃取](https://mrxn.net/tag/%E9%9A%90%E7%A7%81%E7%AA%83%E5%8F%96)
* [#
  黑客](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2)

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
[在Windows平台下搭建WiFi蜜罐小计（附工具下载）](https://mrxn.net/jswz/28.html)
  
文章链接：
<https://mrxn.net/jswz/28.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/28.html"),
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
text: encodeURI("https://mrxn.net/jswz/28.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});