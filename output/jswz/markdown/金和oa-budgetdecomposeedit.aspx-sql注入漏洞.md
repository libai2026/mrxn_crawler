---
title: "金和OA BudgetDecomposeEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BudgetDecomposeEdit-sqli.html
asset_dir: assets/金和oa-budgetdecomposeedit.aspx-sql注入漏洞
---

# 金和OA BudgetDecomposeEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/27 13:05
- 275浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

木马

数据库

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BudgetDecomposeEdit.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BudgetDecomposeEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **BudgetDecomposeEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strAppId = this.Request["httpAppID"].ToString();
  this.strBudgetDecomposeId = this.Request["httpOID"].ToString();
  this.strAppNow = this.GetAppNow("Budget_Decompose", this.strAppId);
  if (!this.IsPostBack)
    this.BindBudgetDecomposeInfo();
  this.InitPrive();
}
```

跟进`GetAppNow`方法

```
private string GetAppNow(string appt_id, string app_id)
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"select appd_id,Instance_ID from jhoa_approve where app_id='{app_id}'");
  string str1 = dataTable.Rows[0]["appd_id"].ToString();
  string str2 = dataTable.Rows[0]["Instance_ID"].ToString();
  ((MarshalByValueComponent) dataTable).Dispose();
  string str3 = this.db.ExecSQLReobject($"select version FROM JHOA_Approve_Instance WHERE (Instance_ID = '{str2}')").ToString();
  return this.db.ExecSQLReobject($"select appds_level from dbo.jhoa_approve_temp_dispose_sort where appt_id='{appt_id}' and version='{str3}' and appd_id='{str1}'").ToString();
}
```

参数`httpAppID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

深入探索

安全运维咨询

文件大小转换

物流软件安全

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/BudgetDecomposeEdit.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

