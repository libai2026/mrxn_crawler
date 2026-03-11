---
title: "一段代码让nginx实现网站资源防盗链"
source: https://mrxn.net/jswz/block-file-nginx-protect.html
asset_dir: assets/一段代码让nginx实现网站资源防盗链
---

# 一段代码让nginx实现网站资源防盗链

[Mrxn](https://mrxn.net/author/1)* 发表于2015/9/24 21:36
* 10275浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

Windows安全工具

安全运维咨询

漏洞扫描服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

[[![一段代码让nginx实现网站资源防盗链](images/img-001-8f83fa8493c3.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201509/thum-a94c1443105550.jpg)](https://mrxn.net/content/uploadfile/201509/a94c1443105550.jpg)

很多人喜欢复制粘贴别人的东西，这没啥，说明有价值，作者应该高兴，但是呢，不留出处，这就不好了，于是呢，可以再服务器段简单的设置一下实现防盗链。

```
 location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|flv)$
        {
            expires      30d;
            valid_referers none blocked *.mrxn.net *.emlog.net *.qq.com;
            if ($invalid_referer) {
            rewrite ^/ http://i11.tietuku.com/0783ef75758999f8.gif;
            #return 404;
            }//防盗链
        }
```

资源类型可以自己增加或者是删除，第二句 expires 30d; 是资源在客服端浏览器缓存的时间为30天，这样可以加速网站打开速度，减轻服务器负担，更具实际情况做适当调整。下面几句就是防盗链的白名单，支持正则匹配，只是修改有点麻烦，每次添加或者是删除都需要修改配置文件。

深入探索

物流软件安全

编码转换工具

安全

具体的nginx配置专业术语可参考相关文章：

## [nginx配置location总结及rewrite规则写法](https://mrxn.net/nginx-location-rewrite.html "链接到 nginx配置location总结及rewrite规则写法")

## [nginx配置ssl加密（单双向认证、部分https）](https://mrxn.net/nginx-ssl.html "链接到 nginx配置ssl加密（单双向认证、部分https）")

## [NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](https://mrxn.net/nginx-ua-https.html "链接到 NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转")

## [SSL/TLS原理详解](https://mrxn.net/tls-ssl-understand.html "链接到 SSL/TLS原理详解")

## [OpenSSL 与 SSL 数字证书概念贴](https://mrxn.net/openssl-certificate-encryption.html "链接到 OpenSSL 与 SSL 数字证书概念贴")

## [基于OpenSSL自建CA和颁发SSL证书](https://mrxn.net/openssl-self-sign-ca.html "链接到 基于OpenSSL自建CA和颁发SSL证书")

* 标签：
* [#ssl](https://mrxn.net/tag/ssl)
* [#https](https://mrxn.net/tag/https)
* [#nginx](https://mrxn.net/tag/nginx)
* [#vps](https://mrxn.net/tag/vps)
* [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

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

* [1.
  nginx配置location总结及rewrite规则写法](#toc-1-)
* [2.
  nginx配置ssl加密（单双向认证、部分https）](#toc-2-)
* [3.
  NginxRewrite规则判断普通用户与搜索引擎爬虫（UA）实现https跳转](#toc-3-)
* [4.
  SSL/TLS原理详解](#toc-4-)
* [5.
  OpenSSL 与 SSL 数字证书概念贴](#toc-5-)
* [6.
  基于OpenSSL自建CA和颁发SSL证书](#toc-6-)



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
文章标题：[一段代码让nginx实现网站资源防盗链](https://mrxn.net/jswz/block-file-nginx-protect.html)  
文章链接：<https://mrxn.net/jswz/block-file-nginx-protect.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKkklEQVR4AeycgXbjtg5Ec/v//9znETIEJFKMko0tvy57gh1wZgAqhOk4257+8/Hx8e+fxr+f/4z6fEo7uOpz0cg/41w3wlo306tWa5xXXbn5P0UN5NFjfb3LCbSBPKb88Z2YfQO1z8hnvWrAB1CplttfsYklsV6oaQpse0LirIc14ayx9O9E7dUGUsmV33cC3UAgXy3Q51ceFbLOfui5+iqyb4aQPWqtc9dC+mCf2yM81omD8Ct3jHzWZgjRC8Y4qu0GMjIt7nUnsAbyurO+tNOvDsRXuyLEda3cpSd7mCBqIfBBTb/g3Ff3dw6931rdCMIHiVX/zfxXB/KbD/a39nrKQGD+SoLQ66GPXpnmRgh9j9rPuWu9rmitIkRfSLReayH0yv1G/pSBfPzGk/2lPdZA3mzw3UB8Pc9w9vzw59cYogckjvb080H6zI38EL6ZBjTZvYQmlR/D2giP3uN6VNMNZGRa3OtOoA0E6P5eB8652SPWV8LMVzWIvWa1EB6glv44B7bvebanmkP4lDug544ahAfm6DphG4gWK+4/gTWQ+2ewe4J/6nX9ab7reLKAvLYji/eG3gfB2SOEc672h/CZg1gDpra3LWDDRpZE+ykgPED7VxW2Sf+NWDfEJ/om2A0E8lUAfe7nhtTMGSE1v2qsCc1B+sQrrAm1VihXQPq1Vkh3aK3wuqL4Y1g/8lpD7jXymYP0wT63pyLsPbBfdwOpxW+W/xWP8w/sJ6RXh8Mn4LUQwq/ccfR5XdFeoXnlDoi+kGgfBGev8KgBpnYorwLofkaIV9QC6H3WITRItDZCmPu0t6LWrhtST+MN8jWQNxhCfYT2sdck5DXTdVLAnIPQ3WOEEB5gJA857V0D2N52gKEf2PShOCAh/JBY93PuUq+FI078WYz8I27dEJ/Km2D7oT6aLMQrp2rQc8fvpfqtjTiIXtD/oqU6CF35MeBcO3q19v7Kj2FNCH1fCA4S3QOC81oI1zh5FRB+4GPdkI/3+mcN5L3mkTcE8tpA5H5WiDXkWwskZ58Reg16Tm8RDteOEKK2aq4bYfU5h/Me9lSE8EN+z1U/7lu1WQ7ZFyKvvdYNmZ3eDVobSJ3SLId+qvZDaKPvwx4hhA8SXSPdYc5oXghRa00IwUl3iD8LCD8kjuogdGtCCA569H6QmjnVOsxB+tpALC689wTWQO49/2739ps6xLWpDug5XzcIDRKtVYTQa1/rlXMO4QdMdf8ySMKox4iT9zsBbL/tu1dFCA36H/TV5/0q59ya0FzFdUN0Mm8UlwYC+cqAyOtUnUNokOjvFZKDyK0JITj3qgihQY+qPQakz5r7eX2GV30Qe9gPsYa8PZDc2X5H/tJAjkVr/bwTWAN53tn+qPN0IL6OtbM5yOsIkdtnz1dov9BeiF6QKF1hT0VIH0ReddUpIDRIFH8MSB0iP3rqGsJT94Secw2EBmOcDsRNFn77BH5c8O2BQEy2viKc+ykgPICpHQLdR0vouWPfXZPPhT3CT+oyqOYYl4s/ja6HeH7gU/nYvkdghx/lH9cWKv9ysZIrv+8EpjcEYrqepNCPCqEBpoa/wFkE2itFfRSQ3MgHocursKcihAeufdxUHwdkLUReex9z11W0p3LOrQnNVRSvqNx0IDKveO0JrIG89ry/3G06EF8liOsMtIbWhMD2dmRRnOO7nP1fIcSe3kfoGuWOI+d1RXuFlXcOsRf0OPKYqwhRW7lRPh3IqGBxzz2BNhC9OhQQkwTazuKPAWy3AvKHaSv4IoGo/cLWyRB1kHtCcnCeuxmkx9+TNaG5EUp3WD+uxUPsofwYEBrg0h22gezYtbjtBNZAbjv68cbdQOoVA9rbEuzzkc9bQHpnnLUz9B4Q/bwWuka5Y8RZg74HBOe6M4TeB3sOYg20NkB3fn4eIfR6N5DWbSW3nEAbCPTT0hSP4aeE9NsDwXkthOBcd4byKqoO12pdo3qF1xXFKyB6wvUPBu6jeoc5o/mK1oTmlTvMVWwDsWnhvSewBnLv+Xe7T//rd7uhv+b1mkHoI7+5rxD2PeSveyiH8ECifA4I3uuKcK6p9yzcB6IHYKoh0H6Am6w9zY0QsnbdkNEJ3chN/7ssP9do0pBTHflqjXJ7hForlDu0Vng9QukO65DPcdTs+QnCvO9xL6+Fs/0g+0LkqnGsGzI7vRu0NhBPaPQMEJMEmmy/sJGfCdDeTyHyT2kDOOfUzwG9b2vw+MOeihB+6PFR8pQv6PeCc64+rx8I0t8GYvH5uHaYncAayOx0btDax97Z3vWaQV4viNz61R4jvzmInkBrB2xvgY14JNBz7jHDR2n3BdEL6LRK1L7A9kzmqm+Uj3zmKq4bMjq9G7npx16IVwEk1mk6Pz6/+YpHz9l6VgP9c5z1ucJD9Kt7Qs+5F4QGmGpYe5isHLDdKGtnuG7I2cncxK+B3HTwZ9u2gfh6QVwtyL+ersWQOuzz6nMO4fG6IoQGVPpSDpy+BUBo0KO/T+FoI/EKyNqZb6TNOJj3bQOZNVna606gfeyFmJxeHQ4/htdfIUQPSHSPihB67Vf1s7z6nUP0As7KNt7+bXH4A9huGyTaL4TglTvcAkKDxJFmriJkDUT+n7kh9Rv9f87XQN5sem0gvooQVwcSR88MqUPkI9+or30QdTBG+9zDayFEjXIH9JxroddcZ09Faz/B2sf5qI+1im0go4LFvf4EfjyQOlXnfnyvheYqij+Lka9yzs/qj7z9RoibAvOP9fafIUSfM/2Mr88H0QMSfzyQsw0X/2cnsAbyZ+f369XfHgjk9YLIf/2pPhvCvj/EGsb4Wbb7ncLcCCH6VM1vKRAa5FsbJFdrjjmkDyKf9bUm/PZAjpuv9e+eQPvrd7fVlI5hTXjUtBZfA+JVATRaPgewvYqb+Eig52b+R8n2ZY8Q+h6b6fGH9GM86O4Lokf12vQVV3XlrhNC3xeCg8R1Q3Rap/F6ofu7LMhpwbXcj61XhcJrIfQ9xF8JiFr1VFypkUdeh9ZnYQ/EPpA/L2oNpA6RV105BA9oeSm8f8V1Qy4d3etMayCvO+tLO7WB1GtzJZ91H9XP/NJco9wx4qzNENg+NACdDeg07yPsCh6EeMUjPf2S7hiZRhrks0DkbSCjJot7/Ql0A4GYFIxx9ogQNdUDPedXC4QGiaNaCL1q7lE559aEELUQKM4BwUGie1SE0F0ntA6hQY/2VIT0qY+i6t1Aqrjy15/AGsjrz3y649MHoit5jNET2VO1I+e10D7o3wIgOftUo/BaqPUxIGshcnsg1tD/vmKPUL0Vyh0QteJn8fSBzDb/W7XZ9/2UgUC8GoC2N9B93GziI4HQ/YoSPuhvfUHfQ30UbgThAUy154LkVOMANo/XQgjOTSDWgKmtBthQNYomPhLYa9KfMpDHXuvrhyewBvLDg3tWWTcQXZtZzB7EddUDcS1HnP0Vq8+5dYhegKX2/3m0R9jERwJsbxmPtPuC0FRzjM78DcK9agn0e1XdeTcQCwvvOYE2EIgJwjW8+rijV8uoFmLfqkFwEOhewupzDuHzuiKEplqHdQgNMLXdKmDDo1+mESdeAVGn3GE/hAb9R2d520C0WHH/CayB3D+D3RP8DwAA//+eYnYOAAAABklEQVQDAENZ5ZsYesTnAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/block-file-nginx-protect.html"),
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
text: encodeURI("https://mrxn.net/jswz/block-file-nginx-protect.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 