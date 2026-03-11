---
title: "金和OA AjaxForSetDecompose.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForSetDecompose-sqli.html
asset_dir: assets/金和oa-ajaxforsetdecompose.ashx-sql注入漏洞
---

# 金和OA AjaxForSetDecompose.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/26 13:05
- 248浏览
- [0评论](#comment)
- 1小时阅读

深入探索

SQL

网络安全课程

企业安全咨询

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForSetDecompose.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

文本剥离工具

网络安全会议

软件

根据 `AjaxForSetDecompose.ashx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForSetDecompose** 的处理逻辑

```
context.Response.ContentType = "text/plain";
string str1 = "设置成功！";
string str2 = context.Request["strType"];
if (string.op_Equality(str2, "add"))
{
  string str3 = context.Request["strBudgetManageInfo"];
  string strDeptCollect = context.Request["strDeptCollect"];
  string strUserIdAndDeptId = context.Request["strUserIdAndDeptId"];
  string empty1 = string.Empty;
  if (!string.IsNullOrEmpty(strDeptCollect))
    empty1 = strDeptCollect.Split(new char[1]{ '@' })[0].Split(new char[1]
    {
      '|'
    })[0];
  if (string.op_Equality(context.Request["strCollectState"], "old"))
  {
    string empty2 = string.Empty;
    DataTable budgetCollectManage = this.budgetDecomposeDao.GetBudgetCollectManage(empty1);
    string str4 = budgetCollectManage == null || ((InternalDataCollectionBase) budgetCollectManage.Rows).Count <= 0 ? "没进行过公司汇总流程" : budgetCollectManage.Rows[0]["BudgetTime"].ToString();
    if (string.op_Equality(str4, "0"))
      str1 = empty1 + "年度全部期间的汇总已经提交，不能进行设置的修改操作！";
    else if (string.op_Equality(str4, "没进行过公司汇总流程"))
    {
      string ToUsersList1 = string.Empty;
      string str5 = string.Empty;
      string strContent1 = $"您好，{empty1}年的预算汇总做了重新设置，您之前提交的汇总已经被撤销，请知晓！";
      DataTable dataTable1 = this.db.ExecSQLReDataTable("select * from BudgetUserAndDept where BudgetType = 1");
      if (dataTable1 != null && ((InternalDataCollectionBase) dataTable1.Rows).Count > 0)
      {
        for (int index = 0; index < ((InternalDataCollectionBase) dataTable1.Rows).Count; ++index)
          str5 = index != 0 ? $"{str5},{dataTable1.Rows[index]["DeptId"].ToString()}" : dataTable1.Rows[index]["DeptId"].ToString();
        ((MarshalByValueComponent) dataTable1).Dispose();
      }
      DataTable dataTable2 = this.db.ExecSQLReDataTable($"select UserID from BudgetUserAndDept where BudgetType = 1 \r\n                                    union \r\n                                    select distinct UserID from RelationshipUsers where DeptLeader = 1 and DeptID in ({str5})");
      if (dataTable2 != null && ((InternalDataCollectionBase) dataTable2.Rows).Count > 0)
      {
        for (int index = 0; index < ((InternalDataCollectionBase) dataTable2.Rows).Count; ++index)
          ToUsersList1 = index != 0 ? $"{ToUsersList1},{dataTable2.Rows[index]["UserID"].ToString()}" : dataTable2.Rows[index]["UserID"].ToString();
        ((MarshalByValueComponent) dataTable2).Dispose();
      }
      this.Callt.InsertCall(strContent1, ToUsersList1, context.Session["UserCode"].ToString(), context.Session["DeptID"].ToString(), "", "", "", "", "", "");
      this.db.ExecSQLReInt("delete CollectList where CollectYear = " + empty1);
      if (this.budgetDecomposeDao.AddBudgetManageInfo((object[]) str3.Split(new char[1]
      {
        '|'
      }), strUserIdAndDeptId) == 0)
      {
        str1 = "设置失败！";
      }
      else
      {
        this.budgetDecomposeDao.AddDeptCollect(strDeptCollect);
        string ToUsersList2 = string.Empty;
        string strContent2 = $"<a href='../JHSoft.Web.CostControl/Collect/DepartmentBudgetCollect.aspx?strYear={empty1}'>您好，{empty1}年的预算汇总已经设置，请抓紧时间处理，逾期将不能提交！</a>具体设置：";
        string str6 = strDeptCollect;
        char[] chArray1 = new char[1]{ '@' };
        foreach (string str7 in str6.Split(chArray1))
        {
          char[] chArray2 = new char[1]{ '|' };
          string[] strArray = str7.Split(chArray2);
          if (string.op_Equality(strArray[5], "0"))
            strContent2 = $"{strContent2}<br />第{strArray[1]}区间起始时间：{strArray[2]} 至 {strArray[3]}";
        }
        DataTable dataTable3 = this.db.ExecSQLReDataTable("select * from BudgetUserAndDept where BudgetType = 1");
        if (dataTable3 != null && ((InternalDataCollectionBase) dataTable3.Rows).Count > 0)
        {
          for (int index = 0; index < ((InternalDataCollectionBase) dataTable3.Rows).Count; ++index)
            str5 = index != 0 ? $"{str5},{dataTable3.Rows[index]["DeptId"].ToString()}" : dataTable3.Rows[index]["DeptId"].ToString();
          ((MarshalByValueComponent) dataTable3).Dispose();
        }
        DataTable dataTable4 = this.db.ExecSQLReDataTable($"select UserID from BudgetUserAndDept where BudgetType = 1 \r\n                                    union \r\n                                    select distinct UserID from RelationshipUsers where DeptLeader = 1 and DeptID in ({str5})");
        if (dataTable4 != null && ((InternalDataCollectionBase) dataTable4.Rows).Count > 0)
        {
          for (int index = 0; index < ((InternalDataCollectionBase) dataTable4.Rows).Count; ++index)
            ToUsersList2 = index != 0 ? $"{ToUsersList2},{dataTable4.Rows[index]["UserID"].ToString()}" : dataTable4.Rows[index]["UserID"].ToString();
          ((MarshalByValueComponent) dataTable4).Dispose();
        }
        this.Callt.InsertCall(strContent2, ToUsersList2, context.Session["UserCode"].ToString(), context.Session["DeptID"].ToString(), "", "", "", "", "", "");
      }
    }
    else
      this.budgetDecomposeDao.AddDeptCollect(strDeptCollect);
  }
  else if (this.budgetDecomposeDao.AddBudgetManageInfo((object[]) str3.Split(new char[1]
  {
    '|'
  }), strUserIdAndDeptId) == 0)
    str1 = "设置失败！";
else if (string.op_Equality(str2, "getDetpCollect"))
  str1 = this.SetDepartmentBudgetCollect(context.Request["strYear"]);
else if (string.op_Equality(str2, "getAppCollect"))
{
  string str10 = context.Request["strYear"];
  DataTable dataTable = new DataTable();
  if (!string.IsNullOrEmpty(str10))
    dataTable = this.db.ExecSQLReDataTable($"select * from BudgetCollectManage where BudgetYear = {str10} and CollectState in (0,1) order by BudgetTime");
  str1 = ((InternalDataCollectionBase) dataTable.Rows).Count <= 0 ? "0" : "1";
}
context.Response.Write(str1);
```

当 `strType=getDetpCollect` 时，**strYear** 被带入`SetDepartmentBudgetCollect`方法

```
protected string SetDepartmentBudgetCollect(string strYear)
{
  string str1 = string.Empty;
  DataTable dataTable = new DataTable();
  if (!string.IsNullOrEmpty(strYear))
    dataTable = this.db.ExecSQLReDataTable($"select * from BudgetCollectManage where BudgetYear = {strYear} and CollectState in (0,1) order by BudgetTime");
```

参数strYear被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

整体执行流程如下，当中其他几个方法也存在同样的sql注入漏洞，就不赘述了

代码安全审计

[![金和OA AjaxForSetDecompose.ashx SQL注入漏洞](images/img-001-a737a06024d5.webp)](https://image.mrxn.net/bb308744f9fc452db524be90299389d4.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/AjaxForSetDecompose.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getDetpCollect&strYear=SQLI_POC
```

[![金和OA AjaxForSetDecompose.ashx SQL注入漏洞](images/img-002-3837ef13ae4b.webp)](https://image.mrxn.net/b23f03f6bde346b680d2970a12299ce0.webp)

成功延时 8 秒

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
