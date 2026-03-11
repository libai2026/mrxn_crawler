---
title: "用友NC cartabletimeline/doList SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-cartabletimeline-doList-sqli.html
asset_dir: assets/用友nc-cartabletimelinedolist-sql注入漏洞
---

# 用友NC cartabletimeline/doList SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/3 09:02
* 697浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

计算机安全

鉴权

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统的 cartabletimeline/doList 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意的 SQL 语句注入请求参数，绕过身份验证或获取数据库敏感信息，进而可能导致任意数据读取、篡改甚至系统权限提升，影响系统的安全性和数据完整性。

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

深入探索

安全工具开发

VPN服务

文本剥离工具

直接看`VsmAction` 类的`doList`方法的实现逻辑吧

```
@Servlet(
    path = "/cartabletimeline"
)
public class VsmAction extends BaseAction {
    @Action
    public void doList() {
        HttpServletRequest request = this.request;
        String pks = request.getParameter("mtr");
        StringBuilder sd = new StringBuilder();
        sd.append("<?xml version='1.0' encoding='UTF-8' ?>");
        ICarTalbeService carTalbeService = (ICarTalbeService)NCLocator.getInstance().lookup(ICarTalbeService.class);
        StringBuffer sb = new StringBuffer();
        sb.append("(").append(pks).append(")");
        ApplyVO[] applyVOs = null;
        PersonVO[] personVOS = null;
        Map<String, PersonVO> personMap = new HashMap();

        try {
            applyVOs = carTalbeService.getVehicleApplyInfo((String)null, sb.toString(), (PaginationInfo)null);
            sd.append("<data>");
```

深入探索

服务器安全服务

企业安全咨询

防火墙软件

跟进`ICarTalbeService`的`getVehicleApplyInfo`方法

```
public ApplyVO[] getgetUserVehicleApplyInfo(String pkUser, String whereSql, PaginationInfo pageInfo) throws LfwBusinessException {
    ApplyVO applyVOs = new ApplyVO();
    StringBuilder sb = new StringBuilder();
    if (!StringUtils.isBlank(whereSql)) {
        sb.append(" ( billstatus = 5 or billstatus = 6 ) and dispatchvehicle in  ").append(whereSql);
    }

    return (ApplyVO[])CRUDHelper.getCRUDService().queryVOs(applyVOs, pageInfo, sb.toString(), (Map)null, (String)null);
}
```

参数**mtr**这里被拼接进SQL语句中，整个过程没有对参数**mtr**进行校验或过滤，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，朴实无华的！

# 漏洞复现

> 需注意NC 大多数为Oracle 少数MSSQL

```
POST /portal/pt/cartabletimeline/doList HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

pageId=login&meapk=SQLI_POC
```

