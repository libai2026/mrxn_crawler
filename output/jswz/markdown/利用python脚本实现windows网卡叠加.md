---
title: "利用python脚本实现Windows网卡叠加"
source: https://mrxn.net/jswz/python-improve-windows-netcard.html
asset_dir: assets/利用python脚本实现windows网卡叠加
---

# 利用python脚本实现Windows网卡叠加

[Mrxn](https://mrxn.net/author/1)* 发表于2016/3/28 09:21
* 5709浏览
* [0评论](#comment)
* 1小时阅读

深入探索

安全工具开发

企业安全咨询

JSON处理工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

以前经常在网上找网卡叠加的小软件，找过很多个，有的用不来有的没效果，偶尔找到一个能用的批处理，于是根据这个脚本自己用python写了一个修改路由表的方案，这样一来下次就不用在网上找来找去了，简单实用（水平有限，还请在座各位多多指教）。

[[![利用python脚本实现Windows网卡叠加](images/img-001-182e51410f36.png "点击查看原图")](https://mrxn.net/content/uploadfile/201603/thum-9cfc1459128240.png)](https://mrxn.net/content/uploadfile/201603/9cfc1459128240.png)

废话不多说直接贴代码，送给需要的人

```
#coding:utf-8

#调用库
import sys,os,re

#函数
def pro_continue():
    input("按Enter键退出")

def nic_count(x):
    if   x<2:
         print("网络叠加需要两块或两块以上网卡")
         exit()
    elif x>4:
         print("该程序最多支持叠加四块网卡")
         exit()

def add_routetables2(i,g):
    net_1=[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,163,165,167,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199,201,203,205,207,209,211,213,215,217,219,221,223]
    net_2=[2,4,6,8,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128,130,132,134,136,138,140,142,144,146,148,150,152,154,156,158,160,162,164,166,168,170,174,176,178,180,182,184,186,188,190,194,196,198,200,202,204,206,208,210,212,214,216,218,220,222]
    print("开始<span class='wp_keywordlink_affiliate'><a href="http://www.slll.info/archives/tag/%e8%b4%9f%e8%bd%bd%e5%9d%87%e8%a1%a1" title="View all posts in 负载均衡" target="_blank">负载均衡</a></span>")
    os.system("route delete 0.0.0.0")
    os.system("route add 0.0.0.0 mask 0.0.0.0 " + str(g[0]) + " metric 30 if " + str(i[0]))
    a=0
    for x in net_1:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[0]) +" metric 25 if " + str(i[0]))
    for x in net_2:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[1]) +" metric 25 if " + str(i[1]))
    print("双网卡叠加成功")

def add_routetables3(i,g):
    net_1=[1,4,7,13,16,19,22,25,28,31,34,37,40,43,46,49,52,55,58,61,64,67,70,73,76,79,82,85,88,91,94,97,100,103,106,109,112,115,118,121,124,130,133,136,139,142,145,148,151,154,157,160,163,166,175,178,181,184,187,190,193,196,199,202,205,208,211,214,217,220,223]
    net_2=[2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50,53,56,59,62,65,68,71,74,77,80,83,86,89,92,95,98,101,104,107,110,113,116,119,122,125,128,131,134,137,140,143,146,149,152,155,158,161,164,167,170,173,176,179,182,185,188,191,194,197,200,203,206,209,212,215,218,221]
    net_3=[3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90,93,96,99,102,105,108,111,114,117,120,123,126,129,132,135,138,141,144,147,150,153,156,159,162,165,168,171,174,177,180,183,186,189,195,198,201,204,207,210,213,216,219,222]
    print("开始<span class='wp_keywordlink_affiliate'><a href="http://www.slll.info/archives/tag/%e8%b4%9f%e8%bd%bd%e5%9d%87%e8%a1%a1" title="View all posts in 负载均衡" target="_blank">负载均衡</a></span>")
    os.system("route delete 0.0.0.0")
    os.system("route add 0.0.0.0 mask 0.0.0.0 " + str(g[0]) + " metric 30 if " + str(i[0]))
    a=0
    for x in net_1:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[0]) +" metric 25 if " + str(i[0]))
    for x in net_2:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[1]) +" metric 25 if " + str(i[1]))
    for x in net_3:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[2]) +" metric 25 if " + str(i[2]))
    print("三网卡叠加成功")

def add_routetables4(i,g):
    net_1=[1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,65,69,73,77,81,85,89,93,97,101,105,109,113,117,121,125,129,133,137,141,145,149,153,157,161,165,173,177,181,185,189,193,197,201,205,209,213,217,221]
    net_2=[2,6,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94,98,102,106,110,114,118,122,126,130,134,138,142,146,150,154,158,162,166,170,174,178,182,186,190,194,198,202,206,210,214,218,222]
    net_3=[3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63,67,71,75,79,83,87,91,95,99,103,107,111,115,119,123,131,135,139,143,147,151,155,159,163,167,171,175,179,183,187,191,195,199,203,207,211,215,219,223]
    net_4=[4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,176,180,184,188,196,200,204,208,212,216,220]
    print("开始负载均衡")
    os.system("route delete 0.0.0.0")
    os.system("route add 0.0.0.0 mask 0.0.0.0 " + str(g[0]) + " metric 30 if " + str(i[0]))
    a=0
    for x in net_1:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[0]) +" metric 25 if " + str(i[0]))
    for x in net_2:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[1]) +" metric 25 if " + str(i[1]))
    for x in net_3:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[2]) +" metric 25 if " + str(i[2]))
    for x in net_4:
        os.system ("route add " + str(x) + ".0.0.0 mask 255.0.0.0 "+ str(g[3]) +" metric 25 if " + str(i[3]))
    print("四网卡叠加成功")

def check_ip(ip_str):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, ip_str):
        return True
    else:
        return False

#主程序
os.system("title 网卡叠加-www.slll.info&&color 18")
net_count=int(input("请输入网卡数量(MAX:4,Min:2): "))
nic_count(net_count)
arr_1=[]
arr_2=[]
for x in range(1,net_count+1):
    temp=input("请输入第"+str(x)+"块需要叠加的网卡索引号 (cmd下面利用该命令查看:route print | find \"...\"[第一列即索引号]): ")
    arr_1.append(temp)
    temp=input("请输入网卡(" +str(x)+") 的网关: ")
    while True:
        if check_ip(temp):
            arr_2.append(temp)
            break
        else:
            temp=input("输入错误,请重新输入网卡(" +str(x)+") 的网关: ")
if net_count==2:
    add_routetables2(arr_1,arr_2)
elif net_count==3:
    add_routetables3(arr_1,arr_2)
elif net_count==4:
    add_routetables4(arr_1,arr_2)
pro_continue()
```

注：此文并非博主原创，文章很有实用性，转载之，原文请移步：http://www.slll.info/archives/2153.html

* 标签：
* [#脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#windows](https://mrxn.net/tag/windows)

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
文章标题：[利用python脚本实现Windows网卡叠加](https://mrxn.net/jswz/python-improve-windows-netcard.html)  
文章链接：<https://mrxn.net/jswz/python-improve-windows-netcard.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/python-improve-windows-netcard.html"),
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

安全研究工具

  

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
text: encodeURI("https://mrxn.net/jswz/python-improve-windows-netcard.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 