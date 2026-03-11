---
title: "百度网盘MAC客户端netdisk_service服务浅析小记"
source: https://mrxn.net/jswz/baidupan-netdisk_service-analyzing.html
---

# 百度网盘MAC客户端netdisk\_service服务浅析小记

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/7 11:08
* 1106浏览
* [2评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 前言

前几日出了百度云Windows客户端
`YunDetectService.exe`
服务的10000端口的命令注入致
[RCE漏洞](https://mrxn.net/news/baidupan-windows-client-rce.html "RCE漏洞")
后，今日得闲，看了下MAC客户端是否存在同样的服务，发现也存在同样的服务，就粗略的看了下，献丑了。

# 正文

在没有打开百度网盘之前，通过
`lsof -i:10000`
命令没有发现任何服务，打开百度网盘后，发现了存在监听
`10000`
端口的
**netdisk\_service**
服务，因此粗略的审计一番。

然后通过系统自带的获得监视器找到了
**netdisk\_service**
服务

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/0148b18a365844fda3e074fef7331829.webp)

使用ghidra打开
`/Applications/BaiduNetdisk.app/Contents/Frameworks/netdisk_service`
文件发现了如下几个API相关的初始化

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/4e8a387cca4946eaaa4439fb893a82ce.webp)

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/9e479d91b14944b79e2292cdaa05b3b5.webp)

* `METHOD_GET_VERSION`
  为
  `"GetVersion"`
* `METHOD_GET_PCCODE`
  为
  `"GetPCCode"`
* `METHOD_DOWNLOAD_SHARE`
  为
  `"DownloadShareItems"`
* `METHOD_DOWNLOAD_SELFOWN`
  为
  `"DownloadSelfOwnItems"`
* `METHOD_OPEN_SAFEBOX`
  为
  `"OpenSafebox"`
* `METHOD_WEB_UPLOAD`
  为
  `"WebUpload"`
* `METHOD_HTTPS_DOWNLOAD`
  为
  `"/downloadpc"`
  (这看起来像一个URL路径)
* `METHOD_HTTPS_WEB_GET_LOGIN_TOKEN`
  为
  `"WebGetLoginToken"`

在本地使用curl测试获取登录token

```
curl 'http://127.0.0.1:10000?method=WebGetLoginToken'
```

可以成功获取到当前已经登录的百度云账户用户名（展示名displayname）、头像连接（portrait）以及最重要的
**authToken**

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/b96702cef1f441dc94d12faa74945eb2.webp)

拿到
`authToken`
就可以直接登录百度云盘等涉及百度账户的验证环境。

同样想看下
**OpenSafebox**
是否也存在类似Windows客户端的命令注入漏洞，

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/ad58fec238e7474db2bfd2b84ba6a57a.webp)

因此可利用交叉引用
**（XREF）从数据（方法名）找到使用它的代码（分发函数），再从分发函数找到真正的处理函数。**

如上图所示的XREF有很多，其中一个引用来自get\_request\_response函数，双击即可跟进函数的具体实现处理方式等，或者从ghidra的反编译窗口里找if语句调用的process\_open\_safebox\_request函数，同样可双击跟进函数内的具体实现方式。

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/170a54f5ea244e35ba6cf563fd48eacf.webp)

双击跟进后就来到了
`OpenSafebox`
请求的分发点

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/8f3a101796574a04b3d22b75c202bcb7.webp)

`process_open_safebox_request(HttpsRequestProcessor *this, int *param_1, string *param_2)`

* `this`
  : 指向
  `HttpsRequestProcessor`
  对象的指针，包含了请求的所有上下文信息。
* `int *param_1`
  :
  **输出参数**
  ，用于设置返回的 HTTP 状态码 (例如 200, 400)。
* `string *param_2`
  :
  **输出参数**
  ，用于设置返回给客户端的响应体内容。

然后根据不同的结果响应不同的状态码以及内容

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/d99a97f06a8e43f9bcbc690dadf38202.webp)

请求参数解读如下

```
local_40 = (string)0x4; // 字符串长度 4
local_3f = 0x6b75;     // ASCII "uk"
local_3d = 0;           // 字符串结束符

pHVar2 = (HttpsRequestProcessor *)std::__tree<>::find<>((__tree<> *)(this + 0x80),&local_40);
```

* 这几行代码首先在栈上构造了一个
  `std::string`
  对象，内容是
  **`"uk"`**
  。
