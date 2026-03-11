---
title: "Charles 的 SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations 解决"
source: https://mrxn.net/jswz/Charles-SSL-Proxying-not-enabled-for-this-host-enable-in-Proxy-Settings-SSL-locations.html
asset_dir: assets/charles-的-ssl-proxying-not-enabled-for-this-host-enable-in-proxy-settings,-ssl-locations-解决
---

# Charles 的 SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations 解决

[Mrxn](https://mrxn.net/author/1)* 发表于2022/3/6 21:35
* 7205浏览
* [0评论](#comment)
* 5分钟阅读

深入探索

数据包分析器

查尔斯代理

代理


(adsbygoogle = window.adsbygoogle || []).push({});

---

# Charles（Charles Proxy 查尔斯代理）

简介：  
Charles Web调试[代理](#)是用Java编写的跨平台HTTP调试代理服务器应用程序。它使用户能够查看从本地计算机访问的HTTP，HTTPS，HTTP / 2以及从本地计算机访问或通过本地计算机访问的已启用的TCP端口通信。这包括请求和响应，包括HTTP标头和元数据，其功能旨在帮助开发人员分析连接和消息传递。

代理与过滤

## 出现错误情形

[[![Charles 的 SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations 解决](images/img-001-2b6530380da7.png)](https://mrxn.net/content/uploadfile/202203/13be1646573915.png)](https://mrxn.net/content/uploadfile/202203/thum-13be1646573915.png)

在软件左边的区域抓包 HTTPS 的域名展开后出现 `<unknown>` , 其对应右边就是标题显示的错误说明:  
`SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations`

解决办法也很简单，提示就说明了，此域名没有开启 `SSL Proxy` ,直接在 `Proxy ---> SSL Proxying Settings` 下设置此域名和端口，或者均使用 `*` 将说有的流量都进行 `SSL Proxy` 即可。  
[[![Charles 的 SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations 解决](images/img-002-065573bd45da.png)](https://mrxn.net/content/uploadfile/202203/b96c1646574661.png)](https://mrxn.net/content/uploadfile/202203/b96c1646574661.png)

保存后再次进行抓包的 HTTPS 流量即可解密:  
[[![Charles 的 SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations 解决](images/img-003-c4685201762c.png)](https://mrxn.net/content/uploadfile/202203/b35f1646574719.png)](https://mrxn.net/content/uploadfile/202203/thum-b35f1646574719.png)

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

* [1.Charles（Charles Proxy 查尔斯代理）](#toc-1-)
* [1.1.出现错误情形](#toc-1-1-)



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
文章标题：[Charles 的 SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations 解决](https://mrxn.net/jswz/Charles-SSL-Proxying-not-enabled-for-this-host-enable-in-Proxy-Settings-SSL-locations.html)  
文章链接：<https://mrxn.net/jswz/Charles-SSL-Proxying-not-enabled-for-this-host-enable-in-Proxy-Settings-SSL-locations.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAPxElEQVR4AeyagXbjuLFE9+7//3OeLnqKaICQ7PHLjp1EOS5Vd1U1SBGk5HH277/++utfv4N//frfqxkju68mdr33+kHXraPL9jvUO+Kr9dq+I97OZnYtvV4QLRxdjvY77Ib89Rj+EI9Fbz/P5gzuHvAXMI6j/wwwc30N4NnI0IGxPhQP8fECdUzXerTjB2ZGXQyjvQCtq9KcqK5e7UV151f9j5DJsSFp3vz9V2DZEGC5y4CnZ+iOA7c88HRGA6bvGh1wv5ud2ZGZru/a3psFxvlaC0AaSL7zMB4v0R7l+IE5ByxrjsCTF6gsTN6jy4bs5rv/81fgyxsC97u530kw7wJYsz3nW4bKqtt/BJh5Z0RmrEXvofJdMyOiwZqJfuI+Zy1Oua9oX96QrxzsPfPxFfh/bQisdxXM3rtGvDoFqLw5AdXDnfX3teCeg9KSBVKO3/BO61yBVsCcAz79PdGW+FK5bIgnu+Mzq76aidfXgXqDJ++kOQs1A9gOJNt5GE9egHFhodgYVJ011H4H8Pn5HKPzfqxlQ3bz3f/5KzA2BGqX4TmfTi07DTWXDI++10Dawc/mhrm9JKvca/sA1vWjh/e59DB/2QDG05MZOTnrDqC3Sw13Dxhrw3POImND0rz5+6/A37kLPss5ZfOpd9aDuhteeeYEzCxUrS4ybw3lRQvrpQ5DZV95ZqFy1gKq73PWQl/02v4ZzP0u3k/Is6v5TfpxQ6Dukn5OcNfi5y6AygCxLgbG5+glPCmy1snePag1YfJpLto+n15OJgykHOcNLHyZnyhgnQWuKWBZ92/gMl8VnrQAlgWAa0z/I8DMZ7DPAMv6yXROPpp9r+0DdVjX7J7+R3iV3z37fT01oS4LqHNS6zg+IT3wrv/sFThuiDso+qlA7aj6jp6zBqQPAYynoQezdtesAWkAGHOnLJQ3go8XmL/aPtrbD6z5BFw7dVgtiAY1D3feM/ZQOWuxr3fcEINvfM8VGL/2Qu0aPOd9Jz1dqLy1gLXvGpTnOurCWkB5gPKAugDG06AIs7YPgJTX36uAMdfXsBZX+FHYdzyk8QM1D4zeF2Cs2evMqu2Ayp8y0WDN/Cc9Ifv7/a/sl9+ysmt5p/apoXYSiqOf2DmonLU45WDN9ByUlzm9IBpUJrocz1rA/A6ByicDpDyy8wIYT4a1AG559SBmemDMR3/FyxMC6yDMN5PFsxiQchwMZq+x59V+B5kPn2bjAdc5QNXJm0kdhjUTvbNzUDlrEb/XUJl4H7GzAmrOWkD1y4Z8tNjb/+evwPhS3w/jjgXxoHaw6702lx6wXRCviyet+8/qfc4+WWsB3J4a9R2Zg8qnPzFUBrjsrBcB5qdKtM7AOK+uWWed9xPi1fhBOH6pQ+0icJ1qdvASWhEPGLtvHxtKg2J1fWEtYHr2HfDcSw7ud6Xr7+h5IO2RYfrA9b5c0wFZWD8D1Fz3nemIB5V9PyG5Ij+Ex3dIdgxql9L3c4TyopmBu6ZuBsqz74DSAWM3AONuvBkPAZ57D3v5gXsWSsv5OAClWXckI3c9NdQcFEc/5dWC5MKwzo8nBFYRqncRmHXvs2BnqCzcP0KgPNcIoLS+xme85GHOw6z1s471KzzLQa0H9/eSmc5Q+VfHgsoAt1jWGhtyc/+XhB/2Xj+9IcDtoyS7CuWl9z1CaVAcD9BeEE8RuB2n61A+zDvXeTMnwMzHh9LSy67RobYD5hzM2lxmrYNXGqzzUP2nNyQHefM/ewXGr72nncxh44Wjnxhql5PtDOU5B1XHh+r1gnivGOZccpkPq6c+Mcw19KF65wIoTV8A0gCwPNHA0H0BhgfFrqcurDvUxPsJ8Sr8IIxfe3M+2bH0nWHusjk9KM26A+jtqJ0RNrKwFtYC5vcCMO4ufQHVA7YDzojRbC/ANW9GJGIt0ssw8+nlE5wNTj7UWnsGSgeuMeA6T8XxkQUlQrFGAKVlcaheP5r1Dpg5PVj7k+Z66iecPLiveZqFcw644q4vIuy1fQCv55LLWp3jAWMj0ifz/sjKlfghvGxIdisMXKcJjB29hBeF87Gh5tSEOpRmLWDt1QIoD772cQZkqev/3r2EQ+E5CphziQHXNYCq4c7Jnxgq7zHEnlk2ZDff/Z+/AuNL3Z0SULuX01DbEe/EycK8m6P1/Enrfq97FtbzS85MaqgMFOsFUBoUR5czHz5pJ8+ciCcD15Nk/wpQ55LM+wnJlfghPH7Lyrm40wLWXdOH0vQFoHxEfJgZYNw1ehmyFullmLnu7bV94Fyv7QOo9WA+tScvWhjmHFTdvV4Dacf3VBpgvOf08n6eez8+smAd7CEoLxpU7+I74LnXs1A5KI4HpBxvBNY+55AQMHLp5WTCXYPKx5P1P4K5Z8hs/PRytLAa1DlYn/D+yDpdlW/UXm4IcJ0acLsbY/Y7IFoY1jm4f3T0+dRhqHn7V2tC5WDlzHSGmYkOpaWXPaaA8mCyvtAX1gKQBoBxzaB4iL9eoDQodg3xckN+zb7pD16BZUOgdguKPQ937QQ9qBwUqwmYT8FpFu55wNEbMq8BjDvOWsTrrL4Daq7nrHvOXkBlu5daX9hD5aBYLTBzgv5JV9MTy4YovPG9V2D82usOiVenAh/fCZl3LVjzUD2Q2I2du4m/BJhP3S/pIriv6VpBgsB4wqA4vgylJXvS4sn6HWo7YF1z9+1hzYwnBFbR4I4cfNdPPTy/eD2/rwl1HnDnPrfXrrNrMNfQF6fMrpkTwGXZiwi9jnZic6J7wLgpoumL9GND0uz87v/8FRj/MHSHRA5vLeyhdhRWPnnOBHDPOxNfthfWotf2HXpQa1oLqB4mq4t9dtf01QJ7AbWWdbwwlJe+M0wPqoaVT3lYM+8npF+lH1CPL/XPnId3jOhZexEN5m6ri3jWIn1nqDl9qLr71no71HckA3MdmLV5qN4sVK0u1ARgOwCMz311oQilQbG60JOFtbD+LN5PiFfsB2F8h8C6y1B9P09YNXc8vrVIL0Pl1QVU3z2YWnRZQHnwnM0J1w+g8urBMw9I5GJgPA2X0AqYXtaMDdODqvdMsp2hstFefmS5YILWIv0r7jmoA6oJuP9KrC76mvYder3vtV4QPT2Q8sbJyjGtPwLMNZM9zQOf2lxnobLvjyyvxg/C+MjK+UDtUt/11LB6QMYu7tnUYWDcLfYw61PftWvxVkDNw+TYUJprCHUozboD6O2ogXGewOhPL64LXDm4P/WnOTWoOWvhWsJavJ8Qr8IPwtgQd6gD1l30fONbC3tZwD2vfsZU4T4Hpbm+SNoayosW1kt9Yn0Rz1rYQ60JxWo7oDwo7r7rCCgPuGx1AVxPU0x1AeVZi7EhCb35+6/A2BCoXYJid0pA9XDm/fShcn12z9jrC+sOmJ/FUGt135mOeFBZuM+bT27nV55ZqHWthXkB2C5QF4rAeCKshXpgL6Ay0aH6sSERww6I9CfWh1pk9wHtBcl0MVpYDxhvpmvR5WfY872Hj9dMPuxxUoeh1ukelAbFycpQGkxWF65xwtiQk/HWvucKjA2B2sGcAqy9OqyauxxAeVAcXYbSYLLrnWD+pKvpwVwD5seTnpmPADV/ykF5UGwGZm3fAavnOQgoHdbz0+vz9iKatRgbEvHN338FXv7pxNOD2nF3T0D1gPZTAMt3gbNBhqAyvX+WARIb/3WguUt4FMA4Hqz8sG55qIxe4HoivWwvrDvUgq5bq8sC1uN0T19AZaD4/YR4VX4Qxoa4cwJql6wFcJ0qMO7ASzgUzgiYn597DNilpQfGcaDY9YQhWUB5agKQBvQ7YHoj8HjpfmpgHPdhjx/1UTxeYPWgeji/T2fFY3T8QOVtYNb2O8aGRHQRATVkvSPZE8Ocg6ph5Y/mPnO8ZPpa0aCOF08dVi0elA5Eun28abiGsA7sRXrg2lCYtb45Yf0M+mLZkGfht/7nrsD4ay/UjkKxOyWA60yA6w6ICKvmjAASuVg9iJg+rA6M48DKZvQF3D0ozZyA6mF+rKgL13gGqLlnvvppDTUBGFkAjPekaEbA1NSh+vcT4tX4QRgb4o6J/by6Zi2SsQ6ifZah7gYozhy8vpuh8jluOPOduwc1B8U9l7rno4Wh5noGSksmbCb1zsAlmRMRrMXYkIhv/v4r8Ol/GALX56CnDUgD7qwAroy9GIEnL/oC5hxUDcX6ArhWAcZxYLIZcYV+FWo7flmD4o2mvQCtqxIYx7Xb56A8mE+5OZGsDJVT74DSlyfEAQFl9gH1Dj1Yc7tvJoCZTS5e+s7xwt1LHU+Guf7eQ3mwsrkdWVuOZ90Bc509Yw/lWwuYfdZRF3u/bIiBN773CiwbArWT+655ilAeFKsFsGpQPZDI8R9cwPURYBCQBvZzAEYWGL4vPZMaGLn0PRetM1TeXAfQ21EDY22brAGlQXH3rEWy1lA5KFbrWDakG+/aK/DnMTYE1t2C6mF+QWWXw/1Uo0HNvfKAbn9YA+Ou9Bh7GMpTh6rNCaheL4DSoFjdrLB+Bph5M+Zh1dSFniyshXVg3xE9PDYkzZu//wqMP530HdvrnCLc74hkkwmrp4aaUwvihWFmTppz6rKAyqvtgOdesq4hgEgXA+OJVIBZ2wfw/JMDagbOnDXCULn0n35CfAMigzLUYlCsJgBpwBkxml8vwPWmf0mDoHRg9L4AIwuT1YXr7lAX0a2hZqNB9d2D0pLRC6KF1aHyUKwWJLezPlQeipPRE5/eEMNv/PNXYPxLHWq34GPOKWVn5V1LL0Otaf0MrhF8JQPcxoDrycraUFoPxwt371mdbOdTFp4fL3moTNZ6PyG5Mj+Ex4Zkd17x75xvX2efg/mFGA/qLrHvs9ZqApCO6LkE1IQ9MJ4Wa6EurF/BjIB1HqoHrnFgOYaGs8J6h7qIDjU/NiTim7//CiwbArVLMPnVKULl9gxwSd4FArjdQQnpCyDSkYFlDageJu+DrrsjGfXUMNeAeorjndhZATVnLcxCabCynuhwpmPZkB78qAauSBaMYJ8aGBdRTajDXVM/wRnRPXsRrdfRoI4BRBrnAbO/jEfhGuJRjh/gyquLYTxe9rr3D/v6u516hx7MdeFef3lDXPyNf/8V+PKGuPM5HVh3Wh1KMyfUngFmFqqGlZ11HQHlqQmojxg9e2Ed2J8AtQ5M7jO9dh4qZ70D7h6UBsXOZM2d9cSXN8ThN/79V2DZkH3X7F8dUl8kYy3sZWEtYN4l9h3mhJrcoRZArdH91MmcGNa5ZDIrR4PKppehNHMCqofJ6oEzYu/VniHZZUOehd/6n7sCY0Ng7jSc69MpQWV3D7gkYPy2kjtAjgnlQXH0zzLUHEw+zXpMAZXrGbhr+j1vLaCy1jucEYA0ADx97yPweIHKPMrxMzZkVO+XH3EF/g8AAP//0SHv/QAAAAZJREFUAwAH4mXa/1/zMQAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Charles-SSL-Proxying-not-enabled-for-this-host-enable-in-Proxy-Settings-SSL-locations.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/Charles-SSL-Proxying-not-enabled-for-this-host-enable-in-Proxy-Settings-SSL-locations.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 