---
title: "金和OA OuterAppTIDSave.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-OuterAppTIDSave-sqli.html
asset_dir: assets/金和oa-outerapptidsave.aspx-sql注入漏洞
---

# 金和OA OuterAppTIDSave.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/19 08:31
* 488浏览
* [0评论](#comment)
* 18分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `OuterAppTIDSave.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OuterAppTIDSave.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **OuterAppTIDSave** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strOuterAppTID = this.Request.QueryString["OuterAppTID"].ToString();
  this.strSystemID = this.Request.QueryString["SystemID"].ToString();
  this.strOwnerAppTID = this.Request.QueryString["AppTID"].ToString();
  int num = new OuterOpenGroup().OuterAppTIDSave(this.strSystemID, this.strOuterAppTID, this.strOwnerAppTID);
  if (num > 0)
    this.Response.Write("true");
  else if (num == int.MinValue)
    this.Response.Write("error");
  else
    this.Response.Write("false");
}
```

参数`OuterAppTID`、`SystemID`和`AppTID`被带入`OuterAppTIDSave`方法

```
public int OuterAppTIDSave(string SystemID, string OuterAppTID, string OwnerAppTID)
{
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append(" select count(*) from JHOA_Approve_OuterProcess");
  stringBuilder.Append($" where System_ID='{SystemID}' ");
  stringBuilder.Append($" and ModuleTemplate_ID='{OwnerAppTID}'");
  object obj = this.dbo.ExecSQLReobject(stringBuilder.ToString());
  if ((obj == null ? -1 : Convert.ToInt32(obj)) > 0)
    return int.MinValue;
  return this.dbo.ExecSQLReInt($"update JHOA_Approve_OuterProcess set ModuleTemplate_ID='{OwnerAppTID}' where System_ID='{SystemID}' and Template_ID='{OuterAppTID}'");
}
```

至此，就非常明了了，三个参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/OuterAppTIDSave.aspx/?SystemID=SQLI_POC&OuterAppTID=1&AppTID=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA OuterAppTIDSave.aspx SQL注入漏洞](images/img-001-56fba3ce9443.webp)](https://image.mrxn.net/9fb0f99a3f94423d9fcd9530d598eb8c.webp)

成功延时 10 秒（执行两次）

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
文章标题：[金和OA OuterAppTIDSave.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-OuterAppTIDSave-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-OuterAppTIDSave-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKrUlEQVR4AeyZgXrbOAyD8+/93/kuEAOJtmTF7bLad9O+MqAAkFbFqOm2X4/H45/fjX9ef9zntdyANeFGeC3EK17LDYg/imw88ojPPufi93FGsyfjvs931xrIs3Z93eUE6kCe0358JWbfAPCAiJnvq1ren2shngOY2qBrNuRrMdKAsveX5VvgvmcxP6QOJJMrv+4EuoFAvENgjLOt+h0x82QN2jNcC42zd6SZy7j3S4PWD7ClINDdBtUoiuH1orXitSwAfW0R0guEB8aYrDXtBlKVlVxyAmsglxz78UM/OhCIq3n8uGMF+lrYcvqx4YCtljtDaED9RcU6HGv2CP0cIbQaiFy8Qt5PxkcH8smN/a29/shA9M5x+GC9FsL2XSbOYf8IIeqAkVxvg3sJbVSu8PodAuUDH6hW1Tsq+eHkjwzk8eFN/k3t1kBuNu1uIL6SR3hm/0B33Ud10HwQefZ5D+a8FpqDqIMx7n2qdVgboT1C69A/w9oIVTuLUU03kJFpcT93AnUg0E8fjrnZFvO7AqLHyJ991jMH21qINfS/zqretcrPBEQ/1wkhuFG9dMdINwfRA86h64R1IFqsuP4E1kCun8FmB798BX8H3dE9oF1Vaxnte8dZh+jntRCCcy8hBCfdAVsOYg3YUn8BgfajEKi8jdA4PU9hTfknYt0Qn+hNcDoQiHfEaK8QGjCSpxxQ3n3ZBMFBQ+uzdx58zT/rJQ2in/J9eD/vEKIH9JhrodenA8nFN8j/ii2cGgj0k8zvntlJ2TfyQOtr3whdC81vLvvNZYRWA2Sp3FLYchvDawEUb34WBAeBL2uB7HNehOcLhB/a59WTrl+nBlLdK/njJ7AG8seP+GsP+AVxhUZlvm4Z7YOogx5HftdlzD7o+0Bwrhn5rQmtQ9TB+MeCvEfhHiMd+r72Q9NGtSMOosY9hOuGjE7qQq7+xRBiWqO9QGjQ3nGapsM1+7V4iFrl+4DQgCq5R0aLQPlwhbYPaBxEnmshOPd4h9D7cz/n+z7mhXtNa/EK5Q6tFV4L1w3RKdwo1kBuNAxtpQ5EV0ch0gFxfcU79hpg6rfQ/YH6Y8kNITh7hNBz9meUV2EOog4wVZ8H5zmg1LkJxBoaWhNC8NqLA4KT7qgDMfHX4c2+4e7XXoipQfvgzHuG0D1loXUIDRpKV9hzhBA18jqOvOJHnhEnbw57Mr7TIfaWfc4htNzPuT1HOPKtG3J0WhfxayAXHfzRY7u/h/gaCY+KxENcVeh/tKnWAeFTzSzsn3kgegEzW/mwBQra6P4QPGBpg0Cpg4Y2uMcIofe7Tuga5Q5oNRD5uiE+nZtg/VD3BCEmBQ1He7VfuNfhXG2ug1YD21zPUGS/c9h6od1Y1UDo9otzzDhrGSF6QcOsO4fQvRZCz+33Id+6ITqFG8UayI2Goa3UD3UtvhIQVxCYlo2upQusCUeceAVQPmjtySh9HxB+oFqB0gMaWoSe2/fU2n6h1grlCuUOrc8ExHOzd92QfBqfy7/daToQTxxikrD9wNzr3oV5oTloPSBya0J5FRAaIPowgMN3vPrsw40yD9Ejc/ZBaICpKQJ1PyOjnwHNZy77pwPJxpX/zAnUX3shJuepCaHnvC0IDfpbA02zf4TQfBD5yGdOe3KYGyFEL2g4qptx1oR+hnIHtN6ALQWPPLD1AeVWlaLXy7ohr4O4C6yB3GUSr33UX3tH18zcy1sA4ppZExbh4AXCP5JVu4/sg+/V5p65n3KInnAeVbeP/Ix9DtE7867PnHNrwnVDdAo3iumHuvcJMXHAVPkwAjZYxTeJ3xnQ6l1ibYTQ+6Hn3EvoPhA+r9+hah0QtV5nhNCgYdb3OTQfRJ4964bk07hBvgZygyHkLdSB+Apn0bm1I7TPmH0zzpoQ+usLW27UV7UOCD/0aE9GCN87zs8d+UbaiHOtNaG5jHUgmVz5dSdQf+31FiDeNYCp4Qc3UHkboXEQud4JCnuEsNWkO6QfBUQdcGQpvHsJC/F8Ua4A6r61Vjzl+qW1ohLPBFoNRC6P4imXL+WOQjxfILzQ/jXjSXdfrhOuG9Idz7XEGsi15989vQ4E4nrp2jjs9loI53zyKiD80NB9Yc6pXmF/Roha6Y6sO7cG4Td/hBA+1x3hUb14iB7K9wGhAVUC6o/ROpCqruTSE6h/U/c7Adq0IPLRDiE0OP+B5WeM+pmzRwjtGYAtBaUrgPru0lpRDAcv0h0HlkJD61uI5ws0Do7zp7V8+TlCCL9yRzHtXtYN2R3I1cs6EDg3QU83I0Tt6JuBYy374ZzPNRD+vA9rGSF85iDWgKm3CJRbmI35uUd59s/yXF8HMiv4rLa6zU5gDWR2OhdodSC+Nmf3AHGNoX2oQ3CjHhAaUGU/U2gSKD8eoPWVvg/7M0Krhciz/pU8P891mYPoD4H2ZITQoH0vWXc/aL46kGxc+XUnUAcCMaXRViA0oMqertCkcgXQvcvtEcqjgLlP3ncBfQ/1dszqIWpHHggNGMkdB9Tv2aL3IDQ3QumOOpCRcXE/fwJrID9/5tMn1n9+95XJbnMZoV1NiNw1sF2bF+YeWisyB30t9JzqFLnWOXzNv68D1LoL+7Kw57wWAuXHV/aPcuh964aMTupCbjoQiAlCQ+9V7wTHnvP6HULr614Z39VLh76HeIf7ef0O7c/4rkY6tH1o/d2YDuS7Ta+o+788cw3kZpOs//w+2le+ts7tg3ZFYZvbK7R/hNId1qH1mmkQPtdlhNDgHPo5wtxnlkP0Vs1R5HoIf+acQ2jAY92Qx73+1F97vS1o04I+P3o3iHePjND3yPosh23tzCsNwq98H9qfYs9rDVEHY5RnH+qlgKjJOgQHDbPuXPUKr4XrhugUbhRrIDcahrYy/VCXQaFr5YB2DSFyeXJA8EClXS8Eur/JQs/JexS1cUqOvOKh7+9S6Q5zI4ToAQ3tg56zJnR/aD6I3Jpw3RCd1o2i+1DXlPaR97vXtM66cnEOrRUQ7wZAyxJAuSnQ/gPHdUIIvZh3L9IVmYbwQ4/2qWYf1jJmD0S/zNmbuX1uT8bsMQ/RH1i/9j6mf35erJ8h0KYEX8u9bU8fWr21jPZlzjkc10LTIHL3Oot+jhCih/J9QGjQbu/ek9fQ/Jl3Dk2HyK3lva/PEJ/KTXAN5CaD8DbqQPK1OZO7wQjf1Y9qznC578wP8SMB6GxA94tENvkZmTuTu0448otXjDRoe6oDGRkX9/Mn0A0E2rSgz89sEeZ1EPqol95FDusQfmg40sy5XgitBrClIFBuS1m8XiA41Tpe0hAg/NDjqMA9hdaVO7qB2LTwmhNYA7nm3A+f+tGBQFzb/DRfxRFnTWgdogf0v//L57Dfa6G5jOLfxcifuVHunl/Vsn/U46MDyQ9b+fEJzJSPDsQTz+iHQ3vnQ+TWhHCOkzcHRB2M0V4I3Wsh9Jx4BYQGDcXvI3+vzvcerSH6KN8HhAasf8t63OzPR2/Izb63/+R2uoH42h3hme8S2hWEyEd1EBpQ5dFzq3gyyT1cYs7rIwS6v5u4FkKDc+i6jPm5EH2y3g0kF6z850+gDgRiWnAOZ1vNE3ee/TMO+ufP/NaE+RnOYdvPfEZoHvVRZH2Wy6sYeaD1hchHvszVgWRy5dedwBrIdWc/fPK/AAAA///F2N+bAAAABklEQVQDAAXou542y9N0AAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-OuterAppTIDSave-sqli.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-OuterAppTIDSave-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 