* 然后，它调用
  `std::__tree<>::find<>`
  在一个树形结构（通常是
  `std::map`
  的底层实现）中查找这个
  `"uk"`
  键。
* `this + 0x80`
  指向的正是存储了所有请求参数的
  `map`
  。

下面属于对uk参数的校验

```
if (pHVar2 == this + 0x88) {
  _internal_log(0x40,"HttpsRequestProcessor::process_open_safebox_request uk not found");
  uVar3 = 1;
}
```

* `this + 0x88`
  是参数
  `map`
  的
  `end()`
  迭代器。如果
  `find`
  的结果等于
  `end()`
  ，说明没有找到。
* 如果找不到名为
  `"uk"`
  的参数，程序会记录一条日志
  **"uk not found"**
  并返回错误。

关键处理如下

```
else {
  // 从map中提取"uk"参数的值
  std::string::string(&local_40,(string *)(pHVar2 + 0x38));

  // 将"uk"的值传递给真正的处理函数
  iVar1 = open_safebox(&local_40); 

  // 根据open_safebox的返回值设置HTTP响应
  if (iVar1 == 0) { // 成功
    *param_1 = 200;
  }
  else { // 失败
    *param_1 = 400;
  }
  // ...
  uVar3 = 0;
}
```

然后我们跟进
**`open_safebox`**
，看下它的实现

