---
title: "金和OA VouchUpdate.aspx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-VouchUpdate-sqli.html
asset_dir: assets/金和oa-vouchupdate.aspx-多处sql注入漏洞
---

# 金和OA VouchUpdate.aspx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/14 13:28
- 301浏览
- [0评论](#comment)
- 27分钟阅读

深入探索

SQL注入防护

Nessus

网络安全会议

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `VouchUpdate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `VouchUpdate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **VouchUpdate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  if (!string.IsNullOrEmpty(this.Request["no"].ToString()))
    ((HtmlInputControl) this.hidAppNo).Value = this.Request["no"].ToString();
  if (!string.IsNullOrEmpty(this.Request["type"].ToString()))
    ((HtmlInputControl) this.hidAccType).Value = this.Request["type"].ToString();
  this.cm.BindDropDownList(this.ddlAccount, this.cm.dtAccount(), "请选择", "");
  this.cm.BindDropDownList(this.ddlVoucherType, this.cm.dtVoucherType(), "请选择", "");
  ((ListControl) this.ddlAccount).SelectedValue = this.cm.GetAccByRecordNo(((HtmlInputControl) this.hidAppNo).Value);
  ((ListControl) this.ddlVoucherType).SelectedValue = this.cm.GetVoucherByRecordNo(((HtmlInputControl) this.hidAppNo).Value);
  this.getAccSubData(((HtmlInputControl) this.hidAppNo).Value, ((HtmlInputControl) this.hidAccType).Value);
  this.fType = this.cm.getFinanceType();
}
```

参数**no**和**type**赋值给**hidAppNo**和**hidAccType**后被带入`GetAccByRecordNo`、`GetVoucherByRecordNo`与`getAccSubData`方法中，它们的实现如下

代码安全审计

## GetAccByRecordNo

```
public string GetAccByRecordNo(string strRecordNo)
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"SELECT ZT FROM dbo.Budget_RecordNoVouch WHERE RecordNo='{strRecordNo}'");
  return ((InternalDataCollectionBase) dataTable.Rows).Count == 1 ? dataTable.Rows[0][0].ToString() : "";
}
```

至此，就非常明了了，参数`projid`被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

## GetVoucherByRecordNo

```
public string GetVoucherByRecordNo(string strRecordNo)
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"SELECT VoucherType FROM dbo.Budget_RecordNoVouch WHERE RecordNo='{strRecordNo}'");
  return ((InternalDataCollectionBase) dataTable.Rows).Count == 1 ? dataTable.Rows[0][0].ToString() : "";
}
```

## getAccSubData

```
public void getAccSubData(string recordNo, string accType)
{
  DataTable dataTable = this.cm.Budget_AccountSubject_Search(recordNo, accType);

public DataTable Budget_AccountSubject_Search(string AppNo, string accType)
{
  return this.db.ExecSQLReDataTable($"select Budget_AccountSubject.*,Budget_Subject.SubjectCode from Budget_AccountSubject\r\nleft join Budget_Subject on Budget_AccountSubject.ItemCode = Budget_Subject.SubjectNo and Budget_Subject.DelFlag=0 where AppNo = '{AppNo}' and acctype='{accType}'");
}
```

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/VouchUpdate.aspx/?no=SQLI_POC&type=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA VouchUpdate.aspx 多处SQL注入漏洞](images/img-001-cfe170f49a54.webp)](https://image.mrxn.net/2cb5d0ca3b8f4b06a557abb11b118a7a.webp)

成功延时 4 秒

漏洞修复方案

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
- [4.1.GetAccByRecordNo](#toc-4-1-)
- [4.2.GetVoucherByRecordNo](#toc-4-2-)
- [4.3.getAccSubData](#toc-4-3-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKlUlEQVR4AeydgXLrtg5Ec/r//9znFbIkREKynJtra/qYCbLAYgEyhBg7aaf95+vr698/tX+/P6o+36kdvKpzcVWXOesy5rz8s1zOy7e5xrHQnFHcb5gG8uizPu9yAm0gj0l/vWLVN+D6Kldx1gur/MhJZxtzioEvQG6zUQ9sGqB9v038cCDyrhNCcI90+4SZc1I1r5jrhG0gCpZ9/gSmgUBMHmq8suX8dMDc50qPn2i8bq6FWN+5jNZVHEQdYFm7UdI38sQB2m2E2a9Kp4FUosW97wTWQN531pdW+tWBwPG11DUfDbr+0m4LUe5ZpBsFfS0I30mIGOoX+ld11v8Ef3UgP9nAqtmfwK8OJD+t9vfLRQTxRFojhOCgo3hZVO2/ipft2TmSJtus2DMQ6+/Z90W/OpC27eX8+ATWQH58dH+ncBpIvt6Vf2UbENceaHKgvSdvZHK8VqKaC70W9n4THTiw13sdIUQul4qXZe6nvvqcWdV3GkglWtz7TqANBOJpgWtYbRGiNj8V1lWcc0KYa2HPSWdzPwgN4FS7iXD+NtYF7iUEtnr5tjOdcxkhesA1zLVtIJlc/udOYA3kc2dfrvyPr+WfoDu7h2Phb3LuJVRvmXybYpljIcSPDfEyiBhQuBmw/ZgCtlhfgIkTb1Nv2RiL+xNbN8QnehOcBgLzkwGdg9n39wJzDmbO+oww62DPZX3lw14PVLLGVU9ySybHOqDdGtj7SV66EPoqCZEDvqaBfN334/9iZ/9Anw70t4l6KqoTED+adeYdC81lFC+DvnbO25dG5hi6HmZf2tFca96x0FyFytsg1nIsdI18meNnCNELOuaadUPyadzAXwO5wRDyFtrbXpPQrxKErytpg+BgRvewVgihc04I1zjVy1Qjk29TPJpzGSHWMgcRQ8exz5V47FfVQF/D+qyruHVD8gndwG8D8bQyen/QJ20u6+w79wwrfcVBXxf2/pk+rz/qHGfMevvQ17PWOSFE/iwn3WjWC52Tb2sDcXLhZ09gDeSz5z+t3gYCcQWho9W+TkJzMOucqxC6HsKvdJnTejJz8m1wrQfsdRAx1Oi1KoReM+4Des611ggh8s4dYRvIkeA/z9/sGzwdiCYrg5gu0LYv3mYS2P7W4zijtUcIcy0E55rcr/Ktg6iD/peHM32VyxxEv8yd+d5H1lQcRF/oeDqQ3HD57zmBNZD3nPPlVdofF6srVXWxDvo1s845x88Qeg/Xwsyd9XGdEKI26yE4CMy5M1/9zsy11jgWwvFaEDlA0snWDZmO5LNE+1sWML0gw8x5u34yhOYg9NBReZk1GcXbzDsWmqtQeRnMa4k/stwLojZrnYfIAaa28wE2bORFB6KuWiu3WDckn8YN/DWQGwwhb+F0IPl62XcxxBWEjs5ZK4Seh/Ctg4ihRusqhKjRGjYIDjq6FoKzVjjm4NrvLaqF6Ocez1A1sme604E8K175wxP4ceLSQCCeBuioaY9W7cKas5w1wqyDvh7sfWll0HnFo+V+oz9qFUP0G7WvxOojq2og+kN9Gy8NpGq8uL9zAu0Xw6o9xDQ17dEgcsBUCmxvDYGWy/UmgUu6XGvfPTJC9Mvcq777Z4TjvvA8B6GBfivUH4LPe1w3JJ/GDfw1kBsMIW+h/aZuUlfJZg7iakFHa4TWyZc5FkLUyB9NWptzEHro17vKQehcLzzTXclZI4ToDyjcDDj8EbsJvr9A6LSn0b4lG4w5xeuGbEdzny/TizrEdGF+QrVtTVEGXQfhKz+atDIIDdAkQHviIHxpbRbCcc6ajK7PmPP2nXec0Tmhefk2cxB7cywcNeJg1kFw0HHdEJ3WjWwN5EbD0FbaQKprBnGVnBOqSCZ/NJj1MHOqH829Mg9Raw4ihv7jFGbOeiFEXr7M6wgVjwahh46jJsfqI8tc5Usjg/O+bSBVk8W9/wTaQCAmpymOlrcFoYOOOS8fjnM5n9eBqFHelvOjD7PedRW6HqIOOlb6Z9zYr9LDvIbrhFVNG0iVXNz7T2AN5P1nfrpiG4iukCyroV85CF+a0eA4l/ud+e4J0QuY5ED7vWVKPgjoeQj/QW+fELHXEW6JC1+klWUpzP2kkVkn32buGbaBPBOu/HtOoP0tC2Li1bKestB5CD30t6BVzlyF0Hs4rzVsEHnnMlqT0fnMjT5ET5j37fojhF5rDXQOwnfuGXpvWbduSD6NG/htINW0Kg7iKXBOOH4f4mxjTrFzGSH6Km9zHuacNRA5qJ946HnoGvV2j4ziZZmD6CH+yLL+qg/RN+vbQDL5d/3V/ewE1kDOTucDuWkgENcION0O0N6CQvinBSkJs94/CiBy0NGl1ggh8s4JITjoKK1MeRn0HIQv3gYz51yFEHqtYYPgzvRAlV7/rZPyVD5IthsCbE+8pyyE4PL+xI+W8/Ih6qC/iELnpJHBzOXe0sjMyT8z6zJCrGHurP6VHETfV2qk9T6EimXybW0gSiz7/AmsgXx+BrsdtIH4ykBcReg/bnYV3wF03Te1/cgDHG4IbLz7C7fE8AVCBx2llQ3SwxB6LYR/KH4k1FsGoYX6e5ZGBl33KN8+xctgzm2C7y8Q+e/wENpADhUr8dYTOB0IHE9VT8Vo3vnIK3Yuo3hb5l/xXS90nXybOZi/F5g5668iRA+vlzH3MA+hh/o2ng4kN7y7/1/Z3xrIzSY5/YtyvloZ856hXznY+9ZB569yXs/6CmHuW+ky574VWpdzZ5xzGV2bucqH2Lv1QggOOq4bUp3eB7npH1BBnxaEX+1PE7aNefPCMadYvEz+aOJtEOtD4Kgd46rOGjjuAZEDLN/eqgM7dH+hhbDXQB2rRuY6oeLR1g3RydzI1kBuNAxtpb2oj1cnxxKOBv1qWjtqjmKIWtcJITjoKF7mPvJHg66H8K3P6LqKc06Y86MP0R8YUz+Kge1HYi5eNySfxg389qJ+dS96ikY7q4X5KXA9RA76b63OCSHy7g8RA6Yu//9pgelphGNO64/WFk3OqMlxkp26EPsA1j+g+jr9eH+yvYZAnxK85nvbfjqg15vLCJF33RG6psrDcQ/XCatac8rLHAsVyyD6A6KfGrDdQKDUAi0P4VfC9RpSncoHuTWQDx5+tXQbiK7pK1Y1g/kqwsxdra105rxXiP7Q3xhA56yvELoO9r77C10r32bOaF5oLqP40XLefhuIiYWfPYFpILB/UmAfv3O7EGv7yXq2NoQ+62DmnL/a1/oKIfrDjJW+4rwP4TSQqmBx7zuBNZD3nfWllX51ILpysmcrSzOaa6BffXNnmPtYl7nRh94fws8a96gQQg/9DYR1uYd954TQayF86yBiYP2m/vWBj7Mlf/WGQEzak8+YNwGhy5y1mTvzYe5R6SF0EFhpMlftA6LWOSHsudwDIpc51cgyV/m/OpBqgcW9dgJrIK+d119XTwPRtTqzsx25Lmsgri90dB5mzj0yQuhclxEiBzQaaH/Iy33kN9HDUSx7uO0Tei2EL40MIgZO9U6qxlZxwLZPa4TTQFy48DMn0AYCMS24hmfbhd6j0ulJGA16Dez9Uav4p31zHezXAXJ68rWuzUnHGZ0DthsAHZ3LCD3fBpIFy//cCayBfO7sy5X/BwAA//+zv9kUAAAABklEQVQDAKX+RrlnEz8oAAAAAElFTkSuQmCC)

手机扫码阅读
