---
title: "如何修复usb接口出现该设备无法启动。 (代码 10)的小问题"
source: https://mrxn.net/jswz/USB-code-10-fixed.html
asset_dir: assets/如何修复usb接口出现该设备无法启动。-(代码-10)的小问题
---

# 如何修复usb接口出现该设备无法启动。 (代码 10)的小问题

[Mrxn](https://mrxn.net/author/1)* 发表于2015/11/12 22:39
* 13718浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

U盘

软件

注册表


(adsbygoogle = window.adsbygoogle || []).push({});

---

背景：今天晚上在写材料的时候呢，由于房间里面的灯太暗了（不明具体原因，可能是上次灯坏了，换灯管和镇流器时其中一个买到了假货-\_-|），灯是32W的节能灯，按理说不会太暗的，哎！不就结这个了。于是我就在箱子里找出了去年双十一在某宝买的一个USB接口的小灯（放置了一年了|+\_+），还带个夹子，可以夹在桌子上，为了避免广告嫌疑，这里就不贴图了！反正多得是，我运气不好吧，买到了这个玩意儿；

正常插上我电脑的USB接口上开始写材料，出于方便是插在usb3.0接口上的，材料字数有点多，大概写了一个小时左右，结束后拔下小灯，插上键盘准备码代码的时候出事故了，嗯，之所以要先拔掉键盘是因为穷买不起电脑桌，只能先把键盘拔下来挪开，然后好写材料。。。

计算机硬件

这时候我的键盘没反应了，我赶紧拔掉又重试了一下，还是不行，果断拔掉，换用本本自带的键盘，没问题，可以输入，于是把键盘插到另外的一个USB2.0接口上，啊哈！键盘又好了！于是开始探究什么原因导致USB3.0接口失效了。。。插上键盘，打开设备管理器，在里面发现了感叹号的标志，正是USB3.0 总线控制 哪里：[[![如何修复usb接口出现该设备无法启动。 (代码 10)的小问题](images/img-001-f47dabf8a633.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201511/44b71447342843.jpg)](https://mrxn.net/content/uploadfile/201511/44b71447342843.jpg)

我的乖乖，右键 提示：该设备无法启动。 (代码 10) ，接下来就是搜索了。自己也是第一次碰见这种情况。。。

根据如下搜索内容我跟着操作：

```
你好 解决方法 开始-运行输入regedit

定位到HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E96B-E325-11CE-BFC1-08002BE10318}

删除UpperFilters项

卸载设备，电脑重新启动。

然后设备管理器里变成：代码 10：该设备无法启动。

定位到HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E96B-E325-11CE-BFC1-08002BE10318}

添加字符串UpperFilters项，内容是kbdclass

卸载设备，重新启动
```

深入探索

云安全解决方案

漏洞修复方案

企业安全咨询

当然，他这里没有提示在操作注册表之前保存一下，我恰好有这个好习惯。保存之后再修改相应的键值（删除UpperFilters项），重启。这时候问题来了，TMD 自带键盘不能用了，没法输入密码，于是重启饶过密码，进入系统，从桌面恢复备份的注册表文件，重启，OK了!这回是都好了，usb3.0接口也好使了，自带的也没问题了。

Windows 操作系统

我得出的结论是，usb3.0接口由于之前长时间被小灯使用导致供电不足，然后再插入键盘、[U盘](#)这类小功率型的就不能识别了，解决办法就是先备份注册表，删除开机密码，然后重启，恢复，再重新设置密码！比较烦人。。。最好的就是使用充电器一类的插头链接这些USB灯，免得再次搞得本本的USB供电不足。当然，你如果知道你的外界USB功率大小和你的本本的USB接口最大功率，那就没问题了！

最后提醒：切记！切记！养成备份注册表的习惯！

* 标签：
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#注册表](https://mrxn.net/tag/%E6%B3%A8%E5%86%8C%E8%A1%A8)

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
文章标题：[如何修复usb接口出现该设备无法启动。 (代码 10)的小问题](https://mrxn.net/jswz/USB-code-10-fixed.html)  
文章链接：<https://mrxn.net/jswz/USB-code-10-fixed.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKcUlEQVR4AeybgXrjOA6D88/7v/NeYC4kWpIVp01r3476DQcUAFKuGKWZ7d2fx+Pxz3fjn3+/Rn3+lXZ7mBvhqMdZbtTPnHt4LTSXUbwic6Ncnhwjz1c4DeRZt/7c5QTKQJ7TfrwTs28g9wEewMy+acDmy7XON8PBX/YIIXpAj9IVuY3Wisw5F+8YcRB7WMvourOYa8tAMrny606gGwjE5GGMs0f1KwJqrf3WhBC6NaF4hfJ3AqIXUMrUp40ipgTobmWSv51C9IcxjjboBjIyLe73TmAN5PfO+tROHx0IxNUc7QyhASN5e+uAsda+/bxaA4f9oGruM3ogqD7r0HPWPoUfHcinHupv7nObgfjVCv2rEIL7zqAgengfoftBaFDR2hGqXnGkf5X/mYF89WlW3WMN5GYvgm4guoazePf5R71GPSDeLrIGPZd15RAeqJj3hODlVUCsoaL4NnKPVju7zj1G+ahPN5CRaXG/dwJlIFBfMfA6nz1ifjVA9Jr5s5ZrzZuD6AVY2uHIZ85Gr4UzzlpG1TiA7aN11p1DaHAOXScsA9FixfUnsAZy/Qx2T/DHV/A76I7u4fURjnwj7qj+Fe9eQoi3DeWKs7UQdcCrkk1X70/EuiHbcd7nr+lAgFM/uGbfjl81M480ON5LehsQfvcX2gOhAaYKAtv3BJRfyEHlIHL1a6M0eSbWnmn3B6IH9JjN0OvTgeTiG+R/xSN0A4E6tdEJQOh+hQghODjGUa/MqY8Cao+st7m8ipZ/tVaNA2Ivr4Wuh9CgojUhVB72ufq0oRoFVK/WiuztBiLDiutOYA3kurMf7twNJF8fV0B/zaByrrHfa6E5qH5zGSH0zKleYU65w1xGiB72ZMw+59a9Fo448QqI/lA/EIhvA6oPIm89eQ3hAdZ/7X3c7OsP1OkALx/Pr6CMwPZR0hzEGij9rAmBzQ8VxStKwTOB0J/p9gdiDWNUvWIzN39B1GQajjn1cbjGa6G5s6gaxSt/95b1qmDpP3sCayA/e75vdy8D0XVSQFxjOP+Dy7tC1KpPGxAazPu6l9A9lCu8FmrdBsQeLZ/XEB6ozwGVy17n2k8Bxz7pjrZOPEStcsfIVwZi8a/Dm33DZSAQE8zPBz1n3VMWmjNC1EFFa0IIXvksYO+DWAPDMj2LAigfGlqjdEeraW0N+h7WhPLmgOqXrsj62bwM5GzB8v3sCayB/Oz5vt29/IJqVKlrpxhp0F9ReRXZr3UbWW/z1qs1xF7KHa7zWjjiIGqtvUI454fwaV/Fq77yKLJPawVEL2D9S/1xs6/ylqVJKfLzQUxuxMnryPo7ueuFEHtBRfeSrvD6CCFqs666HFmD8B/p2ascwg/1I7P4NiB8mYees573LwOxuPDaE1gDufb8u91PDSRfKXeAuIKAqYLv+kvhQQKUf1dA5N4jl5iD8EDF7HM+8puzRwjRR7kD9pzrhPa8Qtj3kP/UQGRc8dYJfNk8HYimrYCYJNQfZuIdUHXY534ye4XmoHrFK6xlFN8G1FrY59nrPhAer4UQXPZDz2W9zdVHAVEHaNmF67JgDijvANOB5OKV/84JdL+g8tSEfgTlDnNQp2rOaK/QHBz75YHQlTsgOOhRvRX2CrVWKHdonQNqL3teIURN9kFwEJg17wehwRxz7boh+TRukK+B3GAI+RHKQHzNsugc+itnv9A+5QqvhRC14tuQ7mi1vB55RhzEXlDRPgjO64wQGtQPLVC57HWen6/NIWpb/mjtnsIyEC1WXH8CZSAQU82PBD1nHUIDTJWPboVICVB0iDzJwxTC51cWxBoqjgrtF0J47RPnGHGw99sjhNBgju4Pcx+Ert6OMhATC689gTWQa8+/2336Cyq7fQWFM84axFUETJX/L4Z6OIr4TIDtLe2ZHv5xXcZsNj/irEHsA/UHePa/m7tvroPYw5rQunKHuYzrhuTTuEFe/qXuqUFMF+orCCrnZ4bKudZaxpEGUZt9Z3KIOqj4qg6qF9jZgZe3cleQFv6+IHp4LbQNQoP5WarGsW6IT+8muAZyk0H4MU4NxNdJ6ELlDnNG80Ko1xYity+jvAoID1Bk4NtvLerdRtkgJa3naJ1KthTiGaG+PeVaCH0zT/46NZBJ/ZI+fALlYy/EBPNUZ3tB+IHOBmyvaKDTjghgq8l6fpY2tw+iDjC19QF2WMQXCezrgFIB7HoCRftUsm7Ip07yQ33Kx173A8qrYMS1r1St7TOKc4y4VrPnCCGe6UhveffPCH0P6219u4bXte4lhN7vntId5iD8wBX/y8XH+pqcwHrLmhzOFVL5od5eIz0MxFVS7oDgoMeRZ8ZZy+jnEGZeOdQ9pSvEzwKiRl7FzJs1eR3mvRbCvi/EGrC9vPVD/ShcxGeiPopnWv6sG1KO4h5JGQiwTVQTayM/aqtpbV25wmuh1grlDoi9vD5C2PvUxwGheS2E4HI/8YrMOYfe32owfnXbZ9QejhlnTQixv+uEZSAyrLj+BNZArp/B7gm6gUBcI6ioq+RwNVTdnNFeobmM4hWZcw61rzyKmQa9HyoHkY96zDhrQtj3EPfJgOgPrH+HPG721d0QvSLbgDpBiDx72u8JwgO00rYGtg8Q22LyF4Qv7+Ucem3Sqkiuz1jEZ2L+mZY/5iD2hHM/6EuDN5JuIG/U3sr6X3mYNZCbTbL8x8XRtZw9K9Trax8E5/VvIMSewNvbAdtbp7934dkmELUjv/oosgbH/uxbNySfxg3y8t+yZs+iaX81oH9lzHqNngP6HvblXuYyWs9cm0P0h4qt52gNUZN1CA4qZn2WrxsyO50LtDWQCw59tmX5oT4zQb160OeuhdC8FvotI6N4BYQfKop3uMZrqD5rUDn7rAnNQfVB5NLPhHvMEKInMLR5H2D7IAEMfeuGDI/lOrL7oe5JCv1Yymdh3wiB7RUx0kZc3qfVR9qIg9gTaFvs1kD3bNBzLhrtlbk2d50Qom/2iG9j3ZD2RHbr31+UnyEQE4T30Y/t6Xt9hBB72C888n6Xh9jLfbRXG9aE1iDqANEvA9huGzD0zvpaE64bMjy+68g1kOvOfrhzGYiuyzsx7DYg3XMgDSlgevVdBOHzOqP3HCFEHYwx93knz3uN6iD2m2nA+gXV42Zf5Yb4uSAmCWO0b4YwroXg/WqCWAOlnTWhSeUKrzMC5UbB61x9HLmPc4ge9gitjRDCDz2O/OrnsO61sBuITQuvOYE1kGvO/XDXjw4E4trm3XQN28j6LIe+38w/0ry3NYieUH8vbk9G+zNCX5t15+7jdUaoPTLv/KMDcdOF8xOYqR8diF8ZGb059K+M7HNuv9AcRK24NuzJmD2wrz3y5RrlEHVQMddC8Jlzrvo2Rpo5iF7A+tj7uNnXR2/Izb63/8vH6Qbia3SEZ75LqFfwjF8eiBrlDgjOzwKxhvoDGSrnuoyuNWbNOdQeELk1oWshNED0FsDhv4NcJ9zMzV8QtdId3UCamrX85RMoA4GYFpzD2XN62kKIfsodEBxUtHa278w30iD2yhr03JnnyD1mfoj+UDHXjvIykJG4uN8/gTWQ3z/z6Y7/AwAA///+LgHyAAAABklEQVQDAOJ16ZjpRhu1AAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/USB-code-10-fixed.html"),
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

闪存

  

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
text: encodeURI("https://mrxn.net/jswz/USB-code-10-fixed.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 