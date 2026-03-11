---
title: "金和OA AjaxForSetDecompose.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForSetDecompose-sqli.html
asset_dir: assets/金和oa-ajaxforsetdecompose.ashx-sql注入漏洞
---

# 金和OA AjaxForSetDecompose.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/26 13:05
* 244浏览
* [0评论](#comment)
* 1小时阅读

深入探索

恶意软件分析工具

编程语言教程

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForSetDecompose.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForSetDecompose.ashx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForSetDecompose** 的处理逻辑

```
context.Response.ContentType = "text/plain";
string str1 = "设置成功！";
string str2 = context.Request["strType"];
if (string.op_Equality(str2, "add"))
{
  string str3 = context.Request["strBudgetManageInfo"];
  string strDeptCollect = context.Request["strDeptCollect"];
  string strUserIdAndDeptId = context.Request["strUserIdAndDeptId"];
  string empty1 = string.Empty;
  if (!string.IsNullOrEmpty(strDeptCollect))
    empty1 = strDeptCollect.Split(new char[1]{ '@' })[0].Split(new char[1]
    {
      '|'
    })[0];
  if (string.op_Equality(context.Request["strCollectState"], "old"))
  {
    string empty2 = string.Empty;
    DataTable budgetCollectManage = this.budgetDecomposeDao.GetBudgetCollectManage(empty1);
    string str4 = budgetCollectManage == null || ((InternalDataCollectionBase) budgetCollectManage.Rows).Count <= 0 ? "没进行过公司汇总流程" : budgetCollectManage.Rows[0]["BudgetTime"].ToString();
    if (string.op_Equality(str4, "0"))
      str1 = empty1 + "年度全部期间的汇总已经提交，不能进行设置的修改操作！";
    else if (string.op_Equality(str4, "没进行过公司汇总流程"))
    {
      string ToUsersList1 = string.Empty;
      string str5 = string.Empty;
      string strContent1 = $"您好，{empty1}年的预算汇总做了重新设置，您之前提交的汇总已经被撤销，请知晓！";
      DataTable dataTable1 = this.db.ExecSQLReDataTable("select * from BudgetUserAndDept where BudgetType = 1");
      if (dataTable1 != null && ((InternalDataCollectionBase) dataTable1.Rows).Count > 0)
      {
        for (int index = 0; index < ((InternalDataCollectionBase) dataTable1.Rows).Count; ++index)
          str5 = index != 0 ? $"{str5},{dataTable1.Rows[index]["DeptId"].ToString()}" : dataTable1.Rows[index]["DeptId"].ToString();
        ((MarshalByValueComponent) dataTable1).Dispose();
      }
      DataTable dataTable2 = this.db.ExecSQLReDataTable($"select UserID from BudgetUserAndDept where BudgetType = 1 \r\n                                    union \r\n                                    select distinct UserID from RelationshipUsers where DeptLeader = 1 and DeptID in ({str5})");
      if (dataTable2 != null && ((InternalDataCollectionBase) dataTable2.Rows).Count > 0)
      {
        for (int index = 0; index < ((InternalDataCollectionBase) dataTable2.Rows).Count; ++index)
          ToUsersList1 = index != 0 ? $"{ToUsersList1},{dataTable2.Rows[index]["UserID"].ToString()}" : dataTable2.Rows[index]["UserID"].ToString();
        ((MarshalByValueComponent) dataTable2).Dispose();
      }
      this.Callt.InsertCall(strContent1, ToUsersList1, context.Session["UserCode"].ToString(), context.Session["DeptID"].ToString(), "", "", "", "", "", "");
      this.db.ExecSQLReInt("delete CollectList where CollectYear = " + empty1);
      if (this.budgetDecomposeDao.AddBudgetManageInfo((object[]) str3.Split(new char[1]
      {
        '|'
      }), strUserIdAndDeptId) == 0)
      {
        str1 = "设置失败！";
      }
      else
      {
        this.budgetDecomposeDao.AddDeptCollect(strDeptCollect);
        string ToUsersList2 = string.Empty;
        string strContent2 = $"<a href='../JHSoft.Web.CostControl/Collect/DepartmentBudgetCollect.aspx?strYear={empty1}'>您好，{empty1}年的预算汇总已经设置，请抓紧时间处理，逾期将不能提交！</a>具体设置：";
        string str6 = strDeptCollect;
        char[] chArray1 = new char[1]{ '@' };
        foreach (string str7 in str6.Split(chArray1))
        {
          char[] chArray2 = new char[1]{ '|' };
          string[] strArray = str7.Split(chArray2);
          if (string.op_Equality(strArray[5], "0"))
            strContent2 = $"{strContent2}<br />第{strArray[1]}区间起始时间：{strArray[2]} 至 {strArray[3]}";
        }
        DataTable dataTable3 = this.db.ExecSQLReDataTable("select * from BudgetUserAndDept where BudgetType = 1");
        if (dataTable3 != null && ((InternalDataCollectionBase) dataTable3.Rows).Count > 0)
        {
          for (int index = 0; index < ((InternalDataCollectionBase) dataTable3.Rows).Count; ++index)
            str5 = index != 0 ? $"{str5},{dataTable3.Rows[index]["DeptId"].ToString()}" : dataTable3.Rows[index]["DeptId"].ToString();
          ((MarshalByValueComponent) dataTable3).Dispose();
        }
        DataTable dataTable4 = this.db.ExecSQLReDataTable($"select UserID from BudgetUserAndDept where BudgetType = 1 \r\n                                    union \r\n                                    select distinct UserID from RelationshipUsers where DeptLeader = 1 and DeptID in ({str5})");
        if (dataTable4 != null && ((InternalDataCollectionBase) dataTable4.Rows).Count > 0)
        {
          for (int index = 0; index < ((InternalDataCollectionBase) dataTable4.Rows).Count; ++index)
            ToUsersList2 = index != 0 ? $"{ToUsersList2},{dataTable4.Rows[index]["UserID"].ToString()}" : dataTable4.Rows[index]["UserID"].ToString();
          ((MarshalByValueComponent) dataTable4).Dispose();
        }
        this.Callt.InsertCall(strContent2, ToUsersList2, context.Session["UserCode"].ToString(), context.Session["DeptID"].ToString(), "", "", "", "", "", "");
      }
    }
    else
      this.budgetDecomposeDao.AddDeptCollect(strDeptCollect);
  }
  else if (this.budgetDecomposeDao.AddBudgetManageInfo((object[]) str3.Split(new char[1]
  {
    '|'
  }), strUserIdAndDeptId) == 0)
    str1 = "设置失败！";
else if (string.op_Equality(str2, "getDetpCollect"))
  str1 = this.SetDepartmentBudgetCollect(context.Request["strYear"]);
else if (string.op_Equality(str2, "getAppCollect"))
{
  string str10 = context.Request["strYear"];
  DataTable dataTable = new DataTable();
  if (!string.IsNullOrEmpty(str10))
    dataTable = this.db.ExecSQLReDataTable($"select * from BudgetCollectManage where BudgetYear = {str10} and CollectState in (0,1) order by BudgetTime");
  str1 = ((InternalDataCollectionBase) dataTable.Rows).Count <= 0 ? "0" : "1";
}
context.Response.Write(str1);
```

当 `strType=getDetpCollect` 时，**strYear** 被带入`SetDepartmentBudgetCollect`方法

```
protected string SetDepartmentBudgetCollect(string strYear)
{
  string str1 = string.Empty;
  DataTable dataTable = new DataTable();
  if (!string.IsNullOrEmpty(strYear))
    dataTable = this.db.ExecSQLReDataTable($"select * from BudgetCollectManage where BudgetYear = {strYear} and CollectState in (0,1) order by BudgetTime");
```

参数strYear被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

整体执行流程如下，当中其他几个方法也存在同样的sql注入漏洞，就不赘述了

[![金和OA AjaxForSetDecompose.ashx SQL注入漏洞](images/img-001-a737a06024d5.webp)](https://image.mrxn.net/bb308744f9fc452db524be90299389d4.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/AjaxForSetDecompose.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getDetpCollect&strYear=SQLI_POC
```

[![金和OA AjaxForSetDecompose.ashx SQL注入漏洞](images/img-002-3837ef13ae4b.webp)](https://image.mrxn.net/b23f03f6bde346b680d2970a12299ce0.webp)

成功延时 8 秒

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
文章标题：[金和OA AjaxForSetDecompose.ashx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AjaxForSetDecompose-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AjaxForSetDecompose-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForSetDecompose-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AjaxForSetDecompose-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 