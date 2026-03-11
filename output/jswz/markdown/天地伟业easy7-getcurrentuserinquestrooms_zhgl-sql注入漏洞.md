---
title: "天地伟业Easy7 getCurrentUserInquestRooms_ZHGL SQL注入漏洞"
source: https://mrxn.net/jswz/easy7-inquestRoom-getCurrentUserInquestRooms_ZHGL-sqli.html
asset_dir: assets/天地伟业easy7-getcurrentuserinquestrooms_zhgl-sql注入漏洞
---

# 天地伟业Easy7 getCurrentUserInquestRooms\_ZHGL SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/4 08:29
* 299浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

软件

数据库

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

SQL注入检测工具

该系统的 /Easy7/rest/inquestRoom/getCurrentUserInquestRooms\_ZHGL 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意请求执行任意SQL语句，可能导致敏感信息泄露或数据库被篡改。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

代码安全审计

再来看本次的漏洞接口 /Easy7/rest/inquestRoom/getCurrentUserInquestRooms\_ZHGL 对应的 `getCurrentUserInquestRooms_ZHGL()` 方法实现逻辑

```
@Controller
@RequestMapping({"/inquestRoom"})
public class CLS_REST_InquestRoom {
    private static final Logger log = LoggerFactory.getLogger(CLS_REST_InquestRoom.class);
    @Resource(
        name = "boInquestRoom"
    )
    private CLS_BO_InquestRoom boInquestRoom;
    @RequestMapping({"/getCurrentUserInquestRooms_ZHGL"})
    public void getCurrentUserInquestRooms_ZHGL(HttpServletRequest request, HttpServletResponse response, String currentCourtFjm) throws Exception {
        response.getWriter().print(JSONObject.fromObject(this.boInquestRoom.getCurrentUserInquestRooms_ZHGL(currentCourtFjm)));
    }
```

深入探索

漏洞预警服务

企业安全咨询

VPN服务

参数`currentCourtFjm`被直接带入`boInquestRoom.getCurrentUserInquestRooms_ZHGL`方法

```
public CLS_VO_Result getCurrentUserInquestRooms_ZHGL(String currentCourtFjm) {
        CLS_VO_Result result = new CLS_VO_Result();
        result.setContent(this.daoInquestRoom.getCurrentUserInquestRooms_ZHGL(currentCourtFjm));
        result.setRet(0);
        return result;
    }
```

继续跟进 `daoInquestRoom.getCurrentUserInquestRooms_ZHGL(currentCourtFjm)`方法

