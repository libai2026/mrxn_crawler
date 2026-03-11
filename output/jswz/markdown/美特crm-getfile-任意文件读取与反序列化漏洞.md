---
title: "美特CRM getFile 任意文件读取与反序列化漏洞"
source: https://mrxn.net/jswz/metasoft-getFile-rce-fileread.html
asset_dir: assets/美特crm-getfile-任意文件读取与反序列化漏洞
---

# 美特CRM getFile 任意文件读取与反序列化漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/9 08:32
* 1250浏览
* [0评论](#comment)
* 1小时阅读

深入探索

encrypt

Encrypt

加密


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

MetaCRM是一款智能平台化CRM软件,通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM getFile 接口存在任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)和fastjson[反序列化漏洞](https://mrxn.net/tag/rce)。

# 影响版本

CRM6.5

# fofa语法

> `body="/common/scripts/basic.js" && body="www.metacrm.com.cn"`

# 漏洞分析

先看 web.xml 里对于 getFile 接口的定义

客户关系管理

```
<!-- 流的方式展示文件 -->
    <servlet>
        <servlet-name>getFile</servlet-name>
        <servlet-class>com.metasoft.framework.controller.getFile</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>getFile</servlet-name>
        <url-pattern>/getFile</url-pattern>
    </servlet-mapping>
```

深入探索

Web安全课程

身份验证

漏洞扫描器

进入 `com.metasoft.framework.controller.getFile` 看下其实现逻辑

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-001-3c6829ebc9ee.webp)](https://image.mrxn.net/17cd8d4bb8b84abe8171ac39996c8c54.webp)

以及系统的fastjson版本 fastjson-1.2.4.jar,是存在漏洞的版本

漏洞预警服务

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-002-9fc49f9e3085.webp)](https://image.mrxn.net/66fd2a7d00644896b6b04010da7c0f8f.webp)

看下AES加解密的部分

```
public class AesEcbCipher {
    private static final String SECRET_KEY = "metacrmloginpass";
    private byte[] key = "metacrmloginpass".getBytes();

    public AesEcbCipher(String secretKey) {
        this.key = secretKey.getBytes();
    }

    public AesEcbCipher() {
    }

    public String Encrypt(String sSrc) {
        try {
            SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(1, skeySpec);
            byte[] encrypted = cipher.doFinal(sSrc.getBytes("UTF-8"));
            return (new BASE64Encoder()).encode(encrypted);
        } catch (Exception ex) {
            Debug.error("", ex);
            return null;
        }
    }

    public String Decrypt(String sSrc) {
        if (sSrc != null && sSrc.length() != 0) {
            try {
                SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
                cipher.init(2, skeySpec);
                byte[] encrypted1 = (new BASE64Decoder()).decodeBuffer(sSrc);
                byte[] original = cipher.doFinal(encrypted1);
                return new String(original, "UTF-8");
            } catch (Exception ex) {
                Debug.error("", ex);
                return sSrc;
            }
        } else {
            return sSrc;
        }
    }

    public String encrypt(String sSrc) {
        try {
            SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
            cipher.init(1, skeySpec);
            byte[] encrypted = cipher.doFinal(sSrc.getBytes("UTF-8"));
            return Hex.encodeHexStr(encrypted);
        } catch (Exception ex) {
            Debug.error("", ex);
            return null;
        }
    }

    public String decrypt(String sSrc) {
        if (sSrc != null && sSrc.length() != 0) {
            try {
                SecretKeySpec skeySpec = new SecretKeySpec(this.key, "AES");
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
                cipher.init(2, skeySpec);
                byte[] encrypted1 = Hex.decodeHex(sSrc.toCharArray());
                byte[] original = cipher.doFinal(encrypted1);
                return new String(original, "UTF-8");
            } catch (Exception ex) {
                Debug.error("", ex);
                return sSrc;
            }
        } else {
            return sSrc;
        }
    }
}
```

硬编码密钥 `metacrmloginpass` ，加解密都是基于hex格式进行，即传入的数据为hex格式。

物流软件安全

## 反序列化

再看下涉及反序列化的处理逻辑

```
import com.alibaba.fastjson.JSONObject;
......
String a = request.getServletPath();
String c = request.getRequestURI();
c = StringUtil.replaceStr(c, a + "/", "");
String[] ps = StringUtil.string2array(c, "/");
String url = ps[0];
AesEcbCipher aec = new AesEcbCipher();
String dec = aec.decrypt(url);
JSONObject json = JSONObject.parseObject(dec);
```

`dec` 最终来自AES解密后 `url` 后的结果，而 `url`又来自 `request.getRequestURI()` 替换掉 ServletPath+/ 后的值，如请求 `/mrxn/xxxxxxx` 得到的最终 `url` 值就是去掉 `mrxn/` 后的 `xxxxxxx` ；经过上述处理后，直接调用 fastjson 的 `parseObject` 方法处理，导致fastjson 反序列化漏洞。

漏洞预警服务

## 文件读取

```
String fileName = json.getString("fileName");
String folder = json.getString("folder");
String sCorpName = json.getString("sCorpName");
String securityCode = json.getString("securityCode");
UserState us = UserManager.getUserBySessionId(request.getSession().getId());
if (us == null && !FileSecurityCode.checkSecurityCode(securityCode)) {
    request.setAttribute("error", (new ResourceService()).getDispMessage("error.common.upanddown.login"));

    try {
        request.getRequestDispatcher("/common/images/default/limit.png").forward(request, response);
    } catch (ServletException e) {
        Debug.error("", e);
    }

} else {
    FileSecurityCode.visits(securityCode);
    response.setContentType(Path.getContentType(fileName));
    String path;
    if ("attach".equals(folder)) {
        path = Path.getAttachAbsoluteDirectory(sCorpName);
    } else if ("template".equals(folder)) {
        path = Path.getTemplateAbsoluteDirectory(sCorpName);
    } else if ("userlogo".equals(folder)) {
        path = Path.getLogoAbsoluteDirectory(sCorpName);
    } else if ("messageserv".equals(folder)) {
        path = Path.getMessageServerAbsoluteDirectory(sCorpName);
    } else if ("picture".equals(folder)) {
        path = Path.getPictureAbsoluteDirectory(sCorpName);
    } else if ("skinbackground".equals(folder)) {
        path = Path.getBackgroundAbsoluteDirectory(sCorpName);
    } else if ("icon".equals(folder)) {
        path = Path.getIconAbsoluteDirectory(sCorpName);
    } else {
        path = Path.getTempAbsoluteDirectory(sCorpName);
    }

    path = path + fileName;
    this.log.debug("path={}", path);
    FileInputStream fio = new FileInputStream(new File(path));
    IOUtils.copyLarge(fio, response.getOutputStream());
    IOUtils.closeQuietly(fio);
```

AES解密后的内容经fastjson处理后，取出其中需要的 fileName 、folder、sCorpName、securityCode等，主要是`path = path + fileName;` 其中 path 与 fileName 都是用户可控，且对路径无任何校验或过滤，拼接后直接调用 `new File(path)` 进行文件操作，造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

整体执行流程如下图所示

漏洞预警服务

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-003-45d7ac5b4abf.webp)](https://image.mrxn.net/91a1f5068aab4ef580b25c59b0af52ce.webp)

# 漏洞复现

## 反序列化

```
GET /getFile/AES加密后的payload HTTP/1.1
Host: metasoft.mrxn.net
Cookie: JSESSIONID=D74D969B9489FFBE41D5F5ACE5CAC014
```

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-004-ed6e8367b5f4.webp)](https://image.mrxn.net/e384f1c4633d4822803e7d85d3cc0e17.webp)

DNSLOG平台成功收到请求

## 文件读取

> [漏洞利用](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)需要合法的cookie或者securityCode
>
> 漏洞预警服务
>
> 而系统自带 druid ，因此可以访问 `/druid/websession.html` 拿到系统以及存在的 `SESSIONID` 后进行批量枚举尝试

```
GET /getFile/AES加密后的payload HTTP/1.1
Host: metasoft.mrxn.net
Cookie: JSESSIONID=2A6482AE7774FBC13DD7854E15CE90F4
```

[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-005-e7446d765335.webp)](https://image.mrxn.net/f8ea7ec43dbc4568bd42aaaa15a43b51.webp)  
[![美特CRM getFile 任意文件读取与反序列化漏洞](images/img-006-ade69cb525fe.webp)](https://image.mrxn.net/6ff0bddd7fdb498793e60cb057177031.webp)

成功读取到 `web.xml` 文件内容

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
* [#目录遍历](https://mrxn.net/tag/%E7%9B%AE%E5%BD%95%E9%81%8D%E5%8E%86)

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
* [4.1.反序列化](#toc-4-1-)
* [4.2.文件读取](#toc-4-2-)
* [5.漏洞复现](#toc-5-)
* [5.1.反序列化](#toc-5-1-)
* [5.2.文件读取](#toc-5-2-)



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
文章标题：[美特CRM getFile 任意文件读取与反序列化漏洞](https://mrxn.net/jswz/metasoft-getFile-rce-fileread.html)  
文章链接：<https://mrxn.net/jswz/metasoft-getFile-rce-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/metasoft-getFile-rce-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/metasoft-getFile-rce-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 