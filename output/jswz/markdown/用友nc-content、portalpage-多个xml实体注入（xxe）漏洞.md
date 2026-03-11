---
title: "用友NC content、portalpage 多个XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/yonyou-nc-portalpage-content-XXE.html
asset_dir: assets/用友nc-content、portalpage-多个xml实体注入（xxe）漏洞
---

# 用友NC content、portalpage 多个XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/27 09:47
* 792浏览
* [0评论](#comment)
* 1小时阅读

深入探索

parse

parser

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统存在XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。攻击者可通过构造恶意XML内容，利用portalpage/doNew接口解析，实现任意文件读取或SSRF攻击等攻击，进而可能导致敏感信息泄露或进一步的系统入侵。

代码安全审计

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"
>
> 漏洞扫描服务

# 漏洞分析

深入探索

VPN服务

服务器安全服务

网页浏览器

根据官方漏洞通告部分可知漏洞点为 **PmlUtil**

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-001-61b4b0c46b74.webp)](https://image.mrxn.net/f4058a77c2da45978bb231dda4c4348a.webp)

那就搜索**PmlUtil**，找到了 `nc/uap/portal/util/PmlUtil.java` 看下它的实现吧

计算机科学

```
public class PmlUtil {
    public static Digester getPortletDigester() {
        Digester pmlDigester = LfwXmlUtil.getDigester((String)Page.class.getName());
        if (pmlDigester == null) {
            pmlDigester = new Digester();
            LfwXmlUtil.setDigester((String)Page.class.getName(), (Digester)pmlDigester);
            PmlUtil.initPsmlDigester(pmlDigester);
        }
        return pmlDigester;
    }

    private static void initPsmlDigester(Digester pmlDigester) {
        pmlDigester.setValidating(false);
        pmlDigester.addObjectCreate("page", Page.class.getName());
        pmlDigester.addSetProperties("page");
        pmlDigester.addCallMethod("page/title", "setTitle", 0);
        String layoutClazz = Layout.class.getName();
        String portletClazz = Portlet.class.getName();
        pmlDigester.addObjectCreate("page/layout", layoutClazz);
        pmlDigester.addSetProperties("page/layout");
        pmlDigester.addSetNext("page/layout", "setLayout", layoutClazz);
        String layoutPath = "page/layout";
        for (int i = 0; i < 10; ++i) {
            String _layoutPath = layoutPath + "/layout";
            pmlDigester.addObjectCreate(_layoutPath, layoutClazz);
            pmlDigester.addSetProperties(_layoutPath);
            pmlDigester.addSetNext(_layoutPath, "addChild", layoutClazz);
            String portletPath = layoutPath + "/portlet";
            pmlDigester.addObjectCreate(portletPath, portletClazz);
            pmlDigester.addSetProperties(portletPath);
            pmlDigester.addSetNext(portletPath, "addChild", portletClazz);
            layoutPath = _layoutPath;
        }
    }
    //xml文件解析
    public static Page parser(File pml) throws PortalServiceException {
    Digester digester = PmlUtil.getPortletDigester();
    try {
        Page page = null;
        Digester digester2 = digester;
        synchronized (digester2) {
            page = (Page)digester.parse(pml);
        }
        String pmlName = pml.getName();
        page.setPagename(pmlName.substring(0, pmlName.length() - 4));
        return page;
    }
    catch (Exception e) {
        throw new PortalServiceException(e.getMessage(), e.getCause());
    }
}
//xml内容解析
public static Page parser(String pml) throws SAXException {
    Object object;
    Digester digester = PmlUtil.getPortletDigester();
    StringReader reader = null;
    try {
        Page page = null;
        reader = new StringReader(pml);
        object = digester;
        synchronized (object) {
            page = (Page)digester.parse((Reader)reader);
        }
        object = page;
    }
    catch (Exception e) {
        try {
            PortalLogger.error((String)LfwResBundle.getInstance().getStrByID("pserver", "PmlUtil-000002"), (Throwable)e);
            throw new SAXException(e.getMessage());
        }
        catch (Throwable throwable) {
            IOUtils.closeQuietly(reader);
            throw throwable;
        }
    }
    IOUtils.closeQuietly((Reader)reader);
    return object;
}
//文件流的形式解析
public static Page parser(InputStream in) throws SAXException {
    if (in == null) {
        return null;
    }
    Digester digester = PmlUtil.getPortletDigester();
    try {
        Page page = null;
        Object object = digester;
        synchronized (object) {
            page = (Page)digester.parse(in);
        }
        object = page;
        return object;
    }
    catch (Exception e) {
        PortalLogger.error((String)LfwResBundle.getInstance().getStrByID("pserver", "PmlUtil-000002"), (Throwable)e);
        throw new SAXException(e.getMessage());
    }
    finally {
        IOUtils.closeQuietly((InputStream)in);
    }
}
```

代码不多，很简单，就是对多个形式如string、流、文件几种形式的内容进行解析，且`PmlUtil.initPsmlDigester()` 方法中并未发现**禁用外部实体解析功能设置。**这意味着攻击者可以通过注入恶意 XML 实体来读取服务器本地文件、发起 SSRF 攻击或导致拒绝服务。

漏洞扫描服务

那就看下有那些地方调用了`PmlUtil.parser()` 方法，

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-002-796dca6d9338.webp)](https://image.mrxn.net/34de27cb0ff84d1fbabb97de04a5fad4.webp)

总共找到了4个地方的11个调用，只需关注首尾两个action相关的，中间的两个是不对外的。

在`PagePreviewAction.java` 中找到了**content**方法相关实现

计算机科学

## content

```
@Servlet(path="/page/preview")
public class PagePreviewAction
extends BaseAction {
    @Action
    public void content() {
        try {
            String page_xml = this.request.getParameter("page_xml");
            byte[] bytes = page_xml.getBytes("ISO-8859-1");
            String xml = new String(bytes, "UTF-8");
            xml = URLDecoder.decode(xml, "UTF-8");
            Page page = PmlUtil.parser((String)xml);
```

参数`page_xml`的值赋值给**page\_xml**后按照 `ISO-8859-1` 编码方式转换成字节数组，然后使用 `UTF-8` 编码方式，将上一步得到的字节数组 `bytes` 解码成一个新的 `String` 对象 `xml`，最后进行URL解码后就带入`PmlUtil.parser` 方法中进行解析，因此造成了XML实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。。

代码安全审计

再看其他几处

## portalpage

### doNew

```
@Servlet(path="/portalpage")
public class PortalPageManagerAction
extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    @Action(method="POST")
    public void doNew(@Param(name="groupid") String pk_group, @Param(name="pml") String pml) {
        LfwSessionBean ses = LfwRuntimeEnvironment.getLfwSessionBean();
        if (pml == null || ses == null) {
            return;
        }
        try {
            Page page = PmlUtil.parser((String)URLDecoder.decode(pml, "UTF-8"));
```

该方法还存在SQL注入漏洞，可参考 [用友NC portalpage/doNew sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-portalpage-doNew-groupid-sqli.html) （需要合法session）

计算机科学

### doEdit

```
@Action(method="POST")
public void doEdit(@Param(name="pk") String pk, @Param(name="pml") String pml) {
    LfwSessionBean ses = LfwRuntimeEnvironment.getLfwSessionBean();
    if (pml == null || pk == null || ses == null) {
        return;
    }
    try {
        boolean pageNameHasModify;
        PtPageVO oldVersion = PortalServiceUtil.getPageQryService().getPageByPk(pk);
        if (oldVersion == null) {
            this.print("<result><success>false</success><detail>" + NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000006") + "</detail></result>");
            return;
        }
        String pk_group = oldVersion.getPk_group();
        Page page = PmlUtil.parser((String)URLDecoder.decode(pml, "UTF-8"));
```

### importPml

> 文件上传形式
>
> 漏洞扫描服务

```
@Action
public void importPml() throws IOException {
    MultipartHttpServletRequest req = PortalPageManagerAction.getMultipartResolver(this.request);
    Map fileMap = req.getFileMap();
    ArrayList files = new ArrayList();
    String billitem = req.getParameter("billitem");
    if ("null".equals(billitem)) {
        billitem = "";
    }
    if (MapUtils.isNotEmpty((Map)fileMap)) {
        files.addAll(fileMap.values());
    }
    String name = ((MultipartFile)files.get(0)).getOriginalFilename();
    name = name.replace(".pml", "");
    InputStream in = ((MultipartFile)files.get(0)).getInputStream();
    try {
        Page page = PmlUtil.parser((String)IOUtils.toString((InputStream)in, (String)"UTF-8"));
```

该方法还存在SQL注入漏洞，可参考 [用友NC portalpage/importPml sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-portalpage-importPml-billitem-sqli.html)

# 漏洞复现

## content

> 需要URL双重编码
>
> SQL注入防护

```
POST /portal/pt/page/preview/content?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

page_xml=XXE_POC
```

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-003-170aa3320b0f.webp)](https://image.mrxn.net/9b25a12720104df280bd2cd59e4333c6.webp)

成功在DNSLOG平台收到其DNS请求和HTTP请求

代码安全审计

## importPml

```
POST /portal/pt/portalpage/importPml?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarybXJ4bi5uZXQ

------WebKitFormBoundarybXJ4bi5uZXQ
Content-Disposition: form-data; name="file"; filename="1.png"

XXE_POC
------WebKitFormBoundarybXJ4bi5uZXQ--
```

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-004-5818ea781827.webp)](https://image.mrxn.net/4917ffd246194c7b94a93fa7341d76b6.webp)

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-005-227c45c7afcc.webp)](https://image.mrxn.net/eb712599d6bb4cb08094797a81773b4f.webp)

也是可以在DNSLOG平台收到DNS和HTTP请求

漏洞扫描服务

# 参考

* [关于NC系统content接口的XML注入漏洞的安全通告](https://security.yonyou.com/#/noticeInfo?id=733)

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
* [4.1.content](#toc-4-1-)
* [4.2.portalpage](#toc-4-2-)
* [4.2.1.doNew](#toc-4-2-1-)
* [4.2.2.doEdit](#toc-4-2-2-)
* [4.2.3.importPml](#toc-4-2-3-)
* [5.漏洞复现](#toc-5-)
* [5.1.content](#toc-5-1-)
* [5.2.importPml](#toc-5-2-)
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
文章标题：[用友NC content、portalpage 多个XML实体注入（XXE）漏洞](https://mrxn.net/jswz/yonyou-nc-portalpage-content-XXE.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-portalpage-content-XXE.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-portalpage-content-XXE.html"),
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

安全工具开发

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-portalpage-content-XXE.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 