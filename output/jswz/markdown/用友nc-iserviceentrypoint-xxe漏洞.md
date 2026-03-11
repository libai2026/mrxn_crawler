---
title: "用友NC IServiceEntryPoint XXE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-IServiceEntryPoint-getResult-xxe.html
asset_dir: assets/用友nc-iserviceentrypoint-xxe漏洞
---

# 用友NC IServiceEntryPoint XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/10 08:30
* 1228浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

Web服务

SQL

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

⽤友NC IServiceEntryPoint 接⼝处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感⽂件，进 ⼀步利⽤可导致服务器失陷。

漏洞预警服务

# 影响版本

NC65

# fofa语法

> `app="⽤友-UFIDA-NC"`

# 漏洞分析

看下 `IServiceEntryPoint` 的业务逻辑

深入探索

网络安全课程

防火墙软件

数据库

```
package nc.uap.oba.word.webservice;

import nc.bs.framework.common.UserExit;
import nc.uap.oba.Serializer;
import nc.uap.oba.word.webservice.entity.BusinessResult;
import nc.uap.oba.word.webservice.entity.RequestInfo;
import nc.uap.oba.word.webservice.entity.ResponseService;
import nc.uap.oba.word.webservice.handler.CustomServiceHandler;
import nc.uap.oba.word.webservice.handler.ReqServiceHandler;

public class ServiceEntryPointImpl implements IServiceEntryPoint {
    public ServiceEntryPointImpl() {
    }

    public String getResult(String data) {
        BusinessResult result = new BusinessResult();
        result.setSuccessful(false);
        String message = null;

        try {
            RequestInfo reqInfo = (RequestInfo)Serializer.deserialize(data, RequestInfo.class);
            UserExit.getInstance().setUserDataSource(reqInfo.getDsName());
            message = reqInfo.getName();
```

深入探索

JSON处理工具

网络安全培训

漏洞扫描服务

`getResult` 方法直接将 `data` 带入 `Serializer.deserialize` 方法中，看下其实现逻辑

网络安全

```
package nc.uap.oba;

import java.io.StringReader;
import java.io.StringWriter;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import javax.xml.transform.stream.StreamSource;

public class Serializer {
    public Serializer() {
    }

    public static String serialize(Object value) throws Exception {
        StringWriter writer = new StringWriter();
        JAXBContext jaxbContext = JAXBContext.newInstance(new Class[]{value.getClass()});
        Marshaller marshaller = jaxbContext.createMarshaller();
        marshaller.marshal(value, writer);
        return writer.getBuffer().toString();
    }

    public static <T> T deserialize(String xml, Class<?> type) throws Exception {
        JAXBContext jaxbContext = JAXBContext.newInstance(new Class[]{type});
        StreamSource streamSouce = new StreamSource(new StringReader(xml));
        Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
        return (T)unmarshaller.unmarshal(streamSouce);
    }
}
```

`deserialize` 方法里直接使用 `javax.xml.bind.Unmarshaller` 对 xml 内容进行操作，而JAXB的`Unmarshaller`默认启用外部实体解析功能，未对XML输入中的实体引用进行限制，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)测试

```
POST /uapws/service/nc.uap.oba.word.webservice.IServiceEntryPoint HTTP/1.1
Host: nc.mrxn.net
Content-Type: text/xml;charset=UTF-8

<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:iser="http://webservice.word.oba.uap.nc/IServiceEntryPoint">  
  <soapenv:Header/>  
  <soapenv:Body> 
    <iser:getResult> 
      <!--type: string-->  
      <iser:string>XXE POC</iser:string> 
    </iser:getResult> 
  </soapenv:Body> 
</soapenv:Envelope>
```

DNSLOG 平台成功收到HTTP请求

计算机服务器

[![用友NC IServiceEntryPoint XXE漏洞](images/img-001-625a4ddb57c1.webp)](https://image.mrxn.net/1996db71b511443ca42b5b9b92f32c1f.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
* [#XXE](https://mrxn.net/tag/XXE)

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
文章标题：[用友NC IServiceEntryPoint XXE漏洞](https://mrxn.net/jswz/yonyou-nc-IServiceEntryPoint-getResult-xxe.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-IServiceEntryPoint-getResult-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-IServiceEntryPoint-getResult-xxe.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-IServiceEntryPoint-getResult-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 