[![天地伟业Easy7 getCurrentUserInquestRooms_ZHGL SQL注入漏洞](images/img-001-ee9ea8924d3f.webp)](https://image.mrxn.net/2331eb7d71864907a4a4010f67ffa574.webp)

最终在dao层，参数`currentCourtFjm`是未经任何过滤或校验就被直接拼接进`"AND ROOM.S_SX_CODE = '" + currentCourtFjm + "'"`SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /Easy7/rest/inquestRoom/getCurrentUserInquestRooms_ZHGL HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

currentCourtFjm=SQLI_POC
```

[![天地伟业Easy7 getCurrentUserInquestRooms_ZHGL SQL注入漏洞](images/img-002-5ee67d00f7cf.webp)](https://image.mrxn.net/de52a0e915c74c4bb1047e76d5576169.webp)

成功延时5秒

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

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
文章标题：[天地伟业Easy7 getCurrentUserInquestRooms\_ZHGL SQL注入漏洞](https://mrxn.net/jswz/easy7-inquestRoom-getCurrentUserInquestRooms_ZHGL-sqli.html)  
文章链接：<https://mrxn.net/jswz/easy7-inquestRoom-getCurrentUserInquestRooms_ZHGL-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALbUlEQVR4Aeyb4VojuQ5EOfv+77wXpXIaW91OB9hL8qP5EOUqlWRjdZYhs/PPx8fHvz+Jf+8fq9p7euvd+Xfrnq0f+/Ya+QrH2kfrXq9XXf4TrIF81l2f73ID20A+p/vxTKwObu0qD3wAW/rMvxnvC2Cqv8sTrHp2HdILgjbRJ3ZdDqmDoHpH+5zhWLcNZBSv9etuYDcQyNRhxtURnb55OaRe3rH7zXe9c32i+ULInrV+FEe15Ye5vvvkYtU8E5C+MONR7W4gR6ZL+7sb+PVAYJ46hPstQDgEVzo8zvc6uU/rEUJ6QtAa0ZrO4divr2Pv0/Pf4b8eyHc2u7znN/CfDaQ/JZ17FJifPn0izHnrOkJ8sEZ7ivaA1MhFiN795js+6+t1j/h/NpBHm1y5529gNxCn3vGsJeTpuvk+v8DMP6XbZ+8L8UHwZhq+6Ic5r36ElsNco26NvCMc1+mDx3l9ovt1ND/ibiBj8lr//Q1sA4FMHR7j6ohO3/yKQ/rrE8/8PW8dpB+gtKE1wPRbPhxz/VuD+wJm/13eAI7zEB0e49boc7EN5HN9fb7BDfzjU/Fd9OzWrbg65CnpfvOieZj9EK5P1F+odoblrYD0rHUFhFsPx7y8FTDnravcT+N6hXiLb4LLgcDx9OFY9/uB47xPzMoHqYOgfph5r4fk4Qu7p/cyL0Jq5fpF9RWufJC+MKN9YNaBj+VAPq6Pl9zAciB96pBprvR+eoj/TLdfx1WdPvPyQrWOMJ8FwqumQn+tK+RiaWN0Xd5xrBnXcLx/1S8HUskr/v4G/oFMC2b0KBC9c4ju5GHm+s2vuPoTeLNA9rmRzy8QDuz+xvMzPX32s0BqJ9MngegQ/JRun3DMIToEb+bhCzyvX6+Q4eLeYbkN5NmnR5+4+ibMw/x0wMyth1mHmeuzr3xEmGv0iqN3XJuH1Mv1QPTO9YnmO/b8ipe+DaQ3ufhrbmD7Tb1vX9MawzzkaYEZzXe0B8Qv774V1y9C+qz8RzrMNfY68j7SrBNXXsh+cIy9Dr581yuk386L+W4gTh8ytX4+8+pyER7XQfJnfvtD/HLrjlBPR70w9zrzWSfCXA/hENQn2l8uqh/hbiBHpkv7uxtYDsRpQqbvkWDm6iuE2d/7yq2Hx359IsQPKN3+7gP23L2Am2cruC/gWL+nt99zID77ifrElQ5zvf7C5UAqecXf38BuIJDpeZQ+ZbkI8UOw6/aB5OUrn/kVQvpA0D4jrmoP9UG0xyDdlpC9bmT4AtFhRi0w6xDe95EX7gZiswtfcwPbQCDT8xgw85peBUSHoP7KVcCsmxcheQhWzRj6OupR71y90Bxkj9IqYOYr30qH1JsXq/cYMPvM6YfkIWi+cBtIkStefwPbu739KE5THTJNdbHn5T2/0iF9IbiqW9WrF0J6QNBeK4T4qrYCZl5aRa+H+CBovrwVKw7xl6dCH0QHrr8x/Hizj+29LKclrs4JmeYqrw6zz75wrK/q1FcI6QesLDsdmH4P8WwizHmYuT4bQ/IrXd9ZvnzXz5C6hTeKbSCQKfezQXSnK3afumj+jH/Xpx9yLnlh36u0Cth7S9cPyUNQvTxjQPIQNKcfZt08HOvmR9wGMorX+nU3sP0pyyl7FJinCuEQ1NcRkrcfhHefHH6Xd59CSK9aV7iHCMnLO1ZNBcRX64ru6xziVwcOf0ZBfNVzFdcrxFt8E9wNBM6nWNP1/LWugLkOjrl1YtVWdA6pV4dwCFZNBYTD1/91Al8aYIslVp8KDbWukHes3DOxqlMHbq8k+MLdQDRf+Job2H4PcXsnL4ev6cF63es6t98KYe7dfb0fxD/6YK9Vvtd2DnMdhEOw+6vnGBAfzKgHjnXzI16vkPE23mC9/SnLs0CmKRd9Sjqah7kOZm4dzLr15ldcXdR/hN0D2VMvhENQP4TrEyG6PhFmXX9H/epyUb3weoV4K2+C288QmKcNM/e8cKybP8N6CsaA9IOgubM+5iF1gNKGwO1PMfaE8M1wX5i/0w1g9q98W8F9AXPdXb6dBZDu/o4euN7t/Xizj+s/We8+kPFleXTWs7w1+oDtpQqY3jR9W+K+AG6eO72tAemG1hdu4n1RWgVwq6/1UcCch5lbc297Cs/6Yb/P9Qo5vd6/NWwDcaqQqfVjQHSYsftW3P49D+mnDuHd3znEB3u0V0eIVx2O+WqvXrfyQfpC0DoRolsP4cD1Q/3jzT62V4jncmpn2P3yjvbputx8R/Mi5CnSpy4f0VxHPSvdPGSv7pPrk4tdl6/QuhF3AxmT1/rvb2B76wTmpwLCIejRYObqPgVwnNcHcx7CYUb99hW7Li+E9OjeylVA8hDUB+EQ7HrVVkDyECytQn+tKzovbQxIPQTH3PUKGW/jDdbbQFZTVYdMU/7Ts5/Vm4fsB8G+H+x1a7tXbl6EfQ+9I+oXx9zRGua+MHP7iGOPbSCjeK1fdwPbQCBThKDTg3CPCI+5dd0P1iXTfVG/vpoXvzLnKzjeC6JD0N4dVztA6p7NQ/z2tw6iQ1C9cBtIkStefwPb2+8epU9TfobWQ6YOQevMizDnz3y9Tv4IIXvocQ8R5rw+mHWYub6O9lXvXF00P+L1CvF23gS3gTilfi7I0wEzdp981Ucd0kf/CuHYZ5+jOkiNHlEvJC//br777XOGMO+rH/b6NhBNF772BnYDgXlqPhUdYfb1b0M/PPb1us57H0i/I12t94C5pufl1otwXNfzEF/v0znEZ715iA5c7/Z+vNnH9l6W53J68DU12K+7z3qYvfrMrxAe19lHhPjlhfaG5OQizDqEwzGu6tRrzwo5zH26Ln+Eu/9kPTJfuf//DWwDgXm6NfkxPIqavKN5Eea+3Q/J6zcP0eUiRO/+ysOcg/DKVRzVlG70fOf6VnjmP8tX320gRa54/Q1sA3F6okeDPGXqEA7B7ltx683LRXWx65D9Vjp8/XOE3sMaSA8I6hMhevf3vFzULxfhcT99I24DGcVr/bob2AYCmSYEPVKfvryjftG8XFSHeZ+el3eE47ruKw7xQrC0Cs8gllYhh/jllXsUED8EV95n+m0DWTW59L+9gdN3ez0OZPoQVBedPiQPwa7rFyE+OEZ9HSH+UYe9VnnPIMKxD45160SYfepi7TkGxA8zjh7X1yvEm3gT3A0Ejqfo9EWIr38f5rsuh8d1q3r1R+geol6Y9+y6XLS+I8x9en7F7bvCsW43kDF5rf/+BnbvZXkEpykX4bmnpNd3bj91eNwXkoc12hNmj3rHs73huT7w2AdzHmY+nut6hYy38Qbr7U9ZPi3i6mzmRci0V351iM860bwc4lMXzXeuPqIe0ZxchOy1yqt3tL5j98n1yTuaL7xeIXULbxTbzxDI0wLPod+D04bUqcPM1TvC7LOfqB9mX9cBpR0Ct39BBUEN7gGzbh6iw4zP1tmnI8z9xvz1Chlv4w3W20Cc+hk+e2b7QJ6Gzld9IH7zEG69uqheqLbC8lRAep75Vnn4Xf2qb+nbQIpc8fob2A0EMn2Y8dmjQur01xNZAdFrXQHh+mDm6iLMeQiHPVpT+1TIId7Oy1OhLpZWIe9YuQp1SH+YseerZhW7gVh84Wtu4NcDgTwNfeIQHYLmYebPftvWi9bJRzTXcfSMa32Qs634WFNrmP3WVW6MrsuP8NcDOWp6aT+/gV8PxCfBI0CeGnXRvBxm3yqvLsJcB+HwhX0Pa8+w18mtg+whF7tP/Qwh/eALfz2Qs02v/PduYDcQp93xe22fd0OeDisgvO8Ps65/9KmJ5uSQHvKO8Djf+/X6ziH9rINwfeoj7gai+cLX3MA2EMj04DGujgmpc9o/9VkP6QdB9d4Xkof9/5el11oRUmMeZr7S4din/wzdXx+kH3zhNhBNF772Bq6BvPb+d7v/DwAA//9ReZhKAAAABklEQVQDAO41ua0/ArC6AAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-inquestRoom-getCurrentUserInquestRooms\_ZHGL-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/easy7-inquestRoom-getCurrentUserInquestRooms\_ZHGL-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 