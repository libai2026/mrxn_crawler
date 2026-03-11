---
title: "Oracle 11g sys和system用户密码都忘记了的解决办法"
source: https://mrxn.net/jswz/modified-Oracle-system-password.html
asset_dir: assets/oracle-11g-sys和system用户密码都忘记了的解决办法
---

# Oracle 11g sys和system用户密码都忘记了的解决办法

[Mrxn](https://mrxn.net/author/1)* 发表于2018/4/26 14:17
* 7026浏览
* [7评论](#comment)
* 10分钟阅读

深入探索

客户关系管理

Oracle数据库

CRM


(adsbygoogle = window.adsbygoogle || []).push({});

---

最近因为工作需要在学习Oracle，但是我这个人记性不好，当初设置的system密码忘了。

搜索查看了很多的关于忘记Oracle密码的解决办法，加上自己的亲自实践（前车之鉴），得出如下方法修改你忘记的Oracle中的system这些用户密码，很简单，只有几步。

第一步，打开的sqlplus.(系统菜单Oracle下面的或者是cmd里面你输入sqlplus都可以)

编程

第二步，在弹出的输入用户名界面输入 /as sysdba 然后使劲儿啪的一下敲下你的回车键！

SQL\*Plus: Release 11.2.0.1.0 Production on 星期四 4月 26 14:09:47 2018

Copyright (c) 1982, 2010, Oracle. All rights reserved.

请输入用户名: /as sysdba

连接到:  
Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production  
With the Partitioning, OLAP, Data Mining and Real Application Testing options

第三步，在SQL>的右边输入：conn sys/sys as sysdba;（我也不知道原理，为嘛这里可以连接）

PS：因为sys的也忘了=\_=|，所以不信的可以去sqlplus下测试应该是如下结果：

请输入用户名: sys  
输入口令:  
ERROR:  
ORA-01017: invalid username/password; logon denied

最后一步，直接使用alter命令修改你要修改的用户密码即可（下面语法中的红色部分1是需要修改的用户名，红色部分2是改成你的新密码）。

语法为：alter user **username** identified by **newpassword**;

深入探索

结构化查询语言加

网络安全课程

安全认证考试

SQL> alter user system identified by system;

用户已更改。

SQL> conn system/system  
已连接。  
SQL>

如果你需要修改的账户是锁定的，比如scott用户，那么只需要在最后一步这里使用如下命令解锁即可：

alter user scott account unlock;

溜了，有时间把自己学习Oracle的笔记贴出来（滥竽充数）。下回见！

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
文章标题：[Oracle 11g sys和system用户密码都忘记了的解决办法](https://mrxn.net/jswz/modified-Oracle-system-password.html)  
文章链接：<https://mrxn.net/jswz/modified-Oracle-system-password.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALm0lEQVR4Aeyci3LbvA6E/f3v/849XW2WhEhKVnISxzNVpsgCiwVIE2KdS6f/PR6PP1+1Px8fqf8INwg34pb8+HSWk2TM11h52YoTL6s5+eJiileWfMXoKic/vFCxTP7/YxrI3/r7z7ucQBvI3+k+rtrR5oEH2KIZe4LzwLReaoJjbY3BfSqXOphz0oF5mNdWXpYeQrBefjUwL32s5uWHv4LSx9pAQtz4uycwDQQ8fZjx2Vbr0/BMqzzs1xAngz0PPVb+mWUf4LrowwvBOTBGA46h36LkvoLQ+8HeX/WbBrIS3dzrTuBbBqInTgb9CVAsG1+KuNiYS5z8CsFrJAeOYcZRk/5nmBrhmU456Gsq/g77loF8x0buHj6Bbx2InqqY2/fP4KepM3+/AfrzZ/tKKxzsNeAYOh5pw1cE1x3taaUF1wA1vfnA9lXkFvzQp28dyA/t8Z9q+zMD+aeO8Htf7DSQXO8VHi0N81UGc2Bc1YJz41rRjrzis5zyslEDXid8RemPrOrkH+nEK78y5Y5spZ8GshLd3OtOoA0E/BTBc/zM9vJ0XKkBrx0tOAZCTQhsb7TAlPsMAWx9ag2Yy2sAx9GAYyBUQ2DrB8+xFf112kD++vefNziB/zL9r+DZ/tMP/ISstNGMOZhrYOZUlx5CxdVgXXOmAdcAVbbzge3p15qxCBJ/Fe8bkpN8E5wGAp4+zJg9g3OJg2AeOo5PSrQVwfrKyR9rFYuXgWtgRuVl0leDrg0v3ZFd0aQWem/ofvIVoedh708DqYW3//oTaAMBT+rsqYBzTWqFeSngGjCGryi9rHLPfOllVae4GnhNMK5y4Wqf+OA6MI5aMA+kZPtRkHSN+KTTBvLJut+Q/xNr3gN5szG3geiayYDdl3R1v8rLwJrkxMnAPMy/bVNeBl0Dez/9grDPw3Hf2jv14qpB7xf+SJu8MBpwfeIVwl4DjoEmV09ZCPmxNpAkb/zdE/gP2G4EGK9sJ9OMFuZaMBctOE7NFUxtRXjeB6wB42otcA72WLXgXF1ffjTyjyyaiuB+YEwOHAOP+4Y83uujDWScdLZZeeiTBCJZfqmXuogSr/BIE14IbDdZvgwcQ0fxsnENcaNFEz4x9H7hogHnEp9haj+LbSBnze/c606g/XAxS4KfAjCGr5iph4NjLTgHM6Y+CHtNeGHWDIo7MnCfMZ9a4ZgD1ygXGzUjD66BjqkBc4nPEKwF7veQx5t93H9lvdtAoF8X4HR7ubLA7g02/FnxZzTRgtcBWmtgWzuaMwRr4RjHepi1WRycS1xrw4E1yYWvCNaAMVrhfUPqSb2BPw1EU6pW9wj7iYLjqokPzqUX7GPxsOfAMRjTSwgzV3lA4WbAdou24OCT1pfBXisullKwZuSTXyG4BmZc6cNNA0nixt85gTaQr0w/WwY/BYmF6QfOjTEg2c6iCZm4YnLAdgtqDmau5qsPe+3YF+YfZIJroj3Dulb86BMHwX2B+8vex5t9tBsCfUqw9jPRYF7LGIcXjrnEQuWvGnhPqqsG5oHWCthuTyM+HDAPfDCPTQc9fiw+6nryIwGmeuVl0XwW20A+W3jrf+YE2kA0VVmWkT8a9CcCiLRh1QPt6QGaBmh89EmCc2MMhGoIbH3SQ5ikfFlimLXKVwNrUiMEc7BH5WS1Pj5Yq/xo0YQHa8ML20AiuvFbTuDLTe6BfPnofqawDQR8fbIM7OPwQl2tamAtdKx5+eCc/Jh6VRv5xBXBfWrd6IM1YEweHEPH5K5g3Yd86H3AvngZOIZjlE4GXdMGcmVDt+bnT+BwIJqcDPr0sh3oHBB6icD25rtKgnOwR60rW9WMHPTaMacespFXLF4Grhc3mvKykT+L4Xk/9ZTBrD0cyNmid+7nTqANRBOTnS2l/Mo+UwN+KqD/aCI9z/qA66JJzQqjgX1NeCE4l3pxssRCWGvAvPQx6VeWvBBcB8bolYu1gYS48XdPYBpIpgae4mp7cJyLHqyBPSZ/huCaqsm+KicfrAUU7uyopoqAw/e41IM1YAxf+8QHaxJXTF0QrE0snAZSG9z+60/gHsjrz/x0xfbPgMDXJ2pdH1niiuJllZMvLqZYljgo7siiCVYd7PeXXLTCcEFwjXKy8ELFMvnPTDrZM53y0snkjwbeDxilk4Fj4P59yOPNPto/ts6+oE8LCL0hsL0Bwh635MVPeiJiKYF9P3Cc/ArBGphx1IM1I684ewmCtTCj9EcGsx7YybNGcJf8CO73kI+DeBdoA8nURqwbHXNjDLQblDroHBB6Q2DTp89Glk/gPMzfRKamYkorJ3/Fg3snF5Q+NnKJYa5NTTDaxMJwQZj7tIFEdOPvnsD0VRZ4amDUZGNgDvaYlxDdCqNZIbhf6qJJLAwXBNdAx+SOEGYtdA72fvqAee1DFv6zCO4DxtSrZ+y+ITmVN8HDgWRi4GkCbcvJBYHtvaAJLjqpvyIHrwHG1KRHRbAGjNGusNbJP9PAvp/0sdSBNSOf/ArBNcD9fcjjzT4Ob8jP7fPufHYChwMBX6NcPWEagXOJlZMlrgjWKi9b5SpXfXAtUOnNVy/ZFgyfxF81YPvrFoy1VXpUTv6KB9ePOTAPqHSzUbORH58OB/KRv+HFJzANJNMLAu0Jyt6SS7xCcN0qFy59guGD4YUjB3N/2HPgGIzpsUKtIas52NcpL6uaZ770sWhh3ze8cBqIyNt+7wQOBwLzFDNpcA72WF9GtMGaiw+ufxYDkUy3tSWKA2y6rB0E80BTj7nEFYGtHxxja/jhgLUf4QbpuQXlU3jh4UCK/nZfeALtx++ajuzK2tLJrmijgfmJSW5E9R5t1CQG9wVCtf9ZAtg92U3w1wHn/rqHf+C5JsXZL7gmcfJX8b4hV0/qRbp7IC866KvLfGkg4GuZRXI9wTx0jCYIPZe65EaErh1zY23Ng+sqN/pjfWJwLfTfwRzVpkYIrpMvA8fQMX2UlyWGrvnSQNLoxu8/gen3IVeW0HRlo1Zc7CwXDfQnA+YnMjrh2G8VSydLTr5sjMXBfm1wHK0Q9pzqZMqNJl4WXv5o4H5gTD41wvuG6BTeyNpAxmmNcd0zeMKVu+qDa6HfiKwFPQd7P5rgaj1wzZhLDTgPfe1oo1lhNNDrYe2fadN71IQXtoFEdOPvnkAbCJxPvG5Tk5SFA9cmFiovky8Da8TFxMtgnxM3Glgz8uklHHNjLE0M9v1gH6sW9lxqzxBcE436xMC5xCtNG0hEN/7uCUw/OllNbdwieNJnWrAmtWfaaIIrbThwX5gx9UcIvSb9ok0Msya5aIPQtWB/zCWumH6wr5HmviE6hTeyeyCnw3h9sn1jOC6da1UxmnCJP4Pgawo8Lcs6QmD7yW2KxB1ZNLCvCV8xPWDWwsypFmY+fUaUfjRwfbTgGLj/GdDjzT7amzr0KcE1P68lk068QnDPmgNzqQfHMGM0tV4+dK3ilYE16SGMDva58BXBGjCqXlY18cGaxFdQvWL3e8iVE3uhpg0kE7qCR/sDPx0w/2giNbV/OHBdcuErgjWVk58aoeJq4qrVHKz7Vc3opxcc10Yz1p7F4H7A/R7yeLOPdkOyL+jTgr0fzYhgXZ4O4ahJDNZCv0XSy8C5aMWNlhxYCzMeacJfxaO1V/Uw7wNYSaff+VfRNJCavP3Xn8A9kNef+emKPzYQYPtGDoy5/me7OdOA+6Q+2s9galcI+/4rzchdWbvWRF+50f+xgYwL3fG1E/ixgeRpCML1J3CsAaZXA+xuIMzxWARdM+ZWMVifHKxjMA8dU5PXIoSeh/mLGml+bCDZ0I2fO4FpIJrSkR21jn6VBz8V0VRc6cXBXCNelnr5zwzcB4ypFaZWfrXwwvAw1yd3hKqXgWsBhU9tGsjTilvwoyfQBgI8/TsZrLmyI7iuHfvlqat8OLjeNzW1T/yjXHjhM23yQvC+YI/qc2RgrepjbSAhbvzdE7gH8rvnP63+PwAAAP//jsAy3QAAAAZJREFUAwChx/B0lIHBUwAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/modified-Oracle-system-password.html"),
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

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/modified-Oracle-system-password.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 