httpAppID=SQLI_POC&httpOID=1
```

[![金和OA BudgetDecomposeEdit.aspx SQL注入漏洞](images/img-001-c222dd727371.webp)](https://image.mrxn.net/d70a8d33cb674ff9b1cae5934fa14fac.webp)

成功延时 4 秒

代码安全审计

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALUklEQVR4AeyZgXbbvA6D8+393/m/gVlIFCU5adc2uWfuKQcRAGlFtNuk+3O73f77avxXvp7pU0qeTt3bBc7P0N4zPKu3tqu3LrRH678JDeRef32/ywm0gdwnfHs26uaBGzDU21N7QnhhRtdAaM5XWPuucog+EPhMn+xxz8xpDdHPulB8DnHPRq5rA8nktX7dCUwDgZg+zLjbpu+ElQ5jn+ypdRBeeyBywNTxJAJLtAlCd36GEF4IXHlhr638mYOohRmzz+tpIBYufM0J/NhAfPdXzC8T4q7JnNau0dpROecZd17zZ5j7eH3mlwaxf0Dpt8SPDeRbdvcPNvnWgQDTz/azM6134i4XX/vAfC0YOdeoXgGjDtjS9t2I+wI4eNUqIPK79GPf3zqQH9vlP9T4ZwbyDx3gd7/UaSB6NHexuzjMj7J7wKzt+lQeohY62uP+K7THCFHvfIXuA+EFJps9K5zMH8TKa+7DMsA0kEG9kl8/gTYQ4PgFBo9xt0tPXgjRR2sFjPmKg/Cs+suvqBpEDVCl9qccC6p3VA44Xr91oT1GCE/NAVMNgaMfPMZWdF+0gdzX1/cbnMAf3Qlfjbp/6HeDe1ZPzu2BqMua1taF8NijmhwQNapXQORAth1r6Qqg3dmHkP6RrkjUtJT+N3E9IdORvpZ4OBDodwys16s7AsLrl2cPBA8drRkhNNeuEMIDM1Y/hCfz9VoQHvNC+yE0CDQvj8MchAcCza8QZs/DgawaXdzPnUAbCMS0YMR8ad8NFbPHa3sg+pn/W3Tfsz72nOFZfdVqH4jXBB13NZmH8GeurttAqvCG+T+xpWsgbzbmPzA+RvXxzLn3DmNN5SF06P/Pbk/u5zWEv3ogeOh9IDjXukZoDsIjTgGRQ0fxq4DZA8HZ7+tkhNEDY+7aR3g9IY9O6Jf1aSDweLK+MyC8EGg+o18PhAc6Wtth7gNRZ841zoWVg7FGHoe9RvMZqwbRz3zGXJfXK0/mtIboC9ymgdyur5eewPZPJxBTW+0OQvOdYA8EDx2tVa954ZkmPQf03kCW2p88gGPtvhA5dBwKHyQQdWc2CA+MeFbj/WW8npCzE3uBNr3Lgpjw2V480TNP1eBxX3jsqdeGqIH+Tqx6al73phx6H4i1+BzuA6FDR2vZrzV0j/IcEFrmrickn8YbrK+BvMEQ8hbaL3WYH59szGsILwRa82Ob8UyDqIdAe2HMzWfM1/DaOkQ9BJq3Twihaa2wJ6P4HFnTOmsQ/cQrsuY1jB75alxPSD2RF+fTQDxN7wtiqoCp7f9VN8N9ARxvPWGPvtYO722mb9j3s9n9nMNcUz32mhdC1FmDyKUpzK8QwgsdVaOofuieaSDVfOW/ewLT296zy0OfJPS3masa3QmPAqJfrYc1X301h6iDwKrn/cDosVZrlMPohTGXx/VGcQrnQhjrxNW4nhCd2htFG4gn9czeqhfGya96QHig48q343xN4873WR5iP66DyGH+CVCvDd1b652fIUR99rSBZPJav+4EtgPx3bBCiMlCoD1/+zJg3w9C8zV8zYzWjNacQ/SA+e63xzVCCL81ozSF8xVKV6w0WPeVdzsQiVd8+QS+XHgN5MtH9zOF7U8nbg/j4wSRA7a0D4Z6JBUWgO2HQXvkd5iDqNvl4nc1ELUw/xiC0FybUT1XAVEDNNl1wPD6zAtt1loB4TUvFL8KCC9w/Y/h7c2+2gdDiCl5ghB53i8EB2t0bcZcX9fZl9f2Qb9O5ZxnhPCbc0/nGWH0QuSuEWa/1uJyQNTAjPIroGvKV5F7Xr9DVif0Qu5TA8mTzOuz/Wef1isvxF200szB6FGvXbimIkQP6L9v3MNemD0QXPU4F7pPRWkOiD4wonXhpwaigit+9gTaQDzZZy4HMeHqheCBKrUcGN6pAJPmvaywmT8WQOv3QTWA0BqRFjBqz1wrlW+XMPbdGjdCG8hGv+hfPoFrIL984I8u1z4Ywvio6RFWrBqIV1RNnAOiH4xYa5S7xghRI80BMyfNNULlOcQpYF2bvWdr9VCceazJp3CeUfwqIPYHXB8Mb2/2Nf3Igj4tYNgu0H6BQl8Ppi8kEL1c6rvIubByEDUwo/w5XLvC7Hu0hriW+2Q/hAYjrjzmILzuJ5wGYvOFrzmBNhBNZxV5W1XPmtYQE4f5g1etVa6aHBD1mdutVa9Y6eIVEP1gj7UeutcaBLfLzQt13V1IfxRtII+Ml/47J9D+uFgvB+NdkXVYa/nOgNEDY5775Tqt4bEXZo9qFTBq4hSra2aurmHsY129algzQtRCR9fYs8LrCVmdygu56XMIxES9J09VWDnnRohawNQpqqfCJuB4F+f8swhRr54K10PwzoUQHIyoOod8CudGcQrotcoVEFz1SnsmrifkmVP6Rc8LBvKLr+7/8FIPBwLxCALt5QHHjxY/lsZmOFlA1ALNBRz9TDzTz54V1j6f8UDsBXCbY29AQwu5rzkjhN+5EGYu88D1p5Pbm31Nb3vz1OvaezfvHNaTt75DiLraz34IHTDV7lLgWDfhvoCZu9OHD0KDQPE5YM1nz26f8lgzilM4zyg+R9Ye/sjKhdf6509gGgjs7xQIDQK9PU/YubByNX/G4xohjNdUvQKCB5Sehvo4bASOJ6jy0lec+FVA9KkaBA9UaZlPA1m6LvLXTqB9MPTdYASOOwc6WjNCaN6teaG5itIcVas5RH+gSi13r4xN/FhYA9prMvdhaWBe2MiygN4HYi2/AsY8l0JomdMaggeud1m3N/u6fmS960CgPzbQ/z8j7xdGjzUI3nlGCA1mtA9mDbB8oH4c5DjI+z/A8WMIOt7p4xuCO5L7P6t6czB67/bWt3qcZ5T/Udh/5ruekLPTeYE2fTD0HiDuGE/1DF2zwmfqdp5Vv69wEK9lVQuheQ8QOTDZ7ZmEOwEcT9R9eXxD5K4RQnAQeBjv/0hzXE/I/UDe6Xv7ttcTg5gm0PYNHHcDBFqAyAFTzWcCmDhrFb0H4ZkmPUf1Ood+bYh11ZwL3RMee+VXuEbrXZx5ridkd2ov4ttAIO4CGHG1L0/YaI9zobmK0hzW4PE1n/FC9LHX1/kqQvRzPaxz6O9KYfR4L0L30ToHRA1wfTC8vdlXe5fl6RnP9gkx0eqB4KFj7Qddg1jXPs4hdOhozQizBp2DvnaNEDoPfS2tBoReX0v2QXjMQeQwoz0rbD+yVuLF/f4JXAM5PfPfF9vb3nppP54Z7THnfIX2QDyy9pgXrrgdb69Rvl1Uj3OIvUD/JWxthe5fNYg+mbe3YvZ4DWN9rrmeEJ/Sm2D7pQ4xNXge62vIk64azH3t33krv8qh9606hFb5sxyiBjru9rnqA1G30tynYvZeT0g+jTdYt4HUqZ3lu31D3B3QsXpzX2vQ/YDp9icW6FwTPxarfh/SU+D6MzNw7MWes5ozzfUVIfoD1wfD25t9tSfE+4I+LRjX9jyDvlOMroHe09wOXZvRXuh9YFzb47qai4eoWWnSFdaeQYh+MGKuhdAyp7Wu5ZgGIsMVrzuBayCvO/vllb9lIH7c8hUgHk8ItCdj9ue1PZnbre0VVg+M14bI4bkPhrWfc4g+uqbDmnHHS4eo17rGtwykNr3yr5/Atw7Ed4XwmS3BeKeoTgHBw4zP9LVHvRTOM8LY2xp03px6KHa5+WdRvRQr/7cOZHWBi/vcCUwD0eR28ZnWtQf0Ow9ivfM8cx3XQvQCWlnVLJjPaA0YPvyJtw9Cgz3aa4Twqs9nYhrIZ4ov7/efQBsIxEThMe62Ab3WHgjOue8gIYQGgeJyuEZoXusc5oWZz2uI/tDRuupymBdC+LVWZF9dS89R9Zxnn9YQ1wGuP53c3uyrPSFvtq9/djv/AwAA///A40XTAAAABklEQVQDAINVjZKz1YqOAAAAAElFTkSuQmCC)

手机扫码阅读