[![用友NC cartabletimeline/doList SQL注入漏洞](images/img-001-22adcf601f59.webp)](https://image.mrxn.net/2e7bb6fe2cce4b2ca98e44430c3e87e4.webp)

成功延时 3 秒

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
文章标题：[用友NC cartabletimeline/doList SQL注入漏洞](https://mrxn.net/jswz/yonyou-cartabletimeline-doList-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-cartabletimeline-doList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALV0lEQVR4AeycgXbbuA5Efff//3lf4MlVRIi0lWRb+5ynnCLDGQxAmpA3SdvtP7fb7d+fxL+fH2drP+0bWLcJn4uzur49frbYwNwmtEXPyzu2sgPVb0L+E6yBfNRdv97lBraBfEz3dib6wa1Z6T0P3IBtr14nh/gg2PvoUy9U6wjp0fWqqei6vHIVMNZDOAT1d6zaM7Gv2wayF6/1627gMBDI1GHEs0f0idAP5/pAfNZ3hOTta14+Qz0ipAeMOKstDeKzvrSKzkt7FJA+MOKs5jCQmenS/t4N/HogkKn3pwbm+sq3eskw9oFwCO7rIBoEzUF437tz/eqi+grP+lb1e/3XA9k3u9a/v4FfD6Q/HTA+jTDnEN2XYB84p1sH8QNKB7S3ic6B+3d+5mHkK7330fcb/PVAfrP5VXu8gcNAnHrHY+mowO6p+kjByD+k+y/73snkk3kY69Utkc9QjwjpBcGuyzvC6DcPc918x9kZS+u+4oeBlHjF625gGwhk6vAY+1Eh/pp4hflaV8hFmPtXeYjffEdIHuipA6/zVAD3rxm1rtBY64rOYe7XB8nLRYgOj1F/4TaQIle8/gb+qSfiJ+HRrZWLkKei53/KIf3sL9qvUG2FMPaA8KqtsK7WFSuuDo/rq8d343qHeLtvgoeBQKbu+SAcRux5eUeY1+mD5Fdc3SdNDqmDI+pZob3E7oP0VIdwCJ6ts16E1MtFiA7cDgO5XR8vvYFtIJApraavLsLoh5H/168Knvf3bKu9zUN66YNwCOozLxe7Ln+G1kP2geC+bhvIXrzWr7uBw0AgU4Pgs6nC6Hv2UiB+CPb+cvtAfLfbTekp2gNSK++FkLz6WR+kDoKrekgegvoe4WEgj8xX7s/fwD+Q6a2ejn4EfR31wdiv++Qr/3d1+xX2WvkKq6bCPOTsnZenQl0srUIOqYdg5SrMi6VVdF7a9Q7xVt4Evz0QyPRhxGevB+LvvnoqKtQhvtIq1Gu9D4gPjqjPWhHiXeW7T34We1/Ifmfry/ftgVTRFX/uBpYDcdowTlndI8lh9Jl/hvC4DpKHEd13318N4pXr6Vy9Y/dB+kHQPISv6vWJ+mCsg3Dg+kn99mYf2zsEMiWnCeGed6X3vD51seuddx9kf30d4Zi3hwjxdA6jbu/uk5sXIfVyfRBdLsKoWyfqK9wGUuSK19/ANpDZtGbHW/lgfAqshe/p1rkPpB5G1LdHiMdace85rD8EGOs+pPsv6yH5u7j7BNEhuEvdl3BOd5/CbSD3Dtenl9/AciA1rX14UphP3XxHe0DqIKgu9jp47JvVqUFq7Qnh5tVXqA9S133muy6HeZ15EeKDL1wOxKIL/+4NbAOBTMntYeTqPh0ijD4Yea+Tw9wHow7hELR+hjD3eNZZzUyD9FnVQfLWdp9c1Adjnfoet4HsxWv9uhvYBtKnKYdMFea4OjrEv8qrQ3wQdN9nCPHDF/YaSK7v1bl16t9FmO8D0e0vPuq/DeSR6cr9vRvYBgKZJozoVM+iR9cP8376OkL8Kx3m+b0f4ulnkHe0FlInP4v20y8XYeyrrn+P20D24rV+3Q1sf3PRIzg9EcbpQjgErYM5t48Io0/dPiLMfd0vL7S2Y+Uq1CG9YcTyVHRf5+XZh3k14P53hyH9zcPI1a0rvN4h3sqb4GEgkClCsKZW4XlrXSEXS6uQi5A+EFQvb8WKq0PqIKguQnRA6fD/wAPTJ7b2r9gKPxelzeIz/RSs1SgX1UX4Ot9hIJoufM0NbH/rZLU9fE0Pvtb64UuDr3+hYfU0rHT7mRe7DtlPfY+QHAT3uVr3nqU9CkgfCPZ6iA5ztDc8zusrvN4hdQtvFIfvsjxbfxrkHfU/Q+v0wfjUqJ9F+82w99AD2XOVV4e5D6JDUL/oPh1XefU9Xu+Q/W28wXobiFP1TDB/CmCuWydCfGf7WifCvN68CPEBShsCp767gvgs7Gfu+iqvD8Z+z3T7FW4DsejC197ANZDX3v9h9+3bXji+zQ7uD6HeVhUfyx/9qtp99CaQc+iBcAh2v77CR7lZXn/lKuRiafuA8Qzm9IvPdEifme96h3iLb4LbQJxWR88JmSqMaH6FEL95GLn6Cr97HmBrBdy/qCvYC0YdwiGov6P1XZdD6mHEnpeL8OXfBmLywtfewPaDIWRKHgfCfSo66num6+sI6a8Oj7m+jn3/4npqXQFjb/MQvTwVXe8c4lfvWD0q1Gv9KGa+6x3irbwJbgNxkpCnQN7PCcl3fcV7H/kztB9kPwiqzxDisXf3wOP8yq++6mte7D7IvuY7QvLA9b8j3N7sY3uHQKbk+SAcguqr6cPog5FbD9HhMfZ95B3tu0dI771Wa2trvQ+I3/wK9zW1htTVugLCIVjaPiA6jLj3bAPZi9f6dTewDaQ/FasjQaa7yqvbTw7WqXwPYayHke+79b33udl65Yf1HtVnVVe5fZz1Vc02kCJXvP4Gvj2Q1bTVIU8VBH2J5uXiSjffEdLXOggHunXjejfhyQIYfsLvdpjnV/tA/OYf4bcH0g938f/2Bk4PBDJlCPZjwDm9Px29j3lIP3lH67peHFKrR4ToEFQXYa6b/ynWmSpW9ZB9gevnkNubfRz+PAQyrdU5a9LfCftA+kJQvSPM8zDqEA5HXPXs59YH6fEsr18fpE4dRq4uQvIwovnC0//JKvMVf/4Gtt/tderPEDJdjwbhMKJ5sfdV76hPHdJ3xfXP0JpnaC2Me1lnXi6qi+q/wesd8pvb+wO1h4HA/Clx72dPg3lIH7n1EL3z7jMvmhfVxTMI2RuCvZcc5nn3gOQ7t15dhNGvb4aHgdjkwtfcwDYQGKcIcw6j7pTPHl8/jH0gHIL67AvR5TOEeGBEvb2nOsQv7z54nNcP8cl7v65D/PCF20AsvvC1N7ANpE9vdSx9kKmufOoQH4xoXrSvCPHL9cFcN79Ha0VI7d5Ta/O1roDR9yxfNRXdV9o+4HHf8m4DKXLF629gGwhkek5Z7EeE+LquHx7n9XVc9VPXL4fjPs885sVHvcwVwnGv0ntAfBDseTkkD0H1wm0gRa54/Q0cBgKZGgQ9ok+VqA7xQdB8R/0ixA9B9Y6QPAR7fs9h9HgGPTDm1UVIvtedzevrCOmrbn9RvfAwkBKveN0NbL/b248wm155INPueTkkD3OsHhX6xdIqIHW1rjAvlrYPiB/Yy/c1cP+TPwjexd0neKzD47yt4Jyv+yF1vrbC6x3iLb0JLn+3d3W+mmJFz8M4bfPl3QfEZx7CIagXwmFE6/TNUI+oRw7p2XXz6h17Xi52v3yVV4ecB7j+xPD2Zh/b1xD4mhI8X/s6+lOgLkJ6yfVDdLkI0btf3hHiB3pq+yc2gPvXEvcQDwWfAsT/SQ8AyUOwG2Cu64N1/voa4i29CW4D8al5hv3ckGlbByPvOiRvHwiHoPpZtH/hsxrIHjCiddWjQg6jr3IV5ldYnoqf5LeBrIov/e/ewGEgMD4VEP7sWBBfPRkVz/zmy/souk8O2Q+OqEe0/4qri92vDtnLvNjzEB8Ee14u2qfwMBBNF77mBn49kJrqPuDxU7H31hpGf78GGPNVczbsBWMPCO99ILp1YvepQ/w9L9cnqncO6QNcP4fc3uzj1+8Q+JousHx5Ph3A/WcCjeryFULqIKgPwuELzYl9DzmkZuVT/y7C2LfXwzr/64H0zS7+uxs4DMSnp+Nqm7M+GJ8K+B5f7dP14pDeMGLlKvprgdEH4eWtgHDr4DGvmn30OnOQPvLCw0AsvvA1N7ANBDIteIxnjwnp88wPc189LRXWw+iDkZcPolVdRWkVta6A5CFYuUcBow/Cq1eFtbWukK+wPBU9D+kLXN9l3d7sY3uHvNm5/m+P8z8AAAD//54emGsAAAAGSURBVAMAO1FW1JFpvFYAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-cartabletimeline-doList-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-cartabletimeline-doList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 