![百度网盘MAC客户端netdisk_service服务浅析小记](https://image.mrxn.net/cf113443f20b44cca6ef0259f6d409d1.webp)

完整的反汇编如下

```
/* baidu::netdisk::service::open_safebox(std::string const&) */

undefined4 baidu::netdisk::service::open_safebox(string *param_1)

{
  int iVar1;
  undefined4 uVar2;
  void *pvVar3;
  void *pvVar4;
  pair<> *this;
  pair<> *ppVar5;
  ulong local_88;
  undefined8 uStack_80;
  void *local_78;
  void *local_70;
  locale local_60 [8];
  locale local_58 [8];
  util local_50;
  undefined4 local_4f;
  undefined1 local_4b;
  long local_48;
  void *local_40;
  undefined1 local_38;
  undefined4 *local_30;

  local_88 = 0;
  uStack_80 = 0;
  local_78 = (void *)0x0;
  pvVar3 = operator.new(0x20);
  pvVar4 = operator.new(0x60);
  *(void **)((long)pvVar3 + 8) = pvVar4;
  *(undefined8 *)((long)pvVar4 + 0x38) = 0;
  *(long *)((long)pvVar4 + 0x40) = (long)pvVar4 + 0x38;
  *(long *)((long)pvVar4 + 0x48) = (long)pvVar4 + 0x38;
  *(long *)((long)pvVar4 + 0x58) = (long)pvVar4 + 0x50;
  *(long *)((long)pvVar4 + 0x50) = (long)pvVar4 + 0x50;
  *(undefined8 *)((long)pvVar3 + 0x18) = 0;
  local_50 = (util)0x4;
  local_4f = CONCAT13(local_4f._3_1_,0x6b75);
  local_38 = 0x2e;
  local_70 = pvVar3;
  local_30 = &local_4f;
  boost::property_tree::basic_ptree<>::put<>(&local_88,&local_50,param_1);
  if (((byte)local_50 & 1) != 0) {
    operator.delete(local_40);
  }
  local_50 = (util)0x8;
  local_4f = 0x65707974;
  local_4b = 0;
  local_38 = 0x2e;
  local_30 = &local_4f;
  std::locale::locale(local_58);
  std::locale::locale(local_60,local_58);
  boost::property_tree::basic_ptree<>::put<>
            ((basic_ptree<> *)&local_88,&local_50,"open_safebox",local_60);
  std::locale::~locale(local_60);
  std::locale::~locale(local_58);
  if (((byte)local_50 & 1) != 0) {
    operator.delete(local_40);
  }
  base::util::convert_ptree_to_string(&local_50,(basic_ptree *)&local_88);
  if (((byte)local_50 & 1) == 0) {
    if ((byte)local_50 >> 1 != 0) goto LAB_10007560c;
  }
  else if (local_48 != 0) {
LAB_10007560c:
    iVar1 = send_message((string *)&local_50);
    if (iVar1 == 0) {
      uVar2 = 0;
    }
    else {
      uVar2 = start_netdisk_process((string *)&local_50);
    }
    goto joined_r0x000100075660;
  }
  uVar2 = 1;
  _internal_log(0x40,"ASSERT FAIL @ %s(%d)",
                "/Users/ferry5/ONLINE_SERVICE/other/ferry/task_workspace/2b7eb7a409efeaf01018ee5eb06 5b8ce/baidu/netdisk/pc-browserengine/source/startupservice/httpsservice/https_util.c pp"
                ,0xd5);
joined_r0x000100075660:
  if (((byte)local_50 & 1) != 0) {
    operator.delete(local_40);
  }
  pvVar3 = local_70;
  ppVar5 = *(pair<> **)((long)local_70 + 8);
  this = (pair<> *)(*(long *)(ppVar5 + 0x58) + -0x50);
  if (*(long *)(ppVar5 + 0x58) == 0) {
    this = (pair<> *)0x0;
  }
  if (this != ppVar5) {
    do {
      ppVar5 = (pair<> *)(*(long *)(this + 0x58) + -0x50);
      if (*(long *)(this + 0x58) == 0) {
        ppVar5 = (pair<> *)0x0;
      }
      std::pair<>::~pair(this);
      operator.delete(this);
      this = ppVar5;
    } while (ppVar5 != *(pair<> **)((long)pvVar3 + 8));
  }
  operator.delete(ppVar5);
  operator.delete(pvVar3);
  if ((local_88 & 1) != 0) {
    operator.delete(local_78);
  }
  return uVar2;
}
```

> 可以看到开发或者打包百度网盘这个功能的哥们电脑用户名ferry5，以及项目路径/baidu/netdisk/pc-browserengine/ ，为了方便调试而留的

整个函数的功能并没有直接的执行操作，更像是一个中间人，负责传话的。简析如下

```
// ...
// 1. 添加 "uk" 字段
boost::property_tree::basic_ptree<>::put<>(&local_88, "uk", param_1);

// 2. 添加 "type" 字段
boost::property_tree::basic_ptree<>::put<>
          ((basic_ptree<> *)&local_88, "type", "open_safebox", local_60);
// ...
```

* 代码使用了
  `boost::property_tree`
  库，这是一个常用于处理配置数据（如 JSON、XML）的工具。
* 它创建了一个数据结构，并向其中添加了两个键值对：
  + 键
    `uk`
    ，值是
    `param_1`
    (客户端传来的
    `uk`
    值)。
  + 键
    `type`
    ，值是固定的字符串
    `"open_safebox"`
    。
* `base::util::convert_ptree_to_string(&local_50, (basic_ptree *)&local_88);`
  序列化数据。
* 发送消息（传话）

```
iVar1 = send_message((string *)&local_50);
if (iVar1 == 0) {
  uVar2 = 0; // 成功
}
else {
  // 如果发送失败，尝试启动主进程再发送
  uVar2 = start_netdisk_process((string *)&local_50);
}
```

* 这是最关键的一步。程序调用
  `send_message`
  函数，将刚刚生成的包含
  `type`
  和
  `uk`
  的字符串
  **发送给另一个正在运行的进程**
  。
* 如果
  `send_message`
  失败（可能因为主程序没有运行），它会尝试调用
  `start_netdisk_process`
  来启动主程序，并把消息作为启动参数传递过去。

因此需要继续分析的话，就需要分析百度网盘主程序，看了一眼是个混血儿界面是
**Electron**
写的，还要跟踪分析
**寻找监听和读取名为
`"netdisk_unite_message_queue"`
的消息队列的逻辑**
，这就触及我的知识盲区了啊！等有能力的师傅去分析或者等我学会了再来分析。

通过本次简单分析并不是毫无收获嘛，我们找到了一个可用于蜜罐的百度网盘API，通过WebGetLoginToken获取已经登录的百度账户的token、头像、用户名等等信息。

* 标签：
* [#
  网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)

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
[百度网盘MAC客户端netdisk\_service服务浅析小记](https://mrxn.net/jswz/baidupan-netdisk_service-analyzing.html)
  
文章链接：
<https://mrxn.net/jswz/baidupan-netdisk_service-analyzing.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/baidupan-netdisk\_service-analyzing.html"),
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
text: encodeURI("https://mrxn.net/jswz/baidupan-netdisk\_service-analyzing.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});